# 07 — Pinokio basic: install, run, update and remove

**Vision gaps:** [Platform reliability](../../visions/gaps/F-001-platform-reliability.md) (primary).

**Start here:** read [AGENTS.md](../../AGENTS.md), choose a workflow in the [skills guide](../../skills/README.md), follow the [run contract](../../skills/astrid-dev-shared/run-contract.md), and look up terms in the [glossary](../../docs/glossary.md).

Prove the everyday Pinokio backend path on hosted Linux, macOS, and Windows through a separate three-row gate. This is the basic R1.1 increment; full engine, custody, and fully-local qualification stays in [Plan 10](../10-pinokio-qualification/plan.md).

## Goal and scope

- **Included:** install, start, health check, task execution, normal and busy stop, restart, update to a stand-in release, and uninstall through Pinokio's backend launcher scripts. Preserve user data, including when an action fails or is refused.
- **Deferred:** engine Stop/Quit refusal veto, direct-custody provider, fully-local mode, and unknown-state stop (Plan 10).
- Pinokio had no users at R1, so no old-launcher migration or compatibility work is needed. The prior six-row deferred Pinokio matrix (`RELEASE1_1_DEFERRED_PINOKIO_MATRIX`) stopped at setup (0/6), mixed basic and qualification scope, and is retired rather than revived.

## What we build on

R1 shipped Pinokio on `astrid-pinokio` `main`, but the basic path is **shipped, not yet proven**. It reuses the installer transaction, locks, Runtime, and data; the Pinokio start/stop supervision (about 1,500 launcher lines), `--update-app` route, uninstall, and foreground Runtime remain untested by a hosted gate. Known issues are setup-install ending with “terminated shell” without an inner exit code on macOS and Windows, Windows `npm ci` failing in `better-sqlite3`, and a missing Linux Worker profile. Current source identities must be confirmed at task start; see [inputs](inputs.md).

**Restarted and shipped on indicative evidence (5 Nov 2026).** The launcher no longer force-stops (astrid-pinokio #12, `main` `7144bc130fbe8c22e33d2dcc698edfaac2a74cfc`): Stop sends SIGTERM (or `taskkill` without `/F`), waits about 5 s, and otherwise refuses once and exits non-zero, leaving the process running. A Runtime busy refusal stays retryable. The owner chose to ship once there was indicative evidence and track the gaps here.

Indicative evidence: hosted `pinokio-linux` driver runs on the astrid-agent lane branch `lane/M-INT/pinokio-rows` (not yet on `main`) against App `57d39bd6`, Agent `9373955d`, Runtime `9fc53b77` and launcher `7144bc13`. Run 42058623476 passed the first four of six steps: install, start and a settled task, graceful stop and restart, and busy stop (one refusal, the same Runtime, the task finished, the retried stop succeeded, data kept). Update and uninstall were not reached in that run.

**Open gaps (remaining Plan 07 work):**

| Gap | Next step |
|---|---|
| Update to the stand-in release and uninstall through Pinokio are not yet proven on a hosted row | Get a full six-step `pinokio-linux` pass (driver fixes for the app-folder layout and the busy task are on the lane branch) |
| macOS and Windows rows not run | Reuse the same driver; replace the dropped macOS-only "other Runtime unchanged" process check with a per-OS one |
| The row driver and `pinokio-row-v1` checker are only on the lane branch | Land them on astrid-agent and re-align the App pins in the same change |
| The real Pinokio app is not exercised by the hosted rows: they run the launcher's own commands, not Pinokio's buttons or `pinokio.js` wiring | macOS: the owner tested the real Pinokio app by hand on 5 Nov 2026 and everything worked. Linux and Windows: not yet checked by hand. A hosted engine-driven row stays in [Plan 10](../10-pinokio-qualification/plan.md) |
| A process that ignores the graceful stop is left running after the refusal | Accepted fail-closed limitation; Plan 10 covers engine Stop/Quit |
| The retired old-launcher Pinokio route (`execute_pinokio_backend`, M4-4a backend checks) is still in astrid-agent | Remove it once nothing selects it |

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
