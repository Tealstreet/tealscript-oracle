# Oracle probe round v79 — capture handoff v2

Do NOT publish publicly. If a private library cannot be imported in this account, STOP and record BLOCKED-NEEDS-OWNER-APPROVAL instead of publishing publicly.

Seven sources: one Pine v5 library prerequisite plus six v5/v6 consumers. **The capture agent must PUBLISH the supplied library** as a new PRIVATE (unlisted, author-only) Pine v5 library P425PrivateV79v1, version1, using its authenticated TradingView account. Follow the complete publication dialog sequence and description in instructions/INSTRUCTIONS-v2.md; preserve published URL, account/import/version, source bytes/hash and screenshots. Only PRIVATE publication is authorized. Public publication is NOT authorized. If publication or access fails, record CONTEXT-UNMET; do not substitute a v6 library. Do not execute consumer placeholders unbound.

After verifying the immutable v5 publication, run `python3 bind-import-v1.py --publisher ACTUAL_USERNAME --output bound-v1` from this v79 directory. The helper only replaces the publisher token, records template/executed hashes and never publishes. Run both exported-controls consumers before their same-version private calls. Capture all six indicators separately; a private method refusal does not settle a private namespace function. Native outcomes and values remain UNSPECIFIED.

Run `sha256sum -c SHA256SUMS` from this round directory. Read [bundle manifest](bundle-manifest-v2.json), [published instructions](instructions/INSTRUCTIONS-v2.md), [producer entry](instructions/ENTRY-v1.json) and [producer handoff](instructions/PRODUCER-HANDOFF-v1.md). Producer sources/ paths are archival provenance; published sources are at the round root. Producer publication directions are superseded by this owner restriction; Pine source bytes remain unchanged.

| Probe | Source | Role | Version |
| --- | --- | --- | --- |
| `v79-library-v5-v1` | [source](v79-library-v5-v1.pine) | PUBLICATION-PREREQUISITE | v5 |
| `v79-v5-exported-controls-v1` | [source](v79-v5-exported-controls-v1.pine) | exported-controls | v5 |
| `v79-v5-private-receiver-v1` | [source](v79-v5-private-receiver-v1.pine) | private-receiver | v5 |
| `v79-v5-private-function-v1` | [source](v79-v5-private-function-v1.pine) | private-function | v5 |
| `v79-v6-exported-controls-v1` | [source](v79-v6-exported-controls-v1.pine) | exported-controls | v6 |
| `v79-v6-private-receiver-v1` | [source](v79-v6-private-receiver-v1.pine) | private-receiver | v6 |
| `v79-v6-private-function-v1` | [source](v79-v6-private-function-v1.pine) | private-function | v6 |

Return v79/captures/v79/RESPONSE-v79.md with raw observations, exact executed source hashes, complete error/warning/code/site details, original CSVs and confirmed cutoffs where admitted. Requests only; no local engine output is native authority. Do not repair refused inputs.
