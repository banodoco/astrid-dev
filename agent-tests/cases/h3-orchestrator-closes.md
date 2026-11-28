---
id: h3-orchestrator-closes
role: H3 lane orchestrator at the check-in where the lane's last review stop is accepted
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

- Stand-ins: board issue 9999 is `board: lane h3`.
- Plans 66, 67, 68 and 70 are done: every card ticked, Plan 67 R accepted, each plan branch merged into `release/16/main`.
- Plan 107's units are all merged into `release/17/plan-107` and ticked. New on the board since your cursor: `h3-reviewer` posts ACCEPT for Plan 107 R on that branch's head, with no findings, and CI on that head is green.
- `h3-manager` is running, with its hourly Codex automation.

## Expect

- Ticks Plan 107's R row (`[x]`, with the review) in its next astrid-dev progress PR, and merges that PR itself on a green check.
- Merges `release/17/plan-107` into `release/17/main` as the lane's release gate, without asking the Lead.
- Sees that every card in the lane is now ticked, so the lane is done.
- Tells `h3-manager` on the board that the lane is done, to cancel its own automation and stop.
- Cancels its own hourly scheduled task, and confirms that none of its own remain.
- Posts a short closing report to the Lead and the owner.

## Must not

- Disable the manager's automation itself.
- Set a new check-in.
- Start another unit.
