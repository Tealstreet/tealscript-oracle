import json
import runpy
from collections import Counter
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
SHARED=runpy.run_path(str(BASE/'numeric-context-v1.py'))
Context,classify=SHARED['Context'],SHARED['classify']


def analyze(attempt,asset):
    c=Context(attempt,asset)
    if not c.session:return c.report()
    earlier=json.loads((ROOT/'v98/captures/v98/numeric-controls-v6.json').read_text())
    baseline=next(r for r in earlier['sources'] if r['sourceId']=='v98-color-na-cast-v6')
    originals=json.loads((ROOT/'v98/bundle-manifest-v1.json').read_text())
    original=next(s for s in originals['sources'] if s['sourceId']=='v98-color-na-cast-v6')
    semantic=[p['title'] for p in original['plots'] if p['title'] not in ['INPUT_INDEX','INPUT_TIME','CHART_CONFIRMED']]
    groups={}
    for row in baseline['rows']:
        points={p['headerRaw']:p for p in row['allRequestedRawCells']}
        previous={p['headerRaw']:p for p in row['predecessorRawCells']}
        key=(points['CASE_ID']['valueRaw'],int(previous['CASE_ID']['valueRaw'])%2)
        groups.setdefault(key,[]).append(points)
    consistency=[]
    for n in c.selected:
        row=c.row(n)
        key=(c.point(n,'CASE_ID')['valueRaw'],int(c.value(n-1,'CASE_ID'))%2)
        references=groups.get(key,[])
        stable=bool(references) and all(len({r[title]['valueRaw'] for r in references})==1 for title in semantic)
        prediction={title:references[0][title]['valueRaw'] if references else 'UNDECIDED' for title in semantic}
        dependency=[references[0][title] for title in semantic] if references else []
        comparison=c.compare(row,'UNCHANGED_ORIGINAL_CONTROL_CONTEXT_VS_V98',prediction,['CASE_ID'],dependency,raw=True,applies=stable,cause='Old and new sessions remain separate; baseline row group is selected only by CASE_ID and witnessed original predecessor branch. Any changed control or inconsistent baseline holds extrapolation, never removes a row.')
        controls_recur=stable and comparison['verdict']=='SUPPORTED'
        consistency.append(controls_recur)
        for name,value in [('STABLE_INITIALIZER_FOLDING_RUNTIME_MISSING',0),('COPIED_MISSING_CAST_TOKEN',1)]:
            c.compare(row,name,{'ARRAY_EQ_SELF':value},semantic,dependency,applies=controls_recur,cause='Exact owner-selected minimal witness, conditional on original semantic controls recurring. Raw target/prediction relationship is retained even if contextual extrapolation is held.')
        row['originalControlsRecur']=controls_recur
        row['arraySelfRawCell']=c.point(n,'ARRAY_EQ_SELF')
        row['rawWitnessDirection']='RUNTIME_MISSING_WITNESS' if c.value(n,'ARRAY_EQ_SELF')==0 else 'COPIED_TOKEN_WITNESS' if c.value(n,'ARRAY_EQ_SELF')==1 else 'UNDECIDED / unexpected native code'
    report=c.report()
    report['baselineEvidence']={k:baseline[k] for k in ['sourceId','sourceSha256','csv','columnBindings','closureMask']}
    report['baselinePhaseGroupCertificates']=[dict(caseId=key[0],previousBranchParity=key[1],allOriginalControlCells=[[r[t] for t in semantic] for r in refs],controlRawValuesConsistent=all(len({r[t]['valueRaw'] for r in refs})==1 for t in semantic)) for key,refs in groups.items()]
    report['originalControlComparisonScope']=dict(excludedContextFields=['INPUT_INDEX','INPUT_TIME','CHART_CONFIRMED'],comparedOriginalTitles=semantic,joinFields=['CASE_ID','actual original preceding CASE_ID parity'],allPrimaryRowsControlsRecur=all(consistency) if consistency else False,baselineAndNewSessionNeverStitched=True)
    verdicts={p['model']:p['verdict'] for p in report['propertyVerdicts'] if p['model'] in ['STABLE_INITIALIZER_FOLDING_RUNTIME_MISSING','COPIED_MISSING_CAST_TOKEN']}
    report['witnessAdjudication']=classify(verdicts)
    codes=Counter(c.point(n,'ARRAY_EQ_SELF')['valueRaw'] for n in c.selected if c.point(n,'ARRAY_EQ_SELF') is not None and 'ARRAY_EQ_SELF' in c.owned)
    numeric_codes={SHARED['number'](code) for code in codes}
    if len(numeric_codes)>1 or any(code not in [0,1] for code in numeric_codes):
        report['witnessAdjudication']['observation']='UNDECIDED / mixed or unexpected native codes'
    report['witnessAdjudication']['primaryRawCodeCounts']=dict(codes)
    report['witnessAdjudication']['discriminatorBindingStatus']='CAPTURED' if 'ARRAY_EQ_SELF' in c.owned else 'NOT OBSERVED / absent or ambiguous binding'
    report['witnessAdjudication']['fullControlAndPhaseCertificate']=len(c.selected)==64 and all(consistency)
    if not c.selected and c.session['eligibleDataRowOrdinals'] and 'ARRAY_EQ_SELF' in c.owned:
        n=c.session['eligibleDataRowOrdinals'][0]
        report['partialClosedDiscriminator']=dict(nativeCell=c.point(n,'ARRAY_EQ_SELF'),predictions={'STABLE_INITIALIZER_FOLDING_RUNTIME_MISSING':0,'COPIED_MISSING_CAST_TOKEN':1},rawValueObserved=True,full64RowAndControlCertificate='NOT OBSERVED; raw cell does not borrow old controls or certify extrapolation')
    return report
