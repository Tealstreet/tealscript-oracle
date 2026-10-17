# V98 source inventory v1

Four new import-free numeric probes, PRIVATE unpublished saves only. Maximum 4 Save/Add/export sessions, retries0/input variants0, one NEW layout. Run in the order below. From this directory verify `sha256sum -c SHA256SUMS`; manifest paths are repository-root-relative, checksum paths are relative to v98/.

| Source | Bytes | SHA256 | Plot calls/counts |
| --- | ---: | --- | ---: |
| `v98/sources/v98-color-constructors-v5.pine` | 9015 | `718cee58cafa93bcf402485fc0bbf8213f8a0c31e1e496019041b63ce8b7d42c` | 63 |
| `v98/sources/v98-color-constructors-v6.pine` | 8998 | `fba851172d72dbe8d9bd74b08ea4bc7857f57633294493d81e9b2f8cb87aa245` | 63 |
| `v98/sources/v98-color-na-cast-v5.pine` | 5506 | `5a0b9dae7bbfe1692be0df2ba1738d5d6d1831d8e00b2c9c70616ffa554d4663` | 63 |
| `v98/sources/v98-color-na-cast-v6.pine` | 5489 | `c1b586591b542c8e4efaa35c38d5246ea0ad7acc28ba6ccd5f068dd02331574a` | 63 |

All 63 plot columns per source are listed with their zero-based literal source ordinals in [bundle-manifest-v1.json](bundle-manifest-v1.json). Actual native plot IDs/CSV columns must be observed and bound; those source ordinals do not presume native column numbering or hidden colorer values. The four sources have no dynamic plot colors. Their one-line per-file MIT notices license only these new probes.

The constructor pair uses the same 16 transparency cases, literal token palettes and frozen four mathematical byte hypotheses in the manifest and [request](REQUEST-v98-v1.md). The cast pair has nine getter/NA tuples and independently encoded equality/transfer/fallback/gradient controls. The Boolean encoder is intentionally version-specific: v5 preserves missing Boolean as−1; v6 has0/1 and never calls na(bool). Version/title/encoder are the only v5/v6 source differences. No output is copied from TealScript or prior native targets.
