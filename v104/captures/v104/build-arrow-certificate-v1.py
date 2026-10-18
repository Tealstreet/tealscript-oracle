import csv
import json
import runpy
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
HELPERS=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put,number=HELPERS['ref'],HELPERS['put'],HELPERS['number']


def build():
    source_id='v104-arrow-direction-v6';directory=BASE/source_id;pixel_path=directory/'pixel-certificate-v1.json';pixel=json.loads(pixel_path.read_text())
    inspection_path=directory/'visual-inspection-v1.json';inspection=json.loads(inspection_path.read_text());finding=inspection['facets'][0]
    session=json.loads((ROOT/pixel['rowSet']['path']).read_text());raw=list(csv.reader((ROOT/pixel['originalCsv']['path']).open(newline='')));headers=raw[0]
    anchor=session['uniqueVisualAnchorRowOrdinal'];a=int(number(raw[anchor][headers.index('INPUT_INDEX')]))
    primary=session['selectedPrimaryClosedRowOrdinals'];b=pixel['registration']['pixelsPerOwnBar'];xa=pixel['registration']['anchorXPx']
    def point(n,title):
        c=headers.index(title);return dict(csvSha256=pixel['originalCsv']['sha256'],rowOrdinal=n,columnOrdinal=c+1,headerRaw=title,valueRaw=raw[n][c])
    def row(phase):
        found=[n for n in primary if int(number(raw[n][headers.index('INPUT_INDEX')]))%32==phase];assert len(found)==1
        return found[0]
    price1,price2=inspection['axisCalibration']['priceTicks'][:2];slope=(price2['yPx']-price1['yPx'])/(price2['value']-price1['value']);price_y=lambda value:price1['yPx']+(float(value)-price1['value'])*slope
    arrows=[]
    for name,phase,sign,control_phase,literal in [('positive',8,1,12,'U'),('negative',24,-1,28,'D')]:
        n=row(phase);control=row(control_phase);own=int(number(raw[n][headers.index('INPUT_INDEX')]))
        profiles=[p for p in pixel['rowProfiles'] if p['specification']['objectId']==name];assert profiles
        sample=profiles[0]['specification']['exactBodySample'];measurements=[]
        for profile in profiles:
            xs=[x for r in profile['runs'] if r['sample']==sample for x in range(r['first'],r['last']+1)]
            measurements.append(dict(yPx=profile['yPx'],firstXPx=min(xs) if xs else None,lastXPx=max(xs) if xs else None,widthInclusivePx=max(xs)-min(xs)+1 if xs else 0))
        obj=finding['arrowObjects'][name];top,bottom=obj['bodyYInclusivePx'];height=bottom-top+1;quarter=max(1,height//4)
        widths={r['yPx']:r['widthInclusivePx'] for r in measurements};assert all(y in widths for y in range(top,bottom+1))
        upper=max(widths[y] for y in range(top,top+quarter));lower=max(widths[y] for y in range(bottom-quarter+1,bottom+1))
        ui=[upper-2,upper+2];li=[lower-2,lower+2]
        head='top' if ui[0]>li[1] else 'bottom' if li[0]>ui[1] else None
        outward=[r for r in measurements if r['widthInclusivePx']>0]
        if head=='bottom':outward=list(reversed(outward))
        tip_widths=[r['widthInclusivePx'] for r in outward[:6]]
        narrowing=head is not None and len(tip_widths)==6 and tip_widths[0]<tip_widths[-1] and all(v>u for u,v in zip(tip_widths,tip_widths[1:]))
        expected_x=xa+(own-a)*b;actual_x=obj['centerXPx'];join=abs(actual_x-expected_x)<=2 and number(raw[n][headers.index('SIGN')])==sign and number(raw[n][headers.index('DIRECTION')])==sign
        ctrl=finding['controls'][literal];ctrl_own=int(number(raw[control][headers.index('INPUT_INDEX')]))
        control_join=ctrl['literal']==literal and abs(ctrl['centerXPx']-(xa+(ctrl_own-a)*b))<=2 and number(raw[control][headers.index('CONTROL_SIGN')])==sign and number(raw[control][headers.index('UP_CONTROL' if sign==1 else 'DOWN_CONTROL')])==1
        high_y=price_y(raw[n][headers.index('high')]);low_y=price_y(raw[n][headers.index('low')])
        clearance=top-max(high_y,low_y) if sign==1 else min(high_y,low_y)-bottom
        candle_clear=clearance>4
        complete=candle_clear and join and control_join and narrowing and obj['bothEndsAndShaftReadable'] and obj['clearOfCandlesAndOtherObjects'] and ctrl['completeUnoccluded']
        outcome='SUPPORTED_A' if complete and head==('top' if sign==1 else 'bottom') else 'SUPPORTED_B' if complete and head==('bottom' if sign==1 else 'top') else 'UNDECIDED'
        arrows.append(dict(objectId=name,phase=phase,sign=sign,sourceOwnIndex=own,chartTime=point(n,'time'),inputIndex=point(n,'INPUT_INDEX'),signCell=point(n,'SIGN'),directionCell=point(n,'DIRECTION'),ownOhlc={title:point(n,title) for title in ['open','high','low','close']},sourceCenterXPx=expected_x,observedCenterXPx=actual_x,sourceJoin=join,ownCandlePixelEnvelopeYPx=[min(high_y,low_y),max(high_y,low_y)],rawOwnCandleClearancePx=clearance,ownCandleClearBeyondFrozenFourPixelYAndEdgeUncertainty=candle_clear,bodyYInclusivePx=[top,bottom],registeredQuarterHeightPx=quarter,upperQuarterMaximumWidthPx=upper,lowerQuarterMaximumWidthPx=lower,quarterWidthIntervalsPx=dict(top=ui,bottom=li),headAt=head,outwardTipWidthsPx=tip_widths,tipNarrowingReadable=narrowing,control=dict(phase=control_phase,inputIndex=point(control,'INPUT_INDEX'),chartTime=point(control,'time'),signCell=point(control,'CONTROL_SIGN'),literal=literal,glyphRegionPx=ctrl['glyphRegionPx'],sourceJoin=control_join),rawRowMeasurements=measurements,outcome=outcome))
    outcomes={a['outcome'] for a in arrows};outcome=next(iter(outcomes)) if len(outcomes)==1 else 'UNDECIDED' if 'UNDECIDED' in outcomes else 'CONTRARY'
    return dict(version='v1',sourceId=source_id,sourceSha256=pixel['sourceSha256'],privateScriptId=pixel['privateScriptId'],originalPng=pixel['originalPng'],originalCsv=pixel['originalCsv'],pixelCertificate=ref(pixel_path),manualInspection=ref(inspection_path),morphologyPreregistration=ref(BASE/'environment-v1/arrow-morphology-preregistration-v1.json'),rowSet=pixel['rowSet'],anchorOwnIndex=a,arrows=arrows,outcome=outcome,scope='Actual native tip narrowing and head shoulders distinguish ends, separately from source SIGN, color, above/below placement and U/D. Only this source/version/closed block; old arrow holds retain zero retroactive credit.')


if __name__=='__main__':
    result=build();put(BASE/'v104-arrow-direction-v6/arrow-certificate-v1.json',result)
    print(json.dumps(dict(outcome=result['outcome'],arrows=[dict(objectId=a['objectId'],headAt=a['headAt'],upperWidth=a['upperQuarterMaximumWidthPx'],lowerWidth=a['lowerQuarterMaximumWidthPx']) for a in result['arrows']])))
