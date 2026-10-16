import csv
import hashlib
import json
import re
import runpy
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
P = runpy.run_path(str(BASE / 'package-evidence-v1.py'))


def read(path):
    return json.loads(path.read_text())


def bound(pointer):
    raw = (ROOT / pointer['path']).read_bytes()
    assert len(raw) == pointer['bytes'] and hashlib.sha256(raw).hexdigest() == pointer['sha256']
    return raw


def validate(revision, check_integrity=True, require_preservation=False):
    inventory = read(BASE / f'attempt-inventory-v{revision}.json')
    selection = json.loads(bound(inventory['selection']))
    eligible = [r for r in selection['records'] if r['eligible']]
    assert len(eligible) == 14 and selection['mandatorySlots'] == 8 and selection['activatedConditionalSlots'] == 6
    assert [r['v95Item'] for r in eligible] == [2, 2, 3, 3, 4, 4, 5, 5, 7, 7, 10, 10, 14, 14]
    bound(selection['publishedV95Response'])
    for record in selection['records']:
        bound(record['source'])
        numeric = json.loads(bound(record['reviewedNumericArtifact']))
        bound(record['originalUnchangedCriterion']['artifact'])
        if record['eligible']:
            assert record['holdCitations']
            for citation in record['holdCitations']:
                bound(citation['artifact'])
                index = int(citation['jsonPointer'].split('/')[-1])
                assert numeric['facets'][index] == citation['exactFacet']
                assert citation['exactFacet']['captureStatus'] == 'NOT OBSERVED'
        else:
            assert record['selectionReason'].startswith('SKIPPED')
    assets = {a['id']: a for a in read(ROOT / 'v97/bundle-manifest-v1.json')['sources']}
    assert len(inventory['attempts']) <= 14
    assert len(list(BASE.glob('*/attempt-v1/attempt-start-v1.json'))) <= 14
    totals, private_ids, session_cache = Counter(), set(), {}
    for ordinal, attempt in enumerate(inventory['attempts']):
        source = attempt['source']
        assert source['sourceId'] == eligible[ordinal]['sourceId']
        asset = assets[source['originalSourceId']]
        executed = bound(source['executed'])
        assert executed == (ROOT / asset['path']).read_bytes() and hashlib.sha256(executed).hexdigest() == asset['sha256']
        assert not re.search(rb'^\s*import\s', executed, re.M)
        assert re.findall(r'plot\([^\n]+?[, ](?:title=)?"([^"]+)"', executed.decode()) == [p['title'] for p in asset['plotColumns']]
        form = bound(source['sourceForm'])
        boundary = form.split(b'\r\n')[0]
        native = form.split(b'\r\n\r\n', 1)[1].split(b'\r\n' + boundary, 1)[0]
        assert native.replace(b'\r\n', b'\n') == executed
        saved = json.loads(bound(source['saveBody']))
        receipt = json.loads(bound(source['receipt']))
        totals.update(nativeSaves=1, compilerBodies=1)
        if not saved['success']:
            assert not attempt['sessions'] and source['addBody'] is None
            totals['nativeRefusals'] += 1
            continue
        meta = saved['result']['metaInfo']
        assert meta['scriptIdPart'] == source['privateScriptId'] not in private_ids
        private_ids.add(source['privateScriptId'])
        assert meta['pine']['version'] == source['privateVersion'] == '1.0'
        added = json.loads(bound(source['addBody']))
        assert added['result']['metaInfo']['scriptIdPart'] == source['privateScriptId']
        totals.update(nativeAdds=1, compilerBodies=1)
        assert receipt['sourceExact'] and receipt['removed']
        assert len(attempt['sessions']) <= 2 and attempt['calendarSelections'] <= 1
        totals['calendarSelections'] += attempt['calendarSelections']
        assert len(receipt['sessions']) == len(attempt['sessions'])
        if len(attempt['sessions']) == 2:
            assert attempt['calendarSelections'] == 1
            directory = (ROOT / source['receipt']['path']).parent
            start, action = read(directory / 'history-navigation-start-v1.json'), read(directory / 'history-navigation-action-v1.json')
            assert start['requestedDate'] == action['requestedDate']
            initial = receipt['sessions'][0]['frontierInspection']
            if initial['observedOwnFirstTimeDateUtc']:
                assert action['requestedDate'] == initial['observedOwnFirstTimeDateUtc']
            assert P['epoch'](receipt['sessions'][0]['completedAtUtc']) <= P['epoch'](start['attemptStartedAtUtc']) <= P['epoch'](action['atUtc']) <= P['epoch'](receipt['sessions'][1]['startedAtUtc'])
        for index, session in enumerate(attempt['sessions']):
            csv_raw = list(csv.reader(bound(session['csv']).decode('utf-8-sig').splitlines()))
            headers, rows = csv_raw[0], csv_raw[1:]
            bindings = json.loads(bound(session['columnBindings']))
            frontier = json.loads(bound(session['frontier']))
            masks = list(csv.DictReader(bound(session['closureMask']).decode().splitlines()))
            assert len(rows) == len(masks) == frontier['dataRows']
            assert [c['originalHeader'] for c in bindings['columns']] == headers
            owned = set()
            for column in bindings['columns']:
                if column['owner'] == source['privateScriptId']:
                    title = column['originalHeader']
                    plot = next(p for p in asset['plotColumns'] if p['title'] == title)
                    assert column['sourceSha256'] == asset['sha256'] and column['privateVersion'] == '1.0'
                    assert column['sourceLiteralPlotOrdinal'] == plot['sourcePlotOrdinal']
                    assert added['result']['metaInfo']['styles'][column['nativePlotId']]['title'] == title
                    owned.add(title)
            download = read((ROOT / session['csv']['path']).parent / 'chart-download-v1.json')
            assert download['sha256'] == session['csv']['sha256']
            assert P['epoch'](download['exportTrigger']['startedAtUtc']) <= download['downloadModifiedAtEpoch'] <= P['epoch'](receipt['sessions'][index]['completedAtUtc'])
            closed, prefix = [], True
            for n, (values, mask) in enumerate(zip(rows, masks), 1):
                row = dict(zip(headers, values))
                own_index, own_time, stamp = P['number'](row.get('INPUT_INDEX')), P['number'](row.get('INPUT_TIME')), P['number'](row['time'])
                context = set(P['FRONTIER']) <= owned and own_index is not None and own_time is not None and own_index.denominator == own_time.denominator == 1 and own_time == stamp * 1000
                eligible_closed = context and stamp + 120 <= P['epoch'](download['exportTrigger']['startedAtUtc']) and row['CHART_CONFIRMED'] == '1'
                assert mask['csv_sha256'] == session['csv']['sha256'] and int(mask['row_ordinal']) == n and mask['time_raw_seconds'] == values[0]
                assert int(mask['closed_numeric_eligible']) == eligible_closed
                assert json.loads(mask['blank_column_ordinals']) == [i for i, v in enumerate(values, 1) if v == '']
                if eligible_closed:
                    closed.append(n)
                prefix = prefix and context and own_index == n - 1 and row['IS_FIRST'] == str(int(n == 1)) and row['FIRST_INDEX'] == '0' and row['FIRST_TIME'] == dict(zip(headers, rows[0]))['FIRST_TIME']
                if n > 1:
                    prefix = prefix and F(values[0]) > F(rows[n - 2][0])
                if source['item'] == 5:
                    prefix = prefix and all(t in owned and P['number'](row[t]) == P['number'](row[k]) for t, k in [('INPUT_OPEN', 'open'), ('INPUT_HIGH', 'high'), ('INPUT_LOW', 'low'), ('INPUT_CLOSE', 'close')])
            first = dict(zip(headers, rows[0]))
            prefix = prefix and P['number'](first['FIRST_TIME']) == F(rows[0][0]) * 1000 and set(range(1, 129)) <= set(closed) and not bindings['missingOrAmbiguousRequestedTitles']
            assert bool(prefix) == session['strictOwnIndexZeroPrefixAvailable'] == frontier['strictOwnIndexZeroPrefixAvailable']
            assert closed == session['eligibleDataRowOrdinals']
            assert session['primaryModelDataRowOrdinals'] == (list(range(1, 129)) if prefix else [])
            assert frontier['physicalFirstRow']['raw'] == rows[0] and frontier['physicalLastRow']['raw'] == rows[-1]
            for edge in ['physicalFirstRow', 'physicalLastRow']:
                for p in frontier[edge]['ownFrontierCells']:
                    if p is not None:
                        assert csv_raw[p['rowOrdinal']][p['columnOrdinal'] - 1] == p['valueRaw']
                        assert headers[p['columnOrdinal'] - 1] == p['headerRaw']
            totals.update(originalCsvs=1, archiveDataRows=len(rows), independentlyClosedArchiveRows=len(closed))
            if index == attempt['selectedFinalSession'] and prefix:
                totals.update(completeOwnPrefixSources=1, primaryOwnClosedRows=128)
            session_cache[session['csv']['path']] = csv_raw
    assert totals['nativeSaves'] <= 14 and totals['nativeAdds'] <= 14 and totals['originalCsvs'] <= 28 and totals['calendarSelections'] <= 14
    expected = runpy.run_path(str(BASE / 'analyze-evidence-v1.py'))['analyze'](revision)
    numeric = read(BASE / f'numeric-controls-v{revision}.json')
    for report, summary in zip(expected['sources'], numeric['sources']):
        actual = json.loads(bound(summary['numericEvidence']))
        assert actual == report
        assert {k: v for k, v in summary.items() if k != 'numericEvidence'} == {k: v for k, v in report.items() if k != 'records'}
        if not report.get('csv'):
            continue
        raw = session_cache[report['csv']['path']]
        def pointer(p):
            assert raw[p['rowOrdinal']][p['columnOrdinal'] - 1] == p['valueRaw']
            assert raw[0][p['columnOrdinal'] - 1] == p['headerRaw']
            totals['rawCellPointerReferences'] += 1
        for record in report['records']:
            pointer(record['nativeCell'])
            assert record['nativeCell']['rowOrdinal'] in report['selectedBlockDataRowOrdinals']
            for p in record.get('inputCells', []) + record.get('dependencyCells', []):
                pointer(p)
            if record.get('completePriorInputBlock'):
                block = record['completePriorInputBlock']
                assert block['csvSha256'] == report['csv']['sha256'] and block['firstDataRowOrdinal'] == 1 and block['lastDataRowOrdinal'] == record['nativeCell']['rowOrdinal']
                for column in block['columns']:
                    assert raw[0][column['columnOrdinal'] - 1] == column['headerRaw']
                totals['completeInputBlockReferences'] += 1
            if record['verdict'] == 'SUPPORTED':
                assert record['nativeCell']['valueRaw'] == '' if record['predictedBlank'] else F(record['nativeCell']['valueRaw']) == F(record['predictedRational'])
            totals['modelRecords'] += 1
            totals['verdict_' + record['verdict']] += 1
        for vector in report.get('nativeVectorPresenceSummary', []):
            if vector['firstFiniteClosedCell'] is not None:
                pointer(vector['firstFiniteClosedCell'])
        for transition in report.get('allClosedDirectionTransitions', []):
            pointer(transition['previous'])
            pointer(transition['current'])
            block = transition['completePriorOhlcInputs']
            assert block['csvSha256'] == report['csv']['sha256'] and block['firstDataRowOrdinal'] == 1 and block['lastDataRowOrdinal'] == transition['current']['rowOrdinal']
            for column in block['columns']:
                assert raw[0][column['columnOrdinal'] - 1] == column['headerRaw']
            totals['observedClosedDirectionTransitions'] += 1
    if require_preservation or inventory['completeFiniteRound']:
        preservation = read(BASE / 'environment-v2/existing-layout-comparison-v1.json')
        assert preservation['allBeforeRecordsUnchanged'] and preservation['allOpenTabSignaturesUnchanged']
        before, after = json.loads(bound(preservation['beforeSavedRecords'])), json.loads(bound(preservation['afterSavedRecords']))
        indexed = {r['id']: r for r in after}
        assert len(before) == 12 and len(after) == 13 and all(indexed[r['id']] == r for r in before)
        assert len(preservation['openTabComparisons']) == 8
        sign = runpy.run_path(str(ROOT / 'v96/captures/v96/validate-evidence-v1.py'))['signature']
        for pair in preservation['openTabComparisons']:
            assert sign(bound(pair['beforeEvidence'])) == sign(bound(pair['afterEvidence'])) == pair['before'] == pair['after']
    if check_integrity:
        for artifact in read(BASE / f'artifact-integrity-v{revision}.json')['files']:
            bound(artifact)
    return {'version': f'v{revision}', 'status': 'PASS', 'returnedSourceSlots': len(inventory['attempts']), 'eligibleSourceSlots': 14, 'completeFiniteRound': inventory['completeFiniteRound'], **dict(totals), 'scope': 'Exact new private native source/admission, original CSV/source/column ownership, closure, single-session own-prefix certificates, frozen startup models and raw pointers. Archive-row counts can include separate frontier overlap; model records and pointer references are not unique cells. No old-frontier reconstruction, precision fitting, live update replay, engine approval or fixture promotion.'}


if __name__ == '__main__':
    revision = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    result = validate(revision)
    assert result == read(BASE / f'validation-result-v{revision}.json')
    print(json.dumps(result, indent=2))
