# 07 — Pinokio basic: install, run, update and remove

[README queue](../README.md) · [Initiative handoff](MANAGER.md). The first Pinokio increment, shipped as Release 1.1 straight after [Plan 08](08-release1-install-update.md). Its goal is a hosted test proving that a user can install, start, stop, update and remove Astrid through Pinokio on Linux, macOS and Windows without losing data. The full engine, custody and fully-local qualification work moves to [Plan 10](10-pinokio-qualification.md). Decisions and evidence are in the R1 merge docs (`DECISIONS.md`, 5 Nov 2026 "Pinokio for R1").

## Goal

Make the Pinokio backend launcher dependable for the everyday user path, proven by a separate three-row hosted gate. Preserve user data in every case: a failed or refused action leaves the previous working version and all data in place.

## Starting point (5 Nov 2026)

- Pinokio has no users yet, so there is no old-launcher migration or compatibility work, now or later. `astrid-pinokio` `main` ships with R1, and this gate proves it afterwards.
- The six earlier Pinokio rows (`RELEASE1_1_DEFERRED_PINOKIO_MATRIX`) never got past setup (0/6). They mixed the everyday path with engine, custody and fully-local work. They are retired rather than revived; their scope moves to Plan 10.
- Known hosted failures to fix: setup-install ends with "terminated shell" and no inner exit code on macOS and Windows; Windows `npm ci` exits 1 (better-sqlite3); the Linux Worker profile is missing.

## Scope

### In scope

A new gate, separate from the R1 five-row gate (`RELEASE1_1_PINOKIO_MATRIX`, its own checker function and dispatch; `RELEASE1_MATRIX` unchanged). The rows are `pinokio-linux`, `pinokio-macos` and `pinokio-windows`, on hosted runners. Each runs through the Pinokio backend launcher scripts:

1. Install.
2. Start, then check health and run one task.
3. Stop. Only this install's Runtime stops (same root and instance id); any other Runtime on the host is untouched. Start again and check it's healthy.
4. Busy stop: start a task and press Stop while it runs. Start again. The data marker is intact, and the task has either finished or cleanly failed (never stuck or corrupt).
5. Update to the stand-in next release (`scripts/make_standin_release.py`).
6. Start waits for readiness. Health reports the new release, and one task passes.
7. Uninstall.

Fix whatever the gate finds on `int/r1` and fast-forward `main` again.

### Out of scope (Plan 10)

Engine Stop/Quit refusal veto, direct-custody provider, fully-local mode, unknown-state stop.

## Tasks and acceptance

| Task / outcome | Route | Dependency | Focused acceptance evidence | Progress |
|---|---|---|---|---|
| PB-1 Separate three-row gate: matrix constant, checker, dispatch | N | — | Checker requires exactly the three job ids; R1 gate unchanged | [ ] |
| PB-2 Linux row, steps 1–7 | X | PB-1 | Hosted `pinokio-linux` passes | [ ] |
| PB-3 macOS row: capture the real setup-install exit, fix it | X | PB-2 | Hosted `pinokio-macos` passes, or a named limitation | [ ] |
| PB-4 Windows row: setup-install exit, `npm ci` better-sqlite3 | X | PB-2 | Hosted `pinokio-windows` passes, or a named limitation | [ ] |
| PB-END Record the green gate; fast-forward `main` to the verified heads | N | PB-2–4 | Gate green at frozen heads; `main` checked with `git ls-remote` | [ ] |

If PB-3 or PB-4 needs Sol-level digging, stop with the evidence. The coordinator decides, most likely recording a named limitation for that OS.

## Completion and handoff

Done when the three-row gate is green at frozen heads and those heads are on `main`. Record any OS left unsupported as a named limitation here. Hand everything out of scope to [Plan 10](10-pinokio-qualification.md).
