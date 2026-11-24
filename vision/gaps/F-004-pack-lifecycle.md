# F-004 — Pack installation and upgrades aren't yet proven under demanding conditions

**Aspiration:** [Packs are live, portable and extensible](../pillars/liquid-software.md#packs-are-live-portable-and-extensible) (primary) · [Built to be found and reused](../principles/open-by-design.md#built-to-be-found-and-reused) (supporting) · **Assessment:** Open / partial current mechanisms (2026-11-06).

## Desired state

Demanding packs that meet the [live, portable extension contract](../pillars/liquid-software.md#packs-are-live-portable-and-extensible) can be installed, enabled, used, updated, disabled and safely rolled back with their frontend and backend contributions intact. Compatibility, source identity, trust, ownership and project-reference continuity remain understandable and reliable through failures and recovery.

## Current state

Agent has manifest-defined packs with actions, skills, UI and rendering contributions. App has trusted bundled extension lifecycle and editor SDK mechanisms. [Plan 06](../../plans/06-packs/plan.md) explicitly targets pack extraction and reliable installation, trust, transaction, rendering and editor integration. [Plan 11](../../plans/11-threejs-pack/plan.md) is a case of converting a first-party feature into a pack, but is not a generic workspace engine.

## Gap

We haven't tested a diverse set of demanding frontend, backend and combined packs far enough to expose the limits of the extension system. Installation, real use, upgrade, rollback and recovery need integrated, version-pinned proof across dependency, compatibility, trust, failure and project-state boundaries.

## Closure evidence

Run meaningful frontend-only, backend-only and combined packs against real project data, including substantial interactive UI and long-running processing. Demonstrate install, use, update and rollback with pinned source identity; include dependency conflicts, rejected/untrusted contributions, incompatible versions, failed migrations, interruption and recovery without lost project references. Do not claim arbitrary dynamically generated third-party code can run safely without independent isolation evidence.

## Closure approach

Start with a real, local rendering contribution used in an existing project: its exact source and compiled revision must remain identifiable through admission and failure. [Plan 78](../../plans/78-live-custom-element-editing/plan.md) exercises that narrow live editing path. It does not establish isolation for untrusted code or the full lifecycle of demanding packs.

Next, qualify a demanding creative pack that combines two independently authored rendering technologies through ordinary managed artifacts, declared inputs and exact source revisions. [Plan 99](../../plans/99-composable-creative-rendering/plan.md) uses Astrid Video and HyperFrames for that bounded local authoring, use and revision witness with preserved managed references and failed-update recovery; it is not the whole lifecycle or a new general renderer architecture.

Then qualify frontend-only, backend-only and combined packs across installation, update, rollback and interruption, including substantial UI and long-running processing. The remaining broader work is not established by the narrow rendering proof.

## Route to closure

| Step | Plan | Contributes (closure evidence it delivers) | Milestone |
|---|---|---|---|
| 1 | [Plan 78](../../plans/78-live-custom-element-editing/plan.md) | Partial: real project use of a pinned locally authored frontend rendering contribution; failed admission preserves prior selection and project references. | A creator sees a custom element edit in the open editor. |
| 2 | [Plan 99](../../plans/99-composable-creative-rendering/plan.md) | Partial demanding-pack proof: two trusted rendering contributions in one project, declared managed inputs, real use, source revisions and failed-update recovery with old project references intact. Preserve existing supported transfer behavior; full portability qualification remains separate. | A creator authors and combines editable visual effects from two technologies in one timeline. |
| — | unplanned | Meaningful frontend-only, backend-only and combined packs with substantial interactive UI and long-running processing; install, use, update, rollback, pinned identity, dependency conflicts, rejected/untrusted contributions, incompatibility, failed migrations, interruption and recovery without lost references. | — |

Critical path: step 1 → step 2 for the live rendering authoring witness; the remaining broader lifecycle qualification is still unplanned.

## Sources and reassessment

[Plan 06](../../plans/06-packs/plan.md) · [Plan 11](../../plans/11-threejs-pack/plan.md) · [Liquid Software LS-003](LS-003-full-stack-contributions.md) · [Plan 47 — demanding pack tests](../../plans/47-pack-stress-tests/plan.md). F-004 covers **trusted pack lifecycle**, while LS-003 covers **creative composition of capabilities and views**; one need not prove the other.
