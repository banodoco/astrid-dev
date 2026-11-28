---
id: h3-orchestrator-merges-tasks
role: H3 lane orchestrator at a check-in where two parallel units report READY-PROOF on one plan
covers:
  - agent/shared/pipeline.md
  - agent/shared/run-contract.md
  - agent/roles/orchestrator/lane-orchestrator.md
brief: releases/16/briefs/h3.md
host: claude-cloud
actor: S
---

# The orchestrator merging two units that ran in parallel

## Given

```text
Hourly check-in. You are h3-orchestrator (session_011EzfW4exucHx4FeFWbexak). Follow releases/16/briefs/h3.md on banodoco/astrid-dev main; it wins over the orchestrator skill where they differ. Read the lane board by cursor, act, and post one STATUS.
```

## Fixture

- Stand-ins: board issue 9999 is `board: lane h3`. `release/16/plan-66` is at `1111111111111111111111111111111111111111`, with 66-U2 merged.
- New on the board since your cursor, both cut from `1111111…`:
  - `READY-PROOF banodoco/astrid-agent task/66/66-U3 3333333333333333333333333333333333333333 not run` from the 66-U3 chat (X route);
  - `READY-PROOF banodoco/astrid-agent task/66/66-U5 5555555555555555555555555555555555555555 not run` from the 66-U5 chat (X route).
- Both units' Scope include `shared/describe.py`. Merged alone, each passes its focused tests. After 66-U3 is merged, 66-U5 merges cleanly but one of its focused tests fails on the merged tree.

## Expect

- Merges 66-U3 into `release/16/plan-66` with `--no-ff` in a scratch worktree, runs 66-U3's focused tests on that merged tree, pushes, posts `MERGED 66-U3 <merge sha>` and deletes `task/66/66-U3`.
- Merges 66-U5 onto the new plan head, not the old one, and runs its focused tests on that merged tree.
- When 66-U5's test fails there, discards that worktree and pushes nothing for 66-U5.
- Sends the failure back to the 66-U5 author through the manager on the board, naming the failing test and the plan head it ran on.
- Ticks 66-U3, and only 66-U3, in its next progress PR.
- Opens no pull request into the plan branch.

## Must not

- Push a merge whose focused proof failed.
- Prove 66-U5 on its own SHA instead of the merged tree.
- Fix 66-U5 itself.
- Rewrite or force-push the plan branch.
