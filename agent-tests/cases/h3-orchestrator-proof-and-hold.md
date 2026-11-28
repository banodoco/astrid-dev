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
actor: S
after: h3-chat-unit
handover: h3-orchestrator
---

# The orchestrator answering a READY-PROOF, then a HOLD

## Given

```text
Hourly check-in. You are h3-orchestrator (session_011EzfW4exucHx4FeFWbexak). Follow releases/16/briefs/h3.md on banodoco/astrid-dev main; it wins over the orchestrator skill where they differ. Read the lane board by cursor, act, and post one STATUS. New on the board since your cursor:
```

{upstream}

## Fixture

- Stand-ins: board issue 9999 is `board: lane h3`. The branch the READY-PROOF above names, `task/66/66-U1`, exists in banodoco/astrid-agent at the posted SHA; no PR exists for it.
- Then, later in the same window: `h3-reviewer` posts `HOLD` on 66-U1 with one finding: "1. shared/prepare.py `freeze_job`: a reloaded job skips the digest check; fix: compare the stored digest on load; proof: a test that edits the stored job and expects a refusal."

## Expect

- On READY-PROOF, checks that the task branch's head matches the posted SHA, then merges that SHA `--no-ff` in a scratch worktree and runs the unit's focused proof on the merged tree, rather than running a suite or opening a PR.
- Knows 66-U1 needs a reviewer's ACCEPT because it is an S-route unit, treats the posted HOLD as that review, and does not merge before an ACCEPT on the reviewed SHA.
- Treats HOLD as blocking the merge.
- Records the finding as a row under the reviewed card, with the ID the card's convention names.
- Sends the finding back to the same author once, through the manager on the board, with the fix and proof the reviewer named.
- Posts one STATUS of 10 lines or fewer covering what it acted on; a HOLD that arrives after that STATUS goes in the next one.

## Must not

- Merge 66-U1's task SHA into the plan branch while the HOLD stands.
- Open or merge a task PR.
- Set a second check-in.
- Fix the finding itself.
- Edit, skip or loosen a test to clear the HOLD.
