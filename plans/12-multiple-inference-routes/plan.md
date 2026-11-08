# Wan2GP as a second engine on the one generation path

**Vision gaps:** [Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary) · [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (supporting).

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

**Draft; not ready for execution.** Wan2GP becomes the **second engine on the one generation path** that [Plan 32](../32-generation-placement-targets/plan.md) builds. It shares the same Placement, lease and remote-machine route as ComfyUI through VibeComfy, which stays primary, and adds only its own `align` and `execute`. Current status and owner remain in the [project queue](../../README.md).

## Goal and scope

- **Included:**
  - a Wan2GP entry whose manifest says `engine: wan2gp` and names its base environment;
  - Wan2GP's `align` (environment and models on that machine) and `execute` (today an in-process persistent session: `shared.api.init` → `submit_task`, used through `_ManagedWanChildAdapter`, `core/execution/generic_host.py` ~969), returning output files in the job directory;
  - a Linux recipe (today the only recipe is Windows cu128) and a filled models lock (empty today);
  - running it locally and on a RunPod machine through Plan 32's route, with model load and unload inside the engine's `execute`, and models pre-fetched into the storage volume;
  - `wan2gp.generate_video` as an explicit-only video entry (MiniMax H3 stays the default).
- **External process ownership:** attaching to an external server does not transfer ownership of its process or GPU. Never stop or kill a user's server or unload models the route did not load or own.
- **Deferred:** an attached, user-owned Wan2GP instance. It has no endpoint or object_info equivalent, so it waits until one is defined. Also deferred: other inference backends.
- **Still undecided:** hardware and models for the real inference proof; whether the Wan2GP pack is installed by default.

## What we build on

The starting premise is that VibeComfy is already the primary route and some setup and instance-connection infrastructure is reusable. Treat this as unverified until current-source inspection. Map the existing generation contract, pack boundaries, setup paths, and ownership/custody/lease primitives before choosing implementation. The [consistent generation plan](../02-consistent-generation/plan.md) and [pack plan](../06-packs/plan.md) are context to verify at start, not proof of current implementation or source identity.

## Sequence

1. **Scoping and the Linux recipe**, in parallel with Plan 32 T2–T5: map the current Wan2GP pack and its session, then build a Linux recipe and a models lock.
2. **Wiring, after Plan 32 T6:** add `wan2gp` to the one engine table in `run()`, with its `align` and `execute`. Replace the host's Wan2GP-specific branches (`generic_host.py` ~11673, ~12497) with that engine entry.
3. **Real inference:** run Wan2GP locally and on a RunPod machine through the same placement and lease. A warm second job loads nothing new. Prove failure, cancellation and release; controlled failures may use fixtures, but successful inference must be real.
4. **Record unsupported combinations**, and confirm that explicitly selected external inference stays usable.

See [tasks.md](tasks.md) for the draft work outline and [inputs.md](inputs.md) for provenance and source identities to establish.

## Completion

Wan2GP runs a real generation through the same path as ComfyUI, locally and on RunPod, chosen only by `manifest.engine`; VibeComfy remains primary. Focused lifecycle evidence covers failure, cancellation, cleanup/release, and contention. Existing external instances and unrelated loaded models remain untouched, and unsupported hardware, model, or environment combinations are recorded. This draft does not yet define executable tasks, routes, exact selectors, or source identities; those must be scoped before dispatch. Follow the existing [shared run contract](../../skills/astrid-dev-shared/run-contract.md) and its execution/publication authority limits.
