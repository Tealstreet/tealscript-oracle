# Oracle probe round v63 — capture handoff v1

Eight source-only indicator consumers in one custom-TA boundary group: `ta.change`, `ta.rsi`, `ta.highest`, `ta.crossover`, each in Pine v5 and v6. The sources, per-source instructions and producer manifest are preserved byte-for-byte. Original filenames and probe identifiers still say v61; v63 is the publication round because v62 was already pushed. No captures or native predictions are bundled. Every exact-source native phase and value remains UNSPECIFIED until observed.

Run `sha256sum -c SHA256SUMS` from v63. Follow the [bundle manifest](bundle-manifest-v1.json), unchanged [producer manifest](instructions/producer-manifest-v1.json) and per-source instructions below. No external library publication/import is required. Earlier requests remain available in [v61](../v61/HANDOFF-v61-v1.md) and [v62](../v62/HANDOFF-v62-v1.md).

## Question and scope

Does each custom UDT call on a parameter named `ta` run, or does native refuse it as shadowing the matching builtin? v59 settled only sma/ema refusal and w0Value admission; those observations do not establish outcomes for these four names. Keep each name/version separate. Do not infer a general namespace policy or realtime behavior. Paste each source unchanged: do not rename the parameter, change the call, inline the method or replace its arithmetic.

## Evidence and settings

Use BINANCE:BTCUSDT, 2m, chart display timezone Etc/UTC, default inputs. Record exact executed source/SHA, compiler diagnostics with class/text/code if exposed and line:column, compiler/Save responses, screenshots and runtime error/bar. Mark codes unavailable when not exposed. Preserve compile admission separately from execution and values.

For admitted indicators export original CSV with time/OHLC/Volume and the positional `Plot` column after at least 32 closed bars. Preserve numeric strings, missing cells and duplicate headers. Record actual chart settings and the last confirmed closed-bar cutoff; separate/exclude the open row. Preserve unavailable evidence as CONTEXT-UNMET rather than semantic refusal. No engine output is native evidence.

Return `v63/captures/v63/RESPONSE-v63.md`, an attempt inventory and integrity hashes, with an independent record per source. Raw capture evidence belongs in this oracle repository.

## Source checklist

- [custom-ta-change-v5-v61-v1.pine](custom-ta-change-v5-v61-v1.pine) — [instructions](instructions/custom-ta-change-v5-v61-v1-instructions-v1.md); custom `ta.change`, Pine v5.
- [custom-ta-change-v6-v61-v1.pine](custom-ta-change-v6-v61-v1.pine) — [instructions](instructions/custom-ta-change-v6-v61-v1-instructions-v1.md); custom `ta.change`, Pine v6.
- [custom-ta-crossover-v5-v61-v1.pine](custom-ta-crossover-v5-v61-v1.pine) — [instructions](instructions/custom-ta-crossover-v5-v61-v1-instructions-v1.md); custom `ta.crossover`, Pine v5.
- [custom-ta-crossover-v6-v61-v1.pine](custom-ta-crossover-v6-v61-v1.pine) — [instructions](instructions/custom-ta-crossover-v6-v61-v1-instructions-v1.md); custom `ta.crossover`, Pine v6.
- [custom-ta-highest-v5-v61-v1.pine](custom-ta-highest-v5-v61-v1.pine) — [instructions](instructions/custom-ta-highest-v5-v61-v1-instructions-v1.md); custom `ta.highest`, Pine v5.
- [custom-ta-highest-v6-v61-v1.pine](custom-ta-highest-v6-v61-v1.pine) — [instructions](instructions/custom-ta-highest-v6-v61-v1-instructions-v1.md); custom `ta.highest`, Pine v6.
- [custom-ta-rsi-v5-v61-v1.pine](custom-ta-rsi-v5-v61-v1.pine) — [instructions](instructions/custom-ta-rsi-v5-v61-v1-instructions-v1.md); custom `ta.rsi`, Pine v5.
- [custom-ta-rsi-v6-v61-v1.pine](custom-ta-rsi-v6-v61-v1.pine) — [instructions](instructions/custom-ta-rsi-v6-v61-v1-instructions-v1.md); custom `ta.rsi`, Pine v6.
