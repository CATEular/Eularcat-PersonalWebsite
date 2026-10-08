"""Extract one AC bandwidth from exact PSF in an isolated OCEAN process.

Uses the locally installed bridge v0.7 SSH transport (private runner interface).
Does not launch a simulation or modify a schematic; the caller supplies exact PSF.
"""
import argparse
import importlib.util
import json
import math
import re
import shlex
import uuid
from pathlib import Path, PurePosixPath

CONFIG_SOURCE = Path(__file__).resolve().parents[2] / 'virtuoso-connect/scripts/workflow_config.py'
config_spec = importlib.util.spec_from_file_location('virtuoso_workflow_config', CONFIG_SOURCE)
workflow_config = importlib.util.module_from_spec(config_spec)
config_spec.loader.exec_module(workflow_config)

def configured_ocean_bin(config_path=None):
    config = workflow_config.load_config(config_path)
    return absolute_remote_path(workflow_config.require(config, 'remote.executables.ocean'))


def skill_string(value):
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def absolute_remote_path(value):
    if not isinstance(value, str) or not re.fullmatch(r'/[A-Za-z0-9_./-]+', value):
        raise ValueError('remote path must be an absolute POSIX path with plain characters')
    if '..' in PurePosixPath(value).parts:
        raise ValueError('parent traversal is not allowed')
    return value.rstrip('/')


def extract_ac_bandwidth(client, psf_dir, remote_root, output_dir, node='/OUT', timeout=45,
                         ocean_bin=None):
    psf_dir = absolute_remote_path(psf_dir)
    remote_root = absolute_remote_path(remote_root)
    ocean_bin = absolute_remote_path(ocean_bin) if ocean_bin is not None else configured_ocean_bin()
    if not re.fullmatch(r'(/[A-Za-z_][A-Za-z0-9_!<>-]*)+', node):
        raise ValueError('unsupported signal path')
    if not 5 <= timeout <= 300:
        raise ValueError('timeout must be between 5 and 300 seconds')
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=False)
    if not client.test_connection():
        raise RuntimeError('bridge connection unavailable')
    runner = client._tunnel._ssh_runner
    remote_run = remote_root + '/run_' + uuid.uuid4().hex

    def command(text, limit=20):
        result = runner.run_command(text, timeout=limit)
        if result.returncode:
            raise RuntimeError(f'remote command failed ({result.returncode}): {result.stderr[-500:]}')
        return result

    command('test -d ' + shlex.quote(psf_dir))
    command('mkdir -p ' + shlex.quote(remote_root))
    command('mkdir ' + shlex.quote(remote_run))
    metric_path = remote_run + '/metric.json'
    script_path = remote_run + '/measure.ocn'
    script = '\n'.join([
        '; Generated locally. Read exactly one saved AC point; main CIW untouched.',
        f'unless(openResults({skill_string(psf_dir)}) error("Cannot open exact PSF"))',
        'unless(selectResult(\'ac) error("Missing AC result"))',
        f'cwWave = getData({skill_string(node)} ?result "ac")',
        'unless(cwWave error("Missing output waveform"))',
        'cwBW = bandwidth(mag(cwWave) 3 "low")',
        'unless(numberp(cwBW) && cwBW>0 error("Invalid bandwidth"))',
        f'cwPort = outfile({skill_string(metric_path)})',
        'fprintf(cwPort "{\\\"ok\\\":true,\\\"metrics\\\":{\\\"bandwidth_hz\\\":%.17g}}\\n" cwBW)',
        'close(cwPort)',
        'exit()',
        '',
    ])
    local_script = output_dir / 'measure.ocn'
    local_script.write_text(script, encoding='utf-8')
    transfer = client.upload_file(local_script, script_path)
    if not transfer.ok:
        raise RuntimeError(str(transfer))
    launch = (f'timeout --signal=TERM --kill-after=5s {timeout}s {shlex.quote(ocean_bin)} '
              f'-nograph -restore {shlex.quote(script_path)} -log {shlex.quote(remote_run + "/ocean.log")} '
              f'> {shlex.quote(remote_run + "/console.log")} 2>&1')
    # The remote timeout owns only this foreground child process group.
    execution = runner.run_command(launch, timeout=timeout + 10)
    for name in ['console.log', 'ocean.log']:
        transfer = client.download_file(remote_run + '/' + name, output_dir / name)
        if not transfer.ok:
            (output_dir / (name + '.missing.txt')).write_text(str(transfer), encoding='utf-8')
    if execution.returncode:
        raise RuntimeError(f'OCEAN failed or timed out: rc={execution.returncode}; see {output_dir}')
    transfer = client.download_file(metric_path, output_dir / 'metric.json')
    if not transfer.ok:
        raise RuntimeError('OCEAN did not produce fresh metric JSON: ' + str(transfer))
    result = json.loads((output_dir / 'metric.json').read_text(encoding='utf-8'))
    value = result.get('metrics', {}).get('bandwidth_hz')
    if result.get('ok') is not True or not isinstance(value, (float, int)) or not math.isfinite(value) or value <= 0:
        raise ValueError('invalid OCEAN metric')
    result['evidence'] = {'psf_dir': psf_dir, 'node': node, 'remote_run': remote_run,
                          'backend': 'isolated_ocean_ac', 'script': str(local_script)}
    (output_dir / 'result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--psf-dir', required=True)
    parser.add_argument('--remote-root', required=True, help='authorized remote workspace for this worker')
    parser.add_argument('--output-dir', type=Path, required=True, help='new local result directory')
    parser.add_argument('--node', default='/OUT')
    parser.add_argument('--timeout', type=int, default=45)
    parser.add_argument('--ocean-bin', help='override the configured remote OCEAN executable')
    parser.add_argument('--config', type=Path, help='override the shared local workflow config')
    args = parser.parse_args()
    config = workflow_config.load_config(args.config)
    ocean_bin = args.ocean_bin or workflow_config.require(config, 'remote.executables.ocean')
    result = extract_ac_bandwidth(workflow_config.make_client(config, timeout=30), args.psf_dir,
                                 args.remote_root, args.output_dir, args.node, args.timeout, ocean_bin)
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
