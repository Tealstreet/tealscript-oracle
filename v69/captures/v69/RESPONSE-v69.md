# v69 native capture response v1

All eight exact custom TA indicators were independently attempted through Chrome MCP. Four RUNS with original native CSVs; four refuse compilation. The v63 input-history bridge is CAPTURED for all four unchanged sources, including all twelve requested prior physical bars and 985 exact OHLCV overlap matches per existing capture.

[Attempt inventory](attempt-inventory-v1.json) · [Audit](audit-v1.json) · [History bridge inventory](history-bridge-inventory-v1.json) · [Integrity hashes](environment-v1/integrity-v1.json)

Captured on the mini as sours-lat: BINANCE:BTCUSDT, Binance provider, ordinary candles, 2 minutes, Etc/UTC, 24x7, default inputs. All 20 request checksum entries pass. Original source/CSV bytes, compiler response bodies, all marker owners/codes/sites, runtime status, screenshots, snapshots, export settings and per-export cutoff/open rows are preserved. No realtime credit.

## Group 1: custom TA boundaries

- `stdev` and `valuewhen` refuse independently in both versions at 8:5: constructs cannot shadow existing built-in functions. v6 exposes CE10195; v5 code is unavailable. Full native messages and marker owners are retained.
- `lowest` RUNS in both versions with a varying price-scale Plot. Separate derived checks match `2 * minimum physical low over 13 bars + 1` on all 1007 closed rows with sufficient exported inputs. The original native strings remain authoritative.
- `cum` RUNS in both versions with increasing Plot strings, from 620335 at the first exported row to 646803 at the last confirmed closed row. A separate derived comparison matches consecutive increments of 26 across 1018 closed transitions. Prior cumulative history is unavailable from these exports and is not reconstructed.
- None of the admitted closed Plot strings equals the custom-body arithmetic result 41. These numeric observations distinguish the exact programs; they do not establish a namespace-wide rule.

| Source | Outcome | Native evidence |
| --- | --- | --- |
| `custom-ta-stdev-v5-v63-followup-v1.pine` | COMPILE-ERROR | [observation](custom-ta-stdev-v5-v63-followup-v1/attempt-v1/observation-v3.json) |
| `custom-ta-lowest-v5-v63-followup-v1.pine` | RUNS | [observation](custom-ta-lowest-v5-v63-followup-v1/attempt-v1/observation-v3.json) |
| `custom-ta-cum-v5-v63-followup-v1.pine` | RUNS | [observation](custom-ta-cum-v5-v63-followup-v1/attempt-v1/observation-v3.json) |
| `custom-ta-valuewhen-v5-v63-followup-v1.pine` | COMPILE-ERROR | [observation](custom-ta-valuewhen-v5-v63-followup-v1/attempt-v1/observation-v3.json) |
| `custom-ta-stdev-v6-v63-followup-v1.pine` | COMPILE-ERROR | [observation](custom-ta-stdev-v6-v63-followup-v1/attempt-v1/observation-v3.json) |
| `custom-ta-lowest-v6-v63-followup-v1.pine` | RUNS | [observation](custom-ta-lowest-v6-v63-followup-v1/attempt-v1/observation-v3.json) |
| `custom-ta-cum-v6-v63-followup-v1.pine` | RUNS | [observation](custom-ta-cum-v6-v63-followup-v1/attempt-v1/observation-v3.json) |
| `custom-ta-valuewhen-v6-v63-followup-v1.pine` | COMPILE-ERROR | [observation](custom-ta-valuewhen-v6-v63-followup-v1/attempt-v1/observation-v3.json) |

Each successful boundary export has 1019 confirmed closed bars, with raw OHLCV and positional Plot preserved. Compile-refused programs have no numeric export.

## Group 2: v63 input-history bridge

Native chart history was loaded using Go to date, Friday 9 October 2026. Four fresh native CSV exports rerun the unchanged v63 highest/change sources. They begin at UNIX 1791513240 and retain 1761 confirmed closed rows each, including the twelve requested bars from 1791600720 through 1791602040. Full source/settings/export/hash provenance and individual cutoff/open rows are linked below.

All 985 original confirmed closed timestamps in each v63 capture have identical original OHLCV strings in the bridge export, including the first original row 1791602160. Original open rows are excluded from that comparison. Every existing closed Plot string also matches the respective rerun. The original v63 source and CSV hashes match the request manifest; no v63 evidence is overwritten.

A separate Decimal comparison of the original highest Plot against `2 * maximum physical high over 13 bars + 1` matches all 985 original closed rows in each version, now including the first twelve rows with authentic prior inputs. This derived check is retained separately from the native observations.

| Existing v63 attempt | Bridge mapping and comparison |
| --- | --- |
| `custom-ta-highest-v5-v61-v1` | [history bridge](custom-ta-highest-v5-v61-v1/attempt-v1/history-bridge-v1.json) · [original native export](custom-ta-highest-v5-v61-v1/attempt-v1/native-v1.csv) |
| `custom-ta-highest-v6-v61-v1` | [history bridge](custom-ta-highest-v6-v61-v1/attempt-v1/history-bridge-v1.json) · [original native export](custom-ta-highest-v6-v61-v1/attempt-v1/native-v1.csv) |
| `custom-ta-change-v5-v61-v1` | [history bridge](custom-ta-change-v5-v61-v1/attempt-v1/history-bridge-v1.json) · [original native export](custom-ta-change-v5-v61-v1/attempt-v1/native-v1.csv) |
| `custom-ta-change-v6-v61-v1` | [history bridge](custom-ta-change-v6-v61-v1/attempt-v1/history-bridge-v1.json) · [original native export](custom-ta-change-v6-v61-v1/attempt-v1/native-v1.csv) |

No synthetic bars, indicator reconstruction, repaired sources or engine output were used. All requested outcomes have observations; no context is unavailable for the history bridge.
