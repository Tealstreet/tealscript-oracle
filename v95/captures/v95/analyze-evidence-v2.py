import json
import runpy
from pathlib import Path

BASE = Path(__file__).resolve().parent


def analyze(inventory_name, revision):
    module = runpy.run_path(str(BASE / 'analyze-evidence-v1.py'))
    result = module['analyze'](inventory_name, revision)
    for report in result['sources']:
        path = BASE / report['sourceId'] / 'attempt-v1/runtime-observation-v1.json'
        if not path.exists():
            continue
        native = json.loads(path.read_text())
        report['nativeRuntimeObservation'] = module['reference'](path)
        report['captureStatus'] = 'ORIGINAL CSV CAPTURED / NATIVE RUNTIME ERROR / NUMERIC EXECUTION CONTEXT NOT OBSERVED'
        report['facets'].append({'facet': 'Native runtime admission', 'captureStatus': 'CAPTURED', 'hypothesisVerdict': 'UNDECIDED', 'cause': 'Native UI reports runtime error ' + ','.join(native['nativeRuntimeCodes']) + '; no numeric match or source-origin reconstruction credited', 'details': native})
    return result
