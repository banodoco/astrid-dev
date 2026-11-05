# 09 — Install and update confidence

[README queue](../README.md) · [Initiative handoff](MANAGER.md). Next after [Plan 08](08-release1-install-update.md) (Release 1); it starts from Plan 08's verified output. It doesn't authorize product execution until the owner starts it. Pinokio stays in [Plan 07](07-pinokio.md), and pack updates stay in [Plan 06](06-packs.md) PK-9.

## Goal

Make installing and updating Astrid dependable on Linux, macOS and Windows. Every supported way a user installs, updates, rolls back or removes Astrid is exercised by a real (not mocked) test on each OS, through one update path.

Preserve user data in every case: a failed or unsupported operation leaves the previous working version and all data in place.

## Scope

### In scope

- One update entry point. The install line `--update`, the in-app route (`astrid/installer/local_update.py`), the background job (`update_job.py`) and the App route (`app_update.py`) delegate to one transaction (stage → switch `current` → restart → verify → roll back on failure); `custody.py` is folded in or retired.
- Real hosted tests on all three OSes for:
  - update to a newer release;
  - update while the Runtime is running;
  - rollback after a failed update (fault injected after staging);
  - the in-app update button and the background job, or their removal if the single entry point makes one redundant;
  - re-running the install line (repair);
  - uninstall.
- A real version-to-version update: the previous released R1 updated to the candidate, including a workspace schema migration, with data checked after restart.
- Windows specifics: stop ordering and locked files during an update (`service.py` stop, ~972–983); refuse cleanly when a file is locked.
- Uninstall after an R0 → R1 upgrade, using the verified-program-path rule (R1's label, then R0's, only when each points into its own root).
- Windows upgrade from R0. Low priority: few R0 Windows users. The owner may instead keep the R1 refusal permanently.
- A typed Agent ↔ Runtime control contract (the Runtime CLI schema): retire the Runtime discovery file except as an endpoint hint, and delete R0-era Agent code with no remaining callers.
- Platform breadth for fresh install and update: Linux without a systemd user manager (the unsupervised fallback, `service.py` ~110–127), Intel macOS, Windows 11 Home, non-admin users and Defender.
- Unit-test fakes for `systemctl`, `launchctl` and `schtasks` output replaced by captured real output (the `=> true` vs `=> disabled` bug hit twice in R1).

### Out of scope / deferred

- Pinokio install and update routes and rows: [Plan 07](07-pinokio.md).
- Pack install, update and rollback: [Plan 06](06-packs.md) PK-9.
- The unused Release-2 browser machinery (`scripts/release2_executor.py`, `installed_browser_adapter.py`, the `m4_5` job): retire it unless a task here reuses it.
- Broad unit-suite debt in the Agent repository: recorded as known debt, not fixed here.

## Inputs and dependencies

| Input or dependency | Why it matters | Evidence / link |
|---|---|---|
| Plan 08 output | Starting candidate, the five-row gate and the update step | [Plan 08](08-release1-install-update.md); R1 merge docs |
| Per-OS coverage baseline (5 Nov 2026) | Shows which paths are real-tested, mocked, or untested per OS | Recorded in this plan's task IU-0 at start |
| Plan 01 (installer consent) | Touches the same installer files (`cli.py`, `backend.py`) | Sequence IU-1 against Plan 01 I-02; rebase whichever lands second |

### Starting code and custody

| Field | Value / rule |
|---|---|
| Product repository | astrid-agent (installer, journey); astrid-runtime (control contract, update restart); astrid-app (in-app route) |
| Starting branch/base | Freeze each repository's `pre-main` at start |
| Reusable donor commits and dirty-work custody | Plan 08's update step and stand-in generator; record exact commits at start |
| Predecessor output | Plan 08's verified heads |
| Fresh candidate branch | Record the actual create-only name at execution |
| Merge destination | `pre-main` |

## Tasks and acceptance

| Task / outcome | Route | Dependency | Focused acceptance evidence | Progress |
|---|---|---|---|---|
| IU-0 Freeze sources; record the per-OS coverage baseline (path × OS × real/mocked/none) | N | start | Baseline table in this plan | [ ] |
| IU-1 One update transaction; all routes delegate to it | X | IU-0 | Existing update unit tests pass unchanged; routes share one call path | [ ] |
| IU-2 Hosted update-while-running and rollback-after-failure legs on 3 OSes | X | IU-1 | Each leg passes; the injected failure leaves the old version current and healthy | [ ] |
| IU-3 Real version-to-version update with schema migration | X | IU-1 | Previous R1 → candidate on 3 OSes; data and task intact after restart | [ ] |
| IU-4 Windows locked-file handling during update | X | IU-2 | Update succeeds, or refuses in one sentence with the old version working | [ ] |
| IU-5 In-app and background routes: hosted test, or removal | N | IU-1 | Each kept route has a hosted pass on 3 OSes | [ ] |
| IU-6 Uninstall after R0 → R1 upgrade | N | IU-0 | Hosted upgrade legs assert a clean uninstall | [ ] |
| IU-7 Windows R0 → R1 upgrade, or a permanent refusal (owner decision) | X | IU-1 | Hosted Windows upgrade leg passes, or the refusal is recorded | [ ] |
| IU-8 Agent ↔ Runtime control contract; retire discovery file; delete dead R0 code | S | IU-1 | Contract tests on both sides; no callers of deleted code | [ ] |
| IU-9 Platform breadth (no systemd user manager, Intel macOS, Windows Home / non-admin / Defender) | N | IU-2 | Fresh install + update pass, or a named limitation is recorded | [ ] |
| IU-10 Captured real `systemctl` / `launchctl` / `schtasks` output in unit fakes | N | IU-0 | Fakes match the captured output; tests pass | [ ] |
| IU-END Scoped review and promotion | X | all | Review of the exact candidate; promote to `pre-main` | [ ] |

Each task lists exact test selectors at execution. No broad or repository-wide suites.

## Completion and handoff

Done when the IU-0 coverage table has a real hosted test for every supported path on every OS (or a recorded limitation for that cell), and IU-END promotes the candidate. Record any path left unsupported as a named limitation in this plan.
