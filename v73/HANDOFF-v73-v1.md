# Oracle probe round v73 — capture handoff v1

Fifteen source-only inputs: ten v5/v6 original custom Holder.set_top namespace-parameter shapes for line, box, label, table and linefill, plus five renamed v6 controls. Native outcomes are UNSPECIFIED. These exact shapes are open questions following the batch-55 naming attribution; prior w0Value captures or local-variable naming evidence do not settle them. Arithmetic value 20 is a question, never native truth.

Run `sha256sum -c SHA256SUMS` from v73. Use the [bundle manifest](bundle-manifest-v1.json), unchanged [producer entry](instructions/ENTRY-v1.json), and unchanged [instructions](instructions/INSTRUCTIONS-v1.md). The earlier [v72 request](../v72/HANDOFF-v72-v1.md) remains available.

Attempt each exact source unchanged on BINANCE:BTCUSDT ordinary 2-minute candles, Etc/UTC, 24x7, default inputs. Record executed source/hash, settings, compile status and every marker including exact diagnostic text, code and line/column. Do not rename namespace parameters or repair refused sources. Capture renamed controls separately. If admitted, record runtime status/error/bar and export original time/OHLCV/Plot CSV for at least 32 closed physical rows, including cutoff and open-row identity. Preserve original numeric strings, missing cells and headers. Record namespace resolution separately from arithmetic output. Unavailable context stays CONTEXT-UNMET, and failed attempts stay in the inventory. No realtime claim.

| Probe | Source | Role | Version |
| --- | --- | --- | --- |
| `box-holder-control-v1` | [source](box-holder-control-v1.pine) | control | v6 |
| `label-holder-control-v1` | [source](label-holder-control-v1.pine) | control | v6 |
| `line-holder-control-v1` | [source](line-holder-control-v1.pine) | control | v6 |
| `linefill-holder-control-v1` | [source](linefill-holder-control-v1.pine) | control | v6 |
| `ns-param-set-top-box-v5-v1` | [source](ns-param-set-top-box-v5-v1.pine) | consumer | v5 |
| `ns-param-set-top-box-v6-v1` | [source](ns-param-set-top-box-v6-v1.pine) | consumer | v6 |
| `ns-param-set-top-label-v5-v1` | [source](ns-param-set-top-label-v5-v1.pine) | consumer | v5 |
| `ns-param-set-top-label-v6-v1` | [source](ns-param-set-top-label-v6-v1.pine) | consumer | v6 |
| `ns-param-set-top-line-v5-v1` | [source](ns-param-set-top-line-v5-v1.pine) | consumer | v5 |
| `ns-param-set-top-line-v6-v1` | [source](ns-param-set-top-line-v6-v1.pine) | consumer | v6 |
| `ns-param-set-top-linefill-v5-v1` | [source](ns-param-set-top-linefill-v5-v1.pine) | consumer | v5 |
| `ns-param-set-top-linefill-v6-v1` | [source](ns-param-set-top-linefill-v6-v1.pine) | consumer | v6 |
| `ns-param-set-top-table-v5-v1` | [source](ns-param-set-top-table-v5-v1.pine) | consumer | v5 |
| `ns-param-set-top-table-v6-v1` | [source](ns-param-set-top-table-v6-v1.pine) | consumer | v6 |
| `table-holder-control-v1` | [source](table-holder-control-v1.pine) | control | v6 |

Return `v73/captures/v73/RESPONSE-v73.md`, an attempt inventory, raw observations and integrity hashes. Preserve all 15 program outcomes separately; raw captures belong only in this repository.
