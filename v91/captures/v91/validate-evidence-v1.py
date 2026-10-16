import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from decimal import Decimal, getcontext
from pathlib import Path

ROOT=Path('v91/captures/v91')
CHECKS=Counter()
CACHE={}
getcontext().prec=100


def read(p):
    return json.loads(Path(p).read_text())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def data(path, expected=None):
    if path not in CACHE:
        raw=list(csv.reader(Path(path).open(newline='')))
        CACHE[path]=(raw[0],raw[1:],sha(path))
    h,rows,digest=CACHE[path]
    assert expected is None or expected==digest,path
    return h,rows


def epoch(s):
    return datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()


inventory=read(ROOT/'attempt-inventory-v1.json')
manifest=read('v91/bundle-manifest-v1.json')
assets={a['probe']:a for a in manifest['scripts']}
identities=[]
for entry in inventory['attempts']:
    o=read(entry['observationPath']);assert sha(entry['observationPath'])==entry['observationSha256']
    p=Path(entry['observationPath']).parent
    source=(p/'executed-v1.pine').read_bytes();expected=(Path('v91')/assets[o['probe']]['path']).read_bytes()
    assert sha(p/'executed-v1.pine')==o['executedSourceSha256']
    assert (source==expected)==o['sourceMatchesRequest']
    form=(p/'save-request-v1.txt').read_bytes();sep=b'\r\n' if b'\r\n' in form else b'\n';boundary=form.strip().split(sep)[0]
    actual=form.split(sep+sep,1)[1].split(sep+boundary,1)[0]
    assert actual.replace(b'\r\n',b'\n')==source
    assert hashlib.sha256(actual).hexdigest()==o['nativeMultipartSourceSha256']
    response=read(p/'save-response-v1.json');meta=response['result']['metaInfo']
    assert meta['scriptIdPart']==o['privateScriptId'] and meta['pine']['version']=='1.0'
    identities.append(o['privateScriptId'])
    if o['sourceMatchesRequest']:
        assert response['success'] and read(p/'add-response-v1.json')['success']
        assert (p/'post-remove-v1.txt').exists()
        for prefix in ['save','add']:
            receipt=read(p/(prefix+'-transport-v1.json'));body=p/(prefix+'-response-v1.json')
            assert sha(body)==receipt['responseSha256'] and body.stat().st_size==receipt['responseBytes']
            CHECKS['exactSourceCompilerBodies']+=1
        assert len(o['exportPaths'])>0
        CHECKS['exactSourceSaveAddRuns']+=1
    else:
        assert not response['success'] and not (p/'add-response-v1.json').exists()
        CHECKS['failedEntrySavesRetainedWithoutAdd']+=1
    assert o['immediateMarkers'] is None and o['settledMarkers'] is None
assert len(identities)==len(set(identities))==18

for p in sorted(ROOT.glob('**/*-native-v1.csv')):
    h,rows=data(str(p));stage=p.name.removesuffix('-native-v1.csv')
    raw_sha=sha(p)
    b=read(p.parent/(stage+'-column-bindings-v1.json'))
    assert b['sha256']==sha(p) and b['headers']==h and b['rows']==len(rows)
    download=read(p.parent/(stage+'-download-v1.json'));trigger=read(p.parent/(stage+'-export-trigger-v1.json'))
    assert download['sha256']==sha(p) and download['downloadModifiedAtEpoch']>=epoch(trigger['startedAtUtc'])-.5
    assert download['exportTrigger']['startedAtUtc']==trigger['startedAtUtc']
    assert all(len(row)==len(h) for row in rows)
    assert all(int(brow[0])-int(arow[0])==120 for arow,brow in zip(rows,rows[1:]))
    assert sorted(x['columnOrdinal'] for x in b['plotBindings'])==list(range(7,len(h)+1))
    for binding in b['plotBindings']:
        assert h[binding['columnOrdinal']-1]==binding['nativePlotTitle']
    masks=list(csv.DictReader((p.parent/(stage+'-row-closure-mask-v1.csv')).open()))
    assert len(masks)==len(rows)
    for i,(row,mask) in enumerate(zip(rows,masks),1):
        assert int(mask['data_row_ordinal_1based_excluding_header'])==i and mask['csv_sha256']==raw_sha
        assert mask['time_raw']==row[0]
        assert int(mask['observed_plot_cell_count'])==sum(v!='' for v in row[6:])
        assert int(mask['blank_plot_cell_count'])==sum(v=='' for v in row[6:])
        if mask['closed_eligible']=='1':
            assert int(row[0])+120<=epoch(trigger['startedAtUtc'])
            own=next((n for n in ['CHART_ISCONFIRMED','FRONTIER_ISCONFIRMED','INPUT_CHART_CONFIRMED'] if n in h),None)
            if own:
                assert row[h.index(own)]=='1'
            else:
                reference=b['independentConfirmationReferences'][mask['independent_confirmation_reference']]
                rh,rr=data(reference['path'],reference['sha256'])
                ri=(int(row[0])-int(rr[0][0]))//120
                assert rr[ri][0]==row[0] and rr[ri][1:6]==row[1:6] and rr[ri][rh.index('CHART_ISCONFIRMED')]=='1'
            if 'INPUT_D_TIME_CLOSE' in h:
                assert int(row[h.index('INPUT_D_TIME_CLOSE')])<=b['dailyObservationCutoffMs']
        CHECKS['independentMaskRowsVerified']+=1
    CHECKS['nativeCsvDownloadsBindingsAndShapes']+=1


def verify_fields(raw_fields,provenance,logical_names=True):
    h,rows=data(provenance['csv'],provenance['sha256']);row=rows[provenance['dataRowOrdinal']-1]
    for name,column in zip(raw_fields,provenance['columnOrdinals']):
        assert h[column-1]==name and row[column-1]==raw_fields[name]
        CHECKS['derivedRawCellReferences']+=1
    return h,row


facets=read(ROOT/'footprint-repeat-facets-v1.json')
expected_variants=defaultdict(lambda:defaultdict(list))
for record in facets['records']:
    h,row=verify_fields(record['rawFields'],record['provenance'])
    assert row[0]==record['key']['timeSecondsRaw']
    f=record['rawFields']
    if 'FP_TOTAL_VOLUME' in f:
        values=tuple(f[n] for n in ['FP_TOTAL_VOLUME','FP_BUY_VOLUME','FP_SELL_VOLUME','FP_DELTA'])
        expected_variants[row[0]][values].append(record['provenance'])
        total,buy,sell,delta=map(Decimal,values);relation=record['rawDecimalRelations']
        assert Decimal(relation['totalMinusBuyPlusSellDecimal'])==total-(buy+sell)
        assert Decimal(relation['deltaMinusBuyMinusSellDecimal'])==delta-(buy-sell)
for key in facets['summaryVariantsByKey']:
    expected=expected_variants[key['timeSecondsRaw']]
    assert key['rawVariantCount']==len(expected)
    for variant in key['variants']:
        assert variant['totalBuySellDeltaRaw'] in [list(v) for v in expected]
        for observation in variant['observations']:
            h,rows=data(observation['provenance']['csv'],observation['provenance']['sha256'])
            row=rows[observation['provenance']['dataRowOrdinal']-1]
            assert row[0]==key['timeSecondsRaw']
            assert [row[h.index(n)] for n in ['FP_TOTAL_VOLUME','FP_BUY_VOLUME','FP_SELL_VOLUME','FP_DELTA']]==variant['totalBuySellDeltaRaw']
            CHECKS['perKeyCrossRepeatVariantReferences']+=1

price_rows=read(ROOT/'native-price-rows-v1.json')
for record in price_rows['records']:
    assert [r['role'] for r in record['roles']]==['LOWEST','POC','HIGHEST']
    for role in record['roles']:
        _,row=verify_fields(role['rawFields'],role['provenance']);assert row[0]==record['timeSecondsRaw']
        CHECKS['boundedNativePriceRoles']+=1

frontiers=read(ROOT/'cumulative-frontier-v1.json')
for record in frontiers['exports']:
    h,rows=data(record['path'],record['sha256'])
    assert record['nativeFirstPhysicalRowRaw']==rows[0] and record['nativeLastPhysicalRowRaw']==rows[-1]
    assert record['originalOwnedFrontierFields'] is None
    for field,detail in record['companionOwnedFields'].items():
        assert h[detail['columnOrdinal']-1]==field and rows[0][detail['columnOrdinal']-1]==detail['firstRaw'] and rows[-1][detail['columnOrdinal']-1]==detail['lastRaw']
    if record['companionFrontierStatus']=='COMPLETE-INDEX0-OBSERVED':
        assert rows[0][h.index('FRONTIER_BAR_INDEX')]=='0' and rows[0][h.index('FRONTIER_ISFIRST')]=='1'
        assert rows[0][h.index('FIRST_CHART_TIME')]==str(int(rows[0][0])*1000)
        assert all(int(row[h.index('FRONTIER_BAR_INDEX')])==i for i,row in enumerate(rows))
        CHECKS['completeCompanionFrontiers']+=1

events=[json.loads(line) for line in (ROOT/'developing-input-events-v1.jsonl').read_text().splitlines()]
for event in events:
    h,rows=data(event['provenance']['csv'],event['provenance']['sha256']);row=rows[event['provenance']['dataRowOrdinal']-1]
    assert row[0]==event['targetChartTimeSecondsRaw']
    for channel in ['originalOwnedTargetFields','companionOnlyInputClockFlagsFields']:
        for name,field in event[channel].items():
            assert h[field['columnOrdinal']-1]==name and row[field['columnOrdinal']-1]==field['valueRaw']
            assert field['valueStatus']==('OBSERVED' if field['valueRaw']!='' else 'NA-RAW-BLANK')
            CHECKS['developingRawTargetInputCells']+=1
    assert event['sourceSpecificExactAsOfInputIdentity'] is None and event['closedScoreEligible'] is False
    CHECKS['developingEvents']+=1

for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix in ['.json','.jsonl','.txt','.md','.csv','.pine','.py']:
        assert not re.search(r'(?im)^\s*["\x27]?(?:cookie|set-cookie|authorization)\s*:',p.read_text()),p
        CHECKS['publicTextAuthenticationHeaderScans']+=1

assert CHECKS['exactSourceSaveAddRuns']==15 and CHECKS['failedEntrySavesRetainedWithoutAdd']==3
assert CHECKS['nativeCsvDownloadsBindingsAndShapes']==18 and CHECKS['independentMaskRowsVerified']==243625
assert CHECKS['boundedNativePriceRoles']==27 and CHECKS['developingEvents']==8
assert CHECKS['completeCompanionFrontiers']==2
print(json.dumps({'status':'PASS','checks':dict(CHECKS)},indent=2))
