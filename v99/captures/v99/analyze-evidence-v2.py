import json
import runpy
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
SHARED=runpy.run_path(str(BASE/'numeric-context-v1.py'))
classify=SHARED['classify']


def analyze(revision=1):
    inventory=json.loads((BASE/f'attempt-inventory-v{revision}.json').read_text())
    manifest=json.loads((ROOT/'v99/bundle-manifest-v1.json').read_text())
    reused=runpy.run_path(str(BASE/'analyze-reused-v1.py'))['analyze'](revision)['sources']
    reports=[]
    for attempt in inventory['attempts']:
        asset=next(a for a in manifest['sources'] if a['sourceId']==attempt['source']['sourceId'])
        if asset['reusedUnchanged']:
            report=next(r for r in reused if r['sourceId']==asset['sourceId'])
            for row in report['rows']:
                for route in row.get('routes',[]):route['policyAdjudication']=classify({c['model'].split('/',1)[1]:c['verdict'] for c in row['comparisons'] if c['model'].startswith(route['route']+'/')})
            report['routePolicyAdjudications']={route:classify({p['model'].split('/',1)[1]:p['verdict'] for p in report['propertyVerdicts'] if p['model'].startswith(route+'/')}) for route in ['LITERAL_RGB','LITERAL_NEW','SERIES_RGB','SERIES_NEW']}
            report['scope']='New v99 private source execution of unchanged v98 source; original v98 four models only. Old consumed v98 slot stays held.'
        elif asset['item']==1:
            report=runpy.run_path(str(BASE/'analyze-direct-v2.py'))['analyze'](attempt,asset,manifest)
        elif asset['sourceId']=='v99-array-self-v6':
            report=runpy.run_path(str(BASE/'analyze-minimal-v2.py'))['analyze'](attempt,asset)
        else:
            report=runpy.run_path(str(BASE/'analyze-identity-v2.py'))['analyze'](attempt,asset)
        reports.append(report)
    combined={}
    for route in ['RGB','NEW']:
        verdicts={};certificates=[]
        for policy in [p for p in manifest['comparisonPolicies'] if p!='scope']:
            matching=[]
            for sourceid in ['v99-direct-colors-core-v5','v99-direct-colors-edge-v5']:
                source=next((s for s in reports if s['sourceId']==sourceid),None)
                record=next((p for p in source['propertyVerdicts'] if p['model']==route+'/SOURCE_QUERY_VECTOR/'+policy),None) if source else None
                complete=source is not None and len(source.get('selectedDataRowOrdinals',[]))==64 and record is not None
                matching.append(record['verdict'] if complete else 'UNDECIDED')
                certificates.append(dict(model=policy,sourceId=sourceid,coverageComplete=complete,propertyVerdict=record,sourceCsv=source.get('csv') if source else None,actualNativeTargetCells=[p for row in source['rows'] for c in row['comparisons'] if c['model']==route+'/SOURCE_QUERY_VECTOR/'+policy for p in c['nativeCells']] if source else []))
            verdicts[policy]='UNDECIDED' if 'UNDECIDED' in matching else 'REFUTED' if 'REFUTED' in matching else 'SUPPORTED'
        combined[route]=dict(classify(verdicts),sourceCertificates=certificates,scope='Complete six-case finite-query vector across two separately owned fixed programs; no row/session stitching, cross-source calibration or getter/hidden-byte prediction')
    return dict(version=f'v{revision}',requestCommit=inventory['requestCommit'],sources=reports,sixCaseDirectComparisonPolicies=combined,selectionPolicy=manifest['primarySelection'],pointerCountsAreNotUniqueCells=True,historicalHolds='UNCHANGED; no engine approval/fixture promotion/universal identity or storage model')
