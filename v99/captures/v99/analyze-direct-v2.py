import json
import re
import runpy
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
SHARED=runpy.run_path(str(BASE/'numeric-context-v1.py'))
Context,classify=SHARED['Context'],SHARED['classify']


def analyze(attempt,asset,manifest):
    c=Context(attempt,asset)
    if not c.session:return c.report()
    cases=[x for x in manifest['comparisonCases'] if x['sourceId']==asset['sourceId']]
    calibration={}
    source=(ROOT/asset['path']).read_text()
    for line in source.splitlines():
        m=re.search(r'plot\(f_code\((#[A-Fa-f0-9]+) == (#[A-Fa-f0-9]+)\), title="(LIT_[^"]+)"',line)
        if m:calibration[m[3]]=int(m[1]==m[2])
    for n in c.selected:
        row=c.row(n);row['cases']=[]
        c.compare(row,'SAME_SOURCE_LITERAL_CALIBRATION_GRAPH',calibration,cause='Core graph is complete for its four literals; edge graphs are only the explicitly queried local self/adjacent pairs. No cross-source calibration borrowing.')
        for route in ['RGB','NEW']:
            combined={}
            for case in cases:
                prefix=route+'_'+case['caseId']
                flags=[prefix+'_EQ_'+token[-2:] for token in case['comparedSourceLiterals']]
                codes=[c.value(n,t) for t in flags]
                matching=[token for token,code in zip(case['comparedSourceLiterals'],codes) if code==1]
                outcome='UNDECIDED / exact ownership unavailable' if not all(t in c.owned for t in flags) else 'BOOLEAN_NA_EQUALITY' if -1 in codes else 'UNEXPECTED_OR_UNAVAILABLE_CODE' if any(v not in [0,1] for v in codes) else 'NEITHER_LITERAL' if not matching else 'MULTIPLE_LITERAL_MATCHES' if len(matching)>1 else 'SINGLE_LITERAL_MATCH'
                row['cases'].append(dict(route=route,caseId=case['caseId'],transparencyRaw=case['transparencyRaw'],actualEqualityCells=[c.point(n,t) for t in flags],getterAndPredicateTargets=[c.point(n,prefix+'_'+channel) for channel in ['R','G','B','T','NA'] if prefix+'_'+channel in c.owned],equalityObservation=outcome,matchingSourceLiterals=matching,calibrationCells=[c.point(n,t) for t in calibration],calibrationScope='Complete core four-literal graph' if 'core' in asset['sourceId'] else 'Partial local self/adjacent graph; nonadjacent/global identity UNOBSERVED',getterPolicy='Actual native targets only; no T prediction inferred from comparison alpha'))
                for policy,prediction in case['comparisonPolicyPredictions'].items():
                    expected={prefix+'_EQ_'+token[-2:]:v for token,v in prediction['literalCodes'].items()}
                    c.compare(row,route+'/'+case['caseId']+'/'+policy,expected,list(calibration),applies=len(c.selected)==64,cause='Frozen comparison flags only. Neither ordinary literal calibration nor getter outputs filter native rows.')
                    combined.setdefault(policy,{}).update(expected)
            for policy,predictions in combined.items():
                c.compare(row,route+'/SOURCE_QUERY_VECTOR/'+policy,predictions,list(calibration),applies=len(c.selected)==64)
    report=c.report();report['routePolicyAdjudications']={route:classify({p['model'].rsplit('/',1)[1]:p['verdict'] for p in report['propertyVerdicts'] if p['model'].startswith(route+'/SOURCE_QUERY_VECTOR/')}) for route in ['RGB','NEW']}
    report['immediateComparisonContext']='Every constructor/comparator is immediate in its own Boolean plot expression; no switch/series/getter-route substitution'
    return report
