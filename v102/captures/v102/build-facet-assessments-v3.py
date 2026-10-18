import json
import runpy
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
HELPERS=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put=HELPERS['ref'],HELPERS['put']


def combine(statuses):
    if 'REFUTED' in statuses:return 'REFUTED'
    return 'SUPPORTED' if statuses and all(s=='SUPPORTED' for s in statuses) else 'UNDECIDED'


def build(source_id):
    manifest=json.loads((ROOT/'v102/bundle-manifest-v1.json').read_text());asset=next(a for a in manifest['sources'] if a['sourceId']==source_id)
    matrix_path=ROOT/'v102/CASE-MATRIX-v1.json';matrix=json.loads(matrix_path.read_text());case_index=next(i for i,c in enumerate(matrix['cases']) if c['sourceId']==source_id);spec=matrix['cases'][case_index]
    report_path=BASE/source_id/'numeric-results-v1.json';report=json.loads(report_path.read_text());report_ref=ref(report_path)
    properties={p['title']:(i,p) for i,p in enumerate(report['properties'])};alternatives={p['id']:(i,p) for i,p in enumerate(report['numericAlternatives'])}
    visual_path=BASE/source_id/'derived-region-map-v1.json';visual=json.loads(visual_path.read_text()) if visual_path.exists() else None
    visual_cases={f['caseId']:(i,f) for i,f in enumerate(visual['facets'])} if visual else {}

    addendum_path=BASE/source_id/'visual-inspection-addendum-v1.json'
    visual_artifacts={}
    if addendum_path.exists():
        addendum=json.loads(addendum_path.read_text())
        for i,item in enumerate(addendum['facets']):
            assert item['caseId'] not in visual_cases
            visual_cases[item['caseId']]=(i,item);visual_artifacts[item['caseId']]=ref(addendum_path)

    def numeric(titles):
        evidence=[]
        for title in titles:
            pair=properties.get(title)
            evidence.append(dict(title=title,verdict=pair[1]['verdict'] if pair else 'UNDECIDED',artifact=report_ref,jsonPointer='/properties/'+str(pair[0]) if pair else None,cause=None if pair else 'Requested numeric property is unavailable; no substitute value'))
        return dict(verdict=combine([e['verdict'] for e in evidence]),properties=evidence)

    def alternative(name):
        pair=alternatives.get(name)
        if pair is None:return dict(verdict='UNDECIDED',cause='No owned native numeric alternative scope available')
        i,item=pair;variants=item['variants'];status='SUPPORTED' if item['supportedVariantIds'] else 'REFUTED' if variants and all(v['verdict']=='REFUTED' for v in variants) else 'UNDECIDED'
        return dict(verdict=status,scope=name,observation=item['observation'],supportedVariantIds=item['supportedVariantIds'],artifact=report_ref,jsonPointer='/numericAlternatives/'+str(i),meaning='Support identifies only a registered finite numeric alternative; NEITHER refutes this frozen family rather than erasing its contrary native outputs')

    def appearance(case_id):
        pair=visual_cases.get(case_id)
        if pair is None:return dict(verdict='UNDECIDED',cause='No independently owned/readable/discriminating PNG region for this visual property; no getter/intent replacement')
        i,item=pair
        return dict(verdict=item['verdict'],artifact=visual_artifacts.get(case_id,ref(visual_path)),jsonPointer='/facets/'+str(i),cause=item.get('notObservedCause'),supportedCandidate=item.get('supportedCandidate'),scope='Only the bound original PNG pixels and explicit intersections/occlusions/uncertainty in this map')

    def choice(title,values):
        block=json.loads((ROOT/report['nativeBlock']['path']).read_text());variants=[]
        for name,expected in values.items():
            codes=[]
            for row in block['rows']:
                point=row['cells'].get(title)
                codes.append('U' if point is None or title not in block['ownedTitles'] else 'S' if HELPERS['number'](point['valueRaw'])==HELPERS['number'](expected) else 'R')
            status='REFUTED' if 'R' in codes else 'SUPPORTED' if block['completePrimaryCertificate'] and len(codes)==32 and all(c=='S' for c in codes) else 'UNDECIDED'
            variants.append(dict(id=name,expectedRaw=expected,verdict=status,comparisonCodes=''.join(codes)))
        supported=[v['id'] for v in variants if v['verdict']=='SUPPORTED']
        status='SUPPORTED' if supported else 'REFUTED' if all(v['verdict']=='REFUTED' for v in variants) else 'UNDECIDED'
        return dict(verdict=status,title=title,variants=variants,supportedVariantIds=supported,nativeTargets=report['nativeBlock'],basis='These exact alternatives are stated in the frozen CASE-MATRIX and request; every code resolves by row order to the original CSV pointer in the native block. No token explanation or unrelated lifecycle facet is fitted.')

    rules={
        'copy-appearance':{
            'line-copy-preserves-dash-width-color':['LINE_SOURCE_X_REL','LINE_COPY_X_REL','LINE_SOURCE_Y','LINE_COPY_Y'],
            'box-copy-preserves-style-independent-text':['BOX_SOURCE_LEFT_REL','BOX_COPY_LEFT_REL'],
            'label-copy-preserves-style-independent-text':['LABEL_SOURCE_EXACT','LABEL_COPY_EXACT']},
        'coordinate-render':{
            'line-time-index-point-copy':['LINE_TIME_X1_DELTA','LINE_POINT_X1_REL','LINE_POINT_Y1'],
            'box-point-copy-no-set_xloc-v5':['BOX_POINT_LEFT_REL','BOX_POINT_TOP'],
            'box-point-copy-and-time-index':['BOX_TIME_DELTA','BOX_POINT_LEFT_REL','BOX_POINT_TOP'],
            'label-time-index-point-copy':['LABEL_POINT_X_REL','LABEL_POINT_Y']},
        'box-text-layout':{
            'complete-short-sentinel-setter-vs-constructor':['BOX_LEFT_REL','BOX_TOP']},
        'line-price':{
            'positive-negative-exact-slopes':['LEFT_EXTRAPOLATE','ENDPOINT1','INTERPOLATE','HALF_STEP','ENDPOINT2','RIGHT_EXTRAPOLATE','DESC_LEFT','DESC_RIGHT','DESC_HALF']},
        'extend-stroke':{
            'none-left-right-both-extension':['LINE_X1_REL','LINE_Y1','BOX_LEFT_REL']}}
    numeric_only=set(rules['coordinate-render'])|{'positive-negative-exact-slopes'}
    numeric_alternatives={
        'same-position-retain-vs-replace':'table-collision-lifecycle',
        'same-pair-replace-vs-add':'same-pair-count-and-old-handle-delete',
        'old-handle-delete-new-fill-survival':'same-pair-count-and-old-handle-delete',
        'infinite-slope-vs-extend-clamping':'exterior-interpolation',
        'getter-reflects-mutated-endpoint':'mutated-slope',
        'undefined-vertical-vs-endpoint-choice-vs-runtime-refusal':'vertical-price-result'}
    decisions=[]
    for name in spec['cases']:
        case_id=source_id+':'+name;numeric_evidence=None;visual_evidence=None;admission=None
        titles=rules.get(asset['family'],{}).get(name,[])
        if titles:numeric_evidence=numeric(titles)
        if name in numeric_alternatives:numeric_evidence=alternative(numeric_alternatives[name])
        if name=='same-pair-replace-vs-add':numeric_evidence=choice('SAME_PAIR_COUNT',dict(REPLACEMENT='1',ADDITIVE='2'))
        if name=='old-handle-delete-new-fill-survival':numeric_evidence=choice('AFTER_OLD_DELETE',dict(ALIASED_G_REMOVED='0',INDEPENDENT_G_RETAINED='1'))
        if name=='sloped-both-extension-follows-endpoints':numeric_evidence=numeric(['TRACK_FIRST_Y1','TRACK_FIRST_Y2','TRACK_SECOND_Y1','TRACK_SECOND_Y2'])
        if name=='phase3-4-holes-vs-bridges':numeric_evidence=numeric(['HOLE_NA','LINE_CONTINUOUS','LINE_BREAK','AREA_CONTINUOUS','AREA_BREAK','STEP_CONTINUOUS','STEP_BREAK'])
        if name=='offset-plus-one-vs-zero':numeric_evidence=alternative('offset-export-policy')
        if name=='required-argument-refusal-vs-admission':
            source=report['sourceObservation'];body=json.loads((ROOT/source['saveBody']['path']).read_text());reason=json.dumps(dict(reason=body.get('reason'),reason2=body.get('reason2')),ensure_ascii=False)
            if body.get('success') is True:admission=dict(verdict='SUPPORTED',supportedCandidate='EXACT_OMITTED_CALL_ADMITTED',refutedCandidate='FORMATTING_ARGUMENT_REQUIRED_FOR_THIS_CALL',body=source['saveBody'],cause='Exact PRIVATE Save admission only; no execution/formatting behavior follows from Save success')
            elif body.get('success') is False:
                import re
                required=bool(re.search('format',reason,re.I) and re.search('no value assigned|missing|required|not enough arguments|too few arguments|not.*specif',reason,re.I))
                admission=dict(verdict='SUPPORTED' if required else 'UNDECIDED',supportedCandidate='REQUIREDNESS_FOR_THIS_EXACT_CALL' if required else None,body=source['saveBody'],nativeRefusal=True,nativeDiagnostic=reason,cause='Native diagnostic expressly addresses the missing formatting argument' if required else 'Exact native refusal retained, but requiredness is not inferred from a different or unavailable diagnostic')
            else:admission=dict(verdict='UNDECIDED',cause='No exact native Save admission/refusal exposed')
        elif name not in numeric_only and name not in numeric_alternatives:
            visual_evidence=appearance(case_id)
        statuses=[e['verdict'] for e in [numeric_evidence,visual_evidence,admission] if e is not None]
        decisions.append(dict(caseId=case_id,verdict=combine(statuses),numeric=numeric_evidence,visual=visual_evidence,admission=admission,scope='Named finite case only; subfacets retain their own status. Numerical getters/counts/intent never certify an unexposed visual field.',versionBoundary='This exact source/version independently owned; no v5/v6 transfer',v5BoxXlocCredit=0 if name=='box-point-copy-no-set_xloc-v5' else None,unobservedIntermediateLabelTimeTransition='No getter observes the transient label bar_time state; only final point/index fields are certified' if name=='label-time-index-point-copy' else None))
    return dict(version='v3',visualAddendum=ref(addendum_path) if addendum_path.exists() else None,sourceId=source_id,sourceSha256=asset['sha256'],matrix=ref(matrix_path),matrixPointer='/cases/'+str(case_index),numericReport=report_ref,visualMap=ref(visual_path) if visual else None,cases=decisions,held=['Any absent/unreadable/nonintersecting/already obscured/precision-ambiguous pixel region','All native backend token explanations, universal raster/font metrics and historical holds'],scope='Per-case conjunctions preserve independently scored numeric, native-admission and visual evidence. A contrary scoped property remains a refutation; missing matching coverage remains undecided, with no broad family PASS.')


if __name__=='__main__':
    value=build(sys.argv[1]);put(BASE/sys.argv[1]/'facet-assessment-v3.json',value)
    print(json.dumps(dict(sourceId=value['sourceId'],cases={c['caseId']:c['verdict'] for c in value['cases']}),indent=2))
