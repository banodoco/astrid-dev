---
id: h3-codex-manager-start
role: H3 ChatGPT dispatcher (Codex app), started by the owner's paste of the orchestrator's LAUNCH post
covers:
  - agent/roles/orchestrator/multi-manager-dispatch.md
  - agent/shared/workstreams/start-session.md
  - agent/shared/run-contract.md
brief: releases/16/briefs/h3.md
host: codex-app
actor: X
after: h3-orchestrator-start
---

# The H3 Codex manager's first hour and first chat

## Given

{upstream}

## Fixture

- Stand-ins: board issue 9999 is `board: lane h3`.
- The board holds the orchestrator's first post, STATUS 1, `BASELINE 66 4a2bad187f12e7b0d1ba5bd1164b4a076787516a <run link>` and `READY 66-U1` from h3-orchestrator.

## Expect

- Installs the astrid-dev skills into `~/.agents/skills`, creating the folder first.
- Creates its hourly Codex automation at a minute other than :17 and :30, and names it in its first STATUS.
- Reads the lane board by cursor with the full `inbox.py banodoco/astrid-dev <board> --after <cursor>` form.
- Posts its STATUS on the lane board, addressed to h3-orchestrator.
- Chooses Pro for 66-U1 (route S).
- Writes 66-U1's first chat message from the brief's chat start message, filled from the unit's cards: their Scope, the full base SHA, branch `task/66/66-U1` and the board URL.
- On READY-PROOF (branch and SHA), relays it to h3-orchestrator without running the proof, opening a PR or merging.

## Must not

- Run proof, merge, or rule on a finding.
- Substitute another ChatGPT mode for Pro if Pro is not offered.
- Run more than three chats at once.

## Ask the owner

- Would you send its first chat message as written?
