# 08 — Release 1: install and update

**Start here:** read [AGENTS.md](../AGENTS.md), choose a workflow in the [skills guide](../skills/README.md), follow the [run contract](../skills/astrid-dev-shared/run-contract.md), and look up terms in the [glossary](../docs/glossary.md).

[README queue](../README.md) · [Initiative handoff](MANAGER.md). This plan records the Release 1 (R1) merge that the owner started on 4 Nov 2026. It runs under its own merge coordinator and lane managers, with detailed decisions and evidence in the [R1 merge docs](https://github.com/hannahsubmarine/repo/tree/claude/jolly-feynman-l6ckx7/docs/merge-plan) (`R1-PLAN.md`, `DECISIONS.md`, `status/FAILURES.md`). It doesn't start or authorize any other plan. Deferred work goes to [Plan 09](09-install-and-update-confidence.md).

## Goal

Ship R1 so that a new user can install Astrid on Linux, macOS and Windows and update it to the next version, and an existing Release 0 (R0) user on Linux or macOS can upgrade without losing data, all proven by hosted CI runs.

Preserve R0's data: R1 never writes R0's root, and every unsupported or ambiguous state refuses before changing anything.

## Scope

### In scope

- The strict five-row ship gate (`scripts/journey_matrix.py` RELEASE1_MATRIX, `.github/workflows/journey.yml`, `scripts/check_journey_evidence.py`):
  - `direct-linux`, `direct-macos`: R0 → R1 upgrade, install checks, task, and cleanup asserting the after-upgrade uninstall refusal.
  - `direct-linux-fresh`, `direct-macos-fresh`: fresh install, install checks, task, then an update to a stand-in next version.
  - `direct-windows`: fresh install, install checks, task, update to the stand-in next version, and the R0 → R1 upgrade refusal.
- The R0 boundary upgrade: stop R0 through its service manager and wait for its `owner.lock`; adopt a read-only copy into `<old>-r1` (clone, else hard-link the write-once CAS store); register R1 under a new service label with a fixed launcher; roll back by disabling R1's label and re-enabling R0's.
- The update test: a generated stand-in release (same code, release + 1) applied by re-running the public install line, asserting a new version directory, the switched `current` pointer, the retained old version, a healthy service under the same label, intact data, and the install checks and task after the update.
- One pin bump of Agent and App locks to the verified heads, then one strict run.

### Out of scope / deferred

- Everything in [Plan 09](09-install-and-update-confidence.md), in particular other update routes, update consolidation, rollback fault injection, real version-to-version migrations, Windows upgrade from R0, and uninstall after an upgrade.
- Pinokio rows and routes: [Plan 07](07-pinokio.md).

## Inputs and dependencies

| Input or dependency | Why it matters | Evidence / link |
|---|---|---|
| R1 merge docs | Decisions, the failure ledger and named limitations | [docs/merge-plan](https://github.com/hannahsubmarine/repo/tree/claude/jolly-feynman-l6ckx7/docs/merge-plan) |
| Agent, Runtime, App and Pinokio integration heads | The R1 candidate. Landed work is mirrored fast-forward to each repository's `pre-main` | Integration branch `int/r1` in each repository; freeze exact SHAs in the strict run |
| Hosted GitHub runners (ubuntu-24.04, macos-15, windows-2022) | The strict gate requires hosted provenance | `scripts/check_journey_evidence.py` |

### Starting code and custody

| Field | Value / rule |
|---|---|
| Product repository | astrid-agent, astrid-runtime, astrid-app, astrid-pinokio |
| Starting branch/base | `int/r1` in each repository, recorded per landing in the merge fixes log |
| Reusable donor commits and dirty-work custody | Per landing, in the merge fixes log; no dirty work carried |
| Predecessor output | R0 as served by the public install line (the `served` row in Agent `tests/upgrade/releases.json`) |
| Fresh candidate branch | Lane branches named per landing; none invented here |
| Merge destination | `int/r1`, fast-forward mirrored to `pre-main` |

## Tasks and acceptance

| Task / outcome | Route | Dependency | Focused acceptance evidence | Progress |
|---|---|---|---|---|
| R0 boundary pieces A–C (stop, register, adopt) | X | — | Landed with data checks; Linux and macOS upgrade rows reach the install checks | [x] |
| Strict gate of five direct rows; Pinokio deferred | N | — | Gate requires exactly the five job ids | [x] |
| Install-check identity by candidate self-consistency (R0 pins kept) | N | — | `runtime.identity` passes on all three rows | [x] |
| Upgrade-leg cleanup asserts the after-upgrade uninstall refusal | N | gate | `direct-linux` and `direct-macos` reach `final_cleanup` pass | [ ] |
| Update step (generator, Linux/macOS step, Windows step) | N, X, X | gate | The update section passes on all three fresh rows and the checker requires it | [ ] |
| Windows upgrade refusal text printed by the installer | N | — | `direct-windows` refusal check passes | [ ] |
| One-command pin bump, then one strict run | N | all above | Strict run green on all five rows at frozen heads | [ ] |
| Owner ship call | — | strict run | Recorded owner decision | [ ] |

Focused selectors are each landing's own tests plus the five journey rows. No broad suites.

## Completion and handoff

Done when the strict run passes on all five rows at frozen heads and the owner makes the ship call. Named limitations, also in `R1-PLAN.md`:

- After an R0 → R1 upgrade, uninstall refuses and keeps both data folders.
- Windows R0 → R1 upgrade refuses safely; Windows users reinstall.
- An upgrade stops a busy R0 through its service manager, interrupting an in-flight task; stored data is untouched.
- Legacy R0 tools may still write R0's own root. R1 never writes it.
- The update test uses a same-code stand-in, so it proves update mechanics, not a real schema migration.

Hand all deferred items to [Plan 09](09-install-and-update-confidence.md).
