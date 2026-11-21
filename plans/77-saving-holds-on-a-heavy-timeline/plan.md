# Saving holds on a heavy timeline

**Project:** Saving holds on a heavy timeline

**Goal:** On an asset-heavy timeline, every ordinary edit saves in about two seconds, alone, twice back to back, in bursts and as repeated drags, and any refusal is a real clash that the person can retry or discard.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 4 engineering days (3 to 5): about 1.5 for the setup cards, about 0.5 to recover the lost work, and 2 for the first three loop rounds. Further rounds are extra.

**Waiting on:** a machine with 25 GB free and the [handover](handover.md) steps.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-001 — Reliability isn't proven across supported setups](../../vision/gaps/F-001-platform-reliability.md) (primary): saving is the first thing a person loses work to, so it is a reliability failure. F-001's route does not name this plan, so there is no `Contributes to closure` line.

**Plan type:** a [loop plan](../../skills/roles/astrid-dev-manage/workstreams/live-loop.md). The end state is known; the tasks after the setup cards come from each round's live measurement.

## Outcome and scope

On a synthetic timeline shaped like the owner's heavy one (profiled on 18 November: 616 clips, a document of about 2.6 MB), run through the real installed stack:

- every ordinary edit the editor can make saves: alone, twice back to back, ten in a burst, and the same drag repeated;
- nothing vanishes (a failed drop keeps its placeholder; a dropped file is never silently lost);
- a refusal happens only on a real clash, and shows Try again and Discard;
- a save reaches "Saved" in about 2 s or better on the heavy fixture ([time to Saved](#terms); a warm commit median through the Runtime was 3.74 s on the profiled timeline against 0.22 s on one clip; editor time to Saved has never been measured, so round 1 sets the baseline);
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
- **time to Saved:** from the end of a gesture to the editor's Saved badge, measured by the harness in the browser. For a burst or a repeat it runs from the end of the last gesture. Each scenario runs at least 3 times per round, and passes at a median of 2.0 s or less over those runs with no run over 4 s (the planner's reading of "about 2 s" and the planner's run count; the owner may change either).

## Existing work and decision

The [reviews and profile](inputs.md#planning-evidence) say where the time goes (`validate_final_candidate`, about 59% of a commit, with a pass run twice inside) and why edits are refused. The longer-term plans were costed from design reviews with no live loop on a heavy timeline, and the one-shot sweep of 14 edit kinds on 18 November missed the repeated-gesture failures. So this plan measures first, fixes the cheapest causes, and lets the evidence rewrite the longer plans. **Speed risk:** the [profile](evidence/sonnet-commit-profile-r14.md) bounds the known trim: skipping `validate_final_candidate` entirely took the commit from 3.74 s to 1.63 s, and the editor adds its own time on top. The pass that runs twice runs on two different documents (the candidate and the baseline), so it is not a plain duplicate to delete. About 2 s may therefore need more than card-sized fixes; if a round shows that, the loop stops and asks the owner (the workstream's stop rule) and does not start Plan 75's design here. The 14-kind sweep harness is the seed; its first run saved 3 and refused 11 of the 14 scenarios that completed, and then crashed when its browser closed (the disk was nearly full). The seed's timer starts before the gesture and polls the badge every 500 ms, so it cannot judge a 2 s target; SL-2 replaces it.

## Sequence and readiness

The order is SL-1 (a stack), then SL-0 (the fixture, which needs a stack to build on), then SL-2 (the harness, which needs both); SL-0 and SL-2 can be drafted while SL-1 runs. The loop card SL-4 starts when the three are done. Round 1 runs on the plan branches as cut, as the baseline; SL-3's recovered fixes merge after it, so their effect shows in a round. See [tasks.md](tasks.md). The first actions on a new machine are in the [handover](handover.md).

## Interfaces and handoff

It consumes the three `release/15/plan-77` branches (App, Agent, Runtime), cut on 21 November from Release 14's integration of Plans 59, 64 and 65; the exact SHAs are in [inputs.md](inputs.md#source-identities). It produces: fixes as PRs into those branches; a fixture and a harness in astrid-app `scripts/save-loop/` that any machine can rerun; and the round rows and plan deltas in [rounds.md](rounds.md), which Plans 63, 75 and 76 and 18 take up.

## Completion

Two consecutive loop rounds, each on a fresh stack installed from the plan branches by SL-1's route, in which every scenario in the matrix either saves within about 2 s ([time to Saved](#terms)) on the heavy fixture or is refused for a real clash with Try again and Discard, with no vanished work and one head. Limits: the fixture is synthetic, so a real-timeline check by the owner stays the owner's; the 2 s figure is a stop-gap, not Plan 75's target.
