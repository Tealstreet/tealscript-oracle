# V80 Nested-6 confirmed daily input capture handoff v1

Status: PROBE READY; design only. No engine changes, no native admission/value credit, no publication performed.

Read [instructions](INSTRUCTIONS-v1.md) and [entry](ENTRY-v1.json). Exact sources are in `sources/`; verify their hashes against ENTRY before using them. Native phase, diagnostics and values remain UNSPECIFIED. Publication/binding or feed-identity prerequisites are mandatory, with CONTEXT-UNMET recorded when unmet. The capture agent returns raw observations and the round response; the overseer/integration publisher owns the oracle commit.

The packet is ready for publication as round v80. Local compiler/tests were not run because the task is probe design only. Static source, identity, schema and materialization checks are recorded separately in DESIGN-CHECK-v1.json.
