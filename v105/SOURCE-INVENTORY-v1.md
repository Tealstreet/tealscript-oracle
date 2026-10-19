# V105 exact source inventory v1

Oracle baseline `04a6378c310ef405448e5eea719bf4bc0e699e1a`. Native outcomes UNSPECIFIED. Five independent source slots, four v5/one v6; eight visual facets; 51 plot calls, prospective 1632 primary cells including context and intentional blanks.

| Slot | Slot identity | Exact indicator/source identity | Bytes | SHA256 | Plots |
| ---: | --- | --- | ---: | --- | ---: |
| 1 | v105-alpha-composite-v6 | [v105-alpha-composite-v6](sources/v105-alpha-composite-v6.pine) | 4424 | `1256da2a975e8c87c8b605e10a93d2a3bb916eb0f1c053721e1d4f2b1c7f459c` | 14 |
| 2 | v105-table-survival-v5 | [v105-table-survival-v5](sources/v105-table-survival-v5.pine) | 1529 | `53d74858a26c6e3cbce7c4e1412d5aa3ad92050b19fab34fdd3a3c366e8d3ee2` | 10 |
| 3 | v105-table-relocation-v5 | [v105-table-relocation-v5](sources/v105-table-relocation-v5.pine) | 1292 | `070fa78f0f606b14b1d19f7a90b0b412d202f26bc93cfaff6fe0e21521b31afb` | 9 |
| 4 | v105-table-frame-v5 | [v104-table-frame-v5](sources/v104-table-frame-v5.pine) | 1552 | `2efb2ee771728ce469ec9f36b8eb8bf9e0d160927739aa7dd3874e4c0af7fd82` | 9 |
| 5 | v105-table-merge-v5 | [v104-table-merge-v5](sources/v104-table-merge-v5.pine) | 1601 | `f4ca586354bd444194e7eb90e44592e73c1c145701d3c5047667f97ee312d892` | 9 |

## v105-alpha-composite-v6

Source-order plots: 0:BLUE50_R, 1:BLUE50_B, 2:BLUE50_T, 3:RED50_R, 4:RED50_B, 5:RED50_T, 6:INPUT_INDEX, 7:INPUT_TIME, 8:CHART_CONFIRMED, 9:CASE_ID, 10:VISUAL_ANCHOR_INDEX, 11:VISUAL_ANCHOR_TIME, 12:SCALE_LOW, 13:SCALE_HIGH.

Facets: `v105-alpha-composite-v6:fill-over-fill`, `v105-alpha-composite-v6:fill-over-background`, `v105-alpha-composite-v6:line-over-line`, `v105-alpha-composite-v6:line-over-background`.

Previous exact source `v104/sources/v104-alpha-composite-v6.pine`, SHA256 `b30dc532bad869957a3299a30afb8300d50f2252d67ef85da5c6510b3a88659b`; unchanged bytes: False.

Numeric witnesses: {"BLUE50_R": {"expression": "color.r(blue50)", "role": "per-row source color channel; no compositing-paint credit", "everyPrimaryExpected": 0}, "BLUE50_B": {"expression": "color.b(blue50)", "role": "per-row source color channel; no compositing-paint credit", "everyPrimaryExpected": 255}, "BLUE50_T": {"expression": "color.t(blue50)", "role": "per-row source color channel; no compositing-paint credit", "everyPrimaryExpected": 50}, "RED50_R": {"expression": "color.r(red50)", "role": "per-row source color channel; no compositing-paint credit", "everyPrimaryExpected": 255}, "RED50_B": {"expression": "color.b(red50)", "role": "per-row source color channel; no compositing-paint credit", "everyPrimaryExpected": 0}, "RED50_T": {"expression": "color.t(red50)", "role": "per-row source color channel; no compositing-paint credit", "everyPrimaryExpected": 50}}. All analytical inputs/intent remain separate from native paint and handle observations.

## v105-table-survival-v5

Source-order plots: 0:TABLE_COUNT, 1:OLD_NA, 2:INPUT_INDEX, 3:INPUT_TIME, 4:CHART_CONFIRMED, 5:CASE_ID, 6:VISUAL_ANCHOR_INDEX, 7:VISUAL_ANCHOR_TIME, 8:SCALE_LOW, 9:SCALE_HIGH.

Facets: `v105-table-survival-v5:same-position-lifetime`.

Previous exact source `v104/sources/v104-table-survival-v5.pine`, SHA256 `8849cf5ec18f778bb193e97ff471479b002d151a59194cc9eb2bc49bdcb0cc13`; unchanged bytes: False.

Numeric witnesses: {"TABLE_COUNT": {"expression": "array.size(table.all)", "role": "build-event lifetime observation only; native result unspecified, no appearance credit", "anchorExpected": "UNSPECIFIED"}, "OLD_NA": {"expression": "na(a) ? 1 : 0", "role": "build-event handle observation only; no survival-paint credit", "anchorExpected": "UNSPECIFIED"}}. All analytical inputs/intent remain separate from native paint and handle observations.

## v105-table-relocation-v5

Source-order plots: 0:TABLE_COUNT, 1:INPUT_INDEX, 2:INPUT_TIME, 3:CHART_CONFIRMED, 4:CASE_ID, 5:VISUAL_ANCHOR_INDEX, 6:VISUAL_ANCHOR_TIME, 7:SCALE_LOW, 8:SCALE_HIGH.

Facets: `v105-table-relocation-v5:final-position`.

Previous exact source `v104/sources/v104-table-relocation-v5.pine`, SHA256 `fd160ac84d0321ca444ef3f36b24f813f470e1a524b89b0cc7b39daec72d206a`; unchanged bytes: False.

Numeric witnesses: {"TABLE_COUNT": {"expression": "array.size(table.all)", "role": "build-event lifetime observation only; native result unspecified, no appearance credit", "anchorExpected": "UNSPECIFIED"}}. All analytical inputs/intent remain separate from native paint and handle observations.

## v105-table-frame-v5

Source-order plots: 0:TABLE_COUNT, 1:INPUT_INDEX, 2:INPUT_TIME, 3:CHART_CONFIRMED, 4:CASE_ID, 5:VISUAL_ANCHOR_INDEX, 6:VISUAL_ANCHOR_TIME, 7:SCALE_LOW, 8:SCALE_HIGH.

Facets: `v104-table-frame-v5:frame-border-paint`.

Previous exact source `v104/sources/v104-table-frame-v5.pine`, SHA256 `2efb2ee771728ce469ec9f36b8eb8bf9e0d160927739aa7dd3874e4c0af7fd82`; unchanged bytes: True.

Keep original v104 indicator title and source bytes; create a distinct new PRIVATE unpublished script identity, never overwrite the old script. Separate v105 slot/session identity prevents double-counting. Existing lower-left control occlusion means NOT OBSERVED, without repair.

Numeric witnesses: {"TABLE_COUNT": {"expression": "array.size(table.all)", "role": "build-event lifetime observation only; native result unspecified, no appearance credit", "anchorExpected": "UNSPECIFIED"}}. All analytical inputs/intent remain separate from native paint and handle observations.

## v105-table-merge-v5

Source-order plots: 0:TABLE_COUNT, 1:INPUT_INDEX, 2:INPUT_TIME, 3:CHART_CONFIRMED, 4:CASE_ID, 5:VISUAL_ANCHOR_INDEX, 6:VISUAL_ANCHOR_TIME, 7:SCALE_LOW, 8:SCALE_HIGH.

Facets: `v104-table-merge-v5:merged-row`.

Previous exact source `v104/sources/v104-table-merge-v5.pine`, SHA256 `f4ca586354bd444194e7eb90e44592e73c1c145701d3c5047667f97ee312d892`; unchanged bytes: True.

Keep original v104 indicator title and source bytes; create a distinct new PRIVATE unpublished script identity, never overwrite the old script. Separate v105 slot/session identity prevents double-counting. Existing lower-left control occlusion means NOT OBSERVED, without repair.

Numeric witnesses: {"TABLE_COUNT": {"expression": "array.size(table.all)", "role": "build-event lifetime observation only; native result unspecified, no appearance credit", "anchorExpected": "UNSPECIFIED"}}. All analytical inputs/intent remain separate from native paint and handle observations.
