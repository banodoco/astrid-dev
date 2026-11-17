# Workstream: fresh-session ChatGPT packet dispatch

Use when the Lead prepares accepted plan work for a Codex Orchestrator to assign to **a fresh ChatGPT manager session per packet**. The [Lead responsibilities](../SKILL.md) continue to apply.

## Set up once

1. **Prepare packets.** Read the brief and the plans' `tasks.md`. Group ready, compatible task IDs from **one plan** into briefs of at most ~**three human engineering days** each. An **issue packet** groups issues from the brief's list instead; its fix branches `release/<N>/<topic>` target `release/<N>/main`, per [Release](../../astrid-dev-release/SKILL.md). Put them at `releases/<N>/packets/<id>.md` using [the packet template](../../../templates/release/packet.md). Link, never copy, the tasks, dependencies and proof. Split oversized or unclear tasks in `tasks.md` first.
2. **Prepare one queue.** Link each packet from `releases/<N>/run.md`, with Ready / Running / Review / Blocked / Done, the packet session and next action. The Orchestrator updates dispatch state after setup; `tasks.md` remains the source of truth for engineering progress.
3. **Own plan-level completion.** For plans assigned through this workstream, record the **Lead as the accountable agent for the plan run** in its `inputs.md` Run start, subject to the owner's authorization. There is **no separate ongoing plan manager**. Each fresh ChatGPT session works one packet, submits PRs and proof, then stops or responds to review. You ensure accepted task PRs are reviewed and land in the plan branch, reconcile `tasks.md` through a reviewed progress PR on astrid-dev `main`, and oversee later release integration under the normal permissions.
4. **Prepare the mailbox.** Reuse the release's existing coordination issue, or create one `coordination: Release <N> Lead / Orchestrator` linked from `run.md`. It is for short attributed STATUS / REQUEST / DECISION / BLOCKED / ACK comments following the [existing mailbox protocol](../../astrid-dev-orchestrate/codex-cloud/README.md#establish-the-mailbox), **not** packet issues or source-of-truth task statuses. No `plan:NN`, `release:NN` or `planned` labels.
5. **Hand off to the owner.** Provide queue and mailbox links, ready/blocked packets, any missing authorization and the [Orchestrator launch message](#launch-message). Verify available GitHub access and whether session creation, hourly scheduling and resumption actually work; describe any manual steps. The Orchestrator verifies two-way mailbox communication at startup.

## At each Lead check-in

Read the Orchestrator's compact hourly report and requests. Review submitted packet PRs and proof; post a DECISION accepting the packet or naming concrete rework. Ensure accepted work is landed through authorized review/merge and that the plan's `tasks.md` is reconciled by its normal reviewed PR route. Prepare the next packets and resolve dependencies. The Orchestrator updates the queue's handoff status; the Lead owns engineering acceptance and release integration.

## Launch message

```text
You are the Codex Orchestrator for Release <N>, reporting to Lead <session>.
Follow astrid-dev-orchestrate and workstreams/multi-manager-dispatch.md.
Read releases/<N>/run.md at <SHA>; Ready rows link packet Markdown briefs.
Mailbox: <issue URL>. Create a FRESH ChatGPT session for each packet, following
its Manage packet workstream. Never retain one manager across packets.
Check every open packet hourly, read the mailbox, unblock or escalate stalls,
and post one compact hourly STATUS covering all packets. Send submitted PRs
and proof to the Lead for review; the Lead handles plan-level acceptance,
integration and tasks.md reconciliation. You may <authorized actions>.
Escalate <reserved actions>. Verify scheduling and session creation/resume;
if unavailable, identify the manual nudges instead of promising automation.
```
