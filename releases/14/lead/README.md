# Release 14 Lead handoff

Resume as `r14-lead`. Read the [run board](../run.md) for authority, the dispatch queue and the mailbox cursor. Read [mailbox #796](https://github.com/banodoco/astrid-dev/issues/796) from that cursor for later submissions and handoffs. Schedule the next check-in in 30–60 minutes with `send_later`. The scheduled task **R14 strategic review (every 3 hours)** handles the longer review.

For an independent reviewer, run `codex exec -m gpt-6.2-astra --dangerously-bypass-approvals-and-sandbox -c model_reasoning_effort=<low|medium|high>`, choosing low for mechanical work, medium for bounded fixes and high for gates, design, concurrency or security. If Codex is unavailable, use a Claude sub-agent (owner, 18 Nov).

The [Lead notes](lead-notes.md), [review tiers](review-tiers.md), [gate review notes](gate-common.md) and [18:49 strategy brief](strategy-brief.md) are working notes. The run board records the rulings in force. Substitute the current scratchpad directory for `<scratchpad>`.

[sync-refspecs.sh](sync-refspecs.sh) refreshes fetch refspecs and removes local branches gone from origin, except main and the checked-out branch. [resolve.py](resolve.py) resolves conflicted task rows in place and accepts row preferences such as `GL.2=theirs`. Inspect the resulting diff.
