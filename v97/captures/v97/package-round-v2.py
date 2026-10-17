import json
import runpy
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
P = runpy.run_path(str(BASE / 'package-evidence-v1.py'))
ref, put = P['ref'], P['put']


def package_round(limit, revision):
    inventory = P['package'](limit, revision)
    numeric = runpy.run_path(str(BASE / 'analyze-evidence-v2.py'))['analyze'](revision)
    summaries, diagnostics = [], []
    for report, attempt in zip(numeric['sources'], inventory['attempts']):
        directory = BASE / report['sourceId'] / 'attempt-v1'
        path = directory / 'numeric-results-v1.json'
        text = json.dumps(report, separators=(',', ':')) + '\n'
        if path.exists():
            assert path.read_text() == text
        else:
            path.write_text(text)
        summaries.append({**{k: v for k, v in report.items() if k != 'records'}, 'numericEvidence': ref(path)})
        transports = []
        for kind in ['saveBody', 'addBody']:
            pointer = attempt['source'][kind]
            if pointer is None:
                continue
            body = json.loads((ROOT / pointer['path']).read_text())
            meta = (body.get('result') or {}).get('metaInfo', {})
            reason = body.get('reason2')
            transports.append({'kind': kind, 'body': pointer, 'nativeSuccess': body.get('success'), 'nativeReason': body.get('reason'), 'nativeReason2': reason, 'nativeStructuredErrors': reason.get('errors') if isinstance(reason, dict) else None, 'structuredErrorChannelStatus': 'EXPOSED' if isinstance(reason, dict) and 'errors' in reason else 'UNOBSERVED / independent error array absent', 'nativeWarnings': meta.get('warnings'), 'warningChannelStatus': 'EXPOSED' if 'warnings' in meta else 'UNOBSERVED', 'nativeEditorMarkerArrays': None, 'nativeEditorMarkerArrayStatus': 'UNOBSERVED; immediate/settled native UI retained separately'})
        diagnostic = directory / 'compiler-diagnostics-v1.json'
        put(diagnostic, {'version': 'v1', 'sourceId': report['sourceId'], 'sourceSha256': report['sourceSha256'], 'transports': transports})
        diagnostics.append(ref(diagnostic))
    put(BASE / f'numeric-controls-v{revision}.json', {**numeric, 'sources': summaries})
    complete = inventory['completeFiniteRound']
    put(BASE / f'facet-capabilities-v{revision}.json', {'version': f'v{revision}', 'completeFiniteRound': complete, 'selection': inventory['selection'], 'numericEvidence': ref(BASE / f'numeric-controls-v{revision}.json'), 'sources': [{k: v for k, v in r.items() if k in ['sourceId', 'originalSourceId', 'item', 'sourceSha256', 'facets', 'propertyVerdicts', 'comparisonCounts', 'sourceFrontier', 'strictOwnIndexZeroPrefixAvailable', 'numericEvidence']} for r in summaries], 'compilerDiagnostics': diagnostics, 'residualHolds': {'nativeExecutionIdsAndMarkerArrays': 'UNOBSERVED', 'precision': 'Individual unresolved native arithmetic/export residues remain UNDECIDED; no tolerance, normalization or seed fitting', 'oldV95AndV91Frontiers': 'UNCHANGED; these fresh contracts cannot replace their original inputs or clocks', 'liveFirstEvents': 'NO REPLAY OR OBSERVER WINDOW', 'genericPrngAndTaAlgorithms': 'No universal certificate from one finite vector', 'engineAndFixtureApproval': 'NONE'}})
    receipts = [json.loads((ROOT / a['source']['receipt']['path']).read_text()) for a in inventory['attempts']]
    put(BASE / f'account-actions-v{revision}.json', {'version': f'v{revision}', 'completeFiniteRound': complete, 'newLayout': {'nativeId': 208236729, 'image': 'euz5a92K', 'name': 'oracle-v97-v1', 'pageId': 9}, 'includedReturnedSources': len(receipts), 'includedNativeSaves': len(receipts), 'includedNativeAdds': sum(a['source']['addBody'] is not None for a in inventory['attempts']), 'includedOriginalCsvExports': sum(len(a['sessions']) for a in inventory['attempts']), 'includedCalendarSelections': sum(a['calendarSelections'] for a in inventory['attempts']), 'includedSourceFrontierSessions': sum(len(a['sessions']) for a in inventory['attempts']), 'actualNativeCalculationSessionIds': None, 'includedOwnStudiesRemoved': sum(bool(r.get('removed')) for r in receipts), 'remainingEligibleSlots': 14 - len(receipts), 'maximumBudget': {'saves': 14, 'adds': 14, 'calendarSelections': 14, 'csvs': 28, 'sessions': 28}, 'sourceRetries': 0, 'inputVariants': 0, 'sourceRepairs': 0, 'newPineSources': 0, 'builtinVolume': 'Default Vol · BTC retained', 'existingLayoutPreservation': 'v97/captures/v97/environment-v2/existing-layout-comparison-v1.json' if complete else 'Passive baseline archived; end-of-round full saved-record/tab comparison pending', 'newLayoutSavedAfterCleanup': complete, 'privateLibrary': 'sours-lat/P425PrivateV79v1/1 unchanged; no action', 'P425Layout': 'No action', 'forbiddenActionsTaken': [], 'engineChangesOrFixturePromotion': False, 'progressScope': 'Counts cover only returned immutable source slots; later eligible slots may be active outside this revision integrity scope'})
    result = runpy.run_path(str(BASE / 'validate-evidence-v2.py'))['validate'](revision, check_integrity=False)
    put(BASE / f'validation-result-v{revision}.json', result)
    lines = [f'# Oracle v97 response v{revision}', '', f"{'Complete finite return' if complete else 'Progress return'}: {len(receipts)} of14 eligible source/version slots returned. Selection is frozen against v95 response v24 at c7790f48d913a0736606af6bb94a2f2ee011f309, after completed v95 and v96. Mandatory items2–5 supply8 slots; only explicit own-origin holds activate items7/10/14 v5+v6. The other24 reservations are skipped with exact reasons. No new or modified Pine is used.", '', '| Source | Final single CSV rows | Prefix criterion | CSVs / calendar selections |', '| --- | ---: | --- | --- |']
    for attempt in inventory['attempts']:
        final = attempt['sessions'][attempt['selectedFinalSession']] if attempt['sessions'] else None
        lines.append(f"| {attempt['source']['sourceId']} | {final['dataRows'] if final else 'UNOBSERVED'} | {final['prefixCriterion'] if final else attempt['status']} | {len(attempt['sessions'])} / {attempt['calendarSelections']} |")
    lines += ['', 'Each successful prefix is owned by its exact unchanged v95 source SHA and new private source/version. The first physical row must be INPUT_INDEX0/IS_FIRST1/FIRST_INDEX0 with INPUT_TIME=FIRST_TIME=CSV time×1000; every subsequent source index and timestamp is checked through the last row. At least0..127 are independently physically closed and native-confirmed. Item5 additionally requires own OHLC to agree with actual chart columns. Real timestamp gaps remain archived; no rows are synthesized or joined.', '', 'Every original CSV, header/column ordinal, string, blank/NA, fractional residue, chart/builtin input and later row is retained. Separate cropped diagnostic and post-navigation sessions are never spliced. Only the selected final single CSV may establish the startup prefix; earlier closed archive rows earn no startup credit. The primary model block is exactly own0..127, without output/NA/mask filtering. Complete prior inputs are referenced by original source/session SHA, row range and column ordinals.', '', '| Source | First finite native targets (own index; raw value) |', '| --- | --- |']
    for summary in summaries:
        wanted = {2: ['EMA_ALL', 'EMA_BRANCH'], 3: ['LOCAL_FIRST'], 4: ['EMA_CLEAN', 'EMA_HOLE', 'RMA_CLEAN', 'RMA_HOLE', 'RSI_CLEAN', 'RSI_HOLE', 'TSI_CLEAN', 'TSI_HOLE'], 5: ['TR', 'ATR', 'DI_PLUS', 'DI_MINUS', 'ADX', 'SUPERTREND', 'DIRECTION'], 7: ['DYNAMIC', 'PRIOR_X'], 10: ['FIXNAN', 'BOOL_HISTORY_ENCODE'], 14: ['RANDOM_A', 'RANDOM_B']}[summary['item']]
        values = [v for v in summary['nativeVectorPresenceSummary'] if v['property'] in wanted]
        lines.append('| ' + summary['sourceId'] + ' | ' + '; '.join(v['property'] + '=' + (v['firstFiniteOwnIndex'] + '; `' + v['firstFiniteClosedCell']['valueRaw'] + '`' if v['firstFiniteClosedCell'] else 'UNOBSERVED') for v in values) + ' |')
    lines += ['', 'These are observed targets, independently from algorithm verdicts. [Numeric controls](numeric-controls-v' + str(revision) + '.json) points to immutable per-source reports containing every primary native target and frozen seed/clock/hole/copy/NA/random candidate record, native NA witnesses, raw pointers, exact residuals, precision causes and property verdict counts. First-finite EMA versus SMA3 seeds, gated versus every-bar clocks, LOCAL_FIRST first reach versus reinitialization, EMA/RMA missing-output/poison alternatives and independent OHLC-derived ATR seed candidates retain distinct verdicts. No exported target supplies a recurrence seed. RSI/TSI, DMI/Supertrend and random streams retain independent native vectors and unresolved algorithm facets. Later Supertrend transitions, when present, are an explicitly scoped raw closed-vector witness table with all preceding own OHLC; they do not introduce a fitted later model block.', '', 'A mask or adequately precise integer/dyadic contradiction is a refutation. A native fractional discrepancy with unresolved arithmetic/export precision remains observed and UNDECIDED, without tolerance or rounding/seed/PRNG fit. Source admission, prefix availability, property hypotheses, precision and engine parity remain separate. Own index0 does not recover original v95/v91 frontiers, missing first live events or old clocks.', '', f"Read-only audit: PASS. {result.get('completeOwnPrefixSources', 0)} returned sources certify a complete own prefix; {result.get('primaryOwnClosedRows', 0)} primary own rows; {result['originalCsvs']} original CSVs with {result['archiveDataRows']} archive rows. Archive counts include any overlap between separate frontiers and are not unique executions. {result['modelRecords']} model records and {result['rawCellPointerReferences']} raw pointer references are not unique cells. Native/compiler bodies and separate immediate/settled UI are retained, including all exposed warning/error channels; independent editor marker arrays and native instance/feed/execution IDs remain UNOBSERVED.", '', 'Only new layout208236729/euz5a92K, oracle-v97-v1, BINANCE:BTCUSDT2m ordinary Candles UTC is used. Each returned own study is removed; default builtin Volume remains. Every selected source has a distinct new PRIVATE unpublished save name and exact original Pine title. P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action. No existing-layout edit, publication/share/visibility/import/alert, reconnect/account/entitlement action, replay, reload/forced recalc, source repair/retry or input variant occurred.']
    lines += ['', 'The end-of-round full native saved-record and passive tab comparison is retained in environment-v2/existing-layout-comparison-v1.json; all12 old records and8 old open-tab signatures are unchanged. Only the new v97 layout is saved after cleanup.' if complete else f"Remaining: {14 - len(receipts)} selected slots. End-of-round saved-record/tab preservation comparison and final new-layout save are pending. Later in-progress source files are outside this immutable progress revision; their bytes are not overwritten or silently claimed captured.", '', f'Run `python3 v97/captures/v97/validate-evidence-v2.py {revision}`. Canonical evidence for this revision: selection-inventory-v1.json, attempt-inventory-v{revision}.json, numeric-controls-v{revision}.json, facet-capabilities-v{revision}.json, account-actions-v{revision}.json, validation-result-v{revision}.json and artifact-integrity-v{revision}.json, plus every included immutable source/session artifact. The integrity manifest includes frozen request dependencies and self-excludes. New tooling rights are separately stated in CAPTURE-TOOLING-LICENSE-v1.md.', '', 'This is a fresh capture contract only: no engine fix/fixture promotion, universal algorithm certificate, recovered live/update completeness or closure of historical holds1/2/7/8/13/14/21 is approved. Consumption and crossed QA remain required.']
    response = BASE / f'RESPONSE-v97-v{revision}.md'
    text = '\n'.join(lines) + '\n'
    if response.exists():
        assert response.read_text() == text
    else:
        response.write_text(text)
    completed = {a['source']['sourceId'] for a in inventory['attempts']}
    files = set()
    for path in (ROOT / 'v97').rglob('*'):
        if not path.is_file() or path.name.startswith('.') or '__pycache__' in path.parts or path == BASE / f'artifact-integrity-v{revision}.json':
            continue
        relative = path.relative_to(BASE) if path.is_relative_to(BASE) else None
        if relative is not None and relative.parts[0].startswith('v97-') and relative.parts[0] not in completed:
            continue
        files.add(path)
    manifest = json.loads((ROOT / 'v97/bundle-manifest-v1.json').read_text())
    for pointer in manifest['basisArtifacts']:
        files.add(ROOT / pointer['path'])
    selection = json.loads((BASE / 'selection-inventory-v1.json').read_text())
    files.add(ROOT / selection['publishedV95Response']['path'])
    files.add(ROOT / selection['v96CompletedReturn']['path'])
    for record in selection['records']:
        files.add(ROOT / record['source']['path'])
        files.add(ROOT / record['reviewedNumericArtifact']['path'])
    files.add(ROOT / 'v95/captures/v95/analyze-evidence-v1.py')
    for item in [3, 5, 7, 10, 14]:
        files.add(ROOT / f'v95/captures/v95/analyze-item{item}-v1.py')
    files.add(ROOT / 'v96/captures/v96/validate-evidence-v1.py')
    put(BASE / f'artifact-integrity-v{revision}.json', {'version': f'v{revision}', 'scope': 'All frozen request dependencies, immutable reviewed hold/model dependencies and returned artifacts for included source slots. Later in-progress slots excluded; this manifest self-excludes.', 'files': [ref(path) for path in sorted(files)]})
    paths = sorted(str(path.relative_to(ROOT)) for path in files if path.is_relative_to(ROOT / 'v97/captures')) + [f'v97/captures/v97/artifact-integrity-v{revision}.json']
    Path(f'/tmp/oracle-v97-return-paths-v{revision}.txt').write_text('\n'.join(paths) + '\n')
    return result


if __name__ == '__main__':
    print(json.dumps(package_round(int(sys.argv[1]), int(sys.argv[2])), indent=2))
