from pathlib import Path
import argparse, hashlib, json, re
parser = argparse.ArgumentParser()
parser.add_argument('--publisher', required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
assert re.fullmatch(r'[A-Za-z0-9_-]+', args.publisher), 'Use the exact publisher username'
packet = Path(__file__).resolve().parent
entry = json.loads((packet / 'instructions/ENTRY-v1.json').read_text())
args.output.mkdir(parents=True, exist_ok=False)
rows = []
for source in entry['sources']:
    if not source.get('requiresPublicationBinding'):
        continue
    raw = (packet / Path(source['path']).name).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == source['sourceSha256']
    assert raw.count(b'__PUBLISHER__') == 1
    bound = raw.replace(b'__PUBLISHER__', args.publisher.encode())
    path = args.output / Path(source['path']).name
    path.write_bytes(bound)
    rows.append({'probe': source['probe'], 'path': path.name,
                 'templateSha256': source['sourceSha256'],
                 'executedSourceSha256': hashlib.sha256(bound).hexdigest(),
                 'nativeStatus': 'UNOBSERVED'})
(args.output / 'BOUND-SOURCES-v1.json').write_text(json.dumps(
    {'version': 'v1', 'publisher': args.publisher,
     'import': args.publisher + '/P425PrivateV79v1/1',
     'publicationVerificationRequired': True, 'sources': rows}, indent=2) + '\n')
