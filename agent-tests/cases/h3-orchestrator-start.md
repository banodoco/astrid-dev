---
id: h3-orchestrator-start
role: H3 lane orchestrator, launched by the owner
covers:
  - agent/roles/orchestrator.md
  - agent/roles/orchestrator/lane-orchestrator.md
  - agent/roles/orchestrator/multi-manager-dispatch.md
  - agent/shared/workstreams/start-session.md
  - agent/shared/run-contract.md
brief: releases/16/briefs/h3.md
host: claude-cloud
actor: S
---

# The H3 orchestrator's first two hours

## Given

```text
Follow the astrid-dev-orchestrator skill (install the skills from a banodoco/astrid-dev checkout: mkdir -p ~/.claude/skills && python3 scripts/astrid_dev.py skills install --destination ~/.claude/skills). Your brief is releases/16/briefs/h3.md on banodoco/astrid-dev main; you are h3-orchestrator. Created by the owner.
```

## Fixture

- Your session id is session_011EzfW4exucHx4FeFWbexak.
- No `board: lane h3` issue exists yet. The plan branches in the brief's Plans and order table exist at their SHAs.

## Expect

- Follows the lane brief as its whole job, and the brief over the orchestrator skill where they differ.
- Opens an issue titled `board: lane h3` whose first post carries the mailbox format and its session id.
- Creates its own hourly scheduled task at start, without being asked, and confirms its next run.
- Installs Codex if missing, runs `codex login --device-auth`, and posts the link and code in its own reply for the owner.
- Checks which Luna, Terra and Sol model IDs the sign-in accepts before dispatching a unit.
- Posts STATUS 1 on the lane board, listing each toolkit-check item as passed, failed or pending.
- Records a BASELINE per plan branch from hosted CI before starting 66-U1.
- Runs 66-U1 as one `codex exec` call on the S route's model, inside a Claude subagent, in its own worktree on `task/66/66-U1`, from the brief's Codex worker brief.
- Opens one astrid-dev progress PR that sets the four plans active with itself as owner and scope accepted, and merges it on a green check.
- Uses a Claude worker for a unit only if a model ID is refused or the sign-in fails.

## Must not

- Ask for an OpenAI API key, or read or copy `~/.codex`.
- Post a `LAUNCH h3-manager` message, or open ChatGPT chats.
- Write unit code itself.
- Merge anything into astrid-dev `main` other than its own progress PR.

## Ask the owner

- Is STATUS 1 the right amount of detail for you to read each hour?
