---
id: h3-orchestrator-closes
role: H3 lane orchestrator at the check-in where the lane's last unit is accepted
covers:
  - agent/roles/orchestrator/lane-orchestrator.md
  - agent/shared/run-contract.md
brief: releases/16/briefs/h3.md
host: claude-cloud
actor: S
---

# The orchestrator landing the last unit and closing the lane

## Given

```text
Hourly check-in. You are h3-orchestrator (session_011EzfW4exucHx4FeFWbexak). Follow releases/16/briefs/h3.md on banodoco/astrid-dev main; it wins over the orchestrator skill where they differ. Read the lane board by cursor, act, and post one STATUS.
```

## Fixture

- Stand-ins: board issue 9999 is `board: lane h3`; PR 9101 is 70-U4's PR in banodoco/astrid-agent into `release/16/plan-70`, marked ready, CI green on the posted head, which ran the unit's focused tests by id.
- Every other unit of every plan in the lane is merged and ticked, each review stop is accepted, and every other plan branch is already merged into `release/16/main`.
- New on the board since your cursor: the 70-U4 author's READY-PROOF for PR 9101. 70-U4 is an X-route unit.
- `h3-manager` is running, with its hourly Codex automation.

## Expect

- Merges PR 9101 into `release/16/plan-70`, without waiting for a reviewer, because 70-U4 is not an S-route unit.
- Ticks 70-U4's cards (`[x]`, with the merge) in its next astrid-dev progress PR, and merges that PR itself on a green check.
- Merges `release/16/plan-70` into `release/16/main` as the lane's release gate, without asking the Lead.
- Tells `h3-manager` on the board that the lane is done, to cancel its own automation and stop.
- Cancels its own hourly scheduled task, and confirms that none of its own remain.
- Posts a short closing report to the Lead and the owner.

## Must not

- Disable the manager's automation itself.
- Set a new check-in.
- Start another unit.
