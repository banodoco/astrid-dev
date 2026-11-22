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

Steps 3 and 4 of the [sequence](plan.md#sequence), drafted on 22 November 2026 from the [map](map.md), four checks of it against today's file and an independent critique ([evidence](evidence/)). The file is 18,888 lines on astrid-agent `release/15/main` at `aac1ceb6`: the `GenericPackHost` class 8,416, other classes 4,709, top-level functions 4,892. Line numbers and counts are re-checked at dispatch.

**Task ids:** `EX-0` to `EX-9`, `RS2`, `R`. **Committed for Release 15:** EX-0 to EX-3, then a re-estimate. **Test inventory:** the nine `tests/core/execution/test_host_characterisation_*.py` files from HM2 (one is on `release/15/main`; eight are still on `release/14/plan-13`), `tests/test_structure_contracts.py`, `tests/packs/test_capability_bind_contract.py` (it parses this file's source), `tests/core/execution/test_windows_diagnostic_sinks.py` (it replaces `generic_host.os` and rebinds module state), `tests/sdk/test_host_recovery.py`, and the other test files that patch names on this module.

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
| EX-0 Nothing in the execution package can grow past the guard. One check, comparing a pull request with its merge base, so that editing a baseline in the same change cannot bless growth: `generic_host.py` may not gain lines; `GenericPackHost` may not gain methods; a function or method already over 200 lines may not grow, counting nested functions inside it; no file under `astrid/core/execution/` may newly pass 1,200 lines and no function may newly pass 200 | X | D2 | astrid-agent `tests/test_structure_contracts.py`, a comparison in the style of `scripts/reshape/compare_structure_baseline.py`, and the CI step that gives it the merge base. The existing giant-file inventory test and its 18 failures are not this card's ([#1290](https://github.com/banodoco/astrid-dev/issues/1290)) | Each of these fails the check and is named: one line added to the file; one method added to the class; one line added to `_run_task_impl`, directly or in a nested function; a new 1,300-line sibling. A change that removes lines passes. A change that deletes code elsewhere in the file to pay for a longer method fails. Research: L4 | [ ] |
| EX-1 The safety net is on the branch. The eight HM2 characterisation files still on `release/14/plan-13` are brought to the Release 15 plan branch and pass there | N | — | astrid-agent `tests/core/execution/test_host_characterisation_*.py`; no product code | All nine files pass on `release/15/plan-13`; any that fail are listed with the reason and block the cards that rely on them | [ ] |
| EX-2 The genuine leaves leave: the shared `HostError` base first, then the input and output naming helpers (R03), the selector and contract helpers that call each other (`_task_selector`, `_execution_contract`, `_canonical_digest` and what they need), and `GenericPackHost._load_matrix`, a static method other code calls directly. `CapabilityRecord`, whose `manifest()` reaches into source custody, and `_AttemptLifetime`, which changes its own phase and deadlines, stay | X | EX-0, EX-1 | astrid-agent `astrid/core/execution/generic_host.py` (near 266, 1956, 3087, 5304, 7722) and new sibling modules; names chosen at dispatch | The rules above, shown for each moved name. The characterisation tests pass unchanged. The guard is lowered by what moved. Research: L1, critique | [ ] |
| EX-3 The first measured extraction, and the re-estimate. Record for EX-2: days taken, lines removed net of the wrappers and imports left behind, tests that had to move, and what broke. Re-state the estimate for everything below, and bring it to the owner before any further card is dispatched | N | EX-2 | this plan's `tasks.md` and `inputs.md` | The figures, and a go or a changed plan from the owner | [ ] |
| EX-4 What the Runtime adapter stands on leaves: the digest and claim-field helpers, the terminal persistence, rejection and exception helpers, and the protected JSON and private-bytes readers it shares with the handoff code, with duplicate-key rejection and canonical form kept exactly | S | EX-3 | astrid-agent the same file (near 5476–5913, 15453) and a new sibling module | The rules above. A file with a duplicate key, and one that is not canonical, are refused exactly as before | [ ] |
| EX-5 The Runtime adapter leaves: `RuntimeProtocolClient` and terminal evidence (R02, 953 lines). At least 18 tests replace the client through imported module names, and each must still take effect | S | EX-4 | astrid-agent the same file, a new sibling module, `tests/sdk/test_host_recovery.py` (near 90) and the other tests that replace the client | The rules above, for every replacement site | [ ] |
| EX-6 Source custody and pack capture (R10, 675 lines) leaves, once `_runtime_external_sources` has one accessor | X | EX-3 | astrid-agent the same file (near 543, 6729), `_child_bridge.py` (near 38), `generic_host_worker.py`, and a new sibling module | The rules above. A consumer that read the binding before installation sees it after. A deferred bridge call works from the host and from the worker. `astrid/core/source_identity.py` (near 39) still covers every file that now holds host code | [ ] |
| EX-7 Interactive review and discovery (R09, 1,291 lines) and the native engine graph (R13, 422) leave. Worker bindings (R06) and managed execution adapters (R04) move only where they import no concrete pack; the rest stays in the host | X | EX-6 | astrid-agent the same file (near 950, 1540, 2156) and new sibling modules | The rules above. The authority lint passes with no new exemption | [ ] |
| EX-8 Local preparation and authenticated handoff (R12, 2,168 lines) and activation and the command-line lifecycle (R14, 969) leave. Custody-sensitive: it follows [Plan 38](../38-one-process-identity/plan.md) | S | EX-5; Plan 38 | astrid-agent the same file and new sibling modules; `python -m astrid.core.execution.generic_host` and its service-mode alias keep working | The rules above, plus the activation and handoff characterisation tests and one real `-m` launch | [ ] |
| RS2 Review stop before the class is touched (rounds at most 1): a design note naming the objects that take state out of `GenericPackHost`, what each owns, and what a claim slot shares with the host and what it keeps private. It reuses `ManagedToolSession` and `WarmHolds` where they already own that state | S | EX-6, EX-8 | read-only, on a note added to this plan's folder | Same protocol as R; findings become rows `RS2.<n>`. EX-9 depends on this row. Reason: a wrong boundary changes cancellation, cleanup or settlement order | [ ] |
| EX-9 Owners come out of the class as objects that hold their own state, not as mixins: held sessions, process and renderer custody, input and output handling, launching a command or capability; and last, one attempt (`run_task`, 747 lines, and `_run_task_impl`, 1,689), whose shared record gets an owner with its ordering written down before the body is split. The riskiest step is handing an unsettled attempt to the reconciliation thread: releasing its accounting early makes the host look idle when it is not | S | RS2 | astrid-agent the same file (near 6806, 12376, 14903) and new sibling modules. Split into its own rows by RS2 | The characterisation tests pass unchanged. With the terminal acknowledgement blocked: the session stays occupied, one attempt stays counted, and a cancellation is published once (`test_host_characterisation_cancel_handoff.py`, near 98) | [ ] |
| R Review rounds (at most 2, pending the owner's agreement) | S | all other tasks | read-only | Rounds per the [run contract](../../skills/shared/run-contract.md): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; landing waits for them | [ ] |

**Sizes.** EX-0 to EX-3: about 5 to 6 days, and they are the commitment. Everything after EX-3 is a planning allowance of about 25 more days until the first extraction has been measured.

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
