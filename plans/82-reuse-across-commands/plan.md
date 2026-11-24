# Reuse across commands

**Project:** Reuse across commands

**Goal:** `astrid generate` is queued within a second of running the command on a warm local machine, because a command reuses what an earlier command already worked out, and never uses a result that is out of date.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 8 engineering days.

**Waiting on:** Release 15 (the owner's decision, 24 November 2026), the thin-client floor experiment, and D1 to D3 ([inputs.md](inputs.md#owner-decisions)).

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-008 — Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary): a person who already runs ComfyUI routes work through Astrid only if Astrid costs them nothing they can feel. F-008's route does not name this plan, so there is no `Contributes to closure` line.

## Outcome and scope

This is the second half of the under-a-second work, split from [Plan 81](../81-once-per-command/plan.md) on 22 November 2026 at the owner's request. Plan 81 makes each command work each thing out once. What is left after it is the work a command repeats that the command before it already did: building the workflow (about 3.4 s for a default one), finding the entry (2.7 to 3.9 s), loading registries (1.5 to 1.8 s), discovering and hashing packs, and asking ComfyUI what nodes it has. Removing that needs something kept between commands.

**The budget:** from starting `astrid generate` to the Runtime having admitted the task, under 1 second at the median, on a warm local machine with an installed Astrid, for a repeated prompt and for a changed one. A workflow used for the first time, or one whose files or target changed, is built in full and is outside the budget.

**Included, in two layers** (owner's decision, 24 November 2026; [inputs.md](inputs.md#owner-decisions)):

- **A general command layer,** for every backend and pack: a thin client handing the request to a warm resident host; caches for shipped packs under the install stamp; the pack-host identity held warm; lazy imports.
- **One "prepare once, fill per request" contract per backend,** implemented for ComfyUI only: the compiled workflow is prepared once and a new prompt or seed is filled in. No Wan2GP work; the contract must not preclude another backend.
- **ComfyUI's node list,** only if a real ComfyUI shows it keeps the command above a second.
- **The one-second budget asserted** by Plan 81's test, and a third real baseline.

**The rule for everything here:** a reused result is used only when it can be shown to be current; otherwise the command works it out as today and says so in its timings. The worst failure this plan must make impossible is Astrid admitting a different workflow under an earlier approval. **No check is removed:** each is kept every command, or cached with its stated invalidation ([why each check](evidence/2026-11-24-why-each-check/README.md)).

**Not included:** the time from queued to a finished result; moving workflow building to after the task is queued; timeline commands, which Plan 81 and [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md) cover.

## Existing work and decision

Where the time goes, stage by stage, and what each cache needs to stay safe, is in the [first-principles note](evidence/2026-11-23-generate-first-principles/README.md): of about 5.8 s, about 0.3 s depends on the request; disk caches alone reach about 2.0 s *est.*, a thin client to the warm pack host about 1.3 s *est.*, and under 1 s is unproven. [Plan 55](../55-local-speed/plan.md)'s resident-session branch (`24c68a270`, VibeComfy `d8e61a50`) is the donor for the host and the prepared template, whose process-bound template RA-2 makes content-keyed. The research and critique are Plan 81's ([inputs.md](inputs.md#planning-evidence)).

**The Lead's recommendation (D1, pending the floor experiment):** the resident host and thin client first, with disk caches only for the first command after a restart.

## Sequence and readiness

1. **General layer:** RA-0a (measure, largely answered by the floor experiment), RA-0b (shipped-pack caches, read-only install), RA-0c (object-info trust), RA-1 (thin client and resident host), RA-1b (lazy imports).
2. **ComfyUI contract:** RA-2 (prepared template), RA-3 (own and project packs), RA-4 (node list, conditional).
3. **RA-5,** the budget asserted; **R,** one final review.

**Real dependencies:** Plan 81 landed; Release 15's pack-root seam (Plan 87 RN-4, PB-7b). **Unresolved:** D1 to D3. Recording this plan authorizes no implementation. Cards: [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** Plan 81's stage timings, ceiling test and baselines; the Runtime's task admission request, unchanged.

**Produces:** a written rule for each reused result (its inputs, its key, what makes it stale); the reuse itself; the one-second budget held by a test. **Compatibility:** no wire, schema or store change. Anything this plan writes to disk can be deleted at any time and the next command works as it does today.

## Completion

- **The budget:** a real baseline on an installed Astrid with a real ComfyUI shows `generate` to queued under 1 second at the median, with a repeated and with a changed prompt.
- **Nothing stale:** editing a workflow, a pack file, a model list, the target's node list or a source file between two commands changes the second command's result, and its timings show the value was recomputed. The graph admitted always equals the graph a full build would produce.
- **Safe to lose:** deleting everything this plan keeps between commands only makes the next command slower.
- **Held:** Plan 81's test asserts the one-second budget and fails when a 1.5-second delay is injected into any stage.
- **Limits of the proof:** CI uses a stand-in ComfyUI. If ComfyUI's own answer about its node list takes most of a second and D3 keeps asking every time, the budget is stated as Astrid's share of the time. Landing and publishing remain the owner's.
