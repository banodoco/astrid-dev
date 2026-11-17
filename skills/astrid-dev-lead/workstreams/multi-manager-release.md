# Workstream: multi-manager release dispatch

Use when a Lead directs an Orchestrator that hands bounded work from accepted plans to ChatGPT manager sessions. **Everything in the [Lead skill](../SKILL.md) still applies.** This guide covers only the extra setup and handoffs.

## Set up

1. **Prepare packets.** Read `releases/<N>.md` and each included plan's `tasks.md`. Group compatible, ready task IDs from **one plan** into assignments of roughly **three human engineering days maximum**. Create concise briefs at `releases/<N>/packets/<id>.md` using [the packet template](../../../templates/release/packet.md). Point to canonical tasks, proof, dependencies, branch and accountable plan manager; don't copy task checklists or invent a new project. If a task needs splitting or lacks acceptance/proof, correct its original task card through the normal review path first.
2. **Prepare the queue.** Add packet links to the existing `releases/<N>/run.md` (create from its template if missing). The queue has **Ready / Running / Review / Blocked / Done**, session and next-action/evidence links. The plan's `tasks.md` alone records engineering completion. The Lead prepares packets and decides acceptance; **after handoff the Orchestrator maintains dispatch state in the queue**. For other release-wide `run.md` edits, reread the latest version and avoid competing changes.
3. **Keep one accountable plan manager.** Reuse an existing manager session where possible. The manager integrates that plan's PRs and keeps its `tasks.md` current. A separate packet chat, if needed for parallelism, is a bounded delegate, **not a second owner of the plan run**. Never start a session without the required owner authorization.
4. **Set up one mailbox, if needed.** Search for the release's existing coordination issue; reuse it if present. Otherwise create one issue titled `coordination: Release <N> Lead / Orchestrator`, with a short body identifying it as **coordination only**, linking `run.md`, naming roles/sessions and pointing to the [existing mailbox protocol](../../astrid-dev-orchestrate/codex-cloud/README.md#establish-the-mailbox). Link it from the queue. Do **not** open an issue per packet or add `plan:NN`, `release:NN` or `planned` labels: ordinary issues remain for product reports and ideas. Messages identify sender, recipient, session, ID, action and evidence; acknowledgements are comments, not edits.
5. **Hand off to the owner.** Check that links and issue read/write access work. Give the owner the queue, mailbox, ready/blocked packet links, any missing authorizations and the exact [Orchestrator launch prompt](#launch-prompt). State whether hourly scheduling **and session resume** are verified; if not, say who must manually nudge sessions. The Orchestrator tests two-way mailbox delivery at startup; the Lead cannot claim that test passed before it launches.

## Each Lead check-in (hourly when scheduled)

Read requests and submissions. Review PRs, proof and independent findings; post **ACCEPT** or a concrete rework request to the mailbox. Reconcile actual work with the plan manager's `tasks.md`, resolve dependencies, prepare next packets and monitor release integration. The Orchestrator updates packet handoff states; the Lead owns acceptance and release decisions. Put substantive rulings in the release's existing decision record, not a new log.

## Launch prompt

```text
You are the Codex Orchestrator for Release <N>, supervised by Lead <session>.
Follow astrid-dev-orchestrate and its multi-manager dispatch workstream.
Start at releases/<N>.md and releases/<N>/run.md at <SHA>.
Ready rows link packet briefs in releases/<N>/packets/; mailbox: <issue URL>.
Reuse accountable plan managers; dispatch authorized packets and supervise sessions.
Maintain dispatch states, send completed work to Lead for acceptance, unblock stalls
and escalate technical/cross-plan choices. Check hourly only with a proven scheduler
and resume mechanism; otherwise report the manual nudge required.
You may <authorized actions>; ask the owner for <reserved decisions>.
First verify two-way mailbox communication; do not publish or accept Lead reviews.
```
