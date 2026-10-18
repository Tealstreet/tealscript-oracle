import hashlib
import json
import re
import runpy
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
split_arguments = runpy.run_path(str(ROOT / 'v102/captures/v102/audit-request-v1.py'))['split_arguments']


def audit():
    manifest = json.loads((ROOT / 'v103/bundle-manifest-v1.json').read_text())
    matrix = json.loads((ROOT / 'v103/CASE-MATRIX-v1.json').read_text())
    cases = {c['sourceId']: c for c in matrix['sourceCases']}
    assert len(manifest['sources']) == len(cases) == 29
    checksums = []
    for line in (ROOT / 'v103/SHA256SUMS').read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        name = name.lstrip('*')
        raw = (ROOT / 'v103' / name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == digest, name
        checksums.append(dict(path='v103/' + name, sha256=digest, bytes=len(raw)))
    sources = []
    for asset in manifest['sources']:
        raw = (ROOT / asset['path']).read_bytes()
        assert len(raw) == asset['bytes'] and hashlib.sha256(raw).hexdigest() == asset['sha256']
        source = raw.decode()
        titles = []
        for line in source.splitlines():
            match = re.search(r'\bplot(?:shape|char|arrow)?\(', line)
            if match:
                arguments = split_arguments(line[match.end():])
                title = next((a.split('=', 1)[1].strip() for a in arguments if re.match(r'^title\s*=', a)), arguments[1])
                titles.append(json.loads(title))
        assert titles == [p['title'] for p in asset['plots']]
        assert len(set(titles)) == asset['plotCalls']
        assert cases[asset['sourceId']]['sourceSha256'] == asset['sha256']
        assert cases[asset['sourceId']]['visualFacets'] == asset['visualFacets']
        assert cases[asset['sourceId']]['numericWitnesses'] == asset['numericWitnesses']
        assert not re.search(r'^\s*import\s|\brequest\.|\balert\(|\bstrategy\(', source, re.M)
        assert 'build = barstate.islastconfirmedhistory and na(anchorIndex) and bar_index >= 240' in source
        assert source.count('anchorIndex := bar_index') == source.count('anchorTime := time') == 1
        sources.append(dict(slot=asset['slot'], sourceId=asset['sourceId'], bytes=len(raw), sha256=asset['sha256'], plots=titles, visualFacets=len(asset['visualFacets'])))
    assert sum(len(s['plots']) for s in sources) == 300
    assert sum(s['visualFacets'] for s in sources) == 88
    return dict(version='v1', status='PASS', requestCommit='1e7fb20eb7f52ef024c9b7df0e4293faee485237', checksumEntries=checksums, sources=sources, totalPlotColumns=300, prospectivePrimaryCells=9600, nativeOutcome='UNSPECIFIED; frozen models are hypotheses, not native observations')


if __name__ == '__main__':
    result = audit()
    path = BASE / 'environment-v1/request-audit-v1.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(result, indent=2) + '\n'
    if path.exists():
        assert path.read_text() == content
    else:
        path.write_text(content)
    print(json.dumps(dict(status=result['status'], sources=len(result['sources']), checksumEntries=len(result['checksumEntries']), visualFacets=88, totalPlotColumns=300)))
