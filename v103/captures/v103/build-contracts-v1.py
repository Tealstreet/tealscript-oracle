import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]


def build():
    manifest = json.loads((ROOT / 'v103/bundle-manifest-v1.json').read_text())
    sources = []
    for asset in manifest['sources']:
        properties = []
        for plot in asset['plots']:
            title = plot['title']
            witness = asset['numericWitnesses'].get(title)
            contract = dict(title=title, sourcePlotOrdinal=plot['sourcePlotOrdinal'], rule='OWNED_CONTEXT', prediction=None)
            if witness:
                match = re.search(r'anchor(?: only)?:\s*(-?\d+)', witness)
                assert match, (title, witness)
                contract.update(rule='BUILD_EVENT', prediction=match[1], note=witness, primaryMeaning='31 intentional blanks plus one original closed build-event observation; not32 independent getter observations')
            elif title in ['SCALE_LOW', 'SCALE_HIGH', 'WIDTH_INTENT', 'LEFT_X_INTENT', 'RIGHT_X_INTENT']:
                contract.update(rule='CONSTANT', prediction={'SCALE_LOW':'0', 'SCALE_HIGH':'100', 'WIDTH_INTENT':'4', 'LEFT_X_INTENT':'-85', 'RIGHT_X_INTENT':'-15'}[title], intentOnly=title.endswith('INTENT'))
            elif title in ['VISUAL_ANCHOR_INDEX', 'VISUAL_ANCHOR_TIME']:
                contract.update(rule='UNIQUE_BUILD_MARKER', prediction='Own index/time at A; blank at other primary rows')
            elif asset['family'] == 'visible-gap' and title not in ['INPUT_INDEX', 'INPUT_TIME', 'CHART_CONFIRMED', 'CASE_ID']:
                if title in ['OFFSET0', 'OFFSET1']:
                    contract.update(rule='OFFSET_POLICY' if title == 'OFFSET1' else 'PHASE_FORMULA', prediction=['94' if p == 0 else '' for p in range(8)])
                    if title == 'OFFSET1':contract['alternativeScreenAligned'] = ['94' if p == 1 else '' for p in range(8)]
                elif title == 'STEP':contract.update(rule='PHASE_FORMULA', prediction=[str(70+p) for p in range(8)])
                else:
                    base = {'LINE':10, 'BREAK':25, 'AREA':40, 'AREA_BREAK':55, 'DASH':85}[title]
                    contract.update(rule='PHASE_FORMULA', prediction=['' if p in [3,4] else str(base+p) for p in range(8)])
            elif asset['family'] == 'fillgaps-overloads' and title in ['P20','P40','P60','P80']:
                contract.update(rule='PHASE_FORMULA', prediction=['' if p in [3,4] else title[1:] for p in range(8)])
            elif asset['family'] == 'plot-controls' and title in ['JOIN','NOJOIN','TAIL4','TRACK']:
                base = 15 if title == 'JOIN' else 45
                values = [str(base+2*p) if p % 4 < 2 else '' for p in range(8)] if title in ['JOIN','NOJOIN'] else ['65' if title == 'TAIL4' else '90']*8
                contract.update(rule='PHASE_FORMULA', prediction=values)
            elif asset['family'] == 'markers' and title in ['SMALL_SQUARE','LARGE_SQUARE','CHAR_X']:
                phase, value = {'SMALL_SQUARE':(0,'80'), 'LARGE_SQUARE':(4,'60'), 'CHAR_X':(2,'30')}[title]
                contract.update(rule='PHASE_FORMULA', prediction=[value if p == phase else '' for p in range(8)])
            elif title in ['ARROW_PHASE','ARROWS']:
                contract.update(rule='MOD32_FORMULA', prediction=[str(p) if title == 'ARROW_PHASE' else {0:'1',8:'2',16:'4',24:'-4'}.get(p,'') for p in range(32)])
            properties.append(contract)
        sources.append(dict(sourceId=asset['sourceId'], sourceSha256=asset['sha256'], contracts=properties, frozenNumericWitnesses=asset['numericWitnesses'], lifecycleScope='Getter/state output only at the retained build event; pixel outcomes are separately tested against frozen visual models'))
    return dict(version='v1', method='Frozen request/source-derived contracts before native Save/output observation; no engine values or fitted targets', sources=sources, primarySelection='A-31..A, rotated phase cycles, eight original closed predecessors', calibrationUncertaintyBeforeScoring=dict(axisXPx=2, axisYPx=3, strokeEdgePx=1), missingOrOverlappingCandidates='UNDECIDED; no adjusted viewport, tolerance, source or model')


if __name__ == '__main__':
    result = build()
    path = BASE / 'numeric-contracts-v1.json'
    content = json.dumps(result, indent=2) + '\n'
    if path.exists():
        assert path.read_text() == content
    else:
        path.write_text(content)
    print(json.dumps(dict(sources=len(result['sources']), properties=sum(len(s['contracts']) for s in result['sources']))))
