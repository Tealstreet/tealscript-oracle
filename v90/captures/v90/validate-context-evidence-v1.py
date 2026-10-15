import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path('v90/captures/v90')
CACHE = {}
CHECKS = Counter()


def read(p):
    return json.loads(Path(p).read_text())


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def csv_data(p, expected_hash=None):
    if p not in CACHE:
        rows = list(csv.reader(Path(p).open(newline='')))
        CACHE[p] = (rows[0], rows[1:], digest(p))
    h, rows, sha = CACHE[p]
    assert expected_hash is None or expected_hash == sha, p
    return h, rows


def sec(utc):
    return datetime.fromisoformat(utc.replace('Z', '+00:00')).timestamp()


manifest = read('v90/bundle-manifest-v1.json')
assets = {a['probe']: a for a in manifest['scripts']}
for p in sorted(ROOT.glob('v90-*/attempt-v*/observation-v1.json')):
    if 'dxy' in str(p):
        continue
    d = p.parent
    obs = read(p)
    expected = Path('v90') / assets[obs['probe']]['path']
    assert expected.read_bytes() == (d / 'executed-v1.pine').read_bytes()
    assert digest(expected) == obs['sourceSha256']
    body = (d / 'save-request-v1.txt').read_bytes()
    sep = b'\r\n' if b'\r\n' in body else b'\n'
    boundary = body.strip().split(sep)[0]
    source = body.split(sep + sep, 1)[1].split(sep + boundary, 1)[0]
    assert source.replace(b'\r\n', b'\n') == expected.read_bytes()
    CHECKS['exactNativeMultipartSourceBindings'] += 1
    for prefix in ['save', 'add']:
        receipt = read(d / (prefix + '-transport-v1.json'))
        response = d / (prefix + '-response-v1.json')
        decoded = read(response)
        assert response.stat().st_size == receipt['responseBytes'] and digest(response) == receipt['responseSha256']
        assert decoded['success'] is True
        assert decoded['result']['metaInfo']['scriptIdPart'] == obs['privateScriptId']
        assert decoded['result']['metaInfo']['pine']['version'] == obs['scriptVersion']
        CHECKS['completeSuccessfulCompilerBodies'] += 1
    for e in obs['exports']:
        h, rows = csv_data(e['path'], e['sha256'])
        assert h == e['headers'] and len(rows) == e['rows']
        stage = e['stage']
        trigger = read(d / (stage + '-export-trigger-v1.json'))
        download = read(d / (stage + '-download-v1.json'))
        assert download['sha256'] == e['sha256'] and download['downloadModifiedAtEpoch'] >= sec(trigger['startedAtUtc']) - .5
        assert download['exportTrigger']['startedAtUtc'] == trigger['startedAtUtc']
        bindings = read(d / (stage + '-column-bindings-v1.json'))
        assert bindings['sha256'] == e['sha256'] and [c['headerRaw'] for c in bindings['columns']] == h
        masks = list(csv.DictReader((d / (stage + '-row-closure-mask-v1.csv')).open()))
        assert len(masks) == len(rows)
        for ordinal, (row, mask) in enumerate(zip(rows, masks), 1):
            assert int(mask['data_row_ordinal_1based_excluding_header']) == ordinal
            assert mask['time_raw'] == row[0] and mask['csv_sha256'] == e['sha256']
            if mask['closed_eligible'] == '1':
                if 'CHART_ISCONFIRMED' in h:
                    assert row[h.index('CHART_ISCONFIRMED')] == '1'
                else:
                    reference = bindings['confirmationReferences'][mask['confirmation_reference_id']]
                    rh, rr = csv_data(reference['csv'], reference['sha256'])
                    ri = (int(row[0]) - int(reference['referenceFirstTimeRaw'])) // 120
                    assert rr[ri][0] == row[0] and rr[ri][1:6] == row[1:6]
                    assert rr[ri][rh.index('CHART_ISCONFIRMED')] == '1'
                interval = 86400 if 'daily-chart' in obs['probe'] else 120
                assert int(row[0]) + interval <= sec(trigger['startedAtUtc'])
                if 'D_CLOSE_TIME' in h:
                    assert int(row[h.index('D_CLOSE_TIME')]) <= bindings['dailyGlobalObservationCutoffMs']
            CHECKS['shaRowKeyedClosureMasks'] += 1
        CHECKS['nativeCsvShapeTimestampAndDownloadFreshness'] += 1

daily = read(ROOT / 'daily-provider-table-v1.json')
for day in daily['days']:
    for variant in day['variants']:
        for o in variant['provenance']:
            h, rows = csv_data(o['csv'], o['sha256'])
            start, end = o.get('rowOrdinalRangeInclusive', [o.get('rowOrdinal'), o.get('rowOrdinal')])
            time_col = h.index('D_TIME') if 'D_TIME' in h else None
            for i in range(start, end + 1):
                row = rows[i-1]
                assert [row[c-1] for c in o['columnOrdinals']] == variant['ohlcvRaw']
                assert (row[time_col] if time_col is not None else str(int(row[0])*1000)) == day['requestedDayTimeMsRaw']
                CHECKS['dailyProviderRowDerivations'] += 1

for filename, key, valuekey, start_col, end_col in [
    ('chart2m-inputs-v1.json', 'ohlcvVariants', 'valuesRaw', 1, 6),
    ('prefix-table-v1.json', 'variants', 'ohlcvAndPlotRaw', 1, 7)]:
    table = read(ROOT / filename)
    sources = table['sources']
    for record in table['records']:
        for variant in record[key]:
            for o in variant['observations']:
                source = sources[o['sourceId']]
                _, rows = csv_data(source['path'], source['sha256'])
                row = rows[o['dataRowOrdinal']-1]
                assert row[0] == record['timeRaw'] and row[start_col:end_col] == variant[valuekey]
                CHECKS[filename + 'RowDerivations'] += 1

fp = read(ROOT / 'provider-presence-v1.json')
for record in fp['records']:
    for o in record['observations']:
        source = fp['sources'][o['sourceId']]
        h, rows = csv_data(source['path'], source['sha256'])
        row = rows[o['dataRowOrdinal']-1]
        assert row[0] == record['timeRaw'] and row[6] == o['targetPresencePlotRaw']
        if o['nativeGetterValuesRaw'] is not None:
            assert row[11:15] == o['nativeGetterValuesRaw']
        if o['providerStatus'] == 'PRESENT':
            assert row[6] == '1' and all(x != '' for x in row[11:15]) and len(row) == 15
        if o['providerStatus'] == 'UNAVAILABLE':
            assert row[6] == '0'
        CHECKS['footprintProviderRawCellDerivations'] += 1

for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix in ['.json', '.jsonl', '.md', '.txt', '.pine', '.py', '.csv']:
        content = p.read_text()
        assert not re.search(r'(?im)^\s*(?:["\x27])?(?:cookie|set-cookie|authorization)\s*:', content), p
        CHECKS['publicTextFilesWithoutAuthenticationHeaderLines'] += 1

assert CHECKS['exactNativeMultipartSourceBindings'] == 25
assert CHECKS['completeSuccessfulCompilerBodies'] == 50
assert CHECKS['nativeCsvShapeTimestampAndDownloadFreshness'] == 28
print(json.dumps({'status': 'PASS', 'checks': dict(CHECKS)}, indent=2))
