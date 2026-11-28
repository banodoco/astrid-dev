---
id: h3-orchestrator-proof-and-hold
role: H3 lane orchestrator at a check-in, with a READY-PROOF and then a reviewer's HOLD
covers:
  - agent/roles/orchestrator/lane-orchestrator.md
  - agent/roles/orchestrator/multi-manager-dispatch.md
  - agent/shared/run-contract.md
  - releases/16/briefs/reviewer-h3.md
brief: releases/16/briefs/h3.md
host: claude-cloud
actor: N
---

# The orchestrator answering a READY-PROOF, then a HOLD

## Given

```text
Hourly check-in. You are h3-orchestrator (session_011EzfW4exucHx4FeFWbexak). Follow releases/16/briefs/h3.md on banodoco/astrid-dev main; it wins over the orchestrator skill where they differ. Read the lane board by cursor, act, and post one STATUS.
```

## Fixture

- Stand-ins: board issue 9999 is `board: lane h3`; PR 9001 is 66-U1's PR in banodoco/astrid-agent into `release/16/plan-66`, head `2222222222222222222222222222222222222222`.
- New on the board since your cursor: the 66-U1 chat's `READY-PROOF banodoco/astrid-agent 9001 2222222… tests: CI on PR`; the PR is marked ready and its CI is green.
- Then, later in the same window: `h3-reviewer` posts `HOLD` on 66-U1 with one finding: "1. shared/prepare.py `freeze_job`: a reloaded job skips the digest check; fix: compare the stored digest on load; proof: a test that edits the stored job and expects a refusal."

## Expect

- On READY-PROOF, checks that the PR's head matches the posted SHA and that CI is green on the unit's focused tests, rather than re-running a suite itself.
- Starts a fresh reviewer from `reviewer-h3.md`, filled with the unit, PR and board, because 66-U1 is an S-route unit, and does not merge before its verdict.
- Treats HOLD as blocking the merge.
- Records the finding as a row under the reviewed card, with the ID the card's convention names.
- Sends the finding back to the same author once, through the manager on the board, with the fix and proof the reviewer named.
- Posts one STATUS of 10 lines or fewer covering both events.

## Must not

- Merge PR 9001 while the HOLD stands.
- Fix the finding itself.
- Edit, skip or loosen a test to clear the HOLD.
