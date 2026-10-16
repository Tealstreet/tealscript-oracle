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


def bound(item):
    data = (ROOT / item['path']).read_bytes()
    assert len(data) == item['bytes'] and hashlib.sha256(data).hexdigest() == item['sha256']
    return data


def validate(revision=2, check_integrity=True):
    inventory = read(f'attempt-inventory-v{revision}.json')
    numeric = read(f'numeric-controls-v{revision}.json')
    materialized = []
    for summary in numeric['sources']:
        report = json.loads(bound(summary['numericEvidence']))
        assert {k: v for k, v in report.items() if k != 'records'} == {k: v for k, v in summary.items() if k != 'numericEvidence'}
        materialized.append(report)
    numeric['sources'] = materialized
    assets = {a['id']: a for a in json.loads((ROOT / 'v95/bundle-manifest-v1.json').read_text())['sources']}
    assert len(assets) == 40
    attempts = inventory['attempts']
    assert len(attempts) <= 38
    reserved = list(BASE.glob('*/attempt-v1/attempt-start-v1.json'))
    assert len(reserved) <= 40 and {p.parent.parent.name for p in reserved} <= set(assets)
    totals = Counter()
    ids = set()
    for attempt in attempts:
        source = attempt['source']
        asset = assets[source['sourceId']]
        assert asset['item'] < 20
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
        assert receipt['sourceExact']
        saved = json.loads(bound(source['saveBody']))
        assert saved['success'] == source['nativeCompileSuccess']
        totals['nativeSaves'] += 1
        totals['compilerBodies'] += 1
        if not saved['success']:
            assert source['addBody'] is None and not attempt['sessions'] and not receipt['studyAdded']
            totals['nativeRefusals'] += 1
            continue
        meta = saved['result']['metaInfo']
        assert meta['scriptIdPart'] == source['privateScriptId']
        assert meta['pine']['version'] == source['privateVersion'] == '1.0'
        assert source['privateScriptId'] not in ids
        ids.add(source['privateScriptId'])
        added = json.loads(bound(source['addBody']))
        totals['nativeAdds'] += 1
        totals['compilerBodies'] += 1
        if not added['success']:
            assert not attempt['sessions']
            totals['nativeRefusals'] += 1
            continue
        assert receipt['removed']
        assert len(receipt['sessions']) == len(attempt['sessions']) == 1
        assert added['result']['metaInfo']['scriptIdPart'] == source['privateScriptId']
        for session in attempt['sessions']:
            raw = list(csv.reader(bound(session['csv']).decode('utf-8-sig').splitlines()))
            headers = raw[0]
            bindings = json.loads(bound(session['columnBindings']))
            assert [c['originalHeader'] for c in bindings['columns']] == headers
            assert not bindings['unresolvedColumnOrdinals'] and not bindings['missingOrAmbiguousRequestedPlotTitles']
            requested = {p['title']: p['sourcePlotOrdinal'] for p in asset['plotColumns']}
            for column in bindings['columns']:
                if column['originalHeader'] in requested:
                    assert column['owner'] == source['privateScriptId']
                    assert column['privateVersion'] == source['privateVersion']
                    assert column['sourceSha256'] == source['sourceSha256']
                    assert column['sourceLiteralPlotOrdinal'] == requested[column['originalHeader']]
            download = json.loads(((ROOT / session['csv']['path']).parent / 'chart-download-v1.json').read_text())
            assert download['sha256'] == session['csv']['sha256']
            clock = datetime.fromisoformat(download['exportTrigger']['startedAtUtc'].replace('Z', '+00:00')).timestamp()
            assert clock <= download['downloadModifiedAtEpoch'] <= datetime.fromisoformat(receipt['completedAtUtc'].replace('Z', '+00:00')).timestamp()
            masks = list(csv.DictReader(bound(session['closureMask']).decode().splitlines()))
            assert len(masks) == len(raw) - 1
            eligible = []
            for n, (row, mask) in enumerate(zip(raw[1:], masks), 1):
                values = dict(zip(headers, row))
                assert len(row) == len(headers)
                assert int(values['INPUT_TIME']) == int(row[0]) * 1000
                assert mask['csv_sha256'] == session['csv']['sha256']
                assert int(mask['row_ordinal']) == n and mask['time_raw_seconds'] == row[0]
                physical = int(row[0]) + 120 <= clock and values['CHART_CONFIRMED'] == '1'
                assert int(mask['closed_numeric_eligible']) == physical
                assert mask['present_cell_status'].startswith('OBSERVED')
                assert json.loads(mask['blank_column_ordinals']) == [i for i, v in enumerate(row, 1) if v == '']
                if physical:
                    eligible.append((n, int(values['INPUT_INDEX'])))
            assert len(eligible) == session['independentlyClosedRows']
            first = dict(zip(headers, raw[1]))
            prefix = first['IS_FIRST'] == '1' and first['INPUT_INDEX'] == first['FIRST_INDEX'] == '0' and first['INPUT_TIME'] == first['FIRST_TIME'] and all(n == i + 1 and index == i for i, (n, index) in enumerate(eligible))
            assert prefix == session['strictOwnIndexZeroPrefixAvailable']
            totals.update(csvs=1, dataRows=len(masks), independentlyClosedRows=len(eligible), ownIndexZeroPrefixes=int(prefix))
    assert totals['nativeSaves'] <= 40 and totals['nativeAdds'] <= 40 and totals['csvs'] <= 50
    analyzer = runpy.run_path(str(BASE / 'analyze-evidence-v1.py'))['analyze']
    assert analyzer(f'attempt-inventory-v{revision}.json', revision) == numeric
    for report in numeric['sources']:
        if 'records' not in report:
            continue
        raw = list(csv.reader(bound(report['csv']).decode('utf-8-sig').splitlines()))
        masks = {int(m['row_ordinal']): m for m in csv.DictReader(bound(report['closureMask']).decode().splitlines())}
        def pointer(p):
            n, i = p['rowOrdinal'], p['columnOrdinal']
            assert raw[n][i - 1] == p['valueRaw'] and raw[0][i - 1] == p['headerRaw']
            assert masks[n]['closed_numeric_eligible'] == '1'
            totals['rawCellPointers'] += 1
        for record in report['records']:
            pointer(record['nativeCell'])
            for p in record['inputCells'] + record.get('dependencyCells', []):
                pointer(p)
            actual = record['nativeCell']['valueRaw']
            if record['predictedRational'] is not None:
                if record['nativeNumericParsingStatus'] == 'FINITE_RATIONAL_STRING':
                    delta = F(actual) - F(record['predictedRational'])
                    assert str(delta) == record['exactExportedStringResidual']
                if record['verdict'] == 'SUPPORTED':
                    assert actual != '' and F(actual) == F(record['predictedRational'])
            if record['predictedBlank']:
                assert (record['verdict'] == 'SUPPORTED') == (actual == '')
            totals['numericRecords'] += 1
            totals['verdict_' + record['verdict']] += 1
        totals['propertyVerdicts'] += len(report['propertyVerdicts'])
    if check_integrity:
        for prior_revision in range(1, revision):
            for previous in read(f'artifact-integrity-v{prior_revision}.json')['files']:
                bound(previous)
        integrity = read(f'artifact-integrity-v{revision}.json')
        for item in integrity['files']:
            bound(item)
        assert not any(p['path'].endswith(f'artifact-integrity-v{revision}.json') for p in integrity['files'])
    return {'version': f'v{revision}', 'status': 'PASS', 'sourceSlotsAudited': len(attempts), **dict(totals), 'scope': 'Finite closed-source progress return: source/transport identity, plot ownership, clocks, physical closure, own-prefix guards, family calculations and raw pointers. Observer slots remain reserved. No engine approval or historical hold closure.'}


if __name__ == '__main__':
    revision = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    result = validate(revision)
    assert result == read(f'validation-result-v{revision}.json')
    print(json.dumps(result, indent=2))
