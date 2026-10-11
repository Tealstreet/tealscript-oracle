# Oracle probe round v70 — capture handoff v1

Eight source-only Pine v4 indicators (legacy study) in four direct-RHS/function-control pairs: bool, string, identifier and numeric. Preserve every source and instruction byte. Outcomes are UNSPECIFIED; producer candidate observations are questions, never native evidence. No library prerequisites.

Run `sha256sum -c SHA256SUMS` from v70. Use [bundle manifest](bundle-manifest-v1.json) and the unchanged [producer request](instructions/producer-PROBE-REQUEST-v1.json). Earlier [v69](../v69/HANDOFF-v69-v1.md) remains available.

Use BINANCE:BTCUSDT, ordinary candles, 2-minute bars, Etc/UTC, default inputs. Run each source independently in a fresh indicator tab. Record executed source/hash and exact compile phase, text, exposed code and line/column; unavailable codes remain unspecified. Preserve failed attempts and do not repair refused sources. If admitted, capture runtime diagnostics and export at least 32 closed bars with original CSV headers, numeric strings, missing cells, settings, exact cutoff and excluded open-bar timestamp. Plot(1) observes admission/execution, not tuple contents. Context unavailable is CONTEXT-UNMET. No realtime or tuple-content numeric credit.

| Probe | Source | Instructions |
| --- | --- | --- |
| `tuple-rhs-bool-v4-direct-be-v1` | [source](tuple-rhs-bool-v4-direct-be-v1.pine) | [instructions](instructions/tuple-rhs-bool-v4-direct-be-v1-instructions-v1.md) |
| `tuple-rhs-bool-v4-function-control-be-v1` | [source](tuple-rhs-bool-v4-function-control-be-v1.pine) | [instructions](instructions/tuple-rhs-bool-v4-function-control-be-v1-instructions-v1.md) |
| `tuple-rhs-string-v4-direct-be-v1` | [source](tuple-rhs-string-v4-direct-be-v1.pine) | [instructions](instructions/tuple-rhs-string-v4-direct-be-v1-instructions-v1.md) |
| `tuple-rhs-string-v4-function-control-be-v1` | [source](tuple-rhs-string-v4-function-control-be-v1.pine) | [instructions](instructions/tuple-rhs-string-v4-function-control-be-v1-instructions-v1.md) |
| `tuple-rhs-identifier-v4-direct-be-v1` | [source](tuple-rhs-identifier-v4-direct-be-v1.pine) | [instructions](instructions/tuple-rhs-identifier-v4-direct-be-v1-instructions-v1.md) |
| `tuple-rhs-identifier-v4-function-control-be-v1` | [source](tuple-rhs-identifier-v4-function-control-be-v1.pine) | [instructions](instructions/tuple-rhs-identifier-v4-function-control-be-v1-instructions-v1.md) |
| `tuple-rhs-numeric-v4-direct-be-v1` | [source](tuple-rhs-numeric-v4-direct-be-v1.pine) | [instructions](instructions/tuple-rhs-numeric-v4-direct-be-v1-instructions-v1.md) |
| `tuple-rhs-numeric-v4-function-control-be-v1` | [source](tuple-rhs-numeric-v4-function-control-be-v1.pine) | [instructions](instructions/tuple-rhs-numeric-v4-function-control-be-v1-instructions-v1.md) |

Return `v70/captures/v70/RESPONSE-v70.md`, attempt inventory, raw observations and integrity hashes. Keep direct tuple RHS and tuple-returning function controls distinct in the response; no general rule inferred beyond captured v4 shapes. Raw captures belong only in this oracle repository.
