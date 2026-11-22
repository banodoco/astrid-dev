# Execution host refactor

**Project:** Execution host refactor

**Goal:** Split the oversized execution host into clear, maintainable modules while preserving supported execution behavior.

**Status:** active

**Owner:** Release 14 Lead (`session_011EzfW3Zy19ncNecpQnKb7D`), by [packet dispatch](../../releases/14/run.md)

**Estimate:** About 30 engineering days for the extraction: phase A, out of the class, about 11; local preparation and the command-line lifecycle 4 to 5 more; phase B, the class itself, about 12; reviews 2. HM1 to HM3 are done.

**Waiting on:** the owner's decisions D1 to D3 in [inputs.md](inputs.md#owner-decisions) and an independent critique of the extraction rows; a manager; the HM2 characterisation tests, which are on `release/14/plan-13` and must be on the Release 15 branch before any code moves. It no longer waits for Plan 55, which left Release 15 on 22 November 2026.

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

Drafted on 22 November 2026. The [map](map.md) still holds: the same 188 top-level definitions, and `GenericPackHost` now has 102 methods, three more than mapped. The file is 18,888 lines, up from 397 on 30 August, and grew about 2,700 lines in the three weeks to 21 November.

**The host coordinates; it does not compute.** Anything that needs none of the host's state leaves the file. Anything that owns state becomes its own object. Half the file is not the host class at all, so about 9,000 lines can leave before the hard part is touched.

**First, the file cannot grow.** Its line count, the number of methods on the class and the number of top-level definitions each get a ceiling that may only fall, kept where a code change cannot raise it. Every extraction lowers them. Without this the file regrows during the work: the existing check only asks that a document's number be updated, and it is failing today ([#1290](https://github.com/banodoco/astrid-dev/issues/1290)). This is a ceiling, not a size target; the plan still sets none.

**Then, in order:** the stateless helpers; the Runtime adapter; source custody with worker set-up; interactive review and the adapters; local preparation and the command-line lifecycle; and last the class, by extracting owners and finally one attempt. The rows are in [tasks.md](tasks.md#release-15-the-extraction).

**New code goes beside the host.** Plan 55's branch already puts its resident sessions in new files next to it, and still adds 233 lines to the host; when that work returns it fits under the ceilings or brings its own extraction.

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
