# Oracle archive migration

Capture requests, native observations, raw exports, screenshots and capture-agent responses now belong in `Tealstreet/tealscript-oracle` on `master`. The application cutover is [tealstreet-next commit 58db566](https://github.com/Tealstreet/tealstreet-next/commit/58db566f513784917bde9861f9a683ea69c5b3c4). The [portable setup fix](https://github.com/Tealstreet/tealstreet-next/commit/75550b21f0bccfff35e0c6345e06a55ba36f9710) also makes direct CLI invocation through symlink paths execute normally. Author engine fixes and regression assertions in the application/source mirror; author new probes and capture results here. Copybara still owns the engine/source mirror and does not synchronize this archive.

## Preserved evidence

The import snapshot is [8425039](https://github.com/Tealstreet/tealscript-oracle/tree/8425039c3539ac14152e305ee4b627128efc2551): 20,553 original files, 5,540,068,844 bytes, all verified byte-for-byte against the migration manifest. The application deletion set exactly matches that inventory. Sources, capture manifests, compile/runtime errors, screenshots and existing responses were not reinterpreted or regenerated. No private monorepo history was imported and no existing repository history was rewritten.

Historical `packages/tealscript/oracle-probes/` paths resolve from this repository root. Historical absolute intake paths are provenance rather than required dependencies. Retain original per-file attribution and license notices.

## Application test inputs

The application fixture lock pins the import snapshot and 79 exact files totaling 317,971,889 bytes. Those files include 24 full CSV exports, 51 Pine sources, three JSON manifests/outcomes and one diagnostic text file. Full histories and hashes remain intact; assertions are unchanged. Screenshots and unused exports stay here.

Run `yarn oracle:fetch` and `yarn oracle:verify` from the application’s `packages/tealscript` directory. The checkout is local, sparse, detached and gitignored. Both CI workflows perform explicit acquisition and SHA verification before tests. Missing fixtures raise a setup error, and tracked captures are refused. No fetch runs during application install/build; fixture-lock and capture-tool changes do not change Vercel runtime fingerprints.

To promote evidence, commit it here, review the exact source/settings/native observation, then update the application’s immutable fixture revision, selected hashes and corresponding assertions together. Never float the application pin to archive `master`, replace native expected values with engine output, or copy the full archive into application source. To recheck the original import after later capture edits, use a separate checkout of the import snapshot and run `node scripts/verify-migration.mjs` there.

## Capture handoff

The [v58 request](v58/HANDOFF-v58-v1.md) is preserved and remains pending. This migration performed no new TradingView captures or library publications. Its 449 Pine assets and request hashes are unchanged. Follow that handoff’s exact prerequisite, import-binding and evidence requirements when capturing. Previous v49–v56 receipts and agent responses remain available in [CAPTURE-RESPONSE.md](CAPTURE-RESPONSE.md) and their round directories.

Commit future inter-agent capture responses next to the relevant handoff here, then push archive `master`. Do not add requests/results back to the application’s ignored test checkout.

## Verification

The public sparse fetch verified all 79 fixture hashes and lengths, including a fresh checkout after archive `master` advanced beyond the pinned commit. Package typecheck and scoped lint passed. Fourteen fixture-tool tests and 27 deployment-selector tests passed, including proved-failed corruption, checkout-identity and deployment-selection regressions. Ten existing native test files passed all 118 tests across full-history CSVs, manifests/outcomes, text diagnostics and dynamic paths. The deletion inventory and integration were independently reviewed by sub-agents. Full application suites remain CI’s gate.

New application trees exclude 5.54 GB of archive evidence. Selected test data is about 94% smaller than the complete archive. Old application and mirror histories still retain previous objects; vendored source clones must remain shallow. Docker/EAS and both mirror-direction exclusions remain in place.
