# Tasks — Agent main green

[Plan](plan.md) · [Inputs](inputs.md)

**Task ids:** `AG-<n>`. Plan 39 row ids (AT1.10, AT1.34 and so on) are kept in brackets where a row carries one, so the history stays traceable. **Critical path:** AG-0 → AG-1 → AG-3, AG-4 → RS1 → AG-9 → AG-10 → R. **Test inventory:** the 321 unit test files and the integration and opt-in files with a failing ID on 22 November ([clusters](inputs.md#failure-clusters-22-november-2026)); AG-0 commits the exact list.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| AG-0 Measure: the per-ID failing list for every Agent workflow on the head `release/<NN>/plan-91` is cut from, with the `darwin native` job re-run to an outcome, grouped by cause | N | the owner's go | read-only; writes `plans/91-agent-main-green/evidence/` | One committed file per workflow and job listing each failing ID with its message; totals equal each job's pytest summary line; the cut commits recorded in [inputs](inputs.md#source-identities) | [ ] |
| AG-1 Safety net: carry the Agent rows SF3a, GL, GL.1, GL.2, K0, K1a and the Agent side of K2/K3 from `release/14/plan-39` onto the plan branch, seal AG-0's list as the ceiling, and get the comparison to pass once on an unchanged tree | X | AG-0 | astrid-agent `.github/workflows/`, `tests/lanes.py`, `tests/test_skip_policy.py`, `scripts/reshape/`, `ci/` | On an unchanged tree the comparison passes; a scratch commit that turns one passing test red fails it; a cancelled shard turns the run red; the stored per-test results count equals each job's summary | [ ] |
| AG-2 Required checks: the Agent's entries in `ci/required-checks.json` (D4), and the list for the owner's branch protection | N | AG-1 | astrid-dev `ci/required-checks.json` (Agent entries only) | The file names every check GitHub shows on the AG-0 run; the owner confirms protection is on for `release/<NN>/main` | [ ] |
| AG-3 The Runtime resolves from the checkout in unit and integration jobs (183 unit IDs), by changing how CI installs it or how the tests locate it, whichever matches what an installed Agent does | X | AG-1 | astrid-agent `.github/workflows/ci.yml`, `.github/workflows/lanes.yml`, `tests/helpers/runtime.py` | The 183 IDs reach their assertions; none of them changes its expectation; the installed-wheel job stays green | [ ] |
| AG-4 CI provides the inputs the tests ask for: pinned Node/esbuild (62), `ASTRID_REMOTION_PROJECT_DIR` (34), staged resources (31), the RunPod lifecycle checkout as a git checkout (8) | N | AG-1 | astrid-agent `.github/workflows/`, test fixtures under `tests/` | Each cluster's IDs reach their assertions; the tests that refuse without explicit inputs still refuse when the input is removed | [ ] |
| AG-5 Diagnose the integration refusal "render and visualize cannot open the result" (249 IDs): one cause, or several, and fix the first | X | AG-4 | astrid-agent `tests/`, the renderer and Remotion test setup | The cause is named with its first-failure boundary; after the fix the IDs it covers pass, and the rest get AG-9 rows | [ ] |
| AG-6 Installer tests follow the copy-only upgrade boundary (72 IDs) [AT1.10; packet R14-P39-18] | X | AG-1 | astrid-agent `tests/test_installer_*.py`, `tests/test_local_install.py` and their fixtures | Each test names the behaviour change it follows; upgrade with existing state, failure recovery and retry are each still exercised | [ ] |
| AG-7 The custody tests import what exists (45 IDs), then residual failures go on the ceiling with Plan 38 as owner (D3) | N | AG-1 | astrid-agent `tests/core/execution/test_runtime_*_custody_d40.py` and their helpers | The 45 IDs collect and run; each still-failing ID is listed with Plan 38 as owner | [ ] |
| AG-8 Timeline fixtures follow the fork native binding schema (18+ IDs) [AT1.34] | N | AG-1 | astrid-agent `tests/sdk/`, `tests/editing_conformance/` fixtures | The IDs pass; the commit or contract that changed the schema is named on the card | [ ] |
| RS1 Review stop after AG-1 to AG-8: re-measure, cluster what is left, re-estimate AG-9; if more than 60 distinct causes remain, split AG-9 into cards before going on (at most 1 round) | S | AG-1 to AG-8 | read-only | Same protocol as R; findings become rows `RS1.<n>`; AG-9 depends on this row | [ ] |
| AG-9 The long tail, one card per cause from RS1, including Plan 39's Agent ceiling rows (AT1.1, AT1.2, AT1.3, AT1.5, AT1.14, AT1.15, AT1.38, AT1.96, AT1.233, R15-1, R15-2), the tests that fail under load (AT11, AT12, AT12.1, AT27, LS-7) and the renderer inputs (AT1.21, AT1.50, AT1.111, AT1.113) | N or X per card | RS1 | per card | Per card: its IDs pass, or are quarantined under the rule with an issue, an owner and an expiry; the ceiling falls by those IDs | [ ] |
| AG-10 Three consecutive green nights on the head of `release/<NN>/main` for every Agent workflow, with the quarantine listed and within age | N | AG-9 | read-only | Three nightly run links on one head, each green, recorded here | [ ] |
| R Review rounds (at most 2, agreed with the owner) | S | all other tasks | read-only | Rounds per the [run contract](../../skills/shared/run-contract.md): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; publishing or closing waits for them | [ ] |

## Taken from Plan 39

These Plan 39 rows and packets are this plan's from 23 November 2026 (D2). Their evidence stays where it is; this plan links it rather than copying it.

| Plan 39 row or packet | Here |
| --- | --- |
| SF3a, GL, GL.1, GL.2, K0, K1a (Agent), K2/K3 (Agent side) | AG-1 |
| AT1.10, R14-P39-18 | AG-6 |
| SF6d (the Agent custody fixture) | AG-7 |
| AT1.34 | AG-8 |
| AT1.1, AT1.2, AT1.3, AT1.5, AT1.14, AT1.15, AT1.38, AT1.96, AT1.233, R15-1, R15-2 | AG-9 |
| AT11, AT12, AT12.1, AT27, LS-7, R14-P39-10 | AG-9 |
| AT1.21, AT1.50, AT1.111, AT1.113 (renderer inputs) | AG-9 or AG-5, as AG-5 finds |
| AT4, AT9 (both done in Release 14) | kept green by AG-10 |

## Estimate

13–25 engineering days, 2–3 weeks elapsed:
- AG-0 to AG-2, 2–3 days;
- AG-3 to AG-5, 1–3 days;
- AG-6 to AG-8, 2–4 days;
- AG-9, 8–15 worker-days, re-estimated at RS1; with about five workers, 1–1.5 weeks elapsed, set by CI time;
- AG-10, three nights at least.

More workers shorten AG-9 only; more CI capacity shortens every step.
