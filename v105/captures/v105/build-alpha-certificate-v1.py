import csv
import hashlib
import json
import math
import runpy
import subprocess
import sys
from datetime import datetime,timezone
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
HELPERS=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put,number=HELPERS['ref'],HELPERS['put'],HELPERS['number']
PNG=runpy.run_path(str(BASE/'read-png-pixels-v1.py'))


def build(write=False):
    directory=BASE/'v105-alpha-composite-v6';session_dir=directory/'attempt-v1/session-mode0-v1'
    selected_path=directory/'profile-selection-v1.json';selected=json.loads(selected_path.read_text())
    asset=json.loads((ROOT/'v105/bundle-manifest-v1.json').read_text())['entries'][0]
    session=json.loads((session_dir/'row-set-observation-v1.json').read_text());observation=json.loads((directory/'attempt-v1/observation-v1.json').read_text())
    inspection_path=directory/'visual-inspection-v1.json';inspection=json.loads(inspection_path.read_text());cal=inspection['axisCalibration']
    png=ROOT/session['renderPng']['path'];decoded=PNG['decode'](png);pixel=decoded['pixel'];raw=list(csv.reader((ROOT/session['csv']['path']).open(newline='')));headers=raw[0]
    ticks=[]
    for tick in cal['xTicks']:
        n=[n for n,r in enumerate(raw[1:],1) if r[0]==str(tick['unixSeconds'])];assert len(n)==1
        ticks.append((tick['xPx'],number(raw[n[0]][headers.index('INPUT_INDEX')])))
    b=(ticks[1][0]-ticks[0][0])/float(ticks[1][1]-ticks[0][1]);anchor=session['uniqueVisualAnchorRowOrdinal'];a=number(raw[anchor][headers.index('INPUT_INDEX')]);xa=ticks[0][0]+b*float(a-ticks[0][1]);y0,y100=cal['yZeroPx'],cal['yHundredPx'];yp=lambda v:y0-v*(y0-y100)/100
    sampling=asset['sampling'];records=[];all_samples=bytearray()
    groups=[('subjects',sampling['subjects']),('controls',sampling['controls']),('lineControls',sampling['lineControls']),('background',[sampling['background']])]
    for role,specs in groups:
        for spec in specs:
            x,y=map(lambda v:math.floor(v+0.5),[xa+spec['center'][0]*b,yp(spec['center'][1])]);samples=[]
            for yy in range(y-2,y+3):
                for xx in range(x-2,x+3):
                    value=pixel(xx,yy);samples.append(dict(xPx=xx,yPx=yy,rawSample=value));all_samples.extend(value[:3])
            tuples=sorted({tuple(p['rawSample']) for p in samples});actual_bounds=inspection['patchInteriorBoundsPx'].get(spec['id']);clearance=None
            if actual_bounds:clearance=min(x-2-actual_bounds[0],y-2-actual_bounds[1],actual_bounds[2]-(x+2),actual_bounds[3]-(y+2))
            records.append(dict(patchId=spec['id'],role=role,frozenSpecification=spec,centerPx=[x,y],samples=samples,uniqueRawSamples=[list(v) for v in tuples],flat=len(tuples)==1,independentlyInspectedInteriorBoundsPx=actual_bounds,minimumSampleEdgeClearancePx=clearance,edgeClearancePass=clearance is not None and clearance>=5,occlusion=inspection['patchOcclusion'].get(spec['id'],'UNOBSERVED')))
    assert len(records)==31 and len({p['patchId'] for p in records})==31 and len(all_samples)==31*25*3
    raw_path=directory/'original-fixed-patch-samples-rgb8-v1.bin';converted_path=directory/'derived-fixed-srgb-samples-rgb8-v1.bin';conversion=None;converted=None
    if write:
        if raw_path.exists():assert raw_path.read_bytes()==all_samples
        else:raw_path.write_bytes(all_samples)
    pipeline=selected['selectedPipeline']
    if pipeline=='EMBEDDED_ICC_TO_FIXED_SRGB_RELATIVE_NO_BPC':
        icc=ROOT/next(c['decodedIcc']['path'] for c in selected['originalColorChunks'] if c['type']=='iCCP');target=ROOT/selected['targetProfile']['path']
        command=['/tmp/oracle-v105-convert-icc-samples-v1',str(icc),str(target),str(raw_path),str(converted_path)]
        if write and not converted_path.exists():
            r=subprocess.run(command,text=True,capture_output=True);assert r.returncode==0,r.stderr
            put(directory/'conversion-receipt-v1.json',dict(version='v1',command=command,stdout=r.stdout,stderr=r.stderr,exitCode=r.returncode,implementation='Apple ColorSync, macOS27.0 build26A428',inputProfile=ref(icc),outputProfile=ref(target),inputSamples=ref(raw_path),outputSamples=ref(converted_path),tool=ref(BASE/'convert-icc-samples-v1.c'),intent='relative-colorimetric',blackPointCompensation=False,channels=3,inputBitDepth=8,outputBitDepth=8,syntheticAlpha=False))
        if converted_path.exists():converted=converted_path.read_bytes();conversion=ref(directory/'conversion-receipt-v1.json')
    elif pipeline=='AUTHENTICATED_SRGB_RAW_ENCODED8':converted=bytes(all_samples)
    if converted is not None:assert len(converted)==len(all_samples)
    for i,record in enumerate(records):
        values=[]
        for j,sample in enumerate(record['samples']):
            offset=(i*25+j)*3;value=list(converted[offset:offset+3]) if converted is not None else None
            sample['comparisonRgb8']=value
            if value is not None:values.append(tuple(value))
        record['uniqueComparisonRgb8']=[list(v) for v in sorted(set(values))]
    patches={p['patchId']:p for p in records}
    def complete(name):return patches[name]['flat'] and patches[name]['edgeClearancePass'] and patches[name]['occlusion']=='NONE' and len(patches[name]['uniqueComparisonRgb8'])==1
    def value(name):return patches[name]['uniqueComparisonRgb8'][0] if len(patches[name]['uniqueComparisonRgb8'])==1 else None
    gate_checks={name:dict(expected=literal,all25Exact=complete(name) and all(p['comparisonRgb8']==literal for p in patches[name]['samples']),observedValues=patches[name]['uniqueComparisonRgb8']) for name,literal in {'RED':[255,0,0],'BLUE':[0,0,255],'PURPLE':[128,0,128]}.items()}
    gate=pipeline is not None and all(c['all25Exact'] for c in gate_checks.values());facets=[]
    control_ids=[p['id'] for p in sampling['controls']];classes={}
    for name in control_ids:
        if value(name) is not None:classes.setdefault(tuple(value(name)),[]).append(name)
    for facet in asset['visualFacets']:
        causes=[];pairs=[]
        if not gate:causes.append('Exact all25 opaque RED/BLUE/PURPLE gate or preregistered profile pipeline fails; zero composite scoring credit')
        required=control_ids+['PANE_BG']+facet['subjectPatchIds']
        if 'line-' in facet['facetId']:required+=['OPAQUE_LINE_RED','OPAQUE_LINE_BLUE','OPAQUE_LINE_GRAY']
        if not all(complete(name) for name in required):causes.append('One or more frozen required patches are nonflat, occluded, missing or fail five-pixel edge clearance')
        if value('PANE_BG')!=value('GRAY') or value('GRAY') is None:causes.append('Source-owned pane background does not authenticate against GRAY swatch')
        if 'line-' in facet['facetId'] and any(value('OPAQUE_LINE_'+name)!=value(name) for name in ['RED','BLUE','GRAY']):causes.append('Independent opaque line controls do not match same-shot box controls')
        encoded=set(facet['encodedCandidateIds']);linear=set(facet['linearCandidateIds']);collisions=[names for names in classes.values() if encoded.intersection(names) and linear.intersection(names)]
        for subject in facet['subjectPatchIds']:
            foreground='BLUE' if '_BLUE_' in subject else 'RED';background='GRAY' if '_BG' in subject else 'RED' if foreground=='BLUE' else 'BLUE';sample=value(subject)
            matches=[name for name in facet['encodedCandidateIds']+facet['linearCandidateIds'] if sample is not None and sample==value(name)]
            behavior='BLEND_SEPARATED' if sample is not None and sample!=value(foreground) and sample!=value(background) else 'OPAQUE_OVERWRITE' if sample is not None and sample==value(foreground) else 'CONTRARY'
            pairs.append(dict(subjectPatchId=subject,comparisonRgb8=sample,foregroundControl=foreground,backgroundControl=background,matchingFiniteCandidateIds=matches,matchingRawSameShotCandidateIds=[name for name in control_ids if patches[subject]['uniqueRawSamples']==patches[name]['uniqueRawSamples']],behavior=behavior,finiteCandidateStatus='UNDECIDED_COLLIDED_CLASSES' if collisions else 'MATCHED_EQUIVALENCE_CLASS' if matches else 'UNLISTED_CONTRARY' if sample is not None else 'UNDECIDED',scoringEligible=not causes))
        behaviors={p['behavior'] for p in pairs};outcome='UNDECIDED' if causes else 'SUPPORTED_A' if behaviors=={'BLEND_SEPARATED'} else 'SUPPORTED_B' if behaviors=={'OPAQUE_OVERWRITE'} else 'CONTRARY'
        facets.append(dict(facetId=facet['facetId'],outcome=outcome,notObservedCauses=causes,encodedLinearCandidateCollisions=collisions,subjects=pairs,scope='Finite blending-versus-overwrite pair; candidate equivalence/unknowns remain separate. No nearest-color fit or recovered intermediate alpha.'))
    return dict(version='v1',sourceId=asset['sourceId'],sourceSha256=asset['sha256'],privateScriptId=observation['privateScriptId'],privateVersion=observation['privateVersion'],originalPng=session['renderPng'],originalCsv=session['csv'],rowSet=ref(session_dir/'row-set-observation-v1.json'),inspection=ref(inspection_path),profileSelection=ref(selected_path),conversionReceipt=conversion,originalRgbSamples=ref(raw_path),convertedRgbSamples=ref(converted_path) if converted_path.exists() else None,patches=records,opaqueGatePassed=gate,opaqueGateChecks=gate_checks,candidateEquivalenceClasses=[dict(comparisonRgb8=list(k),candidateIds=v) for k,v in classes.items()],facets=facets,scope='Original31 fixed5x5 patches and optional separately DERIVED preregistered ColorSync samples. Zero tolerance, zero original-image edits, RGB container has no observed intermediate alpha; no v104 retroclassification.')


if __name__=='__main__':
    result=build(write=True);put(BASE/'v105-alpha-composite-v6/alpha-certificate-v1.json',result)
    summary={'opaqueGatePassed':result['opaqueGatePassed'],'gateChecks':result['opaqueGateChecks'],'facets':[{k:f[k] for k in ['facetId','outcome']} for f in result['facets']]}
    print(json.dumps(summary))
