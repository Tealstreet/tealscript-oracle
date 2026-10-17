import json
import runpy
import sys
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
PACKAGE = runpy.run_path(str(BASE / 'package-evidence-v1.py'))
ref, put = PACKAGE['ref'], PACKAGE['put']


def package_round(revision=1):
    inventory = PACKAGE['package'](1, revision)
    numeric = runpy.run_path(str(BASE / 'analyze-evidence-v1.py'))['analyze'](revision)
    put(BASE / f'numeric-controls-v{revision}.json', numeric)
    attempt = inventory['attempts'][0]
    source, session = attempt['source'], attempt['sessions'][0]
    directory = (ROOT / source['receipt']['path']).parent
    diagnostics = []
    for kind in ['saveBody', 'addBody']:
        body = json.loads((ROOT / source[kind]['path']).read_text())
        meta = (body.get('result') or {}).get('metaInfo', {})
        reason = body.get('reason2')
        diagnostics.append(dict(kind=kind, body=source[kind], nativeSuccess=body.get('success'), nativeReason=body.get('reason'), nativeReason2=reason, nativeStructuredErrors=reason.get('errors') if isinstance(reason, dict) else None, structuredErrorChannelStatus='EXPOSED' if isinstance(reason, dict) and 'errors' in reason else 'UNOBSERVED / no independent array exposed', nativeWarnings=meta.get('warnings'), warningChannelStatus='EXPOSED' if 'warnings' in meta else 'UNOBSERVED', nativeEditorMarkerArrays=None, nativeEditorMarkerArrayStatus='UNOBSERVED; separate immediate/settled UI retained'))
    diagnostic_path = directory / 'compiler-diagnostics-v1.json'
    put(diagnostic_path, dict(version='v1', sourceId=source['sourceId'], sourceSha256=source['sourceSha256'], transports=diagnostics))
    preservation_path = BASE / 'environment-v2/existing-layout-comparison-v1.json'
    preservation = json.loads(preservation_path.read_text())
    creation = json.loads((BASE / 'environment-v1/native-layout-create-response-v1.json').read_text())
    put(BASE / f'account-actions-v{revision}.json', dict(version=f'v{revision}', newLayout=dict(nativeId=creation['id'], image=creation['image_url'], name='oracle-v101-v1', pageId=13), nativeSaves=1, nativeAdds=1, originalCsvExports=1, sourceInputWorkflowSessions=1, actualNativeCalculationCount=None, actualNativeCalculationCountStatus='UNOBSERVED', sourceRetries=0, inputVariants=0, historyNavigation=0, ownStudiesRemoved=1, newLayoutSavedAfterCleanup=True, builtinVolume='Native default Vol retained', forbiddenActionsTaken=[], privateLibrary='P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action', oldPrivateScriptInventory='UNOBSERVED; distinct new private Save, no old overwrite/rename/delete', passivePreservation=ref(preservation_path), preservationToolError=ref(BASE / 'environment-v2/preservation-tool-error-v1.json'), engineChangesOrFixturePromotion=False))
    put(BASE / f'facet-capabilities-v{revision}.json', dict(version=f'v{revision}', source=source, primaryInputCertificate=session['primaryInputCertificateValid'], contexts=numeric['contextProperties'], newDiscriminator=numeric['discriminator'], completeWitnessVectors={m['modelId']:m['verdict'] for m in numeric['models']}, repeatedControlVerdict=numeric['priorControlVerdict'], priorSurfaceExtrapolation=numeric['priorSurfaceExtrapolation'], compilerDiagnostics=ref(diagnostic_path), preservation=ref(preservation_path), held=numeric['unobserved'], encodingLimit=numeric['encodingLimit'], historicalHolds='Unchanged; no retroactive capture credit'))
    result = runpy.run_path(str(BASE / 'validate-evidence-v1.py'))['validate'](revision, integrity=False)
    put(BASE / f'validation-result-v{revision}.json', result)
    counts = result['counts']
    lines = [f'# Oracle v101 response v{revision}', '', '**'+numeric['modelSummary']+'** on the complete frozen37-code source vector. DIRECT_RGB_NEW_90_EQ is raw `1` on all64 selected owned physically closed rows. CM-A is REFUTED; CM-B is SUPPORTED for this finite unchanged-source execution. All36 repeated color-code controls match their independently retained v100 reference. No universal native algorithm or hidden byte identity follows.', '', '| Source | Native status | Private source / version | Original / closed / primary rows |', '| --- | --- | --- | --- |', '| '+source['sourceId']+' | '+attempt['status']+' | `'+source['privateScriptId']+'` / '+source['privateVersion']+' | '+str(session['dataRows'])+' / '+str(session['independentlyClosedRows'])+' / '+str(len(session['selectedPrimaryConsecutiveClosedRows']))+' |', '', 'Requested/executed source SHA256 `'+source['sourceSha256']+'`,4895 bytes,40 plots. The first4768 bytes are the exact v100 source; the original V100 indicator title is intentionally preserved. The distinct native PRIVATE Save/version and full Save/Add metadata bind ownership beyond that title. Separate complete compiler bodies and raw Save-form transport retain CRLF-only normalization. One source entry, PRIVATE Save, Add, original CSV and unchanged input session; zero source retries, input variants, history actions, reloads or forced recalculations.', '', 'Native source Save request321 and Add request325 both succeeded. No runtime error was exposed. [Compiler diagnostics]('+str(diagnostic_path.relative_to(BASE))+') retain each genuinely exposed warning/error channel separately; independent editor marker arrays remain UNOBSERVED. Immediate/settled source-owned UI and screenshots are archived.', '', 'Original CSV SHA256 `'+session['csv']['sha256']+'`; all46 columns and301 rows are preserved unchanged, including main chart and native builtin Vol. Primary selection is the first64 consecutive independently closed source-owned rows, original ordinals1–64: increasing timestamps and consecutive own INPUT_INDEX, source millisecond INPUT_TIME matching chart Unix seconds, physical2m close before actual native export UTC and CHART_CONFIRMED1. No result/model agreement selects rows; no own-origin/predecessor requirement or forced120-second spacing. Every outside/developing cell remains OBSERVED / EXCLUDED in the closure mask with exact cause and zero primary credit.', '', '| Model | New-column property | Complete37-code vector |', '| --- | --- | --- |']
    for model in numeric['models']:
        lines.append('| '+model['modelId']+' | '+numeric['discriminator']['perColumnVerdicts'][model['modelId']]+' | '+model['verdict']+' |')
    lines += ['', '| Source plot ordinal | Numeric column | Actual raw counts on primary rows | CM-A expected | CM-B expected |', '| ---: | --- | --- | ---: | ---: |']
    for a, b in zip(numeric['models'][0]['properties'], numeric['models'][1]['properties']):
        lines.append('| '+str(a['sourcePlotOrdinal'])+' | '+a['title']+' | `'+json.dumps(a['observedRawCounts'], sort_keys=True)+'` | '+a['expectedRawCode']+' | '+b['expectedRawCode']+' |')
    first = numeric['discriminator']['firstOwnedClosedCell']
    lines += ['', 'First new-code target: original CSV-SHA `'+first['csvSha256']+'`, data row'+str(first['rowOrdinal'])+', column'+str(first['columnOrdinal'])+', header `'+first['headerRaw']+'`, raw `'+first['valueRaw']+'`. Every model/property record retains its exact frozen prediction-file SHA/JSON pointer, recipe-file SHA/JSON pointer, all source plot ordinals, every actual CSV-SHA/row/column/header/raw pointer and S/R/U comparison. Present blanks/unexpected numeric codes are contrary observations; absent ownership is held. Matching partial data never supports a complete vector.', '', 'All three context properties are independently SUPPORTED on the selected block. All2304 repeated-control targets are from this new export and match the separately pointed previous source values. Old controls supply provenance only; no old cell fills an absent new target. This is bounded repeated-control agreement, without a new audit of the entire historical23448-cell surface.', '', 'The frozen v5 helper is exactly `value ? 1 : 0`: code0 collapses false and Boolean NA. Exported numeric codes establish neither defined false/non-missingness nor hidden color/byte identity. All omitted NA/getter/calibration channels, generic equality, missing-color casts, gradient algorithms and unqueried inputs remain UNOBSERVED / HELD. No third model, tolerance, fitted quantizer, source change or post-capture fit is introduced.', '', 'Read-only validation: **'+result['status']+'**; '+str(counts['uniquePrimaryPlotCells'])+' unique primary plot cells =192 context +2304 repeated controls +64 new-query cells. Color-code cells total2368. The4736 model/cell comparisons are repeated analysis relations, not additional native cells or parity credit.', '', 'Only NEW layout `'+str(creation['id'])+'/'+creation['image_url']+'` (`oracle-v101-v1`) was used. Its own study is removed and the new layout saved; native default Vol retained. Passive comparison shows16/16 old saved records and12/12 old open-tab signatures unchanged. P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action. Full private inventory, native feed/execution IDs and actual backend calculation count remain UNOBSERVED.', '', 'A preservation-tool element lookup used an old-page snapshot with the new-page click target; the native lookup rejected it before any click. [Error receipt](environment-v2/preservation-tool-error-v1.json) and both workflow versions are retained. Passive inventory collection continued on the correct new page, without repeating source entry/Save/Add/export or the new-layout Save. No old layout/script/tab edit, reload, rename, deletion, restoration, account action, publication/share/visibility, alert or library import occurred. Historical preservation/semantic holds remain held.', '', f'Run `python3 v101/captures/v101/validate-evidence-v1.py {revision}`. [Inventory](attempt-inventory-v{revision}.json), [numeric controls/properties](numeric-controls-v{revision}.json), [facets](facet-capabilities-v{revision}.json), [validation](validation-result-v{revision}.json), [account actions](account-actions-v{revision}.json), [preservation](environment-v2/existing-layout-comparison-v1.json), [integrity](artifact-integrity-v{revision}.json) and [tooling license](CAPTURE-TOOLING-LICENSE-v1.md). Integrity binds every dependency/return path, length and SHA256, self-excluded. No engine change, fixture promotion, generic color/identity, pixel/CSS/DPI contract, original-frontier reconstruction or historical-hold closure.']
    response = BASE / f'RESPONSE-v101-v{revision}.md'
    content = '\n'.join(lines) + '\n'
    if response.exists():
        assert response.read_text() == content
    else:
        response.write_text(content)
    files = [p for p in (ROOT / 'v101').rglob('*') if p.is_file() and '__pycache__' not in p.parts and not p.name.startswith('.') and p != BASE / f'artifact-integrity-v{revision}.json']
    manifest = json.loads((ROOT / 'v101/bundle-manifest-v1.json').read_text())
    files += [ROOT / p['path'] for p in manifest['priorEvidence']]
    put(BASE / f'artifact-integrity-v{revision}.json', dict(version=f'v{revision}', scope='All v101 request/source/prediction/native/derived dependencies and returns, self-excluded; body-only transports, no authentication headers', artifacts=[ref(p) for p in sorted(set(files))]))
    return result


if __name__ == '__main__':
    print(json.dumps(package_round(int(sys.argv[1]) if len(sys.argv) > 1 else 1), indent=2))
