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


def write(path, value):
    data = json.dumps(value, indent=2) + '\n'
    if path.exists():
        assert path.read_text() == data, str(path)
    else:
        path.write_text(data)


def package_numeric(revision, closed_revision):
    previous = json.loads((BASE / f'numeric-controls-v{closed_revision}.json').read_text())
    analyze = runpy.run_path(str(BASE / 'analyze-observer-v1.py'))['analyze']
    assets = json.loads((ROOT / 'v95/bundle-manifest-v1.json').read_text())['sources']
    sources = list(previous['sources'])
    for asset in assets[38:]:
        result = analyze(asset['id'])
        path = BASE / asset['id'] / 'attempt-v1/numeric-results-v1.json'
        raw = json.dumps(result, separators=(',', ':')) + '\n'
        if path.exists():
            assert path.read_text() == raw
        else:
            path.write_text(raw)
        summary = {k: v for k, v in result.items() if k != 'records'}
        summary['numericEvidence'] = reference(path)
        sources.append(summary)
    index = {**previous, 'version': f'v{revision}', 'inventory': f'attempt-inventory-v{revision}.json', 'sources': sources, 'policy': previous['policy'] + ' Both item20 sources use their one bounded unchanged-source observer windows. Live/close/next tuples and repeated history receive no CLOSED credit; only the first export supplies the closed baseline. Native calculation-session IDs and intervening event completeness remain unobserved.'}
    write(BASE / f'numeric-controls-v{revision}.json', index)
    return index


def compiler_diagnostics(inventory):
    result = []
    for attempt in inventory['attempts']:
        source = attempt['source']
        directory = (ROOT / source['receipt']['path']).parent
        transports = []
        for kind in ['saveBody', 'addBody']:
            if source[kind] is None:
                continue
            body = json.loads((ROOT / source[kind]['path']).read_text())
            meta = (body.get('result') or {}).get('metaInfo', {})
            reason = body.get('reason2')
            transports.append({'kind': kind, 'body': source[kind], 'nativeSuccess': body.get('success'), 'nativeReason': body.get('reason'), 'nativeReason2': reason, 'nativeStructuredErrors': reason.get('errors') if isinstance(reason, dict) else None, 'structuredErrorChannelStatus': 'EXPOSED' if isinstance(reason, dict) and 'errors' in reason else 'UNOBSERVED / no independent structured error array exposed', 'nativeWarnings': meta.get('warnings'), 'warningChannelStatus': 'EXPOSED' if 'warnings' in meta else 'UNOBSERVED', 'nativeEditorMarkerArrays': None, 'nativeEditorMarkerArrayStatus': 'UNOBSERVED; raw immediate/settled UI retained separately'})
        path = directory / 'compiler-diagnostics-v1.json'
        write(path, {'version': 'v1', 'sourceId': source['sourceId'], 'sourceSha256': source['sourceSha256'], 'transports': transports})
        result.append({'sourceId': source['sourceId'], 'path': str(path.relative_to(ROOT)), 'transports': transports})
    return result


def package_round(revision, closed_revision, response_path):
    inventory = json.loads((BASE / f'attempt-inventory-v{revision}.json').read_text())
    assert len(inventory['attempts']) == 40
    numeric = package_numeric(revision, closed_revision)
    diagnostics = compiler_diagnostics(inventory)
    receipts = [json.loads((ROOT / a['source']['receipt']['path']).read_text()) for a in inventory['attempts']]
    observers = [r.get('observer') for r in receipts[38:]]
    write(BASE / f'facet-capabilities-v{revision}.json', {'version': f'v{revision}', 'status': 'All40 finite source slots returned with explicit property-specific native outcomes and holds', 'sources': numeric['sources'], 'compilerDiagnostics': diagnostics, 'residualHolds': {'ownPrefix': 'Each property retains its actual own-prefix/dependency guard; no missing input rows reconstructed', 'nativeInstanceIdsAndEditorArrays': 'UNOBSERVED; independent source/private-version, metadata, native UI and download evidence retained', 'oldMtfDevelopingIdentity': 'DEFERRED / unchanged', 'samplingCompleteness': 'NOT CLAIMED', 'nativeCalculationSessionCount': 'UNOBSERVED; one unchanged source/version/settings session requested per source, potential export rebuilds independently recorded', 'engineParityAndOldHolds': 'NO APPROVAL / UNCHANGED'}})
    write(BASE / f'account-actions-v{revision}.json', {'version': f'v{revision}', 'status': 'Finite40-source round returned including explicit capability/runtime holds', 'newLayout': {'nativeId': 208224726, 'image': 'q38mQ4Nz', 'name': 'oracle-v95-v1', 'pageId': 7}, 'sourceSlots': 40, 'nativeSaveAttempts': sum(a['source']['saveBody'] is not None for a in inventory['attempts']), 'nativeAddAttempts': sum(a['source']['addBody'] is not None for a in inventory['attempts']), 'closedSourceOriginalCsvs': sum(len(a['sessions']) for a in inventory['attempts'][:38]), 'observerDownloadAttemptSlots': sum(o['exports'] for o in observers if o), 'observerInspectedOriginalCsvs': sum(len(o['sampleInspections']) for o in observers if o), 'includedOwnStudiesRemoved': sum(bool(r.get('removed')) for r in receipts), 'sourceRetries': 0, 'inputChanges': 0, 'builtinVolume': 'Default Vol · BTC retained unchanged', 'maximumBudget': {'saves': 40, 'adds': 40, 'csvs': 50, 'observerWindowsPerVersion': 1, 'observerCsvsPerVersion': 6}, 'existingLayoutPreservation': 'v95/captures/v95/environment-v2/existing-layout-comparison-v1.json', 'newLayoutSavedAfterCleanup': True, 'privateLibrary': 'sours-lat/P425PrivateV79v1/1 unchanged; no action', 'P425Layout': 'Name not exposed in full native list; no action', 'forbiddenActionsTaken': [], 'observerSourceSettingsSessions': [o['sourceSessions'] if o else 0 for o in observers], 'actualNativeCalculationSessionCounts': [None, None], 'engineChangesOrFixturePromotion': False})
    path = BASE / f'RESPONSE-v95-v{revision}.md'
    assert not path.exists()
    path.write_bytes(Path(response_path).read_bytes())
    result = runpy.run_path(str(BASE / 'validate-evidence-v4.py'))['validate'](revision, closed_revision, False)
    write(BASE / f'validation-result-v{revision}.json', result)
    files = [p for p in (ROOT / 'v95').rglob('*') if p.is_file() and not p.name.startswith('.') and '__pycache__' not in p.parts and p != BASE / f'artifact-integrity-v{revision}.json']
    write(BASE / f'artifact-integrity-v{revision}.json', {'version': f'v{revision}', 'scope': 'All request/frozen source and returned v95 artifacts, every original compiler body/export/UI frame, native admission/runtime and observer evidence, standalone derived analysis/validators, both environment baselines and all prior immutable returns. This manifest self-excludes.', 'files': [reference(p) for p in sorted(files)]})
    Path(f'/tmp/oracle-v95-return-paths-v{revision}.txt').write_text('\n'.join([str(p.relative_to(ROOT)) for p in sorted(files) if '/captures/' in str(p.relative_to(ROOT))] + [f'v95/captures/v95/artifact-integrity-v{revision}.json']) + '\n')
    return result


if __name__ == '__main__':
    print(json.dumps(package_round(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]), indent=2))
