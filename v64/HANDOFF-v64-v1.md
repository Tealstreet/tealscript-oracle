# Oracle probe round v64 — capture handoff v1

Eight source-only Pine v6 indicator consumers in four natural/control pairs: array and map reassignment under `var` and `varip`. Sources, instructions and the v2 producer request are preserved byte-for-byte. Original probe names and indicator titles still say v61; v64 is their publication round. No captures or native predictions are bundled. Every exact-source outcome is UNSPECIFIED until observed.

Run `sha256sum -c SHA256SUMS` from v64. The [bundle manifest](bundle-manifest-v1.json) records source/instruction hashes, settings and pair membership. The [producer request v2](instructions/producer-PROBE-REQUEST-v2.json) is unchanged; its historical absolute paths are provenance rather than runtime dependencies. Use the relative source/instruction paths below. No external imports or library publication are required. Only these v2 sources are active; do not reconstruct the superseded v1 packet.

## Questions and limits

For each collection/declaration pair, capture the float-to-int reassignment natural and the same-kind float-to-float control independently. Does each source refuse compilation, fault at runtime or run? The producer's VALUE=3 is a candidate answer only; preserve any observed value. Plain-declaration v60 observations do not settle these `var`/`varip` aliases. Do not convert declaration modes, add annotations or repair sources. Closed-bar results do not certify intrabar persistence or realtime behavior.

## Evidence and settings

Use BINANCE:BTCUSDT, 2m, chart display timezone Etc/UTC, default settings. Paste exact sources into new indicators. Record executed source/SHA, all compiler refusal text/code/site (code unavailable if not exposed), compiler responses, screenshot notes and actual symbol/timeframe. If admitted, add to chart and preserve runtime errors with message/site/bar. Keep compile admission, execution and values separate.

For running indicators export original native CSV including time/OHLC/Volume and the positional plot after at least 32 closed bars. Preserve original headers, numeric strings and missing cells. Record the last confirmed closed-bar cutoff and separate/exclude the open row. When both pair members run, compare identical closed physical rows and retain both exports. No rounding or numerical credit from screenshots alone. Context unavailable is CONTEXT-UNMET, not semantic refusal; engine output is never native evidence.

Return `v64/captures/v64/RESPONSE-v64.md`, an attempt inventory and integrity hashes, with an independent record for each source and paired comparisons where possible. Preserve unavailable outcomes explicitly. Raw evidence belongs in this oracle repository. Earlier [v61](../v61/HANDOFF-v61-v1.md), [v62](../v62/HANDOFF-v62-v1.md) and [v63](../v63/HANDOFF-v63-v1.md) requests and captures remain available.

## Paired source checklist

| Pair | Natural | Same-kind control |
| --- | --- | --- |
| `array-var` | [v61-array-reassign-var-natural-v2.pine](v61-array-reassign-var-natural-v2.pine) · [instructions](instructions/v61-array-reassign-var-natural-v2-instructions-v2.md) | [v61-array-reassign-var-control-v2.pine](v61-array-reassign-var-control-v2.pine) · [instructions](instructions/v61-array-reassign-var-control-v2-instructions-v2.md) |
| `array-varip` | [v61-array-reassign-varip-natural-v2.pine](v61-array-reassign-varip-natural-v2.pine) · [instructions](instructions/v61-array-reassign-varip-natural-v2-instructions-v2.md) | [v61-array-reassign-varip-control-v2.pine](v61-array-reassign-varip-control-v2.pine) · [instructions](instructions/v61-array-reassign-varip-control-v2-instructions-v2.md) |
| `map-var` | [v61-map-reassign-var-natural-v2.pine](v61-map-reassign-var-natural-v2.pine) · [instructions](instructions/v61-map-reassign-var-natural-v2-instructions-v2.md) | [v61-map-reassign-var-control-v2.pine](v61-map-reassign-var-control-v2.pine) · [instructions](instructions/v61-map-reassign-var-control-v2-instructions-v2.md) |
| `map-varip` | [v61-map-reassign-varip-natural-v2.pine](v61-map-reassign-varip-natural-v2.pine) · [instructions](instructions/v61-map-reassign-varip-natural-v2-instructions-v2.md) | [v61-map-reassign-varip-control-v2.pine](v61-map-reassign-varip-control-v2.pine) · [instructions](instructions/v61-map-reassign-varip-control-v2-instructions-v2.md) |
