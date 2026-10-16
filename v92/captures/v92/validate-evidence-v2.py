import csv
import hashlib
import json
import re
import subprocess
from datetime import datetime
from decimal import Decimal
from pathlib import Path

root = Path(__file__).resolve().parents[3]
capture = Path(__file__).resolve().parent
counts = {}

def read(path):
    return json.loads((capture / path).read_text())

def verify_ref(item):
    data = (root / item['path']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == item['sha256'], item['path']
    assert len(data) == item['bytes'], item['path']
    return data

def epoch(raw):
    return datetime.fromisoformat(raw.replace('Z', '+00:00')).timestamp()

inventory = read('attempt-inventory-v2.json')
assert inventory['saveAttempts'] == inventory['addAttempts'] == 3 <= 13
assert inventory['exactSourceRuns'] == 3
ids = set()
for attempt in inventory['attempts']:
    expected = (root / attempt['source']).read_bytes()
    executed = verify_ref(attempt['executed'])
    assert executed == expected
    assert not re.search(rb'^\s*import\s', executed, re.M)
    directory = root / attempt['directory']
    form = (directory / 'save-request-v1.txt').read_bytes()
    boundary = form.split(b'\r\n')[0]
    raw_source = form.split(b'\r\n\r\n', 1)[1].split(b'\r\n' + boundary, 1)[0]
    assert raw_source.replace(b'\r\n', b'\n') == expected
    for phase in ['save', 'add']:
        body = json.loads(verify_ref(attempt[phase]))
        assert body['success'] is True
        meta = body['result']['metaInfo']
        assert meta['scriptIdPart'] == attempt['privateScriptId']
        assert meta['pine']['version'] == '1.0'
        assert meta['warnings'] == []
    ids.add(attempt['privateScriptId'])
    assert attempt['removed']
assert len(ids) == 3
counts['exactSourcePrivateSaveAddRuns'] = 3
counts['completeNativeCompilerBodies'] = 6

total_rows = 0
for item in inventory['csvInventory']:
    data = verify_ref(item['csv'])
    raw = list(csv.reader(data.decode('utf-8-sig').splitlines()))
    headers = raw[0]
    assert len(headers) == item['columns']
    assert len(raw) - 1 == item['rows']
    binding = read(item['binding'])
    assert [c['originalHeader'] for c in binding['columns']] == headers
    assert [c['columnOrdinal'] for c in binding['columns']] == list(range(1, len(headers) + 1))
    if binding['sourceExecution']:
        attempt = binding['sourceExecution']
        meta = json.loads((root / attempt['add']['path']).read_text())['result']['metaInfo']
        for col in binding['columns'][6:]:
            assert col['owner'] == meta['scriptIdPart']
            assert col['nativePlotTitle'] == meta['styles'][col['nativePlotId']]['title']
    mask = list(csv.DictReader((capture / item['closureMask']).open()))
    assert len(mask) == len(raw) - 1
    for i, (row, proof) in enumerate(zip(raw[1:], mask), 1):
        assert proof['csv_sha256'] == item['csv']['sha256']
        assert int(proof['row_ordinal']) == i and proof['time_raw'] == row[0]
        assert int(proof['bar_close_epoch']) == int(row[0]) + 120
        values = dict(zip(headers, row))
        clock = values.get('OBSERVATION_CLOCK')
        confirmed = values.get('CHART_ISCONFIRMED')
        closed = int(row[0]) + 120 <= epoch(item['observationUtc'])
        if clock:
            closed = closed and int(row[0]) * 1000 + 120000 <= int(clock)
        closed = closed and confirmed != '0'
        assert int(proof['independently_closed']) == int(closed)
        assert proof['present_cell_status'] == 'OBSERVED'
        assert proof['closed_score_credit'] == '0'
        assert json.loads(proof['blank_columns']) == [j for j, v in enumerate(row, 1) if v == '']
    total_rows += len(mask)
counts['nativeCsvBindingsMasks'] = len(inventory['csvInventory'])
counts['independentlyVerifiedMaskRows'] = total_rows
assert total_rows == inventory['maskRows'] == 2747

events = [json.loads(line) for line in (capture / 'availability-events-v1.jsonl').read_text().splitlines()]
assert len(events) == 5
assert [e['nativeIsConfirmedRaw'] for e in events] == ['0', '0', '0', '0', '1']
for event in events:
    raw = list(csv.reader(verify_ref(event['csv']).decode('utf-8-sig').splitlines()))
    row = raw[event['rowOrdinal']]
    assert row[0] == event['timeRaw'] == '1792159800'
    assert [cell['raw'] for cell in event['allRawCells']] == row
    assert [cell['header'] for cell in event['allRawCells']] == raw[0]
    v = dict(zip(raw[0], row))
    assert v['FP_AVAILABLE'] == event['fpAvailableRaw'] == '1'
    assert v['FP_AVAILABLE_ZERO_TOTAL'] == event['fpZeroTotalRaw'] == '0'
    assert Decimal(v['FP_TOTAL_VOLUME']) > 0
    assert v['FP_TOTAL_VOLUME'] == event['fpTotalRaw']
    assert v['OBSERVATION_CLOCK'] == event['nativeClockRaw']
assert all(int(b['nativeClockRaw']) > int(a['nativeClockRaw']) for a, b in zip(events, events[1:]))
assert events[-1]['nativeClockRaw'] == '1792159920356'
counts['sourceBoundAvailabilityFrames'] = len(events)

full = read('footprint-full-distribution-v2.json')
for item in full['chosenBarIndependentSourceRecords']:
    raw = list(csv.reader(verify_ref(item['csv']).decode('utf-8-sig').splitlines()))
    row = raw[item['rowOrdinal']]
    assert row[0] == full['chosenClosedBar']['barTimeRaw'] == '1792158960'
    assert [cell['raw'] for cell in item['columns']] == row
counts['selectedClosedBarIndependentSourceRecords'] = 3

facets = read('facet-capabilities-v2.json')['facets']
assert len(facets) == 6 and all(f['facetVerdict'] == 'NOT OBSERVED' for f in facets)
assert all(f['closedScoreCredit'] == 0 for f in facets)
for family in ['cumulative-original-frontier-v2.json', 'dxy-execution-input-completeness-v2.json', 'developing-input-context-v2.json']:
    result = read(family)
    assert result['facetVerdict'] == 'NOT OBSERVED'
assert (capture / 'realtime-events-v2.jsonl').read_bytes() == b''
assert (capture / 'developing-input-events-v2.jsonl').read_bytes() == b''
counts['separateHeldFacetVerdicts'] = len(facets)

comparison = read('environment-resumed-v1/existing-layout-comparison-v1.json')
native_before = read('environment-resumed-v1/native-layout-list-before-response-v1.json')
native_after = read('environment-resumed-v1/native-layout-list-after-response-v1.json')
assert len(comparison['comparisons']) == 3
for item in comparison['comparisons']:
    assert item['before'] == item['after'] and not item['differences']
    assert item['before'] == next(x for x in native_before if x['name'] == item['name'])
    assert item['after'] == next(x for x in native_after if x['name'] == item['name'])
created = read('environment-resumed-v1/native-layout-create-response-v1.json')
assert created['id'] == 208188529 and created['image_url'] == 'EPoTcWl1'
counts['unchangedExistingNativeLayoutRecords'] = 3

files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', '-z', '7e06024'], cwd=root).decode().split('\x00')
prior = [f for f in files if f.startswith('v92/captures/v92/') and f]
for name in prior:
    original = subprocess.check_output(['git', 'show', '7e06024:' + name], cwd=root)
    assert (root / name).read_bytes() == original, name
counts['publishedV1ArtifactsUnchanged'] = len(prior)

scanned = 0
for path in capture.rglob('*'):
    if not path.is_file() or path.suffix == '.jpg':
        continue
    assert not re.search(rb'(?im)^(?:cookie|set-cookie|authorization):', path.read_bytes()), path
    scanned += 1
counts['publicTextAuthenticationHeaderScans'] = scanned
print(json.dumps({'version': 'v2', 'result': 'PASS', 'checks': counts}, indent=2))
