# Execution host in modules

**Project:** Execution host in modules

**Goal:** The execution host is split into clear modules that each own one responsibility, and the host class coordinates objects that hold their own state, with supported execution behaviour unchanged.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 28 engineering days as a planning allowance: about 11 for what leaves the file without touching the class, about 17 for local preparation and the class. [Plan 13](../13-execution-host-refactor/plan.md)'s first measured move re-states it.

**Waiting on:** [Plan 13](../13-execution-host-refactor/plan.md) landed, and the re-estimate it brings the owner (its EX-3); a release.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary): an 18,888-line file that every execution change passes through is where regressions hide. F-001's route does not name this plan, so there is no `Contributes to closure` line.

## Outcome and scope

This is the extraction that [Plan 13](../13-execution-host-refactor/plan.md) prepares. It was the later part of Plan 13 until 22 November 2026, when the owner said a plan should sit wholly in one release; Plan 13 keeps the guard, the safety net and the first measured move, which are Release 15's, and everything after them is here, in no release yet.

**The host coordinates; it does not compute.** Anything that needs none of the host's state leaves `astrid/core/execution/generic_host.py`. Anything that owns state becomes its own object. The design, the reasons and the order are in [Plan 13's Release 15 scope](../13-execution-host-refactor/plan.md#release-15-scope), and are not repeated here.

**Included:**

- **What leaves without touching the class** (EX-4 to EX-7): what the Runtime adapter stands on, the adapter, source custody, interactive review and the native engine graph. Together about 4,500 to 5,500 lines, less the wrappers and imports left behind.
- **Local preparation and the command-line lifecycle** (EX-8), which follows [Plan 38](../38-one-process-identity/plan.md).
- **The class** (RS2, EX-9): a reviewed design note, then owners that hold their own state, with one attempt last.

**Not included:** any behaviour change, a replacement execution framework, a size target, and renaming the module's `os` alias ([#1294](https://github.com/banodoco/astrid-dev/issues/1294)).

**Larger than one release as written.** When the owner gives it a release, it is cut to what fits and joins whole; the natural cut is after EX-7, before the class, and the rest becomes its own plan then.

## Existing work and decision

Plan 13's [map](../13-execution-host-refactor/map.md) assigns every top-level definition in the file to a responsibility; four checks against the file of 22 November 2026 and an independent critique are in its [evidence](../13-execution-host-refactor/evidence/) and summarised in its [inputs](../13-execution-host-refactor/inputs.md#extraction-evidence-22-november-2026). Its guard (EX-0) stops the file growing while this plan waits, and its characterisation tests (EX-1) are the safety net every card here relies on.

## Sequence and readiness

1. **EX-4, then EX-5:** what the adapter stands on, then the adapter.
2. **EX-6, then EX-7,** beside them: source custody, then review and the native graph.
3. **EX-8,** once EX-5 and Plan 38 have landed.
4. **RS2,** the design note for the class and its review.
5. **EX-9,** the class, split into its own rows by RS2.
6. **R.**

**Real dependencies:** Plan 13 landed; Plan 38 for EX-8. **Unresolved:** its release, where it is cut, and its review rounds. Recording this plan authorizes no implementation. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** Plan 13's guard, characterisation tests, map and re-estimate. **Produces:** sibling modules under `astrid/core/execution/`, each lowering the guard by what it removed. **Compatibility:** `generic_host` keeps exporting every name callers use and stays runnable as `python -m astrid.core.execution.generic_host`; no wire, schema or store change.

## Completion

- **The modules:** each responsibility named above lives in its own module, and existing callers and tests work unchanged.
- **The class:** state that belonged to held sessions, process custody, input and output handling and one attempt is owned by objects, and the class coordinates them.
- **Preserved behaviour:** the characterisation tests pass unchanged after every card, and each moved name is shown still to be patched where a test patches it.
- **Limits of the proof:** the characterisation tests pin what Plan 13 found reachable; behaviour they do not reach is named in each card. Landing and publishing remain the owner's.
