# Oracle probe round v67 — capture handoff v1

Four indicator consumers and two library prerequisites: independent v5/v6 private ordinary-function namespace calls `lib.pick(3.5)` and exported `lib.forward(3.5)` controls. All six staged Pine sources, all four producer consumer instructions and the producer handoff are preserved byte-for-byte. No captures or native predictions are bundled. Every exact-source phase/value is UNSPECIFIED until observed.

Run `sha256sum -c SHA256SUMS` from v67. Follow the [bundle manifest](bundle-manifest-v1.json), [producer handoff](instructions/producer-HANDOFF-v1.json) and source instructions below. Earlier [v66 handoff](../v66/HANDOFF-v66-v1.md) and capture rounds remain available.

## Library prerequisites and binding

Compile/publish the exact v5 library as `sours-lat/PrivateFunctionQA5/1` and the exact v6 library as `sours-lat/PrivateFunctionQA6/1`. These contain a private ordinary function `pick` and an exported ordinary function `forward` that calls it. Do not export `pick`, turn it into a method or modify either source. Preserve source/hash, Pine version, library title, Save/compiler response, immutable owner/title/version, publication URL and access status.

If a requested immutable publication exists, authenticate source bytes/hash and version before reuse; never overwrite it. If the named identity is unavailable, the producer permits explicit import mapping: publish the same source unchanged under an available immutable identity and substitute only that import path in BOTH version-matched consumers. Preserve each executed source/hash and its import-only diff, plus the actual library source/hash/version and publication identity. No silent edits, inlining or version conversion. In particular, a v5 consumer must import a v5-published library: earlier v60 private visibility was masked by importing v6 from v5. If a matching-version library cannot be published/accessed, record the exact blocker as CONTEXT-UNMET; do not count it as a private-function refusal.

## Isolated namespace-call attempts

Run each exported-forward control independently before the corresponding private witness, on the same chart settings. Establish compilation/execution and library access with that control; never combine both calls in one source where a private refusal could hide the control. Preserve all outcomes separately. This question concerns namespace visibility of a private ordinary function. It supplies no receiver-method, transitive dependent-library or realtime credit, and earlier method visibility evidence does not predict the answer.

Use ordinary BINANCE:BTCUSDT candles, 2m, Etc/UTC chart display, default inputs. Preserve all compiler diagnostic owners, exact text/class/code when exposed (unavailable code stays unspecified), line/column, compiler responses, screenshots, executed source/SHA and compile/runtime status. Record runtime error message/site/bar separately from admission.

For running indicators export original native CSV with time/OHLC/Volume and RESULT after at least 32 closed bars. Preserve headers, numeric strings and missing cells; record actual setup, inputs, capture/export timestamps and confirmed cutoff. Separate/exclude open rows. Compare private/control on identical closed physical rows if both run. A failed control supplies no private visibility conclusion. No engine or screenshot-only numerical inference.

Return `v67/captures/v67/RESPONSE-v67.md`, an attempt inventory and integrity hashes. Keep independent source records, library publication records, explicit import mappings and unavailable outcomes. Raw evidence belongs in this oracle repository.

## Source checklist

- [private-function-library-v5-g6-v1.pine](private-function-library-v5-g6-v1.pine) — [library-prerequisite instructions](instructions/private-function-library-v5-g6-v1-instructions-v1.md); Pine v5, prerequisite.
- [private-function-library-v6-g6-v1.pine](private-function-library-v6-g6-v1.pine) — [library-prerequisite instructions](instructions/private-function-library-v6-g6-v1-instructions-v1.md); Pine v6, prerequisite.
- [private-function-namespace-exported-control-v5-g6-v1.pine](private-function-namespace-exported-control-v5-g6-v1.pine) — [consumer instructions](instructions/private-function-namespace-exported-control-v5-g6-v1-instructions-v1.md); Pine v5, exported-control.
- [private-function-namespace-exported-control-v6-g6-v1.pine](private-function-namespace-exported-control-v6-g6-v1.pine) — [consumer instructions](instructions/private-function-namespace-exported-control-v6-g6-v1-instructions-v1.md); Pine v6, exported-control.
- [private-function-namespace-private-v5-g6-v1.pine](private-function-namespace-private-v5-g6-v1.pine) — [consumer instructions](instructions/private-function-namespace-private-v5-g6-v1-instructions-v1.md); Pine v5, private.
- [private-function-namespace-private-v6-g6-v1.pine](private-function-namespace-private-v6-g6-v1.pine) — [consumer instructions](instructions/private-function-namespace-private-v6-g6-v1-instructions-v1.md); Pine v6, private.
