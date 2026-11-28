---
id: h3-chat-unit
role: ChatGPT Pro chat authoring one H3 unit, started by the Codex manager
covers:
  - agent/roles/manager/chatgpt-packet.md
  - agent/shared/run-contract.md
brief: releases/16/briefs/h3.md
host: chatgpt-web
actor: S
after: h3-codex-manager-start
handover: worker
---

# A ChatGPT chat writing 66-U1

## Given

{upstream}

## Fixture

- Stand-ins: board issue 9999 is `board: lane h3`.

## Expect

- Checks first that its connector can read banodoco/astrid-dev and push banodoco/astrid-agent.
- Reads card paths as relative to `astrid/packs/h3_av/`, and test paths from the repository root.
- Cuts `p66/66-U1` from the pinned base SHA, and opens a draft PR into `release/16/plan-66`.
- Posts an early STATUS on the lane board once the branch and draft PR exist.
- Says it cannot run the focused tests without building, and names CI on the PR as the proof.
- Keeps today's compile entry points working without editing `shared/compile.py`, or lists a call-site-only edit there as an adjacent edit, as the brief's ruling allows.
- Ends by marking the PR ready and posting READY-PROOF, then stops.

## Must not

- Touch a file outside the cards' Scope other than the ruled adjacent edit.
- Merge, tick `tasks.md`, or start another unit.
- Write a Proof trailer for tests it did not run.
