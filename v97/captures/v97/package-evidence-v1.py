import csv
import hashlib
import io
import json
from datetime import datetime
from fractions import Fraction as F
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
FRONTIER = ['INPUT_INDEX', 'INPUT_TIME', 'CHART_CONFIRMED', 'IS_FIRST', 'FIRST_INDEX', 'FIRST_TIME']


def ref(path):
    raw = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def put(path, value):
    text = json.dumps(value, indent=2) + '\n'
    if path.exists():
        assert path.read_text() == text, str(path)
    else:
        path.write_text(text)


def number(value):
    try:
        return F(value)
    except (ValueError, TypeError, ZeroDivisionError):
        return None


def epoch(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()


def package_session(asset, source, directory):
    path = directory / 'chart-native-v1.csv'
    raw = list(csv.reader(path.open(newline='')))
    headers, data = raw[0], raw[1:]
    csv_ref = ref(path)
    attempt_dir = directory.parent
    meta = json.loads((attempt_dir / 'add-response-v1.json').read_text())['result']['metaInfo']
    titles = {p['title']: p['sourcePlotOrdinal'] for p in asset['plotColumns']}
    columns = []
    for i, title in enumerate(headers, 1):
        column = {'columnOrdinal': i, 'originalHeader': title}
        if i <= 5:
            assert title == ['time', 'open', 'high', 'low', 'close'][i - 1]
            column.update(owner='Native main chart', bindingStatus='OBSERVED')
        elif title == 'Volume':
            column.update(owner='Native builtin Vol · BTC', bindingStatus='OBSERVED')
        else:
            matches = [pid for pid, style in meta['styles'].items() if style.get('title') == title]
            if title in titles and headers.count(title) == 1 and len(matches) == 1:
                column.update(owner=source['privateScriptId'], privateVersion=source['privateVersion'], sourceSha256=asset['sha256'], nativePlotId=matches[0], sourceLiteralPlotOrdinal=titles[title], bindingStatus='OBSERVED')
            else:
                column.update(owner=None, bindingStatus='UNOBSERVED / ambiguous or absent source ownership', candidateNativePlotIds=matches)
        columns.append(column)
    owned = {c['originalHeader'] for c in columns if c['owner'] == source['privateScriptId']}
    bindings = {'version': 'v1', 'csv': csv_ref, 'sourceId': source['sourceId'], 'originalSourceId': asset['id'], 'sourceSha256': asset['sha256'], 'privateId': source['privateScriptId'], 'privateVersion': source['privateVersion'], 'nativeMetaInfoId': meta['id'], 'columns': columns, 'missingOrAmbiguousRequestedTitles': sorted(set(titles) - owned), 'nativePlotDefinitions': meta.get('plots'), 'nativeColorerPolicy': 'Native metadata alone does not create an exported value; no hidden decoding', 'ownershipBasis': 'Exact request/executed/form SHA, new private source/version, complete native compiler metadata, own-study UI and original download chronology; titles alone are insufficient'}
    put(directory / 'column-bindings-v1.json', bindings)
    download = json.loads((directory / 'chart-download-v1.json').read_text())
    clock = epoch(download['exportTrigger']['startedAtUtc'])
    mask_io = io.StringIO(newline='')
    mask = csv.writer(mask_io, lineterminator='\n')
    mask.writerow(['csv_sha256', 'row_ordinal', 'time_raw_seconds', 'input_time_raw_ms', 'input_index_raw', 'native_confirmed_raw', 'export_utc', 'physical_close_epoch', 'closed_numeric_eligible', 'present_cell_status', 'blank_column_ordinals', 'exclusion_cause'])
    parsed, closed, index_errors, time_errors, market_gaps, origin_errors, ohlc_errors = [], [], [], [], [], [], []
    prior = None
    for n, values in enumerate(data, 1):
        assert len(values) == len(headers)
        row = dict(zip(headers, values))
        own_index, own_time, stamp = number(row.get('INPUT_INDEX')), number(row.get('INPUT_TIME')), number(row['time'])
        context = set(FRONTIER) <= owned and own_index is not None and own_time is not None and stamp is not None and own_index.denominator == own_time.denominator == 1 and own_time == stamp * 1000
        eligible = context and stamp + 120 <= clock and number(row.get('CHART_CONFIRMED')) == 1
        cause = '' if eligible else 'OWN_SOURCE_EXECUTION_CONTEXT_UNAVAILABLE' if not context else 'PHYSICALLY_OPEN_OR_NATIVE_CONFIRMATION_UNMET'
        mask.writerow([csv_ref['sha256'], n, values[0], row.get('INPUT_TIME'), row.get('INPUT_INDEX'), row.get('CHART_CONFIRMED'), download['exportTrigger']['startedAtUtc'], str(stamp + 120) if stamp is not None else '', int(eligible), 'OBSERVED' if eligible else 'OBSERVED / EXCLUDED', json.dumps([i for i, v in enumerate(values, 1) if v == ''], separators=(',', ':')), cause])
        if eligible:
            closed.append(n)
        parsed.append({'rowOrdinal': n, 'inputIndex': own_index, 'time': stamp, 'row': row, 'context': context})
        if own_index is None or own_index.denominator != 1 or own_index != n - 1:
            index_errors.append({'rowOrdinal': n, 'inputIndexRaw': row.get('INPUT_INDEX'), 'expectedOwnPrefixIndex': n - 1})
        if not context or row.get('IS_FIRST') != str(int(n == 1)) or row.get('FIRST_INDEX') != '0' or row.get('FIRST_TIME') != dict(zip(headers, data[0])).get('FIRST_TIME'):
            origin_errors.append(n)
        if prior is not None and stamp is not None and prior['time'] is not None:
            if stamp <= prior['time']:
                time_errors.append({'priorRowOrdinal': n - 1, 'rowOrdinal': n, 'priorTimeRaw': str(prior['time']), 'timeRaw': values[0]})
            if stamp != prior['time'] + 120:
                market_gaps.append({'priorRowOrdinal': n - 1, 'rowOrdinal': n, 'priorTimeRaw': str(prior['time']), 'timeRaw': values[0]})
        if asset['v95Item'] == 5:
            for own, chart in [('INPUT_OPEN', 'open'), ('INPUT_HIGH', 'high'), ('INPUT_LOW', 'low'), ('INPUT_CLOSE', 'close')]:
                if own not in owned or number(row.get(own)) is None or number(row.get(own)) != number(row.get(chart)):
                    ohlc_errors.append({'rowOrdinal': n, 'own': own, 'ownRaw': row.get(own), 'chart': chart, 'chartRaw': row.get(chart)})
        prior = parsed[-1]
    mask_path = directory / 'row-closure-mask-v1.csv'
    if mask_path.exists():
        assert mask_path.read_text() == mask_io.getvalue()
    else:
        mask_path.write_text(mask_io.getvalue())

    def pointer(n, title):
        if headers.count(title) != 1:
            return None
        col = headers.index(title)
        return {'rowOrdinal': n, 'columnOrdinal': col + 1, 'headerRaw': title, 'valueRaw': data[n - 1][col]}

    first, last = parsed[0], parsed[-1]
    closed_set = set(closed)
    extent = -1
    for n, item in enumerate(parsed, 1):
        if item['inputIndex'] != n - 1 or n not in closed_set:
            break
        extent = n - 1
    origin_equal = number(first['row'].get('FIRST_TIME')) == first['time'] * 1000 if first['time'] is not None else False
    complete = not (index_errors or time_errors or origin_errors or ohlc_errors or bindings['missingOrAmbiguousRequestedTitles']) and origin_equal and extent >= 127 and last['inputIndex'] is not None and last['inputIndex'] + 1 == len(data)
    frontier = {'version': 'v1', 'sourceId': source['sourceId'], 'originalSourceId': asset['id'], 'sourceSha256': asset['sha256'], 'privateId': source['privateScriptId'], 'privateVersion': source['privateVersion'], 'csv': csv_ref, 'columnBindings': ref(directory / 'column-bindings-v1.json'), 'closureMask': ref(mask_path), 'dataRows': len(data), 'physicalFirstRow': {'rowOrdinal': 1, 'raw': data[0], 'ownFrontierCells': [pointer(1, t) for t in FRONTIER]}, 'physicalLastRow': {'rowOrdinal': len(data), 'raw': data[-1], 'ownFrontierCells': [pointer(len(data), t) for t in FRONTIER]}, 'minimumInputIndex': str(min(p['inputIndex'] for p in parsed if p['inputIndex'] is not None)) if any(p['inputIndex'] is not None for p in parsed) else None, 'maximumInputIndex': str(max(p['inputIndex'] for p in parsed if p['inputIndex'] is not None)) if any(p['inputIndex'] is not None for p in parsed) else None, 'ownPrefixIndexGapsOrDuplicates': index_errors, 'nonIncreasingOrDuplicateTimes': time_errors, 'actualMarketTimestampGaps': market_gaps, 'originContextViolationRowOrdinals': origin_errors, 'item5OwnOhlcDisagreements': ohlc_errors, 'closedOwnPrefixLastIndex': extent, 'strictOwnIndexZeroPrefixAvailable': complete, 'prefixCriterion': 'CAPTURED / COMPLETE_OWN_INDEX_ZERO_PREFIX' if complete else 'NOT OBSERVED / OWN_INDEX_ZERO_PREFIX_NOT_EXPORTED', 'prefixFailureCauses': ([] if complete else [name for name, bad in [('OWN_INDEX_SEQUENCE_UNMET', bool(index_errors)), ('OWN_TIME_ORDER_UNMET', bool(time_errors)), ('OWN_ORIGIN_CONTEXT_UNMET', bool(origin_errors) or not origin_equal), ('OWN_OHLC_BINDING_UNMET', bool(ohlc_errors)), ('SOURCE_PLOT_OWNERSHIP_UNAVAILABLE', bool(bindings['missingOrAmbiguousRequestedTitles'])), ('FEWER_THAN_128_CLOSED_OWN_PREFIX_ROWS', extent < 127)] if bad]), 'independentlyClosedRows': len(closed), 'eligibleDataRowOrdinals': closed, 'primaryModelOwnIndices': [0, 127], 'primaryModelDataRowOrdinals': list(range(1, 129)) if complete else [], 'timeUnits': {'nativeCsv': 'UNIX seconds', 'INPUT_TIME': 'UNIX milliseconds'}, 'nativeExportUtc': download['exportTrigger']['startedAtUtc'], 'noCrossSessionStitching': True, 'scope': 'One exact-source original CSV only. Own origin and complete dependency-index order are independently required; real market time gaps are archived without synthesizing rows. Every later raw row is retained; no original v95 or live frontier is reconstructed.'}
    put(directory / 'source-frontier-v1.json', frontier)
    return {'sessionDirectory': str(directory.relative_to(ROOT)), 'csv': csv_ref, 'columnBindings': frontier['columnBindings'], 'closureMask': frontier['closureMask'], 'frontier': ref(directory / 'source-frontier-v1.json'), **{k: frontier[k] for k in ['dataRows', 'independentlyClosedRows', 'eligibleDataRowOrdinals', 'strictOwnIndexZeroPrefixAvailable', 'primaryModelDataRowOrdinals', 'prefixCriterion', 'prefixFailureCauses']}}


def package(limit, revision):
    manifest = json.loads((ROOT / 'v97/bundle-manifest-v1.json').read_text())
    assets = {a['id']: a for a in manifest['sources']}
    selection = json.loads((BASE / 'selection-inventory-v1.json').read_text())
    chosen = [r for r in selection['records'] if r['eligible']]
    attempts = []
    for selected in chosen[:limit]:
        asset = assets[selected['originalSourceId']]
        directory = BASE / selected['sourceId'] / 'attempt-v1'
        receipt_path = directory / 'capture-receipt-v1.json'
        receipt = json.loads(receipt_path.read_text())
        saved_path = directory / 'save-response-v1.json'
        saved = json.loads(saved_path.read_text())
        meta = (saved.get('result') or {}).get('metaInfo', {})
        assert (directory / 'executed-v1.pine').read_bytes() == (ROOT / asset['path']).read_bytes()
        source = {'sourceId': selected['sourceId'], 'originalSourceId': asset['id'], 'item': asset['v95Item'], 'pineVersion': asset['pineVersion'], 'requestSource': selected['source'], 'sourceSha256': asset['sha256'], 'executed': ref(directory / 'executed-v1.pine'), 'sourceForm': ref(directory / 'save-request-v1.txt'), 'saveBody': ref(saved_path), 'addBody': ref(directory / 'add-response-v1.json') if (directory / 'add-response-v1.json').exists() else None, 'nativeCompileSuccess': saved.get('success'), 'privateScriptId': meta.get('scriptIdPart'), 'privateVersion': meta.get('pine', {}).get('version'), 'nativeStudyInstanceId': None, 'nativeStudyInstanceStatus': 'UNOBSERVED', 'receipt': ref(receipt_path)}
        put(directory / 'observation-v1.json', source)
        sessions = [package_session(asset, source, directory / ('session-' + r['frontier'] + '-v1')) for r in receipt.get('sessions', [])]
        attempts.append({'source': source, 'status': receipt['status'], 'removed': receipt.get('removed'), 'calendarSelections': receipt.get('calendarSelections', 0), 'sessions': sessions, 'selectedFinalSession': len(sessions) - 1 if sessions else None})
    inventory = {'version': f'v{revision}', 'requestCommit': selection['requestCommit'], 'selection': ref(BASE / 'selection-inventory-v1.json'), 'eligibleSourceSlots': 14, 'capturedSourceSlots': len(attempts), 'completeFiniteRound': len(attempts) == 14, 'sourceRetries': 0, 'inputVariants': 0, 'attempts': attempts}
    put(BASE / f'attempt-inventory-v{revision}.json', inventory)
    return inventory
