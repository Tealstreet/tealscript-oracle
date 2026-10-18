import csv
import json
import runpy
import sys
from fractions import Fraction
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
PREVIOUS=runpy.run_path(str(BASE/'validate-evidence-v3.py'))
read,clock=PREVIOUS['read'],PREVIOUS['PREVIOUS']['clock']


def validate(revision=1,integrity=True,preservation=None):
    result=PREVIOUS['validate'](revision,integrity=integrity,preservation=preservation)
    inventory=read(BASE/f'attempt-inventory-v{revision}.json');sid='v104-arrow-direction-v6'
    attempt=next((a for a in inventory['attempts'] if a['source']['sourceId']==sid),None)
    path=BASE/sid/'arrow-certificate-v1.json'
    if attempt and path.exists():
        certificate=read(path);assert runpy.run_path(str(BASE/'build-arrow-certificate-v1.py'))['build']()==certificate
        session=attempt['sessions'][0];source=attempt['source'];assert certificate['originalPng']==session['renderPng'] and certificate['originalCsv']==session['csv'] and certificate['privateScriptId']==source['privateScriptId']
        visual=read(BASE/sid/'derived-region-map-v1.json');inspection=read(BASE/sid/'visual-inspection-v1.json');prereg=read(BASE/'environment-v1/arrow-morphology-preregistration-v1.json')
        assert clock(prereg['recordedAtUtc'])<clock(inspection['inspectedAtUtc']) and prereg['edgeUncertaintyPx']==1
        assert visual['facets'][0]['outcome']==certificate['outcome'] or visual['facets'][0]['outcome']=='UNDECIDED'
        raw=list(csv.reader((ROOT/session['csv']['path']).open(newline='')));headers=raw[0];primary=session['selectedPrimaryClosedRowOrdinals']
        assert len(certificate['arrows'])==2
        for arrow in certificate['arrows']:
            assert arrow['phase']==(8 if arrow['sign']==1 else 24)
            assert int(arrow['inputIndex']['valueRaw'])%32==arrow['phase'] and arrow['inputIndex']['rowOrdinal'] in primary
            control=arrow['control'];assert control['phase']==(12 if arrow['sign']==1 else 28) and int(control['inputIndex']['valueRaw'])%32==control['phase'] and control['inputIndex']['rowOrdinal'] in primary
            assert control['literal']==('U' if arrow['sign']==1 else 'D') and Fraction(control['signCell']['valueRaw'])==arrow['sign']
            pointers=[arrow[k] for k in ['chartTime','inputIndex','signCell','directionCell']]+list(arrow['ownOhlc'].values())+[control[k] for k in ['chartTime','inputIndex','signCell']]
            for p in pointers:assert p['csvSha256']==session['csv']['sha256'] and raw[p['rowOrdinal']][p['columnOrdinal']-1]==p['valueRaw'] and headers[p['columnOrdinal']-1]==p['headerRaw']
            top,bottom=arrow['bodyYInclusivePx'];q=(bottom-top+1)//4;widths={r['yPx']:r['widthInclusivePx'] for r in arrow['rawRowMeasurements']}
            upper=max(widths[y] for y in range(top,top+q));lower=max(widths[y] for y in range(bottom-q+1,bottom+1))
            assert arrow['quarterWidthIntervalsPx']==dict(top=[upper-2,upper+2],bottom=[lower-2,lower+2])
            if arrow['outcome']=='SUPPORTED_A':
                assert arrow['headAt']==('top' if arrow['sign']==1 else 'bottom') and arrow['sourceJoin'] and control['sourceJoin'] and arrow['tipNarrowingReadable'] and arrow['ownCandleClearBeyondFrozenFourPixelYAndEdgeUncertainty'] and arrow['rawOwnCandleClearancePx']>4
                assert upper-2>lower+2 if arrow['sign']==1 else lower-2>upper+2
        result['counts']['arrowCertificates']=1
    result['policy']+='; native arrow endpoint morphology, strict shoulder/shaft intervals and four independent closed modulo32 sign/control joins'
    return result


if __name__=='__main__':print(json.dumps(validate(int(sys.argv[1])),indent=2))
