# Execution host refactor

**Project:** Execution host refactor

**Goal:** Split the oversized execution host into clear, maintainable modules while preserving supported execution behavior.

**Status:** active

**Owner:** Release 14 Lead (`session_011EzfW3Zy19ncNecpQnKb7D`), by [packet dispatch](../../releases/14/run.md)

**Estimate:** About 16 engineering days in Release 15 (13 to 19) for the growth guard and everything that leaves the file without touching the class, re-stated after the first measured extraction. About 17 more, in no release, for local preparation and the class itself. HM1 to HM3 are done.

**Waiting on:** a manager for the Release 15 extraction, and the owner's decision D2 in [inputs.md](inputs.md#owner-decisions). The owner chose the Release 15 scope on 22 November 2026. It no longer waits for Plan 55, which left Release 15 the same day.

**Vision role:** Foundational enabler — clarifies execution modules while preserving existing behavior.

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

Separate Astrid's execution host into cohesive modules while preserving its existing execution behavior. Current status, owner, and estimate remain in the [project queue](../../README.md).

## Goal and scope

- **Included:** map responsibilities and coupling in `generic_host.py`, then extract cohesive responsibilities incrementally while preserving public entry points and execution contracts.
- **Deferred:** semantic behavior changes, a replacement execution framework, and arbitrary line-count targets.
- **Still undecided:** exact module boundaries and executable task breakdown, which depend on inspecting the chosen source base.

## Release 14 scope

Added on 16 November 2026, when the owner brought the first two steps of the [sequence](#sequence) into [Release 14](../../releases/14.md): the map of `generic_host.py`'s responsibilities, callers and shared state, and focused checks that pin the behaviour of each. Nothing moves in Release 14. The file is 18,784 lines at Release 13, and [Plan 55](../55-local-speed/tasks.md) changes it in LS-6, LS-7 and LS-8 during the same release, so the map is drawn on `release/14/main` and redrawn once Plan 55's fast lane has landed. Its first use is LS-8: resident sessions arrive as a module beside the host, not as more lines in it. The extraction, steps 3 and 4, is [Release 15](../../releases/15.md)'s, on the tests Plan 39 has made green.

## Release 15 scope

Drafted on 22 November 2026 and changed by an independent critique the same day. The [map](map.md) still holds: the same 188 top-level definitions, and `GenericPackHost` now has 102 methods, three more than mapped. The file is 18,888 lines, up from 397 on 30 August, and grew about 2,700 lines in the three weeks to 21 November.

**The host coordinates; it does not compute.** Anything that needs none of the host's state leaves the file. Anything that owns state becomes its own object. Half the file is not the host class at all.

**First, nothing can grow.** One check compares a pull request with its merge base: this file may not gain lines, the class may not gain methods, and a function already over 200 lines may not grow. Three fixed numbers would not be enough: deleting code elsewhere could pay for a longer method, and a baseline can be edited in the same change. The existing check only asks that a document's number be updated, and it is failing today ([#1290](https://github.com/banodoco/astrid-dev/issues/1290)). This is a guard, not a size target; the plan still sets none.

**Then one small, measured extraction** of the genuine leaves, and a re-estimate reported to the owner. The first draft called a third of the definitions stateless; the critique found the exceptions among them, and that the Runtime adapter and source custody each stand on helpers that have to move first. So the order after the leaves is: what the adapter stands on, the adapter, source custody, interactive review, local preparation with Plan 38, and last the class. The rows are in [tasks.md](tasks.md#release-15-the-extraction).

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

The agreed responsibilities have clear module boundaries, existing callers still work, and focused before-and-after evidence demonstrates preserved behavior. Record results against the actual source identities and the existing publication authority in [inputs.md](inputs.md). This project does not establish an arbitrary size target or authorize implementation by itself.

## Read next

- [tasks.md](tasks.md): draft work outline and focused proof requirements.
- [inputs.md](inputs.md): historical evidence, source identity fields, and constraints.
