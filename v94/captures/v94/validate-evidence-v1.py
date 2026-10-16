import csv
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from datetime import datetime
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True


def load(name):
    return json.loads((BASE / name).read_text())


def bound(item):
    data = (ROOT / item['path']).read_bytes()
    assert len(data) == item['bytes']
    assert hashlib.sha256(data).hexdigest() == item['sha256']
    return data


def validate(revision=1, check_integrity=True):
    inventory = load(f'attempt-inventory-v{revision + 1}.json')
    numeric = load(f'numeric-controls-v{revision}.json')
    manifest = json.loads((ROOT / 'v94/bundle-manifest-v1.json').read_text())
    assets = {a['id']: a for a in manifest['sources']}
    attempts = inventory['attempts']
    assert len(assets) == 6 and len(attempts) <= 6
    starts = list(BASE.glob('*/attempt-v1/attempt-start-v1.json'))
    assert len(starts) <= 6
    assert {p.parent.parent.name for p in starts} <= set(assets)
    assert len({a['source']['privateScriptId'] for a in attempts}) == len(attempts)
    totals = Counter()
    for attempt in attempts:
        source = attempt['source']
        asset = assets[source['sourceId']]
        executed = bound(source['executed'])
        assert executed == (ROOT / source['requestSource']).read_bytes()
        assert hashlib.sha256(executed).hexdigest() == asset['sha256'] == source['sourceSha256']
        assert not re.search(rb'^\s*import\s', executed, re.M)
        directory = (ROOT / source['receipt']['path']).parent
        form = (directory / 'save-request-v1.txt').read_bytes()
        boundary = form.split(b'\r\n')[0]
        native = form.split(b'\r\n\r\n', 1)[1].split(b'\r\n' + boundary, 1)[0]
        assert native.replace(b'\r\n', b'\n') == executed
        receipt = json.loads(bound(source['receipt']))
        assert receipt['sourceExact'] and receipt['removed']
        assert len(receipt['sessions']) == len(attempt['sessions']) == 1
        for key in ['saveBody', 'addBody']:
            body = json.loads(bound(source[key]))
            assert body['success']
            meta = body['result']['metaInfo']
            assert meta['scriptIdPart'] == source['privateScriptId']
            assert meta['pine']['version'] == source['privateVersion'] == '1.0'
            totals['compilerBodies'] += 1
        for session in attempt['sessions']:
            raw = list(csv.reader(bound(session['csv']).decode('utf-8-sig').splitlines()))
            headers = raw[0]
            bindings = json.loads(bound(session['columnBindings']))
            assert not bindings['missingOrAmbiguousRequestedPlotTitles']
            assert not bindings['unresolvedColumnOrdinals']
            assert [c['originalHeader'] for c in bindings['columns']] == headers
            requested = {p['title']: p['sourcePlotOrdinal'] for p in asset['plotColumns']}
            for c in bindings['columns']:
                if c['originalHeader'] in requested:
                    assert c['owner'] == source['privateScriptId']
                    assert c['privateVersion'] == source['privateVersion']
                    assert c['sourceLiteralPlotOrdinal'] == requested[c['originalHeader']]
            assert len(bindings['chartVolumeColumnOrdinals']) == 1
            assert headers[bindings['chartVolumeColumnOrdinals'][0] - 1] == 'Volume'
            download = json.loads(((ROOT / session['csv']['path']).parent / 'chart-download-v1.json').read_text())
            assert download['sha256'] == session['csv']['sha256']
            clock = datetime.fromisoformat(download['exportTrigger']['startedAtUtc'].replace('Z', '+00:00')).timestamp()
            assert clock <= download['downloadModifiedAtEpoch'] <= datetime.fromisoformat(receipt['completedAtUtc'].replace('Z', '+00:00')).timestamp()
            masks = list(csv.DictReader(bound(session['closureMask']).decode().splitlines()))
            assert len(masks) == len(raw) - 1
            closed = 0
            for n, (row, mask) in enumerate(zip(raw[1:], masks), 1):
                values = dict(zip(headers, row))
                assert len(row) == len(headers)
                assert int(values['INPUT_TIME']) == int(row[0]) * 1000
                assert int(mask['row_ordinal']) == n and mask['time_raw_seconds'] == row[0]
                assert mask['csv_sha256'] == session['csv']['sha256']
                eligible = int(row[0]) + 120 <= clock and values['CHART_CONFIRMED'] == '1'
                assert int(mask['closed_numeric_eligible']) == eligible
                assert mask['present_cell_status'].startswith('OBSERVED')
                assert json.loads(mask['blank_column_ordinals']) == [i for i, v in enumerate(row, 1) if v == '']
                closed += eligible
            assert closed == session['independentlyClosedRows']
            totals.update(csvs=1, dataRows=len(masks), independentlyClosedRows=closed)
    assert [s['sourceId'] for s in numeric['sources']] == [a['source']['sourceId'] for a in attempts]
    spec = importlib.util.spec_from_file_location('oracle_analysis', BASE / 'analyze-evidence-v1.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.analyze(len(attempts)) == numeric
    for report in numeric['sources']:
        raw = list(csv.reader(bound(report['csv']).decode().splitlines()))
        masks = {int(m['row_ordinal']): m for m in csv.DictReader(bound(report['closureMask']).decode().splitlines())}
        for row in report['rows']:
            n = row['rowOrdinal']
            assert masks[n]['closed_numeric_eligible'] == '1'
            assert raw[n][0] == row['timeRaw']
            for p in row['cells']:
                assert raw[n][p['columnOrdinal'] - 1] == p['valueRaw']
                assert raw[0][p['columnOrdinal'] - 1] == p['headerRaw']
                totals['rawCellPointers'] += 1
            actual = {p['headerRaw']: p['valueRaw'] for p in row['cells']}
            for comparison in row['comparisons']:
                for p in comparison['properties']:
                    equal = actual[p['property']] != '' and Fraction(actual[p['property']]) == Fraction(p['predictedRational'])
                    assert (p['verdict'] == 'SUPPORTED') == equal
                    totals['numericCellComparisons'] += 1
                    totals['contraryCellComparisons'] += not equal
        coverage = report['coverage']
        assert len(report['rows']) == coverage['consecutiveIndependentlyClosedRows'] == 32
        assert all(b['rowOrdinal'] == a['rowOrdinal'] + 1 and int(b['timeRaw']) == int(a['timeRaw']) + 120 for a, b in zip(report['rows'], report['rows'][1:]))
        if 'rsi' in report['sourceId']:
            assert coverage['distinctInteriorRatios'] >= 3 and coverage['separatingRatioRows'] >= 1
        if 'discriminators' in report['sourceId']:
            assert coverage['observedPhases'] == list(range(7))
        totals['propertyVerdicts'] += len(report['propertyVerdicts'])
    if revision == 2:
        assert len(attempts) == len(starts) == 6
        preservation = load('environment-v1/existing-layout-comparison-v1.json')
        assert preservation['allBeforeRecordsUnchanged'] and preservation['allOpenTabSignaturesUnchanged']
    if check_integrity:
        integrity = load(f'artifact-integrity-v{revision}.json')
        for artifact in integrity['files']:
            bound(artifact)
        assert not any(a['path'].endswith(f'artifact-integrity-v{revision}.json') for a in integrity['files'])
    return {'version': f'v{revision}', 'status': 'PASS', 'sourceAttemptsAudited': len(attempts), 'nativeSaves': len(attempts), 'nativeAdds': len(attempts), **dict(totals), 'scope': 'Source identity, transport, native plot ownership, closure, exact rational frozen-model comparisons, raw pointers and available preservation evidence. No engine approval.'}


if __name__ == '__main__':
    revision = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    result = validate(revision)
    assert result == load(f'validation-result-v{revision}.json')
    print(json.dumps(result, indent=2))
