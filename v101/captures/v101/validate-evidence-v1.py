import csv
import hashlib
import json
import re
import runpy
import sys
from datetime import datetime
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]


def read(path):
    return json.loads(path.read_text())


def bound(reference):
    raw = (ROOT / reference['path']).read_bytes()
    assert len(raw) == reference['bytes'] and hashlib.sha256(raw).hexdigest() == reference['sha256'], reference['path']
    return raw


def signature(text):
    return dict(url=re.search(r'url="([^"]+)"', text)[1], canvas=re.findall(r'Canvas "([^"]+)"', text), checkedRadios=re.findall(r'radio "([^"]+)" checked', text), activeLayout=re.findall(r'button "Logged in as [^"]+ Active layout: ([^"]+)"', text))


def validate(revision=1, integrity=True, preservation=True):
    manifest = read(ROOT / 'v101/bundle-manifest-v1.json')
    asset = manifest['sources'][0]
    requested = (ROOT / asset['path']).read_bytes()
    assert len(requested) == asset['bytes'] and hashlib.sha256(requested).hexdigest() == asset['sha256']
    prefix = bound(asset['preservedV100Prefix'])
    assert requested[:len(prefix)] == prefix
    for entry in manifest['predictionArtifacts'] + manifest['priorEvidence']:
        bound(entry)
    inventory = read(BASE / f'attempt-inventory-v{revision}.json')
    numeric = read(BASE / f'numeric-controls-v{revision}.json')
    assert len(inventory['attempts']) == 1
    assert len(list(BASE.glob('*/attempt-v1/attempt-start-v1.json'))) == 1
    assert not list(BASE.glob('**/history-navigation-action*.json'))
    attempt = inventory['attempts'][0]
    source = attempt['source']
    assert bound(source['executed']) == requested
    assert source['sourceSha256'] == asset['sha256']
    assert not re.search(rb'^\s*import\s', requested, re.M)
    form = bound(source['sourceForm'])
    separator = b'\r\n' if b'\r\n' in form else b'\n'
    boundary = form.split(separator)[0]
    assert form.split(separator + separator, 1)[1].split(separator + boundary, 1)[0].replace(b'\r\n', b'\n') == requested
    receipt = json.loads(bound(source['receipt']))
    saved, added = json.loads(bound(source['saveBody'])), json.loads(bound(source['addBody']))
    assert saved['success'] and added['success'] and receipt['sourceExact'] and receipt['removed']
    meta = added['result']['metaInfo']
    private = source['privateScriptId']
    assert saved['result']['metaInfo']['scriptIdPart'] == meta['scriptIdPart'] == private
    assert saved['result']['metaInfo']['pine']['version'] == source['privateVersion'] == '1.0'
    old_inventory = read(ROOT / 'v100/captures/v100/attempt-inventory-v3.json')
    assert private not in {a['source']['privateScriptId'] for a in old_inventory['attempts']}
    assert len(attempt['sessions']) == len(receipt['sessions']) == 1
    session = attempt['sessions'][0]
    raw = list(csv.reader(bound(session['csv']).decode('utf-8-sig').splitlines()))
    headers, rows = raw[0], raw[1:]
    titles = re.findall(r'plot\([^\n]*title="([^"]+)"', requested.decode())
    assert titles == [p['title'] for p in asset['plots']] and len(set(titles)) == 40
    bindings = json.loads(bound(session['columnBindings']))
    assert [c['originalHeader'] for c in bindings['columns']] == headers
    owned = set()
    for c in bindings['columns']:
        ordinal = c.get('sourceLiteralPlotOrdinal')
        if ordinal is None:
            continue
        title = titles[ordinal]
        assert c['owner'] == private and c['sourceSha256'] == asset['sha256'] and c['privateVersion'] == '1.0'
        assert c['originalHeader'] == title and meta['styles'][c['nativePlotId']]['title'] == title
        assert headers.count(title) == 1
        owned.add(title)
    assert not bindings['missingOrAmbiguousRequestedPlotTitles'] and owned == set(titles)
    assert not bindings['actuallyExportedColorerColumns'] and not bindings['nativeColorerDefinitions']
    directory = (ROOT / session['csv']['path']).parent
    download = read(directory / 'chart-download-v1.json')
    clock = datetime.fromisoformat(download['exportTrigger']['startedAtUtc'].replace('Z', '+00:00')).timestamp()
    end = datetime.fromisoformat(receipt['completedAtUtc'].replace('Z', '+00:00')).timestamp()
    assert clock <= download['downloadModifiedAtEpoch'] <= end and download['sha256'] == session['csv']['sha256']
    masks = list(csv.DictReader(bound(session['closureMask']).decode().splitlines()))
    assert len(rows) == len(masks) == session['dataRows']
    closed = []
    for n, (row, mask) in enumerate(zip(rows, masks), 1):
        assert len(row) == len(headers)
        values = dict(zip(headers, row))
        context = all(values[t] for t in titles[:3])
        if context:
            context = F(values['INPUT_INDEX']).denominator == 1 and F(values['INPUT_TIME']) == 1000 * F(values['time'])
        eligible = context and not session['runtimeFailed'] and F(values['time']) + 120 <= clock and F(values['CHART_CONFIRMED']) == 1
        assert int(mask['closed_numeric_eligible']) == bool(eligible)
        assert mask['csv_sha256'] == session['csv']['sha256'] and int(mask['row_ordinal']) == n
        assert mask['time_raw_seconds'] == values['time'] and mask['input_time_raw_ms'] == values['INPUT_TIME']
        assert mask['input_index_raw'] == values['INPUT_INDEX'] and mask['native_confirmed_raw'] == values['CHART_CONFIRMED']
        assert json.loads(mask['blank_column_ordinals']) == [i for i, value in enumerate(row, 1) if value == '']
        if eligible:
            closed.append(n)
    selected = []
    for start in closed:
        block = list(range(start, start + 64))
        if not all(n in closed for n in block):
            continue
        indices = [F(rows[n - 1][headers.index('INPUT_INDEX')]) for n in block]
        times = [F(rows[n - 1][0]) for n in block]
        if all(b == a + 1 for a, b in zip(indices, indices[1:])) and all(b > a for a, b in zip(times, times[1:])):
            selected = block
            break
    assert selected == session['selectedPrimaryConsecutiveClosedRows']
    assert closed == session['eligibleDataRowOrdinals'] and len(closed) == session['independentlyClosedRows']
    assert session['primaryInputCertificateValid'] == (len(selected) == 64)
    for n, mask in enumerate(masks, 1):
        primary = len(selected) == 64 and n in selected
        assert int(mask['primary_scoring_eligible']) == primary
        assert mask['present_cell_status'] == ('OBSERVED' if primary else 'OBSERVED / EXCLUDED')
        assert primary or mask['primary_exclusion_cause']
    assert runpy.run_path(str(BASE / 'analyze-evidence-v1.py'))['analyze'](revision) == numeric
    mapping = read(ROOT / manifest['predictionMap'])
    counts = dict(nativeSaves=1, nativeAdds=1, completeCompilerBodies=2, originalCSVs=1, dataRows=len(rows), independentlyClosedRows=len(closed), primaryRows=len(selected), uniquePrimaryPlotCells=len(selected) * 40, uniquePrimaryColorCodeCells=len(selected) * 37, repeatedControlCells=len(selected) * 36, newDiscriminatorCells=len(selected), modelComparisons=0)

    def check_pointer(pointer):
        assert pointer['csvSha256'] == session['csv']['sha256']
        n, c = pointer['rowOrdinal'], pointer['columnOrdinal']
        assert n in closed and headers[c - 1] == pointer['headerRaw'] and raw[n][c - 1] == pointer['valueRaw']

    for index, model in enumerate(numeric['models']):
        frozen = mapping['models'][index]
        assert model['modelId'] == frozen['modelId'] and model['predictionPointer'] == '/models/' + str(index)
        bound(model['predictionMap']); bound(model['recipeFile'])
        all_codes = []
        for prop, expected in zip(model['properties'], frozen['expectedColumns']):
            assert prop['title'] == expected['title'] and prop['sourcePlotOrdinal'] == expected['sourcePlotOrdinal'] and prop['expectedRawCode'] == expected['expectedRawCode']
            for comparison in prop['comparisons']:
                point = comparison['target']; check_pointer(point)
                try:
                    code = 'S' if F(point['valueRaw']) == F(expected['expectedRawCode']) else 'R'
                except (ValueError, ZeroDivisionError):
                    code = 'R'
                assert comparison['verdict'] == code
                all_codes.append(code); counts['modelComparisons'] += 1
        status = 'REFUTED' if 'R' in all_codes else 'SUPPORTED' if len(selected) == 64 and len(all_codes) == 64 * 37 and all(c == 'S' for c in all_codes) else 'UNDECIDED'
        assert model['verdict'] == status
    prior = list(csv.reader(bound(mapping['controlReference']['csv']).decode().splitlines()))
    for control in numeric['priorControls']:
        old = control['priorReference']
        assert old['csvSha256'] == mapping['controlReference']['csv']['sha256'] and prior[0][old['columnOrdinal'] - 1] == old['headerRaw'] and prior[old['rowOrdinal']][old['columnOrdinal'] - 1] == old['valueRaw']
        for comparison in control['targets']:
            check_pointer(comparison['target'])
            try:
                matches = F(comparison['target']['valueRaw']) == F(old['valueRaw'])
            except (ValueError, ZeroDivisionError):
                matches = False
            assert comparison['verdict'] == ('S' if matches else 'R')
    if preservation:
        before = read(BASE / 'environment-v1/native-layout-list-before-response-v1.json')
        after = read(BASE / 'environment-v2/native-layout-list-after-response-v1.json')
        indexed = {r['id']: r for r in after}
        creation = read(BASE / 'environment-v1/native-layout-create-response-v1.json')
        assert len(before) == 16 and len(after) == 17 and creation['id'] not in {r['id'] for r in before}
        assert indexed[creation['id']]['image_url'] == creation['image_url']
        comparison = read(BASE / 'environment-v2/existing-layout-comparison-v1.json')
        equal = [r == indexed.get(r['id']) for r in before]
        assert equal == [r['equal'] for r in comparison['savedRecordComparisons']]
        tabs = [signature((BASE / f'environment-v1/page-{p}-before-v1.txt').read_text()) == signature((BASE / f'environment-v2/page-{p}-after-v1.txt').read_text()) for p in range(1, 13)]
        assert tabs == [r['equal'] for r in comparison['openTabComparisons']]
        counts.update(oldSavedRecordsUnchanged=sum(equal), oldSavedRecordsChanged=sum(not x for x in equal), oldOpenTabsUnchanged=sum(tabs), oldOpenTabsChanged=sum(not x for x in tabs))
    if integrity:
        references = read(BASE / f'artifact-integrity-v{revision}.json')['artifacts']
        assert len({r['path'] for r in references}) == len(references)
        for reference in references:
            bound(reference)
        counts['integrityBoundFiles'] = len(references)
    return dict(version=f'v{revision}', status='PASS', counts=counts, modelSummary=numeric['modelSummary'], modelVerdicts={m['modelId']: m['verdict'] for m in numeric['models']}, policy='Read-only independent source/form/ownership/closure/selection/pointer/integer/preservation/integrity validation; model comparisons never multiply native cells')


if __name__ == '__main__':
    print(json.dumps(validate(int(sys.argv[1]) if len(sys.argv) > 1 else 1), indent=2))
