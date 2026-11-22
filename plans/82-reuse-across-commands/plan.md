# Reuse across commands

**Project:** Reuse across commands

**Goal:** `astrid generate` is queued within a second of running the command on a warm local machine, because a command reuses what an earlier command already worked out, and never uses a result that is out of date.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 10 engineering days if the reuse is kept on disk; it is re-stated by RA-1, which may choose a process that stays running instead and hand most of the work to Plan 55.

**Waiting on:** [Plan 81](../81-once-per-command/plan.md) landing. Its second baseline now exists (22 November 2026: `generate image` queued in 5.4 s on an installed build, down from 15.0 s); the owner's decisions D1 to D3 in [inputs.md](inputs.md#owner-decisions); a release.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-008 — Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary): a person who already runs ComfyUI routes work through Astrid only if Astrid costs them nothing they can feel. F-008's route does not name this plan, so there is no `Contributes to closure` line.

## Outcome and scope

This is the second half of the under-a-second work, split from [Plan 81](../81-once-per-command/plan.md) on 22 November 2026 at the owner's request. Plan 81 makes each command work each thing out once. What is left after it is the work a command repeats that the command before it already did: building the workflow (about 3.4 s for a default one), finding the entry (2.7 to 3.9 s), loading registries (1.5 to 1.8 s), discovering and hashing packs, and asking ComfyUI what nodes it has. Removing that needs something kept between commands.

**The budget:** from starting `astrid generate` to the Runtime having admitted the task, under 1 second at the median, on a warm local machine with an installed Astrid, for a repeated prompt and for a changed one. A workflow used for the first time, or one whose files or target changed, is built in full and is outside the budget.

**Included:**

- **A decision first** (RA-1): where each reused result lives, on disk or in a process that stays running, and for each one what proves it is still current.
- **The compiled workflow is reused,** and a new prompt or seed is filled in, not rebuilt.
- **Entries, registries and pack discovery are reused** across commands.
- **ComfyUI's node list,** if the baseline shows it is what keeps the command above a second.
- **The one-second budget asserted** by Plan 81's test, and a third real baseline.

**The rule for everything here:** a reused result is used only when it can be shown to be current; otherwise the command works it out as today and says so in its timings. The worst failure this plan must make impossible is Astrid admitting a different workflow under an earlier approval.

**Not included:** the time from queued to a finished result; moving workflow building to after the task is queued; timeline commands, which Plan 81 and [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md) cover.

## Existing work and decision

**Where the time is after Plan 81** (installed build, CPU container, stand-in ComfyUI, same prompt, 22 November 2026; [evidence](../81-once-per-command/evidence/)): 5.4 s in all. Registry loading 1.09 s (pack discovery 0.48 s of it); candidate preparation 1.06 s (workflow build 0.73 s); Runtime connection 0.80 s (attaching the pack host 0.54 s); qualification 0.51 s; emission 0.41 s; and about 1.5 s outside the named stages, believed to be mostly start-up and imports. Nearly all of it is work the command before already did. The question for each is not whether it can be kept but what is the cheapest way to know it is still valid.

**The order, added 22 November 2026 at the owner's prompting** ("could we preload stuff once it's loaded once? ... why do we need to?"): first what cannot change within an install (RA-0); then what is provably the same by its contents (the compiled workflow, RA-2; a person's own packs, RA-3); then what only ComfyUI knows (RA-4); and, if RA-1 chooses it, the command as a thin client to the host that is already running. Each step pays for itself and makes the next safer.

Two designs answer the same question. Caches on disk, keyed by content, keep the command line as it is and must prove freshness every time. A process that stays running holds the results in memory and knows when they change; that is [Plan 55](../55-local-speed/plan.md)'s resident session, already partly built on its branch and costly to land. Building both wastes one. So this plan starts with a decision made on Plan 81's measurements, not on the dated figures available on 22 November 2026.

Plan 55's branch has the compiled-template work (astrid-agent `24c68a270`, VibeComfy `d8e61a50`), whose template is tied to one process and session. The research and the independent critique that shaped these tasks are Plan 81's ([inputs.md](inputs.md#planning-evidence)).

## Sequence and readiness

1. **RA-0,** two measurements and the pieces that cannot go stale: shipped packs kept under the install's stamp, and code a command does not use not loaded. It needs no decision between disk and a running process.
2. **RA-1,** the decision note and its review.
3. **RA-2, RA-3 and RA-4** as RA-1 decides, side by side.
3. **RA-5,** the budget asserted and a real baseline.
4. **R,** one review round.

**Real dependencies:** Plan 81 landed, for its timings, its ceiling test and its baseline. If RA-1 chooses a resident process, RA-2 to RA-4 become Plan 55's and this plan keeps only RA-1 and RA-5.

**Unresolved:** D1 to D3, and its release. Recording this plan authorizes no implementation. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** Plan 81's stage timings, ceiling test and baselines; the Runtime's task admission request, unchanged.

**Produces:** a written rule for each reused result (its inputs, its key, what makes it stale); the reuse itself; the one-second budget held by a test. **Compatibility:** no wire, schema or store change. Anything this plan writes to disk can be deleted at any time and the next command works as it does today.

## Completion

- **The budget:** a real baseline on an installed Astrid with a real ComfyUI shows `generate` to queued under 1 second at the median, with a repeated and with a changed prompt.
- **Nothing stale:** editing a workflow, a pack file, a model list, the target's node list or a source file between two commands changes the second command's result, and its timings show the value was recomputed. The graph admitted always equals the graph a full build would produce.
- **Safe to lose:** deleting everything this plan keeps between commands only makes the next command slower.
- **Held:** Plan 81's test asserts the one-second budget and fails when a 1.5-second delay is injected into any stage.
- **Limits of the proof:** CI uses a stand-in ComfyUI. If ComfyUI's own answer about its node list takes most of a second and D3 keeps asking every time, the budget is stated as Astrid's share of the time. Landing and publishing remain the owner's.
