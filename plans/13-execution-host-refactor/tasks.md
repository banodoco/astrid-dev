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

Steps 3 and 4 of the [sequence](plan.md#sequence), drafted on 22 November 2026 from the [map](map.md) and four checks of it against today's file ([evidence](evidence/)). The file is 18,888 lines on astrid-agent `release/15/main` at `aac1ceb6`: the `GenericPackHost` class 8,416, other classes 4,709, top-level functions 4,892. Line numbers and counts are re-checked at dispatch.

**Task ids:** `EX-0` to `EX-8`, `RS2`, `R`. **Critical path:** EX-0, EX-2, EX-3, EX-4, RS2, EX-7, EX-8, R. **Test inventory:** the nine `tests/core/execution/test_host_characterisation_*.py` files from HM2, `tests/test_structure_contracts.py`, and the 9 test files that patch names on this module ([host-check-L3.txt](evidence/host-check-L3.txt)).

Every card: **a pure move.** No behaviour change, no renamed public name, no new feature; a fix that a move uncovers is filed and made separately. `generic_host` keeps exporting every name callers use today. A name that a test patches on this module either stays where it is, or moves in the same change as that test. Each card lowers the ceilings from EX-0 by what it removed, in the same pull request. Never edit, skip or weaken an existing test to pass.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| EX-0 The file cannot grow. Three ceilings for `generic_host.py`, each allowed only to fall: its lines (18,888), the methods of `GenericPackHost` (102) and its top-level definitions (188). The numbers live in a baseline file; a pull request that raises one fails, whatever else it changes. Modules extracted by this plan may not import `generic_host` | X | D2 | astrid-agent `tests/test_structure_contracts.py`, a baseline beside `scripts/reshape/` in the style of `compare_structure_baseline.py`, `astrid/core/structure.py` (the import rule). The existing giant-file inventory test and its 18 current failures are not this card's ([#1290](https://github.com/banodoco/astrid-dev/issues/1290)) | A change adding one line, one method or one top-level definition to the file fails the check and names which ceiling; lowering a ceiling passes; raising one in the same change as code fails. Research: L4 | [ ] |
| EX-1 `os` means the standard library. The Runtime filesystem adapter imported as `os` at line 59 gets a name that says what it is, everywhere in the file | N | EX-0 | astrid-agent `astrid/core/execution/generic_host.py` only. Closes [#1294](https://github.com/banodoco/astrid-dev/issues/1294) | A check that the file has no bare `os.` use of the adapter; the characterisation tests pass unchanged; the syntax tree is identical apart from that one name | [ ] |
| EX-2 The stateless helpers leave: managed inputs and output identities (R03, 225 lines), capabilities and readiness (R05, 491) and execution contracts and storage guards (R08, 771). None uses `self`, the adapter, or state changed at run time; R05 and R08 call each other in two places (`_task_selector` and `_execution_contract`) and move together | N | EX-1 | astrid-agent `astrid/core/execution/generic_host.py` and new sibling modules; module names chosen at dispatch | Each moved function's body is identical before and after (compared by syntax tree); every name is still importable from `generic_host`; the characterisation tests and the importer tests pass unchanged; ceilings lowered by about 1,490 lines and 63 definitions. Research: L1 | [ ] |
| EX-3 The Runtime adapter leaves: `RuntimeProtocolClient` and terminal evidence (R02, 953 lines). Three test patches target it and move in the same change | X | EX-2 | astrid-agent the same file, a new sibling module, and the tests that patch `RuntimeProtocolClient` on this module | As EX-2, plus: every patch that named the class on `generic_host` still takes effect (each such test fails if its patch is removed) | [ ] |
| EX-4 Source custody and pack capture (R10, 675 lines) and worker bindings, imports and network policy (R06, 735) leave together. They have a deferred import cycle with `_child_bridge.py` and retained descriptors, so the boundary is drawn once | X | EX-3 | astrid-agent the same file, `_child_bridge.py`, `generic_host_worker.py` (which imports helpers from the host) and new sibling modules | As EX-2, plus: no import cycle at module load (a test imports each new module alone in a fresh interpreter); `source_identity.py:39` and `scripts/ci_windows_journey.py:468` still find what they name | [ ] |
| EX-5 Interactive review and discovery (R09, 1,291 lines), managed execution adapters (R04, 400) and the native engine graph (R13, 422) leave | X | EX-3 | astrid-agent the same file and new sibling modules | As EX-2 | [ ] |
| EX-6 Local preparation and authenticated handoff (R12, 2,168 lines) and activation and the command-line lifecycle (R14, 969, of which `_cli_impl` is 598) leave. Custody-sensitive: it follows [Plan 38](../38-one-process-identity/plan.md) or is agreed with its owner first | S | EX-4; Plan 38 | astrid-agent the same file and new sibling modules; the public command-line and bootstrap entry points keep their paths | As EX-2, plus the activation and handoff characterisation tests | [ ] |
| RS2 Review stop before the class is touched (rounds at most 1): a short design note naming the objects that take state out of `GenericPackHost` (held sessions, process custody, a claim slot, an attempt), what each owns, and what a claim slot shares with the host and what it keeps private | S | EX-5 | read-only, on a note added to this plan's folder | Same protocol as R; findings become rows `RS2.<n>`. EX-7 and EX-8 depend on this row. Reason: a wrong boundary here changes cancellation, cleanup or settlement order, and both cards build on it | [ ] |
| EX-7 Owners come out of the class, as objects that hold their own state, not as mixins: held sessions (slice H04), process and renderer custody (H03), input and output handling (H08, H10: `_materialize_inputs` 577 lines, `_typed_outputs` 239), and launching a command or capability (H09, H11: `_run_command_definition` 486, `invoke_capability` 269, `_child_environment` 262) | S | RS2 | astrid-agent the same file and new sibling modules; the host keeps one attribute per owner | The characterisation tests for managed sessions, slots, diagnostics and preparation pass unchanged; the method ceiling falls by what moved; no new shared mutable state between host and owner | [ ] |
| EX-8 One attempt becomes an object. `run_task` (747 lines) and `_run_task_impl` (1,689) share one mutable record across lease renewal, forced abort, completion, reconciliation and result writing; that record gets an owner with the ordering written down, then the body is split behind it. Terminal-request recovery (`_recover_terminal_requests`, 291) goes with it. Last | S | EX-7 | astrid-agent the same file and a new sibling module; `run_task` stays callable and patchable where tests patch it | The attempt-lifecycle, cancel-handoff and activation-abort characterisation tests pass unchanged; an injected failure at each of renewal, abort, completion and result writing gives the same terminal record as before the change | [ ] |
| R Review rounds (at most 2, pending the owner's agreement) | S | all other tasks | read-only | Rounds per the [run contract](../../skills/shared/run-contract.md): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; landing waits for them | [ ] |

**Phases.** A, out of the class: EX-0 to EX-5, about 11 days, and the file falls by about 6,000 lines. EX-6 adds about 3,100 more and 4 to 5 days when Plan 38 allows. B, the class: RS2, EX-7 and EX-8, about 12 days.

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
