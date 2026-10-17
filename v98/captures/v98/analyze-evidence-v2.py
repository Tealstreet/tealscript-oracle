import runpy
from pathlib import Path

BASE=Path(__file__).resolve().parent
ORIGINAL=runpy.run_path(str(BASE/'analyze-evidence-v1.py'))


def classify(verdicts):
    supported=[name for name,status in verdicts.items() if status=='SUPPORTED']
    return dict(frozenModelVerdicts=verdicts,supportedFrozenModels=supported,observation='SUPPORTED_FROZEN_MODELS' if supported else 'NEITHER_MODEL' if verdicts and all(s=='REFUTED' for s in verdicts.values()) else 'UNDECIDED',hiddenStorageVerdict='UNDECIDED; bounded exported vectors and ordinary source-literal equality only')


def analyze(revision=1):
    result=ORIGINAL['analyze'](revision)
    for report in result['sources']:
        for row in report['rows']:
            if 'routes' in row:
                for route in row['routes']:
                    route['policyAdjudication']=classify({c['model'].split('/',1)[1]:c['verdict'] for c in row['comparisons'] if c['model'].startswith(route['route']+'/')})
            else:
                row['castAlternativeAdjudication']=classify({c['model']:c['verdict'] for c in row['comparisons'] if c['model'] in ['A_ORDINARY_MISSING_PROPAGATION','B_PRESENT_TRANSPARENT_BLACK','C_PRESENT_OPAQUE_BLACK','D_NON_NA_WITH_BLANK_GETTERS']})
        if report['rows'] and 'routes' in report['rows'][0]:
            report['routePolicyAdjudications']={route:classify({p['model'].split('/',1)[1]:p['verdict'] for p in report['propertyVerdicts'] if p['model'].startswith(route+'/')}) for route in ORIGINAL['ROUTES']}
    return result
