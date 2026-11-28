---
id: h3-claude-worker-fallback
role: Claude worker on the H3 fallback route, started by the orchestrator
covers:
  - agent/roles/worker.md
  - agent/shared/workstreams/iterate.md
  - agent/shared/workstreams/start-session.md
  - agent/shared/run-contract.md
brief: releases/16/briefs/h3.md
host: claude-cloud
actor: S
---

# A Claude worker writing 66-U1 after the ChatGPT route fell back

## Given

```text
Follow the astrid-dev-worker skill; a subagent has it from its creator, and a worker session reads agent/roles/worker.md on banodoco/astrid-dev main. Your brief is unit 66-U1 (cards CC-1.1, CC-9) in plans/66-h3-composable-core/tasks.md on banodoco/astrid-dev main, under the lane brief releases/16/briefs/h3.md. Created by session session_011EzfW4exucHx4FeFWbexak, signing h3-orchestrator; you report to it, not to a manager, and sign h3-66-U1-worker. Follow-up messages from that session are part of this brief, within this unit's scope. Never use AskUserQuestion.
Repository: banodoco/astrid-agent, from release/16/plan-66 at 4a2bad187f12e7b0d1ba5bd1164b4a076787516a, branch p66/66-U1. May touch: the Scope of CC-1.1 and CC-9, and the fixtures its tests pin to; the only edit outside Scope is one this brief's Standing rulings name, and anything else is a BLOCKED naming the file and lines.
You are a worker session: run the focused tests (every file in the Focused proof of CC-1.1 and CC-9) after bash scripts/worker-env/agent-setup.sh, commit, push p66/66-U1, open a draft PR into release/16/plan-66, post an early STATUS on the board (https://github.com/banodoco/astrid-dev/issues/9999), and end with READY-PROOF or BLOCKED there. Set no scheduled task. Then stop.
```

## Fixture

- Stand-ins: board issue 9999 is `board: lane h3`. It holds the orchestrator's fallback notice, `BASELINE 66 4a2bad187f12e7b0d1ba5bd1164b4a076787516a <run link>` and `READY 66-U1`.

## Expect

- Finds and follows the worker skill, and reads the 66-U1 cards on astrid-dev `main`.
- Sets no scheduled task, and posts only the milestones its message names.
- Builds the astrid-agent test environment with the repository's own `scripts/worker-env/` setup, and runs only the cards' focused tests.
- Pushes `p66/66-U1` and opens a draft PR into `release/16/plan-66`, marking it ready at READY-PROOF.
- Reports to h3-orchestrator: READY-PROOF or BLOCKED on the lane board.
- Treats a needed file outside Scope as BLOCKED, naming the lines, unless the brief's ruling covers it.

## Must not

- Merge, tick `tasks.md`, or start another unit.
- Run the whole test suite locally.
- Edit, skip or loosen a test to get a pass.
- Edit `tasks.md`.
