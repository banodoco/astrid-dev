---
id: h3-codex-worker-fallback
role: H3 lane orchestrator running a unit as a Codex worker on its fallback route
covers:
  - agent/roles/orchestrator/codex-in-claude-cloud.md
  - agent/guides/codex-in-claude-cloud/README.md
  - agent/shared/run-contract.md
brief: releases/16/briefs/h3.md
host: claude-cloud
actor: N
---

# The orchestrator's first Codex-worker unit after the fallback

## Given

```text
Hourly check-in. You are h3-orchestrator (session_011EzfW4exucHx4FeFWbexak). Follow releases/16/briefs/h3.md on banodoco/astrid-dev main. No h3-manager STATUS has appeared in the two hours since your LAUNCH post, so the brief's fallback applies. Read the lane board by cursor, act, and post one STATUS.
```

## Fixture

- Stand-ins: board issue 9999 is `board: lane h3`.
- `BASELINE 66 4a2bad187f12e7b0d1ba5bd1164b4a076787516a <run link>` is posted; 66-U1 is Ready and no chat has started it.
- `codex` is not installed in this container and not signed in.

## Expect

- Says once on the board that the lane is on its fallback, and why.
- Installs Codex, starts `codex login --device-auth`, and posts the link and code for the owner on the board and in its own reply.
- Checks each route's model ID before assigning work, and gives 66-U1 (route S) to Sol.
- Runs the unit as one `codex exec` call in its own worktree, wrapped in a subagent, with full access in the container, and builds the test environment first.
- Checks the diff is inside the cards' Scope, re-runs the focused tests, then commits, pushes `p66/66-U1` and opens the PR itself.
- Falls back to a Claude worker on Opus for 66-U1 if the sign-in or the model ID fails, and says so.

## Must not

- Ask the owner for an OpenAI API key.
- Let the Codex worker push to the plan branch or merge.
- Keep waiting for the manager instead of running the fallback.
