"""Propose ONE point from completed observations; never launch a simulation.

Requires numpy/scipy/scikit-learn in the science interpreter. The EDA adapter
may run in a different interpreter. Models are refit after each new result.
"""
import argparse
import json
import math
import warnings
from pathlib import Path
import numpy as np
from scipy.special import ndtr
from sklearn.exceptions import ConvergenceWarning
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern
from iterate_params import load_state, summarize
from search_params import prepare, snap, number


def limits(spec):
    return (min(spec['values']),max(spec['values'])) if 'values' in spec else (spec['min'],spec['max'])


def suggest(output, pool_size=512, seed=7, initial_points=None, noise_variance=1e-6):
    config,rows=load_state(output)
    domains,baseline,budget=prepare(config)
    status=summarize(output)['status']
    if status in ('validated','validation_failed','needs_validation','no_feasible_candidate'):
        raise ValueError('no remaining search evaluation; inspect or independently validate')
    if not rows:
        return {'parameters':baseline,'based_on_evaluations':0,'strategy':'baseline',
                'rationale':'Measure the configured baseline before any optimization.'}
    if not 16<=pool_size<=10000:raise ValueError('pool_size must be 16..10000')
    if not 0<noise_variance<=1:raise ValueError('noise_variance must be positive and at most 1 in normalized output units')
    names=list(domains)
    low=np.array([limits(domains[k])[0] for k in names])
    high=np.array([limits(domains[k])[1] for k in names])
    span=np.where(high>low,high-low,1)
    def vector(parameters):return (np.array([parameters[k] for k in names])-low)/span
    seen={tuple(r['parameters'][k] for k in names) for r in rows}
    rng=np.random.default_rng(seed)
    pool={}
    for _ in range(pool_size*5):
        candidate={k:float(snap(float(rng.uniform(*limits(spec))),spec)) for k,spec in domains.items()}
        key=tuple(candidate[k] for k in names)
        if key not in seen:pool[key]=candidate
        if len(pool)>=pool_size:break
    if not pool:raise ValueError('no untested legal candidates found; finite domain may be exhausted')
    candidates=list(pool.values())
    points=np.stack([vector(p) for p in candidates])
    valid=[r for r in rows if r.get('valid') and r['phase']!='independent_validation']
    minimum=initial_points if initial_points is not None else min(8,max(3,2*len(names)+1))
    if not isinstance(minimum,int) or minimum<2:raise ValueError('initial_points must be an integer >=2')
    if budget<minimum+2:
        raise ValueError('Bayesian mode needs initial_points + one BO trial + independent validation; use agent mode for this budget')
    if len(valid)<minimum:
        observed=np.stack([vector(r['parameters']) for r in rows])
        distances=((points[:,None,:]-observed[None,:,:])**2).sum(axis=2).min(axis=1)
        index=int(np.argmax(distances))
        return {'parameters':candidates[index],'based_on_evaluations':len(rows),'strategy':'initial_maximin',
                'rationale':'Add one separated legal point to the small initial design; no GP fit claimed yet.',
                'model':{'valid_observations':len(valid),'initial_points_required':minimum}}
    training=np.stack([vector(r['parameters']) for r in valid])
    required={config['objective']['metric']}|{c['metric'] for c in config.get('constraints',[])}
    predicted={}
    for metric in sorted(required):
        targets=np.array([number(r['result']['metrics'][metric],metric) for r in valid])
        kernel=ConstantKernel(1,(.01,100))*Matern(length_scale=np.full(len(names),.3),length_scale_bounds=(.03,3),nu=2.5)
        gp=GaussianProcessRegressor(kernel=kernel,alpha=noise_variance,normalize_y=True,
                                   n_restarts_optimizer=1,random_state=seed)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',ConvergenceWarning)
            gp.fit(training,targets)
        mean,std=gp.predict(points,return_std=True)
        predicted[metric]=(mean,np.maximum(std,1e-12),str(gp.kernel_))
    constraints={}
    for c in config.get('constraints',[]):
        bound=constraints.setdefault(c['metric'],[-math.inf,math.inf])
        bound[0]=max(bound[0],c.get('min',-math.inf))
        bound[1]=min(bound[1],c.get('max',math.inf))
    log_probability=np.zeros(len(points))
    for metric,(lower,upper) in constraints.items():
        if lower>upper:raise ValueError('contradictory constraints for '+metric)
        mean,std,_=predicted[metric]
        a,b=(lower-mean)/std,(upper-mean)/std
        probability=np.where(a>0,ndtr(-a)-ndtr(-b),ndtr(b)-ndtr(a))
        log_probability+=np.log(np.maximum(probability,1e-300))
    objective=config['objective']
    mean,std,_=predicted[objective['metric']]
    sign=1 if objective['goal']=='max' else -1
    feasible=[r for r in valid if r['feasible']]
    if feasible:
        incumbent=max(sign*r['result']['metrics'][objective['metric']] for r in feasible)
        improvement=sign*mean-incumbent
        z=improvement/std
        expected=improvement*ndtr(z)+std*np.exp(-.5*z*z)/math.sqrt(2*math.pi)
        score=np.log(np.maximum(expected,1e-300))+log_probability
        strategy='gp_constrained_expected_improvement'
    else:
        # Seek feasibility first; uncertainty breaks ties in tiny probabilities.
        score=log_probability+.01*std/max(float(np.max(std)),1e-12)
        strategy='gp_feasibility_first'
    if not np.all(np.isfinite(score)):raise ValueError('non-finite acquisition score')
    index=int(np.argmax(score))
    predictions={metric:{'mean':float(m[index]),'std':float(s[index]),'kernel':kernel}
                 for metric,(m,s,kernel) in predicted.items()}
    return {'parameters':candidates[index],'based_on_evaluations':len(rows),'strategy':strategy,
            'rationale':'Refit GP models to all completed valid results; select one legal untested point by feasibility and expected improvement.',
            'predicted_metrics':predictions,
            'model':{'valid_observations':len(valid),'candidates_scored_without_simulation':len(points),
                     'estimated_probability_feasible':float(np.exp(log_probability[index])),
                     'acquisition_score':float(score[index]),'seed':seed,'independent_metric_models':True,
                     'predictions_are_not_measurements':True}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('state_dir',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--pool-size',type=int,default=512)
    parser.add_argument('--seed',type=int,default=7)
    parser.add_argument('--initial-points',type=int)
    parser.add_argument('--noise-variance',type=float,default=1e-6)
    args=parser.parse_args()
    proposal=suggest(args.state_dir,args.pool_size,args.seed,args.initial_points,args.noise_variance)
    with args.output.open('x',encoding='utf-8') as handle:
        json.dump(proposal,handle,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps(proposal,ensure_ascii=True,indent=2))


if __name__=='__main__':main()
