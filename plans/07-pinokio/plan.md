# 07 — Pinokio basic: install, run, update and remove

**Start here:** read [AGENTS.md](../../AGENTS.md), choose a workflow in the [skills guide](../../skills/README.md), follow the [run contract](../../skills/astrid-dev-shared/run-contract.md), and look up terms in the [glossary](../../docs/glossary.md).

Prove the everyday Pinokio backend path on hosted Linux, macOS, and Windows through a separate three-row gate. This is the basic R1.1 increment; full engine, custody, and fully-local qualification stays in [Plan 10](../10-pinokio-qualification/plan.md).

## Goal and scope

- **Included:** install, start, health check, task execution, normal and busy stop, restart, update to a stand-in release, and uninstall through Pinokio's backend launcher scripts. Preserve user data, including when an action fails or is refused.
- **Deferred:** engine Stop/Quit refusal veto, direct-custody provider, fully-local mode, and unknown-state stop (Plan 10).
- Pinokio had no users at R1, so no old-launcher migration or compatibility work is needed. The prior six-row deferred Pinokio matrix (`RELEASE1_1_DEFERRED_PINOKIO_MATRIX`) stopped at setup (0/6), mixed basic and qualification scope, and is retired rather than revived.

## What we build on

R1 shipped Pinokio on `astrid-pinokio` `main`, but the basic path is **shipped, not yet proven**. It reuses the installer transaction, locks, Runtime, and data; the Pinokio start/stop supervision (about 1,500 launcher lines), `--update-app` route, uninstall, and foreground Runtime remain untested by a hosted gate. Known issues are setup-install ending with “terminated shell” without an inner exit code on macOS and Windows, Windows `npm ci` failing in `better-sqlite3`, and a missing Linux Worker profile. Current source identities must be confirmed at task start; see [inputs](inputs.md).

## Sequence

1. Add a gate separate from the R1 five-row gate: its own `RELEASE1_1_PINOKIO_MATRIX`, checker, and dispatch; leave `RELEASE1_MATRIX` unchanged (PB-1).
2. Make the Linux row exercise all seven user-path steps; then resolve the macOS and Windows setup failures and run their rows (PB-2–PB-4). Each row is hosted and uses the Pinokio backend launcher scripts.
3. Record the gate result at frozen heads and fast-forward the verified heads to `main` (PB-END). If either platform requires Sol-level investigation, stop with the evidence; the coordinator decides whether to record a named OS limitation.

See [task cards](tasks.md) for routes, dependencies, and focused acceptance evidence.

## Completion

Complete when all three rows pass at frozen heads and those heads are on `main`. Record any unsupported OS as a named limitation. This proves the hosted basic backend path, not the deferred qualification behaviors. PB-END preserves the original publication boundary; this plan does not start execution. See the [shared run contract](../../skills/astrid-dev-shared/run-contract.md) for run controls and route bindings.

## Read next

- [tasks.md](tasks.md): task routes, dependencies, work, acceptance, and progress.
- [inputs.md](inputs.md): source identities, evidence provenance, and unresolved setup details.
- [Project status and owner](../../README.md): queue authority.
