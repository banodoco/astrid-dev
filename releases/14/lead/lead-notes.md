Lead notes
- Reviews: codex exec -m gpt-6.2-astra (owner, 11:08 18 Nov). Effort by risk: low mechanical, medium bounded fix, high gates/designs/concurrency/security.
- Full permissions: --dangerously-bypass-approvals-and-sandbox (owner-approved).
- Gate threat model: PRACTICAL (owner 12:50 18 Nov; mailbox 6979024059). Realistic weakening only; crafted bypasses are a stated limit; max two review rounds; GL.3 closed. Use briefs/gate-common.md.
- Lead is a LIGHT gatekeeper (owner, ~14:00 18 Nov): filter reviewer findings. Block only on wrong results accepted, data/install damage, real security/custody holes, regressions from base. Everything else -> follow-up row. Append briefs/review-tiers.md to every review brief.
- P55-08 follow-ups filed as astrid-dev #896 (backlog), not a row.
- Follow-ups lever (owner, ~14:10 18 Nov): FOLLOW-UP/NOTE findings that are nice-to-have or poor structure -> one astrid-dev issue (observation form: What I saw / About; search first; then label backlog), linked from the PR. tasks.md rows only for work the release must do.
- Owed: board row R14-FIX-11 for astrid-dev #905 (cleanup ACK during activation; Agent issue packet after FIX-10), packet file, and #905 cited from the brief issue list.
- Owner decisions 18 Nov 18:35: P55-10 meter "Report totals, gate invariants" (approved changing existing cap assertions; mailbox decision). Record in board Decided.
- STANDBY (owner, 18 Nov ~19:45): a Codex Astra standby takes over after 3h without a Claude Lead heartbeat (releases/14/lead/standby.md). At EVERY check-in: (1) first check the mailbox for a standby takeover message (from_session r14-lead WITHOUT the Claude Code footer, starting "Lead continuity:"); if one exists, stand down: post nothing, do nothing, tell the owner only. (2) post a short Lead STATUS heartbeat if my last mailbox post is older than 60 minutes (must be at least every 90).
- RUN CODEX JOBS AS TRACKED BACKGROUND TASKS (run_in_background), never detached nohup: the machine restarted at 23:34 and 00:07 when only detached jobs were running, killing them.

## Cursor rule (04:05 UTC, 19 Nov)
Pass check.py the id of the last comment I READ, never my own newest post. Using my post id skipped 6998856096 (P39-13 frozen for shard dispatch) for about 40 minutes.
