import json
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]


def build():
    manifest=json.loads((ROOT/'v107/bundle-manifest-v1.json').read_text());sources=[]
    for asset in manifest['entries']:
        contracts=[]
        for plot in asset['plots']:
            title=plot['title'];witness=asset['numericWitnesses'].get(title)
            contract=dict(title=title,sourcePlotOrdinal=plot['sourcePlotOrdinal'],rule='OWNED_CONTEXT',prediction=None)
            if witness:
                assert witness['anchorExpected']=='UNSPECIFIED'
                contract.update(rule='BUILD_EVENT_UNSPECIFIED',prediction=None,frozenWitness=witness)
            elif title in ['SCALE_LOW','SCALE_HIGH']:contract.update(rule='CONSTANT',prediction='0' if title=='SCALE_LOW' else '100')
            elif title in ['VISUAL_ANCHOR_INDEX','VISUAL_ANCHOR_TIME']:contract.update(rule='UNIQUE_BUILD_MARKER',prediction='Own index/time at A; blank elsewhere')
            contracts.append(contract)
        sources.append(dict(sourceId=asset['sourceId'],sourceSha256=asset['sha256'],contracts=contracts,frozenNumericWitnesses=asset['numericWitnesses']))
    return dict(version='v1',method='Frozen exact source/manifest numeric contracts before native entry; no engine or observed-output fitting',sources=sources,primarySelection='CSV own A-31..A plus8 original A-39..A-32 predecessors; no PNG bar-visibility requirement',calibrationUncertaintyBeforeScoring=dict(axisXPx=2,axisYPx=3,strokeEdgePx=1),viewportPrerequisite=manifest['viewportPrerequisite'],missingTableRegistration='UNDECIDED for affected table property; horizontal bar calibration and pane dimensions are recorded without gates',buildEventScope='One actual build event plus31 intentional blanks; unspecified native table state has no invented target')


if __name__=='__main__':
    result=build();path=BASE/'numeric-contracts-v1.json';content=json.dumps(result,indent=2)+'\n'
    if path.exists():assert path.read_text()==content
    else:path.write_text(content)
    print(json.dumps(dict(sources=len(result['sources']),properties=sum(len(s['contracts']) for s in result['sources']))))
