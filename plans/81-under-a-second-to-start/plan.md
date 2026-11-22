# Under a second to start

**Project:** Under a second to start

**Goal:** On a warm local machine, a generation is queued and a timeline edit is accepted within a second of running the command, and a command that is slow says what it is waiting for.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 22 engineering days (18 to 28): the timings, baseline and budget test about 6.5, generation about 10.5, timeline commands about 4, the client's waits about 2, reviews about 2. It is re-stated after the first real measurements and the cache design review ([tasks.md](tasks.md)). Three workers can run most of it side by side.

**Waiting on:** a manager; a machine with an installed Astrid and a real ComfyUI for the baseline (US-0); the owner reading what the critique changed, and D6. D1 to D5 were decided on 22 November 2026 ([inputs.md](inputs.md#owner-decisions)). US-1 can start now.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones. A manager starts at the [handover](handover.md).

**Vision gaps:** [F-008 — Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary): a person who already runs ComfyUI routes work through Astrid only if Astrid costs them nothing they can feel. [F-001 — Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (supporting): a command that stalls without saying why reads as broken. Neither route names this plan, so there is no `Contributes to closure` line.

## Outcome and scope

Measured on 22 November 2026 on the Release 15 code, run from source ([inputs.md](inputs.md#planning-evidence)): creating an empty timeline took 3.5 s and adding one image 3.8 s, though every Runtime request in them answered in under a tenth of a second; `astrid generate` worked for 15.6 s, 10.4 s of it the command's own processor time, before it even reported that no ComfyUI was reachable. The time goes on work done again by every command: identifying the source, discovering and hashing packs, finding the entry, loading registries, and building the workflow twice.

**Two budgets,** at the median, on a warm local machine with an installed Astrid:

- **Command to queued:** from starting `astrid generate` to the Runtime having admitted the task, under 1 second, for a repeated prompt and for a changed one. A workflow used for the first time, or one whose files or target changed, is built in full and is outside the budget.
- **Command to accepted:** from starting an `astrid timelines` edit to the Runtime having accepted the commit, under 1 second on an ordinary timeline.

**Included:**

- **Timings everyone can see.** Each stage of both commands is timed, shown on request and in the JSON result, and a command that has waited two seconds says what for.
- **A test that holds the ceilings.** It runs on every pull request against a real Runtime and a stand-in ComfyUI, and fails when a ceiling is exceeded. One real baseline on an installed Astrid with a real ComfyUI is taken at the start and at the end.
- **Each thing worked out once.** Source identity, pack discovery, the entry, the registries and the compiled workflow are each computed once and reused while their inputs are unchanged.
- **Fewer round trips for timeline commands,** and many edits in one command.
- **No silent waits in the client.** Every client-side lock on these two paths has a limit and a message; a command waiting on the Runtime says so.

**Also measured, with no budget yet:** starting Astrid until it is ready, and one look at a timeline (`timelines visualize`). The numbers decide whether either needs a plan.

**Not included:** the time from queued to a finished result (the worker, polling, a resident process), which is [Plan 55](../55-local-speed/plan.md); saves on a heavy timeline, which [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md) owns; checking only what an edit touches and one acceptor per timeline, which is [Plan 75](../75-fast-saving/plan.md); moving workflow building to after the task is queued, which changes what the Runtime's task request carries; and import-time trimming, which matters only below a second.

## Existing work and decision

This plan removes repeated work on the paths that exist. It adds no process that stays running and changes no request the Runtime accepts. That is the difference from Plans 55 and 75, which redesign who owns the work to reach a tenth of a second; on 22 November 2026 the owner asked for this plan in Release 15 and for those two to wait, in no release.

It takes three things that already exist, and no more: Plan 55's standing meter, which is merged on that plan's branch and measures caller to reply, not command to queued; Plan 55's compiled-template work, as the donor for compiling once; and the Runtime's stage event for commits, which is logged today and never shown. The findings, the measurements and the research behind each task are in [inputs.md](inputs.md#planning-evidence) and [evidence/](evidence/).

## Sequence and readiness

1. **US-1, the timings,** first: nothing after it can be proven without them.
2. **US-0, one real baseline,** and **US-2, the budget test,** as soon as US-1 lands. US-2 starts by recording today's numbers as ceilings that may only fall.
3. **RS1,** a review of one design note: what each cache is keyed on and what makes it stale. It gates US-3, US-4 and US-5b.
4. **The re-estimate gate.** With the baseline and RS1 in, the manager says whether the generation budget is reachable without D6 and re-states the estimate, to the owner.
5. **Three lanes side by side:** generation (US-5a, then US-3, US-4, US-5b); timeline commands (US-6, then US-7); the client's waits (US-8).
6. **R,** one review round on the combined result.

**Real dependencies:** `release/15/plan-77` edits the timeline SDK files US-6 and US-7 change, and raises the client's request timeout. US-6 and US-7 start from `release/15/main` after Plan 77 lands there, or merge its branch first; the manager records which. US-5b reads Plan 55's branch for its donor commits and must not merge that branch. Plan 77's branch also changes generation input inspection.

**Unresolved:** D6 and the number of review rounds. D1 to D5 were decided on 22 November 2026. Recording this plan authorizes no implementation. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** the Runtime's task admission and timeline commit requests, unchanged; the Runtime's existing commit stage event; Plan 55's meter and template commits, read from `release/14/plan-55` at the commits named in [inputs.md](inputs.md#source-identities).

**Produces:** stage timings in each command's JSON result and a `--timings` view; a budget test in the Agent's fast checks; caches keyed by content with a stated rule for when each is stale; a batch form for timeline edits. **Compatibility:** no wire, schema or store change. A cache that cannot prove it is current is not used: the command falls back to working the value out, and says so in the timings.

## Completion

- **Budgets:** on an installed Astrid with a real ComfyUI, the end baseline (US-0) shows under 1 second at the median for command to queued, with a repeated and with a changed prompt, and for command to accepted. In CI the budget test holds the from-source figure of 2 seconds, and the one-second budgets too if an installed-style fixture proves possible.
- **The test is real:** adding a 1.5-second delay to any one stage makes it fail and names the stage.
- **Nothing stale:** editing a workflow, a pack file, a model list or a source file between two commands changes the result of the second, and the timings show the value was recomputed.
- **Slow says why:** a command held behind another process's lock prints what it is waiting for after two seconds, and gives up with a clear message at its limit.
- **Batch:** twenty clips are added by one command in one accepted commit, and a refused batch changes nothing.
- **Unchanged behaviour:** every refusal a command gives today before queuing or committing, it still gives, at the same point.
- **Limits of the proof:** CI uses a stand-in ComfyUI and a Runtime run from a checkout, so the one-second budgets rest on two real baselines, not on every pull request. The generation budget is not promised until the first baseline shows what the live check of ComfyUI's node list costs: if that alone exceeds the budget, D6 decides. Landing and publishing remain the owner's.
