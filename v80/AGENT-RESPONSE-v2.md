# v80 agent response v2

Batch 59 `fcc4eaca5eb7094284c6b389fd54504abd61a0ca` is pushed to pine-parity-integration-v4. Consuming root: codex-p4250m, `80997aafc3e89b87d76b9d4a31d93391485f3dbc`. Inventory SHA256 `d39e4d15ccb10a71d3c6b0bfc7669899b25e8e37b5e4430820ec5b119196929e`. Landed union: 1448 sorted entries at oracle `18e85052633d7e01b1ff7c068a9f77cf77aae48c`.

This v2 corrects the v1 table: the short daily attempt-v2 was not consumed; only selected daily attempt-v3 supplies the provider. All numerical certificate counts and 17 fixture bindings are unchanged.

Nested-6 is consumed with **72,000 / 72,000 exact comparisons**, representing **34,560 unique timestamp/column pairs**: original 2,880, initial observers 34,560, repeat observers 34,560. W is 2026-10-08 00:00 through 2026-10-10 00:00 UTC exclusive, 1,440 confirmed 2-minute bars. A separately captured native 1D provider supplies both requested levels, with 3,343 provider rows / 3,342 independently closed days. No synthetic feed or aggregation. Clock/developing/open rows, full-history generalization and retroactive v58 developing-day credit are excluded. The seven unread fixture entries were removed before acceptance; only 17 consumed v80 files are promoted.

| Attempt | State / owner root | Pushed batch commit | Credited scope | Fixture entries |
| --- | --- | --- | --- | --- |
| `v80-nested6-original-v1/attempt-v1` | CONSUMED / CLOSED-W / p4250m / `80997aafc3e89b87d76b9d4a31d93391485f3dbc` | 59 / `fcc4eaca5eb7094284c6b389fd54504abd61a0ca` | RUNS; Recorded original/observer closed-W comparison or selected independent daily input. Only actual consumed fixture files promoted. | `v80/captures/v80/v80-nested6-original-v1/attempt-v1/executed-v1.pine` (SHA256 `ba47e1d4264c7ff00fd555125dddaa75c557db495e02388aad7beff8246dd008`)<br>`v80/captures/v80/v80-nested6-original-v1/attempt-v1/native-v1.csv` (SHA256 `0cdf4631f413f56ce0165da6acb015f066d1a4ee61f659ada0b46468ff523702`)<br>`v80/captures/v80/v80-nested6-original-v1/attempt-v1/observation-v3.json` (SHA256 `d5cad9a08634e963ed4d468fc5200645fca6f3cd473d0e3d9c6d97f5f122ec25`) |
| `v80-nested6-with-feed-v1/attempt-v1` | CONSUMED / CLOSED-W / p4250m / `80997aafc3e89b87d76b9d4a31d93391485f3dbc` | 59 / `fcc4eaca5eb7094284c6b389fd54504abd61a0ca` | RUNS; Recorded original/observer closed-W comparison or selected independent daily input. Only actual consumed fixture files promoted. | `v80/captures/v80/v80-nested6-with-feed-v1/attempt-v1/executed-v1.pine` (SHA256 `a18d8d1607f3b4d5aff88d6b46270f30af9dc88478ea66d9621822f93f239e5f`)<br>`v80/captures/v80/v80-nested6-with-feed-v1/attempt-v1/native-v1.csv` (SHA256 `d8de685995bde4de9579a4958eabe2f750fcd3c63cd3b1c34a3014b3cf4510f8`)<br>`v80/captures/v80/v80-nested6-with-feed-v1/attempt-v1/observation-v3.json` (SHA256 `09b56e008eb3759a3469e03d4bb97ae3cbdcbd07b01ab62eb0c1de79ab3ca9a3`) |
| `v80-nested6-with-feed-v1/attempt-v2` | CONSUMED / CLOSED-W / p4250m / `80997aafc3e89b87d76b9d4a31d93391485f3dbc` | 59 / `fcc4eaca5eb7094284c6b389fd54504abd61a0ca` | RUNS; Recorded original/observer closed-W comparison or selected independent daily input. Only actual consumed fixture files promoted. | `v80/captures/v80/v80-nested6-with-feed-v1/attempt-v2/executed-v1.pine` (SHA256 `a18d8d1607f3b4d5aff88d6b46270f30af9dc88478ea66d9621822f93f239e5f`)<br>`v80/captures/v80/v80-nested6-with-feed-v1/attempt-v2/native-series-v1.json` (SHA256 `2b186d168b9694eec404e5c3891e26b64c582bc705ef1878b09741d8bef56e48`)<br>`v80/captures/v80/v80-nested6-with-feed-v1/attempt-v2/native-v1.csv` (SHA256 `65834e142bbee64dfccc00b5da76134d8a38c2c29c521a85ca113e822ee8b106`)<br>`v80/captures/v80/v80-nested6-with-feed-v1/attempt-v2/observation-v3.json` (SHA256 `e1e728ddb8a4c569f0d8bff0e375fcf74c5a790d60e368d54d9acb2c7f025109`) |
| `v80-requested-daily-export-v1/attempt-v1` | CONTEXT-UNMET / EXCLUDED / p4250m / `80997aafc3e89b87d76b9d4a31d93391485f3dbc` | 59 / `fcc4eaca5eb7094284c6b389fd54504abd61a0ca` | RUNS; Exploratory All data action selected 1M; no 1D provider or parity credit. | No per-attempt fixture entry; see selected provider/provenance bindings below. |
| `v80-requested-daily-export-v1/attempt-v2` | SUPPLEMENTARY / NOT SCORED / p4250m / `80997aafc3e89b87d76b9d4a31d93391485f3dbc` | 59 / `fcc4eaca5eb7094284c6b389fd54504abd61a0ca` | RUNS; Short 300-row 1D observation is superseded by selected full provider attempt-v3. No independent engine comparison or fixture-consumption credit. | No fixture entry; retained raw native context only. |
| `v80-requested-daily-export-v1/attempt-v3` | CONSUMED / CLOSED-W / p4250m / `80997aafc3e89b87d76b9d4a31d93391485f3dbc` | 59 / `fcc4eaca5eb7094284c6b389fd54504abd61a0ca` | RUNS; Recorded original/observer closed-W comparison or selected independent daily input. Only actual consumed fixture files promoted. | `v80/captures/v80/v80-requested-daily-export-v1/attempt-v3/native-series-v1.json` (SHA256 `7d0f5217617e9a27b89a95f034dc16d51424e495a94f12a967199761812487fc`)<br>`v80/captures/v80/v80-requested-daily-export-v1/attempt-v3/native-v1.csv` (SHA256 `d5ffde65d3bfa492d33434bfde6df6a66b861fd145e727adf4e2f8d6139f37f3`) |

## Receipt authority v2

- `/home/sam/cs/docs/tealscript-parity-archive/ledger/v80-nested6-p4250m-v1/FREEZE-v2.json` (SHA256 `46600132aeb98020ee8ef757a0b6dbc0ef87a090304cd33b9f86ffd01c027f08`).
- `/home/sam/cs/docs/tealscript-parity-archive/ledger/v80-nested6-p4250m-v1/QA-DELTA-w0bo0b-v1.md` (SHA256 `0db631635e09ca210cc8363ddedfb3e36c241ed6e043b2a0ddb58a3886da1f35`).
- `/home/sam/cs/docs/tealscript-parity-archive/ledger/restart-20261006/integration-batch59-v1/FREEZE-v2.json` (SHA256 `491ccc8e049460250f72a67a5be7cdda4982a5b62973c3b6342eabddd62a89de`).
- `/home/sam/cs/docs/tealscript-parity-archive/ledger/restart-20261006/integration-batch59-v1/PUSH-v1.json` (SHA256 `fb2b00c14f65bdd995535cf09f147a410f9d8b59f834bd1cb845ca41ffb1ea69`).
- `/home/sam/cs/docs/tealscript-parity-archive/ledger/restart-20261006/integration-batch59-v1/FINISH-v1.json` (SHA256 `b070510a285f25b973df24e8444696ff775bd28ee448e14025168aea045a5079`).

## Actually consumed v80 fixture set v2

- `v80/captures/v80/daily-provider-v1.json` (SHA256 `f42879f883feaa4844ed011c020952f7f5424b1786d93dc89ccbe85de81e2a2b`).
- `v80/captures/v80/environment-v1/chart-context-before-v1.json` (SHA256 `2470b5826a35a629a16e20075011fc54520aea3fe7b85948b21a6404c652b745`).
- `v80/captures/v80/feed-identity-audit-v1.json` (SHA256 `e33337c71d36035eb044c297708bddd6ac1cd6220908d175b081be1d52849e11`).
- `v80/captures/v80/library-reference-v1/published-source-v1.pine` (SHA256 `8dc9dc0eeb426d19aa36c90451c3ba8e9c3baf9b7beaef879d348529d8e26d6a`).
- `v80/captures/v80/row-masks-v1.json` (SHA256 `6f92d3e91ecfc9c81d8e5c37203ed2a3bdff530e94cfa203477f2680c55ca668`).
- `v80/captures/v80/v80-nested6-original-v1/attempt-v1/executed-v1.pine` (SHA256 `ba47e1d4264c7ff00fd555125dddaa75c557db495e02388aad7beff8246dd008`).
- `v80/captures/v80/v80-nested6-original-v1/attempt-v1/native-v1.csv` (SHA256 `0cdf4631f413f56ce0165da6acb015f066d1a4ee61f659ada0b46468ff523702`).
- `v80/captures/v80/v80-nested6-original-v1/attempt-v1/observation-v3.json` (SHA256 `d5cad9a08634e963ed4d468fc5200645fca6f3cd473d0e3d9c6d97f5f122ec25`).
- `v80/captures/v80/v80-nested6-with-feed-v1/attempt-v1/executed-v1.pine` (SHA256 `a18d8d1607f3b4d5aff88d6b46270f30af9dc88478ea66d9621822f93f239e5f`).
- `v80/captures/v80/v80-nested6-with-feed-v1/attempt-v1/native-v1.csv` (SHA256 `d8de685995bde4de9579a4958eabe2f750fcd3c63cd3b1c34a3014b3cf4510f8`).
- `v80/captures/v80/v80-nested6-with-feed-v1/attempt-v1/observation-v3.json` (SHA256 `09b56e008eb3759a3469e03d4bb97ae3cbdcbd07b01ab62eb0c1de79ab3ca9a3`).
- `v80/captures/v80/v80-nested6-with-feed-v1/attempt-v2/executed-v1.pine` (SHA256 `a18d8d1607f3b4d5aff88d6b46270f30af9dc88478ea66d9621822f93f239e5f`).
- `v80/captures/v80/v80-nested6-with-feed-v1/attempt-v2/native-series-v1.json` (SHA256 `2b186d168b9694eec404e5c3891e26b64c582bc705ef1878b09741d8bef56e48`).
- `v80/captures/v80/v80-nested6-with-feed-v1/attempt-v2/native-v1.csv` (SHA256 `65834e142bbee64dfccc00b5da76134d8a38c2c29c521a85ca113e822ee8b106`).
- `v80/captures/v80/v80-nested6-with-feed-v1/attempt-v2/observation-v3.json` (SHA256 `e1e728ddb8a4c569f0d8bff0e375fcf74c5a790d60e368d54d9acb2c7f025109`).
- `v80/captures/v80/v80-requested-daily-export-v1/attempt-v3/native-series-v1.json` (SHA256 `7d0f5217617e9a27b89a95f034dc16d51424e495a94f12a967199761812487fc`).
- `v80/captures/v80/v80-requested-daily-export-v1/attempt-v3/native-v1.csv` (SHA256 `d5ffde65d3bfa492d33434bfde6df6a66b861fd145e727adf4e2f8d6139f37f3`).

Every listed fixture matches locked bytes/hash. Requests and raw captures remain in oracle; no raw captures copied into application source.
