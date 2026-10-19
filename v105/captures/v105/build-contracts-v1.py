import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]


def build():
    manifest = json.loads((ROOT/'v105/bundle-manifest-v1.json').read_text())
    sources = []
    for asset in manifest['entries']:
        contracts = []
        for plot in asset['plots']:
            title = plot['title']
            witness = asset['numericWitnesses'].get(title)
            contract = dict(title=title, sourcePlotOrdinal=plot['sourcePlotOrdinal'], rule='OWNED_CONTEXT', prediction=None)
            if witness:
                role = witness['role']
                value = witness['everyPrimaryExpected'] if role.startswith('per-row') else witness['anchorExpected']
                if title == 'PHASE32':
                    contract.update(rule='MOD32_FORMULA', prediction=[str(p) for p in range(32)])
                elif role.startswith('per-row'):
                    contract.update(rule='CONSTANT', prediction=str(value))
                elif title in ['RULER8_DELTA', 'RULER24_DELTA']:
                    contract.update(rule='BUILD_DELTA_MOD32', prediction=8 if title == 'RULER8_DELTA' else 24)
                else:
                    contract.update(rule='BUILD_EVENT_UNSPECIFIED' if value == 'UNSPECIFIED' else 'BUILD_EVENT', prediction=None if value == 'UNSPECIFIED' else str(value))
                contract['frozenWitness'] = witness
            elif title in ['SCALE_LOW', 'SCALE_HIGH']:
                contract.update(rule='CONSTANT', prediction='0' if title == 'SCALE_LOW' else '100')
            elif title in ['VISUAL_ANCHOR_INDEX', 'VISUAL_ANCHOR_TIME']:
                contract.update(rule='UNIQUE_BUILD_MARKER', prediction='Own index/time at A; blank elsewhere')
            elif title == 'STEP':
                contract.update(rule='MOD32_FORMULA', prediction=['75' if 8 <= p < 24 else '25' for p in range(32)])
            elif title in ['DIRECTION', 'SIGN', 'CONTROL_SIGN']:
                positive, negative = (12, 28) if title == 'CONTROL_SIGN' else (8, 24)
                contract.update(rule='MOD32_FORMULA', prediction=['1' if p == positive else '-1' if p == negative else '' for p in range(32)])
            elif title in ['UP_CONTROL', 'DOWN_CONTROL']:
                phase = 12 if title == 'UP_CONTROL' else 28
                contract.update(rule='BOOLEAN_EXPORT_POLICY', prediction=['1' if p == phase else '0' for p in range(32)], alternativeSparse=['1' if p == phase else '' for p in range(32)], note='Logical source values and native sparse visibility export are separate finite candidates; no pixel direction follows')
            contracts.append(contract)
        sources.append(dict(sourceId=asset['sourceId'], sourceSha256=asset['sha256'], contracts=contracts, frozenNumericWitnesses=asset['numericWitnesses']))
    return dict(version='v1', method='Frozen source/manifest contracts before native source attempts; no engine or observed-output fitting', sources=sources, primarySelection='A-31..A plus8 original A-39..A-32 predecessors', calibrationUncertaintyBeforeScoring=dict(axisXPx=2, axisYPx=3, strokeEdgePx=1, stepCombinedXPx=3), stepRule='Candidate intervals strictly disjoint or UNDECIDED; no relaxation', viewportPrerequisite=manifest['viewportPrerequisite'], missingOrOverlappingCandidates='UNDECIDED; no later viewport/settings/source rescue', buildEventScope='31 intentional blanks and one closed event; unspecified table state is observed without inventing an expected value')


if __name__ == '__main__':
    result = build()
    path = BASE/'numeric-contracts-v1.json'
    content = json.dumps(result, indent=2)+'\n'
    if path.exists():
        assert path.read_text() == content
    else:
        path.write_text(content)
    print(json.dumps(dict(sources=len(result['sources']), properties=sum(len(s['contracts']) for s in result['sources']))))
