# Tasks: multiple inference routes

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../../README.md)

**Draft outline only; not executable assignments.** The source document specifies intended work and proof, but no task IDs, individual dependencies, difficulty routes, exact selectors, or accepted review rounds. The project number `12` is not an individual task ID. Scope these after inspecting current source; do not infer ready work from the outline below.

## Task index

| Work area | Route | Depends on | Progress |
|---|---|---|---|
| [Scope and deliver the shared inference routes](#intended-work-and-proof) | TBD | Current-source inspection and task breakdown | Draft; not dispatched |

## Intended work and proof

- Map existing generation, setup, instance-connection, ownership/custody, lease, and pack code. Reuse existing primitives rather than introduce a parallel framework.
- Expose VibeComfy and Wan2GP as packs through the shared generation path, keeping VibeComfy primary.
- Demonstrate Wan2GP full installation and connection to an existing instance separately, with real inference through each path; also demonstrate real VibeComfy inference.
- Exercise the shared lifecycle's normal completion, failure, cancellation, cleanup/release, and compute contention. Fixtures may supplement failure checks but cannot replace real successful inference evidence.
- Confirm VibeComfy continues to generate and explicitly selected external inference remains usable. Do not stop or kill an external user's server or unload models the route did not load or own.
- Define narrowly scoped route and pack checks after inspecting the code. Exact selectors are currently unknown; do not invent test names, commands, or routes.

Before dispatch, record actual source identities and retained work in [inputs.md](inputs.md), identify dependencies, assign route tags using the [shared run contract](../../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings), and verify the intended candidate and `pre-main` destination. No implementation or publication is authorized by this draft. Preserve the existing authority boundary and review policy in the [shared run contract](../../../skills/astrid-dev-shared/run-contract.md); this plan sets no active review stage or review-round count.
