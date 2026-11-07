# Tasks: Release 1 install and update

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../index.md)

This records the R1 merge started by the owner on 4 Nov 2026. It is coordinated separately from the initiative by the Release 1 merge coordinator and lane managers. Detailed decisions, failure history, and run evidence remain in the [R1 merge docs](https://github.com/hannahsubmarine/repo/tree/claude/jolly-feynman-l6ckx7/docs/merge-plan): `R1-PLAN.md`, `DECISIONS.md`, and `status/FAILURES.md`. Preserve that run's accepted scope, review state, and authority. This plan authorizes no other work. Deferred work goes to [Plan 09](../09-install-and-update-confidence/plan.md).

## Task index

| Task / outcome | Route | Depends on | Progress |
|---|---|---|---|
| [R0 boundary pieces A–C: stop, register, adopt](#r0-boundary-pieces-ac-stop-register-adopt) | X | — | Complete |
| [Strict gate of five direct rows; Pinokio deferred](#strict-gate-of-five-direct-rows-pinokio-deferred) | N | — | Complete |
| [Install-check identity by candidate self-consistency; retain R0 pins](#install-check-identity-by-candidate-self-consistency-retain-r0-pins) | N | — | Complete |
| [Upgrade-leg cleanup checks post-upgrade uninstall refusal](#upgrade-leg-cleanup-checks-post-upgrade-uninstall-refusal) | N | Strict gate | Open |
| [Update step: generator and three-OS steps](#update-step-generator-and-three-os-steps) | N / X / X | Strict gate | Open |
| [Windows upgrade refusal text printed by installer](#windows-upgrade-refusal-text-printed-by-installer) | N | — | Open |
| [One-command pin bump, then one strict run](#one-command-pin-bump-then-one-strict-run) | N | All preceding tasks | Open |
| [Owner ship call](#owner-ship-call) | — | Strict run | Open |

## Task details

### R0 boundary pieces A–C: stop, register, adopt

- **Outcome:** Stop R0 through its service manager and wait for `owner.lock`; adopt a read-only copy at `<old>-r1` (clone, otherwise hard-link the write-once CAS store); register R1 under a new service label with a fixed launcher; and roll back by disabling R1's label and re-enabling R0.
- **Route:** `X`.
- **Dependencies and inputs:** R0 served release and four `int/r1` integration heads; see [inputs](inputs.md#starting-code).
- **Work:** Preserve the R0 boundary and the recorded A–C implementation.
- **Focused checks:** Existing landed data checks; Linux and macOS upgrade rows reach the install checks.
- **Done / progress:** Recorded landed with data checks; complete.

### Strict gate of five direct rows; Pinokio deferred

- **Outcome:** Keep the R1 ship gate to exactly `direct-linux`, `direct-macos`, `direct-linux-fresh`, `direct-macos-fresh`, and `direct-windows`, as defined by `scripts/journey_matrix.py` `RELEASE1_MATRIX`, `.github/workflows/journey.yml`, and `scripts/check_journey_evidence.py`.
- **Route:** `N`.
- **Dependencies and inputs:** R1 integration candidate; hosted GitHub runners `ubuntu-24.04`, `macos-15`, and `windows-2022`; see [inputs](inputs.md#references-and-evidence).
- **Work:** Keep the strict gate's existing five direct rows. Pinokio rows/routes remain in [Plan 07](../07-pinokio/plan.md).
- **Focused checks:** Gate requires exactly those five job IDs; final acceptance is the one strict hosted run on all five rows at frozen heads.
- **Done / progress:** Exact five-job gate recorded; complete.

### Install-check identity by candidate self-consistency; retain R0 pins

- **Outcome:** Verify `runtime.identity` against the candidate itself while leaving R0 pins unchanged.
- **Route:** `N`.
- **Dependencies and inputs:** Candidate and existing R0 pin arrangement; see [inputs](inputs.md#starting-code).
- **Work:** Preserve candidate self-consistency rather than changing the R0 pin basis.
- **Focused checks:** `runtime.identity` passes on all three OS rows.
- **Done / progress:** Recorded passing on all three rows; complete.

### Upgrade-leg cleanup checks post-upgrade uninstall refusal

- **Outcome:** Assert that uninstall after an R0-to-R1 upgrade refuses and preserves both data folders.
- **Route:** `N`.
- **Dependencies and inputs:** Strict gate; Linux/macOS R0 upgrade rows.
- **Work:** Add the cleanup assertion to both upgrade legs.
- **Focused checks:** `direct-linux` and `direct-macos` reach passing `final_cleanup` evidence.
- **Done / progress:** Both row results are still required; open.

### Update step: generator and three-OS steps

- **Outcome:** Generate a same-code stand-in release at release + 1 and apply it by rerunning the public install line.
- **Route:** Generator `N`; Linux/macOS step `X`; Windows step `X`.
- **Dependencies and inputs:** Strict gate and the four integration heads; see [inputs](inputs.md#starting-code).
- **Work:** On each fresh row, assert a new version directory, switched `current` pointer, retained old version, healthy service under the same label, intact data, then rerun install checks and the task after update.
- **Focused checks:** Update evidence passes on all three fresh rows, and `scripts/check_journey_evidence.py` requires the update section.
- **Done / progress:** All three fresh-row update results remain required; open.

### Windows upgrade refusal text printed by installer

- **Outcome:** Print the safe R0-to-R1 upgrade refusal from the installer on Windows.
- **Route:** `N`.
- **Dependencies and inputs:** None beyond the Windows direct row; see [inputs](inputs.md#starting-code).
- **Work:** Preserve refusal behavior for the unsupported Windows upgrade route.
- **Focused checks:** `direct-windows` refusal check passes.
- **Done / progress:** Refusal evidence remains required; open.

### One-command pin bump, then one strict run

- **Outcome:** Bump Agent and App locks once to verified heads and run the strict gate once at frozen heads.
- **Route:** `N`.
- **Dependencies and inputs:** All preceding tasks and their verified candidate heads; exact SHAs are frozen at run time and recorded per landing in the merge fixes log.
- **Work:** Make the single coordinated lock update, then execute the five-row strict gate. The bump is two steps: Agent `runtime.lock` first, then the App manifest pinned to the new Agent commit (`scripts/regenerate_runtime_pins.py` with `--agent-sha`). Chain them in one command (R1.1).
- **Focused checks:** Strict hosted run passes on all five rows at those frozen heads. Use the accepted run's recorded command and evidence; this migration does not invent a selector or report a result.
- **Done / progress:** Pin bump and strict run remain to be completed; open.

### Owner ship call

- **Outcome:** Record the owner's decision after the strict run.
- **Route:** —.
- **Dependencies and inputs:** Strict run evidence and the existing owner authority.
- **Work:** Record the ship decision and accepted destination in the existing R1 run record.
- **Focused checks:** Owner decision is recorded; no additional approval stage is introduced.
- **Done / progress:** Decision remains outstanding; open.

## Focused evidence and limitations

The original scope specifies each landing's own focused tests plus the five journey rows; it does not name the landing selectors here. Use the selectors and exact commands recorded in the active R1 run rather than inferring test names. No broad suites are in scope.

The completion boundary and authority limits are described in the [plan](plan.md#completion). In particular, an R0 upgrade stops a busy R0 via its service manager and interrupts an in-flight task while leaving stored data untouched; legacy R0 tools can still write R0's own root, though R1 never does. Windows R0-to-R1 upgrade safely refuses, so Windows users reinstall. Post-upgrade uninstall refuses and retains both data folders. The same-code stand-in proves update mechanics, not a real schema migration.
