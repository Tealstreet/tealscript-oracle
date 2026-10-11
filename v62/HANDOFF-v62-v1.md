# Oracle probe round v62 — capture handoff v1

Eight source-only indicator consumers, four natural/renamed-control pairs, one namespace-naming boundary group. All staged Pine sources and the producer packet/instructions are preserved byte-for-byte. Their filenames, probe identifiers and indicator titles still say v61: that was the requested round; they are published in v62 because v61 was already pushed. No captures or native predictions are bundled. Native outcomes are UNSPECIFIED until observed.

Run `sha256sum -c SHA256SUMS` from v62. The [bundle manifest](bundle-manifest-v1.json) records hashes, pairs and settings. The [producer packet](instructions/producer-ENTRY-v1.json) and [producer instructions](instructions/producer-INSTRUCTIONS-v1.md) preserve the original request. No library publication or external import is required. Prior v61 requests remain at [HANDOFF-v61-v1.md](../v61/HANDOFF-v61-v1.md).

## Questions and scope

Capture both Pine v5 and v6, for both distinct boundaries:

- A local variable of user-defined type Holder named `box`, calling its custom `readValue()` method, versus the otherwise matching variable named `holder`.
- An actual builtin box-handle parameter named `box`, calling receiver `get_top()` with no explicit ID argument, versus the parameter named `holder`.

Keep these boundaries separate from v59's UDT-parameter custom-dot refusal. Local declarations and actual drawing-handle receiver calls differ in type and scope; earlier outcomes do not predict these sources. The authority is boundary confirmation only, with no blocker for the already captured v59 scope. Do not rename, inline, add arguments or otherwise repair the sources during capture.

## Evidence and settings

Use BINANCE:BTCUSDT, 2m, chart display timezone Etc/UTC, default inputs. Record exact executed source/hash, all compiler diagnostic codes/text/line:column (code unavailable if not exposed), compiler/Save responses, screenshots and runtime errors/bar. Treat compile admission, execution and values as distinct observations. For admitted indicators export original CSV time/OHLC/Volume/RESULT after at least 32 closed bars; preserve numeric strings, missing cells and headers, record actual settings and confirmed closed-bar cutoff, and exclude the open bar. Compare each pair on identical closed physical rows. Preserve refusals and unavailable evidence instead of inferring values. No realtime or engine-derived native credit.

Return `v62/captures/v62/RESPONSE-v62.md`, an attempt inventory and integrity hashes, with one independent record per source. Identify unavailable context separately from a semantic refusal. Keep all raw evidence in this oracle repository.

## Paired source checklist

| Pair | Natural | Renamed control |
| --- | --- | --- |
| `box-handle-builtin-dot-v5` | [ns-param-naming-box-handle-builtin-dot-v5-natural-v61-v1.pine](ns-param-naming-box-handle-builtin-dot-v5-natural-v61-v1.pine) · [instructions](instructions/ns-param-naming-box-handle-builtin-dot-v5-natural-v61-v1-instructions-v1.md) | [ns-param-naming-box-handle-builtin-dot-v5-renamed-control-v61-v1.pine](ns-param-naming-box-handle-builtin-dot-v5-renamed-control-v61-v1.pine) · [instructions](instructions/ns-param-naming-box-handle-builtin-dot-v5-renamed-control-v61-v1-instructions-v1.md) |
| `box-handle-builtin-dot-v6` | [ns-param-naming-box-handle-builtin-dot-v6-natural-v61-v1.pine](ns-param-naming-box-handle-builtin-dot-v6-natural-v61-v1.pine) · [instructions](instructions/ns-param-naming-box-handle-builtin-dot-v6-natural-v61-v1-instructions-v1.md) | [ns-param-naming-box-handle-builtin-dot-v6-renamed-control-v61-v1.pine](ns-param-naming-box-handle-builtin-dot-v6-renamed-control-v61-v1.pine) · [instructions](instructions/ns-param-naming-box-handle-builtin-dot-v6-renamed-control-v61-v1-instructions-v1.md) |
| `local-udt-custom-dot-v5` | [ns-param-naming-local-udt-custom-dot-v5-natural-v61-v1.pine](ns-param-naming-local-udt-custom-dot-v5-natural-v61-v1.pine) · [instructions](instructions/ns-param-naming-local-udt-custom-dot-v5-natural-v61-v1-instructions-v1.md) | [ns-param-naming-local-udt-custom-dot-v5-renamed-control-v61-v1.pine](ns-param-naming-local-udt-custom-dot-v5-renamed-control-v61-v1.pine) · [instructions](instructions/ns-param-naming-local-udt-custom-dot-v5-renamed-control-v61-v1-instructions-v1.md) |
| `local-udt-custom-dot-v6` | [ns-param-naming-local-udt-custom-dot-v6-natural-v61-v1.pine](ns-param-naming-local-udt-custom-dot-v6-natural-v61-v1.pine) · [instructions](instructions/ns-param-naming-local-udt-custom-dot-v6-natural-v61-v1-instructions-v1.md) | [ns-param-naming-local-udt-custom-dot-v6-renamed-control-v61-v1.pine](ns-param-naming-local-udt-custom-dot-v6-renamed-control-v61-v1.pine) · [instructions](instructions/ns-param-naming-local-udt-custom-dot-v6-renamed-control-v61-v1-instructions-v1.md) |
