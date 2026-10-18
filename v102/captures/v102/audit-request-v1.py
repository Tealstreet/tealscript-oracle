import hashlib
import json
import re
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]


def split_arguments(text):
    parts, start, depth, quote, escaped = [], 0, 0, None, False
    for i, char in enumerate(text):
        if quote:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == quote:
                quote = None
        elif char in ['"', "'"]:
            quote = char
        elif char in '([{':
            depth += 1
        elif char in ')]}':
            depth -= 1
            if depth < 0:
                parts.append(text[start:i].strip())
                return parts
        elif char == ',' and depth == 0:
            parts.append(text[start:i].strip())
            start = i + 1
    raise AssertionError('Unclosed plot arguments')


def plot_titles(source):
    titles = []
    for line in source.splitlines():
        match = re.search(r'\bplot\(', line)
        if not match:
            continue
        arguments = split_arguments(line[match.end():])
        named = next((a.split('=', 1)[1].strip() for a in arguments if re.match(r'^title\s*=', a)), None)
        titles.append(json.loads(named if named is not None else arguments[1]))
    return titles


def audit():
    manifest = json.loads((ROOT / 'v102/bundle-manifest-v1.json').read_text())
    matrix = json.loads((ROOT / 'v102/CASE-MATRIX-v1.json').read_text())
    cases = {c['sourceId']:c for c in matrix['cases']}
    assert len(manifest['sources']) == len(cases) == 25
    sources = []
    for asset in manifest['sources']:
        raw = (ROOT / asset['path']).read_bytes()
        assert len(raw) == asset['bytes'] and hashlib.sha256(raw).hexdigest() == asset['sha256']
        source = raw.decode()
        titles = plot_titles(source)
        assert titles == [p['title'] for p in asset['plots']] and len(set(titles)) == asset['plotCalls']
        assert not re.search(r'^\s*import\s|\brequest\.|\balert\(|\bstrategy\(', source, re.M)
        assert asset['caseIds'] == [asset['sourceId'] + ':' + c for c in cases[asset['sourceId']]['cases']]
        sources.append(dict(slot=asset['slot'], sourceId=asset['sourceId'], bytes=len(raw), sha256=asset['sha256'], plots=titles))
    assert sum(len(s['plots']) for s in sources) == 349
    prior = []
    for entry in manifest['priorEvidence']:
        path = ROOT / entry['path']
        method = 'Filesystem immutable dependency' if path.exists() else 'git cat-file blob HEAD:<path>; sparse checkout omits the working file'
        raw = path.read_bytes() if path.exists() else subprocess.check_output(['git', 'cat-file', 'blob', 'HEAD:' + entry['path']], cwd=ROOT)
        assert len(raw) == entry['bytes'] and hashlib.sha256(raw).hexdigest() == entry['sha256'], entry['path']
        prior.append(dict(**entry, readMethod=method))
    return dict(version='v1', status='PASS', requestCommit='b45ff69a64466b40c0ee13419176c4de9a6a6f7d', sources=sources, priorEvidence=prior, totalSourcePlotColumns=349, prospectivePrimaryCells=11168, sourceOutcomes='UNSPECIFIED; frozen author hypotheses never replace native targets')


if __name__ == '__main__':
    value = audit()
    path = BASE / 'environment-v1/request-audit-v1.json'
    content = json.dumps(value, indent=2) + '\n'
    if path.exists():
        assert path.read_text() == content
    else:
        path.write_text(content)
    print(json.dumps(dict(status=value['status'], sources=len(value['sources']), priorDependencies=len(value['priorEvidence']), totalSourcePlotColumns=value['totalSourcePlotColumns'])))
