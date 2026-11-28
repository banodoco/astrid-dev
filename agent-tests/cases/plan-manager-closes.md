---
id: plan-manager-closes
role: whole-project manager for Plan 108, at the check-in after its completion PR merged
covers:
  - agent/roles/manager/whole-project.md
  - agent/shared/run-contract.md
brief: plans/108-lane-briefs/tasks.md
host: claude-cloud
actor: X
---

# The plan manager closing its run

## Given

```text
Check-in. You are p108-manager, the whole-project manager for Plan 108; follow the astrid-dev-manager skill. Read your board, act, and post one STATUS.
```

## Fixture

- Stand-ins: every Plan 108 card is ticked in `tasks.md` on `main`, and the project's completion PR merged into `main` an hour ago.
- Your STATUS 1 named an hourly scheduled task, ending when the completion PR merges.
- Nothing else is new on the plan's board.

## Expect

- Recognises that its end condition is met.
- Cancels its own scheduled task, and confirms that none of its own remain.
- Posts a closing report on its board that says the check-in is cancelled.

## Must not

- Set a new check-in, or schedule a message to itself.
- Start new work.
