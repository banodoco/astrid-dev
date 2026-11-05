# Inputs and provenance

This plan's source notes are historical observations from 5 Nov 2026, not frozen execution bases or fresh remote checks. Record current repository, branch, and full SHA when the existing task is started. This documentation migration does not start work or change authorization, status, scope, acceptance, or publication authority.

## Starting code, retained work, and destination

| Repository | Starting branch + SHA | Retained work / donors | Verified predecessor output | Candidate branch | Intended destination |
|---|---|---|---|---|---|
| `astrid-pinokio` (the historical flat plan says its `main` ships with R1; canonical remote and exact head were not recorded there) | TBD at task start; do not treat the historical `main` observation as current | TBD; identify the shipped R1.1 integration and any retained work at task start | Release 1.1 shipped Pinokio, but the hosted basic path is not yet proven | TBD; confirm authorized integration branch | `main`, as specified by PB-END; verify current target and fast-forward only verified heads |

The separate source audit in [Plan 10 inputs](../10-pinokio-qualification/inputs.md) records a historical `astrid-pinokio` checkout and distinct refs for that qualification work; those identities are not established as this plan's base or donors. Reconfirm all heads and intended integration at execution. Plan 08 is the predecessor release and [Plan 10](../10-pinokio-qualification/plan.md) receives deferred qualification work.

## References and evidence

| Source | What it establishes | Identity or link | Limits / missing information |
|---|---|---|---|
| Original Plan 07 source | Accepted basic Pinokio scope, R1.1 status, exact gate rows, task IDs/routes/dependencies, historical failures, and PB-END publication boundary | `plans/07-pinokio.md` at the documentation repository's original `HEAD`; removed from the working tree after migration | Historical plan content, not current product evidence. Source identity / full Git SHA for product code was absent. |
| R1 merge decision | Decision context and evidence for “Pinokio for R1,” dated 5 Nov 2026 | `DECISIONS.md`, entry titled “Pinokio for R1” (location not given in the source plan; recover at task setup) | The referenced document was not present in the supplied project record; recover before relying on its evidence. |
| R1 hosted gate | Existing five-row gate that must remain unchanged | `RELEASE1_MATRIX` (source code location and exact selector not recorded in source plan) | Current implementation and exact focused checker command must be identified at PB-1 setup. |
| Retired Pinokio matrix | Six earlier Pinokio rows stopped at setup, 0/6, and mixed basic path with qualification work | `RELEASE1_1_DEFERRED_PINOKIO_MATRIX` | Historical failure only; explicitly retired, not reusable passing evidence and not to be revived. |
| New Pinokio gate contract | Separate matrix, checker, dispatch, and exact three hosted job IDs | `RELEASE1_1_PINOKIO_MATRIX`; required IDs: `pinokio-linux`, `pinokio-macos`, `pinokio-windows` | Exact workflow file, command, and selector are missing and must be recovered at task setup. |
| Stand-in next release | Update target for hosted rows | `scripts/make_standin_release.py` | Current file location/behavior and invoking test selector must be confirmed in the frozen source tree. |
| Shared run controls | Route bindings, task setup, source identity and proof conventions | [Shared run contract](../../skills/astrid-dev-shared/run-contract.md) | Follow project-specific scope and existing authorization above it; no route or plan grants execution by itself. |

## Constraints and evidence limits

- Hosted row outcomes must verify the whole seven-step contract in [tasks.md](tasks.md), including that stopping this install leaves other Runtime instances alone and that data survives busy stop and update.
- Historical failure observations: macOS and Windows setup-install reported “terminated shell” without the inner exit code; Windows `npm ci` failed in `better-sqlite3`; Linux lacked a Worker profile. Capture fresh evidence before attributing current failures to these causes.
- A passing basic hosted gate does not qualify engine Stop/Quit refusal veto, direct custody, fully-local operation, or unknown-state stop; those remain in Plan 10.
- Preserve the original execution and publication boundaries. Only the PB-END task describes fast-forwarding verified heads to `main`; confirm actual source and destination heads at execution. This planning migration authorizes no product edits, tests, commits, pushes, workers, providers, GPUs, or hosted runs.
