# Tasks: execution host refactor

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../README.md)

**Release 14 rows (HM1 to HM3) are executable**; the extraction rows are written after HM1, for [Release 15](../../releases/15.md). The rest of this file is the original outline.

## Release 14

Steps 1 and 2 of the [sequence](plan.md#sequence), on astrid-agent `release/14/main` at `fc391dea6` (`astrid/core/execution/generic_host.py`, 18,784 lines). Nothing moves in Release 14. Work lands on `release/14/plan-13` in astrid-agent and astrid-dev.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| HM1 The map: each responsibility in `generic_host.py` (line ranges, public entry points, the module state it reads and writes), its callers in `astrid/` and `tests/`, and the existing tests that exercise it. It proposes the extraction boundaries, names the ones Plan 55 LS-6, LS-7 and LS-8 touch, and where LS-8's resident sessions sit beside the host | X | — | astrid-dev `plans/13-execution-host-refactor/map.md` (new); read-only in astrid-agent | Every top-level definition in the file is in exactly one responsibility (a script's count of definitions matches the map's); every caller named was found by a recorded search; each responsibility lists the tests that reach it, or "none" | [x] 17 Nov: R14-P13-01, `map.md` merged into astrid-dev `release/14/plan-13` at `a62ae1eb` (#822); 188 definitions recounted independently |
| HM2 Characterisation: for each responsibility HM1 marks "none" or thin, focused tests that pin today's behaviour of its public entry points, including lifecycle, cancellation, process ownership and result handling where it has them. Tests only; no product change | N | HM1 | astrid-agent `tests/core/execution/test_host_characterisation_*.py` (new) | The new tests pass on `release/14/main` and on `release/14/plan-13`; each names the responsibility it pins; a list of what is still unpinned and why | [x] 18 Nov: R14-P13-02, Agent #409 merged into `release/14/plan-13` at `82e19108`. 29 cases pass. The #905 reproducer runs as a visible failing step with JUnit retained until R14-FIX-11 lands. |
| HM3 `_stop_registered_host` (`astrid/sdk/host_bootstrap.py:1086`) uses the current Runtime's support root, not the registration's own, and an empty `support_root` no longer opens `generic-host.lock` relative to the working directory | N | — | astrid-agent `astrid/sdk/host_bootstrap.py`; `tests/sdk/test_host_recovery.py` | Two new cases in `tests/sdk/test_host_recovery.py` (a registration with a foreign support root; an empty one) fail before and pass after; `bash scripts/worker-env/agent-pytest.sh -q tests/sdk/test_host_recovery.py` passes | [x] 17 Nov: R14-P13-01, Agent #383 merged into `release/14/plan-13` at `a9085e17`; `tests/sdk/test_host_recovery.py` 78 pass / 1 fail, the fail being the base's own (Plan 39 AT7) |

The prepared-worker plumbing card below waits for Plan 14's audit and stays out of Release 14.

## Release 15: the extraction

**Now, 22 Nov:** R1 review failed with eight findings; R1.1 and R1.2 are merged, R1.3 is underway. The owner decides Plan 83's release after the re-estimate is updated for the repairs. Final CI and remaining findings gate landing. Spend is CPU only.

The start of steps 3 and 4 of the [sequence](plan.md#sequence), drafted on 22 November 2026 from the [map](map.md), four checks of it against today's file and an independent critique ([evidence](evidence/)). The file is 18,888 lines on astrid-agent `release/15/main` at `aac1ceb6`: the `GenericPackHost` class 8,416, other classes 4,709, top-level functions 4,892. Line numbers and counts are re-checked at dispatch.

**Task ids:** `EX-0` to `EX-3`, `R`. All four are Release 15's, by the owner's decision of 22 November 2026: the guard, the safety net, the first measured move and the re-estimate. This plan ends there. The rest of the extraction, `EX-4` to `EX-9` and `RS2`, moved to [Plan 83](../83-execution-host-in-modules/tasks.md) on 22 November 2026, so that each plan sits wholly in one release; the numbering continues there. **Test inventory:** the nine `tests/core/execution/test_host_characterisation_*.py` files from HM2 (one is on `release/15/main`; eight are still on `release/14/plan-13`), `tests/test_structure_contracts.py`, `tests/packs/test_capability_bind_contract.py` (it parses this file's source), `tests/core/execution/test_windows_diagnostic_sinks.py` (it replaces `generic_host.os` and rebinds module state), `tests/sdk/test_host_recovery.py`, and the other test files that patch names on this module.

Every card is **a move, proved at the point of use, not by looking the same:**

- No behaviour change, no renamed public name, no new feature; a fix a move uncovers is filed and made separately.
- `generic_host` keeps exporting every name callers use, and stays runnable as `python -m astrid.core.execution.generic_host`, which production uses (`astrid/sdk/host_bootstrap.py` near 2376).
- **A patched name must still take effect.** A function with an identical body in a new module looks names up in that module, so a test that patches `generic_host.name` silently stops patching it. For each moved definition, each test that patches it is shown to fail when its patch is removed. A definition whose patch cannot follow it stays where it is.
- **One class, one object.** A class that moves is the same object from every import path; recovery depends on `isinstance`.
- **Module state has one home.** A value that is rebound at run time (`_runtime_external_sources`, `_STARTUP_TIMING_LAST`, `_STARTUP_TIMING_SEEN`) is reached through one accessor, never imported by value.
- **Imports of concrete packs stay in the host.** The structure rules exempt this file alone (`scripts/reshape/authority_lint.py` near 303); a sibling that imported a pack would break them.
- Each card lowers the guard from EX-0 by what it removed. Never edit, skip or weaken an existing test to pass.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| EX-0 Nothing in the execution package can grow past the guard. One check, comparing a pull request with its merge base, so that editing a baseline in the same change cannot bless growth: `generic_host.py` may not gain lines; `GenericPackHost` may not gain methods; a function or method already over 200 lines may not grow, counting nested functions inside it; no file under `astrid/core/execution/` may newly pass 1,200 lines and no function may newly pass 200 | X | D2 | astrid-agent `tests/test_structure_contracts.py`, a comparison in the style of `scripts/reshape/compare_structure_baseline.py`, and the CI step that gives it the merge base. The existing giant-file inventory test and its 18 failures are not this card's ([#1290](https://github.com/banodoco/astrid-dev/issues/1290)) | Each of these fails the check and is named: one line added to the file; one method added to the class; one line added to `_run_task_impl`, directly or in a nested function; a new 1,300-line sibling. A change that removes lines passes. A change that deletes code elsewhere in the file to pay for a longer method fails. Research: L4 | [x] 22 Nov: Agent #484 merged at `2e62e7642c5d1d64f96b38d3e902b603466a0387`; candidate `75badbed0e06c4d679655f49113ea85ff54676e7`. Worker and manager ran the two `test_execution_size_guard_*` cases (2 passed), including the required injected growth and deletion cases; CLI against starting merge base reported zero violations. Existing giant-file inventory is unchanged. |
| EX-1 The safety net is on the branch. The eight HM2 characterisation files still on `release/14/plan-13` are brought to the Release 15 plan branch and pass there | N | — | astrid-agent `tests/core/execution/test_host_characterisation_*.py`; no product code | All nine files pass on `release/15/plan-13`; any that fail are listed with the reason and block the cards that rely on them | [x] 22 Nov: Agent #483 merged at `8ef3208259d4979297208077bd173fd0d699b557`; candidate `9743d4e896cdcbd3cbf6586ed26b9335bc156fa9`, all nine files 30 passed on worker and manager rerun (`PYTEST_ADDOPTS=-rA bash scripts/worker-env/agent-pytest.sh -q tests/core/execution/test_host_characterisation_*.py`). Added files match donor exactly. |
| EX-2 The genuine leaves leave: the shared `HostError` base first, then the input and output naming helpers (R03), the selector and contract helpers that call each other (`_task_selector`, `_execution_contract`, `_canonical_digest` and what they need), and `GenericPackHost._load_matrix`, a static method other code calls directly. `CapabilityRecord`, whose `manifest()` reaches into source custody, and `_AttemptLifetime`, which changes its own phase and deadlines, stay | X | EX-0, EX-1 | astrid-agent `astrid/core/execution/generic_host.py` (near 266, 1956, 3087, 5304, 7722) and new sibling modules; names chosen at dispatch | The rules above, shown for each moved name. The characterisation tests pass unchanged. The guard is lowered by what moved. Research: L1, critique | [x] 22 Nov: Agent #485 merged at `0999079bb5c8ab308dc556784f1fa59326ef09f8`, candidate `29f4bf5d8e50175b5be270da21e60618cb574165`. Focused proof: 330 passed, one failure also reproduced at the merged base (`test_fail_closed_g28.py::test_stalled_stage_deadline_publishes_before_stage_returns[settlement]`); no regressions by baseline comparison. Guard, class identity, module launch and patch-removal probes passed. `_task_generation_intent` stayed: a test that patches it still passed without its patch, so the required sensitivity was not proved. |
| EX-3 The first measured extraction, and the re-estimate. Record for EX-2: days taken, lines removed net of the wrappers and imports left behind, tests that had to move, and what broke. Re-state the estimate for [Plan 83](../83-execution-host-in-modules/tasks.md)'s cards and bring it to the owner, who decides that plan's release | N | EX-2 | this plan's `tasks.md` and `inputs.md` | The figures, and her decision recorded | [ ] Figures prepared 22 Nov; owner decision pending. EX-2 took about 18 elapsed minutes from dispatch to merge (0.038 eight-hour days; worker implementation about 12 minutes), removed 457 net host lines (18,888 to 18,431), and moved no tests. One existing settlement test failed on both base and candidate; one insensitive patch probe kept `_task_generation_intent` in the host. Re-estimate: EX-4 2–3 days, EX-5 3–4, EX-6 2–3, EX-7 4–5 (11–15 total); EX-8 5–7, RS2 2–3, EX-9 10–14 (17–24 total), plus final review and fixes. Total 28–39 engineering days before final review, subject to Plan 38 and owner release decision. This is an allowance, not a linear extrapolation from one easy leaf move. |
| R Review rounds (at most 1, owner-agreed 22 November 2026), by an independent reviewer on Codex Astra that did none of the work | S | all other tasks | read-only | Rounds per the [run contract](../../skills/shared/run-contract.md): findings become rows `R1.<n>` added directly below this one, each with route, scope, dependencies and proof; landing waits for them | [ ] |
| R1.1 Restore unchanged Ruff gate | N | R | `generic_host.py`, `host_naming.py`, `compare_execution_size.py` | Pinned `make ruff` no more than 2,004 findings, unchanged gate; compatibility exports explicit | [x] Agent #488 merged at `83166775484e125a82d80ff2ff8d9aaab5a1b53a`; pinned Ruff 0.12.0 `make ruff` passed at 2,001, ceiling unchanged; worker and manager reruns. |
| R1.2 Catch class control-flow methods and aliases | X | R1.1 | `compare_execution_size.py`, added structure tests | Reviewer guard mutations fail and name violations; existing guard cases pass | [x] Agent #489 merged at `b167f705ef026c01a35d542fd45089d37cd6e60d`; two base guard tests and four head tests passed; reviewer conditional-method and alias mutations fail naming `probe`. |
| R1.3 Count decorators and trailing suite comments | X | R1.2 | guard and added structure tests | Reviewer decorator, long decorated sibling, trailing comment mutations fail; boundary tests | [ ] |
| R1.4 Preserve startup phase before dependency imports | X | R1.3 | host import order and added entry-point test | Reviewer startup hook emits phase as base; service entry test | [ ] |
| R1.5 Preserve patched dependencies and false-valued callables | X | R1.4 | naming and contract helpers, host wrappers | Reviewer exports/runtime probes match base; patch-removal proof | [ ] |
| R1.6 Restrict guard workflow to intended PR checks | X | R1.5 | CI workflow | Separate guard workflow; parsed YAML comparison proves other jobs retain original PR filter | [ ] |
| R1.7 Handle Unicode paths and binary blobs | N | R1.6 | guard | Reviewer Unicode and binary cases pass, byte-safe line counts and encoded Python parsing | [ ] |
| R1.8 Preserve wrapper docs and annotation introspection | N | R1.7 | host and contract helpers | Four docstrings and type hints match base | [ ] |

**Sizes.** EX-0 to EX-3: about 5 to 6 days.

## Task index

Only the card below is recorded so far. Scope the rest from the actual source base, preserving the original intent below:

- Map responsibilities, callers, shared state, and existing focused tests; select natural extraction boundaries.
- Characterize affected behavior before extraction and rerun those exact checks.
- Extract one cohesive responsibility at a time, preserving public entry points and avoiding a replacement execution framework.
- Explicitly cover touched lifecycle, cancellation, process ownership, and result-handling boundaries.
- Keep semantic bug fixes separately named where needed; moving code alone must not silently change execution contracts.

Before execution, each task needs a difficulty route, exact inputs and dependencies, bounded work, explicit focused checks, completion evidence, and the existing review/publication boundary. No broad suites or automatic test discovery are authorized by this draft.

## Task details

### host_bootstrap retirement safety follow-ups

Now row HM3 above.

- **Outcome / work:** `_stop_registered_host`, a test-helper path, trusts the registration's own `support_root` rather than the current Runtime's. An empty `support_root` also opens `generic-host.lock` relative to the cwd. Bind both to the current Runtime support root.
- **Route:** N.
- **Dependencies and inputs:** Execution host bootstrap retirement code; exact file paths TBD at setup.
- **Focused checks:** Exact focused selectors TBD at setup; no broad suites.
- **Done:** Both paths use the current Runtime support root, and the focused checks are recorded.
- **Progress:** [ ]

### Prepared-worker plumbing in `generic_host.py` (follow-up)

- **Outcome / work:** once Plan 14's reachability audit shows the RunPod prepared-worker island dead, remove its readiness-profile plumbing from `generic_host.py` (44 references) and `actions/run/run.py:813-866` (36). Source: Plan 32 review, 9 Nov, at 7209ffcc7. Priority: Medium.
- **Route:** N.
- **Dependencies and inputs:** Plan 14's prepared-worker audit; the `generic_host` machine-path and engine-branch parts were not audited in the review (17,135 lines).
- **Done:** no readiness-profile reference remains outside what the audit kept; focused checks recorded.
- **Progress:** [ ]
