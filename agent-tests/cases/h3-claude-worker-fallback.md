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
actor: N
---

# A Claude worker writing 66-U1 after the ChatGPT route fell back

## Given

```text
Follow the astrid-dev-worker skill (install the skills from a banodoco/astrid-dev checkout: mkdir -p ~/.claude/skills && python3 scripts/astrid_dev.py skills install --destination ~/.claude/skills). Your brief is unit 66-U1 (cards CC-1.1, CC-9) in plans/66-h3-composable-core/tasks.md on banodoco/astrid-dev main, under the lane brief releases/16/briefs/h3.md. Work in banodoco/astrid-agent from release/16/plan-66 at 4a2bad187f12e7b0d1ba5bd1164b4a076787516a, branch p66/66-U1. Created by session session_011EzfW4exucHx4FeFWbexak, signing h3-orchestrator; you report to it, not to a manager. Follow-up messages from that session are part of this brief, within this unit's scope. Never use AskUserQuestion. Post only milestones on the board (https://github.com/banodoco/astrid-dev/issues/9999): early STATUS, READY-PROOF or BLOCKED; set no scheduled task. Then stop.
```

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
