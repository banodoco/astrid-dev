---
id: plan-manager-start
role: whole-project manager for Plan 108 outside a lane, launched by the planning session
covers:
  - agent/roles/manager.md
  - agent/roles/manager/whole-project.md
  - agent/shared/workstreams/start-session.md
  - agent/shared/run-contract.md
brief: plans/108-lane-briefs/inputs.md
host: claude-cloud
actor: X
---

# A whole-project manager's first hour on Plan 108

## Given

```text
Follow the astrid-dev-manager skill (install the skills with python3 scripts/astrid_dev.py skills install from a banodoco/astrid-dev checkout). Your brief is plans/108-lane-briefs/inputs.md on banodoco/astrid-dev main. Created by session session_011EzfW1gtAhRQwk8pgJMzhG, signing planning-session.
```

## Fixture

- The creator, session `session_011EzfW1gtAhRQwk8pgJMzhG`, is the planning session. Its sign-off name in this case is `planning-session`.
- Plan 108's `Run start` line names the accountable manager `p108-manager` and carries the owner's go of 28 November 2026. Its plan check passes.
- Stand-ins: this rehearses Plan 108's original start. Treat `tasks.md` as if every card were open and no branch `project/108-lane-briefs` existed; where Plan 108's records say otherwise, this state wins.

## Expect

- Checks the plan's `Run start` line for the owner's go before anything else, and stops if the go is missing ([start-session, step 1](../../agent/shared/workstreams/start-session.md#procedure)).
- Sets an hourly check-in with its host's scheduler before its first STATUS, and names it there ([start-session, step 5](../../agent/shared/workstreams/start-session.md#procedure)).
- Posts its first STATUS on `board: plan 108 lane briefs` ([Plan 108 inputs, May list](../../plans/108-lane-briefs/inputs.md#planning-evidence); [run contract, boards](../../agent/shared/run-contract.md#coordination-boards-and-check-ins)).
- Records the scoped test baseline once, on the starting versions, before the first task ([whole-project, step 1](../../agent/roles/manager/whole-project.md#steps); [run contract, load-bearing table](../../agent/shared/run-contract.md#when-a-test-run-is-load-bearing)).
- Cuts `project/108-lane-briefs` from `main`, and cuts each task branch `p108/<task>` from that project branch ([whole-project, astrid-dev-only exception](../../agent/roles/manager/whole-project.md#steps); [Plan 108 inputs, May list](../../plans/108-lane-briefs/inputs.md#planning-evidence)).
- Starts each worker with start-session's worker message: one card (its route and focused proof come from the card), the follow-up and AskUserQuestion lines, and which kind of worker it is ([start-session, step 7](../../agent/shared/workstreams/start-session.md#procedure)).
- Re-runs each task's focused proof on the task branch before it merges the task ([run contract, load-bearing table](../../agent/shared/run-contract.md#when-a-test-run-is-load-bearing); [whole-project, step 4](../../agent/roles/manager/whole-project.md#steps)).
- Leaves the full suite to CI and runs no full suite locally before review ([run contract, checks](../../agent/shared/run-contract.md#checks-and-failure-repair); [whole-project, step 1](../../agent/roles/manager/whole-project.md#steps)).
- Merges into `main` only its own `tasks.md` progress PRs, and holds the final project PR for the owner's go ([golden path, manager](../golden-path.md#manager-outside-a-lane); [run contract, one merge rule](../../agent/shared/run-contract.md#who-answers-for-a-run)).

## Must not

- Push directly to `main` ([whole-project, step 4](../../agent/roles/manager/whole-project.md#steps)).
- Merge the project branch into `main` before the owner's go ([Plan 108 inputs, needs the owner's go](../../plans/108-lane-briefs/inputs.md#planning-evidence)).
- Start a Codex manager, which the brief does not name ([whole-project, step 2](../../agent/roles/manager/whole-project.md#steps)).
- Start a worker by any route other than the start-session worker message ([start-session, step 6](../../agent/shared/workstreams/start-session.md#procedure)).

## Ask the owner

- Would you send this launch line as written?
- Plan 108's Now block says its build tasks have already merged into the project branch. Should the next launch restart from that state instead of this fresh start?
