# Oracle probe round v65 — capture handoff v1

Two source-only Pine v5 indicator programs: unused typed method declarations and unused untyped function declarations differing only by a legal literal optional parameter. Sources, per-source instructions and producer handoff are preserved byte-for-byte. Original filenames/probe identifiers still say v61; v65 is the publication round. No captures or native predictions are bundled. Native phase and values remain UNSPECIFIED until observed.

Run `sha256sum -c SHA256SUMS` from v65. The [bundle manifest](bundle-manifest-v1.json) identifies source hashes and settings. The unchanged [producer handoff](instructions/producer-HANDOFF-v1.json) records original absolute intake paths as provenance; use this round's relative source/instruction links. No external imports or library publication are required.

## Questions and scope

Does Pine v5 reject each pair of unused declarations as sharing required parameters, or admit the exact script? v60 already answered the typed ordinary-function counterpart; this round changes the callable/annotation shape. Keep the typed-method and untyped-function outcomes separate. Compile each exact source without edits. Do not add an invocation, change default values, annotate the untyped parameters, rename declarations or publish a library. This request does not infer a general overload rule or realtime behavior.

## Evidence and settings

Use BINANCE:BTCUSDT, 2m, chart display timezone Etc/UTC, default inputs. Preserve executed source/SHA and version, native compilation/Save response, all diagnostic messages/code if exposed and line:column positions, screenshot, actual setup and inputs. Record refused compilation even if no CSV exists; mark codes unavailable when not exposed. Distinguish compile admission, runtime error/bar and plotted values.

If admitted and running, export original native CSV with time/OHLC/Volume and VALUE after at least 32 closed bars. Preserve headers, numeric strings and missing cells; record the last closed-bar cutoff and separate/exclude the open row. Context unavailable is CONTEXT-UNMET, not semantic refusal. Engine output never substitutes for native evidence.

Return `v65/captures/v65/RESPONSE-v65.md`, an attempt inventory and integrity hashes, with an independent record per source. Earlier [v64](../v64/HANDOFF-v64-v1.md) and other round requests/captures remain available. Raw capture evidence belongs in this oracle repository.

## Source checklist

- [v61-v5-optional-only-typed-method-declaration-g6-v1.pine](v61-v5-optional-only-typed-method-declaration-g6-v1.pine) — [instructions](instructions/v61-v5-optional-only-typed-method-declaration-g6-v1-instructions-v1.md); v5 optional-only typed-method declaration identity: do unused declarations sharing required parameters refuse or admit?
- [v61-v5-optional-only-untyped-function-declaration-g6-v1.pine](v61-v5-optional-only-untyped-function-declaration-g6-v1.pine) — [instructions](instructions/v61-v5-optional-only-untyped-function-declaration-g6-v1-instructions-v1.md); v5 optional-only untyped-function declaration identity: do unused declarations sharing required parameters refuse or admit?
