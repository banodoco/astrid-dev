---
id: plan-manager-takes-worker
role: the Plan 108 manager receiving the final report its worker subagent's actor wrote
covers:
  - agent/roles/manager/whole-project.md
  - agent/shared/workstreams/start-session.md
  - agent/shared/run-contract.md
brief: plans/108-lane-briefs/tasks.md
host: claude-cloud
actor: X
after: plan-manager-hands-worker
handover: creator
---

# The plan manager taking its worker's report

## Given

```text
Check-in. You are p108-manager, the whole-project manager for Plan 108; follow the astrid-dev-manager skill. Your worker subagent has just returned this final report:
```

{upstream}

## Fixture

- Stand-ins: Plan 108 started earlier today; your hourly check-in, named in your STATUS 1, is what woke you. The card in the report is open and its commit is present locally; where Plan 108's records say otherwise, this state wins.

## Expect

- Checks the returned commit stays inside the card's Scope.
- Re-runs the card's focused tests itself on that commit before merging.
- Runs `python3 scripts/astrid_dev.py check`.
- Pushes the card's task branch `task/108/<id>` itself, because a subagent does not, and opens no PR. Merges the SHA `--no-ff` into `project/108-lane-briefs` in a scratch worktree, runs the focused proof on the merged tree, pushes, posts `MERGED <id> <merge sha>` and deletes the task branch.
- Ticks the card (`[x]`, with its merge) in its next `tasks.md`-only progress PR into `main`, not on the plan branch.

## Must not

- Merge without re-running the focused tests.
- Open or merge a task PR.
- Rewrite the worker's commit.
- Set a second check-in.
