import json
import runpy
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
PACKAGE=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put=PACKAGE['ref'],PACKAGE['put']


def package_round(limit,revision):
    inventory=PACKAGE['package'](limit,revision)
    numeric=runpy.run_path(str(BASE/'analyze-evidence-v1.py'))['analyze'](revision,write=True)
    put(BASE/f'numeric-controls-v{revision}.json',numeric)
    manifest=json.loads((ROOT/'v104/bundle-manifest-v1.json').read_text());assets={a['sourceId']:a for a in manifest['entries']}
    capabilities=[];case_rows=[]
    for attempt,entry in zip(inventory['attempts'],numeric['sources']):
        source=attempt['source'];directory=BASE/source['sourceId'];body_channels=[]
        for kind in ['saveBody','addBody']:
            if source[kind] is None:continue
            body=json.loads((ROOT/source[kind]['path']).read_text());reason=body.get('reason2');meta=(body.get('result') or {}).get('metaInfo',{})
            body_channels.append(dict(kind=kind,originalBody=source[kind],success=body.get('success'),reason=body.get('reason'),reason2=reason,structuredErrors=reason.get('errors') if isinstance(reason,dict) else None,structuredWarnings=reason.get('warnings') if isinstance(reason,dict) else None,metadataWarnings=meta.get('warnings'),independentEditorMarkerArrays=None,markerStatus='UNOBSERVED; immediate/settled original UI retained separately',scope='Original body/error/warning order and start/end/ctx fields preserved; absent channels are not inferred empty'))
        diagnostic_path=directory/'compiler-diagnostics-v1.json'
        put(diagnostic_path,dict(version='v1',sourceId=source['sourceId'],sourceSha256=source['sourceSha256'],transports=body_channels,sourceEntryStop=source.get('sourceEntryStop')))
        visual_path=directory/'derived-region-map-v1.json';visual=json.loads(visual_path.read_text()) if visual_path.exists() else None
        indexed={f['facetId']:f for f in visual['facets']} if visual else {}
        facets=[]
        for frozen in assets[source['sourceId']]['visualFacets']:
            finding=indexed.get(frozen['facetId'])
            facet=dict(facetId=frozen['facetId'],verdict=finding['verdict'] if finding else 'UNDECIDED',outcome=finding['outcome'] if finding else 'UNDECIDED',modelA=frozen['modelA'],modelB=frozen['modelB'],frozenPixelWindow=frozen['pixelWindow'],visualMap=ref(visual_path) if visual else None,notObservedCauses=finding['notObservedCauses'] if finding else ['No admitted/owned original PNG with independent readable control certificate'],scope='One exact source/version and frozen window; numeric getters/intent never supply pixels')
            facets.append(facet);case_rows.append(facet)
        path=directory/'facet-assessment-v1.json'
        put(path,dict(version='v1',sourceId=source['sourceId'],sourceSha256=source['sourceSha256'],numericReport=entry['report'],compilerDiagnostics=ref(diagnostic_path),nativeAdmission=source['nativeCompileSuccess'],facets=facets,numericScope='Build-event getters are one observation plus31 intentional blanks. Per-bar context, modulo32 step/arrow formulas, source color channels and boolean export policy are distinct.',held='All absent/clipped/overlapping/unreadable controls; native frame/font/DPI/zoom; historical holds and universal raster/API claims'))
        capabilities.append(dict(sourceId=source['sourceId'],sourceSha256=source['sourceSha256'],numericReport=entry['report'],facetAssessment=ref(path),compilerDiagnostics=ref(diagnostic_path),visualMap=ref(visual_path) if visual else None))
    put(BASE/f'facet-capabilities-v{revision}.json',dict(version=f'v{revision}',sources=capabilities,visualFacets=case_rows,maximumRegisteredFacets=13,scope='Returned finite facets only; no broad family PASS, transferred v5/v6 closure, engine parity or fixture promotion'))
    result=runpy.run_path(str(BASE/'validate-evidence-v4.py'))['validate'](revision,integrity=False,preservation=limit==13)
    put(BASE/f'validation-result-v{revision}.json',result)
    creation=json.loads((BASE/'environment-v1/native-layout-create-response-v1.json').read_text());counts=result['counts']
    put(BASE/f'account-actions-v{revision}.json',dict(version=f'v{revision}',newLayout=dict(nativeId=creation['id'],image=creation['image_url'],name='oracle-v104-v1',pageId=16),returnedSourceSlots=limit,maximumSourceSlots=13,returnedNativeCounts=counts,retries=0,inputVariants=0,historyActions=0,subsequentSettingsChanges=0,oldLayoutEdits=0,oldScriptsOverwritten=0,libraryActions=0,reconnectActions=0,publicationOrSharingActions=0,defaultVolumeRetained=True,endPreservationReturned=limit==13,mcpBridgeRestarts=1,nativePageIdRemap='environment-v2/page-id-remap-v1.json',actualBackendCalculationCount=None,backendCountStatus='UNOBSERVED; source workflow/session counts do not establish backend execution count'))
    lines=[f'# Oracle v104 response v{revision}','','Returned '+str(limit)+' of13 finite source slots; '+str(13-limit)+' remain unreturned. '+('Every finite slot has ended.' if limit==13 else 'The same one NEW layout remains reserved for the remaining independent slots.')+' Exact native source bytes and body-only compiler transports are preserved, with zero retries/source repairs/input variants/history actions; only the preregistered initial new-layout zoom setup was used. Native outcomes remain observations, not engine-supplied targets.','', '| Source | Native status | Original / closed / primary rows | Private identity |','| --- | --- | ---: | --- |']
    for attempt in inventory['attempts']:
        source=attempt['source'];session=attempt['sessions'][0] if attempt['sessions'] else None
        rows=(str(session['dataRows'])+' / '+str(session['independentlyClosedRows'])+' / '+str(len(session['selectedPrimaryClosedRowOrdinals']))) if session else 'UNOBSERVED'
        lines.append('| '+source['sourceId']+' | '+attempt['status']+' | '+rows+' | `'+str(source['privateScriptId'])+'` / '+str(source['privateVersion'])+' |')
    lines+=['','Primary selection is the unique one-time retained build anchor A>=240 and its exact own indices A−31..A inclusive, plus eight original physically closed predecessors A−39..A−32. Four rotated modulo8 cycles are required, with no phase0 start requirement, no matching-output filter and no alternate block search. Original input milliseconds equal native chart Unix seconds×1000; confirmation1 and timestamp+120<=actual export UTC independently establish closure. Real increasing timestamps need not have invented120-second continuity.','', 'Each admitted build-event getter/state channel is represented by **one closed event and31 intentional blanks**; unspecified native table values remain observations without an invented target, never32 independent getter observations. The4,608-cell maximum is prospective and includes context, intent and intentional blanks. Raw CSV columns/strings/blanks/ordinals and all developing/other/predecessor rows remain whole; excluded cells have explicit causes and zero primary scoring credit.','', 'Before Save, admitted sources have bounded native editor selections, exact exposed text ranges, independent overlap/cursor/complete-character coverage and assembled full-editor bytes. Save-form line-ending normalization is separate and exact before Add. No browser evaluation, hidden model inspection or clipboard/protocol substitute is used. Consumed verification stops retain zero compiler/execution credit even when later read-only diagnostics recover their entered text.']
    lines+=['', 'Slot13 merge stopped before full editor verification/Save during a Chrome MCP interruption. Pending input was terminated before one bridge restart. The recovered v104 editor exposed a default buffer; its persistence cause is UNOBSERVED. Numeric MCP page IDs changed and were rebound by native layout URL. No source repair/retry, native Save/Add/export/PNG or merge outcome is claimed. [Interruption evidence](v104-table-merge-v5/attempt-v1/source-entry-stop-v1.json), [page identity remap](environment-v2/page-id-remap-v1.json).']
    if (BASE/'ENTRY-VERIFICATION-CLARIFICATION-v1.md').exists():lines+=['', '[Editor verification clarification](ENTRY-VERIFICATION-CLARIFICATION-v1.md) separates abbreviated UI transcripts from the complete entered source recovered after the two consumed pre-Save stops. Neither recovered buffer was saved or executed.']
    for attempt,entry,capability in zip(inventory['attempts'],numeric['sources'],capabilities):
        source=attempt['source'];report=json.loads((ROOT/entry['report']['path']).read_text());assessment=json.loads((ROOT/capability['facetAssessment']['path']).read_text())
        lines+=['','**'+source['sourceId']+'**','','Numeric/context property statuses: `'+json.dumps(entry['propertyVerdicts'],sort_keys=True)+'`; '+str(entry['uniquePrimaryPlotCells'])+' unique primary plot cells. [Raw pointers and frozen contracts]('+source['sourceId']+'/numeric-results-v1.json), [per-facet decisions]('+source['sourceId']+'/facet-assessment-v1.json), [compiler channels]('+source['sourceId']+'/compiler-diagnostics-v1.json).']
        for family in report['numericAlternatives']:lines.append('- Raw CSV export policy '+family['title']+': supported `'+str(family['supportedVariantIds'])+'`; this does not supply a screen coordinate.')
        for facet in assessment['facets']:
            lines.append('- '+facet['facetId'].split(':',1)[1]+': **'+facet['verdict']+'** (`'+facet['outcome']+'`)'+('; '+'; '.join(facet['notObservedCauses']) if facet['notObservedCauses'] else '')+'.')
        if capability['visualMap']:lines+=['','The [DERIVED map]('+source['sourceId']+'/derived-region-map-v1.json) binds original PNG bytes/dimensions, source/private/session/CSV/closed anchor, native axes, fixed registered windows, pre-scoring uncertainty and actual control/occlusion observations. Unexposed font/DPI/frame metadata stay UNOBSERVED. The initial native zoom setup is documented separately; actual per-source PNG axes register every frozen window.']
        if (BASE/source['sourceId']/'step-certificate-v1.json').exists():lines+=['', '[Own modulo32 step/ruler/pixel certificate]('+source['sourceId']+'/step-certificate-v1.json) preserves separate ruler portions, both blue arms/verticals and strictly disjoint frozen candidate intervals.']
        if (BASE/source['sourceId']/'arrow-certificate-v1.json').exists():lines+=['', '[Native arrow morphology and closed sign/control certificate]('+source['sourceId']+'/arrow-certificate-v1.json) separates actual head/shaft/tip pixels from color, placement and control glyphs.']
        if source.get('sourceEntryStop'):lines+=['','[Consumed pre-Save stop]('+source['sourceId']+'/attempt-v1/source-entry-stop-v1.json): no Save/Add/export/PNG credit.']
        for channel in json.loads((ROOT/capability['compilerDiagnostics']['path']).read_text())['transports']:
            if channel['success'] is False:lines+=['','Native '+channel['kind']+' refusal: `'+json.dumps(dict(reason=channel['reason'],reason2=channel['reason2']),ensure_ascii=False)+'`. Original ordered diagnostics and positions remain separate from editor-marker completeness.']
    lines+=['', 'Independent validation: **'+result['status']+'**. Returned evidence contains '+str(counts.get('originalCSVs',0))+' original CSVs, '+str(counts.get('nativeRenderingPNGs',0))+' original render PNGs, '+str(counts.get('primaryRows',0))+' primary rows and '+str(counts.get('uniquePrimaryPlotCells',0))+' unique requested primary plot cells. Returned source actions: '+str(counts.get('nativeSaves',0))+' PRIVATE Saves, '+str(counts.get('nativeAdds',0))+' Adds and '+str(counts.get('compilerBodies',0))+' separately preserved compiler bodies. Unreturned slots are excluded from these return counts, not assigned prospective observations.','', 'Only new layout `'+str(creation['id'])+'/'+creation['image_url']+'` (`oracle-v104-v1`), BINANCE:BTCUSDT2m Candles Etc/UTC. Native default Vol retained. [Initial viewport registration](environment-v1/viewport-preregistration-v1.json) precedes every source attempt; no later viewport/settings rescue. '+('End passive preservation is returned.' if limit==13 else 'End passive preservation awaits the remaining slots; original19 saved records and15 old-tab baselines are retained.')+' P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action. Prior contexts are not edited/restored. Historical holds1/2/7/8/13/14/21 and all earlier finite limits remain held.','', 'No publication/sharing/visibility change, alerts, account/entitlement/reconnect action, import, old script overwrite, history/replay/reload/recalculation, engine fix, fixture promotion or universal parity assertion. Unexposed backend calculation/feed/frame/execution identities remain UNOBSERVED.','', 'Run `python3 v104/captures/v104/validate-evidence-v4.py '+str(revision)+'`. [Inventory](attempt-inventory-v'+str(revision)+'.json), [numeric index](numeric-controls-v'+str(revision)+'.json), [frozen numeric contracts](numeric-contracts-v1.json), [facets](facet-capabilities-v'+str(revision)+'.json), [validation](validation-result-v'+str(revision)+'.json), [account actions](account-actions-v'+str(revision)+'.json), [integrity](artifact-integrity-v'+str(revision)+'.json) and [tooling license](CAPTURE-TOOLING-LICENSE-v1.md).']
    path=BASE/f'RESPONSE-v104-v{revision}.md';content='\n'.join(lines)+'\n'
    if path.exists():assert path.read_text()==content
    else:path.write_text(content)
    included={a['source']['sourceId'] for a in inventory['attempts']};records=[]
    for path in (ROOT/'v104').rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts or path.name.startswith('.') or path==BASE/f'artifact-integrity-v{revision}.json':continue
        relative=path.relative_to(BASE) if path.is_relative_to(BASE) else None
        if relative and relative.parts[0] in assets and relative.parts[0] not in included:continue
        records.append(ref(path))
    records.append(ref(ROOT/'v102/captures/v102/audit-request-v1.py'))
    put(BASE/f'artifact-integrity-v{revision}.json',dict(version=f'v{revision}',scope='All frozen v104 inputs, returned captures and derived/tooling dependencies; original body-only transports; self excluded; unreturned source attempt directories excluded',artifacts=sorted(records,key=lambda r:r['path'])))
    return result


if __name__=='__main__':print(json.dumps(package_round(int(sys.argv[1]),int(sys.argv[2])),indent=2))
