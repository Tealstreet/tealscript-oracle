import json
import runpy
import sys
from fractions import Fraction
from pathlib import Path

BASE=Path(__file__).resolve().parent
HELPERS=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put=HELPERS['ref'],HELPERS['put']


def overlap(intervals):
    left=max(p[0] for p in intervals);right=min(p[1] for p in intervals)
    return [float(left),float(right)] if left<=right else None


def build(source_id):
    directory=BASE/source_id;certificate_path=directory/'pixel-certificate-v1.json';certificate=json.loads(certificate_path.read_text())
    result=dict(version='v1',sourceId=source_id,certificate=ref(certificate_path),originalPng=certificate['originalPng'],originalCsv=certificate['originalCsv'],measurements=[],outcome='UNDECIDED',scope='Finite relationships of exact original sample profiles with independently readable controls; no universal pixel/font/dash law.')
    if source_id=='v104-glyph-advance-v6':
        widths={}
        for profile in certificate['rowProfiles']:
            spec=profile['specification'];runs=[r for r in profile['runs'] if r['sample']==spec['exactBodySample']];assert runs
            first,last=runs[0]['first'],runs[-1]['last'];assert profile['xFirstPx']<first<last<profile['xLastPx']
            widths[spec['name']]=last-first+1
            result['measurements'].append(dict(name=spec['name'],yPx=profile['yPx'],bodyFirstPx=first,bodyLastPx=last,widthInclusivePx=last-first+1,exactObservedBodySample=spec['exactBodySample']))
        assert set(widths)=={'monoI','monoW','defaultI','defaultW'}
        edge=certificate['registration']['strokeEdgePxUncertainty'];uncertainty=4*edge
        observed=widths['monoW']-widths['monoI'];control=widths['defaultW']-widths['defaultI']
        a=[-uncertainty,uncertainty];b=[control-uncertainty,control+uncertainty]
        separate=a[1]<b[0] or b[1]<a[0]
        a_match=a[0]<=observed<=a[1];b_match=b[0]<=observed<=b[1]
        result.update(outerBodyWidthsInclusivePx=widths,observedMonospaceDifferencePx=observed,observedDefaultDifferencePx=control,candidateIntervalsPx=dict(A=a,B=b),uncertaintyDerivation='Four independently measured outer edges times the preregistered one-pixel stroke-edge uncertainty',strictlyDisjoint=separate,outcome='SUPPORTED_A' if separate and a_match and not b_match else 'SUPPORTED_B' if separate and b_match and not a_match else 'CONTRARY' if separate and not a_match and not b_match else 'UNDECIDED')
    elif source_id=='v104-dash-period-v6':
        constant=[];proportional=[];complete=True
        for profile in certificate['rowProfiles']:
            spec=profile['specification'];width=spec['sourceWidth'];assert width in [1,4,8]
            runs=[r for r in profile['runs'] if r['sample']==spec['exactStrokeSample'] and profile['xFirstPx']<r['first']<=r['last']<profile['xLastPx']]
            periods=[b['first']-a['first'] for a,b in zip(runs,runs[1:])]
            gaps=[b['first']-a['last']-1 for a,b in zip(runs,runs[1:])]
            valid=len(periods)>=3 and all(g>0 for g in gaps)
            complete=complete and valid
            interval=[min(periods),max(periods)] if periods else None
            if interval:
                constant.append(interval);proportional.append([Fraction(v,width) for v in interval])
            result['measurements'].append(dict(name=spec['name'],sourceWidth=width,yPx=profile['yPx'],exactObservedStrokeSample=spec['exactStrokeSample'],completeInteriorStrokeRuns=runs,completeInteriorPeriodCount=len(periods),periodsPx=periods,gapsPx=gaps,observedPeriodRangePx=interval,periodsAccessible=valid))
        assert sorted(m['sourceWidth'] for m in result['measurements'])==[1,4,8]
        a=overlap(constant) if len(constant)==3 else None;b=overlap(proportional) if len(proportional)==3 else None
        result.update(allThreeLanesComplete=complete,constantPeriodIntersectionPx=a,widthNormalizedPeriodIntersectionPx=b,periodRangePolicy='Minimum and maximum exact repeated stroke-start distances; no fitted tolerance or nearest-period rule',outcome='SUPPORTED_A' if complete and a is not None and b is None else 'SUPPORTED_B' if complete and b is not None and a is None else 'CONTRARY' if complete and a is None and b is None else 'UNDECIDED')
    else:raise ValueError('No frozen relative-pixel relation for '+source_id)
    return result


if __name__=='__main__':
    result=build(sys.argv[1]);put(BASE/sys.argv[1]/'pixel-relations-v1.json',result)
    print(json.dumps(dict(sourceId=sys.argv[1],outcome=result['outcome'],measurements=len(result['measurements']))))
