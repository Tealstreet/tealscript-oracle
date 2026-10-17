import json
import runpy
import sys
from pathlib import Path

sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
PACKAGE=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put=PACKAGE['ref'],PACKAGE['put']


def package_round(limit=3,revision=1):
    inventory=PACKAGE['package'](limit,revision)
    numeric=runpy.run_path(str(BASE/'analyze-evidence-v1.py'))['analyze'](revision,write=True)
    put(BASE/f'numeric-controls-v{revision}.json',numeric)
    diagnostics=[]
    for attempt in inventory['attempts']:
        source=attempt['source'];directory=(ROOT/source['receipt']['path']).parent;records=[]
        for kind in ['saveBody','addBody']:
            if source[kind] is None:continue
            body=json.loads((ROOT/source[kind]['path']).read_text());meta=(body.get('result') or {}).get('metaInfo',{});reason=body.get('reason2')
            records.append(dict(kind=kind,body=source[kind],nativeSuccess=body.get('success'),nativeReason=body.get('reason'),nativeReason2=reason,nativeStructuredErrors=reason.get('errors') if isinstance(reason,dict) else None,structuredErrorChannelStatus='EXPOSED' if isinstance(reason,dict) and 'errors' in reason else 'UNOBSERVED / no independent array exposed',nativeWarnings=meta.get('warnings'),warningChannelStatus='EXPOSED' if 'warnings' in meta else 'UNOBSERVED',nativeEditorMarkerArrays=None,nativeEditorMarkerArrayStatus='UNOBSERVED; native immediate/settled UI preserved separately'))
        path=directory/'compiler-diagnostics-v1.json';put(path,dict(version='v1',sourceId=source['sourceId'],sourceSha256=source['sourceSha256'],transports=records));diagnostics.append(ref(path))
    preservation=json.loads((BASE/'environment-v2/existing-layout-comparison-v1.json').read_text()) if limit==3 else None
    put(BASE/f'facet-capabilities-v{revision}.json',dict(version=f'v{revision}',sources=[dict(sourceId=r['sourceId'],sourceSha256=r['sourceSha256'],pineVersion=r['pineVersion'],nativeCompileSuccess=r['nativeCompileSuccess'],completePrimaryInputCertificate=r['completePrimaryInputCertificate'],primaryRows=r['primaryRowOrdinals'],scopes=[dict(family=s['family'],adjudication=s['adjudication'],scope=s['scope']) for s in r['scopes']],unobserved=r['unobserved']) for r in numeric['sources']],classVerdicts=numeric['classVerdictCounts'],scopedRepresentativeVerdicts=numeric['scopedRepresentativeVerdictCounts'],sharedMaterialization=numeric['sharedMaterialization'],compilerDiagnostics=diagnostics,preservation=ref(BASE/'environment-v2/existing-layout-comparison-v1.json') if preservation else None,residualHolds=['False/Boolean-NA distinction for frozen v5 ternary0 is UNOBSERVED','No omitted getter/NA/literal-calibration values, hidden alpha byte, complete alias separation or universal quantizer','No engine/fixture/pixel contract approval or historical-hold closure']))
    creation=json.loads((BASE/'environment-v1/native-layout-create-response-v1.json').read_text())
    put(BASE/f'account-actions-v{revision}.json',dict(version=f'v{revision}',newLayout=dict(nativeId=creation['id'],image=creation['image_url'],name='oracle-v100-v1',pageId=12),includedSlots=len(inventory['attempts']),maximumSavesAddsExportsSessions=3,nativeSaves=sum(a['source']['saveBody'] is not None for a in inventory['attempts']),nativeAdds=sum(a['source']['addBody'] is not None for a in inventory['attempts']),originalCsvExports=sum(len(a['sessions']) for a in inventory['attempts']),includedOwnStudiesRemoved=sum(bool(a['removed']) for a in inventory['attempts']),retries=0,inputVariants=0,historyOrCalendarActions=0,actualNativeCalculationCount=None,nativeCalculationCountStatus='UNOBSERVED; source/input workflow sessions only',newLayoutSavedAfterCleanup=limit==3,builtinVolume='Native default Vol retained; never added/removed',privateLibrary='P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action',oldScripts='No overwrite/rename/delete; distinct new PRIVATE Save identities. Full private script inventory remains UNOBSERVED.',forbiddenActionsTaken=[],engineChangesOrFixturePromotion=False))
    result=runpy.run_path(str(BASE/'validate-evidence-v1.py'))['validate'](revision,integrity=False,preservation=limit==3)
    put(BASE/f'validation-result-v{revision}.json',result)
    counts=result['counts'];lines=[f'# Oracle v100 response v{revision}','','Native evidence is returned for '+str(limit)+' of three finite slots. '+('All three slots have ended.' if limit==3 else 'Remaining independent slots have not yet been returned.')+' Exact accepted-proposal source bytes/titles are preserved, with one PRIVATE Save/Add/export per successful slot, separate complete compiler bodies and no source repair, retry, input variant, history navigation, reload or forced recalculation.','', '| Source | Native status | Original / closed rows | Primary row ordinals | New private source/version |','| --- | --- | ---: | --- | --- |']
    for attempt in inventory['attempts']:
        source=attempt['source'];session=attempt['sessions'][0] if attempt['sessions'] else None;selected=session['selectedPrimaryConsecutiveClosedRows'] if session else []
        lines.append('| '+source['sourceId']+' | '+attempt['status']+' | '+(str(session['dataRows'])+' / '+str(session['independentlyClosedRows']) if session else 'UNOBSERVED')+' | '+(str(selected[0])+'–'+str(selected[-1]) if selected else 'NOT OBSERVED')+' | `'+str(source['privateScriptId'])+'` / '+str(source['privateVersion'])+' |')
    lines+=['','Slot1 uses its first64 source-owned independently closed consecutive rows. Materialization sources independently use first76 such rows starting CASE_ID0, with CASE_ID=INPUT_INDEX%19 and four visits/phase. Closure checks original Unix seconds, own millisecond INPUT_TIME, source indices, physical2m close, export UTC and CHART_CONFIRMED. No getter/code/model agreement selects rows. All original rows/columns/strings/blanks remain archived; the explicit masks assign zero primary credit and exact exclusion causes to every outside/developing cell. No prefix, predecessor, original-frontier or sampling-completeness claim.','']
    for report in numeric['sources']:
        lines+=['','**'+report['sourceId']+'**','']
        for scope in report['scopes']:
            proof=scope['adjudication']
            lines.append('- '+scope['family']+': **'+proof['observation']+'**; supported classes `'+str(proof['supportedClassIds'])+'`; '+str(len(proof['supportedModelIds']))+' supported representative IDs; class counts `'+json.dumps(proof['classVerdictCounts'],sort_keys=True)+'`.')
        if 'directDiscriminator' in report:
            d=report['directDiscriminator']
            lines+=['','DIRECT_RGB_NEW_12P1_EQ raw tested-row counts: `'+json.dumps(d['rawObservedCodeCounts'],sort_keys=True)+'`. One-closed-cell D/F verdicts: `'+json.dumps(d['oneClosedCellVerdicts'],sort_keys=True)+'`. Complete19-column scalar-vector verdicts for those same IDs: `'+json.dumps(d['fullScalarClassVerdicts'],sort_keys=True)+'`. The first code distinguishes their predictions without supporting an otherwise refuted full vector.','', 'Scalar S and packing P scopes remain independent. S records predict exactly19 mapped codes; P records exactly17. No scalar/packing pairing forms a full model. Every P member retains its original file/row/getterRoute metadata link, including the38569 scalar-getter records with absent route field and7200 packed-byte-getter records. All supported/undecided/refuted model IDs remain enumerated in their immutable signature-class records.']
        else:
            block=json.loads((ROOT/report['nativeBlock']['path']).read_text());seen=set()
            lines+=['','| Phase | Actual NEW_R /G /B /T /EQ_C0 /EQ_C1 at first tested visit |','| ---: | --- |']
            for row in block['rows']:
                phase=row['phaseValue']
                if phase is None or phase in seen:continue
                seen.add(phase);points=[row['cells'].get(t) for t in ['NEW_R','NEW_G','NEW_B','NEW_T','NEW_EQ_C0','NEW_EQ_C1']]
                lines.append('| '+str(phase)+' | '+' / '.join('UNOBSERVED' if p is None else '∅' if p['valueRaw']=='' else p['valueRaw'] for p in points)+' |')
            lines+=['','The table summarizes first visits; every requested visit and contrary/mixed tuple is preserved in the native block and complete comparison masks. Candidate alpha labels are frozen hypothesis metadata, never recovered native bytes. Phase13 explicitly queries C7/199 in this new19-phase program; no old unqueried palette cell is filled.']
    shared=numeric['sharedMaterialization']['adjudication']
    lines+=['','**Shared v5/v6 B recipes**','', '**'+shared['observation']+'**; supported classes `'+str(shared['supportedClassIds'])+'`; '+str(len(shared['supportedModelIds']))+' shared supported B IDs. Each B ID must match both independently owned version vectors. Missing coverage holds cross-version support; an actual contrary version refutes the conjunction. No cross-version cell borrowing.','', 'The v5 helper is exactly `value ? 1 : 0`: code0 can represent false or Boolean NA. It is an observed numeric code, not proof of defined false, non-missingness or a stored color. These programs expose no NA predicate or independent literal-calibration graph. Omitted fields and hidden storage remain UNOBSERVED; no added model, tolerance, palette change, universal algorithm or complete-alias certificate is fitted.', '',f"Read-only validation: **{result['status']}**; {counts.get('dataRows',0)} original archive rows, {counts.get('independentlyClosedRows',0)} independently closed archive rows, {counts.get('primaryRows',0)} primary rows, {counts.get('uniquePrimaryPlotCells',0)} unique primary plot cells and {counts.get('uniquePrimaryColorCells',0)} unique primary color/getter/code cells. {counts.get('signatureClasses',0)} source-signature records represent {counts.get('scopedRepresentatives',0)} scoped model memberships. {counts.get('classCellComparisons',0)} class/cell comparisons and {counts.get('rawNativePointerReferences',0)} pointer references are repeated analysis relations, not native cells or extra parity credit.", '', 'Each class record binds the prediction-map/file SHA and JSON pointer, every member ID and original-record pointer rule, exact tested columns/phases, expected vector, native-cell-block SHA/row pointers and complete per-row S/R/U comparison mask. No contradictory cell is omitted: each mask position resolves to its exact original CSV-SHA/row/column/header/raw-string target in the shared native block. Per-column and per-phase property verdicts preserve partial coverage and causes. Projection auditing checks every member against its original frozen vector; grouping identical vectors never multiplies native cells.', '',f"Native actions: {counts.get('nativeSaves',0)} PRIVATE Saves, {counts.get('nativeAdds',0)} Adds, {counts.get('compilerBodies',0)} full compiler bodies and {counts.get('csvs',0)} original CSVs. No native refusal or runtime error was exposed in returned successful slots; immediate/settled UI and genuinely exposed warning/error channels remain separate from unexposed editor arrays.", '',f'Only new layout `{creation["id"]}/{creation["image_url"]}` (`oracle-v100-v1`) was used. '+('Every own study is removed and only the new layout saved; native default Vol remains.' if limit==3 else 'Final new-layout Save and preservation comparison await remaining finite slots.'),'','P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action. Full private inventory, independent editor arrays, native execution/feed IDs and actual backend calculation counts remain UNOBSERVED. No publication/share/visibility/account action or old layout/script/tab edit, reload, rename, deletion or restoration occurred. Historical holds remain unchanged.']
    if preservation:
        lines+=['',f"Passive preservation: {counts.get('oldSavedRecordsUnchanged',0)}/15 old saved records and {counts.get('oldOpenTabsUnchanged',0)}/11 old open-tab signatures unchanged; [comparison](environment-v2/existing-layout-comparison-v1.json) retains every before/after record."]
        for tab in preservation['openTabComparisons']:
            if not tab['equal']:lines+=['',f"PRESERVATION HOLD page{tab['pageId']}: `{json.dumps(tab['before'],sort_keys=True)}` → `{json.dumps(tab['after'],sort_keys=True)}`. Cause UNOBSERVED; no restoration performed."]
    lines+=['',f'Run `python3 v100/captures/v100/validate-evidence-v1.py {revision}`. [Inventory](attempt-inventory-v{revision}.json), [numeric controls/classes](numeric-controls-v{revision}.json), [facets](facet-capabilities-v{revision}.json), [validation](validation-result-v{revision}.json), [membership/projection audit](prediction-membership-audit-v1.json), [account actions](account-actions-v{revision}.json), [integrity](artifact-integrity-v{revision}.json) and [tooling rights](CAPTURE-TOOLING-LICENSE-v1.md) are independently bound. Integrity covers all request/source/prediction/native/derived dependencies and returns, self-excluded. No engine fix, fixture promotion, generic color/identity, pixel/CSS/DPI contract or historical-hold closure follows from this capture.']
    response=BASE/f'RESPONSE-v100-v{revision}.md';content='\n'.join(lines)+'\n'
    if response.exists():assert response.read_text()==content
    else:response.write_text(content)
    manifest=json.loads((ROOT/'v100/bundle-manifest-v1.json').read_text());all_ids={a['sourceId'] for a in manifest['sources']};included={a['source']['sourceId'] for a in inventory['attempts']};files=[]
    for p in (ROOT/'v100').rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts or p.name.startswith('.'):continue
        rel=p.relative_to(BASE) if p.is_relative_to(BASE) else None
        if rel and rel.parts[0] in all_ids and rel.parts[0] not in included:continue
        if p==BASE/f'artifact-integrity-v{revision}.json':continue
        files.append(p)
    files.extend(ROOT/r['path'] for r in manifest['priorEvidence'])
    put(BASE/f'artifact-integrity-v{revision}.json',dict(version=f'v{revision}',scope='All v100 request/source/prediction/native/derived dependencies and returned artifacts; self-excluded. Native transport bodies only, no auth headers.',artifacts=[ref(p) for p in sorted(set(files))]))
    return result


if __name__=='__main__':print(json.dumps(package_round(int(sys.argv[1]) if len(sys.argv)>1 else 3,int(sys.argv[2]) if len(sys.argv)>2 else 1),indent=2))
