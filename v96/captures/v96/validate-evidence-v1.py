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
ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent


def read(name):
    return json.loads((BASE / name).read_text())


def bound(pointer):
    raw = (ROOT / pointer['path']).read_bytes()
    assert len(raw) == pointer['bytes'] and hashlib.sha256(raw).hexdigest() == pointer['sha256']
    return raw


def number(value):
    try:
        return F(value)
    except (ValueError, TypeError, ZeroDivisionError):
        return None


def epoch(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()


def signature(raw):
    text = raw.decode()
    return {'url': re.search(r'url="([^"]+)"', text)[1], 'canvas': re.findall(r'Canvas "([^"]+)"', text), 'checkedRadios': re.findall(r'radio "([^"]+)" checked', text), 'activeLayout': re.findall(r'button "Logged in as [^"]+ Active layout: ([^"]+)"', text)}


def validate(revision=1, check_integrity=True, require_preservation=True):
    manifest = json.loads((ROOT / 'v96/bundle-manifest-v1.json').read_text())
    inventory = read(f'attempt-inventory-v{revision}.json')
    numeric = read(f'numeric-controls-v{revision}.json')
    assets = {a['sourceId']: a for a in manifest['sources']}
    assert len(assets) == 2 and len(inventory['attempts']) <= 2
    attempts = list(BASE.glob('*/attempt-v1/attempt-start-v1.json'))
    assert len(attempts) <= 2 and {p.parent.parent.name for p in attempts} <= set(assets)
    totals, private_ids = Counter(), set()
    for attempt in inventory['attempts']:
        source = attempt['source']
        asset = assets[source['sourceId']]
        raw_source = bound(source['executed'])
        assert raw_source == (ROOT / asset['path']).read_bytes()
        assert hashlib.sha256(raw_source).hexdigest() == asset['sha256'] == source['sourceSha256']
        assert not re.search(rb'^\s*import\s', raw_source, re.M)
        titles = re.findall(r'plot\([^\n]+?[, ](?:title=)?"([^"]+)"', raw_source.decode())
        assert titles == [p['title'] for p in asset['plots']] and len(titles) == 60
        form = bound(source['sourceForm'])
        boundary = form.split(b'\r\n')[0]
        native = form.split(b'\r\n\r\n', 1)[1].split(b'\r\n' + boundary, 1)[0]
        assert native.replace(b'\r\n', b'\n') == raw_source
        receipt = json.loads(bound(source['receipt']))
        assert receipt['sourceExact']
        saved = json.loads(bound(source['saveBody']))
        assert saved['success'] == source['nativeCompileSuccess']
        totals.update(nativeSaves=1, compilerBodies=1)
        if not saved['success']:
            assert source['addBody'] is None and not attempt['sessions']
            totals['nativeRefusals'] += 1
            continue
        meta = saved['result']['metaInfo']
        assert meta['scriptIdPart'] == source['privateScriptId'] and meta['pine']['version'] == source['privateVersion'] == '1.0'
        assert meta['scriptIdPart'] not in private_ids
        private_ids.add(meta['scriptIdPart'])
        added = json.loads(bound(source['addBody']))
        totals.update(nativeAdds=1, compilerBodies=1)
        if not added['success']:
            assert not attempt['sessions']
            totals['nativeRefusals'] += 1
            continue
        assert receipt['removed'] and len(receipt['sessions']) == len(attempt['sessions']) == 1
        assert added['result']['metaInfo']['scriptIdPart'] == source['privateScriptId']
        for session in attempt['sessions']:
            raw = list(csv.reader(bound(session['csv']).decode('utf-8-sig').splitlines()))
            headers, rows = raw[0], raw[1:]
            bindings = json.loads(bound(session['columnBindings']))
            assert [c['originalHeader'] for c in bindings['columns']] == headers
            requested = {p['title']: p['sourcePlotOrdinal'] for p in asset['plots']}
            owned = set()
            for column in bindings['columns']:
                title = column['originalHeader']
                if title in requested and column['bindingStatus'] == 'OBSERVED':
                    assert column['owner'] == source['privateScriptId'] and column['privateVersion'] == '1.0'
                    assert column['sourceSha256'] == asset['sha256'] and column['sourceLiteralPlotOrdinal'] == requested[title]
                    owned.add(title)
                if column['bindingStatus'] == 'OBSERVED / NATIVE COLORER':
                    assert any(p['id'] == column['nativePlotId'] and p['type'] == 'colorer' for p in bindings['nativeColorerDefinitions'])
                    assert column['rawEncoding'].startswith('UNINTERPRETED')
            assert set(bindings['missingOrAmbiguousRequestedPlotTitles']) == set(requested) - owned
            download = json.loads(((ROOT / session['csv']['path']).parent / 'chart-download-v1.json').read_text())
            assert download['sha256'] == session['csv']['sha256']
            clock = epoch(download['exportTrigger']['startedAtUtc'])
            assert clock <= download['downloadModifiedAtEpoch'] <= epoch(receipt['completedAtUtc'])
            masks = list(csv.DictReader(bound(session['closureMask']).decode().splitlines()))
            assert len(masks) == len(rows)
            closed, selected, run = [], [], []
            for n, (row, mask) in enumerate(zip(rows, masks), 1):
                assert len(row) == len(headers)
                values = dict(zip(headers, row))
                own_time, own_index = number(values.get('INPUT_TIME')), number(values.get('INPUT_INDEX'))
                context = own_time is not None and own_index is not None and own_time.denominator == own_index.denominator == 1 and own_time == F(row[0]) * 1000 and all(t in owned for t in ['INPUT_TIME', 'INPUT_INDEX', 'CHART_CONFIRMED'])
                eligible = context and F(row[0]) + 120 <= clock and number(values.get('CHART_CONFIRMED')) == 1
                assert mask['csv_sha256'] == session['csv']['sha256'] and int(mask['row_ordinal']) == n
                assert mask['time_raw_seconds'] == row[0] and int(mask['closed_numeric_eligible']) == eligible
                assert mask['present_cell_status'].startswith('OBSERVED')
                assert json.loads(mask['blank_column_ordinals']) == [i for i, value in enumerate(row, 1) if value == '']
                if eligible:
                    closed.append(n)
                    if run and (n != run[-1] + 1 or own_index != number(rows[run[-1] - 1][headers.index('INPUT_INDEX')]) + 1):
                        run = []
                    run.append(n)
                    if len(run) == 32 and not selected:
                        selected = list(run)
                else:
                    run = []
            assert closed == session['eligibleDataRowOrdinals'] and len(closed) == session['independentlyClosedRows']
            assert selected == session['selectedFirst32ConsecutiveClosedRows']
            totals.update(csvs=1, dataRows=len(rows), independentlyClosedRows=len(closed))
    assert totals['nativeSaves'] <= 2 and totals['nativeAdds'] <= 2 and totals['csvs'] <= 2
    assert runpy.run_path(str(BASE / 'analyze-evidence-v1.py'))['analyze'](revision) == numeric
    for report in numeric['sources']:
        if 'csv' not in report:
            continue
        raw = list(csv.reader(bound(report['csv']).decode('utf-8-sig').splitlines()))
        masks = {int(r['row_ordinal']): r for r in csv.DictReader(bound(report['closureMask']).decode().splitlines())}
        assert [r['rowOrdinal'] for r in report['rows']] == report['selectedDataRowOrdinals']
        for row in report['rows']:
            n = row['rowOrdinal']
            assert masks[n]['closed_numeric_eligible'] == '1'
            def pointer(p):
                if p is not None:
                    assert raw[p['rowOrdinal']][p['columnOrdinal'] - 1] == p['valueRaw']
                    assert raw[0][p['columnOrdinal'] - 1] == p['headerRaw']
                    totals['rawCellPointers'] += 1
            for p in row['allRequestedRawCells'] + row['nativeContextCells']:
                pointer(p)
            for comparison in row['comparisons']:
                pointer(comparison['nativeCell'])
                for p in comparison['inputCells']:
                    pointer(p)
                if comparison['verdict'] == 'SUPPORTED':
                    assert comparison['nativeCell'] is not None and number(comparison['nativeCell']['valueRaw']) == number(comparison['predictedRational'])
                if not comparison['semanticCalibrationAdequate']:
                    assert comparison['verdict'] == 'UNDECIDED'
                totals['numericComparisons'] += 1
                totals['verdict_' + comparison['verdict']] += 1
            for case in row['cases']:
                if case['literalCandidateVerdict'].startswith('SUPPORTED'):
                    assert case['literalEqualityCalibrationAdequate'] and case['nativePresenceZeroObserved']
                    assert sum(number(p['valueRaw']) == 1 for p in case['actualEqualityCells'].values()) == 1
                assert case['scope'].startswith('Observed equality')
        totals['propertyVerdicts'] += len(report['propertyVerdicts'])
    if require_preservation:
        assert len(inventory['attempts']) == 2
        preservation = read('environment-v2/existing-layout-comparison-v1.json')
        assert preservation['allBeforeRecordsUnchanged'] and preservation['allOpenTabSignaturesUnchanged']
        assert len(preservation['savedRecordComparisons']) == 11 and len(preservation['openTabComparisons']) == 7
        before = json.loads(bound(preservation['beforeSavedRecords']))
        after = json.loads(bound(preservation['afterSavedRecords']))
        indexed = {r['id']: r for r in after}
        assert len(before) == 11 and len(after) == 12 and all(indexed[r['id']] == r for r in before)
        for pair in preservation['openTabComparisons']:
            assert signature(bound(pair['beforeEvidence'])) == pair['before'] == pair['after'] == signature(bound(pair['afterEvidence']))
        assert indexed[208235696]['pro_symbol'] == 'BINANCE:BTCUSDT' and indexed[208235696]['interval'] == '2'
    if check_integrity:
        for item in read(f'artifact-integrity-v{revision}.json')['files']:
            bound(item)
    return {'version': f'v{revision}', 'status': 'PASS', 'sourceSlotsAudited': len(inventory['attempts']), **dict(totals), 'scope': 'Exact native source/admission, original CSV ordinals, physical closure, source ownership, all five cases/calibration on the same first32 rows and explicit literal/byte holds. No packed decoder, native-value normalization, fitted quantizer, raster parity or engine approval.'}


if __name__ == '__main__':
    result = validate()
    assert result == read('validation-result-v1.json')
    print(json.dumps(result, indent=2))
