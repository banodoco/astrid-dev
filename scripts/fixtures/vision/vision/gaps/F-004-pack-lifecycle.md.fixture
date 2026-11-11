# F-004 — Pack installation and upgrades aren't yet proven under demanding conditions

**Applies to:** [Agent-Powered Liquid Software](../pillars/liquid-software.md) (primary) · [Open by design](../principles/open-by-design.md) (supporting) · **Assessment:** Open / partial current mechanisms (2026-11-06).

## Desired state

Artists and agents can discover, install, enable, use, update, disable and safely roll back supported creative packs and their frontend/backend contributions. Compatibility, source identity, trust, ownership and project reference continuity remain understandable and reliable.

## Current state

Agent has manifest-defined packs with actions, skills, UI and rendering contributions. App has trusted bundled extension lifecycle and editor SDK mechanisms. [Plan 06](../../plans/06-packs/plan.md) explicitly targets pack extraction and reliable installation, trust, transaction, rendering and editor integration. [Plan 11](../../plans/11-threejs-pack/plan.md) is a case of converting a first-party feature into a pack, but is not a generic workspace engine.

## Gap

We haven't tested a diverse set of demanding frontend, backend and combined packs far enough to expose the limits of the extension system. Installation, real use, upgrade, rollback and recovery need integrated, version-pinned proof across dependency, compatibility, trust, failure and project-state boundaries.

## Closure evidence

Run meaningful frontend-only, backend-only and combined packs against real project data, including substantial interactive UI and long-running processing. Demonstrate install, use, update and rollback with pinned source identity; include dependency conflicts, rejected/untrusted contributions, incompatible versions, failed migrations, interruption and recovery without lost project references. Do not claim arbitrary dynamically generated third-party code can run safely without independent isolation evidence.

## Sources and reassessment

[Plan 06](../../plans/06-packs/plan.md) · [Plan 11](../../plans/11-threejs-pack/plan.md) · [Liquid Software LS-003](LS-003-full-stack-contributions.md) · [Plan 47 — demanding pack tests](../../plans/47-pack-stress-tests/plan.md). F-004 covers **trusted pack lifecycle**, while LS-003 covers **creative composition of capabilities and views**; one need not prove the other.
