import hashlib
import json
import re
import runpy
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
split_arguments = runpy.run_path(str(ROOT/'v102/captures/v102/audit-request-v1.py'))['split_arguments']


def audit():
    manifest = json.loads((ROOT/'v104/bundle-manifest-v1.json').read_text())
    matrix = json.loads((ROOT/'v104/CASE-MATRIX-v1.json').read_text())
    facets = {f['facetId']: f for f in matrix['facets']}
    assert len(manifest['entries']) == len(facets) == 13
    checksums = []
    for line in (ROOT/'v104/SHA256SUMS').read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        name = name.lstrip('*')
        raw = (ROOT/'v104'/name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == digest, name
        checksums.append(dict(path='v104/'+name, sha256=digest, bytes=len(raw)))
    sources = []
    versions = {5: 0, 6: 0}
    for asset in manifest['entries']:
        raw = (ROOT/asset['path']).read_bytes()
        assert len(raw) == asset['bytes'] and hashlib.sha256(raw).hexdigest() == asset['sha256']
        source = raw.decode()
        plots = []
        for line in source.splitlines():
            match = re.search(r'\b(plot(?:shape|char|arrow)?)\(', line)
            if match:
                args = split_arguments(line[match.end():])
                title = next((a.split('=', 1)[1].strip() for a in args if re.match(r'^title\s*=', a)), args[1])
                plots.append(dict(sourcePlotOrdinal=len(plots), function=match[1], title=json.loads(title)))
        assert plots == asset['plots']
        assert len({p['title'] for p in plots}) == asset['plotCalls']
        assert re.search(r'indicator\("([^"]+)"', source)[1] == asset['indicatorTitle']
        assert not re.search(r'^\s*import\s|\brequest\.|\balert\(|\bstrategy\(', source, re.M)
        assert 'build = barstate.islastconfirmedhistory and na(anchorIndex) and bar_index >= 240' in source
        assert source.count('anchorIndex := bar_index') == 1
        assert 'plot(build ? time : na, "VISUAL_ANCHOR_TIME"' in source
        for line in source.splitlines():
            if re.search(r'\b(?:box|label|line|table)\.(?:new|copy|set_\w+|merge_cells|cell|delete)\(', line):
                assert line.startswith('    '), line
        assert len(asset['visualFacets']) == 1
        for facet in asset['visualFacets']:
            assert facets.pop(facet['facetId']) == facet
        versions[asset['pineVersion']] += 1
        sources.append(dict(slot=asset['slot'], sourceId=asset['sourceId'], bytes=len(raw), sha256=asset['sha256'], plots=plots))
    assert not facets and versions == {5: 8, 6: 5}
    assert sum(len(s['plots']) for s in sources) == 144
    return dict(version='v1', status='PASS', requestCommit='c9a226074c15cbaea93381d27aaa0e406f14e108', checksumEntries=checksums, sources=sources, totalPlotColumns=144, prospectivePrimaryCells=4608, nativeOutcome='UNSPECIFIED; source hypotheses do not supply native targets')


if __name__ == '__main__':
    result = audit()
    path = BASE/'environment-v1/request-audit-v1.json'
    content = json.dumps(result, indent=2)+'\n'
    if path.exists():
        assert path.read_text() == content
    else:
        path.write_text(content)
    print(json.dumps(dict(status='PASS', sources=len(result['sources']), checksumEntries=len(result['checksumEntries']), totalPlotColumns=144)))
