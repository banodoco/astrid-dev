# Saving holds on a heavy timeline

**Project:** Saving holds on a heavy timeline

**Goal:** Open an asset-heavy timeline quickly and keep ordinary edits saving in about two seconds, alone, twice back to back, in bursts and as repeated drags. Measure CPU alongside wall time. Any save refusal is a real clash the person can retry or discard.

**Status:** active

**Owner:** Codex manager (hosted in Claude session session_011EzfW1FXS3o7GFnNSB7cZS)

**Estimate:** About 4 engineering days (3 to 5): about 1.5 for the setup cards, about 0.5 to recover the lost work, and 2 for the first three loop rounds. Further rounds are extra.

**Waiting on:** the Plan 77 Runtime checkpoint repair and regenerated pins, then a practical public seed for the heavy fixture. Qualify the fixture and run Round 1 on the current plan branches.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-001 — Reliability isn't proven across supported setups](../../vision/gaps/F-001-platform-reliability.md) (primary): saving is the first thing a person loses work to, so it is a reliability failure. F-001's route does not name this plan, so there is no `Contributes to closure` line.

**Plan type:** a [loop plan](../../agent/roles/manager/live-loop.md). The end state is known; the tasks after the setup cards come from each round's live measurement.

## Outcome and scope

On a synthetic timeline shaped like the owner's heavy one (profiled on 18 November: 616 clips, a document of about 2.6 MB), run through the real installed stack:

- every ordinary edit the editor can make saves: alone, twice back to back, ten in a burst, and the same drag repeated;
- nothing vanishes (a failed drop keeps its placeholder; a dropped file is never silently lost);
- a refusal happens only on a real clash, and shows Try again and Discard;
- a save reaches "Saved" in about 2 s or better on the heavy fixture ([time to Saved](#terms); a warm commit median through the Runtime was 3.74 s on the profiled timeline against 0.22 s on one clip; editor time to Saved has never been measured, so round 1 sets the baseline);
- the first 15 s of the timeline become visible and editable quickly. Track about 5 s to first usable and about 15 s to full open as provisional targets on the standard 616-clip fixture;
- Runtime and browser CPU seconds are recorded alongside opening and saving wall time. Round fixes are judged on both measurements;
- the optional `large-shots` fixture uses a few large synthetic shots with many child clips, longer durations and larger generated media. The standard fixture is the completion reference;
- the plan deltas for Plans 63, 75 and 76 and 18 (astrid-dev PR #880) are written from this live evidence.

In scope: the fixture, the harness, the loop, recovery of the uncommitted work from the 18 November crash, and the fixes each round picks, in astrid-app, astrid-agent and astrid-runtime. Out of scope: the 300 ms target (Plan 75's), the shot-trim task (its branches are only listed in the [handover](handover.md)), and the [Plan 63](../../plans/index.md), 75 and 76 designs themselves.

## Terms

- **realm:** one workspace's data store; a stack gets its own copy.
- **head:** the latest accepted revision of a timeline; "head count" is how many a timeline has (it should be one).
- **occurrence:** one placement of a clip on a track; a clip can be placed more than once.
- **door:** the port a running stack's Runtime listens on for clients.
- **sandbox project:** a project the harness creates for itself in the stack's realm; no scenario touches any other project.
- **hold:** saving holds when an edit that should save does, within the target time, and keeps working under repeated or concurrent use.
- **real clash:** another actor changed the same occurrence or field since this client's read head.
- **first usable:** from editor navigation until the first 15 s of the selected timeline are visible and editable.
- **full open:** from navigation until the whole timeline is loaded and the editor displays Saved.
- **process CPU:** Runtime and browser CPU seconds over the same opening or edit interval, measured separately from wall time.
- **time to Saved:** from the end of a gesture to the editor's Saved badge, measured by the harness in the browser. For a burst or a repeat it runs from the end of the last gesture. Each scenario runs at least 3 times per round, and passes at a median of 2.0 s or less over those runs with no run over 4 s (the planner's reading of "about 2 s" and the planner's run count; the owner may change either).

## Existing work and decision

The [reviews and profile](inputs.md#planning-evidence) say where the time goes (`validate_final_candidate`, about 59% of a commit, with a pass run twice inside) and why edits are refused. The longer-term plans were costed from design reviews with no live loop on a heavy timeline, and the one-shot sweep of 14 edit kinds on 18 November missed the repeated-gesture failures. So this plan measures first, fixes the cheapest causes, and lets the evidence rewrite the longer plans. **Speed risk:** the [profile](evidence/sonnet-commit-profile-r14.md) bounds the known trim: skipping `validate_final_candidate` entirely took the commit from 3.74 s to 1.63 s, and the editor adds its own time on top. The pass that runs twice runs on two different documents (the candidate and the baseline), so it is not a plain duplicate to delete. About 2 s may therefore need more than card-sized fixes; if a round shows that, the loop stops and asks the owner (the workstream's stop rule) and does not start Plan 75's design here. The 14-kind sweep harness is the seed; its first run saved 3 and refused 11 of the 14 scenarios that completed, and then crashed when its browser closed (the disk was nearly full). The seed's timer starts before the gesture and polls the badge every 500 ms, so it cannot judge a 2 s target; SL-2 replaces it.

## Sequence and readiness

In Release 15 this plan runs second, after [Plan 69](../69-project-elements/plan.md), by the same manager ([brief](../../releases/15/briefs/plans-69-77.md)). Its branches already contain Plan 69's work. Before SL-1, merge into each `release/15/plan-77` whatever is newer: `release/15/main` once Plan 69 has landed there, or `release/15/plan-69` if it has moved but not landed; regenerate pins (Runtime, then Agent, then App; see [Plan 69's handover](../69-project-elements/handover.md#pins)).

The order is SL-1 (a stack), then SL-0 (the fixture, which needs a stack to build on), then SL-2 (the harness, which needs both); SL-0 and SL-2 can be drafted while SL-1 runs. The loop card SL-4 starts when the three are done. Round 1 records the checkpoint-repaired partial baseline. SL-3's recovered fixes can land after that baseline. The [round order](inputs.md#planning-evidence) gives saving three rounds, opening one, and CPU one, with early stops as recorded there. See [tasks.md](tasks.md). The first actions on a new machine are in the [handover](handover.md).

## Interfaces and handoff

It consumes the three `release/15/plan-77` branches (App, Agent, Runtime), cut on 21 November from Release 14's integration of Plans 59, 64 and 65; the exact SHAs are in [inputs.md](inputs.md#source-identities). It produces: fixes as PRs into those branches; a fixture and a harness in astrid-app `scripts/save-loop/` that any machine can rerun; and the round rows and plan deltas in [rounds.md](rounds.md), which Plans 63, 75 and 76 and 18 take up.

## Completion

Saving completes when both rounds 2 and 3 pass on fresh stacks using the full standard fixture. Each scenario saves within about 2 s ([time to Saved](#terms)) or is refused for a real clash with Try again and Discard, with no vanished work and one head. Round 4 reports opening against the provisional targets. Round 5 addresses the largest measured CPU cost and preserves open and save time. The loop ends after round 5 or an early stop. Record remaining gaps, each measured result, and all four plan deltas. The owner retains the real-timeline check. Plan 75 carries the 300 ms target.
