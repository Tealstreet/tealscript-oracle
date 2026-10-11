# Oracle probe round v78 — capture handoff v1

Twenty-four source-only indicators form twelve pairs: Pine v5/v6 × array.every/some × int/float/string arrays, named `id=items` versus positional `items`. Native admission, diagnostic phase and values are UNSPECIFIED. The positional companion is an outcome control, not a promise of admission.

Run `sha256sum -c SHA256SUMS` from v78. Read the [bundle manifest](bundle-manifest-v1.json), unchanged [producer entry](instructions/ENTRY-v1.json), unchanged [instructions](instructions/INSTRUCTIONS-v1.md), and [producer handoff](instructions/PRODUCER-HANDOFF-v1.json). Producer absolute intake paths are provenance; published manifest paths resolve from this directory. The [v77 request](../v77/HANDOFF-v77-v1.md) remains available.

Attempt each exact source independently in a fresh indicator draft on BINANCE:BTCUSDT, standard candles, 2 minutes, Etc/UTC, regular session, at least 32 confirmed bars. Preserve actual context/settings. No imports, requests or entitlements are required. Record compilation first, executed source/hash, complete error/warning text, exposed CE code (leave unavailable codes absent), observed line:column and screenshots. Do not repair rejected inputs or infer named behavior from the positional companion or local engine.

If admitted, add to chart and export original OHLCV/RESULT CSV with raw hash and confirmed cutoff. Preserve missing cells, numeric strings, runtime errors/bar and warnings; keep live rows separate. Refused sources require no numeric CSV. String empty elements are intentional. If both paired sources run, compare original closed RESULT cells; observe exact diagnostic identifier rendering and named-argument caret independently if they refuse.

The producer describes only the argument-binding difference. The exact sources also have role-specific indicator titles; these are preserved unchanged. After ignoring titles, each pair differs only in named versus positional binding. Keep all 24 attempt identities and outcomes separately, including refusals that appear equivalent. Unavailable context remains CONTEXT-UNMET.

| Probe | Source | Pair | Role | Version |
| --- | --- | --- | --- | --- |
| `v78-v5-every-int-named-tk-v1` | [source](v78-v5-every-int-named-tk-v1.pine) | v5-every-int | named | v5 |
| `v78-v5-every-int-positional-tk-v1` | [source](v78-v5-every-int-positional-tk-v1.pine) | v5-every-int | positional | v5 |
| `v78-v5-every-float-named-tk-v1` | [source](v78-v5-every-float-named-tk-v1.pine) | v5-every-float | named | v5 |
| `v78-v5-every-float-positional-tk-v1` | [source](v78-v5-every-float-positional-tk-v1.pine) | v5-every-float | positional | v5 |
| `v78-v5-every-string-named-tk-v1` | [source](v78-v5-every-string-named-tk-v1.pine) | v5-every-string | named | v5 |
| `v78-v5-every-string-positional-tk-v1` | [source](v78-v5-every-string-positional-tk-v1.pine) | v5-every-string | positional | v5 |
| `v78-v5-some-int-named-tk-v1` | [source](v78-v5-some-int-named-tk-v1.pine) | v5-some-int | named | v5 |
| `v78-v5-some-int-positional-tk-v1` | [source](v78-v5-some-int-positional-tk-v1.pine) | v5-some-int | positional | v5 |
| `v78-v5-some-float-named-tk-v1` | [source](v78-v5-some-float-named-tk-v1.pine) | v5-some-float | named | v5 |
| `v78-v5-some-float-positional-tk-v1` | [source](v78-v5-some-float-positional-tk-v1.pine) | v5-some-float | positional | v5 |
| `v78-v5-some-string-named-tk-v1` | [source](v78-v5-some-string-named-tk-v1.pine) | v5-some-string | named | v5 |
| `v78-v5-some-string-positional-tk-v1` | [source](v78-v5-some-string-positional-tk-v1.pine) | v5-some-string | positional | v5 |
| `v78-v6-every-int-named-tk-v1` | [source](v78-v6-every-int-named-tk-v1.pine) | v6-every-int | named | v6 |
| `v78-v6-every-int-positional-tk-v1` | [source](v78-v6-every-int-positional-tk-v1.pine) | v6-every-int | positional | v6 |
| `v78-v6-every-float-named-tk-v1` | [source](v78-v6-every-float-named-tk-v1.pine) | v6-every-float | named | v6 |
| `v78-v6-every-float-positional-tk-v1` | [source](v78-v6-every-float-positional-tk-v1.pine) | v6-every-float | positional | v6 |
| `v78-v6-every-string-named-tk-v1` | [source](v78-v6-every-string-named-tk-v1.pine) | v6-every-string | named | v6 |
| `v78-v6-every-string-positional-tk-v1` | [source](v78-v6-every-string-positional-tk-v1.pine) | v6-every-string | positional | v6 |
| `v78-v6-some-int-named-tk-v1` | [source](v78-v6-some-int-named-tk-v1.pine) | v6-some-int | named | v6 |
| `v78-v6-some-int-positional-tk-v1` | [source](v78-v6-some-int-positional-tk-v1.pine) | v6-some-int | positional | v6 |
| `v78-v6-some-float-named-tk-v1` | [source](v78-v6-some-float-named-tk-v1.pine) | v6-some-float | named | v6 |
| `v78-v6-some-float-positional-tk-v1` | [source](v78-v6-some-float-positional-tk-v1.pine) | v6-some-float | positional | v6 |
| `v78-v6-some-string-named-tk-v1` | [source](v78-v6-some-string-named-tk-v1.pine) | v6-some-string | named | v6 |
| `v78-v6-some-string-positional-tk-v1` | [source](v78-v6-some-string-positional-tk-v1.pine) | v6-some-string | positional | v6 |

Return `v78/captures/v78/RESPONSE-v78.md`, an attempt inventory, original observations and integrity hashes. This publication contains requests only; captures belong in a later response commit.
