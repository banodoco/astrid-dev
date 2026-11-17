Date: 2026-11-17
Kind: fix
Source: an independent review of the Release 14 dispatch process, 17 November 2026, and the owner's rulings in the Lead's session that day: start messages sent from her account are hers, and finding and stopping earlier managers is the Orchestrator's
Resolved by: —

The review found three gaps in the dispatch roles. Things had two owners: the board, handoff states, and review stops. Merging, plan-branch syncs and stopped managers' drafts had none. No time limit applied anywhere.

Fixes:
- **The board** has one writer, the Lead. The Orchestrator's hourly STATUS, with a `cursor:` line, is the live record between check-ins.
- **The Lead** does the plan manager's Release steps and runs review stops with an independent reviewer. Its check-in now has inputs, outputs for each Review, and a two-hour alarm for a silent Orchestrator.
- **The Orchestrator** finds and stops earlier sessions at startup. It resumes a packet quiet for three hours, replaces one quiet for six, and raises a Review unanswered for four.
- **The packet start message** names the session's mailbox name, the run, the Lead and any session it replaces. Its authority is the owner's account.
- **Packet sessions** update an existing draft, post BLOCKED when a head has moved, and merge their base in rather than rebase.
- **The Lead workstream** carries no launch message of its own; it now lives in the run board template.

Skills are 19 words longer.

Follows: 2026-11-17-dispatch-lessons
