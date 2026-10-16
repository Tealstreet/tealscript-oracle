import json
import runpy
from pathlib import Path


def analyze(limit=6):
    result = runpy.run_path(str(Path(__file__).with_name('analyze-evidence-v1.py')))['analyze'](limit)
    result['version'] = 'v2'
    for source in result['sources']:
        if 'discriminators' not in source['sourceId']:
            continue
        source['perGradientModelVerdicts'] = {}
        for group in ['PARTIAL', 'TRANSPARENT_LOWER', 'OPAQUE']:
            source['perGradientModelVerdicts'][group] = {}
            for model in ['S', 'P']:
                properties = [p for p in source['propertyVerdicts'] if p['model'] == model and p['property'] in [group + '_' + c for c in ['R', 'G', 'B', 'T', 'NA']]]
                assert len(properties) == 5
                source['perGradientModelVerdicts'][group][model] = {'captureStatus': 'CAPTURED', 'verdict': 'REFUTED' if any(p['verdict'] == 'REFUTED' for p in properties) else 'SUPPORTED', 'contraryCellComparisons': sum(p['counts'].get('REFUTED', 0) for p in properties), 'scope': 'This one gradient over the selected 32 closed rows; opaque agreement does not discriminate families.'}
    return result


if __name__ == '__main__':
    result = analyze()
    print(json.dumps({r['sourceId']: {'coverage': r['coverage'], 'models': r['modelVerdicts']} for r in result['sources']}, indent=2))
