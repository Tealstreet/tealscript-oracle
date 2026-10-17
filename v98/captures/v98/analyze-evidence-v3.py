import runpy
from pathlib import Path

BASE=Path(__file__).resolve().parent
PREVIOUS=runpy.run_path(str(BASE/'analyze-evidence-v2.py'))


def analyze(revision=1):
    result=PREVIOUS['analyze'](revision)
    for report in result['sources']:
        if report['nativeCompileSuccess'] is None:
            report['admissionObserved']=False
            report['captureStatus']='NOT OBSERVED; entry stopped before native Save/Add'
    return result
