---
id: lead-divides-lanes
role: Release 16 Lead, asked by the owner to propose lanes for Release 16
covers:
  - agent/roles/leader.md
  - agent/roles/leader/lane-orchestrators.md
  - agent/shared/workstreams/release.md
brief: releases/16.md
host: claude-cloud
actor: X
---

# The Release 16 Lead proposes lanes and waits for the owner

## Given

```text
Follow the astrid-dev-leader skill (install the skills with python3 scripts/astrid_dev.py skills install from a banodoco/astrid-dev checkout). You are the Release 16 Lead. Propose the lanes for Release 16 and post the options on your Lead board. I will choose.
```

## Fixture

- Stand-ins: the owner has recorded the handoff of the Release 16 Lead to this session; where `releases/16/run.md` names an earlier Lead, this state wins.
- The plans to place are those in the H-3 card of `plans/108-lane-briefs/tasks.md`: Plans 93, 94 and 38 (active); Plans 09, 10, 29, 30, 31, 04, 63, 79, 90 and 87 (unstarted); and the H3 programme (Plans 66, 68, 70 and 67).
- The H3 lane already runs under `releases/16/briefs/h3.md` (State `running`, the owner's go of 28 November 2026). Re-laning it is the owner's decision alone.
- `releases/16/run.md` records no lane split beyond the H3 lane.
- The owner has asked this session to act as the Release 16 Lead.

## Expect

- Offers two or three genuinely different groupings, not one grouping with variants ([lanes, step 1](../../agent/roles/leader/lane-orchestrators.md#1-propose-two-or-three-groupings)).
- For each grouping, says which plans share a lane and which run alone, with the reason ([leader's lane rules](../../agent/roles/leader.md#divide-the-release-into-lanes)).
- For each grouping, says how each lane runs (hosted or packets) and the orchestrator's route, X or S ([lanes, step 1](../../agent/roles/leader/lane-orchestrators.md#1-propose-two-or-three-groupings)).
- For each grouping, gives its cut line, its cross-lane coordination and the cost to the owner in lanes they would follow ([lanes, step 1](../../agent/roles/leader/lane-orchestrators.md#1-propose-two-or-three-groupings)).
- Keeps the running H3 lane as it stands in every option, or names any re-lane of it as the owner's decision ([lanes, re-laning](../../agent/roles/leader/lane-orchestrators.md#how-it-runs)).
- Ends with one recommendation and its reason, then stops ([lanes, step 1](../../agent/roles/leader/lane-orchestrators.md#1-propose-two-or-three-groupings)).
- Posts the options on `board: release 16 lead` and tells the owner they are waiting on a choice ([golden path, Release Lead](../golden-path.md#release-lead); [Plan 108 H-3](../../plans/108-lane-briefs/tasks.md)).

## Must not

- Choose the split alone; the owner chooses ([Plan 108 D2](../../plans/108-lane-briefs/inputs.md#owner-decisions)).
- Write or merge any lane brief before the owner has chosen ([lanes, step 1](../../agent/roles/leader/lane-orchestrators.md#1-propose-two-or-three-groupings)).
- Record a split on `releases/16/run.md` before the owner has chosen ([lanes, step 2](../../agent/roles/leader/lane-orchestrators.md#2-record-the-agreed-split-on-the-run-board)).
- Send any lane's launch line, or tell a lane to start ([leader](../../agent/roles/leader.md#divide-the-release-into-lanes); [start-session, step 6](../../agent/shared/workstreams/start-session.md#procedure)).

## Ask the owner

- Which grouping do you choose, or what would you change?
- `releases/16.md` still reads "Release manager: not yet named". Should this session be recorded there as the Lead?
- Does the H3 lane stay exactly as briefed in every option?
- [lanes, step 1](../../agent/roles/leader/lane-orchestrators.md#1-propose-two-or-three-groupings) says to post the proposal on "the run board", but [release.md](../../agent/shared/workstreams/release.md#keep-the-releases-records) calls `releases/16/run.md` the live board and the Lead's board is an issue. Which one should carry the options?
