# Oracle probe round v69 — capture handoff v1

This round contains two separate groups: eight custom TA boundary programs and an authentic input-history bridge for the existing v63 captures. Source bytes, per-source instructions, producer manifest and history request are unchanged. Historical `v63-followup-v1` filenames identify the producer packet; v69 is the publication round. No native predictions or captures are bundled.

Run `sha256sum -c SHA256SUMS` from v69. Use the [bundle manifest](bundle-manifest-v1.json) and unchanged [producer manifest](instructions/producer-manifest-v1.json). Earlier [v68](../v68/HANDOFF-v68-v1.md) and [v63](../v63/HANDOFF-v63-v1.md) requests remain available.

## Group 1: custom TA boundaries

Run all eight exact sources independently. Each declares a custom Holder method named `stdev`, `lowest`, `cum` or `valuewhen` and calls it on a Holder parameter named `ta`. Capture whether Pine v5/v6 refuses, selects the custom method, selects the builtin namespace, or produces another observed outcome. Phase and values remain UNSPECIFIED. Do not repair refused sources or infer a namespace-wide rule from one method/version.

Use BINANCE:BTCUSDT, ordinary candles, 2 minutes, Etc/UTC, 24x7 and default inputs. Record exact executed source/SHA, settings and compiler response/text/code/site if refused (unexposed codes remain unspecified). For admission, capture runtime diagnostics and error bar separately. If it runs, export original CSV with time/OHLCV and positional Plot values, at least 32 confirmed closed bars, exact cutoff and open-row timestamp. Preserve original numeric strings, missing cells and headers; exclude the open bar. Keep native observations separate from any formula comparison. Unavailable context is CONTEXT-UNMET, not semantic refusal. No realtime credit.

| Probe | Source | Instructions |
| --- | --- | --- |
| `custom-ta-stdev-v5-v63-followup-v1` | [source](custom-ta-stdev-v5-v63-followup-v1.pine) | [instructions](instructions/custom-ta-stdev-v5-v63-followup-v1-instructions-v1.md) |
| `custom-ta-lowest-v5-v63-followup-v1` | [source](custom-ta-lowest-v5-v63-followup-v1.pine) | [instructions](instructions/custom-ta-lowest-v5-v63-followup-v1-instructions-v1.md) |
| `custom-ta-cum-v5-v63-followup-v1` | [source](custom-ta-cum-v5-v63-followup-v1.pine) | [instructions](instructions/custom-ta-cum-v5-v63-followup-v1-instructions-v1.md) |
| `custom-ta-valuewhen-v5-v63-followup-v1` | [source](custom-ta-valuewhen-v5-v63-followup-v1.pine) | [instructions](instructions/custom-ta-valuewhen-v5-v63-followup-v1-instructions-v1.md) |
| `custom-ta-stdev-v6-v63-followup-v1` | [source](custom-ta-stdev-v6-v63-followup-v1.pine) | [instructions](instructions/custom-ta-stdev-v6-v63-followup-v1-instructions-v1.md) |
| `custom-ta-lowest-v6-v63-followup-v1` | [source](custom-ta-lowest-v6-v63-followup-v1.pine) | [instructions](instructions/custom-ta-lowest-v6-v63-followup-v1-instructions-v1.md) |
| `custom-ta-cum-v6-v63-followup-v1` | [source](custom-ta-cum-v6-v63-followup-v1.pine) | [instructions](instructions/custom-ta-cum-v6-v63-followup-v1-instructions-v1.md) |
| `custom-ta-valuewhen-v6-v63-followup-v1` | [source](custom-ta-valuewhen-v6-v63-followup-v1.pine) | [instructions](instructions/custom-ta-valuewhen-v6-v63-followup-v1-instructions-v1.md) |

## Group 2: v63 input-history bridge

Follow the unchanged [HISTORY-BRIDGE-v1.md](HISTORY-BRIDGE-v1.md). Capture authentic BINANCE:BTCUSDT 2-minute OHLCV for at least the twelve immediately prior physical bars, UNIX `1791600720` through `1791602040`, before the existing first CSV row at `1791602160` (2026-10-10 03:16 UTC). Also capture an overlap from/after that first row and compare its OHLCV at matching timestamps to the existing CSVs. The producer request covers highest and change; highest needs the missing input history, and change shares the same boundary.

Retain the unchanged v63 sources, ordinary-candle chart context and export/settings/source/hash provenance. The manifest authenticates the existing executed sources and CSVs below. Preserve all existing raw observations. Deliver new bridge evidence under v69, with a mapping to these v63 attempts. Do not synthesize bars, reconstruct values from indicators, substitute TealScript output, or overwrite the v63 CSVs. If authentic prior bars or matching overlap cannot be obtained, record CONTEXT-UNMET and the exact limitation. No claim is settled by invented history.

| Existing attempt | Executed source | Existing CSV |
| --- | --- | --- |
| `custom-ta-highest-v5-v61-v1` | [executed source](../v63/captures/v63/custom-ta-highest-v5-v61-v1/attempt-v1/executed-v1.pine) | [existing CSV](../v63/captures/v63/custom-ta-highest-v5-v61-v1/attempt-v1/native-v1.csv) |
| `custom-ta-highest-v6-v61-v1` | [executed source](../v63/captures/v63/custom-ta-highest-v6-v61-v1/attempt-v1/executed-v1.pine) | [existing CSV](../v63/captures/v63/custom-ta-highest-v6-v61-v1/attempt-v1/native-v1.csv) |
| `custom-ta-change-v5-v61-v1` | [executed source](../v63/captures/v63/custom-ta-change-v5-v61-v1/attempt-v1/executed-v1.pine) | [existing CSV](../v63/captures/v63/custom-ta-change-v5-v61-v1/attempt-v1/native-v1.csv) |
| `custom-ta-change-v6-v61-v1` | [executed source](../v63/captures/v63/custom-ta-change-v6-v61-v1/attempt-v1/executed-v1.pine) | [existing CSV](../v63/captures/v63/custom-ta-change-v6-v61-v1/attempt-v1/native-v1.csv) |

## Capture response

Return `v69/captures/v69/RESPONSE-v69.md`, an attempt inventory and integrity hashes. Keep the two groups separate in the response. For group 1, report all eight independent compile/runtime/value observations. For group 2, include raw native OHLCV bridge evidence, source/settings provenance, closed-bar cutoff, and an overlap comparison tied to the existing v63 source and CSV hashes. Retain unavailable outcomes explicitly. Raw evidence belongs in this oracle repository.
