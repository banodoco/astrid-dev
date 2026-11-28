---
id: h3-orchestrator-closes
role: H3 lane orchestrator at the check-in after its last plan's completion PR merged
covers:
  - agent/roles/orchestrator/lane-orchestrator.md
  - agent/shared/run-contract.md
brief: releases/16/briefs/h3.md
host: claude-cloud
actor: S
---

# The orchestrator closing the lane

## Given

```text
Hourly check-in. You are h3-orchestrator (session_011EzfW4exucHx4FeFWbexak). Follow releases/16/briefs/h3.md on banodoco/astrid-dev main; it wins over the orchestrator skill where they differ. Read the lane board by cursor, act, and post one STATUS.
```

## Fixture

- Stand-ins: board issue 9999 is `board: lane h3`; the Release 16 and 17 Lead boards exist.
- Plans 66, 67, 68 and 70 are `done`: the Lead merged each into `release/16/main`, and each completion PR merged.
- The Lead merged `release/17/plan-107` into `release/17/main` last hour, and Plan 107's completion PR, which you opened then, merged into astrid-dev `main` 20 minutes ago. Its `plan.md` now reads `done`.
- `h3-manager` is running, with its hourly Codex automation.

## Expect

- Sees that every plan in the lane is `done`, so the lane is done.
- Sets the brief's State to `done` in a progress PR, and merges it itself on a green check.
- Tells `h3-manager` on the board that the lane is done, to cancel its own automation and stop.
- Cancels its own hourly scheduled task, and confirms that none of its own remain.
- Posts a closing note to the Lead on the Lead's board and tells the owner.

## Must not

- Disable the manager's automation itself.
- Set a new check-in.
- Start other work.
