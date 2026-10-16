# SPDX-License-Identifier: MIT
import csv
import hashlib
import json
import re
import struct
from datetime import datetime
from decimal import Decimal
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

inventory = read('attempt-inventory-v1.json')
assert inventory['capturedSources'] == 12
assert len(inventory['remainingSourceIds']) == 26
private_ids = set()
total_rows = 0
closed_rows = 0
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
        body = json.loads(bound(source[key]))
        assert body['success'] is True
        meta = body['result']['metaInfo']
        assert meta['scriptIdPart'] == source['privateScriptId']
        assert meta['pine']['version'] == source['privateVersion'] == '1.0'
    private_ids.add(source['privateScriptId'])
    assert attempt['removed']
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
        png = bound(session['nativeScreenshot'])
        assert png[:8] == b'\x89PNG\r\n\x1a\n'
        assert list(struct.unpack('>II', png[16:24])) == session['nativeScreenshot']['dimensionsPixels']
        region = read(str((directory / 'session-mode0-v1/derived-region-map-v1.json').relative_to(base)))
        assert region['screenshot']['sha256'] == session['nativeScreenshot']['sha256']
        assert region['sourceSha256'] == source['sourceSha256']
        assert region['privateScriptId'] == source['privateScriptId']
        total_rows += len(masks)
        closed_rows += eligible
assert len(private_ids) == 12

numeric = read('numeric-controls-v1.json')['results']
for result in numeric:
    assert len(result['nativeCellPointers']) == 32
    source = next(a for a in inventory['attempts'] if a['source']['sourceId'] == result['sourceId'])
    session = source['sessions'][0]
    raw = list(csv.reader(bound(session['csv']).decode().splitlines()))
    for pointer in result['nativeCellPointers']:
        row = raw[pointer['rowOrdinal']]
        assert pointer['csvSha256'] == session['csv']['sha256']
        assert row[0] == pointer['timeRaw']
        assert row[pointer['columnOrdinal'] - 1] == pointer['raw']
        assert raw[0][pointer['columnOrdinal'] - 1] == pointer['title']
        if result['hypothesis'] == 'SUPPORTED':
            assert Decimal(pointer['raw']) == Decimal(pointer['frozenExpected'])

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
print(json.dumps({'version': 'v1', 'status': 'PASS;12-source progress checkpoint only',
    'exactPrivateSaveAddRuns': 12, 'completeCompilerBodies': 24,
    'nativeCsvAndPngBindings': 12, 'independentMaskRows': total_rows,
    'closedRows': closed_rows, 'numericControlProperties': len(numeric),
    'rawNumericCellPointers': sum(len(x['nativeCellPointers']) for x in numeric),
    'unchangedExistingNativeLayouts': 8, 'textAuthenticationHeaderScans': scanned,
    'pendingSources': 26}, indent=2))
