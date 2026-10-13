# Oracle round v88 — requested daily counter discriminator handoff v1

**ALLOWED: Save as a PRIVATE unpublished script, Add to chart, then remove only the request-added study. FORBIDDEN: publish/share, visibility change, new layout, symbol/interval change to any saved layout, alerts, or any library action. Anything beyond this authorized method: STOP as BLOCKED-NEEDS-OWNER-APPROVAL.**

Two indicator sources, **v5 plus v6 control**, each captured **twice** on **BINANCE:BTCUSDT1D**. Read [instructions/INSTRUCTIONS-v1.md](instructions/INSTRUCTIONS-v1.md). Both use request.security(syminfo.tickerid,"1D",...,lookahead=barmerge.lookahead_on). Required context must be available without creating a layout or changing any saved layout's symbol/interval; otherwise STOP BLOCKED-NEEDS-OWNER-APPROVAL.

Per requested bar export time,index,isfirst,timeframe.change("1D"),its missing mask and the var counter. Carried first-evaluation time/index/isfirst/change/missing/counter distinguish a cropped chart export from the actual requested calculation frontier. Preserve native daily OHLCV and every numeric string/empty cell; record closed-row masks and developing-row cutoff. All native outcomes are **UNSPECIFIED**.

| Source | Bytes | SHA256 | Captures |
|---|---:|---|---:|
| [v88-v5-requested-daily-counter-p4250m-v1.pine](v88-v5-requested-daily-counter-p4250m-v1.pine) | 2454 | `630e6784cb7e27585b74bf864d6a1b99c722c7882d113b6ecaec8a39b9337864` | 2 |
| [v88-v6-requested-daily-counter-p4250m-v1.pine](v88-v6-requested-daily-counter-p4250m-v1.pine) | 2433 | `5177d6d738e1f4bdf9339c6fc0374826b76ebc877de78b386f053537a983021b` | 2 |

Original affected source SHA256 `d91765c9517a779ff170b0b6632d4941fac93206a3c48be8015b4758e5d6cf20`; native v4 corpus5-pivot-request-counter-v1. The measured +1 across24545closedcells motivates this question but is not an expected answer or a counter seed. No pivot-array/runtime provider reconstruction is claimed by these minimal discriminators. No library action is needed.

Run `sha256sum -c SHA256SUMS` in v88/. Return v88/captures/v88/RESPONSE-v88-v1.md with four independent attempts and first-requested-bar evidence. Save privately,Add,export through the existing permitted path,remove only request-added studies. No publish/share/visibility/layout/alerts/library action. Incomplete first history is a hold,not evidence for a guessed initialization fix.
