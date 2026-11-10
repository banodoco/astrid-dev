# Release 12 — messages to start the new sessions

These messages are for separate Codex Cloud sessions. The handoffs are in PR #377 on branch `handoff/release12-session-transition` until merged; fetch that branch if they are not yet on `main`. Read the linked handoffs and current release plan for details, exact SHAs, dependencies and limits.

## Orchestrator

> Take over Release 12 as orchestrator. Read [`2026-11-10-release-12-new-session.md`](2026-11-10-release-12-new-session.md), the linked release plan and both manager handoffs. Coordinate the two managers through [issue #368](https://github.com/banodoco/astrid-dev/issues/368), unblock them and ask Astra about hard blockers or consequential decisions. Check in and update me hourly; get a deeper Astra review every two hours. Use Check-in Companion if its actual scheduler is available here: test same-chat delivery before relying on recurring check-ins. Tell me if it isn't available. Follow the release gates and spend limits.

## Track A — fixes and UI

> You are the Release 12 Track A manager. Read [`2026-11-10-track-a-codex-resume.md`](2026-11-10-track-a-codex-resume.md), [`releases/12.md`](../../releases/12.md) and [`releases/12/fixes.md`](../../releases/12/fixes.md); use `astrid-dev-manage`. Reconstruct and verify the pushed refs, then delegate and drive the fixes and UI work through the recorded tasks and gates. Keep task records current, check your work hourly, and escalate blockers or consequential decisions to the orchestrator via [issue #368](https://github.com/banodoco/astrid-dev/issues/368). Treat interrupted or unreviewed work as unfinished.

## Track B — generation

> You are the Release 12 Track B manager. Read [`2026-11-10-release12-track-b-resume.md`](2026-11-10-release12-track-b-resume.md), [`releases/12.md`](../../releases/12.md) and [`releases/12/generation.md`](../../releases/12/generation.md); use `astrid-dev-manage`. Reconstruct and verify the pushed refs, then delegate and drive the generation tasks through their recorded dependencies and gates. Keep task records current, check your work hourly, and escalate blockers or consequential decisions to the orchestrator via [issue #368](https://github.com/banodoco/astrid-dev/issues/368). T9 is unfinished; follow the release's GPU approval, census and spend rules.

Each session should read the [Codex Cloud coordination guide](../../skills/astrid-dev-orchestrate/codex-cloud/README.md), register a unique session ID and acknowledge messages. Issue comments do not by themselves wake an idle chat. If skills aren't in the catalog, read their checked-out `SKILL.md` files directly.
