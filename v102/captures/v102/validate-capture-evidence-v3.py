import csv
import hashlib
import json
import re
import runpy
import struct
import subprocess
import sys
from collections import Counter
from datetime import datetime
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]


def read(path):return json.loads(path.read_text())


def bound(reference):
    path=ROOT/reference['path']
    raw=path.read_bytes() if path.exists() else subprocess.check_output(['git','cat-file','blob','HEAD:'+reference['path']],cwd=ROOT)
    assert len(raw)==reference['bytes'] and hashlib.sha256(raw).hexdigest()==reference['sha256'],reference['path']
    return raw


def number(raw):
    try:return F(raw)
    except (TypeError,ValueError,ZeroDivisionError):return None


def signature(text):
    return dict(url=re.search(r'url="([^"]+)"',text)[1],canvas=re.findall(r'Canvas "([^"]+)"',text),checkedRadios=re.findall(r'radio "([^"]+)" checked',text),activeLayout=re.findall(r'button "Logged in as [^"]+ Active layout: ([^"]+)"',text))


def validate(revision=1,integrity=True,preservation=None):
    manifest=read(ROOT/'v102/bundle-manifest-v1.json');assets={a['sourceId']:a for a in manifest['sources']}
    inventory=read(BASE/f'attempt-inventory-v{revision}.json');numeric=read(BASE/f'numeric-controls-v{revision}.json')
    if preservation is None:preservation=len(inventory['attempts'])==25
    starts=list(BASE.glob('*/attempt-v1/attempt-start-v1.json'))
    assert len(inventory['attempts'])<=len(starts)<=25 and {p.parent.parent.name for p in starts}<=set(assets)
    assert not list(BASE.glob('**/history-navigation-action*.json'))
    assert runpy.run_path(str(BASE/'audit-request-v1.py'))['audit']()==read(BASE/'environment-v1/request-audit-v1.json')
    contracts=read(BASE/'numeric-contracts-v1.json')
    assert runpy.run_path(str(BASE/'build-contracts-v1.py'))['build']()==contracts
    counts=Counter();private=set();cache={};owned_by_sha={};sessions_by_source={}
    for attempt in inventory['attempts']:
        source=attempt['source'];asset=assets[source['sourceId']]
        requested=bound(source['requested'])
        if source['executed'] is None:
            assert len(requested)==asset['bytes'] and hashlib.sha256(requested).hexdigest()==asset['sha256']==source['sourceSha256']
            receipt=json.loads(bound(source['receipt']));stop=json.loads(bound(source['sourceEntryStop']))
            assert receipt['save'] is None and receipt['add'] is None and not receipt['studyAdded'] and not attempt['sessions']
            assert source['saveBody'] is None and source['addBody'] is None and source['privateScriptId'] is None and source['nativeCompileSuccess'] is None
            assert stop['nativeSaves']==stop['nativeAdds']==stop['originalCsvs']==stop['nativeRenderingPngs']==stop['retries']==0
            for snapshot_ref,text_ref in zip(source['nativePartialEntrySnapshots'],source['partialEnteredUiText']):
                snapshot=bound(snapshot_ref).decode();partial=bound(text_ref)
                match=re.search(r'roledescription="editor" value="(.*?)"\n  uid=',snapshot,re.S)
                assert match and match.group(1).encode()==partial and partial!=requested
                assert any(r['sha256']==text_ref['sha256'] and r['bytes']==text_ref['bytes'] for r in stop['nativeUiTextSnapshots'])
            directory=(ROOT/source['receipt']['path']).parent
            assert not list(directory.glob('save-response*.json')) and not list(directory.glob('add-response*.json')) and not list(directory.glob('session-*-v1/chart-native-v1.csv'))
            counts.update(consumedSourceSlots=1,nativeEntryStops=1)
            continue
        assert requested==bound(source['executed'])
        assert len(requested)==asset['bytes'] and hashlib.sha256(requested).hexdigest()==source['sourceSha256']==asset['sha256']
        titles=runpy.run_path(str(BASE/'audit-request-v1.py'))['plot_titles'](requested.decode())
        assert titles==[p['title'] for p in asset['plots']]
        form=bound(source['sourceForm']);sep=b'\r\n' if b'\r\n' in form else b'\n';boundary=form.split(sep)[0]
        assert form.split(sep+sep,1)[1].split(sep+boundary,1)[0].replace(b'\r\n',b'\n')==requested
        receipt=json.loads(bound(source['receipt']));saved=json.loads(bound(source['saveBody']))
        assert receipt['sourceExact'] and saved['success']==source['nativeCompileSuccess']
        counts.update(nativeSaves=1,compilerBodies=1,consumedSourceSlots=1)
        if not saved['success']:
            assert source['addBody'] is None and not attempt['sessions']
            assert not list((ROOT/source['receipt']['path']).parent.glob('session-*-v1/render-v1.png'))
            counts['nativeSaveRefusals']+=1
            continue
        script=saved['result']['metaInfo']['scriptIdPart']
        assert script==source['privateScriptId'] and script not in private and source['privateVersion']=='1.0'
        private.add(script)
        assert source['addBody'] is not None
        added=json.loads(bound(source['addBody']));counts.update(nativeAdds=1,compilerBodies=1)
        if not added['success']:
            assert not attempt['sessions'];counts['nativeAddRefusals']+=1;continue
        meta=added['result']['metaInfo'];assert meta['scriptIdPart']==script
        assert receipt['removed'] and attempt['removed']
        assert len(receipt['sessions'])==len(attempt['sessions'])<=1
        for session in attempt['sessions']:
            raw=list(csv.reader(bound(session['csv']).decode('utf-8-sig').splitlines()));headers,rows=raw[0],raw[1:]
            bindings=json.loads(bound(session['columnBindings']));assert [c['originalHeader'] for c in bindings['columns']]==headers
            owned=set()
            for column in bindings['columns']:
                ordinal=column.get('sourceLiteralPlotOrdinal')
                if ordinal is None:continue
                title=titles[ordinal]
                assert column['originalHeader']==title and headers.count(title)==1
                assert column['owner']==script and column['sourceSha256']==asset['sha256'] and column['privateVersion']=='1.0'
                assert meta['styles'][column['nativePlotId']]['title']==title
                owned.add(title)
            assert set(bindings['missingOrAmbiguousRequestedPlotTitles'])==set(titles)-owned
            download=read((ROOT/session['csv']['path']).parent/'chart-download-v1.json')
            clock=datetime.fromisoformat(download['exportTrigger']['startedAtUtc'].replace('Z','+00:00')).timestamp()
            end=datetime.fromisoformat(receipt['completedAtUtc'].replace('Z','+00:00')).timestamp()
            assert clock<=download['downloadModifiedAtEpoch']<=end and download['sha256']==session['csv']['sha256']
            masks=list(csv.DictReader(bound(session['closureMask']).decode().splitlines()))
            assert len(rows)==len(masks)==session['dataRows']
            closed,eligible,anchors=[],[],[]
            for n,(row,mask) in enumerate(zip(rows,masks),1):
                assert len(row)==len(headers)
                values=dict(zip(headers,row));time=number(values.get('INPUT_TIME'));index=number(values.get('INPUT_INDEX'));phase=number(values.get('CASE_ID'))
                context=time is not None and index is not None and time.denominator==index.denominator==1 and time==1000*number(values['time']) and {'INPUT_INDEX','INPUT_TIME','CHART_CONFIRMED'}<=owned
                physical=context and not session['runtimeFailed'] and number(values['time'])+120<=clock and number(values.get('CHART_CONFIRMED'))==1
                phase_ok=phase is not None and phase.denominator==1 and index is not None and phase==index%8 and 'CASE_ID' in owned
                if physical:closed.append(n)
                if physical and phase_ok and index>=200:eligible.append(n)
                if physical and index>=200 and {'VISUAL_ANCHOR_TIME','VISUAL_ANCHOR_INDEX'}<=owned and number(values.get('VISUAL_ANCHOR_TIME'))==time and number(values.get('VISUAL_ANCHOR_INDEX'))==index:anchors.append(n)
                assert int(mask['row_ordinal'])==n and mask['csv_sha256']==session['csv']['sha256']
                assert int(mask['independently_closed'])==bool(physical) and int(mask['valid_phase_clock'])==bool(phase_ok)
                assert int(mask['eligible_minimum_index'])==bool(physical and phase_ok and index>=200)
                assert mask['time_raw_seconds']==values['time'] and mask['input_time_raw_ms']==values.get('INPUT_TIME') and mask['input_index_raw']==values.get('INPUT_INDEX') and mask['case_id_raw']==values.get('CASE_ID')
                assert json.loads(mask['blank_column_ordinals'])==[i for i,v in enumerate(row,1) if v=='']
            anchor=anchors[0] if len(anchors)==1 else None
            selected,prefix=[],[]
            for start in eligible:
                if number(rows[start-1][headers.index('CASE_ID')])!=0:continue
                block=list(range(start,start+32));previous=list(range(start-asset['requiredOriginalClosedPredecessors'],start))
                if anchor is None or block[-1]>=anchor or not all(n in eligible for n in block) or not all(n in closed for n in previous):continue
                combined=previous+block
                indices=[number(rows[n-1][headers.index('INPUT_INDEX')]) for n in combined];times=[number(rows[n-1][0]) for n in combined]
                if any(b!=a+1 for a,b in zip(indices,indices[1:])) or any(b<=a for a,b in zip(times,times[1:])):continue
                selected,prefix=block,previous;break
            assert selected==session['selectedPrimaryClosedRowOrdinals'] and prefix==session['originalClosedPredecessorRowOrdinals']
            assert anchors==session['visualAnchorCandidates'] and anchor==session['uniqueVisualAnchorRowOrdinal']
            assert closed==session['independentlyClosedRowOrdinals'] and eligible==session['eligibleClosedSourceRows']
            assert session['primaryInputCertificateValid']==(len(selected)==32)
            if selected:assert Counter(int(rows[n-1][headers.index('CASE_ID')]) for n in selected)==Counter({p:4 for p in range(8)})
            for n,mask in enumerate(masks,1):
                primary=len(selected)==32 and n in selected
                assert int(mask['primary_scoring_eligible'])==primary
                assert mask['present_cell_status']==('OBSERVED' if primary else 'OBSERVED / EXCLUDED')
                assert primary or mask['primary_exclusion_cause']
            counts.update(originalCSVs=1,dataRows=len(rows),independentlyClosedRows=len(closed),primaryRows=len(selected),uniquePrimaryPlotCells=len(selected)*len(owned),reservedClosedPredecessors=len(prefix))
            cache[session['csv']['sha256']]=raw;owned_by_sha[session['csv']['sha256']]=owned;sessions_by_source[source['sourceId']]=session
            if session['renderPng']:
                png=bound(session['renderPng']);assert png[:8]==b'\x89PNG\r\n\x1a\n';width,height=struct.unpack('>II',png[16:24]);assert width>0 and height>0
                counts['nativeRenderingPNGs']+=1
    assert all(counts[k]<=25 for k in ['nativeSaves','nativeAdds','originalCSVs','nativeRenderingPNGs','consumedSourceSlots'])
    fresh=runpy.run_path(str(BASE/'analyze-evidence-v1.py'))['analyze'](revision)
    assert fresh==numeric
    assert counts['uniquePrimaryPlotCells']==numeric['uniquePrimaryPlotCells']
    for entry in numeric['sources']:
        report=json.loads(bound(entry['report']));block=json.loads(bound(report['nativeBlock']))
        frozen=next(c for c in contracts['sources'] if c['sourceId']==entry['sourceId'])
        source_session=sessions_by_source.get(entry['sourceId'])
        if source_session:
            raw=cache[block['csv']['sha256']]
            for row in block['rows']+([dict(cells=block['visualAnchor']['cells'])] if block.get('visualAnchor') else []):
                for point in row['cells'].values():
                    if point is None:continue
                    assert point['csvSha256']==block['csv']['sha256'] and raw[point['rowOrdinal']][point['columnOrdinal']-1]==point['valueRaw'] and raw[0][point['columnOrdinal']-1]==point['headerRaw']
                    counts['rawNativePointerReferences']+=1

        def independent_comparisons(title,expected,comparisons):
            assert len(comparisons)==len(block['rows'])
            for row,comparison in zip(block['rows'],comparisons):
                actual=row['cells'].get(title);phase=row['phase'];value=expected[phase] if phase is not None and phase in range(8) else None
                dependency=title not in ['LINE_TIME_X1_DELTA','BOX_TIME_DELTA'] or row['originalClosedDependencyAvailable']
                code='U' if title not in block['ownedTitles'] or actual is None or value is None or not dependency else 'S' if (actual['valueRaw']=='' if value=='' else number(actual['valueRaw'])==number(value)) else 'R'
                assert comparison['rowOrdinal']==row['rowOrdinal'] and comparison['expectedRaw']==value and comparison['cellVerdict']==code
                counts['numericCellComparisons']+=1
        assert len(report['properties'])==len(frozen['contracts'])
        for prop,contract in zip(report['properties'],frozen['contracts']):
            assert prop['title']==contract['title'] and prop['expectedRawByPhase']==contract['expectedRawByPhase']
            independent_comparisons(prop['title'],contract['expectedRawByPhase'],prop['comparisonRows'])
            counts['numericProperty_'+prop['verdict']]+=1
        for family,frozen_family in zip(report['numericAlternatives'],frozen['alternatives']):
            assert family['id']==frozen_family['id']
            for variant,frozen_variant in zip(family['variants'],frozen_family['variants']):
                assert variant['id']==frozen_variant['id'] and variant['expectedRawByPhase']==frozen_variant['valuesByPhase']
                for title,expected in frozen_variant['valuesByPhase'].items():independent_comparisons(title,expected,variant['comparisonsByTitle'][title])
        if report['renderAssessment']:
            visual=json.loads(bound(report['renderAssessment']))
            assert runpy.run_path(str(BASE/'build-region-map-v1.py'))['build'](entry['sourceId'])==visual
            assert visual['originalPng']==source_session['renderPng'] and visual['originalCsv']==source_session['csv']
            assert visual['sourceSha256']==report['sourceSha256'] and visual['nativePrivateId']==block['nativePrivateId']
            case_ids={f['caseId'] for f in visual['facets']}
            extra_path=BASE/entry['sourceId']/'visual-inspection-addendum-v1.json'
            if extra_path.exists():
                extra=read(extra_path)
                assert extra['sourceId']==entry['sourceId'] and extra['sourceSha256']==report['sourceSha256']
                assert extra['originalPng']==source_session['renderPng'] and json.loads(bound(extra['priorDerivedMap']))==visual
                extra_ids={f['caseId'] for f in extra['facets']};assert not case_ids & extra_ids
                assert all(f['verdict']=='UNDECIDED' and f['notObservedCause'] for f in extra['facets'])
                case_ids |= extra_ids
                counts['visualFacet_UNDECIDED']+=len(extra_ids)
            assert case_ids==set(assets[entry['sourceId']]['caseIds'])
            for facet in visual['facets']:
                assert facet['verdict'] in ['SUPPORTED','REFUTED','UNDECIDED']
                counts['visualFacet_'+facet['verdict']]+=1
            counts['derivedRegionMaps']+=1
    if preservation:
        old=read(BASE/'environment-v1/native-layout-list-before-response-v1.json');new=read(BASE/'environment-v2/native-layout-list-after-response-v1.json');indexed={r['id']:r for r in new}
        creation=read(BASE/'environment-v1/native-layout-create-response-v1.json');assert len(old)==17 and len(new)==18 and creation['id'] not in {r['id'] for r in old}
        assert indexed[creation['id']]['image_url']==creation['image_url']
        comparison=read(BASE/'environment-v2/existing-layout-comparison-v1.json')
        saved=[r==indexed.get(r['id']) for r in old];tabs=[signature((BASE/f'environment-v1/page-{p}-before-v1.txt').read_text())==signature((BASE/f'environment-v2/page-{p}-after-v1.txt').read_text()) for p in range(1,14)]
        assert saved==[r['equal'] for r in comparison['savedRecordComparisons']] and tabs==[r['equal'] for r in comparison['openTabComparisons']]
        counts.update(oldSavedRecordsUnchanged=sum(saved),oldSavedRecordsChanged=sum(not x for x in saved),oldOpenTabsUnchanged=sum(tabs),oldOpenTabsChanged=sum(not x for x in tabs))
    if integrity:
        refs=read(BASE/f'artifact-integrity-v{revision}.json')['artifacts'];assert len({r['path'] for r in refs})==len(refs)
        for reference in refs:bound(reference)
        counts['integrityBoundFiles']=len(refs)
    return dict(version=f'v{revision}',status='PASS',counts=dict(counts),policy='Read-only independent source/form/private/column/physical closure/phase/anchor/predecessor/raw-pointer/frozen-integer/PNG-map/preservation/integrity checks. Human visual findings stay scoped to their bound original PNG regions; counts never multiply native cells.')


if __name__=='__main__':print(json.dumps(validate(int(sys.argv[1]) if len(sys.argv)>1 else 1),indent=2))
