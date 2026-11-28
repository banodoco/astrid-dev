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
- Pushes the card's branch itself, because a subagent does not, and merges it into `project/108-lane-briefs` only after the re-run passes.
- Ticks the card (`[x]`, with its merge) in its own `tasks.md`-only progress PR into `main`, not on the plan branch.

## Must not

- Merge without re-running the focused tests.
- Rewrite the worker's commit.
- Set a second check-in.
