"""Read exact transient PSF using an isolated OCEAN worker; never simulates."""
import csv
import importlib.util
import json
import math
from pathlib import Path
import shlex
import uuid

SOURCE = Path(__file__).resolve().with_name('ocean_ac_metric.py')
spec = importlib.util.spec_from_file_location('ocean_common', SOURCE)
common = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common)


def _read_wave(path):
    with Path(path).open(newline='', encoding='utf-8') as handle:
        rows = [(float(row['time_s']), float(row['value'])) for row in csv.DictReader(handle)]
    if len(rows) < 10 or any(not math.isfinite(x) or not math.isfinite(y) for x, y in rows):
        raise ValueError('missing or invalid raw transient wave')
    if any(b[0] <= a[0] for a, b in zip(rows, rows[1:])):
        raise ValueError('transient time must increase strictly')
    return rows


def _window(rows, start, stop):
    def value_at(t):
        for a, b in zip(rows, rows[1:]):
            if a[0] <= t <= b[0]:
                return a[1] + (b[1] - a[1]) * (t - a[0]) / (b[0] - a[0])
        raise ValueError('requested measurement window not covered by transient')
    return [(start, value_at(start))] + [(t,v) for t,v in rows if start<t<stop] + [(stop,value_at(stop))]


def extract_osc_metrics(client, psf_dir, remote_root, output_dir,
                        node='/OUT', current='/VDD_SOURCE/PLUS', start=100e-9, stop=500e-9,
                        supply=1.8, timeout=45, target_frequency=100e6, ocean_bin=None):
    psf_dir = common.absolute_remote_path(psf_dir)
    remote_root = common.absolute_remote_path(remote_root)
    ocean_bin = common.absolute_remote_path(ocean_bin) if ocean_bin is not None else common.configured_ocean_bin()
    import re
    if not all(re.fullmatch(r'(/[A-Za-z_][A-Za-z0-9_!<>-]*)+', path) for path in (node,current)):
        raise ValueError('unsupported voltage/current signal path')
    if not 5 <= timeout <= 300:
        raise ValueError('timeout must be between 5 and 300 seconds')
    if not all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in (start,stop,supply,target_frequency)):
        raise ValueError('measurement values must be finite numbers')
    if not 0 <= start < stop or supply <= 0 or target_frequency <= 0:
        raise ValueError('invalid time window, supply or target frequency')
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=False)
    if not client.test_connection():
        raise RuntimeError('bridge unavailable')
    runner = client._tunnel._ssh_runner
    remote_run = remote_root + '/osc_' + uuid.uuid4().hex
    for command in ['test -d '+shlex.quote(psf_dir), 'mkdir -p '+shlex.quote(remote_root), 'mkdir '+shlex.quote(remote_run)]:
        execution = runner.run_command(command, timeout=20)
        if execution.returncode:
            raise RuntimeError(execution.stderr)
    q = common.skill_string
    script = f'''unless(openResults({q(psf_dir)}) error("Cannot open exact PSF"))
unless(selectResult('tran) error("Missing transient result"))
cwVoltage = v({q(node)} ?result 'tran)
cwCurrent = i({q(current)} ?result 'tran)
unless(cwVoltage && cwCurrent error("Missing saved voltage or supply current"))
procedure(cwWriteWave(wave path)
  let((xx yy port)
    xx=drGetWaveformXVec(wave)
    yy=drGetWaveformYVec(wave)
    port=outfile(path)
    fprintf(port "time_s,value\\n")
    for(k 0 drVectorLength(xx)-1
      fprintf(port "%.17g,%.17g\\n" drGetElem(xx k) drGetElem(yy k)))
    close(port)))
cwWriteWave(cwVoltage {q(remote_run+'/voltage.csv')})
cwWriteWave(cwCurrent {q(remote_run+'/current.csv')})
cwStable=clip(cwVoltage {start:.17g} {stop:.17g})
cwCurrentStable=clip(cwCurrent {start:.17g} {stop:.17g})
cwFirst=cross(cwStable {supply/2:.17g} 1 "rising" nil nil)
cwSecond=cross(cwStable {supply/2:.17g} 2 "rising" nil nil)
unless(numberp(cwFirst) && numberp(cwSecond) && cwSecond>cwFirst error("No stable oscillation"))
cwFrequency=1.0/(cwSecond-cwFirst)
cwVpp=ymax(cwStable)-ymin(cwStable)
cwPower=-{supply:.17g}*average(cwCurrentStable)
cwPort=outfile({q(remote_run+'/metric.json')})
fprintf(cwPort "{{\\\"ok\\\":true,\\\"metrics\\\":{{\\\"frequency_hz\\\":%.17g,\\\"vpp_v\\\":%.17g,\\\"power_w\\\":%.17g}}}}\\n" cwFrequency cwVpp cwPower)
close(cwPort)
exit()
'''
    (output_dir/'measure.ocn').write_text(script, encoding='utf-8')
    transfer=client.upload_file(output_dir/'measure.ocn',remote_run+'/measure.ocn')
    if not transfer.ok:
        raise RuntimeError(str(transfer))
    command=(f'timeout --signal=TERM --kill-after=5s {timeout}s {shlex.quote(ocean_bin)} '
             f'-nograph -restore {shlex.quote(remote_run+"/measure.ocn")} -log {shlex.quote(remote_run+"/ocean.log")} '
             f'> {shlex.quote(remote_run+"/console.log")} 2>&1')
    execution=runner.run_command(command,timeout=timeout+10)
    for name in ['console.log','ocean.log','voltage.csv','current.csv','metric.json']:
        transfer=client.download_file(remote_run+'/'+name,output_dir/name)
        if not transfer.ok:
            (output_dir/(name+'.missing.txt')).write_text(str(transfer),encoding='utf-8')
    if execution.returncode or not (output_dir/'metric.json').is_file():
        raise RuntimeError(f'Isolated OCEAN failed rc={execution.returncode}; inspect {output_dir}')
    result=json.loads((output_dir/'metric.json').read_text(encoding='utf-8'))
    stable=_window(_read_wave(output_dir/'voltage.csv'),start,stop)
    current_wave=_window(_read_wave(output_dir/'current.csv'),start,stop)
    crossings=[]
    for a,b in zip(stable,stable[1:]):
        if a[1]<supply/2<=b[1]:
            crossings.append(a[0]+(supply/2-a[1])*(b[0]-a[0])/(b[1]-a[1]))
    if len(crossings)<3:
        raise ValueError('fewer than two complete stable oscillation periods')
    average_frequency=(len(crossings)-1)/(crossings[-1]-crossings[0])
    integrated_power=-supply*sum((b[0]-a[0])*(a[1]+b[1])/2 for a,b in zip(current_wave,current_wave[1:]))/(stop-start)
    metrics=result['metrics']
    if any(not math.isfinite(v) for v in metrics.values()) or metrics['power_w']<0:
        raise ValueError('invalid OCEAN metrics or supply current sign')
    if abs(metrics['frequency_hz']/average_frequency-1)>.002:
        raise ValueError('oscillation not settled: first period and average frequency differ by >0.2%')
    if abs(metrics['power_w']-integrated_power)>max(1e-9,abs(integrated_power)*.002):
        raise ValueError('OCEAN average current disagrees with time integral')
    metrics['freq_error']=abs(metrics['frequency_hz']/target_frequency-1)
    result['evidence']={'backend':'isolated_ocean_tran','psf_dir':psf_dir,'remote_run':remote_run,
        'measurement_window_s':[start,stop],'target_frequency_hz':target_frequency,'rising_crossings':len(crossings),
        'average_frequency_hz':average_frequency,'integrated_power_w':integrated_power,
        'node':node,'current':current,'voltage_csv':str(output_dir/'voltage.csv'),
        'current_csv':str(output_dir/'current.csv'),'script':str(output_dir/'measure.ocn')}
    (output_dir/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result
