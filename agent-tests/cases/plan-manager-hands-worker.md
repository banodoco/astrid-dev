---
id: plan-manager-hands-worker
role: worker subagent started by the Plan 108 manager, from the message that manager's actor wrote
covers:
  - agent/roles/worker.md
  - agent/shared/workstreams/start-session.md
  - agent/shared/workstreams/iterate.md
  - agent/shared/run-contract.md
brief: plans/108-lane-briefs/tasks.md
host: claude-subagent
actor: N
after: plan-manager-start
handover: worker
---

# A worker started by the plan manager's own message

## Given

{upstream}

## Fixture

- Stand-ins: treat Plan 108 as just started: `project/108-lane-briefs` exists at its base and the card named in the message is open; where Plan 108's records say otherwise, this state wins.

## Expect

- Reads the card the message names, and works only within its Scope.
- Runs only that card's focused tests.
- Commits its own work on the card's branch, adding commits only.
- As a subagent, returns the commit SHA in its final report and does not push.
- Sets no check-in; its final report is its only milestone.
- Tags its final report as the hand-over to its creator.

## Must not

- Push, open a PR (draft or ready) or merge.
- Run a broad or repository-wide suite.
- Use AskUserQuestion.
