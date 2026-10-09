// SPDX-License-Identifier: MIT
import { createReadStream } from 'node:fs';
import { readFile, stat } from 'node:fs/promises';
import { createHash } from 'node:crypto';

const root = new URL('../', import.meta.url);
const manifest = JSON.parse(await readFile(new URL('migration-manifest.json', root), 'utf8'));
let bytes = 0;
for (const entry of manifest.files) {
  if (entry.path.startsWith('/') || entry.path.split('/').includes('..')) throw new Error(`Invalid path: ${entry.path}`);
  const file = new URL(entry.path, root);
  const info = await stat(file);
  if (info.size !== entry.bytes) throw new Error(`Byte length changed: ${entry.path}`);
  const hash = createHash('sha256');
  for await (const chunk of createReadStream(file)) hash.update(chunk);
  if (hash.digest('hex') !== entry.sha256) throw new Error(`SHA-256 changed: ${entry.path}`);
  bytes += info.size;
}
console.log(`Verified ${manifest.files.length} imported files, ${bytes} bytes.`);
