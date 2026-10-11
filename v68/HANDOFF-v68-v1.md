# Oracle probe round v68 — capture handoff v1

Four source-only indicator consumers in two Pine v5/v6 natural/control pairs. Each natural declares a receiver-only UDT method that does not use its receiver; each control reads the receiver field. No further parameters are declared. Sources, per-source instructions and producer request are preserved byte-for-byte. The staging directory `v61-probes-v1` is historical provenance; v68 is the publication round. No captures or native predictions are bundled. Exact-source phase and values remain UNSPECIFIED until observed.

Run `sha256sum -c SHA256SUMS` from v68. Use the [bundle manifest](bundle-manifest-v1.json), unchanged [producer request](instructions/producer-PROBE-REQUEST-v1.json) and per-source instructions below. Historical absolute paths are provenance rather than downloadable dependencies; use the bundled relative paths. No imported library or publication prerequisite exists. Earlier [v67 handoff](../v67/HANDOFF-v67-v1.md) and other rounds remain available.

## Questions and scope

Does each receiver-only method admit and run, refuse at declaration, or error at runtime? Capture both versions and both pair members independently. V60 unused-receiver refusals with further parameters do not establish outcomes for these zero-further-parameter forms. The producer's Plot12 is only a candidate answer; preserve any other native readout. Do not add parameters, change method bodies or repair refused sources. A failed control establishes no unused/used receiver conclusion. This is a historical closed-bar question with no realtime credit.

## Evidence and settings

Paste each exact source into a new indicator on BINANCE:BTCUSDT, 2m, Etc/UTC, default settings/inputs. Preserve executed source and SHA, chart context and source identity in screenshot notes. If refused, retain complete compiler response/message, exposed code (unavailable code stays unspecified), and line/column. If admitted, add to chart and capture runtime errors with exact text/site/bar. Keep compilation, execution and values separate.

For running sources export original native CSV including time/OHLC/Volume and positional Plot after at least 32 closed bars. Preserve original headers, numeric strings and missing cells, timestamps, actual settings and confirmed closed-bar cutoff. Separate/exclude the open row. Compare the natural and used-receiver control on identical closed physical rows if both run. Context unavailable is CONTEXT-UNMET, not semantic refusal; no engine output or screenshot-only number is native evidence.

Return `v68/captures/v68/RESPONSE-v68.md`, an attempt inventory and integrity hashes with independent records and paired comparisons where possible. Preserve unavailable outcomes explicitly. Raw evidence belongs in this oracle repository.

## Paired source checklist

| Pair | Unused-receiver natural | Used-receiver control |
| --- | --- | --- |
| `receiver-only-v5` | [unused-udt-receiver-only-v5-natural-v1.pine](unused-udt-receiver-only-v5-natural-v1.pine) · [instructions](instructions/unused-udt-receiver-only-v5-natural-v1-instructions-v1.md) | [unused-udt-receiver-only-v5-control-v1.pine](unused-udt-receiver-only-v5-control-v1.pine) · [instructions](instructions/unused-udt-receiver-only-v5-control-v1-instructions-v1.md) |
| `receiver-only-v6` | [unused-udt-receiver-only-v6-natural-v1.pine](unused-udt-receiver-only-v6-natural-v1.pine) · [instructions](instructions/unused-udt-receiver-only-v6-natural-v1-instructions-v1.md) | [unused-udt-receiver-only-v6-control-v1.pine](unused-udt-receiver-only-v6-control-v1.pine) · [instructions](instructions/unused-udt-receiver-only-v6-control-v1-instructions-v1.md) |
