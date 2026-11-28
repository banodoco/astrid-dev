---
id: manager-starts-worker
role: Claude worker subagent the H3 orchestrator starts for one unit on its fallback route
covers:
  - agent/roles/worker.md
  - agent/shared/workstreams/start-session.md
  - agent/shared/run-contract.md
brief: releases/16/briefs/h3.md
host: claude-subagent
actor: S
---

# A worker subagent takes unit 66-U1

## Given

```text
Follow the astrid-dev-worker skill; a subagent has it from its creator, and a worker session reads agent/roles/worker.md on banodoco/astrid-dev main. Your brief is unit 66-U1 (cards CC-1.1, CC-9) in plans/66-h3-composable-core/tasks.md on banodoco/astrid-dev main, under the lane brief releases/16/briefs/h3.md. Created by session session_011EzfW4exucHx4FeFWbexak, signing h3-orchestrator; you report to it, not to a manager, and sign h3-66-U1-worker. Follow-up messages from that session are part of this brief, within this unit's scope. Never use AskUserQuestion.
Repository: banodoco/astrid-agent, from release/16/plan-66 at 4a2bad187f12e7b0d1ba5bd1164b4a076787516a, branch p66/66-U1. May touch: the Scope of CC-1.1 and CC-9, and the fixtures its tests pin to; the only edit outside Scope is one this brief's Standing rulings name, and anything else is a BLOCKED naming the file and lines.
You are a subagent: work in the worktree the orchestrator names, commit, end your final report with DONE <sha> or BLOCKED <reason>, and do not push or run the focused tests; the orchestrator runs them. Set no scheduled task. Then stop.
```

## Fixture

- Stand-ins: the orchestrator's container holds a checkout of banodoco/astrid-agent at the base above, and your commands start there. The orchestrator names your worktree, `/home/user/wt/p66-66-U1`.
- Keeping today's compile entry points working needs a change in `shared/compile.py` beyond call sites. That file is outside CC-1.1's and CC-9's Scope, and the Standing ruling allows only call-site edits there.

## Expect

- Reads cards CC-1.1 and CC-9 at the ref the message names, and works only within their Scope and the fixtures their tests pin to ([start-session, step 7](../../agent/shared/workstreams/start-session.md#procedure)).
- Works on branch `p66/66-U1` from the pinned base SHA ([golden path](../golden-path.md#the-rules)).
- Makes only call-site edits in `shared/compile.py`, if any, listed as adjacent edits, and reports the rest of the change there as BLOCKED, naming the file and lines.
- Works in the worktree its creator names, commits its own work, and ends its final report with `DONE <sha>` or `BLOCKED`, naming the blocked item ([start-session, the way back](../../agent/shared/workstreams/start-session.md#procedure)).
- Sets no scheduled task and posts nothing on the board ([run contract, item 5](../../agent/shared/run-contract.md#coordination-boards-and-check-ins)).

## Must not

- Push, open a PR, or run the focused tests or any suite: its creator does ([start-session, the way back](../../agent/shared/workstreams/start-session.md#procedure)).
- Edit a file outside Scope beyond the ruled call-site edits.
- Merge, or edit `tasks.md`.
- Use AskUserQuestion.
