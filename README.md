# TealScript native oracle archive

Public capture requests, Pine source, TradingView observations, exports and evidence used to investigate TealScript parity. This repository is separate from the application and the public [tealchart source mirror](https://github.com/Tealstreet/tealchart).

## Capture and handoff

Create requests and commit capture responses here on `master`. Run the exact sources and settings in each round’s handoff. Preserve source bytes, CSV headers, numeric strings, missing cells, compile/runtime diagnostics and source/capture hashes. Record refusals and unavailable observations; never replace a TradingView observation with engine output. Historical documents contain their original monorepo paths: `packages/tealscript/oracle-probes/` maps to this repository’s root. Historical `/Users/sam/` and `/home/sam/` intake paths record where work originated; they are not downloadable dependencies.

The outstanding v58 request is [v58/HANDOFF-v58-v1.md](v58/HANDOFF-v58-v1.md). Previous capture status and agent responses are in [CAPTURE-RESPONSE.md](CAPTURE-RESPONSE.md). The round handoff owns required evidence and settings; a successful compile alone does not certify parity.

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
