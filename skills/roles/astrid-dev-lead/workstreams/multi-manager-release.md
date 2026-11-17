# Workstream: fresh-session ChatGPT packet dispatch

Use when the Lead prepares accepted plan work for an Orchestrator to assign to **a fresh ChatGPT manager session per packet**. The [Lead responsibilities](../SKILL.md) continue to apply.

## Set up once

1. **Prepare packets.** Start from what exists: bring each plan's `tasks.md` up to date with what has merged, and ask any earlier manager to push its work, write a handover and stop; its open drafts become packet inputs. Group ready, compatible task IDs from **one plan** into briefs of at most ~**three human engineering days** each. An **issue packet** groups issues from the brief's list instead; its fix branches `release/<N>/<topic>` target `release/<N>/main`, per [Release](../../../capabilities/astrid-dev-release/SKILL.md). Put them at `releases/<N>/packets/<id>.md` using [the packet template](../../../../templates/release/packet.md). Link, never copy, the tasks, dependencies and proof. Split oversized or unclear tasks in `tasks.md` first. Order the queue by priority and cap what runs at once (Running plus Review) at what you can review.
2. **Prepare one queue.** List each packet in `releases/<N>/run.md` with its handoff state, session and next action. `tasks.md` stays the record of progress.
3. **Own plan-level completion.** For plans assigned through this workstream, record the **Lead as the accountable agent** on its `inputs.md` Run start, with the owner's authorization; there is **no separate plan manager**. You review and land accepted task PRs, keep `tasks.md` current on `main`, and do the plan manager's [Release](../../../capabilities/astrid-dev-release/SKILL.md#how-a-release-runs) steps: merging `release/<N>/main` into plan branches, and landing them. Review stops (RS1, R) are yours: commission an independent reviewer, not a packet.
4. **Prepare the mailbox.** Reuse the release's existing coordination issue, or create one `coordination: Release <N> Lead / Orchestrator` linked from `run.md`. Comments follow the [mailbox protocol](../../astrid-dev-orchestrate/workstreams/codex-cloud/README.md#establish-the-mailbox); no packet issues, no labels.
5. **Hand off to the owner.** Provide queue and mailbox links, ready/blocked packets, any missing authorization and the Orchestrator launch message, filled in from the [run board template](../../../../templates/release/run.md#orchestrator-launch-message). The board's startup checks verify access, session creation, resume, the hour and the mailbox; describe any manual steps.

## At each Lead check-in

**Inputs:** the mailbox since your cursor, open packet PRs, and `python3 scripts/release_branches.py check <N>`.
**Each Review:** accept, merge, open the `tasks.md` progress PR and post DONE; or list the rework on the PR and post a DECISION. A fresh high-judgment sub-agent may review a packet for you; the decision stays yours.
**Then:** move unblocked packets to Ready and write the next; copy the Orchestrator's STATUS into the board; refresh Now and Waiting on the owner. No Orchestrator STATUS for 2 hours, or a message of yours missing from its `acted on:` line, is the owner's to hear. Schedule your own check-ins; if your session cannot, say which nudge the owner gives.
