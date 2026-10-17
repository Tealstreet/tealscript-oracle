import json
import runpy
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
PACKAGE=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put=PACKAGE['ref'],PACKAGE['put']


def package_round(limit=5,revision=1):
    inventory=PACKAGE['package'](limit,revision)
    numeric=runpy.run_path(str(BASE/'analyze-evidence-v2.py'))['analyze'](revision)
    diagnostics=[]
    for attempt,report in zip(inventory['attempts'],numeric['sources']):
        source=attempt['source'];directory=(ROOT/source['receipt']['path']).parent;transports=[]
        for kind in ['saveBody','addBody']:
            if source[kind] is None:continue
            body=json.loads((ROOT/source[kind]['path']).read_text());meta=(body.get('result') or {}).get('metaInfo',{});reason=body.get('reason2')
            transports.append(dict(kind=kind,body=source[kind],nativeSuccess=body.get('success'),nativeReason=body.get('reason'),nativeReason2=reason,nativeStructuredErrors=reason.get('errors') if isinstance(reason,dict) else None,structuredErrorChannelStatus='EXPOSED' if isinstance(reason,dict) and 'errors' in reason else 'UNOBSERVED / independent array absent',nativeWarnings=meta.get('warnings'),warningChannelStatus='EXPOSED' if 'warnings' in meta else 'UNOBSERVED',nativeEditorMarkerArrays=None,nativeEditorMarkerArrayStatus='UNOBSERVED; separate immediate/settled native UI retained'))
        path=directory/'compiler-diagnostics-v1.json';put(path,dict(version='v1',sourceId=source['sourceId'],sourceSha256=source['sourceSha256'],transports=transports));diagnostics.append(ref(path))
        put(directory.parent/'numeric-results-v1.json',report)
    put(BASE/'direct-six-case-certificate-v1.json',dict(version='v1',policies=numeric['sixCaseDirectComparisonPolicies']))
    index=runpy.run_path(str(BASE/'analysis-index-v1.py'))['compact'](numeric)
    put(BASE/f'numeric-controls-v{revision}.json',index)
    preservation=json.loads((BASE/'environment-v2/existing-layout-comparison-v1.json').read_text()) if limit==5 else None
    put(BASE/f'facet-capabilities-v{revision}.json',dict(version=f'v{revision}',numericEvidence=ref(BASE/f'numeric-controls-v{revision}.json'),sources=[{k:v for k,v in r.items() if k in ['sourceId','sourceSha256','nativeCompileSuccess','selectedDataRowOrdinals','historyPredecessorDataRowOrdinal','primaryUniquePlotCells','facets','propertyVerdicts','comparisonCounts','routePolicyAdjudications','witnessAdjudication','uniformRuleVerdicts']} for r in numeric['sources']],sixCaseDirectComparisonPolicies={k:{a:b for a,b in v.items() if a!='sourceCertificates'} for k,v in numeric['sixCaseDirectComparisonPolicies'].items()},compilerDiagnostics=diagnostics,preservation=ref(BASE/'environment-v2/existing-layout-comparison-v1.json') if preservation else None,residualHolds=['Hidden storage, universal equality/quantizer and unexported channels remain held','No var own-zero initialization, actual calculation-count, native feed/execution-ID or complete private inventory claim','V98 consumed slot and old-page3 context hold remain historical and unchanged','No engine approval or fixture promotion']))
    creation=json.loads((BASE/'environment-v1/native-layout-create-response-v1.json').read_text())
    put(BASE/f'account-actions-v{revision}.json',dict(version=f'v{revision}',newLayout=dict(nativeId=creation['id'],image=creation['image_url'],name='oracle-v99-v1',pageId=11),sourceSlots=len(inventory['attempts']),nativeSaves=sum(a['source']['saveBody'] is not None for a in inventory['attempts']),nativeAdds=sum(a['source']['addBody'] is not None for a in inventory['attempts']),originalCsvExports=sum(len(a['sessions']) for a in inventory['attempts']),includedOwnStudiesRemoved=sum(bool(a.get('removed')) for a in inventory['attempts']),maximumBudget=dict(saves=5,adds=5,csvs=5,unchangedSessions=5),sourceRetries=0,inputVariants=0,calendarOrHistoryActions=0,actualNativeCalculationSessionCount=None,oldScripts='Distinct new PRIVATE Save identities; no old script overwrite/delete/rename. Full private inventory UNOBSERVED.',privateLibrary='P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action',newLayoutSavedAfterCleanup=limit==5,builtinStudies='None on initial/new configured layout; no builtin added or removed',preservationEvidence='environment-v2/existing-layout-comparison-v1.json' if preservation else None,forbiddenActionsTaken=[],engineChangesOrFixturePromotion=False))
    result=runpy.run_path(str(BASE/'validate-evidence-v3.py'))['validate'](revision,integrity=False,preservation=limit==5)
    put(BASE/f'validation-result-v{revision}.json',result)
    c=result['counts'];lines=[f'# Oracle v99 response v{revision}','','Native evidence returned for '+str(limit)+' of five finite slots. '+('All five slots have ended.' if limit==5 else 'Remaining independent listed slots have not yet been returned.')+' Sources use one distinct new PRIVATE Save, one Add and one original export per successful slot. Exact requested/executed bytes, full separate compiler bodies, native context, diagnostics and cleanup receipts are retained. No source repair, retry, input variant, history navigation, reload or forced recalculation.','', '| Source | Native status | Original / closed rows | Primary original rows | New private source/version |','| --- | --- | ---: | --- | --- |']
    for a in inventory['attempts']:
        s=a['source'];session=a['sessions'][0] if a['sessions'] else None;selected=session['selectedFirst64ConsecutiveClosedRows'] if session else []
        lines.append('| '+s['sourceId']+' | '+a['status']+' | '+(str(session['dataRows'])+' / '+str(session['independentlyClosedRows']) if session else 'UNOBSERVED')+' | '+(str(selected[0])+'–'+str(selected[-1]) if selected else 'NOT OBSERVED')+' | `'+str(s['privateScriptId'])+'` / '+str(s['privateVersion'])+' |')
    lines+=['','Constant v5 programs use their earliest64 independently closed consecutive own rows. Phase programs additionally begin CASE_ID0; cast programs require an actual original closed source-index predecessor. Input time milliseconds, CSV Unix seconds, physical2m close, export UTC and CHART_CONFIRMED are checked independently. Neither getter/NA/equality/calibration outputs nor model agreement select rows. Every original row/column/raw string/blank and developing frontier remains retained, with explicit exclusions and zero primary credit outside the selected block.','']
    for report in numeric['sources']:
        lines+=['**'+report['sourceId']+'**','']
        if not report['rows']:
            lines+=['Numeric facets NOT OBSERVED; see the specific native admission/context/coverage record.',''];continue
        row=report['rows'][0]
        if 'cases' in row:
            lines+=['| Constructor / transparency | Actual compared-literal codes in manifest order | Equality observation | Actual getter/predicate targets |','| --- | --- | --- | --- |']
            for case in row['cases']:
                lines.append('| '+case['route']+' / '+case['transparencyRaw']+' | '+' / '.join(('UNOBSERVED' if p is None else p['valueRaw']) for p in case['actualEqualityCells'])+' | '+case['equalityObservation']+' | '+', '.join(p['headerRaw']+'='+('∅' if p['valueRaw']=='' else p['valueRaw']) for p in case['getterAndPredicateTargets'])+' |')
            for route,verdict in report['routePolicyAdjudications'].items():lines+=['',route+' own-source finite policy adjudication: **'+verdict['observation']+'**; '+json.dumps(verdict['frozenModelVerdicts'],sort_keys=True)+'.']
            lines+=['','These are first-primary-row observations; all64 owned rows, every queried literal/control and consistency or contrary cell remain in the numeric report. Getter targets are independent: no comparison alpha predicts T. Core literal calibration is its complete four-token graph; edge calibration is only its queried self/adjacent graph. No cross-source calibration or hidden stored identity is supplied.','']
        elif 'routes' in row:
            lines+=['This is a new v99 execution of the unchanged SHA-bound v98 source, including its original V98 title. The consumed v98 slot remains consumed and numerically UNOBSERVED. All16 cases × four routes × four visits, actual tuples/equality/candidate-T/calibration fields and separate exact12.5 control are retained; only the original four v98 models are tested.','']
            for route,verdict in report['routePolicyAdjudications'].items():lines.append('- '+route+': **'+verdict['observation']+'**; '+json.dumps(verdict['frozenModelVerdicts'],sort_keys=True))
            lines+=['']
        elif 'valueTuples' in row:
            lines+=['| Role | Actual R / G / B / T / NA at first primary row |','| --- | --- |']
            for role,points in row['valueTuples'].items():lines.append('| '+role+' | '+' / '.join('UNOBSERVED' if p is None else '∅' if p['valueRaw']=='' else p['valueRaw'] for p in points)+' |')
            lines+=['','Every direct/alias/var/array/twin/scalar-history/object-history equality and predicate is independently retained on all64 rows. NA-conditioned models apply only to exact operands with exported predicates; inline direct/repeated-get operands never borrow an alias predicate. Actual getters remain observed even with NA1. Equal tuples never replace the native Boolean. Full model counts are in the facet report; unplotted twin/history RGBA channels remain UNOBSERVED.','']
            for family,proof in report.get('uniformRuleVerdicts',{}).items():lines+=['',family+': **'+proof['verdict']+'** across applicable exactly bound expressions; per-expression certificates and conditional applicability remain separate.']
        elif 'witnessAdjudication' in report:
            lines+=['Exact batch77 minimal proposal, with the unchanged original63 plots and added64th ARRAY_EQ_SELF. Actual primary code counts: `'+json.dumps(report['witnessAdjudication']['primaryRawCodeCounts'],sort_keys=True)+'`. Witness adjudication: **'+report['witnessAdjudication']['observation']+'**. Full original-control/phase certificate: `'+str(report['witnessAdjudication']['fullControlAndPhaseCertificate'])+'`.','', 'Original semantic controls are compared to their own pinned v98 native observations by CASE_ID and actual original predecessor branch; absolute index/time/confirmation are context and never expected equal to the older session. Every old/new cell has its own original CSV pointer. All same-phase baseline controls must be consistent; changed controls hold extrapolation without dropping rows. The two frozen predictions remain0 versus1, with no third fitted model or universal identity/storage claim.','']
    lines+=['**Complete six-case immediate comparison policies**','']
    for route,verdict in numeric['sixCaseDirectComparisonPolicies'].items():lines.append('- '+route+': **'+verdict['observation']+'**; '+json.dumps(verdict['frozenModelVerdicts'],sort_keys=True))
    lines+=['','The six-case certificate requires both separately owned fixed v5 programs and complete coverage. A not-yet-returned or incomplete program keeps the full certificate UNDECIDED; every available local contradiction and raw zero/−1 remains separately observed. No rows/calibrations are stitched between executions.','',f"Validation: **{result['status']}**; {c.get('dataRows',0)} original archive rows, {c.get('independentlyClosedRows',0)} independently closed archive rows, {c.get('primaryRows',0)} primary rows, {c.get('uniquePrimaryPlotCells',0)} unique primary plot cells. {c.get('modelRecords',0)} model records / {c.get('rawPointerReferences',0)} pointer references are repeated analysis records, not unique cells. Native actions: {c.get('nativeSaves',0)} PRIVATE Saves, {c.get('nativeAdds',0)} Adds, {c.get('compilerBodies',0)} full compiler bodies and {c.get('csvs',0)} original CSVs.",'',f'Only new layout `{creation["id"]}/{creation["image_url"]}` (`oracle-v99-v1`) was used. '+('Every added own study is removed and only the new layout saved.' if limit==5 else 'End-of-round new-layout Save and preservation comparison await the remaining finite slots.'),'','P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action. No old script/layout/tab was edited, renamed, deleted, reloaded or restored. Full private script inventory, independent editor arrays, native feed/execution IDs and actual native calculation counts remain UNOBSERVED. V98 historical preservation and admission holds remain unchanged.']
    if preservation:
        lines+=['',f"Passive preservation: {c.get('oldSavedRecordsUnchanged',0)}/14 saved records and {c.get('oldOpenTabsUnchanged',0)}/10 open-tab signatures unchanged. Every actual difference is retained as a hold in [comparison](environment-v2/existing-layout-comparison-v1.json), with no inferred cause or old-layout repair."]
        for tab in preservation['openTabComparisons']:
            if not tab['equal']:lines+=['',f"PRESERVATION HOLD page{tab['pageId']}: before `{json.dumps(tab['before'],sort_keys=True)}`; after `{json.dumps(tab['after'],sort_keys=True)}`. Cause UNOBSERVED; unchanged-context preservation cannot be certified."]
    lines+=['',f'Run `python3 v99/captures/v99/validate-evidence-v3.py {revision}`. See [inventory](attempt-inventory-v{revision}.json), [native targets and models](numeric-controls-v{revision}.json), [facets](facet-capabilities-v{revision}.json), [validation](validation-result-v{revision}.json), [actions](account-actions-v{revision}.json), [integrity](artifact-integrity-v{revision}.json) and [tooling rights](CAPTURE-TOOLING-LICENSE-v1.md). Integrity binds all request/source/returned files and actually read prior dependencies, self-excluded. No engine change, fixture promotion, hidden payload decoder, universal quantizer/identity, raster contract or closure of historical holds1/2/7/8/13/14/21 follows from this return.']
    lines+=['','The numeric-controls file is a SHA-bound per-source index (`format: per-source-index-v1`). Each source entry links its complete immutable `numeric-results-v1.json` containing every primary row, raw cell, dependency and hypothesis. The separate direct-six-case certificate retains all combined-query target pointers. The read-only validator hydrates these exact files and compares the complete analysis; no cells/model records are removed. Earlier response artifacts remain byte-for-byte unchanged.']
    for report in numeric['sources']:
        if report['sourceId']=='v98-color-constructors-v6' and report['rows']:
            for title in ['EXACT_RGB12_5_EQ_DF','EXACT_RGB12_5_EQ_DF_CODE']:
                counts=Counter(next(p['valueRaw'] for p in row['allRequestedRawCells'] if p['headerRaw']==title) for row in report['rows'])
                lines+=['',report['sourceId']+' '+title+' raw counts: `'+json.dumps(dict(counts),sort_keys=True)+'`.']
    response=BASE/f'RESPONSE-v99-v{revision}.md';content='\n'.join(lines)+'\n'
    if response.exists():assert response.read_text()==content
    else:response.write_text(content)
    manifest=json.loads((ROOT/'v99/bundle-manifest-v1.json').read_text());all_ids={a['sourceId'] for a in manifest['sources']};included={a['source']['sourceId'] for a in inventory['attempts']};files=[]
    for p in (ROOT/'v99').rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts or p.name.startswith('.'):continue
        rel=p.relative_to(BASE) if p.is_relative_to(BASE) else None
        if rel and rel.parts[0] in all_ids and rel.parts[0] not in included:continue
        if p==BASE/f'artifact-integrity-v{revision}.json':continue
        files.append(p)
    files.extend(ROOT/r['path'] for r in manifest['priorEvidence'])
    files.extend(ROOT/a['path'] for a in manifest['sources'])
    for report in numeric['sources']:
        if 'baselineEvidence' in report:files.extend(ROOT/report['baselineEvidence'][key]['path'] for key in ['csv','columnBindings','closureMask'])
    put(BASE/f'artifact-integrity-v{revision}.json',dict(version=f'v{revision}',scope='All request/source/returned artifacts and actually read prior dependencies; self-excluded. Complete native compiler bodies/form/CSV only; no auth headers.',artifacts=[ref(p) for p in sorted(set(files))]))
    return result


if __name__=='__main__':print(json.dumps(package_round(int(sys.argv[1]) if len(sys.argv)>1 else 5,int(sys.argv[2]) if len(sys.argv)>2 else 1),indent=2))
