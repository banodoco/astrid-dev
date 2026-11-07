# Tasks: Pinokio basic (R1.1)

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../../README.md)

The six-row `RELEASE1_1_DEFERRED_PINOKIO_MATRIX` is historical, retired evidence: 0/6 passed setup. Do not revive it. The new three-row hosted gate is separate from the R1 five-row gate. Current progress is tracked in this file; status, owner, and estimate remain in the [queue](../../../README.md).

## Task index

| ID / outcome | Route | Depends on | Progress |
|---|---|---|---|
| [PB-1 Separate three-row gate: matrix constant, checker, dispatch](#pb-1-separate-three-row-gate-matrix-constant-checker-dispatch) | N | — | [ ] |
| [PB-2 Linux row, steps 1–7](#pb-2) | X | PB-1 | [ ] |
| [PB-3 macOS row: capture the real setup-install exit, fix it](#pb-3-macos-row-capture-the-real-setup-install-exit-fix-it) | X | PB-2 | [ ] |
| [PB-4 Windows row: setup-install exit, `npm ci` better-sqlite3](#pb-4-windows-row-setup-install-exit-npm-ci-better-sqlite3) | X | PB-2 | [ ] |
| [PB-END Record the green gate; fast-forward `main` to the verified heads](#pb-end-record-the-green-gate-fast-forward-main-to-the-verified-heads) | N | PB-2–PB-4 | [ ] |

## Shared row contract

Each hosted row (`pinokio-linux`, `pinokio-macos`, `pinokio-windows`) uses the Pinokio backend launcher scripts and verifies this exact path:

1. Install.
2. Start; check health and run one task.
3. Stop only this install's Runtime (same root and instance ID); leave any other host Runtime untouched. Start again and check health.
4. Start a task, request Stop while it runs, then start again. Confirm the data marker remains intact and the task either completed or failed cleanly (never stuck or corrupt).
5. Update to the stand-in next release using `scripts/make_standin_release.py`.
6. Wait for readiness on start; confirm health reports the new release and one task passes.
7. Uninstall.

The source task provided no exact hosted workflow job selector or focused command beyond the row IDs and stand-in script. Recover the existing selectors at task setup; do not invent selectors or run broad/auto-discovered suites. Freeze source heads and record them with the gate evidence. Current implementation findings are not yet recorded; the known hosted failures below are historical observations from 5 Nov 2026.

**Stop safety (PB-2 to PB-4):** The launcher stop must never force-kill. It may signal only validated processes of this install, and it fails closed with one refusal. An ordinary preview Stop may refuse; this is accepted. Parked launcher changes are on the M-RT lane branch of `astrid-pinokio`.

## Task cards

### PB-1 Separate three-row gate: matrix constant, checker, dispatch

- **Outcome:** Add a Pinokio-only three-row gate with its own `RELEASE1_1_PINOKIO_MATRIX`, checker function, and dispatch. Keep `RELEASE1_MATRIX` and the R1 five-row gate unchanged.
- **Route:** N.
- **Dependencies and inputs:** None. Confirm current source identity at setup; historical `astrid-pinokio` `main` is not a frozen execution base. See [inputs](inputs.md).
- **Work:** Implement and wire the isolated matrix/checker/dispatch. Required row IDs are exactly `pinokio-linux`, `pinokio-macos`, and `pinokio-windows`.
- **Focused checks:** The existing gate checker must require exactly those three job IDs; inspect that the R1 matrix remains unchanged. Exact command/selector was not supplied and must be recovered at setup.
- **Done:** Evidence shows the isolated checker enforces exactly three IDs and the R1 gate is unchanged. No additional review stage is specified.
- **Progress:** [ ]

### PB-2

**Linux row, steps 1–7.**

- **Outcome:** Pass the complete shared row contract on hosted Linux.
- **Route:** X.
- **Dependencies and inputs:** PB-1; current base and retained integration SHAs TBD at setup. Linux Worker profile was historically missing.
- **Work:** Add/fix the Linux Worker profile and exercise install, start/health/task, isolated normal stop/restart, busy stop/restart with intact marker and clean task outcome, stand-in update/readiness/new release/task, and uninstall.
- **Focused checks:** Hosted `pinokio-linux` row only, plus the gate checker from PB-1. Recover its exact workflow selector at setup.
- **Done:** Hosted `pinokio-linux` passes all seven steps at a frozen head; preserve row logs/evidence and head identity in the project evidence record. No broad suite is specified.
- **Progress:** [ ]

### PB-3 macOS row: capture the real setup-install exit, fix it

- **Outcome:** Make the macOS hosted row pass, or record a specific unsupported-platform limitation with evidence.
- **Route:** X.
- **Dependencies and inputs:** PB-2. Historical failure: setup-install ended with “terminated shell” and no inner exit code.
- **Work:** Capture the actual setup-install exit status, fix the cause on the authorized integration branch, then run the complete shared row contract on hosted macOS.
- **Focused checks:** Hosted `pinokio-macos` row only, plus the gate checker. Recover the exact workflow selector at setup; no exact command was supplied.
- **Done:** Hosted row passes all seven steps, or coordinator records a named limitation based on the captured failure evidence. If this needs Sol-level digging, stop with evidence for the coordinator's decision.
- **Progress:** [ ]

### PB-4 Windows row: setup-install exit, `npm ci` better-sqlite3

- **Outcome:** Make the Windows hosted row pass, or record a specific unsupported-platform limitation with evidence.
- **Route:** X.
- **Dependencies and inputs:** PB-2. Historical failures: setup-install ended with “terminated shell” without the inner exit code; Windows `npm ci` exited 1 in `better-sqlite3`.
- **Work:** Capture the actual setup-install exit status, fix the cause(s) on the authorized integration branch, then run the complete shared row contract on hosted Windows.
- **Focused checks:** Hosted `pinokio-windows` row only, plus the gate checker. Recover the exact workflow selector at setup; no exact command was supplied.
- **Done:** Hosted row passes all seven steps, or coordinator records a named limitation based on captured failure evidence. If this needs Sol-level digging, stop with evidence for the coordinator's decision.
- **Progress:** [ ]

### PB-END Record the green gate; fast-forward `main` to the verified heads

- **Outcome:** Record the three-row result and fast-forward the verified heads to `main` when the gate is green.
- **Route:** N.
- **Dependencies and inputs:** PB-2, PB-3, and PB-4 (including any coordinator-recorded OS limitations); frozen source heads and hosted gate results.
- **Work:** Record row results, frozen heads, and any named unsupported OS; verify the destination `main` heads with `git ls-remote` as required by the original task.
- **Focused checks:** Gate green at the frozen heads; `git ls-remote` confirms the intended `main` heads. No other release or publication step is specified.
- **Done:** Green gate and verified heads on `main`; or preserve named OS limitation and hand off unresolved platform scope to the coordinator. Authority boundary is the original fast-forward task; no plan migration itself authorizes execution.
- **Progress:** [ ]

## Completion and handoff

Complete when all three rows pass at frozen heads and those heads are on `main`. Record any unsupported OS as a named limitation. Hand engine Stop/Quit refusal veto, direct custody, fully-local mode, and unknown-state stop to [Plan 10](../10-pinokio-qualification/plan.md).
