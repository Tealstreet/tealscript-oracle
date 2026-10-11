# Oracle repository guidance

This repository owns native capture requests and evidence, not TealScript engine code. Use `master`. Read the selected round’s handoff before capturing. Preserve imported evidence and source bytes; original monorepo prefixes resolve from this repository root. Never infer native acceptance or values from engine output. Commit compilation/runtime errors as observations with source identity and settings.

The active capture request is v61. Start with `v61/HANDOFF-v61-v1.md`, including its v5 publication prerequisite and separate tuple RHS group. Earlier v59/v60 handoffs and captures remain historical evidence. The v58 intake response is `v58/AGENT-RESPONSE-v1.md`; selected native evidence stays in `v58/captures/v58/attempt-inventory-v9.json`. The root historical `HANDOFF.md` does not identify the active round.

Capture requests and inter-agent responses belong here. Application regression inputs are promoted through a reviewed immutable fixture pin in tealchart/tealstreet-next. Do not install application dependencies or copy this archive into application source trees. No application build or deployment workflow belongs here.

Imported corpus licenses are per-file; do not apply a blanket license or strip attribution. The migration manifest is an inventory of the original import, not a demand to rewrite old evidence when adding new captures.
