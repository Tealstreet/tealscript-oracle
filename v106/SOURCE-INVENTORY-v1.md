# V106 exact source inventory v1

Oracle baseline `12bc8a2625ba8fb4631ea427826a8351269a9b77`. Four new v5 sources, four visual facets, 37 literal plot calls and a prospective 1,184 primary cells including context/intentional blanks. Native outcomes UNSPECIFIED.

| Slot | Exact title / source | Bytes | SHA256 | Plots |
| ---: | --- | ---: | --- | ---: |
| 1 | [v106-table-survival-v5](sources/v106-table-survival-v5.pine) | 1534 | `eb893cbc2b1b80322b86b59f5aabdfb9031b7306445b3f3915b8376f70b2a170` | 10 |
| 2 | [v106-table-relocation-v5](sources/v106-table-relocation-v5.pine) | 1296 | `9d8cbbd919acf24bd253a621b69986f3b8671b976007204eaa3e356c288173dd` | 9 |
| 3 | [v106-table-frame-v5](sources/v106-table-frame-v5.pine) | 1554 | `ad41f925347fdb5bcafeea53034fec6739a5d5b1c942d4f8c1eb612d95ba60db` | 9 |
| 4 | [v106-table-merge-v5](sources/v106-table-merge-v5.pine) | 1603 | `9c6633fd0944a505af2f98ca39b5d11db6f0020141e371503f133c222791b9b4` | 9 |

## v106-table-survival-v5

Source-order plots: 0:TABLE_COUNT, 1:OLD_NA, 2:INPUT_INDEX, 3:INPUT_TIME, 4:CHART_CONFIRMED, 5:CASE_ID, 6:VISUAL_ANCHOR_INDEX, 7:VISUAL_ANCHOR_TIME, 8:SCALE_LOW, 9:SCALE_HIGH.

Facet: `v106-table-survival-v5:same-position-lifetime`. Prior source `v105/sources/v105-table-survival-v5.pine`, SHA256 `53d74858a26c6e3cbce7c4e1412d5aa3ad92050b19fab34fdd3a3c366e8d3ee2`. Modified title/positions only; all other bytes and order unchanged. New private script/version/session required.

Build-event numeric witnesses: {"TABLE_COUNT": {"expression": "array.size(table.all)", "role": "build-event lifetime observation only; native result unspecified, no appearance credit", "anchorExpected": "UNSPECIFIED"}, "OLD_NA": {"expression": "na(a) ? 1 : 0", "role": "build-event handle observation only; no survival-paint credit", "anchorExpected": "UNSPECIFIED"}}. No visual credit from counts/handles.


## v106-table-relocation-v5

Source-order plots: 0:TABLE_COUNT, 1:INPUT_INDEX, 2:INPUT_TIME, 3:CHART_CONFIRMED, 4:CASE_ID, 5:VISUAL_ANCHOR_INDEX, 6:VISUAL_ANCHOR_TIME, 7:SCALE_LOW, 8:SCALE_HIGH.

Facet: `v106-table-relocation-v5:final-position`. Prior source `v105/sources/v105-table-relocation-v5.pine`, SHA256 `070fa78f0f606b14b1d19f7a90b0b412d202f26bc93cfaff6fe0e21521b31afb`. Modified title/positions only; all other bytes and order unchanged. New private script/version/session required.

Build-event numeric witnesses: {"TABLE_COUNT": {"expression": "array.size(table.all)", "role": "build-event lifetime observation only; native result unspecified, no appearance credit", "anchorExpected": "UNSPECIFIED"}}. No visual credit from counts/handles.


## v106-table-frame-v5

Source-order plots: 0:TABLE_COUNT, 1:INPUT_INDEX, 2:INPUT_TIME, 3:CHART_CONFIRMED, 4:CASE_ID, 5:VISUAL_ANCHOR_INDEX, 6:VISUAL_ANCHOR_TIME, 7:SCALE_LOW, 8:SCALE_HIGH.

Facet: `v106-table-frame-v5:frame-border-paint`. Prior source `v105/sources/v104-table-frame-v5.pine`, SHA256 `2efb2ee771728ce469ec9f36b8eb8bf9e0d160927739aa7dd3874e4c0af7fd82`. Modified title/positions only; all other bytes and order unchanged. New private script/version/session required.

Build-event numeric witnesses: {"TABLE_COUNT": {"expression": "array.size(table.all)", "role": "build-event lifetime observation only; native result unspecified, no appearance credit", "anchorExpected": "UNSPECIFIED"}}. No visual credit from counts/handles.


## v106-table-merge-v5

Source-order plots: 0:TABLE_COUNT, 1:INPUT_INDEX, 2:INPUT_TIME, 3:CHART_CONFIRMED, 4:CASE_ID, 5:VISUAL_ANCHOR_INDEX, 6:VISUAL_ANCHOR_TIME, 7:SCALE_LOW, 8:SCALE_HIGH.

Facet: `v106-table-merge-v5:merged-row`. Prior source `v105/sources/v104-table-merge-v5.pine`, SHA256 `f4ca586354bd444194e7eb90e44592e73c1c145701d3c5047667f97ee312d892`. Modified title/positions only; all other bytes and order unchanged. New private script/version/session required.

Build-event numeric witnesses: {"TABLE_COUNT": {"expression": "array.size(table.all)", "role": "build-event lifetime observation only; native result unspecified, no appearance credit", "anchorExpected": "UNSPECIFIED"}}. No visual credit from counts/handles.
