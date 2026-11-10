# Release 12 — messages to start the new sessions

Start the two managers as subagents in the orchestrator’s Codex Cloud session. The handoffs and current progress records are on `astrid-dev` main. Read the linked handoffs and release plan for details, exact SHAs, dependencies and limits.

## Orchestrator

> Take over Release 12 as orchestrator. Read [`2026-11-10-release-12-new-session.md`](2026-11-10-release-12-new-session.md), the linked release plan and both manager handoffs. Start one manager subagent per track and use native collaboration messages. Keep them moving, unblock them and consult Astra on hard blockers or consequential decisions. Once they are running, use Check-in Companion to schedule an hourly check-in and update me. Count check-ins; at every third (3, 6, 9, …), ask an Astra subagent with Luna helpers to review progress and opportunities to work faster. Verify the scheduler can resume this chat before relying on it; tell me if unavailable. Then end your turn and wait for the check-in. Follow the release gates and spend limits.

## Track A — fixes and UI

> You are the Release 12 Track A manager. Read [`2026-11-10-track-a-codex-resume.md`](2026-11-10-track-a-codex-resume.md), [`releases/12.md`](../../releases/12.md) and [`releases/12/fixes.md`](../../releases/12/fixes.md); use `astrid-dev-manage`. Reconstruct and verify the pushed refs, then delegate and drive the fixes and UI work through the recorded tasks and gates. Keep task records current, check your work hourly, and escalate blockers or consequential decisions to the orchestrator via collaboration messages. Treat interrupted or unreviewed work as unfinished.

## Track B — generation

> You are the Release 12 Track B manager. Read [`2026-11-10-release12-track-b-resume.md`](2026-11-10-release12-track-b-resume.md), [`releases/12.md`](../../releases/12.md) and [`releases/12/generation.md`](../../releases/12/generation.md); use `astrid-dev-manage`. Reconstruct and verify the pushed refs, then delegate and drive the generation tasks through their recorded dependencies and gates. Keep task records current, check your work hourly, and escalate blockers or consequential decisions to the orchestrator via collaboration messages. T9 is unfinished; follow the release's GPU approval, census and spend rules.

If skills aren't in the catalog, read their checked-out `SKILL.md` files directly. Verify subagent capacity and whether managers can delegate; adjust parallelism to the actual available slots.
