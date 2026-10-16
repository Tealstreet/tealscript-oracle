import hashlib
import json
import runpy
import sys
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]


def reference(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def write(path, data):
    if path.exists():
        assert path.read_text() == data, 'Immutable numeric artifact changed: ' + str(path)
    else:
        path.write_text(data)


def package(revision):
    analyze = runpy.run_path(str(BASE / 'analyze-evidence-v2.py'))['analyze']
    result = analyze(f'attempt-inventory-v{revision}.json', revision)
    index = []
    for source in result['sources']:
        path = BASE / source['sourceId'] / 'attempt-v1/numeric-results-v1.json'
        write(path, json.dumps(source, separators=(',', ':')) + '\n')
        summary = {k: v for k, v in source.items() if k != 'records'}
        summary['numericEvidence'] = reference(path)
        index.append(summary)
    result['sources'] = index
    write(BASE / f'numeric-controls-v{revision}.json', json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    result = package(int(sys.argv[1]))
    print(json.dumps({'version': result['version'], 'sourceReports': len(result['sources']), 'recordStorage': 'Immutable individual source artifacts referenced by the numeric index'}))
