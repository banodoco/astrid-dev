# Multiple inference routes (Wan2GP)

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary).

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

**Draft; not ready for execution.** Provide one shared generation route for VibeComfy (primary) and Wan2GP (additional), with both integrations represented as packs. Current status and owner remain in the [project queue](../../README.md).

## Goal and scope

- **Included:** inspect reusable installation, setup, and instance-connection infrastructure; make both setup paths understandable and usable; run inference through the shared task lifecycle; demonstrate a full Wan2GP installation and connection to an existing Wan2GP instance as separate paths.
- **Lifecycle:** claim the task and required compute resources, load and unload models, execute, handle cancellation, and release resources after success, failure, or cancellation. Reuse existing ownership, custody, and lease primitives first; make the smallest platform change only if they cannot support this lifecycle.
- **External process ownership:** attaching to an external server does not transfer ownership of its process or GPU. Never stop or kill a user's server or unload models the route did not load or own. Explicitly selected external inference remains supported.
- **Deferred:** other inference backends and provider-specific capabilities not needed to establish these routes.
- **Still undecided:** hardware, models, and environment for real inference proof; whether either pack is installed or included by default; reusable setup/connection mechanisms and the smallest supported Wan2GP installation path.

## What we build on

The starting premise is that VibeComfy is already the primary route and some setup and instance-connection infrastructure is reusable. Treat this as unverified until current-source inspection. Map the existing generation contract, pack boundaries, setup paths, and ownership/custody/lease primitives before choosing implementation. The [consistent generation plan](../02-consistent-generation/plan.md) and [pack plan](../06-packs/plan.md) are context to verify at start, not proof of current implementation or source identity.

## Sequence

1. Map current generation, setup, instance connection, ownership/custody, lease, and pack code; identify supported hardware, models, and environments for real inference evidence.
2. Scope the shared lifecycle and focused proof, reusing current primitives where possible.
3. Expose VibeComfy and Wan2GP as packs through the shared route, preserving VibeComfy as primary.
4. Demonstrate Wan2GP full installation and existing-instance connection separately, plus actual inference through both backends. Prove lifecycle failure, cancellation, cleanup/release, and contention; controlled failures may use fixtures, but successful inference must be real.
5. Confirm explicitly selected external inference remains usable and record unsupported combinations.

See [tasks.md](tasks.md) for the draft work outline and [inputs.md](inputs.md) for provenance and source identities to establish.

## Completion

Both packs use the shared lifecycle, VibeComfy remains primary, both Wan2GP setup paths are demonstrated, and real inference succeeds through each backend. Focused lifecycle evidence covers failure, cancellation, cleanup/release, and contention. Existing external instances and unrelated loaded models remain untouched, and unsupported hardware, model, or environment combinations are recorded. This draft does not yet define executable tasks, routes, exact selectors, or source identities; those must be scoped before dispatch. Follow the existing [shared run contract](../../skills/astrid-dev-shared/run-contract.md) and its execution/publication authority limits.
