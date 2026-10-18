import csv
import hashlib
import json
import re
import runpy
import struct
import sys
from collections import Counter
from datetime import datetime
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]


def read(path):
    return json.loads(path.read_text())


def bound(reference):
    raw=(ROOT/reference['path']).read_bytes()
    assert len(raw)==reference['bytes'] and hashlib.sha256(raw).hexdigest()==reference['sha256'],reference['path']
    return raw


def num(raw):
    try:return Fraction(raw)
    except (ValueError,TypeError,ZeroDivisionError):return None


def clock(value):
    return datetime.fromisoformat(value.replace('Z','+00:00')).timestamp()


def editor_ranges(directory,proof_path,requested):
    proof=read(proof_path);expected=requested.decode();covered={};starts=[0]
    for line in expected.split('\n')[:-1]:starts.append(starts[-1]+len(line)+1)
    assert proof['exact'] and proof['sourceRepairOrRetry'] is False and proof['beforeSave'] is True
    assert proof['requestedSourceSha256']==hashlib.sha256(requested).hexdigest() and proof['sourceId']==directory.parent.name
    last_line=1
    for record in proof['rangeSnapshots']:
        raw=(directory/record['nativeUiText']).read_text();snapshot=(directory/record['nativeSnapshot']).read_text()
        exposed=re.search(r'roledescription="editor" value="([\s\S]*?)"\n\s+uid=',snapshot)
        assert exposed and exposed[1]==raw
        assert record['selectionColumns']==[1,1] and record['uniqueExactRequestedRange'] is True
        a,z=record['exposedCharacterRange'];start,end=record['selectionCharacterRange']
        assert a<=start<end<=z and expected[a:z]==raw
        assert record['selectionStartLine']==last_line and starts[last_line-1]==start
        last_line=record['selectionEndLine'];assert starts[last_line-1]==end
        assert f'button "Line {last_line}, Col 1"' in snapshot
        for offset,char in enumerate(raw,a):
            assert offset not in covered or covered[offset]==char
            covered[offset]=char
    assert last_line==len(expected.split('\n')) and set(covered)==set(range(len(expected)))
    assert ''.join(covered[i] for i in range(len(expected)))==expected


def validate(revision=1,integrity=True,preservation=None):
    manifest=read(ROOT/'v104/bundle-manifest-v1.json');assets={a['sourceId']:a for a in manifest['entries']}
    assert runpy.run_path(str(BASE/'audit-request-v1.py'))['audit']()==read(BASE/'environment-v1/request-audit-v1.json')
    contracts=read(BASE/'numeric-contracts-v1.json');assert runpy.run_path(str(BASE/'build-contracts-v1.py'))['build']()==contracts
    inventory=read(BASE/f'attempt-inventory-v{revision}.json');numeric=read(BASE/f'numeric-controls-v{revision}.json')
    if preservation is None:preservation=len(inventory['attempts'])==13
    starts=list(BASE.glob('*/attempt-v1/attempt-start-v1.json'));assert len(inventory['attempts'])<=len(starts)<=13
    assert len({p.parent.parent.name for p in starts})==len(starts) and {p.parent.parent.name for p in starts}<=set(assets)
    counts=Counter();private=set();csv_cache={}
    for attempt,entry in zip(inventory['attempts'],numeric['sources']):
        source=attempt['source'];asset=assets[source['sourceId']];requested=bound(source['requested']);directory=(ROOT/source['receipt']['path']).parent
        assert len(requested)==asset['bytes'] and hashlib.sha256(requested).hexdigest()==asset['sha256']==source['sourceSha256']
        receipt=json.loads(bound(source['receipt']));counts['consumedSourceSlots']+=1
        counts['returnedFiniteVisualFacets']+=len(asset['visualFacets'])
        if not (BASE/source['sourceId']/'derived-region-map-v1.json').exists():counts['visualFacet_UNDECIDED']+=len(asset['visualFacets'])
        if source['saveBody'] is None:
            stop=json.loads(bound(source['sourceEntryStop']));assert receipt['save'] is None and receipt['add'] is None and not receipt['studyAdded'] and not attempt['sessions']
            assert stop['nativeSaves']==stop['nativeAdds']==stop['originalCsvs']==stop['nativeRenderingPngs']==stop['retries']==0
            for snap_ref,text_ref in zip(source['nativePartialEntrySnapshots'],source['partialEnteredUiText']):
                exposed=re.search(r'roledescription="editor" value="([\s\S]*?)"\n\s+uid=',bound(snap_ref).decode());assert exposed and exposed[1].encode()==bound(text_ref)
            if stop.get('diagnosticFullEditorRanges'):
                editor_ranges(directory,directory/stop['diagnosticFullEditorRanges'],requested)
                assert (directory/stop['diagnosticFullEnteredUiText']).read_bytes()==requested
            assert not list(directory.glob('save-response*.json')) and not list(directory.glob('add-response*.json'))
            counts['nativeEntryStops']+=1
        else:
            assert bound(source['executed'])==bound(source['fullEditorUi'])==requested
            editor_ranges(directory,ROOT/source['fullEditorVerification']['path'],requested)
            saved=json.loads(bound(source['saveBody']));counts.update(nativeSaves=1,compilerBodies=1)
            form=bound(source['sourceForm']);sep=b'\r\n' if b'\r\n' in form else b'\n';boundary=form.split(sep)[0]
            assert b'name="source"' in form.split(sep+sep)[0]
            assert form.split(sep+sep,1)[1].split(sep+boundary,1)[0].replace(b'\r\n',b'\n')==requested
            assert clock(json.loads(bound(source['fullEditorRangeClock']))['completedBeforeSaveAtUtc'])<=clock(receipt['save']['observedAtUtc'])
            assert saved['success']==source['nativeCompileSuccess'] and receipt['sourceExact']
            if not saved['success']:
                assert not attempt['sessions'] and source['addBody'] is None;counts['nativeSaveRefusals']+=1
            else:
                script=saved['result']['metaInfo']['scriptIdPart'];assert script==source['privateScriptId'] and script not in private;private.add(script)
                assert source['privateVersion']=='1.0' and source['addBody'] is not None
                added=json.loads(bound(source['addBody']));assert added['result']['metaInfo']['scriptIdPart']==script;counts.update(nativeAdds=1,compilerBodies=1)
                if not added['success']:assert not attempt['sessions'];counts['nativeAddRefusals']+=1
                else:assert attempt['removed'] and receipt['removed'] and len(attempt['sessions'])==len(receipt['sessions'])==1
        for session in attempt['sessions']:
            raw=list(csv.reader(bound(session['csv']).decode('utf-8-sig').splitlines()));headers,rows=raw[0],raw[1:];csv_cache[session['csv']['sha256']]=raw
            bindings=json.loads(bound(session['columnBindings']));assert [c['originalHeader'] for c in bindings['columns']]==headers
            meta=json.loads(bound(source['addBody']))['result']['metaInfo'];owned=set()
            for column in bindings['columns']:
                if column.get('sourceLiteralPlotOrdinal') is None:continue
                p=asset['plots'][column['sourceLiteralPlotOrdinal']];assert column['originalHeader']==p['title'] and headers.count(p['title'])==1
                assert column['owner']==source['privateScriptId'] and column['sourceSha256']==asset['sha256'] and meta['styles'][column['nativePlotId']]['title']==p['title']
                owned.add(p['title'])
            assert set(bindings['missingOrAmbiguousRequestedPlotTitles'])=={p['title'] for p in asset['plots']}-owned
            download=read((ROOT/session['csv']['path']).parent/'chart-download-v1.json');export=clock(download['exportTrigger']['startedAtUtc'])
            assert export<=download['downloadModifiedAtEpoch']<=clock(receipt['completedAtUtc']) and download['sha256']==session['csv']['sha256']
            masks=list(csv.DictReader(bound(session['closureMask']).decode().splitlines()));assert len(masks)==len(rows)==session['dataRows']
            closed=[];eligible=[];anchors=[];markers=[];indices={}
            for n,(values,mask) in enumerate(zip(rows,masks),1):
                assert len(values)==len(headers);r=dict(zip(headers,values));idx=num(r.get('INPUT_INDEX'));time=num(r.get('INPUT_TIME'));phase=num(r.get('CASE_ID'))
                context=idx is not None and time is not None and idx.denominator==time.denominator==1 and time==1000*num(r['time']) and {'INPUT_INDEX','INPUT_TIME','CHART_CONFIRMED'}<=owned
                physical=context and not session['runtimeFailed'] and num(r['time'])+120<=export and num(r.get('CHART_CONFIRMED'))==1
                phase_ok=phase is not None and phase.denominator==1 and idx is not None and phase==idx%8 and 'CASE_ID' in owned
                if physical:closed.append(n)
                if physical and phase_ok and idx>=200:eligible.append(n);indices.setdefault(int(idx),[]).append(n)
                if r.get('VISUAL_ANCHOR_TIME','')!='' or r.get('VISUAL_ANCHOR_INDEX','')!='':markers.append(n)
                if physical and idx>=240 and {'VISUAL_ANCHOR_TIME','VISUAL_ANCHOR_INDEX'}<=owned and num(r.get('VISUAL_ANCHOR_TIME'))==time and num(r.get('VISUAL_ANCHOR_INDEX'))==idx:anchors.append(n)
                assert mask['csv_sha256']==session['csv']['sha256'] and int(mask['row_ordinal'])==n
                assert int(mask['independently_closed'])==bool(physical) and int(mask['valid_phase_clock'])==bool(phase_ok)
                assert json.loads(mask['blank_column_ordinals'])==[i for i,v in enumerate(values,1) if v=='']
            anchor=anchors[0] if len(anchors)==len(markers)==1 else None;selected=[];prefix=[]
            if anchor is not None:
                a=int(num(rows[anchor-1][headers.index('INPUT_INDEX')]));desired=list(range(a-39,a+1))
                if all(len(indices.get(i,[]))==1 for i in desired):
                    ordered=[indices[i][0] for i in desired];times=[num(rows[n-1][0]) for n in ordered]
                    if all(v>u for u,v in zip(times,times[1:])):prefix=ordered[:8];selected=ordered[8:]
            assert selected==session['selectedPrimaryClosedRowOrdinals'] and prefix==session['originalClosedPredecessorRowOrdinals']
            assert anchor==session['uniqueVisualAnchorRowOrdinal'] and closed==session['independentlyClosedRowOrdinals'] and eligible==session['eligibleClosedSourceRows']
            assert bool(selected)==session['primaryInputCertificateValid']
            for n,mask in enumerate(masks,1):assert bool(int(mask['primary_scoring_eligible']))==(n in selected)
            if selected:assert len(selected)==32 and len(prefix)==8 and Counter(int(num(rows[n-1][headers.index('CASE_ID')])) for n in selected)==Counter({i:4 for i in range(8)})
            png=bound(session['renderPng']);assert png[:8]==b'\x89PNG\r\n\x1a\n'
            counts.update(originalCSVs=1,archiveRows=len(rows),independentlyClosedRows=len(closed),primaryRows=len(selected),originalPredecessorRows=len(prefix),nativeRenderingPNGs=1,uniquePrimaryPlotCells=len(selected)*len(owned))
            visual_path=BASE/source['sourceId']/'derived-region-map-v1.json'
            if visual_path.exists():
                visual=read(visual_path);assert runpy.run_path(str(BASE/'build-region-map-v1.py'))['build'](source['sourceId'])==visual
                assert visual['originalPng']==session['renderPng'] and visual['originalCsv']==session['csv'] and visual['nativePrivateId']==source['privateScriptId']
                assert visual['originalDimensionsPx']==dict(zip(['width','height'],struct.unpack('>II',png[16:24])))
                assert [f['facetId'] for f in visual['facets']]==[f['facetId'] for f in asset['visualFacets']]
                counts.update({'visualFacet_'+f['verdict']:sum(g['verdict']==f['verdict'] for g in visual['facets']) for f in visual['facets']})
                pixel_path=BASE/source['sourceId']/'pixel-certificate-v1.json'
                if pixel_path.exists():
                    certificate=read(pixel_path)
                    assert runpy.run_path(str(BASE/'build-pixel-certificate-v1.py'))['build'](source['sourceId'])==certificate
                    assert visual['pixelCertificate']==dict(path=str(pixel_path.relative_to(ROOT)),bytes=pixel_path.stat().st_size,sha256=hashlib.sha256(pixel_path.read_bytes()).hexdigest())
                    assert certificate['privateScriptId']==source['privateScriptId'] and certificate['originalPng']==session['renderPng'] and certificate['originalCsv']==session['csv']
                    for patch in certificate['patches']:
                        assert len(patch['samples'])==25 and len({(p['xPx'],p['yPx']) for p in patch['samples']})==25
                    counts['pixelCertificates']+=1
                counts['derivedRegionMaps']+=1
        report=json.loads(bound(entry['report']));block=json.loads(bound(report['nativeBlock']));assert report['sourceObservation']==source and report['sourceSha256']==asset['sha256']
        frozen=next(c for c in contracts['sources'] if c['sourceId']==source['sourceId'])
        assert block['sourceSha256']==source['sourceSha256'] and block['nativePrivateId']==source['privateScriptId'] and block['nativePrivateVersion']==source['privateVersion']
        if attempt['sessions']:
            session=attempt['sessions'][0];raw=csv_cache[session['csv']['sha256']]
            binding=json.loads(bound(session['columnBindings']));block_owned={c['originalHeader'] for c in binding['columns'] if c.get('sourceLiteralPlotOrdinal') is not None and c['bindingStatus']=='OBSERVED' and c['owner']==source['privateScriptId']}
            assert block['primaryCertificate']==session['primaryInputCertificateValid'] and set(block['ownedTitles'])==block_owned
            assert [r['rowOrdinal'] for r in block['rows']]==session['selectedPrimaryClosedRowOrdinals']
            assert [r['rowOrdinal'] for r in block['predecessors']]==session['originalClosedPredecessorRowOrdinals']
            assert json.loads(bound(block['rowSet']))==session
            assert (block['visualAnchor']['rowOrdinal'] if block['visualAnchor'] else None)==session['uniqueVisualAnchorRowOrdinal']
            records=block['rows']+block['predecessors']+([block['visualAnchor']] if block['visualAnchor'] else [])
            for record in records:
                assert set(record['cells'])=={p['title'] for p in asset['plots']}
                assert record['chartTime']['rowOrdinal']==record['rowOrdinal'] and record['chartTime']['columnOrdinal']==1 and record['chartTime']['valueRaw']==raw[record['rowOrdinal']][0]
                for title,point in record['cells'].items():
                    if point is None:assert raw[0].count(title)!=1;continue
                    assert point['rowOrdinal']==record['rowOrdinal'] and point['csvSha256']==session['csv']['sha256'] and raw[0][point['columnOrdinal']-1]==title and raw[record['rowOrdinal']][point['columnOrdinal']-1]==point['valueRaw']
            assert report['uniquePrimaryPlotCells']==block['primaryScoringCells']==len(block['rows'])*len(block_owned)
        else:
            assert block['rows']==block['predecessors']==block['ownedTitles']==[] and block['visualAnchor'] is None and block['primaryCertificate'] is False and block['primaryScoringCells']==report['uniquePrimaryPlotCells']==0
        assert len(report['properties'])==len(frozen['contracts'])
        for prop,contract in zip(report['properties'],frozen['contracts']):
            assert prop['frozenContract']==contract and prop['title']==contract['title']
            assert len(prop['comparisonRows'])==len(block['rows']);codes=[]
            for comparison,row in zip(prop['comparisonRows'],block['rows']):
                actual=comparison['actual'];title=prop['title']
                if actual is not None:
                    raw=csv_cache[actual['csvSha256']];assert raw[actual['rowOrdinal']][actual['columnOrdinal']-1]==actual['valueRaw'] and raw[0][actual['columnOrdinal']-1]==actual['headerRaw']
                independent=None
                if actual is not None:
                    original=csv_cache[actual['csvSha256']];record=dict(zip(original[0],original[actual['rowOrdinal']]))
                    own=num(record['INPUT_INDEX']);phase=int(own%8);rule=contract['rule']
                    a=num(block['visualAnchor']['cells']['INPUT_INDEX']['valueRaw']) if block['visualAnchor'] else None
                    if rule=='BUILD_EVENT':independent=contract['prediction'] if own==a else ''
                    elif rule=='BUILD_EVENT_UNSPECIFIED':independent=None if own==a else ''
                    elif rule=='BUILD_DELTA_MOD32':independent=str(-((int(a)-contract['prediction'])%32)) if own==a else ''
                    elif rule=='CONSTANT':independent=contract['prediction']
                    elif rule in ['PHASE_FORMULA','OFFSET_POLICY']:independent=contract['prediction'][phase]
                    elif rule in ['MOD32_FORMULA','BOOLEAN_EXPORT_POLICY']:independent=contract['prediction'][int(own%32)]
                    elif rule=='UNIQUE_BUILD_MARKER':independent=str(a) if own==a and title=='VISUAL_ANCHOR_INDEX' else record['INPUT_TIME'] if own==a else ''
                    elif title=='CASE_ID':independent=str(phase)
                    elif title=='INPUT_TIME':independent=str(num(record['time'])*1000)
                    elif title=='CHART_CONFIRMED':independent='1'
                assert comparison['expectedRaw']==independent
                value=comparison['expectedRaw'];code='U' if actual is None or title not in block['ownedTitles'] else 'S' if title=='INPUT_INDEX' and block['primaryCertificate'] else 'U' if value is None else 'S' if (actual['valueRaw']=='' if value=='' else num(actual['valueRaw'])==num(value)) else 'R'
                assert code==comparison['comparison'];codes.append(code);counts['rawPrimaryPointers']+=actual is not None
            expected_status='REFUTED' if 'R' in codes else 'SUPPORTED' if block['primaryCertificate'] and len(codes)==32 and set(codes)=={'S'} else 'UNDECIDED'
            assert prop['verdict']==expected_status
            if contract['rule'] in ['BUILD_EVENT','BUILD_EVENT_UNSPECIFIED','BUILD_DELTA_MOD32']:assert prop['buildEventObservations']==(1 if block['primaryCertificate'] and prop['title'] in block['ownedTitles'] else 0)
            counts['numericProperty_'+prop['verdict']]+=1
        for family in report['numericAlternatives']:
            contract=next(c for c in frozen['contracts'] if c['title']==family['title'])
            assert contract['rule']=='BOOLEAN_EXPORT_POLICY'
            assert [v['id'] for v in family['variants']]==['SOURCE_BOOL','VISIBLE_SPARSE']
            for variant in family['variants']:
                values=contract['prediction'] if variant['id']=='SOURCE_BOOL' else contract['alternativeSparse'];codes=[]
                assert len(variant['comparisons'])==len(block['rows'])
                for comparison,row in zip(variant['comparisons'],block['rows']):
                    actual=row['cells'].get(family['title']);own=num(row['cells']['INPUT_INDEX']['valueRaw']);prediction=values[int(own%32)]
                    assert comparison['actual']==actual and comparison['expectedRaw']==prediction and comparison['rowOrdinal']==row['rowOrdinal']
                    code='U' if actual is None or family['title'] not in block['ownedTitles'] else 'S' if (actual['valueRaw']=='' if prediction=='' else num(actual['valueRaw'])==num(prediction)) else 'R'
                    assert comparison['comparison']==code;codes.append(code)
                expected_status='REFUTED' if 'R' in codes else 'SUPPORTED' if block['primaryCertificate'] and len(codes)==32 and set(codes)=={'S'} else 'UNDECIDED'
                assert variant['verdict']==expected_status
            assert family['supportedVariantIds']==[v['id'] for v in family['variants'] if v['verdict']=='SUPPORTED']
    assert counts['uniquePrimaryPlotCells']==numeric['uniquePrimaryPlotCells']<=4608
    assert all(counts[k]<=13 for k in ['nativeSaves','nativeAdds','originalCSVs','nativeRenderingPNGs','consumedSourceSlots'])
    if preservation:
        comparison=read(BASE/'environment-v2/existing-layout-comparison-v1.json')
        old=read(BASE/'environment-v1/native-layout-list-before-response-v1.json');new=read(BASE/'environment-v2/native-layout-list-after-response-v1.json');indexed={r['id']:r for r in new};creation=read(BASE/'environment-v1/native-layout-create-response-v1.json')
        assert len(old)==19 and len(new)==20 and creation['id'] not in {r['id'] for r in old}
        assert indexed[creation['id']]['image_url']==creation['image_url']
        assert [r==indexed.get(r['id']) for r in old]==[r['equal'] for r in comparison['savedRecordComparisons']]
        def signature(text):return dict(url=re.search(r'url="([^"]+)"',text)[1],canvas=re.findall(r'Canvas "([^"]+)"',text),checkedRadios=re.findall(r'radio "([^"]+)" checked',text),activeLayout=re.findall(r'button "Logged in as [^"]+ Active layout: ([^"]+)"',text))
        equal=[signature((BASE/f'environment-v1/page-{p}-before-v1.txt').read_text())==signature((BASE/f'environment-v2/page-{p}-after-v1.txt').read_text()) for p in range(1,16)]
        assert equal==[r['equal'] for r in comparison['openTabComparisons']]
        assert len(comparison['savedRecordComparisons'])==19 and len(comparison['openTabComparisons'])==15
        counts.update(oldSavedRecordsUnchanged=sum(r['equal'] for r in comparison['savedRecordComparisons']),oldOpenTabsUnchanged=sum(r['equal'] for r in comparison['openTabComparisons']))
    if integrity:
        references=read(BASE/f'artifact-integrity-v{revision}.json')['artifacts'];assert len({r['path'] for r in references})==len(references)
        for reference in references:bound(reference)
        counts['integrityBoundFiles']=len(references)
    return dict(version=f'v{revision}',status='PASS',counts=dict(counts),policy='Independent exact-source/full-editor/native-form/private/column/raw-pointer/physical-closure/anchor-index32+8 selection checks; original snapshots and frozen pixel windows bound; one build event never multiplied to32 getters')


if __name__=='__main__':print(json.dumps(validate(int(sys.argv[1])),indent=2))
