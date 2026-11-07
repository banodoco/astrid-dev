# F-003 — Creative execution isn't yet dependable end to end

**Applies to:** [A Tool for Artistic Ambition](../pillars/artistic-ambition.md) · [Local-first, cloud-capable](../principles.md#local-first-cloud-capable) · **Assessment:** Open / foundations exist (2026-11-06).

## Desired state

From a declared supported starting environment, a person and their agent can choose a suitable creative capability, connect or install what is needed with clear consent, execute real inference or processing, and receive a correct, editable result in the intended workspace—with understandable failures, cleanup and recovery.

## Current state

Astrid has Runtime execution/task primitives, packs, generation integrations and the video editor. [Plan 02](../../plans/02-consistent-generation/plan.md) aims to establish consistent defaults and pinned stack on fixtures and a fresh Linux CPU setup, **explicitly not real inference**. [Plan 12](../../plans/12-multiple-inference-routes/plan.md) targets real multiple inference routes. [Plan 20](../../plans/20-zero-to-first-image/plan.md) targets a real first generated image on a timeline; [Plan 16](../../plans/16-streamlined-agent-experience/plan.md) improves agent readiness.

## Gap

Reliably going from intent through correct model/provider readiness and task execution to usable creative output has not yet been demonstrated across chosen supported routes and recovery cases.

## Closure evidence

A bounded, explicitly scoped real model execution on an approved environment, with setup/defaults, input/output identity, resource lifecycle, failure/retry/stop and a verified creative result in Astrid. Extend route/platform support only as qualified; realistic user effort and recoverability are measured.

## Sources and reassessment

[Plan 02](../../plans/02-consistent-generation/plan.md) · [Plan 12](../../plans/12-multiple-inference-routes/plan.md) · [Plan 16](../../plans/16-streamlined-agent-experience/plan.md) · [Plan 20](../../plans/20-zero-to-first-image/plan.md). Do not equate fixture checks with real GPU/inference qualification.
