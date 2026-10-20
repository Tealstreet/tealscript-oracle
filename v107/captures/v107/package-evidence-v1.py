import csv
import hashlib
import io
import json
import sys
from datetime import datetime
from fractions import Fraction as F
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]


def ref(path):
    raw = path.read_bytes()
    return dict(path=str(path.relative_to(ROOT)), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def put(path, value):
    content = json.dumps(value, indent=2) + '\n'
    if path.exists():
        assert path.read_text() == content, str(path)
    else:
        path.write_text(content)


def number(raw):
    try:
        return F(raw)
    except (ValueError, TypeError, ZeroDivisionError):
        return None


def epoch(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()


def package(limit=4, revision=1):
    manifest = json.loads((ROOT / 'v107/bundle-manifest-v1.json').read_text())
    creation = json.loads((BASE / 'environment-v1/native-layout-create-response-v1.json').read_text())
    attempts = []
    for asset in manifest['entries'][:limit]:
        directory = BASE / asset['sourceId'] / 'attempt-v1'
        receipt_path = directory / 'capture-receipt-v1.json'
        receipt = json.loads(receipt_path.read_text())
        requested = (ROOT / asset['path']).read_bytes()
        assert len(requested) == asset['bytes'] and hashlib.sha256(requested).hexdigest() == asset['sha256']
        if receipt.get('save') is None:
            stop_path=directory/'source-entry-stop-v1.json'
            stop=json.loads(stop_path.read_text())
            source=dict(version='v1',sourceId=asset['sourceId'],slotId=asset['slotId'],sourceSha256=asset['sha256'],pineVersion=asset['pineVersion'],requested=ref(ROOT/asset['path']),executed=None,sourceForm=None,saveBody=None,addBody=None,nativeCompileSuccess=None,privateScriptId=None,privateVersion=None,nativeLayoutId=creation['id'],nativeLayoutImage=creation['image_url'],receipt=ref(receipt_path),editorMarkerArrays=None,editorMarkerStatus='UNOBSERVED; no native compiler attempt',settings='BINANCE:BTCUSDT2m Candles Etc/UTC; one new-layout editor-entry attempt',sourceSpecificExecutionId=None,sourceSpecificExecutionIdStatus='UNOBSERVED; no Save/Add',sourceEntryStop=ref(stop_path),partialEnteredUiText=[ref(directory/r['enteredUiText']) for r in stop['nativeUiTextSnapshots']],nativePartialEntrySnapshots=[ref(directory/r['nativeSnapshot']) for r in stop['nativeUiTextSnapshots']],admissionStatus='NOT OBSERVED; incomplete native entry consumed its slot before Save/Add')
            put(directory/'observation-v1.json',source)
            attempts.append(dict(source=source,status=receipt['status'],removed=False,sessions=[]))
            continue
        verification=json.loads((directory/'full-editor-ranges-verification-v1.json').read_text())
        assert verification['exact'] is True and verification['beforeSave'] is True
        assert (directory/'full-editor-ranges-assembled-v1.pine').read_bytes()==requested
        executed = directory / 'executed-v1.pine'
        assert executed.read_bytes() == requested
        save_path = directory / 'save-response-v1.json'
        saved = json.loads(save_path.read_text())
        meta = (saved.get('result') or {}).get('metaInfo', {})
        add_path = directory / 'add-response-v1.json'
        source = dict(version='v1', sourceId=asset['sourceId'], slotId=asset['slotId'], sourceSha256=asset['sha256'], pineVersion=asset['pineVersion'], requested=ref(ROOT / asset['path']), executed=ref(executed), sourceForm=ref(directory / 'save-request-v1.txt'), saveBody=ref(save_path), addBody=ref(add_path) if add_path.exists() else None, nativeCompileSuccess=saved.get('success'), privateScriptId=meta.get('scriptIdPart'), privateVersion=meta.get('pine', {}).get('version'), nativeLayoutId=creation['id'], nativeLayoutImage=creation['image_url'], receipt=ref(receipt_path), editorMarkerArrays=None, editorMarkerStatus='UNOBSERVED; separate native immediate/settled UI retained', settings='BINANCE:BTCUSDT2m Candles Etc/UTC; one unchanged new-layout session', sourceSpecificExecutionId=None, sourceSpecificExecutionIdStatus='UNOBSERVED')
        source.update(fullEditorUi=ref(directory/'full-editor-ranges-assembled-v1.pine'),fullEditorVerification=ref(directory/'full-editor-ranges-verification-v1.json'),fullEditorSnapshots=[ref(directory/r['nativeSnapshot']) for r in verification['rangeSnapshots']],fullEditorRangeClock=ref(directory/'full-editor-range-clock-v1.json'))
        put(directory / 'observation-v1.json', source)
        sessions = []
        for session_dir in sorted(directory.glob('session-*-v1')):
            path = session_dir / 'chart-native-v1.csv'
            if not path.exists():
                continue
            raw = list(csv.reader(path.read_bytes().decode('utf-8-sig').splitlines()))
            headers, data = raw[0], raw[1:]
            native = json.loads(add_path.read_text())['result']['metaInfo']
            requested_titles = {p['title']:p['sourcePlotOrdinal'] for p in asset['plots']}
            columns = []
            for ordinal, title in enumerate(headers, 1):
                item = dict(columnOrdinal=ordinal, originalHeader=title)
                matches = [pid for pid, style in native['styles'].items() if style.get('title') == title]
                if ordinal <= 5:
                    assert title == ['time', 'open', 'high', 'low', 'close'][ordinal - 1]
                    item.update(owner='Native main chart', bindingStatus='OBSERVED')
                elif title == 'Volume' and title not in requested_titles:
                    item.update(owner='Native builtin Vol · BTC', bindingStatus='OBSERVED')
                elif len(matches) == 1 and headers.count(title) == 1 and title in requested_titles:
                    item.update(owner=native['scriptIdPart'], privateVersion='1.0', sourceSha256=asset['sha256'], nativePlotId=matches[0], sourceLiteralPlotOrdinal=requested_titles[title], bindingStatus='OBSERVED')
                else:
                    item.update(owner=None, bindingStatus='OBSERVED / original non-requested or unresolved column', candidateNativePlotIds=matches)
                columns.append(item)
            owned = {c['originalHeader'] for c in columns if c.get('sourceLiteralPlotOrdinal') is not None}
            bindings = dict(version='v1', csv=ref(path), sourceId=asset['sourceId'], slotId=asset['slotId'], sourceSha256=asset['sha256'], nativePrivateId=native['scriptIdPart'], nativePrivateVersion='1.0', columns=columns, missingOrAmbiguousRequestedPlotTitles=[t for t in requested_titles if t not in owned], exposedNativePlotMetadata=native.get('plots'), exposedNativeStyles=native.get('styles'), scope='Unique requested title plus exact source/form/private version, native Add plot metadata, native own-study UI and fresh original download clock; title alone never establishes ownership. Other original columns retain their own ordinals with no requested-plot credit.')
            put(session_dir / 'column-bindings-v1.json', bindings)
            download = json.loads((session_dir / 'chart-download-v1.json').read_text())
            clock = download['exportTrigger']['startedAtUtc']
            assert download['sha256'] == bindings['csv']['sha256'] and epoch(clock) <= download['downloadModifiedAtEpoch'] <= epoch(receipt['completedAtUtc'])
            runtime = (directory / 'runtime-ui-observation-v1.json').exists()
            masks, closed, eligible, anchors, marker_rows = [], [], [], [], []
            for n, values in enumerate(data, 1):
                assert len(values) == len(headers)
                row = dict(zip(headers, values))
                time, index, phase = number(row.get('INPUT_TIME')), number(row.get('INPUT_INDEX')), number(row.get('CASE_ID'))
                context = time is not None and index is not None and index.denominator == time.denominator == 1 and time == number(row['time']) * 1000 and {'INPUT_INDEX','INPUT_TIME','CHART_CONFIRMED'} <= owned
                physical = context and not runtime and number(row['time']) + 120 <= epoch(clock) and number(row.get('CHART_CONFIRMED')) == 1
                phase_ok = phase is not None and phase.denominator == 1 and index is not None and phase == index % 8 and 'CASE_ID' in owned
                if physical:
                    closed.append(n)
                if physical and phase_ok and index >= 200:
                    eligible.append(n)
                anchor_time, anchor_index = number(row.get('VISUAL_ANCHOR_TIME')), number(row.get('VISUAL_ANCHOR_INDEX'))
                if row.get('VISUAL_ANCHOR_TIME','')!='' or row.get('VISUAL_ANCHOR_INDEX','')!='':marker_rows.append(n)
                if physical and index >= 240 and {'VISUAL_ANCHOR_TIME','VISUAL_ANCHOR_INDEX'} <= owned and anchor_time == time and anchor_index == index:
                    anchors.append(n)
                masks.append(dict(csv_sha256=bindings['csv']['sha256'], row_ordinal=n, time_raw_seconds=row['time'], input_time_raw_ms=row.get('INPUT_TIME'), input_index_raw=row.get('INPUT_INDEX'), case_id_raw=row.get('CASE_ID'), native_confirmed_raw=row.get('CHART_CONFIRMED'), export_utc=clock, physical_close_epoch=str(number(row['time']) + 120), independently_closed=int(physical), valid_phase_clock=int(phase_ok), eligible_minimum_index=int(physical and phase_ok and index >= 200), blank_column_ordinals=json.dumps([i for i,v in enumerate(values,1) if v==''],separators=(',',':'))))
            anchor = anchors[0] if len(anchors) == len(marker_rows) == 1 else None
            selected, predecessors = [], []
            if anchor is not None:
                block=list(range(anchor-31,anchor+1));prefix=list(range(anchor-39,anchor-31))
                if all(n in eligible for n in block) and all(n in closed for n in prefix):
                    combined=prefix+block
                    indices=[number(data[n-1][headers.index('INPUT_INDEX')]) for n in combined]
                    times=[number(data[n-1][0]) for n in combined]
                    if all(b==a+1 for a,b in zip(indices,indices[1:])) and all(b>a for a,b in zip(times,times[1:])):
                        selected,predecessors=block,prefix
            complete = len(selected) == 32
            for mask in masks:
                n = mask['row_ordinal']
                primary = complete and n in selected
                cause = '' if primary else 'RUNTIME_FAILURE_NO_NUMERIC_OR_NA_CREDIT' if runtime else 'PHYSICALLY_OPEN_OR_SOURCE_CONFIRMATION_CONTEXT_UNAVAILABLE' if not mask['independently_closed'] else 'INVALID_PHASE_CLOCK' if not mask['valid_phase_clock'] else 'BELOW_MINIMUM_SOURCE_INDEX' if not mask['eligible_minimum_index'] else 'VISUAL_ANCHOR_ROW' if n in anchors else 'RESERVED_ORIGINAL_CLOSED_PREDECESSOR' if n in predecessors else 'MISSING_UNIQUE_CLOSED_VISUAL_ANCHOR' if anchor is None else 'OUTSIDE_FIXED_PRIMARY_BLOCK'
                mask.update(primary_scoring_eligible=int(primary), present_cell_status='OBSERVED' if primary else 'OBSERVED / EXCLUDED', primary_exclusion_cause=cause)
            output = io.StringIO(newline='')
            writer = csv.DictWriter(output, fieldnames=list(masks[0]), lineterminator='\n')
            writer.writeheader(); writer.writerows(masks)
            mask_path = session_dir / 'row-closure-mask-v1.csv'
            if mask_path.exists():
                assert mask_path.read_text() == output.getvalue()
            else:
                mask_path.write_text(output.getvalue())
            session = dict(version='v1', sourceId=asset['sourceId'], csv=bindings['csv'], columnBindings=ref(session_dir / 'column-bindings-v1.json'), closureMask=ref(mask_path), dataRows=len(data), columnCount=len(headers), independentlyClosedRows=len(closed), independentlyClosedRowOrdinals=closed, eligibleClosedSourceRows=eligible, selectedPrimaryClosedRowOrdinals=selected, originalClosedPredecessorRowOrdinals=predecessors, uniqueVisualAnchorRowOrdinal=anchor, visualAnchorCandidates=anchors, allExposedMarkerRowOrdinals=marker_rows, primaryInputCertificateValid=complete, requiredPrimaryRows=32, requiredOriginalClosedPredecessors=8, nativeExportUtc=clock, runtimeFailed=runtime, renderPng=ref(session_dir / 'render-v1.png') if (session_dir / 'render-v1.png').exists() else None, sessionReceipt=ref(session_dir / 'session-receipt-v1.json'), selection='Fixed32 owned physically closed indices A-31..A inclusive at the unique one-time retained build anchor A>=240, plus8 original closed predecessors A-39..A-32. Four rotated phase cycles, increasing real timestamps and consecutive own indices; no output filter, origin claim, forced120-second continuity or history action.')
            put(session_dir / 'row-set-observation-v1.json', session)
            sessions.append(session)
        attempts.append(dict(source=source, status=receipt['status'], removed=receipt.get('removed',False), sessions=sessions))
    result = dict(version=f'v{revision}', requestCommit='35d3d1914b2a397d961e35968725c198450aea00', consumedSourceSlots=len(attempts), maximumSourceSlots=4, sourceRetries=0, inputVariants=0, settingsChanges=0, attempts=attempts)
    put(BASE / f'attempt-inventory-v{revision}.json', result)
    return result


if __name__ == '__main__':
    result = package(int(sys.argv[1]) if len(sys.argv)>1 else 4, int(sys.argv[2]) if len(sys.argv)>2 else 1)
    print(json.dumps(dict(consumedSourceSlots=len(result['attempts']), originalCSVs=sum(len(a['sessions']) for a in result['attempts']))))
