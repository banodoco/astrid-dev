# F-004 — Dependable pack and extension lifecycle

**Applies to:** [Agent-Powered Liquid Software](../pillars/liquid-software.md) · [Open by design](../principles.md#open-by-design) · **Assessment:** Open / partial current mechanisms (2026-11-06).

## Desired state

Artists and agents can discover, install, enable, use, update, disable and safely roll back supported creative packs and their frontend/backend contributions. Compatibility, source identity, trust, ownership and project reference continuity remain understandable and reliable.

## Current state

Agent has manifest-defined packs with actions, skills, UI and rendering contributions. App has trusted bundled extension lifecycle and editor SDK mechanisms. [Plan 06](../../plans/06-packs/plan.md) explicitly targets pack extraction and reliable installation, trust, transaction, rendering and editor integration. [Plan 11](../../plans/11-threejs-pack/plan.md) is a case of converting a first-party feature into a pack, but is not a generic workspace engine.

## Gap

The practical lifecycle of reusable packs across Agent, Runtime and App still needs integrated, version-pinned proof of installation, runtime availability, use, safe upgrade/rollback, and handling of missing/broken contributions.

## Closure evidence

Install a supported pack, discover its declared actions/UI, use it on project data, update and roll back safely with exact pinned source identity; show missing dependencies, rejected/untrusted cases, recovery and no loss of project references. Do not claim arbitrary dynamically generated third-party code can run safely without independent isolation evidence.

## Sources and reassessment

[Plan 06](../../plans/06-packs/plan.md) · [Plan 11](../../plans/11-threejs-pack/plan.md) · [Liquid Software LS-003](LS-003-full-stack-contributions.md). F-004 covers **trusted pack lifecycle**, while LS-003 covers **creative composition of capabilities and views**; one need not prove the other.
