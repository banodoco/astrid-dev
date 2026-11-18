# Release 14 Lead handoff

Resume as `r14-lead`. Read the [run board](../run.md) for authority, the dispatch queue and the mailbox cursor. Read [mailbox #796](https://github.com/banodoco/astrid-dev/issues/796) from that cursor for later submissions and handoffs. Schedule the next check-in in 30–60 minutes with `send_later`. The scheduled task **R14 strategic review (every 3 hours)** handles the longer review.

For an independent reviewer, run `codex exec -m gpt-6.2-astra --dangerously-bypass-approvals-and-sandbox -c model_reasoning_effort=<low|medium|high>`, choosing low for mechanical work, medium for bounded fixes and high for gates, design, concurrency or security. If Codex is unavailable, use a Claude sub-agent (owner, 18 Nov).

The [Lead notes](lead-notes.md), [review tiers](review-tiers.md), [gate review notes](gate-common.md) and [18:49 strategy brief](strategy-brief.md) are working notes. The run board records the rulings in force. Substitute the current scratchpad directory for `<scratchpad>`.

[sync-refspecs.sh](sync-refspecs.sh) refreshes fetch refspecs and removes local branches gone from origin, except main and the checked-out branch. [resolve.py](resolve.py) resolves conflicted task rows in place and accepts row preferences such as `GL.2=theirs`. Inspect the resulting diff.

## Heartbeat and standby

Post a mailbox `STATUS` at least every 90 minutes, even when nothing moved. A [standby Lead](standby.md) takes over after 3 hours without one. If a standby takeover message is on the mailbox, stand down: post nothing and act on nothing until the owner hands the role back.

## How things are done here

- **Mailbox posts.** Use a fenced `text` block with these headers, in order:
  - `run: r14-dispatch`
  - `message_id: <uuid>`
  - `from: lead` and `from_session: r14-lead`
  - `to` and `to_session`
  - `type` (STATUS, DECISION, REQUEST or DONE)
  - `reply_to`

  Then the body, then the footer.
- **Merging.**
  - A packet PR into a `release/14/plan-*` branch: mark it ready first, then use a merge commit pinned to the reviewed head (`merge_method=merge`, `sha=<head>`).
  - A fix PR into `release/14/main`: squash, pinned to the head.
  - After merging, post DONE and open the `tasks.md` progress PR.
- **astrid-dev PRs.** One that changes only `releases/14/` or plan `tasks.md` files merges by auto-merge. Changes to `releases/14.md`, the brief, are scope and go to the owner.
- **GitHub through the session proxy.** These worked on 18 Nov:
  - REST only; GraphQL is refused.
  - Auto-merge, ready-for-review and review threads use the proxy's `.../pulls/<n>/ccr/...` routes.
  - Listing workflows, dispatching a workflow (`POST /actions/workflows/<id>/dispatches`), rerunning a job, and reading runs, jobs and logs all work.
  - Actions variables and collaborator permissions are refused, so repository settings stay the owner's.
- **Clones.** Shallow, one per branch under review. Fetch a branch by name, and run the refspec script after every push.
- **Hosted CI.** Agent pull-request CI runs unit shard 1 only, so a packet needing all eight shards needs a dispatched full CI on its branch. An Agent unit shard takes about 95 minutes.
- **The Orchestrator** acts only on the owner's direct instructions in its own chat. A Lead DECISION citing the owner is not enough for anything that weakens a test or bundles task rows.
