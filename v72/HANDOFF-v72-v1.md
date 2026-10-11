# Oracle probe round v72 — capture handoff v1

Eight source-only v5/v6 custom TA boundary questions: max, min, wma and variance. Source names retain producer v69-followup provenance. Native outcomes are UNSPECIFIED. The producer hypothesis about builtin one-argument arity is a question only, never an expected result or namespace-wide rule.

Run `sha256sum -c SHA256SUMS` from v72. Use [bundle manifest](bundle-manifest-v1.json), unchanged [producer manifest](instructions/producer-manifest-v1.json), and shared [instructions](instructions/INSTRUCTIONS-v1.md). Earlier [v71](../v71/HANDOFF-v71-v1.md) remains available.

Attempt each exact source unchanged on BINANCE:BTCUSDT ordinary 2-minute candles, Etc/UTC, 24x7, default inputs. Record executed source/hash, settings, compile phase and all markers including exact text/code/site, then runtime status/error/bar separately. If it runs, export original CSV with time/OHLCV and Plot for at least 32 closed rows, cutoff/open-row identity, original strings, missing cells and headers. Do not repair refused sources. Retain unavailable context as CONTEXT-UNMET and preserve failed attempts. Record whether the observed route is custom method, builtin namespace, refusal or another outcome without inferring from engine output.

| Probe | Source | Instructions |
| --- | --- | --- |
| `custom-ta-max-v5-v69-followup-v1` | [source](custom-ta-max-v5-v69-followup-v1.pine) | [instructions](instructions/INSTRUCTIONS-v1.md) |
| `custom-ta-min-v5-v69-followup-v1` | [source](custom-ta-min-v5-v69-followup-v1.pine) | [instructions](instructions/INSTRUCTIONS-v1.md) |
| `custom-ta-wma-v5-v69-followup-v1` | [source](custom-ta-wma-v5-v69-followup-v1.pine) | [instructions](instructions/INSTRUCTIONS-v1.md) |
| `custom-ta-variance-v5-v69-followup-v1` | [source](custom-ta-variance-v5-v69-followup-v1.pine) | [instructions](instructions/INSTRUCTIONS-v1.md) |
| `custom-ta-max-v6-v69-followup-v1` | [source](custom-ta-max-v6-v69-followup-v1.pine) | [instructions](instructions/INSTRUCTIONS-v1.md) |
| `custom-ta-min-v6-v69-followup-v1` | [source](custom-ta-min-v6-v69-followup-v1.pine) | [instructions](instructions/INSTRUCTIONS-v1.md) |
| `custom-ta-wma-v6-v69-followup-v1` | [source](custom-ta-wma-v6-v69-followup-v1.pine) | [instructions](instructions/INSTRUCTIONS-v1.md) |
| `custom-ta-variance-v6-v69-followup-v1` | [source](custom-ta-variance-v6-v69-followup-v1.pine) | [instructions](instructions/INSTRUCTIONS-v1.md) |

Return `v72/captures/v72/RESPONSE-v72.md`, an attempt inventory, raw observations and integrity hashes. Keep all eight method/version observations separate. Raw captures belong only in this repository.
