# Oracle probe round v81 — DXY live capture handoff v1

Two source-only Pine v6 indicators request genuine TVC:DXY initial-open, two subsequent updates and native-close input observations. Read [instructions](instructions/INSTRUCTIONS-v1.md) in full before any account action. Native compilation, values and instrument retention are UNSPECIFIED until capture; missing context remains CONTEXT-UNMET.

## Account scope

Only temporary chart view/navigation, an exact UNSAVED indicator draft, Add to chart, chart/Data Window inspection/screenshots and chart-data export are allowed. **NO Save (script or layout), Publish, Share, alerts, library publication/import, persistent preference/account/subscription changes or saved-layout edits.** If any capture step requires more, STOP and record CONTEXT-UNMET. Requests only; no account actions or captures were performed for publication.

## Capture context and identity

Use TVC:DXY, ordinary candles, 2 minutes, native regular session and actual provider/timezone/feed-status metadata. Prefer an already-UTC chart; never change a persistent preference to satisfy this request. No Bar Replay, synthetic ticks, volume replacement or source repair. Each source needs its own same-target-bar/session INITIAL_OPEN, UPDATE1, UPDATE2 and BAR_CLOSE sequence. Authenticate the physically open attachment, natively missing initial volume, two distinct realtime-unconfirmed executions and the realtime-confirmed closing evaluation. An unavailable/closed/stale feed or incomplete sequence stays CONTEXT-UNMET.

Preserve raw CSV bytes, missing strings, screenshots, executed-source hashes and source/study column ordinals. Keep historical prefix, realtime events and confirmed close separate. Export full available history with at least 32 preceding bars. The 63 columns and retained-frame acceptance rules are defined in [column schema](COLUMN-SCHEMA-v1.json), [observation schema](OBSERVATION-SCHEMA-v1.json) and the detailed instructions. No ACCDIST/OBV engine result or native parity closure is inferred by this input-context request.

| Probe | Source | Role | Version |
| --- | --- | --- | --- |
| v81-dxy-live-inputs-v1 | [source](v81-dxy-live-inputs-v1.pine) | natural | v6 |
| v81-dxy-live-inputs-renamed-control-v1 | [source](v81-dxy-live-inputs-renamed-control-v1.pine) | renamed-control | v6 |

## Packet checks and return

Run `sha256sum -c SHA256SUMS` from v81/. Read [bundle manifest](bundle-manifest-v1.json), [producer entry](instructions/ENTRY-v1.json), [producer handoff](instructions/PRODUCER-HANDOFF-v1.json) and [producer report](instructions/REPORT-v1.md). Original producer files are byte-preserved; their packet-relative references and checksum list are archival provenance. The manifest path mapping and root checksum list describe the published layout. Published instructions differ only in the rebased checksum command.

Return `v81/captures/v81/RESPONSE-v81.md` plus per-source/session observations, executed sources, raw exports, screenshots, column bindings and derived prefix/event/close artifacts. Preserve every failed/partial attempt. State actual account actions and explicitly confirm no Save/Publish/Share/alerts or persistent account changes.
