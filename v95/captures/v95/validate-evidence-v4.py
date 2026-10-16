import csv
import hashlib
import json
import re
import runpy
import sys
from collections import Counter
from datetime import datetime
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path('/Users/samuelsteady/cs/tealscript-oracle')
BASE = ROOT / 'v95/captures/v95'


def bound(pointer):
    raw = (ROOT / pointer['path']).read_bytes()
    assert len(raw) == pointer['bytes']
    assert hashlib.sha256(raw).hexdigest() == pointer['sha256']
    return raw


def read(name):
    return json.loads((BASE / name).read_text())


def epoch(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()


def signature(raw):
    text = raw.decode()
    return {'url': re.search(r'url="([^"]+)"', text)[1], 'canvas': re.findall(r'Canvas "([^"]+)"', text), 'checkedRadios': re.findall(r'radio "([^"]+)" checked', text), 'activeLayout': re.findall(r'button "Logged in as [^"]+ Active layout: ([^"]+)"', text)}


def validate(revision, closed_revision, check_integrity=True):
    closed_result = runpy.run_path(str(BASE / 'validate-evidence-v3.py'))['validate'](closed_revision)
    assert closed_result['sourceSlotsAudited'] == 38
    closed_inventory = read(f'attempt-inventory-v{closed_revision}.json')
    inventory = read(f'attempt-inventory-v{revision}.json')
    numeric = read(f'numeric-controls-v{revision}.json')
    old_numeric = read(f'numeric-controls-v{closed_revision}.json')
    assert len(inventory['attempts']) == 40
    assert inventory['attempts'][:38] == closed_inventory['attempts']
    assert numeric['sources'][:38] == old_numeric['sources']
    assert len(numeric['sources']) == 40
    assets = json.loads((ROOT / 'v95/bundle-manifest-v1.json').read_text())['sources']
    reserved = list(BASE.glob('*/attempt-v1/attempt-start-v1.json'))
    assert len(reserved) == 40
    assert {p.parent.parent.name for p in reserved} == {a['id'] for a in assets}
    totals = Counter({k: v for k, v in closed_result.items() if isinstance(v, int) and k != 'sourceSlotsAudited'})
    private_ids = {a['source']['privateScriptId'] for a in closed_inventory['attempts'] if a['source']['privateScriptId'] is not None}
    analyzer = runpy.run_path(str(BASE / 'analyze-observer-v1.py'))['analyze']
    for position in range(38, 40):
        attempt, asset, summary = inventory['attempts'][position], assets[position], numeric['sources'][position]
        source = attempt['source']
        assert source['sourceId'] == asset['id'] == summary['sourceId']
        assert asset['item'] == 20 and not attempt['sessions']
        directory = (ROOT / source['receipt']['path']).parent
        executed = bound(source['executed'])
        assert executed == (ROOT / source['requestSource']).read_bytes()
        assert hashlib.sha256(executed).hexdigest() == asset['sha256'] == source['sourceSha256']
        assert not re.search(rb'^\s*import\s', executed, re.M)
        form = (directory / 'save-request-v1.txt').read_bytes()
        boundary = form.split(b'\r\n')[0]
        native = form.split(b'\r\n\r\n', 1)[1].split(b'\r\n' + boundary, 1)[0]
        assert native.replace(b'\r\n', b'\n') == executed
        receipt = json.loads(bound(source['receipt']))
        assert receipt['sourceExact']
        saved = json.loads(bound(source['saveBody']))
        assert saved['success'] == source['nativeCompileSuccess']
        totals.update(nativeSaves=1, compilerBodies=1)
        if not saved['success']:
            assert source['addBody'] is None and not receipt['studyAdded']
            totals['nativeRefusals'] += 1
        else:
            meta = saved['result']['metaInfo']
            assert meta['scriptIdPart'] == source['privateScriptId']
            assert meta['pine']['version'] == source['privateVersion'] == '1.0'
            assert meta['scriptIdPart'] not in private_ids
            private_ids.add(meta['scriptIdPart'])
            added = json.loads(bound(source['addBody']))
            totals.update(nativeAdds=1, compilerBodies=1)
            if not added['success']:
                totals['nativeRefusals'] += 1
            else:
                assert receipt['removed'] and added['result']['metaInfo']['scriptIdPart'] == meta['scriptIdPart']
                observer = receipt['observer']
                assert observer['sourceSessions'] == 1
                assert observer['actualNativeCalculationSessionCount'] is None
                assert observer['inputChanges'] == observer['retries'] == 0
                assert observer['nativeExecutionIdentity'] is None
                assert observer['allLiveSnapshotsExcludedFromClosedScoring']
                assert not observer['interveningEventCompleteness']
                assert 0 <= observer['exports'] <= 6
                assert len(observer['sampleInspections']) <= observer['exports']
                assert len(observer['exportAttempts']) == observer['exports']
                assert [e['sampleOrdinal'] for e in observer['exportAttempts']] == list(range(observer['exports']))
                totals['observerDownloadAttempts'] += observer['exports']
                totals['observerExportOrInspectionHolds'] += observer['exports'] - len(observer['sampleInspections'])
                window = observer['window']
                if window is not None:
                    assert window['sourceId'] == asset['id'] and window['sourceSha256'] == asset['sha256']
                    assert window['privateId'] == source['privateScriptId'] and window['privateVersion'] == '1.0'
                    assert window['barOpenEpochMs'] + 120000 == window['barCloseEpochMs'] == window['nextOpenEpochMs']
                    assert window['deadlineEpochMs'] == window['barCloseEpochMs'] + 15000
                    assert window['deadlineEpochMs'] - window['settledAtEpochMs'] <= 255000
                    assert abs(epoch(window['settledAtUtc']) * 1000 - window['settledAtEpochMs']) < 1
                    assert epoch(window['barOpenUtc']) * 1000 == window['barOpenEpochMs']
                    assert epoch(window['barCloseUtc']) * 1000 == window['barCloseEpochMs']
                    assert epoch(window['deadlineUtc']) * 1000 == window['deadlineEpochMs']
                for ordinal, inspection_ref in enumerate(observer['sampleInspections']):
                    inspection = json.loads(bound(inspection_ref))
                    assert inspection['sampleOrdinal'] == ordinal and inspection['window'] == window
                    assert inspection['sourceId'] == asset['id'] and inspection['sourceSha256'] == asset['sha256']
                    assert inspection['privateId'] == source['privateScriptId'] and inspection['privateVersion'] == '1.0'
                    sample_dir = (ROOT / inspection_ref['path']).parent
                    raw = list(csv.reader(bound(inspection['csv']).decode('utf-8-sig').splitlines()))
                    headers, rows = raw[0], raw[1:]
                    bindings = json.loads(bound(inspection['columnBindings']))
                    masks = list(csv.DictReader(bound(inspection['closureMask']).decode().splitlines()))
                    assert len(masks) == len(rows) == inspection['originalDataRows']
                    assert len(headers) == inspection['originalColumnCount']
                    assert [c['originalHeader'] for c in bindings['columns']] == headers
                    assert bindings['instanceId'] is None
                    requested = {p['title']: p['sourcePlotOrdinal'] for p in asset['plotColumns']}
                    for column in bindings['columns']:
                        if column['originalHeader'] in requested and column['bindingStatus'] == 'OBSERVED':
                            assert column['owner'] == source['privateScriptId']
                            assert column['privateVersion'] == '1.0'
                            assert column['sourceSha256'] == asset['sha256']
                            assert column['sourceLiteralPlotOrdinal'] == requested[column['originalHeader']]
                    download = json.loads((sample_dir / 'chart-download-v1.json').read_text())
                    trigger = epoch(download['exportTrigger']['startedAtUtc'])
                    assert download['sha256'] == inspection['csv']['sha256']
                    assert epoch(window['declaredAtUtc']) <= trigger <= window['deadlineEpochMs'] / 1000
                    assert trigger <= download['downloadModifiedAtEpoch'] <= epoch(receipt['completedAtUtc'])
                    baseline = []
                    for n, (row, mask) in enumerate(zip(rows, masks), 1):
                        assert len(row) == len(headers)
                        values = dict(zip(headers, row))
                        assert mask['csv_sha256'] == inspection['csv']['sha256']
                        assert int(mask['row_ordinal']) == n and mask['time_raw_seconds'] == row[0]
                        consistent = values.get('INPUT_TIME') not in [None, ''] and F(values['INPUT_TIME']) == int(row[0]) * 1000
                        physical = int(row[0]) + 120 <= trigger and values.get('CHART_CONFIRMED') == '1' and consistent
                        target = window['barCloseEpochMs'] if inspection['requestedKind'] == 'NEXT_BAR_FIRST' else window['barOpenEpochMs']
                        event = consistent and F(values['INPUT_TIME']) == target
                        eligible = ordinal == 0 and physical and F(values['INPUT_TIME']) < window['barOpenEpochMs'] and not bindings['missingOrAmbiguousRequestedPlotTitles']
                        assert int(mask['physically_closed']) == physical
                        assert int(mask['closed_numeric_eligible']) == eligible
                        assert int(mask['event_target']) == event
                        assert not event or not eligible
                        assert mask['present_cell_status'].startswith('OBSERVED')
                        assert json.loads(mask['blank_column_ordinals']) == [i for i, v in enumerate(row, 1) if v == '']
                        if eligible:
                            baseline.append(n)
                    assert inspection['first32ClosedBaselineDataRowOrdinals'] == baseline[:32]
                    for target_tuple in inspection['targetTuples']:
                        for title, pointer in target_tuple['nativeCellPointers'].items():
                            n, col = pointer['rowOrdinal'], pointer['columnOrdinal']
                            assert raw[n][col - 1] == pointer['valueRaw'] == target_tuple['valuesRaw'][title]
                            assert headers[col - 1] == pointer['headerRaw'] == title
                            assert masks[n - 1]['closed_numeric_eligible'] == '0'
                            totals['rawCellPointers'] += 1
                        assert target_tuple['sameExecutionAsUiScreenshot'] is None
                    totals.update(csvs=1, dataRows=len(rows), independentlyClosedRows=len(baseline), observerExports=1)
        report = json.loads(bound(summary['numericEvidence']))
        assert report == analyzer(asset['id'])
        assert {k: v for k, v in report.items() if k != 'records'} == {k: v for k, v in summary.items() if k != 'numericEvidence'}
        for record in report.get('records', []):
            raw = list(csv.reader(bound(record['csv']).decode('utf-8-sig').splitlines()))
            inspection_dir = (ROOT / record['csv']['path']).parent
            mask = list(csv.DictReader((inspection_dir / 'row-closure-mask-v1.csv').open()))
            for pointer in [record['nativeCell']] + record['inputCells']:
                if pointer is None:
                    continue
                n, col = pointer['rowOrdinal'], pointer['columnOrdinal']
                assert raw[n][col - 1] == pointer['valueRaw'] and raw[0][col - 1] == pointer['headerRaw']
                assert (mask[n - 1]['closed_numeric_eligible'] == '1') == record['closedScoringEligible']
                totals['rawCellPointers'] += 1
            if record['verdict'] == 'SUPPORTED':
                assert F(record['actualValueRaw']) == F(record['predictedRational'])
            totals['numericRecords'] += 1
            totals['verdict_' + record['verdict']] += 1
        totals['observerSourcesReturned'] += 1
    assert totals['nativeSaves'] <= 40 and totals['nativeAdds'] <= 40 and totals['csvs'] <= 50
    assert closed_result['csvs'] + totals['observerDownloadAttempts'] <= 50
    for source in numeric['sources'][:38]:
        discriminator_path = BASE / source['sourceId'] / 'attempt-v1/eigen-orientation-discriminator-v1.json'
        if not discriminator_path.exists():
            continue
        discriminator = json.loads(discriminator_path.read_text())
        assert discriminator['sourceSha256'] == source['sourceSha256'] and discriminator['csv'] == source['csv']
        raw = list(csv.reader(bound(source['csv']).decode('utf-8-sig').splitlines()))
        assert [r['rowOrdinal'] for r in discriminator['rows']] == source['selectedBlockDataRowOrdinals']
        for row in discriminator['rows']:
            for pointer in row['nativeCells'].values():
                n, col = pointer['rowOrdinal'], pointer['columnOrdinal']
                assert raw[n][col - 1] == pointer['valueRaw'] and raw[0][col - 1] == pointer['headerRaw']
            values = {k: F(p['valueRaw']) for k, p in row['nativeCells'].items()}
            assert row['rowAndColumnVectorsIdentical'] == (values['EVEC_0_1'] == values['EVEC_1_0'])
            for association in row['associations']:
                k = association['nativeEigenvalueOrdinal']
                vector = [values['EVEC_' + str(k) + '_' + str(j)] for j in range(2)] if association['orientation'] == 'ROWS' else [values['EVEC_' + str(j) + '_' + str(k)] for j in range(2)]
                assert [str(x) for x in vector] == association['vectorRational']
                residual = [sum(F([[4, 1], [1, 3]][i][j]) * vector[j] for j in range(2)) - values['EIGEN_' + str(k)] * vector[i] for i in range(2)]
                assert [str(x) for x in residual] == association['residualRational']
        assert discriminator['allSelectedTuplesNondiscriminating'] == all(r['rowAndColumnVectorsIdentical'] for r in discriminator['rows'])
    comparison = read('environment-v2/existing-layout-comparison-v1.json')
    assert comparison['allBeforeRecordsUnchanged'] and comparison['allOpenTabSignaturesUnchanged']
    assert len(comparison['savedRecordComparisons']) == 10 and len(comparison['openTabComparisons']) == 6
    for pair in comparison['savedRecordComparisons']:
        assert pair['before'] == pair['after'] and pair['equal']
    for pair in comparison['openTabComparisons']:
        assert pair['before'] == pair['after'] and pair['equal']
        assert signature(bound(pair['beforeEvidence'])) == pair['before']
        assert signature(bound(pair['afterEvidence'])) == pair['after']
    before = json.loads(bound(comparison['beforeSavedRecords']))
    after = json.loads(bound(comparison['afterSavedRecords']))
    indexed = {r['id']: r for r in after}
    assert len(before) == 10 and len(after) == 11
    assert all(indexed[r['id']] == r for r in before)
    assert comparison['newV95Record'] == indexed[208224726]
    assert indexed[208224726]['pro_symbol'] == 'BINANCE:BTCUSDT'
    assert indexed[208224726]['interval'] == '2'
    if check_integrity:
        for previous in range(1, revision + 1):
            for pointer in read(f'artifact-integrity-v{previous}.json')['files']:
                bound(pointer)
    return {'version': f'v{revision}', 'status': 'PASS', 'sourceSlotsAudited': 40, 'closedProgressRevision': closed_revision, **dict(totals), 'allTenOldSavedRecordsUnchanged': True, 'allSixOldOpenTabSignaturesUnchanged': True, 'scope': 'Finite40-slot native round including bounded observer windows, exact source/admission bodies, original exports/ordinals, closure/exclusion masks, independent raw pointers and explicit capability holds. No engine approval, event completeness or old MTF identity recovery.'}


if __name__ == '__main__':
    revision, closed_revision = map(int, sys.argv[1:3])
    result = validate(revision, closed_revision)
    assert result == read(f'validation-result-v{revision}.json')
    print(json.dumps(result, indent=2))
