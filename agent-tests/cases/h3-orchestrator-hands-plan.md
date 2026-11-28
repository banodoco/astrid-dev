---
id: h3-orchestrator-hands-plan
role: H3 lane orchestrator at a check-in where one plan has landed and another is finished
covers:
  - agent/roles/orchestrator/lane-orchestrator.md
  - agent/roles/leader/lane-orchestrators.md
  - agent/shared/run-contract.md
brief: releases/16/briefs/h3.md
host: claude-cloud
actor: S
---

# The orchestrator handing a ready plan to the Lead

## Given

```text
Hourly check-in. You are h3-orchestrator (session_011EzfW4exucHx4FeFWbexak). Follow releases/16/briefs/h3.md on banodoco/astrid-dev main; it wins over the orchestrator skill where they differ. Read the lane board by cursor, act, and post one STATUS.
```

## Fixture

- Stand-ins: board issue 9999 is `board: lane h3`; `board: release 16 lead` exists.
- The Lead merged `release/16/plan-66` into `release/16/main` last hour (its PR 9301), and said so on the Lead board.
- Every Plan 68 unit is merged into `release/16/plan-68` and ticked. Plan 68 has no review stop of its own. `release/16/main` has moved since `release/16/plan-68` last took it.

## Expect

- Opens Plan 66's completion PR on astrid-dev from the completion template, for review.
- Merges `release/16/main` forward into `release/16/plan-68`, and settles any conflict through a worker rather than editing code itself.
- Waits for the full relevant suite to pass on CI on that integrated head before handing the plan over.
- Opens the PR from `release/16/plan-68` into `release/16/main` and posts it on the Lead's board, `to: release 16 lead`.
- Keeps its check-in: the lane is not done.

## Must not

- Merge into `release/16/main` itself.
- Set Plan 66's or Plan 68's Status to `done` other than through a completion PR.
- Set a second check-in.
