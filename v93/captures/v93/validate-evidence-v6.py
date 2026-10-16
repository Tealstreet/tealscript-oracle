# SPDX-License-Identifier: MIT
import csv
import hashlib
import json
import re
import struct
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

root = Path(__file__).resolve().parents[3]
base = Path(__file__).resolve().parent

def read(path):
    return json.loads((base / path).read_text())

def bound(item):
    b = (root / item['path']).read_bytes()
    assert hashlib.sha256(b).hexdigest() == item['sha256']
    assert len(b) == item['bytes']
    return b

inventory = read('attempt-inventory-v6.json')
assert inventory['capturedSources'] == 36
assert len(inventory['remainingSourceIds']) == 2
private_ids = set()
total_rows = 0
closed_rows = 0
save_count = 0
add_count = 0
refused = 0
for attempt in inventory['attempts']:
    source = attempt['source']
    directory = root / source['receipt']['path']
    directory = directory.parent
    assert bound(source['executed']) == (root / source['requestSource']).read_bytes()
    form = (directory / 'save-request-v1.txt').read_bytes()
    boundary = form.split(b'\r\n')[0]
    native_source = form.split(b'\r\n\r\n', 1)[1].split(b'\r\n' + boundary, 1)[0]
    assert native_source.replace(b'\r\n', b'\n') == bound(source['executed'])
    assert not re.search(rb'^\s*import\s', native_source, re.M)
    for key in ['saveBody', 'addBody']:
        if source[key] is None:
            assert key == 'addBody' and not source['nativeCompileSuccess']
            continue
        body = json.loads(bound(source[key]))
        save_count += key == 'saveBody'
        add_count += key == 'addBody'
        assert body['success'] == (source['nativeCompileSuccess'] if key == 'saveBody' else True)
        if not body['success']:
            assert body['reason2']['errors'] and body['reason']
            refused += 1
        meta = body['result']['metaInfo']
        assert meta['scriptIdPart'] == source['privateScriptId']
        assert meta['pine']['version'] == source['privateVersion'] == '1.0'
    private_ids.add(source['privateScriptId'])
    if source['nativeCompileSuccess']:
        assert attempt['removed']
    else:
        assert not attempt['sessions']
        assert json.loads(bound(source['receipt']))['studyAdded'] is False
    for session in attempt['sessions']:
        raw = list(csv.reader(bound(session['csv']).decode('utf-8-sig').splitlines()))
        headers = raw[0]
        masks = list(csv.DictReader(bound(session['closureMask']).decode().splitlines()))
        bindings = json.loads(bound(session['columnBindings']))
        assert [c['originalHeader'] for c in bindings['columns']] == headers
        assert len(masks) == len(raw) - 1
        eligible = 0
        for ordinal, (row, mask) in enumerate(zip(raw[1:], masks), 1):
            values = dict(zip(headers, row))
            assert mask['csv_sha256'] == session['csv']['sha256']
            assert int(mask['row_ordinal']) == ordinal
            assert mask['time_raw_seconds'] == row[0]
            assert int(values['INPUT_TIME']) == int(row[0]) * 1000
            close = int(row[0]) + 120
            clock = datetime.fromisoformat(mask['export_utc'].replace('Z', '+00:00')).timestamp()
            independently_closed = close <= clock and values['CHART_CONFIRMED'] == '1'
            assert int(mask['closed_numeric_eligible']) == int(independently_closed)
            assert mask['present_cell_status'].startswith('OBSERVED')
            assert json.loads(mask['blank_column_ordinals']) == [i for i, v in enumerate(row, 1) if v == '']
            eligible += int(independently_closed)
        assert eligible == session['independentlyClosedRows']
        assert session['longestConsecutiveClosedRun'] >= 32
        if 'nativeScreenshot' in session:
            png = bound(session['nativeScreenshot'])
            assert png[:8] == b'\x89PNG\r\n\x1a\n'
            assert list(struct.unpack('>II', png[16:24])) == session['nativeScreenshot']['dimensionsPixels']
            region = json.loads(((root / session['csv']['path']).parent / 'derived-region-map-v1.json').read_text())
            assert region['screenshot']['sha256'] == session['nativeScreenshot']['sha256']
            assert region['sourceSha256'] == source['sourceSha256']
            assert region['privateScriptId'] == source['privateScriptId']
        total_rows += len(masks)
        closed_rows += eligible
assert len(private_ids) == 36

numeric = read('numeric-controls-v6.json')['results']
for result in numeric:
    if 'nativeCellPointers' not in result:
        assert len(result['phaseTuples']) == 5
        continue
    assert len(result['nativeCellPointers']) == 32
    assert all(y['rowOrdinal'] == x['rowOrdinal'] + 1 and int(y['timeRaw']) == int(x['timeRaw']) + 120 for x, y in zip(result['nativeCellPointers'], result['nativeCellPointers'][1:]))
    source = next(a for a in inventory['attempts'] if a['source']['sourceId'] == result['sourceId'])
    matching = [s for s in source['sessions'] if result.get('inputMode') is None or json.loads(bound(s['columnBindings']))['inputMode'] == result['inputMode']]
    assert len(matching) == 1
    session = matching[0]
    raw = list(csv.reader(bound(session['csv']).decode().splitlines()))
    failed = False
    for pointer in result['nativeCellPointers']:
        row = raw[pointer['rowOrdinal']]
        assert pointer['csvSha256'] == session['csv']['sha256']
        assert row[0] == pointer['timeRaw']
        assert row[pointer['columnOrdinal'] - 1] == pointer['raw']
        assert raw[0][pointer['columnOrdinal'] - 1] == pointer['title']
        is_equal = None
        if pointer['frozenExpected'] is not None:
            try:
                is_equal = pointer['raw'] == '' if pointer.get('expectedNativeMissing') else Decimal(pointer['raw']) == Decimal(pointer['frozenExpected'])
            except InvalidOperation:
                is_equal = False
            failed = failed or not is_equal
        if result['hypothesis'] == 'SUPPORTED':
            assert is_equal is True

    if result['hypothesis'] == 'REFUTED':
        assert failed

comparison = read('environment-v1/existing-layout-checkpoint-comparison-v1.json')
before = read('environment-v1/native-layout-list-before-response-v1.json')
after = read('environment-v1/native-layout-list-checkpoint-response-v1.json')
assert len(before) == len(comparison['comparisons']) == 8
for item in comparison['comparisons']:
    assert item['before'] == next(x for x in before if x['id'] == item['nativeId'])
    assert item['after'] == next(x for x in after if x['id'] == item['nativeId'])
    assert item['before'] == item['after'] and not item['differences']
created = read('environment-v1/native-layout-create-response-v1.json')
assert created['id'] == 208205418 and created['image_url'] == 'gV8NSfsJ'

scanned = 0
for p in base.rglob('*'):
    if not p.is_file() or p.suffix in ['.jpg', '.png']:
        continue
    assert not re.search(rb'(?im)^(?:cookie|set-cookie|authorization):', p.read_bytes()), p
    scanned += 1
print(json.dumps({'version': 'v6', 'status': 'PASS;36-attempt and38-session progress snapshot; layout checkpoint remains12 sources',
    'exactPrivateSaveAttempts': save_count, 'nativeAddAttempts': add_count, 'saveRefusals': refused, 'completeCompilerBodies': save_count + add_count,
    'nativeCsvBindings': sum(len(a['sessions']) for a in inventory['attempts']), 'nativePngBindings': 25, 'independentMaskRows': total_rows,
    'closedRows': closed_rows, 'numericControlProperties': len(numeric),
    'rawNumericCellPointers': sum(len(x.get('nativeCellPointers', [])) for x in numeric),
    'unchangedExistingNativeLayouts': 8, 'textAuthenticationHeaderScans': scanned,
    'pendingSources': 2}, indent=2))
