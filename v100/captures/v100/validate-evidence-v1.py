import csv
import hashlib
import json
import re
import runpy
import sys
from collections import Counter
from datetime import datetime
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def bound(ref):
    b = (ROOT / ref['path']).read_bytes()
    assert len(b) == ref['bytes'] and hashlib.sha256(b).hexdigest() == ref['sha256'], ref['path']
    return b


def signature(text):
    return dict(url=re.search(r'url="([^"]+)"',text)[1],canvas=re.findall(r'Canvas "([^"]+)"',text),checkedRadios=re.findall(r'radio "([^"]+)" checked',text),activeLayout=re.findall(r'button "Logged in as [^"]+ Active layout: ([^"]+)"',text))


def validate(revision=1, integrity=True, preservation=None):
    manifest=read(ROOT/'v100/bundle-manifest-v1.json')
    inventory=read(BASE/f'attempt-inventory-v{revision}.json')
    numeric=read(BASE/f'numeric-controls-v{revision}.json')
    assets={a['sourceId']:a for a in manifest['sources']}
    if preservation is None:preservation=len(inventory['attempts'])==3
    attempts=list(BASE.glob('*/attempt-v1/attempt-start-v1.json'))
    assert len(assets)==3 and len(attempts)<=3
    assert {p.parent.parent.name for p in attempts}<=set(assets)
    assert not list(BASE.glob('**/history-navigation-action*.json'))
    counts=Counter()
    private=set()
    cache={}
    for attempt in inventory['attempts']:
        source=attempt['source'];a=assets[source['sourceId']]
        if source['saveBody'] is None:
            requested=bound(source['requested']);assert len(requested)==a['bytes'] and hashlib.sha256(requested).hexdigest()==a['sha256']
            receipt=json.loads(bound(source['receipt']));assert receipt['save'] is None and receipt['add'] is None and not receipt['studyAdded']
            assert source['nativeCompileSuccess'] is None and source['executed'] is None and source['addBody'] is None and not attempt['sessions']
            assert not list((ROOT/source['receipt']['path']).parent.glob('*-response-v1.json'))
            counts['nativeSourceEntryStops']+=1
            continue
        requested=(ROOT/a['path']).read_bytes();executed=bound(source['executed'])
        assert requested==executed and len(requested)==a['bytes'] and hashlib.sha256(requested).hexdigest()==a['sha256']==source['sourceSha256']
        assert not re.search(rb'^\s*import\s',executed,re.M)
        titles=re.findall(r'\bplot\([^\n]*title="([^"]+)"',executed.decode())
        assert len(titles)==a['plotCalls']==len(set(titles)) and titles==[p['title'] for p in a['plots']]
        form=bound(source['sourceForm']);sep=b'\r\n' if b'\r\n' in form else b'\n';boundary=form.split(sep)[0]
        native=form.split(sep+sep,1)[1].split(sep+boundary,1)[0]
        assert native.replace(b'\r\n',b'\n')==executed
        receipt=json.loads(bound(source['receipt']));save=json.loads(bound(source['saveBody']))
        assert receipt['sourceExact'] and save['success']==source['nativeCompileSuccess']
        counts.update(nativeSaves=1,compilerBodies=1)
        if not save['success']:
            assert source['addBody'] is None and not attempt['sessions']
            counts['nativeRefusals']+=1
            continue
        meta=save['result']['metaInfo'];script=meta['scriptIdPart']
        assert script==source['privateScriptId'] and script not in private and meta['pine']['version']=='1.0'
        private.add(script)
        added=json.loads(bound(source['addBody']));counts.update(nativeAdds=1,compilerBodies=1)
        if not added['success']:
            assert not attempt['sessions'];counts['nativeRefusals']+=1
            continue
        assert added['result']['metaInfo']['scriptIdPart']==script
        assert len(receipt['sessions'])==len(attempt['sessions'])<=1
        if not attempt['sessions']:
            assert any(w in receipt['status'].upper() for w in ['FAIL','UNAVAILABLE','STOP','PARTIAL','HOLD'])
            counts['nativeValueExportHolds']+=1
            continue
        assert receipt['removed']
        for session in attempt['sessions']:
            raw=list(csv.reader(bound(session['csv']).decode('utf-8-sig').splitlines()))
            headers,rows=raw[0],raw[1:];cache[session['csv']['sha256']]=raw
            bindings=json.loads(bound(session['columnBindings']))
            assert [p['originalHeader'] for p in bindings['columns']]==headers
            owned=set()
            for c in bindings['columns']:
                if c.get('sourceLiteralPlotOrdinal') is not None:
                    ordinal=c['sourceLiteralPlotOrdinal'];title=a['plots'][ordinal]['title']
                    assert c['originalHeader']==title and c['owner']==script and c['sourceSha256']==a['sha256'] and c['privateVersion']=='1.0'
                    assert added['result']['metaInfo']['styles'][c['nativePlotId']]['title']==title
                    assert headers.count(title)==1
                    owned.add(title)
            assert set(bindings['missingOrAmbiguousRequestedPlotTitles'])==set(titles)-owned
            assert not bindings['actuallyExportedColorerColumns'] and not bindings['nativeColorerDefinitions']
            download=read((ROOT/session['csv']['path']).parent/'chart-download-v1.json')
            clock=datetime.fromisoformat(download['exportTrigger']['startedAtUtc'].replace('Z','+00:00')).timestamp()
            end=datetime.fromisoformat(receipt['completedAtUtc'].replace('Z','+00:00')).timestamp()
            assert download['sha256']==session['csv']['sha256'] and clock<=download['downloadModifiedAtEpoch']<=end
            masks=list(csv.DictReader(bound(session['closureMask']).decode().splitlines()))
            assert len(rows)==len(masks)==session['dataRows']
            closed=[]
            for n,(row,mask) in enumerate(zip(rows,masks),1):
                assert len(row)==len(headers)
                v=dict(zip(headers,row))
                context=all(t in owned and v[t] for t in ['INPUT_INDEX','INPUT_TIME','CHART_CONFIRMED'])
                if context:
                    context=F(v['INPUT_INDEX']).denominator==1 and F(v['INPUT_TIME'])==1000*F(v['time'])
                eligible=context and not session['runtimeFailed'] and F(v['time'])+120<=clock and F(v['CHART_CONFIRMED'])==1
                assert int(mask['row_ordinal'])==n and mask['csv_sha256']==session['csv']['sha256']
                assert bool(int(mask['closed_numeric_eligible']))==bool(eligible)
                assert mask['time_raw_seconds']==v['time'] and mask['input_time_raw_ms']==v.get('INPUT_TIME')
                assert json.loads(mask['blank_column_ordinals'])==[i for i,x in enumerate(row,1) if x=='']
                if eligible:closed.append(n)
            assert closed==session['eligibleDataRowOrdinals'] and len(closed)==session['independentlyClosedRows']
            selected=[];closed_set=set(closed)
            for start in closed:
                if a.get('phaseModulo') is not None and ('CASE_ID' not in owned or F(rows[start-1][headers.index('CASE_ID')])!=0):continue
                block=list(range(start,start+a['minimumPrimaryClosedRows']))
                if not all(n in closed_set for n in block):continue
                indices=[F(rows[n-1][headers.index('INPUT_INDEX')]) for n in block]
                times=[F(rows[n-1][0]) for n in block]
                if any(b!=a0+1 for a0,b in zip(indices,indices[1:])) or any(b<=a0 for a0,b in zip(times,times[1:])):continue
                if a.get('requiresOriginalClosedPredecessor') and (start-1 not in closed_set or F(rows[start-2][headers.index('INPUT_INDEX')])+1!=indices[0] or F(rows[start-2][0])>=times[0]):continue
                selected=block;break
            phase_clock=not a.get('phaseModulo') or bool(selected) and all(F(rows[n-1][headers.index('CASE_ID')])==F(rows[n-1][headers.index('INPUT_INDEX')])%a['phaseModulo'] for n in selected)
            complete=len(selected)==a['minimumPrimaryClosedRows'] and phase_clock
            assert session['phaseClockValidated']==phase_clock and session['primaryInputCertificateValid']==complete
            for n,mask in enumerate(masks,1):
                primary=complete and n in selected
                assert int(mask['primary_scoring_eligible'])==primary
                assert mask['present_cell_status']==('OBSERVED' if primary else 'OBSERVED / EXCLUDED')
                assert primary or mask['primary_exclusion_cause']
            assert selected==session['selectedPrimaryConsecutiveClosedRows']
            assert session['historyPredecessorDataRowOrdinal']==(selected[0]-1 if selected and a.get('requiresOriginalClosedPredecessor') else None)
            if selected and a.get('phaseModulo') is not None:
                phases=Counter(int(F(rows[n-1][headers.index('CASE_ID')])) for n in selected)
                assert phases==Counter({i:a['minimumPrimaryClosedRows']//a['phaseModulo'] for i in range(a['phaseModulo'])})
            counts.update(csvs=1,dataRows=len(rows),independentlyClosedRows=len(closed),primaryRows=len(selected) if complete else 0,uniquePrimaryPlotCells=len(selected)*len(owned) if complete else 0,uniquePrimaryColorCells=len(selected)*len(owned-set(['INPUT_INDEX','INPUT_TIME','CHART_CONFIRMED','CASE_ID'])) if complete else 0)
    assert counts['nativeSaves']<=3 and counts['nativeAdds']<=3 and counts['csvs']<=3
    fresh=runpy.run_path(str(BASE/'analyze-evidence-v1.py'))['analyze'](revision)
    assert fresh==numeric
    assert runpy.run_path(str(BASE/'audit-predictions-v1.py'))['audit']()==read(BASE/'prediction-membership-audit-v1.json')
    counts['signatureClasses']=sum(len(scope['classes']) for report in numeric['sources'] for scope in report['scopes'])
    counts['scopedRepresentatives']=sum(len(record['modelIds']) for report in numeric['sources'] for scope in report['scopes'] for record in scope['classes'])
    mapping=read(ROOT/'v100/predictions/prediction-map-v1.json')
    for report in numeric['sources']:
        block=json.loads(bound(report['nativeBlock']))
        if 'csv' in block:
            raw=cache[block['csv']['sha256']]
            masks={int(row['row_ordinal']):row for row in csv.DictReader(bound(block['closureMask']).decode().splitlines())}
            for row in block['rows']:
                n=row['rowOrdinal'];assert masks[n]['closed_numeric_eligible']=='1'
                for p in row['inputCells']+list(row['cells'].values()):
                    if p is None:continue
                    assert p['csvSha256']==block['csv']['sha256'] and raw[p['rowOrdinal']][p['columnOrdinal']-1]==p['valueRaw'] and raw[0][p['columnOrdinal']-1]==p['headerRaw']
                    counts['rawNativePointerReferences']+=1
        for scope in report['scopes']:
            family=scope['family'];spec=mapping[family]
            for class_index,record in enumerate(scope['classes']):
                frozen=spec['classes'][class_index]
                assert record['classId']==frozen['classId'] and record['modelIds']==frozen['modelIds']
                assert record['testedColumns']==spec['columnTitles'] and record['nativeTargets']['artifact']==report['nativeBlock']
                assert len(record['comparisonRows'])==len(block['rows'])
                expected_rows={r['CASE_ID']:r['expected'] for r in frozen.get('rows',[])}
                for i,(matrix,row) in enumerate(zip(record['comparisonRows'],block['rows'])):
                    assert matrix['rowOrdinal']==row['rowOrdinal'] and matrix['nativeBlockRowPointer']=='/rows/'+str(i)
                    for j,title in enumerate(spec['columnTitles']):
                        actual=row['cells'].get(title)
                        if family in ['scalar','packing']:expected=frozen['expectedCodes'][j]
                        elif row['phaseInputValid'] and row['phaseValue'] in expected_rows:expected=expected_rows[row['phaseValue']][title]
                        else:
                            options={r[title] for r in expected_rows.values()};expected=next(iter(options)) if len(options)==1 else None
                        if actual is None or title not in block['ownedColumns'] or expected is None:code='U'
                        else:
                            try:matches=F(actual['valueRaw'])==F(expected)
                            except (ValueError,ZeroDivisionError):matches=False
                            code='S' if matches else 'R'
                        assert matrix['cellVerdicts'][j]==code
                        counts['classCellComparisons']+=1
                counts[record['verdict']]+=1
    if preservation:
        old=read(BASE/'environment-v1/native-layout-list-before-response-v1.json');new=read(BASE/'environment-v2/native-layout-list-after-response-v1.json')
        indexed={r['id']:r for r in new};creation=read(BASE/'environment-v1/native-layout-create-response-v1.json')
        assert len(old)==15 and len(new)==16
        comparison=read(BASE/'environment-v2/existing-layout-comparison-v1.json')
        saved_equal=[r==indexed.get(r['id']) for r in old]
        assert [r['equal'] for r in comparison['savedRecordComparisons']]==saved_equal
        tab_equal=[]
        assert indexed[creation['id']]['image_url']==creation['image_url'] and creation['id'] not in {r['id'] for r in old}
        for page in range(1,12):
            before=BASE/f'environment-v1/page-{page}-before-v1.txt'
            after=BASE/f'environment-v2/page-{page}-after-v1.txt'
            tab_equal.append(signature(before.read_text())==signature(after.read_text()))
        assert [r['equal'] for r in comparison['openTabComparisons']]==tab_equal
        counts.update(oldSavedRecordsUnchanged=sum(saved_equal),oldSavedRecordsChanged=sum(not x for x in saved_equal),oldOpenTabsUnchanged=sum(tab_equal),oldOpenTabsChanged=sum(not x for x in tab_equal))
    if integrity:
        refs=read(BASE/f'artifact-integrity-v{revision}.json')['artifacts']
        assert len({r['path'] for r in refs})==len(refs)
        for ref in refs:bound(ref)
        counts['integrityBoundFiles']=len(refs)
    return dict(version=f'v{revision}',status='PASS',counts=dict(counts),policy='Read-only validation; independent selection/closure/binding/preservation and recomputed frozen-model analysis. Pointer records are not unique plot cells.')


if __name__=='__main__':
    print(json.dumps(validate(int(sys.argv[1]) if len(sys.argv)>1 else 1),indent=2))
