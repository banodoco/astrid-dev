# Execution host refactor

**Project:** Execution host refactor

**Goal:** Split the oversized execution host into clear, maintainable modules while preserving supported execution behavior.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD

**Waiting on:** a manager; scope agreement for the extraction (steps 3 and 4), which is Release 15's

**Vision role:** Foundational enabler — clarifies execution modules while preserving existing behavior.

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

Separate Astrid's execution host into cohesive modules while preserving its existing execution behavior. Current status, owner, and estimate remain in the [project queue](../../README.md).

## Goal and scope

- **Included:** map responsibilities and coupling in `generic_host.py`, then extract cohesive responsibilities incrementally while preserving public entry points and execution contracts.
- **Deferred:** semantic behavior changes, a replacement execution framework, and arbitrary line-count targets.
- **Still undecided:** exact module boundaries and executable task breakdown, which depend on inspecting the chosen source base.

## Release 14 scope

Added on 16 November 2026, when the owner brought the first two steps of the [sequence](#sequence) into [Release 14](../../releases/14.md): the map of `generic_host.py`'s responsibilities, callers and shared state, and focused checks that pin the behaviour of each. Nothing moves in Release 14. The file is 18,784 lines at Release 13, and [Plan 55](../55-local-speed/tasks.md) changes it in LS-6, LS-7 and LS-8 during the same release, so the map is drawn on `release/14/main` and redrawn once Plan 55's fast lane has landed. Its first use is LS-8: resident sessions arrive as a module beside the host, not as more lines in it. The extraction, steps 3 and 4, is [Release 15](../../releases/15.md)'s, on the tests Plan 39 has made green.

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
