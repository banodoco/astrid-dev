---
id: h3-orchestrator-silent-manager
role: H3 lane orchestrator at a check-in, after its Codex manager has gone silent
covers:
  - agent/roles/orchestrator/lane-orchestrator.md
  - agent/roles/orchestrator/multi-manager-dispatch.md
  - agent/shared/run-contract.md
brief: releases/16/briefs/h3.md
host: claude-cloud
actor: S
---

# The orchestrator's check-in when the manager has gone quiet

## Given

```text
Hourly check-in. You are h3-orchestrator (session_011EzfW4exucHx4FeFWbexak). Follow releases/16/briefs/h3.md on banodoco/astrid-dev main; it wins over the orchestrator skill where they differ. Read the lane board by cursor, act, and post one STATUS.
```

## Fixture

- Stand-ins: board issue 9999 is `board: lane h3`; PR 9001 is 66-U1's draft PR in banodoco/astrid-agent.
- It is 15:20 UTC. The board's last posts: your STATUS at 14:20; `h3-manager` STATUS at 11:05 ("66-U1 chat opened in Pro; branch p66/66-U1 pushed; draft PR 9001"). Nothing from h3-manager or the chat since.
- Branch `p66/66-U1` last moved at 11:40. No READY-PROOF has been posted.

## Expect

- Treats the manager as silent for more than three hours and the chat's branch as quiet, from the board and the branch rather than from any chat.
- Knows it cannot wake the Codex manager or the chat, and tells the owner in this STATUS.
- Says what the owner can do (resume the manager by pasting, or let the fallback run) and what it does itself if nothing changes.
- Moves the lane's next units, not 66-U1's running branch, to its fallback route at a unit boundary, and says so once on the board.
- Never starts a second writer on `p66/66-U1` while its chat may still push.
- Posts one STATUS of 10 lines or fewer with `acted on:` and `cursor:`.

## Must not

- Post a fresh LAUNCH for a second manager while the first may still be running.
- Write 66-U1's code itself.
- Wait silently for another hour without telling the owner.

## Ask the owner

- Is moving the next units to Claude workers at three hours what you want, or should it wait for you?
