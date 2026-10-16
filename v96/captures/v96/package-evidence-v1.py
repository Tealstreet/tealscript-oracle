import csv
import hashlib
import io
import json
import re
import sys
from collections import Counter
from datetime import datetime
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent


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


def package(limit=2, revision=1):
    manifest = json.loads((ROOT / 'v96/bundle-manifest-v1.json').read_text())
    creation = json.loads((BASE / 'environment-v1/native-layout-create-response-v1.json').read_text())
    attempts = []
    for asset in manifest['sources'][:limit]:
        directory = BASE / asset['sourceId'] / 'attempt-v1'
        receipt = json.loads((directory / 'capture-receipt-v1.json').read_text())
        original = (ROOT / asset['path']).read_bytes()
        assert (directory / 'executed-v1.pine').read_bytes() == original
        assert hashlib.sha256(original).hexdigest() == asset['sha256']
        assert not re.search(rb'^\s*import\s', original, re.M)
        saved = json.loads((directory / 'save-response-v1.json').read_text())
        meta = (saved.get('result') or {}).get('metaInfo', {})
        observation = {'version': 'v1', 'sourceId': asset['sourceId'], 'sourceSha256': asset['sha256'], 'pineVersion': asset['pineVersion'], 'requestSource': asset['path'], 'executed': ref(directory / 'executed-v1.pine'), 'sourceForm': ref(directory / 'save-request-v1.txt'), 'saveBody': ref(directory / 'save-response-v1.json'), 'addBody': ref(directory / 'add-response-v1.json') if (directory / 'add-response-v1.json').exists() else None, 'nativeCompileSuccess': saved.get('success'), 'privateScriptId': meta.get('scriptIdPart'), 'privateVersion': meta.get('pine', {}).get('version'), 'nativeStudyInstanceId': None, 'nativeStudyInstanceStatus': 'UNOBSERVED', 'editorMarkerArrays': None, 'editorMarkerStatus': 'UNOBSERVED; separate immediate/settled native UI retained', 'nativeWarningChannel': meta.get('warnings'), 'nativeWarningChannelStatus': 'EXPOSED' if 'warnings' in meta else 'UNOBSERVED', 'nativeLayoutId': creation['id'], 'nativeLayoutImage': creation['image_url'], 'settings': manifest['context'], 'receipt': ref(directory / 'capture-receipt-v1.json')}
        put(directory / 'observation-v1.json', observation)
        sessions = []
        for session in sorted(directory.glob('session-*-v1')):
            path = session / 'chart-native-v1.csv'
            if not path.exists():
                continue
            raw = list(csv.reader(path.read_bytes().decode('utf-8-sig').splitlines()))
            headers, data = raw[0], raw[1:]
            native = json.loads((directory / 'add-response-v1.json').read_text())['result']['metaInfo']
            requested = {p['title']: p['sourcePlotOrdinal'] for p in asset['plots']}
            plot_defs = {p['id']: p for p in native.get('plots', [])}
            columns = []
            for ordinal, title in enumerate(headers, 1):
                item = {'columnOrdinal': ordinal, 'originalHeader': title}
                if ordinal <= 5:
                    assert title == ['time', 'open', 'high', 'low', 'close'][ordinal - 1]
                    item.update(owner='Native main chart', bindingStatus='OBSERVED')
                elif title == 'Volume' and title not in requested:
                    item.update(owner='Native builtin Vol · BTC', bindingStatus='OBSERVED')
                else:
                    matches = [pid for pid, style in native['styles'].items() if style.get('title') == title]
                    if len(matches) == 1 and headers.count(title) == 1 and title in requested:
                        item.update(owner=native['scriptIdPart'], privateVersion='1.0', sourceSha256=asset['sha256'], nativePlotId=matches[0], sourceLiteralPlotOrdinal=requested[title], bindingStatus='OBSERVED')
                    elif title in plot_defs and plot_defs[title].get('type') == 'colorer':
                        item.update(owner=native['scriptIdPart'], privateVersion='1.0', sourceSha256=asset['sha256'], nativePlotId=title, bindingStatus='OBSERVED / NATIVE COLORER', rawEncoding='UNINTERPRETED; no packed-format/byte decoding or invented palette values')
                    else:
                        item.update(owner=None, bindingStatus='UNOBSERVED / ownership unresolved', candidateNativePlotIds=matches)
                columns.append(item)
            present = {p['originalHeader'] for p in columns if p.get('owner') == native['scriptIdPart'] and p.get('sourceLiteralPlotOrdinal') is not None}
            bindings = {'version': 'v1', 'csv': ref(path), 'sourceId': asset['sourceId'], 'sourceSha256': asset['sha256'], 'nativePrivateId': native['scriptIdPart'], 'nativePrivateVersion': '1.0', 'nativeMetaInfoId': native['id'], 'columns': columns, 'missingOrAmbiguousRequestedPlotTitles': [p for p in requested if p not in present], 'unresolvedColumnOrdinals': [p['columnOrdinal'] for p in columns if p['bindingStatus'].startswith('UNOBSERVED')], 'nativeExposedPlotMetadata': native.get('plots'), 'nativeColorerDefinitions': [p for p in native.get('plots', []) if p.get('type') == 'colorer'], 'actuallyExportedColorerColumns': [p for p in columns if p['bindingStatus'] == 'OBSERVED / NATIVE COLORER'], 'absentColorerPolicy': 'A native colorer definition never creates an absent CSV value', 'inputSession': 'One unchanged default source/settings session; no input variants', 'ownershipBasis': 'Exact source/form transport and private version, native metadata, own-study native UI and fresh download clocks; title equality alone is insufficient'}
            put(session / 'column-bindings-v1.json', bindings)
            download = json.loads((session / 'chart-download-v1.json').read_text())
            clock = download['exportTrigger']['startedAtUtc']
            assert download['sha256'] == bindings['csv']['sha256']
            assert epoch(clock) <= download['downloadModifiedAtEpoch'] <= epoch(receipt['completedAtUtc'])
            output = io.StringIO(newline='')
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow(['csv_sha256', 'row_ordinal', 'time_raw_seconds', 'input_time_raw_ms', 'input_index_raw', 'native_confirmed_raw', 'export_utc', 'physical_close_epoch', 'closed_numeric_eligible', 'present_cell_status', 'blank_column_ordinals', 'exclusion_cause'])
            eligible, selected, run, gaps = [], [], [], []
            prior = None
            for n, values in enumerate(data, 1):
                assert len(values) == len(headers)
                row = dict(zip(headers, values))
                own_time, own_index = number(row.get('INPUT_TIME')), number(row.get('INPUT_INDEX'))
                context = own_time is not None and own_index is not None and own_time.denominator == own_index.denominator == 1 and own_time == F(values[0]) * 1000 and all(t in present for t in ['INPUT_TIME', 'INPUT_INDEX', 'CHART_CONFIRMED'])
                close = F(values[0]) + 120
                closed = context and close <= epoch(clock) and number(row.get('CHART_CONFIRMED')) == 1
                cause = '' if closed else 'SOURCE_EXECUTION_CONTEXT_UNAVAILABLE' if not context else 'PHYSICALLY_OPEN_OR_NATIVE_CONFIRMATION_NOT_REACHED'
                writer.writerow([bindings['csv']['sha256'], n, values[0], row.get('INPUT_TIME'), row.get('INPUT_INDEX'), row.get('CHART_CONFIRMED'), clock, str(close), int(closed), 'OBSERVED' if closed else 'OBSERVED / EXCLUDED', json.dumps([i for i, value in enumerate(values, 1) if value == ''], separators=(',', ':')), cause])
                if closed:
                    eligible.append(n)
                    if run and (n != run[-1] + 1 or own_index != number(data[run[-1] - 1][headers.index('INPUT_INDEX')]) + 1):
                        run = []
                    run.append(n)
                    if len(run) == 32 and not selected:
                        selected = list(run)
                else:
                    run = []
                if prior is not None and F(values[0]) != F(prior[0]) + 120:
                    gaps.append({'priorRowOrdinal': n - 1, 'rowOrdinal': n, 'priorTimeRaw': prior[0], 'timeRaw': values[0]})
                prior = values
            mask = session / 'row-closure-mask-v1.csv'
            if mask.exists():
                assert mask.read_text() == output.getvalue()
            else:
                mask.write_text(output.getvalue())
            result = {'version': 'v1', 'sourceId': asset['sourceId'], 'csv': bindings['csv'], 'columnBindings': ref(session / 'column-bindings-v1.json'), 'closureMask': ref(mask), 'dataRows': len(data), 'columnCount': len(headers), 'independentlyClosedRows': len(eligible), 'eligibleDataRowOrdinals': eligible, 'selectedFirst32ConsecutiveClosedRows': selected, 'requiredRowCriterion': 'CAPTURED' if len(selected) == 32 else 'NOT OBSERVED / insufficient consecutive source-bound closed rows', 'selectionRule': 'First32 eligible rows in original row/index order; no output presence, NA or equality-result filtering', 'nativeExportUtc': clock, 'timeUnits': {'nativeCsv': 'UNIX seconds', 'INPUT_TIME': 'UNIX milliseconds'}, 'timestampGaps': gaps, 'rawFirstRow': data[0], 'rawLastRow': data[-1], 'ownOriginRequired': False, 'samplingCompleteness': False}
            put(session / 'row-set-observation-v1.json', result)
            sessions.append(result)
        attempts.append({'source': observation, 'status': receipt['status'], 'removed': receipt.get('removed'), 'sessions': sessions})
    result = {'version': f'v{revision}', 'requestCommit': 'b0c64e9ba8c291325aa5773acaac335c248df4a3', 'capturedSourceSlots': len(attempts), 'maximumSavesAddsCsvsSessions': 2, 'sourceRetries': 0, 'inputVariants': 0, 'attempts': attempts}
    put(BASE / f'attempt-inventory-v{revision}.json', result)
    return result


if __name__ == '__main__':
    result = package(int(sys.argv[1]) if len(sys.argv) > 1 else 2, int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    print(json.dumps({'sourceSlots': len(result['attempts']), 'originalCsvs': sum(len(a['sessions']) for a in result['attempts'])}))
