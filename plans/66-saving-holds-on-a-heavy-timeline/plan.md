# Saving holds on a heavy timeline

**Project:** Saving holds on a heavy timeline

**Goal:** On an asset-heavy timeline, every ordinary edit saves in about two seconds, alone, twice back to back, in bursts and as repeated drags, and any refusal is a real clash that the person can retry or discard.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 4 engineering days (3 to 5): about 1.5 for the setup cards, about 0.5 to recover the lost work, and 2 for the first three loop rounds. Further rounds are extra.

**Waiting on:** a machine with 40 GB free disk and the [handover](handover.md) steps; Release 14 owner go to run it. Not in a release brief yet: it is cut as `release/14/plan-66`.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-001 — Reliability isn't proven across supported setups](../../vision/gaps/F-001-platform-reliability.md) (primary): saving is the first thing a person loses work to, so it is a reliability failure. F-001's route does not name this plan, so there is no `Contributes to closure` line.

**Plan type:** a [loop plan](../../skills/roles/astrid-dev-manage/workstreams/live-loop.md). The end state is known; the tasks after the setup cards come from each round's live measurement.

## Outcome and scope

On a synthetic timeline shaped like the owner's heavy one ("Almost Ready" on 18 November), run through the real installed stack:

- every ordinary edit the editor can make saves: alone, twice back to back, ten in a burst, and the same drag repeated;
- nothing vanishes (a failed drop keeps its placeholder; a dropped file is never silently lost);
- a refusal happens only on a real clash, and shows Try again and Discard;
- a save reaches "Saved" in about 2 s or better on the heavy fixture (it is 3.74 s on the real timeline and 0.22 s on one clip);
- the plan deltas for Plans 63 to 65 and 18 (astrid-dev PR #880) are written from this live evidence.

In scope: the fixture, the harness, the loop, recovery of the uncommitted work from the 18 November crash, and the fixes each round picks, in astrid-app, astrid-agent and astrid-runtime. Out of scope: the 300 ms target (Plan 64's), the shot-trim task (its branches are only listed in the [handover](handover.md)), and the [Plan 63](../../plans/index.md) to 65 designs themselves.

## Existing work and decision

The [reviews and profile](inputs.md#planning-evidence) say where the time goes (`validate_final_candidate`, about 57% of a save, with a pass run twice) and why edits are refused. The longer-term plans were costed from design reviews with no live loop on a heavy timeline, and the one-shot sweep of 14 edit kinds on 18 November missed the repeated-gesture failures. So this plan measures first, fixes the cheapest causes, and lets the evidence rewrite the longer plans. The 14-kind sweep harness is the seed; its first run saved 3 and refused 11, and it died when the disk filled.

## Sequence and readiness

Setup cards SL-0 to SL-3 run mostly in parallel; the loop card SL-4 starts when SL-0, SL-1 and SL-2 are done. SL-3 may finish during the first rounds. See [tasks.md](tasks.md). The first actions on a new machine are in the [handover](handover.md).

## Interfaces and handoff

It consumes the three `release/14/plan-66` branches (App, Agent, Runtime), cut from `release/14/plan-59`; the exact SHAs are in [inputs.md](inputs.md#source-identities). It produces: fixes as PRs into those branches; a fixture and a harness in astrid-app `scripts/save-loop/` that any machine can rerun; and the round rows and plan deltas in [rounds.md](rounds.md), which Plans 63 to 65 and 18 take up.

## Completion

Two consecutive loop rounds, on a fresh stack built through the release script, in which every scenario in the matrix either saves within about 2 s on the heavy fixture or is refused for a real clash with Try again and Discard, with no vanished work and one head. Limits: the fixture is synthetic, so a real-timeline check by the owner stays his; the 2 s figure is a stop-gap, not Plan 64's target.
