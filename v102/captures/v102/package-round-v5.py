import json
import runpy
import sys
from pathlib import Path

sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
PACKAGE=runpy.run_path(str(BASE/'package-evidence-v2.py'))
ref,put=PACKAGE['ref'],PACKAGE['put']


def package_round(limit=25,revision=1):
    inventory=PACKAGE['package'](limit,revision)
    numeric=runpy.run_path(str(BASE/'analyze-evidence-v1.py'))['analyze'](revision,write=True)
    put(BASE/f'numeric-controls-v{revision}.json',numeric)
    diagnostics=[];facets=[]
    for attempt,index in zip(inventory['attempts'],numeric['sources']):
        source=attempt['source'];directory=(ROOT/source['receipt']['path']).parent;transports=[]
        for kind in ['saveBody','addBody']:
            if source[kind] is None:continue
            body=json.loads((ROOT/source[kind]['path']).read_text());meta=(body.get('result') or {}).get('metaInfo',{});reason=body.get('reason2')
            transports.append(dict(kind=kind,body=source[kind],nativeSuccess=body.get('success'),nativeReason=body.get('reason'),nativeReason2=reason,nativeStructuredErrors=reason.get('errors') if isinstance(reason,dict) else None,structuredErrorChannelStatus='EXPOSED' if isinstance(reason,dict) and 'errors' in reason else 'UNOBSERVED / no independent array exposed',nativeWarnings=meta.get('warnings'),warningChannelStatus='EXPOSED' if 'warnings' in meta else 'UNOBSERVED',nativeEditorMarkerArrays=None,editorMarkerStatus='UNOBSERVED; separate immediate/settled UI retained'))
        diagnostic_path=directory/'compiler-diagnostics-v1.json'
        diagnostic=dict(version='v1',sourceId=source['sourceId'],sourceSha256=source['sourceSha256'],transports=transports)
        if source.get('sourceEntryStop') is not None:diagnostic['sourceEntryStop']=source['sourceEntryStop']
        put(diagnostic_path,diagnostic);diagnostics.append(ref(diagnostic_path))
        report=json.loads((ROOT/index['report']['path']).read_text())
        case_path=BASE/source['sourceId']/'facet-assessment-v3.json'
        put(case_path,runpy.run_path(str(BASE/'build-facet-assessments-v3.py'))['build'](source['sourceId']))
        facets.append(dict(sourceCaseAssessment=ref(case_path),sourceId=source['sourceId'],sourceSha256=source['sourceSha256'],nativeCompileSuccess=source['nativeCompileSuccess'],numericReport=index['report'],numericPropertyVerdicts=index['numericPropertyVerdicts'],numericAlternativeOutcomes=index['numericAlternativeOutcomes'],visualRegionMap=index['renderAssessment'],compilerDiagnostics=ref(diagnostic_path),scope='Numeric/blank/intent properties and separately bound visual case decisions; no broad family PASS or pixel evidence inferred from getters'))
    put(BASE/f'facet-capabilities-v{revision}.json',dict(version=f'v{revision}',sources=facets,remainingFiniteSourceSlots=25-len(inventory['attempts']),held=['Every absent/clipped/nonintersecting/already obscured/precision-ambiguous visual property','Unexposed independent editor arrays, native frame/feed/execution IDs, full private inventory and actual backend calculation count','Historical preservation/semantic holds and universal color/identity/raster/font contracts']))
    creation=json.loads((BASE/'environment-v1/native-layout-create-response-v1.json').read_text())
    put(BASE/f'account-actions-v{revision}.json',dict(version=f'v{revision}',newLayout=dict(nativeId=creation['id'],image=creation['image_url'],name='oracle-v102-v1',pageId=14),returnedSourceSlots=len(inventory['attempts']),nativeEntryStops=sum(a['source']['saveBody'] is None for a in inventory['attempts']),sourceSlotMaximum=25,nativeSaves=sum(a['source']['saveBody'] is not None for a in inventory['attempts']),nativeAdds=sum(a['source']['addBody'] is not None for a in inventory['attempts']),originalCsvExports=sum(len(a['sessions']) for a in inventory['attempts']),nativeRenderPNGs=sum(s['renderPng'] is not None for a in inventory['attempts'] for s in a['sessions']),sourceInputWorkflowSessions=sum(len(a['sessions']) for a in inventory['attempts']),actualNativeCalculationCount=None,actualCalculationCountStatus='UNOBSERVED',sourceRetries=0,inputVariants=0,subsequentSettingsChanges=0,historyActions=0,ownStudiesRemoved=sum(bool(a['removed']) for a in inventory['attempts']),newLayoutSavedAfterAllCleanup=limit==25,passivePreservationStatus='End comparison returned' if limit==25 else 'End comparison pending remaining finite sources; baseline17 saved records/13 old tabs retained',privateLibrary='P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action',oldScripts='Distinct new private identities; no old overwrite/rename/delete. Full private script inventory UNOBSERVED',builtinVolume='Native default Vol retained',forbiddenActionsTaken=[],engineChangesOrFixturePromotion=False))
    result=runpy.run_path(str(BASE/'validate-evidence-v4.py'))['validate'](revision,integrity=False,preservation=limit==25)
    put(BASE/f'validation-result-v{revision}.json',result)
    counts=result['counts'];lines=[f'# Oracle v102 response v{revision}','','Native evidence returned for '+str(limit)+' of25 finite source slots; '+str(25-limit)+' slots remain unreturned. '+('All finite slots have ended.' if limit==25 else 'The same new layout remains reserved for the remaining independent sources.')+' Requested bytes and admitted source transports are preserved unchanged; consumed entry stops preserve exposed partial UI text with zero execution credit. Admitted sources have distinct new PRIVATE Save identities, one Add/export/session and at most one rendering PNG per admitted slot, zero source retries/input/settings/history variants.','', '| Source | Status | Original / closed / primary rows | Unique anchor own index | Private source/version |','| --- | --- | ---: | --- | --- |']
    for attempt,index in zip(inventory['attempts'],numeric['sources']):
        source=attempt['source'];session=attempt['sessions'][0] if attempt['sessions'] else None;report=json.loads((ROOT/index['report']['path']).read_text());block=json.loads((ROOT/report['nativeBlock']['path']).read_text())
        anchor=block.get('visualAnchor');own=anchor['cells']['INPUT_INDEX']['valueRaw'] if anchor else 'UNOBSERVED'
        lines.append('| '+source['sourceId']+' | '+attempt['status']+' | '+(str(session['dataRows'])+' / '+str(session['independentlyClosedRows'])+' / '+str(len(session['selectedPrimaryClosedRowOrdinals'])) if session else 'UNOBSERVED')+' | '+own+' | `'+str(source['privateScriptId'])+'` / '+str(source['privateVersion'])+' |')
    lines+=['','Every complete primary block is the earliest32 consecutive source-owned physically closed indices>=200 starting CASE_ID0, four full0..7 cycles, before its unique closed VISUAL_ANCHOR_TIME/INDEX row. Input milliseconds agree with original chart Unix seconds; confirmation and actual export UTC independently establish physical2m closure. Coordinate slots additionally require eight original closed predecessors. Increasing real timestamps and consecutive source indices are required, without invented120-second continuity. No getter/code/blank/model agreement selects rows.','', 'Every original CSV row/header/column/decimal string/blank is archived. Developing/other/anchor/reserved predecessor cells stay OBSERVED / EXCLUDED with explicit per-row causes and zero primary credit. Anchor blanks in selected historical rows are intentional source context, not absent native channels. No own-origin/frontier completeness, synthetic prefix, history expansion, rebased absolute-index parity or cross-session identity is claimed.','']
    for entry in numeric['sources']:
        report=json.loads((ROOT/entry['report']['path']).read_text())
        lines+=['','**'+entry['sourceId']+'**','', 'Numeric/blank source-property verdicts: `'+json.dumps(entry['numericPropertyVerdicts'],sort_keys=True)+'`; '+str(entry['uniquePrimaryPlotCells'])+' unique primary plot cells. Every property retains its frozen contract/file SHA/pointer, all phases, complete comparison mask and original CSV-SHA/row/column/header/raw targets in the native block. Getter/intent outcomes do not certify unexported style or pixels.']
        assessment=json.loads((BASE/entry['sourceId']/'facet-assessment-v3.json').read_text())
        lines+=['','Per-case decisions: `'+json.dumps({c['caseId'].split(':',1)[1]:c['verdict'] for c in assessment['cases']},sort_keys=True)+'`. The source [facet assessment]('+entry['sourceId']+'/facet-assessment-v3.json) keeps numeric, admission and visual subfacets separate, including unobserved intermediate states.']
        for family in report['numericAlternatives']:
            lines.append('- Numeric scope '+family['id']+': **'+family['observation']+'**; supported `'+str(family['supportedVariantIds'])+'`.')
        if report['renderAssessment']:
            visual=json.loads((ROOT/report['renderAssessment']['path']).read_text())
            lines+=['', 'One original PNG SHA256 `'+visual['originalPng']['sha256']+'`, '+str(visual['originalDimensionsPx']['width'])+'×'+str(visual['originalDimensionsPx']['height'])+'; source/private/version/session/CSV/anchor and native axes/UTC windows are bound in the [DERIVED region map]('+str(Path(report['renderAssessment']['path']).relative_to(BASE.relative_to(ROOT)))+').']
            for facet in visual['facets']:
                text='- Visual '+facet['caseId'].split(':',1)[1]+': **'+facet['verdict']+'**'
                if facet.get('supportedCandidate'):text+=' — '+facet['supportedCandidate']
                if facet.get('notObservedCause'):text+='; '+facet['notObservedCause']
                lines.append(text+'.')
            lines+=['', 'Each actual table/subject intersection is scored independently in the map. Supported unoccluded pairs never supply all-nine-group completeness. Literal visible text is recorded without completing obscured glyphs. Missing/intersecting-but-obscured/thin ambiguous regions remain held; no second viewport, resize, zoom or screenshot repairs them.']
        else:lines+=['', 'Visual certificate: '+report['renderAssessmentStatus']+'.']
    lines+=['',f"Read-only validation: **{result['status']}**; {counts.get('dataRows',0)} original archive rows, {counts.get('independentlyClosedRows',0)} independently closed archive rows, {counts.get('primaryRows',0)} selected primary rows and {counts.get('uniquePrimaryPlotCells',0)} unique primary source plot cells. The11,168-cell full-round maximum is prospective, includes context/scale/intent/intentional anchor blanks and is never assigned to unreturned/refused sources. Repeated models, transports, PNGs and pointer references do not multiply native cells or engine parity credit.",'',f"Returned native actions: {counts.get('nativeSaves',0)} PRIVATE Saves, {counts.get('nativeAdds',0)} Adds, {counts.get('compilerBodies',0)} separate complete compiler bodies, {counts.get('originalCSVs',0)} original CSVs and {counts.get('nativeRenderingPNGs',0)} rendering PNGs. Native refusals/runtime stops, when present, retain raw diagnostics without source repair. Native structured errors/warnings and independent editor markers are separate channels; unexposed arrays remain UNOBSERVED.",'',f'Only NEW layout `{creation["id"]}/{creation["image_url"]}` (`oracle-v102-v1`), BINANCE:BTCUSDT2m Candles Etc/UTC. Every returned own study is removed; native default Vol retained. '+('The new layout Save and full passive end comparison are returned.' if limit==25 else 'New-layout Save and full passive end comparison await the remaining finite slots; the original17 saved records/13 old-tab baselines are retained.'),'','P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action. No old layout/script/tab edit, reload, rename, deletion or restoration, publication/share/visibility change, alert, import, reconnect, entitlement/account action, hidden inspection or direct API. Unexposed native feed/frame/execution IDs, actual backend calculation count, zoom/DPI/resolved-font metrics and full private inventory remain UNOBSERVED. Historical holds remain held.','',f'Run `python3 v102/captures/v102/validate-evidence-v4.py {revision}`. [Inventory](attempt-inventory-v{revision}.json), [numeric per-source index](numeric-controls-v{revision}.json), [frozen request-derived numeric contracts](numeric-contracts-v1.json), [facets](facet-capabilities-v{revision}.json), [validation](validation-result-v{revision}.json), [account actions](account-actions-v{revision}.json), [integrity](artifact-integrity-v{revision}.json) and [tooling license](CAPTURE-TOOLING-LICENSE-v1.md). Integrity covers all request/source/native/derived dependencies and returns, self-excluded. Sparse historical dependencies are verified read-only through their committed Git blobs when absent from the working tree. No engine fix, fixture promotion, universal raster/font/color/identity model, provider/history reconstruction or historical-hold closure.']
    response=BASE/f'RESPONSE-v102-v{revision}.md';content='\n'.join(lines)+'\n'
    if response.exists():assert response.read_text()==content
    else:response.write_text(content)
    manifest=json.loads((ROOT/'v102/bundle-manifest-v1.json').read_text());all_ids={a['sourceId'] for a in manifest['sources']};included={a['source']['sourceId'] for a in inventory['attempts']};files=[]
    for path in (ROOT/'v102').rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts or path.name.startswith('.') or path==BASE/f'artifact-integrity-v{revision}.json':continue
        relative=path.relative_to(BASE) if path.is_relative_to(BASE) else None
        if relative and relative.parts[0] in all_ids and relative.parts[0] not in included:continue
        files.append(path)
    records={str(path.relative_to(ROOT)):ref(path) for path in files}
    for entry in manifest['priorEvidence']:records[entry['path']]=entry
    put(BASE/f'artifact-integrity-v{revision}.json',dict(version=f'v{revision}',scope='All v102 request/source/native/derived dependencies and returned artifacts, self-excluded; body-only native transports, no auth headers. Unreturned source attempt directories are not represented as returns.',artifacts=[records[k] for k in sorted(records)]))
    return result


if __name__=='__main__':print(json.dumps(package_round(int(sys.argv[1]) if len(sys.argv)>1 else 25,int(sys.argv[2]) if len(sys.argv)>2 else 1),indent=2))
