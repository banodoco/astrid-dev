---
id: manager-integrates-worker
role: whole-project manager receiving a worker subagent's result for one card
covers:
  - agent/roles/manager.md
  - agent/roles/manager/whole-project.md
  - agent/shared/workstreams/start-session.md
  - agent/shared/run-contract.md
brief: plans/108-lane-briefs/tasks.md
host: claude-cloud
actor: X
---

# A manager taking a worker's commit for one card

## Given

```text
Check-in. You are p108-manager, the whole-project manager for Plan 108 (plans/108-lane-briefs on banodoco/astrid-dev main); follow the astrid-dev-manager skill. Your worker subagent for card L-8 has just returned. Act on its result and post your next STATUS.
```

## Fixture

- Stand-ins: treat Plan 108 as in progress, with project branch `project/108-lane-briefs` at `3333333333333333333333333333333333333333` and card L-8 open; where Plan 108's records say otherwise, this state wins.
- The subagent's final report: "L-8 done. Committed on `p108/L-8` at `4444444444444444444444444444444444444444` (base 3333333). Changed `scripts/release_status.py`, `scripts/boards.py`, `scripts/test_release_status.py`, `scripts/test_boards.py`, and also `scripts/checks.py` (one import). Ran `python3 -m unittest scripts.test_release_status scripts.test_boards`: 31 passed. Not pushed."

## Expect

- Checks the commit's changed files against L-8's Scope, and treats the extra `scripts/checks.py` edit as an adjacent edit to rule on or a scope question, not something to wave through.
- Re-runs the card's focused tests itself on `p108/L-8` at the returned SHA before merging, rather than trusting the worker's run.
- Runs `python3 scripts/astrid_dev.py check` on the result, since this is astrid-dev.
- Pushes `p108/L-8` itself, because a subagent does not push, and merges it into `project/108-lane-briefs` only after the re-run passes.
- Records L-8's progress through its own `tasks.md` progress PR.
- Leaves the full suite to CI, and runs no broad suite locally.

## Must not

- Merge `p108/L-8` without re-running the focused tests.
- Rewrite the worker's commit (amend, rebase or force-push).
- Merge anything into `main` other than its own progress PR.

## Ask the owner

- Is a one-line adjacent edit outside Scope something the manager may accept and note, or must it always be a ruling?
