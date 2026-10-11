# Oracle probe round v71 — capture handoff v1

Eight exact source-only Pine v5/v6 indicators: unused receiver-only methods of builtin footprint and box type, each paired with a used-receiver control. Outcomes remain UNSPECIFIED. Declared Point UDT evidence does not settle these builtin receivers.

Run `sha256sum -c SHA256SUMS` from v71. Use [bundle manifest](bundle-manifest-v1.json), unchanged [producer request](instructions/producer-PROBE-REQUEST-v2.json), and every source instruction below. Earlier [v70](../v70/HANDOFF-v70-v1.md) remains available.

**V5 footprint availability caveat:** footprint type/version/entitlement availability may prevent observing unused-receiver semantics. Retain the exact first diagnostic and distinguish an unknown/unavailable type or entitlement/version refusal from an unused-receiver refusal. If both natural/control fail before the receiver-usage facet is reached, record that facet CONTEXT-UNMET; do not attribute the earlier error to unusedness or invent v5 support. Do not repair or upgrade sources.

Use BINANCE:BTCUSDT, ordinary candles, 2-minute bars, Etc/UTC, default inputs, a fresh indicator tab for each exact source. Record executed source/hash, full compiler phase/text/exposed code/site, screenshot context and actual settings. On admission, record any runtime error text/site/bar; otherwise export original chart CSV with Plot and at least 32 closed bars, exact cutoff/open-row timestamps, raw numeric strings, missing cells and headers. Used controls read na(self) while both branches return 7; constant 7 is a candidate observer, not preselected native evidence. No realtime or provider availability claim.

| Probe | Source | Instructions |
| --- | --- | --- |
| `unused-builtin-footprint-v5-natural-v2` | [source](unused-builtin-footprint-v5-natural-v2.pine) | [instructions](instructions/unused-builtin-footprint-v5-natural-v2-instructions-v2.md) |
| `unused-builtin-footprint-v5-control-v2` | [source](unused-builtin-footprint-v5-control-v2.pine) | [instructions](instructions/unused-builtin-footprint-v5-control-v2-instructions-v2.md) |
| `unused-builtin-box-v5-natural-v2` | [source](unused-builtin-box-v5-natural-v2.pine) | [instructions](instructions/unused-builtin-box-v5-natural-v2-instructions-v2.md) |
| `unused-builtin-box-v5-control-v2` | [source](unused-builtin-box-v5-control-v2.pine) | [instructions](instructions/unused-builtin-box-v5-control-v2-instructions-v2.md) |
| `unused-builtin-footprint-v6-natural-v2` | [source](unused-builtin-footprint-v6-natural-v2.pine) | [instructions](instructions/unused-builtin-footprint-v6-natural-v2-instructions-v2.md) |
| `unused-builtin-footprint-v6-control-v2` | [source](unused-builtin-footprint-v6-control-v2.pine) | [instructions](instructions/unused-builtin-footprint-v6-control-v2-instructions-v2.md) |
| `unused-builtin-box-v6-natural-v2` | [source](unused-builtin-box-v6-natural-v2.pine) | [instructions](instructions/unused-builtin-box-v6-natural-v2-instructions-v2.md) |
| `unused-builtin-box-v6-control-v2` | [source](unused-builtin-box-v6-control-v2.pine) | [instructions](instructions/unused-builtin-box-v6-control-v2-instructions-v2.md) |

Return `v71/captures/v71/RESPONSE-v71.md`, attempt inventory, raw observations and integrity hashes. Keep availability failures separate from reached receiver-usage outcomes; preserve unsuccessful attempts. Raw evidence belongs only in this oracle repository.
