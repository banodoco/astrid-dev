# Execution host refactor

**Project:** Execution host refactor

**Goal:** The oversized execution host is mapped, its behaviour is pinned by tests, it can no longer grow, and one measured move out of it shows what splitting it into modules will cost.

**Status:** done

**Owner:** Release 14 Lead (`session_011EzfW3Zy19ncNecpQnKb7D`), by [packet dispatch](../../releases/14/run.md)

**Estimate:** 0

**Waiting on:** —

**Vision role:** Foundational enabler — clarifies execution modules while preserving existing behavior.

**Contributing:** [Astrid development skill](../../agent/start.md).

Prepare Astrid's execution host to be separated into cohesive modules, and make the first move, while preserving its existing execution behavior. This plan ends in Release 15; on 22 November 2026 the moves after the first became [Plan 83](../83-execution-host-in-modules/plan.md), so that each plan sits wholly in one release. Current status, owner, and estimate remain in the [project queue](../../README.md).

## Goal and scope

- **Included:** map responsibilities and coupling in `generic_host.py`, pin its behaviour, stop it growing, and extract its genuine leaves while preserving public entry points and execution contracts.
- **Deferred:** every later extraction, which is [Plan 83](../83-execution-host-in-modules/plan.md); semantic behavior changes, a replacement execution framework, and arbitrary line-count targets.
- **Still undecided:** exact module boundaries and executable task breakdown, which depend on inspecting the chosen source base.

## Release 14 scope

Added on 16 November 2026, when the owner brought the first two steps of the [sequence](#sequence) into [Release 14](../../releases/14.md): the map of `generic_host.py`'s responsibilities, callers and shared state, and focused checks that pin the behaviour of each. Nothing moves in Release 14. The file is 18,784 lines at Release 13, and [Plan 55](../55-local-speed/tasks.md) changes it in LS-6, LS-7 and LS-8 during the same release, so the map is drawn on `release/14/main` and redrawn once Plan 55's fast lane has landed. Its first use is LS-8: resident sessions arrive as a module beside the host, not as more lines in it. The extraction, steps 3 and 4, is [Release 15](../../releases/15.md)'s, on the tests Plan 39 has made green.

## Release 15 scope

Drafted on 22 November 2026 and changed by an independent critique the same day. The [map](map.md) still holds: the same 188 top-level definitions, and `GenericPackHost` now has 102 methods, three more than mapped. The file is 18,888 lines, up from 397 on 30 August, and grew about 2,700 lines in the three weeks to 21 November.

**The host coordinates; it does not compute.** Anything that needs none of the host's state leaves the file. Anything that owns state becomes its own object. Half the file is not the host class at all.

**First, nothing can grow.** One check compares a pull request with its merge base: this file may not gain lines, the class may not gain methods, and a function already over 200 lines may not grow. Three fixed numbers would not be enough: deleting code elsewhere could pay for a longer method, and a baseline can be edited in the same change. The existing check only asks that a document's number be updated, and it is failing today ([#1290](https://github.com/banodoco/astrid-dev/issues/1290)). This is a guard, not a size target; the plan still sets none.

**Then one small, measured extraction** of the genuine leaves, and a re-estimate the owner decides on before anything else moves. The first draft called a third of the definitions stateless; the critique found the exceptions among them, and that the Runtime adapter and source custody each stand on helpers that have to move first. So the order after the leaves is: what the adapter stands on, the adapter, source custody, interactive review, local preparation with Plan 38, and last the class. Those are [Plan 83](../83-execution-host-in-modules/plan.md)'s rows; this plan's are in [tasks.md](tasks.md#release-15-the-extraction).

**A move is proved where the name is used.** Tests patch names on this module, Windows tests replace its `os`, production launches it with `-m`, and one test reads its source. A moved function with an identical body can still behave differently. Each card says how that is shown.

**New code goes beside the host.** Plan 55's branch already puts its resident sessions in new files next to it, and still adds 233 lines to the host; when that work returns it fits under the guard or brings its own extraction.

## What we build on

The historical source inspection describes handwritten orchestration in `generic_host.py`; candidate boundaries include Runtime protocol access, capability discovery, task execution and settlement, local preparation, persistent supervision, and process handoff. The generated protocol client is separate. Confirm coupling on the actual starting commit. Source observations and the PR #109 relationship are recorded in [inputs.md](inputs.md).

The shared inference lifecycle remains with [multiple inference routes](../12-multiple-inference-routes/plan.md), and the single agent extension path remains with [streamlined agent experience](../16-streamlined-agent-experience/plan.md). This extraction must not create competing schedulers or agent registries.

## Sequence

1. Inspect the selected source, callers, shared state, and focused tests; choose boundaries and executable tasks.
2. Characterize the affected behavior with exact focused checks.
3. Extract one cohesive responsibility at a time, preserving public entry points and execution contracts.
4. Rerun the same checks, explicitly covering touched lifecycle, cancellation, process ownership, and result handling. Keep any required semantic fix separately identified.

The task outline and its draft limits are in [tasks.md](tasks.md).

## Completion

The guard rejects growth in the execution package, the characterisation tests pass on the Release 15 plan branch, the genuine leaves have left the file with existing callers still working, and the owner has the re-estimate for [Plan 83](../83-execution-host-in-modules/plan.md). Record results against the actual source identities and the existing publication authority in [inputs.md](inputs.md). This project does not establish an arbitrary size target or authorize implementation by itself.

## Read next

- [tasks.md](tasks.md): draft work outline and focused proof requirements.
- [inputs.md](inputs.md): historical evidence, source identity fields, and constraints.

## Completion reconciliation — 26 November 2026

The smaller agreed characterization, growth guard and extraction scope has landed. [Agent #511](https://github.com/banodoco/astrid-agent/pull/511) records the independent review repairs, 30 characterization cases, unchanged Ruff gate (2,008/2,008), measured reduction from 18,888 to 18,446 lines, and the owner's landing approval with the CI caveat. Its merge `9811dc3870f4dd1f98793cb4409cad5e9c6b62e0` is an ancestor of published Agent `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5` (GitHub compare verified 26 November). All 16 task rows are recorded complete. The later header saying the Release 15 tasks had not started and were moved to Release 16 was stale against this landing; preserve the historical decisions but do not rerun the completed extraction. The remaining modular decomposition belongs to [Plan 83](../83-execution-host-in-modules/plan.md). Exact plan-head full CI was cancelled; completion relies on the accepted scoped proof and subsequent integrated Release 15 gate, not a claim of all-green CI. Reconcile any later draft release allocation with the Lead; this record does not allocate or publish a release.

Release 15 was [qualified](https://github.com/banodoco/astrid-dev/issues/1834#issuecomment-7172606069) under the owner's approved conditional gate and [published](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7174076695) on 25 November. The [Lead's stand-down](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7179900972) confirms delivery is over. The owner's long-lived-install check and formal release finalization remain separate; no release status or gap is closed by this metadata reconciliation.
