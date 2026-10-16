import json
import runpy
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
PACKAGE = runpy.run_path(str(BASE / 'package-evidence-v1.py'))
ref, put = PACKAGE['ref'], PACKAGE['put']


def package_round():
    inventory = PACKAGE['package']()
    numeric = runpy.run_path(str(BASE / 'analyze-evidence-v1.py'))['analyze']()
    put(BASE / 'numeric-controls-v1.json', numeric)
    diagnostics = []
    for attempt in inventory['attempts']:
        source = attempt['source']
        directory = (ROOT / source['receipt']['path']).parent
        transports = []
        for kind in ['saveBody', 'addBody']:
            if source[kind] is None:
                continue
            body = json.loads((ROOT / source[kind]['path']).read_text())
            meta = (body.get('result') or {}).get('metaInfo', {})
            reason = body.get('reason2')
            transports.append({'kind': kind, 'body': source[kind], 'nativeSuccess': body.get('success'), 'nativeReason': body.get('reason'), 'nativeReason2': reason, 'nativeStructuredErrors': reason.get('errors') if isinstance(reason, dict) else None, 'structuredErrorChannelStatus': 'EXPOSED' if isinstance(reason, dict) and 'errors' in reason else 'UNOBSERVED / independent error array absent', 'nativeWarnings': meta.get('warnings'), 'warningChannelStatus': 'EXPOSED' if 'warnings' in meta else 'UNOBSERVED', 'nativeEditorMarkerArrays': None, 'nativeEditorMarkerArrayStatus': 'UNOBSERVED; immediate/settled native UI retained separately'})
        path = directory / 'compiler-diagnostics-v1.json'
        put(path, {'version': 'v1', 'sourceId': source['sourceId'], 'sourceSha256': source['sourceSha256'], 'transports': transports})
        diagnostics.append(ref(path))
    put(BASE / 'facet-capabilities-v1.json', {'version': 'v1', 'numericEvidence': ref(BASE / 'numeric-controls-v1.json'), 'sources': [{k: value for k, value in report.items() if k in ['sourceId', 'sourceSha256', 'nativeCompileSuccess', 'captureStatus', 'propertyVerdicts', 'comparisonCounts', 'facets', 'selectedDataRowOrdinals']} for report in numeric['sources']], 'compilerDiagnostics': diagnostics, 'residualHolds': {'hiddenPackedRepresentation': 'UNOBSERVED; only ordinary Pine literal equality/getters', 'universalQuantizer': 'UNDECIDED; no post-capture fitting or normalization', 'nativeExecutionIdsAndMarkerArrays': 'UNOBSERVED', 'rasterParity': 'NOT REQUESTED', 'engineApprovalAndHistoricalHolds': 'UNCHANGED / NO APPROVAL'}})
    receipts = [json.loads((ROOT / a['source']['receipt']['path']).read_text()) for a in inventory['attempts']]
    put(BASE / 'account-actions-v1.json', {'version': 'v1', 'newLayout': {'nativeId': 208235696, 'image': 'SaYl4TD3', 'name': 'oracle-v96-v1', 'pageId': 8}, 'sourceSlots': len(receipts), 'nativeSaveAttempts': len(receipts), 'nativeAddAttempts': sum(a['source']['addBody'] is not None for a in inventory['attempts']), 'originalCsvExports': sum(len(a['sessions']) for a in inventory['attempts']), 'unchangedSourceSettingsSessions': len(receipts), 'actualNativeCalculationSessionCount': None, 'includedOwnStudiesRemoved': sum(bool(r.get('removed')) for r in receipts), 'sourceRetries': 0, 'inputVariants': 0, 'calendarOrHistoryActions': 0, 'maximumBudget': {'saves': 2, 'adds': 2, 'csvs': 2, 'sessions': 2}, 'builtinVolume': 'Default Vol · BTC retained', 'newLayoutSavedAfterCleanup': True, 'preservationEvidence': 'v96/captures/v96/environment-v2/existing-layout-comparison-v1.json', 'privateLibrary': 'sours-lat/P425PrivateV79v1/1 unchanged; no action', 'P425Layout': 'Name not exposed in full native saved list; no action', 'forbiddenActionsTaken': [], 'engineChangesOrFixturePromotion': False})
    result = runpy.run_path(str(BASE / 'validate-evidence-v1.py'))['validate'](check_integrity=False)
    put(BASE / 'validation-result-v1.json', result)
    lines = ['# Oracle v96 response v1', '', 'The two finite source slots are returned with native observations and explicit property holds. Both exact sources saved and added successfully; four complete exposed compiler bodies and two original CSVs are retained. No source repair, repeat, input change or history navigation occurred.', '', '| Source | Original rows | Independently closed | Comparison rows | Private source/version |', '| --- | ---: | ---: | --- | --- |']
    for attempt in inventory['attempts']:
        source = attempt['source']
        for session in attempt['sessions']:
            selected = session['selectedFirst32ConsecutiveClosedRows']
            lines.append(f"| {source['sourceId']} | {session['dataRows']} | {session['independentlyClosedRows']} | {selected[0]}–{selected[-1]} | `{source['privateScriptId']}` / {source['privateVersion']} |")
    lines += ['', 'All five cases and controls use that same first32 consecutive source-bound closed rows in each version. Physical two-minute closure, export UTC, own millisecond INPUT_TIME and CHART_CONFIRMED are jointly checked. Every original row, column, raw string and excluded developing cell is retained. Own index-zero is not required for these pointwise constants.', '', '| Source / case | R / G / B / T / NA | Floor / half-up / pre-T flags | Equality observation |', '| --- | --- | --- | --- |']
    for report in numeric['sources']:
        row = report['rows'][0]
        for case in row['cases']:
            channels = ' / '.join(p['valueRaw'] for p in case['actualChannelCells'])
            flags = ' / '.join(p['valueRaw'] for p in case['actualEqualityCells'].values())
            same = all(other['cases'][row['cases'].index(case)]['actualChannelCells'][i]['valueRaw'] == p['valueRaw'] for other in report['rows'] for i, p in enumerate(case['actualChannelCells']))
            assert same
            assert all([p['valueRaw'] for p in other['cases'][row['cases'].index(case)]['actualEqualityCells'].values()] == [p['valueRaw'] for p in case['actualEqualityCells'].values()] for other in report['rows'])
            lines.append(f"| {report['sourceId']} / {case['case']} | {channels} | {flags} | {case['equalityObservation']} |")
    lines += ['', 'These tuples are actual raw values, repeated on all32 selected rows per source. Case inputs and every actual channel/equality/control pointer, original row/column ordinal, source hash and independent frozen hypothesis are in [numeric controls v1](numeric-controls-v1.json). A unique calibrated literal match supports equality to that explicit literal only; it does not inspect hidden storage or certify a universal alpha algorithm. NEITHER and calibration contradictions remain observations without inventing a byte.', '', '| Source | EQ_SELF / EQ_DISTINCT | CTOR12_5_T / EQ_DF | Literal DF / E0 / DE T | CTOR50_EQ_80 | MISSING_LOWER_NA |', '| --- | --- | --- | --- | --- | --- |']
    for report in numeric['sources']:
        values = {p['headerRaw']: p['valueRaw'] for p in report['rows'][0]['allRequestedRawCells']}
        groups = [['EQ_SELF', 'EQ_DISTINCT'], ['CTOR12_5_T', 'CTOR12_5_EQ_DF'], ['LITERAL_DF_T', 'LITERAL_E0_T', 'LITERAL_DE_T'], ['CTOR50_EQ_80'], ['MISSING_LOWER_NA']]
        assert all(all({p['headerRaw']: p['valueRaw'] for p in row['allRequestedRawCells']}[title] == values[title] for titles in groups for title in titles) for row in report['rows'])
        lines.append('| ' + report['sourceId'] + ' | ' + ' | '.join(' / '.join(values[t] for t in group) for group in groups) + ' |')
    lines += ['', 'Constructor and missing-endpoint control contradictions receive explicit contrary records; they never filter rows or replace gradient observations. The nominal endpoint T controls and all remaining raw calibration getters are separately retained. No byte identity follows from T50 alone. The exported CSV has no colorer value column; native colorer metadata is archived without fabricating an exported value or decoding a packed format.', '', f"Read-only validation: `{result['status']}`; {result['dataRows']} original rows, {result['independentlyClosedRows']} independently closed rows, {result['numericComparisons']} named scalar/model records, {result['rawCellPointers']} raw pointer references. Those counts are model records/references, not unique cells. Full per-hypothesis SUPPORTED/REFUTED/UNDECIDED counts are in [validation result v1](validation-result-v1.json) and [facet capabilities v1](facet-capabilities-v1.json).", '', 'Only new layout `208235696/SaYl4TD3` (`oracle-v96-v1`) was used and saved after both own studies were removed; builtin Volume remains. The full native list and passive snapshots establish all11 prior saved records and all7 prior open-tab signatures unchanged, including v95 and the pre-existing v91 saved/open context discrepancy. See [preservation comparison](environment-v2/existing-layout-comparison-v1.json) and [account actions](account-actions-v1.json). P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action.', '', 'Exact requested/executed hashes, CRLF-only Save-form transport normalization, private metadata, separate Save/Add bodies and immediate/settled UI are retained per source. Independent editor marker arrays, native execution/feed identities and actual native recalculation counts remain UNOBSERVED. No native compilation refusal occurred; complete exposed warning/error channels are preserved separately, with unavailable arrays explicitly UNOBSERVED.', '', 'Run `python3 v96/captures/v96/validate-evidence-v1.py` from repository root. [Integrity v1](artifact-integrity-v1.json) covers the request, frozen sources and all returned artifacts, self-excluded. New capture tooling rights are separately recorded in [tooling license v1](CAPTURE-TOOLING-LICENSE-v1.md).', '', 'This return does not approve7f006314, update application expectations, waive the earlier value-vector failure, resolve every QA finding(B), promote fixtures, grant pixel/DPI/CSS parity or close historical holds. Consumption and crossed QA remain required.']
    response = BASE / 'RESPONSE-v96-v1.md'
    data = '\n'.join(lines) + '\n'
    if response.exists():
        assert response.read_text() == data
    else:
        response.write_text(data)
    files = [p for p in (ROOT / 'v96').rglob('*') if p.is_file() and not p.name.startswith('.') and '__pycache__' not in p.parts and p.name != 'artifact-integrity-v1.json']
    put(BASE / 'artifact-integrity-v1.json', {'version': 'v1', 'scope': 'All v96 request/frozen sources and returned native/derived artifacts; self-excluded. Body-only transport, no auth headers.', 'files': [ref(p) for p in sorted(files)]})
    return result


if __name__ == '__main__':
    print(json.dumps(package_round(), indent=2))
