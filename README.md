# TealScript native oracle archive

Public capture requests, Pine source, TradingView observations, exports and evidence used to investigate TealScript parity. This repository is separate from the application and the public [tealchart source mirror](https://github.com/Tealstreet/tealchart).

See [MIGRATION.md](MIGRATION.md) for the application cutover, verification and other-agent handoff.

## Capture and handoff

The v85 request is [v85/HANDOFF-v85-v1.md](v85/HANDOFF-v85-v1.md): eight exact advisory-presence exceptions/companions/controls, five private Save/Add compiles each; compiler response presence is recorded independently of editor markers.

The v84 request is [v84/HANDOFF-v84-v1.md](v84/HANDOFF-v84-v1.md): fifteen exact parse-refusal/advisory representatives, five private Save/Add compiles each, with unspecified native marker order and separate compiler/editor evidence.

Create requests and commit capture responses here on `master`. Run the exact sources and settings in each round’s handoff. Preserve source bytes, CSV headers, numeric strings, missing cells, compile/runtime diagnostics and source/capture hashes. Record refusals and unavailable observations; never replace a TradingView observation with engine output. Historical documents contain their original monorepo paths: `packages/tealscript/oracle-probes/` maps to this repository’s root. Historical `/Users/sam/` and `/home/sam/` intake paths record where work originated; they are not downloadable dependencies.

The newest v72 request is [v72/HANDOFF-v72-v1.md](v72/HANDOFF-v72-v1.md), with custom TA boundary questions. The v71 request remains at [v71/HANDOFF-v71-v1.md](v71/HANDOFF-v71-v1.md). The v70 request remains at [v70/HANDOFF-v70-v1.md](v70/HANDOFF-v70-v1.md). The v69 request remains at [v69/HANDOFF-v69-v1.md](v69/HANDOFF-v69-v1.md). The v68 request remains at [v68/HANDOFF-v68-v1.md](v68/HANDOFF-v68-v1.md). The v67 private-function request remains at [v67/HANDOFF-v67-v1.md](v67/HANDOFF-v67-v1.md). The v66 local UDT request remains at [v66/HANDOFF-v66-v1.md](v66/HANDOFF-v66-v1.md). The v65 declaration request remains at [v65/HANDOFF-v65-v1.md](v65/HANDOFF-v65-v1.md). The v64 collection reassignment request remains at [v64/HANDOFF-v64-v1.md](v64/HANDOFF-v64-v1.md). The v63 custom-TA request remains at [v63/HANDOFF-v63-v1.md](v63/HANDOFF-v63-v1.md). The v62 namespace-naming request remains at [v62/HANDOFF-v62-v1.md](v62/HANDOFF-v62-v1.md). The earlier v61 request remains at [v61/HANDOFF-v61-v1.md](v61/HANDOFF-v61-v1.md). Earlier responses are [v59](v59/captures/v59/RESPONSE-v59.md) and [v60](v60/captures/v60/RESPONSE-v60.md). The v58 intake and engine candidates are in [v58/AGENT-RESPONSE-v1.md](v58/AGENT-RESPONSE-v1.md). Previous capture status and agent responses are in [CAPTURE-RESPONSE.md](CAPTURE-RESPONSE.md). The round handoff owns required evidence and settings; a successful compile alone does not certify parity.

## Application tests

The application pins an immutable commit and selects the files its tests consume. Application and mobile builds do not vendor this archive. A capture commit here does not trigger application deployments. Promote a reviewed observation by updating the application’s fixture lock and its assertions; do not automatically advance a pin to `master`.

For archive research, use a shallow clone:

```sh
git clone --depth 1 https://github.com/Tealstreet/tealscript-oracle.git
```

## Provenance and rights

[migration-manifest.json](migration-manifest.json) records every file imported from the monorepo snapshot, including original path, byte length and SHA-256. Existing files are preserved byte-for-byte; no private Git history is imported. `node scripts/verify-migration.mjs` checks the imported snapshot locally.

There is no blanket license for this corpus. Original Pine source license and attribution notices remain in their files, including MIT, Apache, MPL, GPL and Creative Commons notices. TradingView screenshots, market-data exports and third-party source retain their respective rights and provider terms; publication here does not grant additional rights. New contributed capture tooling must state its license separately.

Old monorepo and mirror histories still contain the former archive. This migration removes it from new application trees and prevents future capture growth there; it does not rewrite those histories.
