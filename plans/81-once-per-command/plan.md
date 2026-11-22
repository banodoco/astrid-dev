# Once per command

**Project:** Once per command

**Goal:** Every command shows where its time went and says what it is waiting for, a timeline command is accepted in about a second, and `astrid generate` is queued in about half the time it takes today, because each command works each thing out once.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 17 engineering days (14 to 20): the timings, the baseline and the ceiling test about 5.5, generation about 5.5, timeline commands about 4, the client's waits about 2. About 15 without batch edits. Three workers can run most of it side by side.

**Waiting on:** a manager, and a machine with an installed Astrid and a real ComfyUI for the baseline (US-0). The owner's decisions are made ([inputs.md](inputs.md#owner-decisions)). US-1 can start now.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones. A manager starts at the [handover](handover.md).

**Vision gaps:** [F-008 — Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary): a person who already runs ComfyUI routes work through Astrid only if Astrid costs them nothing they can feel. [F-001 — Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (supporting): a command that stalls without saying why reads as broken. Neither route names this plan, so there is no `Contributes to closure` line.

## Outcome and scope

The aim this plan shares with [Plan 82](../82-reuse-across-commands/plan.md) is under a second to start: a generation queued, or a timeline edit accepted, within a second of running the command. This plan is the first half, split off on 22 November 2026 at the owner's request: everything that needs nothing kept between one command and the next.

Measured on 22 November 2026 on the Release 15 code, run from source ([inputs.md](inputs.md#planning-evidence)): creating an empty timeline took 3.5 s and adding one image 3.8 s, though every Runtime request in them answered in under a tenth of a second; `astrid generate` worked for 15.6 s before it reported that no ComfyUI was reachable. Inside one command, Astrid builds the workflow twice, loads registries more than once, finds the entry twice, reads the same timeline bundle twice, and from source spends 2.3 s proving which code it is running.

**Included:**

- **Timings everyone can see.** Each stage of both commands is timed, shown on request and in the JSON result, and a command that has waited two seconds says what for.
- **A real baseline,** on an installed Astrid with a real ComfyUI, before and after.
- **A test that holds the ceilings.** It runs on every pull request against a real Runtime and a stand-in ComfyUI. Its ceilings start at today's numbers and may only fall.
- **Each thing worked out once per command:** the workflow, the entry, the registries, the timeline's bundle, and a cheaper proof of the source.
- **Many timeline edits in one command.**
- **No silent waits in the client.**

**What this should give,** estimated from component timings and not yet measured end to end: timeline commands from about 3.8 s to between 1 and 1.5 s from source; `generate` to queued in about half today's time. It does not get `generate` under a second.

**Not included:** anything kept between commands, which is where a result could be stale: reusing a compiled workflow for the next command, a saved index of entries and registries, trusting an install's stamp, and reusing ComfyUI's node list. Those are [Plan 82](../82-reuse-across-commands/plan.md). Also not here: the time from queued to a finished result and a resident process ([Plan 55](../55-local-speed/plan.md)); saves on a heavy timeline ([Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md)); checking only what an edit touches ([Plan 75](../75-fast-saving/plan.md)).

## Existing work and decision

Nothing here is a cache that outlives its command, so nothing here can be stale and no design review of freshness is needed. That is why it was split from Plan 82: this half is plain changes with clear tests, and its measurements decide what the second half should be. Reusing results across commands can be done with caches on disk or with a process that stays running, which is Plan 55's design; building one before the numbers are in risks building the wrong one.

It takes two things that already exist: Plan 55's standing meter, merged on that plan's branch, as the starting point for the ceiling test; and the Runtime's daemon fixture. The findings, the measurements and the research behind each task are in [inputs.md](inputs.md#planning-evidence) and [evidence/](evidence/).

## Sequence and readiness

1. **US-1, the timings,** first: nothing after it can be proven without them.
2. **US-0, one real baseline,** and **US-2, the ceiling test,** as soon as US-1 lands.
3. **Three lanes side by side:** generation (US-5a, US-4, US-3); timeline commands (US-6, then US-7); the client's waits (US-8).
4. **US-0 again,** then **R,** one review round on the combined result. The second baseline is Plan 82's starting evidence.

**Real dependencies:** `release/15/plan-77` edits the timeline SDK files US-6 and US-7 change, raises the client's request timeout and changes generation input inspection. US-6 and US-7 start from `release/15/main` after Plan 77 lands there, or merge its branch first; the manager records which.

**Unresolved:** nothing for the owner. Recording this plan authorizes no implementation. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** the Runtime's task admission and timeline commit requests, unchanged; Plan 55's meter, read from `release/14/plan-55`.

**Produces:** stage timings in each command's JSON result and a `--timings` view; a ceiling test in the Agent's fast checks; two real baselines; a batch form for timeline edits. **Compatibility:** no wire, schema or store change, and nothing written to disk for a later command to trust.

## Completion

- **Visible:** `--timings` on `generate` and on a timeline edit shows every stage, and the stages add up to the wall time within 10%.
- **Once:** call counts in tests show one workflow build, one entry resolution, one registry load and one bundle read per command.
- **Faster, by measurement:** the second baseline shows a timeline edit at or under 1 second on an installed Astrid, and `generate` to queued at no more than 60% of the first baseline. If the installed timeline figure was already under a second, that is recorded and the ceiling is set there.
- **Held:** the ceiling test fails, naming the stage, when a 1.5-second delay is injected into any one stage, and its ceilings were lowered to the new medians.
- **Slow says why:** a command held behind another process's lock prints what it is waiting for after two seconds, and gives up with a clear message at its limit.
- **Batch:** twenty clips are added by one command in one accepted commit, and a refused batch changes nothing.
- **Unchanged behaviour:** every refusal a command gives today before queuing or committing, it still gives, at the same point.
- **Limits of the proof:** CI uses a stand-in ComfyUI and a Runtime run from a checkout, so the real figures rest on the two baselines. The halving of `generate` is an estimate until the second baseline. Landing and publishing remain the owner's.
