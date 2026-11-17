# Workstream: dispatch ChatGPT managers

Use when a [Release Lead](../../astrid-dev-lead/SKILL.md) has prepared the [multi-manager queue](../../astrid-dev-lead/workstreams/multi-manager-release.md) and the owner has authorized this session. Follow the [Orchestrate role](../SKILL.md); this adds only dispatch mechanics.

**Your job:** keep execution moving. The Lead owns scope, review and release decisions; each plan has **one accountable manager** for implementation and integration.

## Start

1. Read the release `run.md`, linked packet briefs, source `tasks.md`, permissions and mailbox. Confirm who is accountable for each plan. Test an attributable message and acknowledgment with the Lead using the [mailbox protocol](../codex-cloud/README.md#establish-the-mailbox).
2. Give Ready packets to the existing authorized manager sessions when possible, linking each brief and [Manage](../../astrid-dev-manage/SKILL.md). If using a separate packet chat, it works for the plan's accountable manager; it does not start another plan run. Verify that session creation/resume is supported rather than assuming GitHub access provides it.
3. **You own dispatch-state changes** in the `run.md` queue after setup. Record session links and state; reread the current file before writing. The mailbox carries short messages and evidence links, not a second queue.

## Each check-in (hourly when possible)

1. Read and acknowledge new mailbox requests. Compare each Running/Blocked packet with its last evidence.
2. Nudge stalled work with **one concrete next action**, or resume/recover the session through a proven mechanism. If an impediment needs engineering or cross-plan judgment, send evidence and one question to the Lead. Do not restart duplicate sessions blindly.
3. Mark submitted work **Review** and ask the Lead to accept or return it. Move to **Done** only after the Lead accepts and the plan manager reconciles `tasks.md`. Dispatch the next Ready packet.
4. Leave a short attributable mailbox message **only on a change, blocker or request**. Otherwise keep moving without ceremony.

GitHub comments don't wake stopped chats. If hourly scheduling or session resume cannot be verified, state the manual intervention needed; never claim unattended operation.
