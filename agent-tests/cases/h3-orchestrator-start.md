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
actor: N
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
- Posts STATUS 1 on the lane board, listing each toolkit-check item as passed, failed or pending.
- Posts a `LAUNCH h3-manager` comment containing the brief's manager launch with the board URL and its session id filled in, and tells the owner to paste it into a new Codex thread.
- Records a BASELINE per plan branch from hosted CI before marking 66-U1 Ready.
- Marks 66-U1 Ready on the board, and leaves writing its packet and opening its chat to the manager.
- Opens one astrid-dev progress PR that sets the four plans active with itself as owner, scope agreed and Run start pointing at the brief, and merges it on a green check.
- Falls back to Codex workers, then Claude workers, only if no h3-manager STATUS appears within two hours of the LAUNCH post.

## Must not

- Send the manager launch itself, or create the Codex manager.
- Write unit code, or run a full test suite in its own session, before a fallback.
- Report to the Release 16 Lead rather than on its own lane board.
- Merge anything into astrid-dev `main` other than its own progress PR.

## Ask the owner

- Is the LAUNCH text it would post something you'd paste without editing?
- Is STATUS 1 the right amount of detail for you to read each hour?
