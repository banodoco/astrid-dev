# Tasks: multiple inference routes

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../README.md)

**Draft outline only; not executable assignments.** The source document specifies intended work and proof, but no task IDs, individual dependencies, difficulty routes, exact selectors, or accepted review rounds. The project number `12` is not an individual task ID. Scope these after inspecting current source; do not infer ready work from the outline below.

## Task index

| Work area | Route | Depends on | Progress |
|---|---|---|---|
| [E1 Make the declared engine protocol the real one](#e1-engine-protocol) | X | Plan 32 T8; Plan 34's first GPU run record | Follow-up; not dispatched. Start after both (owner, 10 Nov) |
| [Scope and deliver the shared inference routes](#intended-work-and-proof) | TBD | E1 (the Wan2GP work builds on it); current-source inspection and task breakdown | Draft; not dispatched |

## Intended work and proof

- Map existing generation, setup, instance-connection, ownership/custody, lease, and pack code. Reuse existing primitives rather than introduce a parallel framework.
- Expose VibeComfy and Wan2GP as packs through the shared generation path, keeping VibeComfy primary.
- Demonstrate Wan2GP full installation and connection to an existing instance separately, with real inference through each path; also demonstrate real VibeComfy inference.
- Exercise the shared lifecycle's normal completion, failure, cancellation, cleanup/release, and compute contention. Fixtures may supplement failure checks but cannot replace real successful inference evidence.
- Confirm VibeComfy continues to generate and explicitly selected external inference remains usable. Do not stop or kill an external user's server or unload models the route did not load or own.
- Define narrowly scoped route and pack checks after inspecting the code. Exact selectors are currently unknown; do not invent test names, commands, or routes.

Before dispatch, record actual source identities and retained work in [inputs.md](inputs.md), identify dependencies, assign route tags using the [shared run contract](../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings), and verify the intended candidate and `pre-main` destination. No implementation or publication is authorized by this draft. Preserve the existing authority boundary and review policy in the [shared run contract](../../skills/astrid-dev-shared/run-contract.md); this plan sets no active review stage or review-round count.

## E1 Engine protocol

**First task; the Wan2GP work below builds on it.** Source: Plan 32 review, 9 Nov, at 7209ffcc7. Priority: High. Route: X.

**When (owner, 10 Nov):** start after Plan 32's completion PR merges and Plan 34's first GPU run is recorded. It changes the same engine code as Plan 32's last fixes and any `plan34/fix-*` branches, and that run's engine-contract findings are an input. Read the run record (`validation/gpu/<date>-<short-sha>.md`) first. Not urgent: it gates only the Wan2GP work below.

- **Work:** make the `generation.engine` protocol (`requirements / align / execute / cancel / probe`, `astrid/packs/generation/extensions/points/engine_protocol.py:16-27`) the one the run site calls: rename what it calls today (`engine.run`, `engine.finish`; `comfyui_engine.py:213-275`) to `execute(job)`, which aligns, runs and writes into `job.out`; implement `cancel` or drop it from the point.
- Have `astrid/core/generation/local_job.py:44,95` pick the engine from the manifest through `entries.engine_table()` instead of importing the vibecomfy action, and have the host admit "the engine's run" rather than only `vibecomfy.run` (`generic_host.py:6984`; the hard-coded `"comfyui"` at `actions/run/run.py:738,754-775,963,979`). Wan2GP's own host branch (`generic_host.py:10430-12392`) is then not a second run path.
- **Proof:** a second (stub) engine runs through local and machine placements with no change to core.
