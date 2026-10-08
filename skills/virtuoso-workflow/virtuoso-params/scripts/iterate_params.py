"""One real evaluation per call, with decisions supplied by the current agent.

No candidate loop, Cartesian sweep, or external LLM client is hidden here.
"""
import argparse
import json
import math
import os
import uuid
from pathlib import Path
from search_params import prepare, snap, number, assess, load_adapter


def write_json(path, data):
    path=Path(path)
    temporary=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    temporary.replace(path)


def initialize(config, output):
    prepare(config)
    output=Path(output)
    output.mkdir(parents=True,exist_ok=False)
    write_json(output/'config.json',config)
    return summarize(output)


def load_state(output):
    output=Path(output)
    config=json.loads((output/'config.json').read_text(encoding='utf-8'))
    config.setdefault('max_evals',20)
    prepare(config)
    rows=[]
    for folder in sorted(output.glob('run_[0-9][0-9][0-9][0-9]')):
        record=folder/'record.json'
        if not record.is_file():
            raise RuntimeError(f'Unfinished evaluation at {folder}; inspect its remote job before recovery')
        row=json.loads(record.read_text(encoding='utf-8'))
        if row['evaluation']!=len(rows)+1:raise ValueError('non-contiguous evaluation history')
        rows.append(row)
    return config,rows


def summarize(output):
    config,rows=load_state(output)
    valid=[r for r in rows if r.get('valid') and r['phase']!='independent_validation']
    best=min(valid,key=lambda r:tuple(r['rank'])) if valid else None
    validation=next((r for r in rows if r['phase']=='independent_validation'),None)
    if validation:
        status='validated' if validation['valid'] and validation['feasible'] else 'validation_failed'
    elif len(rows)>=config['max_evals']-1:
        status='needs_validation' if best and best['feasible'] else 'no_feasible_candidate'
    else:
        status='needs_agent_analysis' if rows else 'needs_baseline'
    result={'status':status,'evaluations':len(rows),'budget':config['max_evals'],
            'remaining_search_evaluations':max(0,config['max_evals']-1-len(rows)),
            'baseline':rows[0] if rows else None,'latest':rows[-1] if rows else None,
            'best_search_candidate':best,'independent_validation':validation,
            'global_optimum_proven':False}
    if len(rows)>=2 and rows[-1]['valid'] and rows[-2]['valid']:
        before,after=(r['result']['metrics'] for r in rows[-2:])
        result['metric_changes_from_previous']={k:after[k]-before[k] for k in after
            if k in before and isinstance(after[k],(int,float)) and not isinstance(after[k],bool)
            and isinstance(before[k],(int,float)) and math.isfinite(after[k]) and math.isfinite(before[k])}
    return result


def evaluate_step(output, proposal, evaluate, validation=False):
    output=Path(output)
    lock=output/'.iteration.lock'
    descriptor=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    os.close(descriptor)
    try:
        config,rows=load_state(output)
        domains,baseline,budget=prepare(config)
        if len(rows)>=budget or any(r['phase']=='independent_validation' for r in rows):
            raise ValueError('session is finished; do not launch another simulation')
        if validation:
            best=summarize(output)['best_search_candidate']
            if not best or not best['feasible']:raise ValueError('no feasible candidate to validate')
            proposal={'parameters':best['parameters'],'based_on_evaluations':len(rows),
                      'rationale':'Independently rerun the best measured feasible candidate.',
                      'strategy':'independent_validation'}
        elif len(rows)>=budget-1:
            raise ValueError('search budget exhausted; the last evaluation is reserved for validation')
        if proposal.get('based_on_evaluations')!=len(rows) or isinstance(proposal.get('based_on_evaluations'),bool):
            raise ValueError('stale proposal; analyze the current history before deciding again')
        if not isinstance(proposal.get('rationale'),str) or not proposal['rationale'].strip():
            raise ValueError('a decision rationale is required')
        parameters=proposal['parameters']
        if set(parameters)!=set(domains):raise ValueError('candidate must specify every configured parameter')
        clean={}
        for name,spec in domains.items():
            value=number(parameters[name],name)
            legal=snap(value,spec)
            if not math.isclose(value,legal,rel_tol=1e-12,abs_tol=1e-15):
                raise ValueError(f'illegal parameter {name}: {value}')
            clean[name]=legal
        if not rows and clean!=baseline:raise ValueError('first evaluation must be the baseline')
        if not validation and any(r['parameters']==clean for r in rows):
            raise ValueError('candidate already evaluated; choose a new point or independently validate')
        index=len(rows)+1
        folder=output/f'run_{index:04d}'
        folder.mkdir(exist_ok=False)
        row={'evaluation':index,'phase':'independent_validation' if validation else 'baseline' if not rows else 'agent_iteration',
             'parameters':clean,'decision':proposal}
        write_json(folder/'attempt.json',row)
        try:
            result=evaluate(dict(clean),folder)
            json.dumps(result,allow_nan=False)
            rank,feasible=assess(result,config)
            row.update(valid=True,feasible=feasible,rank=list(rank),result=result)
        except Exception as exc:
            row.update(valid=False,feasible=False,error=f'{type(exc).__name__}: {exc}')
        write_json(folder/'record.json',row)
        result=summarize(output)
        write_json(output/'summary.json',result)
        return result
    finally:
        # This is our own short-lived workflow lock, never a Cadence design lock.
        lock.unlink()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    init=commands.add_parser('init');init.add_argument('config',type=Path);init.add_argument('--output',type=Path,required=True)
    show=commands.add_parser('inspect');show.add_argument('output',type=Path)
    step=commands.add_parser('step');step.add_argument('output',type=Path);step.add_argument('--proposal',type=Path,required=True);step.add_argument('--adapter',type=Path,required=True)
    check=commands.add_parser('validate');check.add_argument('output',type=Path);check.add_argument('--adapter',type=Path,required=True)
    args=parser.parse_args()
    if args.command=='init':result=initialize(json.loads(args.config.read_text(encoding='utf-8')),args.output)
    elif args.command=='inspect':result=summarize(args.output)
    elif args.command=='step':result=evaluate_step(args.output,json.loads(args.proposal.read_text(encoding='utf-8')),load_adapter(args.adapter))
    else:result=evaluate_step(args.output,None,load_adapter(args.adapter),validation=True)
    print(json.dumps(result,ensure_ascii=True,indent=2,allow_nan=False))


if __name__=='__main__':
    main()
