import json
import runpy
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
PACKAGE=runpy.run_path(str(BASE/'package-evidence-v3.py'))
ref,put=PACKAGE['ref'],PACKAGE['put']


def package_round(limit=4,revision=1):
    inventory=PACKAGE['package'](limit,revision)
    numeric=runpy.run_path(str(BASE/'analyze-evidence-v3.py'))['analyze'](revision)
    put(BASE/f'numeric-controls-v{revision}.json',numeric)
    diagnostics=[]
    for attempt,report in zip(inventory['attempts'],numeric['sources']):
        source=attempt['source'];directory=(ROOT/source['receipt']['path']).parent
        transports=[]
        for kind in ['saveBody','addBody']:
            if source[kind] is None:continue
            body=json.loads((ROOT/source[kind]['path']).read_text());meta=(body.get('result') or {}).get('metaInfo',{});reason=body.get('reason2')
            transports.append(dict(kind=kind,body=source[kind],nativeSuccess=body.get('success'),nativeReason=body.get('reason'),nativeReason2=reason,nativeStructuredErrors=reason.get('errors') if isinstance(reason,dict) else None,structuredErrorChannelStatus='EXPOSED' if isinstance(reason,dict) and 'errors' in reason else 'UNOBSERVED / independent array absent',nativeWarnings=meta.get('warnings'),warningChannelStatus='EXPOSED' if 'warnings' in meta else 'UNOBSERVED',nativeEditorMarkerArrays=None,nativeEditorMarkerArrayStatus='UNOBSERVED; separate immediate/settled native UI retained'))
        path=directory/'compiler-diagnostics-v1.json';put(path,dict(version='v1',sourceId=source['sourceId'],sourceSha256=source['sourceSha256'],transports=transports));diagnostics.append(ref(path))
        put(directory.parent/'numeric-results-v1.json',report)
    put(BASE/f'facet-capabilities-v{revision}.json',dict(version=f'v{revision}',numericEvidence=ref(BASE/f'numeric-controls-v{revision}.json'),sources=[{k:v for k,v in r.items() if k in ['sourceId','sourceSha256','nativeCompileSuccess','selectedDataRowOrdinals','historyPredecessorDataRowOrdinal','primaryUniquePlotCells','facets','propertyVerdicts','comparisonCounts']} for r in numeric['sources']],compilerDiagnostics=diagnostics,residualHolds=['Hidden stored byte and generic quantizer remain UNOBSERVED/UNDECIDED','No universal color/gradient/identity, raster, engine approval or fixture promotion','All historical holds remain unchanged']))
    creation=json.loads((BASE/'environment-v1/native-layout-create-response-v1.json').read_text())
    put(BASE/f'account-actions-v{revision}.json',dict(version=f'v{revision}',newLayout=dict(nativeId=creation['id'],image=creation['image_url'],name='oracle-v98-v1',pageId=3,originalPageId=10),sourceSlots=len(inventory['attempts']),nativeSaves=sum(a['source']['saveBody'] is not None for a in inventory['attempts']),nativeAdds=sum(a['source']['addBody'] is not None for a in inventory['attempts']),originalCsvExports=sum(len(a['sessions']) for a in inventory['attempts']),includedOwnStudiesRemoved=sum(bool(a.get('removed')) for a in inventory['attempts']),maximumBudget=dict(saves=4,adds=4,csvs=4,unchangedSessions=4),sourceRetries=0,inputVariants=0,calendarOrHistoryActions=0,actualNativeCalculationSessionCount=None,nativeSessionIdentityStatus='UNOBSERVED; source/input sessions are workflow identities',oldScripts='No old script overwritten, renamed or deleted; distinct new private Save names and IDs. Full private-script inventory not inspected.',privateLibrary='sours-lat/P425PrivateV79v1/1 and P425PrivateV79v1 unchanged; no action',newLayoutSavedAfterCleanup=limit==4,preservationEvidence='environment-v2/existing-layout-comparison-v1.json' if limit==4 else None,forbiddenActionsTaken=[],engineChangesOrFixturePromotion=False))
    result=runpy.run_path(str(BASE/'validate-evidence-v4.py'))['validate'](revision,integrity=False,preservation=limit==4)
    put(BASE/f'validation-result-v{revision}.json',result)
    c=result['counts']
    lines=[f'# Oracle v98 response v{revision}','','Native observations returned for '+str(limit)+' of four finite source slots. '+('All four slots have ended.' if limit==4 else 'Remaining listed slots have not yet been returned.')+' Exact requested bytes and separate complete exposed Save/Add compiler bodies are retained, including any refusals or runtime diagnostics. No retry, repair, source/input variant or history navigation.', '', '| Source | Admission | Original / closed rows | Primary original rows | Private source/version |','| --- | --- | ---: | --- | --- |']
    for attempt in inventory['attempts']:
        source=attempt['source'];sessions=attempt['sessions'];session=sessions[0] if sessions else None;selected=session['selectedFirst64ConsecutiveClosedRows'] if session else []
        lines.append('| '+source['sourceId']+' | '+attempt['status']+' | '+(str(session['dataRows'])+' / '+str(session['independentlyClosedRows']) if session else 'UNOBSERVED')+' | '+(str(selected[0])+'–'+str(selected[-1]) if selected else 'NOT OBSERVED')+' | `'+str(source['privateScriptId'])+'` / '+str(source['privateVersion'])+' |')
    lines+=['','Primary selection is the earliest64 consecutive source-owned independently closed rows beginning at CASE_ID0, with increasing timestamps and consecutive INPUT_INDEX. Cast sources additionally retain the immediately preceding closed owned original row. Physical2m closure, export UTC, CHART_CONFIRMED and own millisecond INPUT_TIME are jointly checked. Each available complete constructor block has four visits per case; each available cast block has16 per phase. Admission/coverage is NOT OBSERVED for a stopped entry slot. No getter, NA predicate or equality result is an eligibility filter. All original rows/columns/strings/blanks and developing tails remain retained with explicit masks and zero primary credit outside the selected block.','']
    for report in numeric['sources']:
        lines+=['**'+report['sourceId']+'**','']
        if not report['rows']:
            lines+=['Numeric observations NOT OBSERVED; see the native refusal/context receipts.',''];continue
        if 'routes' in report['rows'][0]:
            lines+=['| Route | Equality outcome counts across64 rows | Frozen full-model verdicts |','| --- | --- | --- |']
            for route in ['LITERAL_RGB','LITERAL_NEW','SERIES_RGB','SERIES_NEW']:
                outcomes=Counter(r['equalityObservation'] for row in report['rows'] for r in row['routes'] if r['route']==route)
                verdicts=[p['model'].split('/',1)[1]+': '+p['verdict'] for p in report['propertyVerdicts'] if p['model'].startswith(route+'/')]
                lines.append('| '+route+' | '+json.dumps(dict(outcomes),sort_keys=True)+' | '+'; '.join(verdicts)+'; '+report['routePolicyAdjudications'][route]['observation']+' |')
            old=[]
            for row in report['rows']:
                values={p['headerRaw']:p['valueRaw'] for p in row['allRequestedRawCells']}
                old.append((values['EXACT_RGB12_5_EQ_DF'],values['EXACT_RGB12_5_EQ_DF_CODE']))
            lines+=['','Old RGB12.5 EQ_DF ternary / Boolean-NA-preserving code combinations: `'+str(dict(Counter(old)))+'`. Full 16-case × four-route × four-visit R/G/B/T/NA and five-equality vectors, candidate actual T getters, adjacency graph, cross-route equality and each frozen rational-policy prediction are in numeric controls. BOOLEAN_NA_EQUALITY, NEITHER_LITERAL, MULTIPLE_LITERAL_MATCHES and calibration contradictions are distinct observations. A supported source-literal equality never proves an unexposed stored alpha byte.','']
        else:
            lines+=['| Value | Phase0 R / G / B / T / NA raw tuple |','| --- | --- |']
            for name,points in report['rows'][0]['valueTuples'].items():
                lines.append('| '+name+' | '+' / '.join('∅' if p['valueRaw']=='' else p['valueRaw'] for p in points)+' |')
            lines+=['','Here ∅ means an original blank cell, not a synthesized color. Every phase and predecessor is retained independently. The v5 −1 code remains Boolean NA, distinct from0/false and a blank numeric getter. VAR/ARRAY and constant/selected-branch history transfers use actual same-source predecessor/target pointers. For a prior DF branch, CASE_ID/CURRENT_NA witness the expression; no absent preceding DF channel tuple is invented. Literal DF T13 is a separate nearest-percent getter hypothesis.','']
            for p in report['propertyVerdicts']:
                if p['model'].startswith(('A_','B_','C_','D_','NZ_','GRAD_')):lines.append('- '+p['model']+': **'+p['verdict']+'**; '+str(p['counts']))
            lines+=['','The ordinary-missing, finite-black and non-NA/blank-getter alternatives are bounded tuple candidates. NZ fallback recognition and cast-versus-bare-na gradient equivalence are separate tests; neither overwrites the native cast predicate or supplies hidden identity.','']
    lines += [f"Read-only validation: **{result['status']}**; {c.get('dataRows',0)} original rows, {c.get('independentlyClosedRows',0)} independently closed archive rows, {c.get('primaryRows',0)} primary rows and {c.get('uniquePrimaryPlotCells',0)} unique primary plot cells. {c.get('modelRecords',0)} model records and {c.get('rawPointerReferences',0)} raw pointer references are repeated analysis records, not unique cells. See [validation](validation-result-v{revision}.json), [numeric controls](numeric-controls-v{revision}.json), [attempt inventory](attempt-inventory-v{revision}.json) and [facet capabilities](facet-capabilities-v{revision}.json).",'',f"Only new layout `{creation['id']}/{creation['image_url']}` (`oracle-v98-v1`) is used. "+('Every successfully added own study has been removed and the new layout saved; builtin Vol remains. Full native records and passive before/after signatures are compared individually; any context difference is recorded as a preservation hold, never repaired by editing an old layout. See [preservation comparison](environment-v2/existing-layout-comparison-v1.json).' if limit==4 else 'Old layout/tab baselines are preserved; the end-of-round comparison awaits the remaining finite slots.'),'','P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action. New private scripts are distinct saves; no old script is overwritten/deleted/renamed. Full private script inventory, independent editor marker arrays, unexposed native feed/execution IDs and actual calculation counts remain UNOBSERVED. Per-source compiler diagnostics keep exposed warnings/errors separate from immediate/settled UI and absent arrays.', '', f'Run `python3 v98/captures/v98/validate-evidence-v4.py {revision}` from repository root. [Integrity](artifact-integrity-v{revision}.json) covers request/frozen sources, all returned artifacts and referenced prior dependencies, self-excluded. [Tooling rights](CAPTURE-TOOLING-LICENSE-v1.md) apply only to new capture tooling. No engine change/fixture promotion, hidden storage decoder, universal color model, rendered pixel/DPI/CSS contract or closure of historical holds1/2/7/8/13/14/21 follows from this capture.']
    lines+=['',f"Native action totals: {c.get('nativeSaves',0)} PRIVATE source Saves, {c.get('nativeAdds',0)} Adds, {c.get('csvs',0)} original exports, {c.get('nativeSourceEntryStops',0)} consumed partial-entry slot(s). Stopped constructor v6 has no Save/Add/compiler result, no executed-byte identity and no numeric credit. No retry or budget borrowing."]
    if limit==4:
        preservation=json.loads((BASE/'environment-v2/existing-layout-comparison-v1.json').read_text())
        lines+=['',f"Preservation observations: {c.get('oldSavedRecordsUnchanged',0)}/13 saved records unchanged; {c.get('oldSavedRecordsChanged',0)} saved-record differences; {c.get('oldOpenTabsUnchanged',0)}/9 open-tab signatures unchanged; {c.get('oldOpenTabsChanged',0)} open-tab differences. Native page IDs were reassigned after the MCP bridge restart and were mapped by stable layout URL."]
        for tab in preservation['openTabComparisons']:
            if not tab['equal']:
                lines+=['',f"**PRESERVATION HOLD — original page{tab['pageId']}**: before `{json.dumps(tab['before'],sort_keys=True)}`; after `{json.dumps(tab['after'],sort_keys=True)}`. The actual context difference is observed; cause is UNOBSERVED. No old layout reload, edit or restoration was performed by this workflow; unchanged-tab preservation cannot be certified for this context. Numeric observations belong only to the independently identified new v98 layout."]
    response=BASE/f'RESPONSE-v98-v{revision}.md';content='\n'.join(lines)+'\n'
    if response.exists():assert response.read_text()==content
    else:response.write_text(content)
    included={a['source']['sourceId'] for a in inventory['attempts']}
    files=[]
    for p in (ROOT/'v98').rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts or p.name.startswith('.'):continue
        rel=p.relative_to(BASE) if p.is_relative_to(BASE) else None
        if rel and rel.parts[0].startswith('v98-') and rel.parts[0] not in included:continue
        if p==BASE/f'artifact-integrity-v{revision}.json':continue
        files.append(p)
    manifest=json.loads((ROOT/'v98/bundle-manifest-v1.json').read_text())
    files.extend(ROOT/r['path'] for r in manifest['priorEvidence'])
    put(BASE/f'artifact-integrity-v{revision}.json',dict(version=f'v{revision}',scope='All returned v98 request/source/native/derived files and exact prior evidence dependencies; self-excluded. Body-only native transport, no headers/auth.',artifacts=[ref(p) for p in sorted(set(files))]))
    return result


if __name__=='__main__':
    print(json.dumps(package_round(int(sys.argv[1]) if len(sys.argv)>1 else 4,int(sys.argv[2]) if len(sys.argv)>2 else 1),indent=2))
