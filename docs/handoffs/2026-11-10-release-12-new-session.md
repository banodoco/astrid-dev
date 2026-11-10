# Release 12 — new session takeover

This is a transition snapshot, not a new release plan or evidence that a gate passed. Read [Release 12](../../releases/12.md), then [Fixes](../../releases/12/fixes.md) and [Generation](../../releases/12/generation.md). They govern the release; the older pause and orchestrator snapshots contain historical facts and may describe superseded status. Fetch current refs and read [Track A's handoff](2026-11-10-track-a-codex-resume.md) and [Track B's handoff](2026-11-10-release12-track-b-resume.md) before acting.

## Role and working style

Act as the orchestrator for both tracks, with a manager for Track A (fixes/P29) and a manager for Track B (generation/P32, P40, P20, P34). On startup obtain their transition briefs, check for existing live owners before starting successors, and give each manager its track document and transition handoff. Managers delegate independent work, maintain task records, and escalate blockers or consequential decisions. Route ordinary tasks to Luna, harder tasks to Terra, very hard tasks to Sol, and seek Astra for a hard or ambiguous blocker or high-stakes decision. Use the models actually available in the new session and explain any constraint.

The owner requests an hourly progress and blocker check with an update, plus a deeper strategic Astra review every two hours. Read [astrid-dev-orchestrate](../../skills/astrid-dev-orchestrate/SKILL.md) and [astrid-dev-manage](../../skills/astrid-dev-manage/SKILL.md). If skills do not appear in the catalog, read the checked-out SKILL.md files directly and install missing links without overwriting existing skills.

## Check-ins and communication

The Check-in Companion skill was visible in the old chat, but that chat did not expose its host scheduling tool. A prior one-time test was reported delivered while its original chat was active; that does not prove an idle chat can resume. The later requested two-minute test was never scheduled. The local Agent Checkpoint prototype has no scheduler and must not be represented as working.

In the new session, discover the actual scheduler; use Check-in Companion if it and the required scheduling tool are available. Create a short one-time same-chat test, end the turn and verify actual delivery before claiming wake-up or setting recurring work. Then configure the requested hourly check-in with a two-hour Astra review if supported, and report exactly what was created. If unavailable, say so and use manual nudges; do not claim an issue comment or a background process wakes the session.

For separate chats use [the Codex Cloud coordination guide](../../skills/astrid-dev-orchestrate/codex-cloud/README.md) and the existing [Release 12 coordination issue #368](https://github.com/banodoco/astrid-dev/issues/368). Register unique session IDs, read prior comments and establish acknowledgment in both directions; comments are a mailbox, not a proven wake mechanism. Existing registration challenges and the old pause document are historical, not proof that new chats are running. Do not send external messages without the owner's authorization beyond the requested project coordination.

## Release safeguards

Follow the current release pages for CI restrictions, exact frozen SHAs, handoffs, review and publication gates. No gate is complete merely because work was committed or a focused test passed. Reconcile the historical $3.13 spend, current provider state and the approved $25 cap before any paid work; check for existing pods and take the required census. P34 must supervise and release paid resources independently of check-ins. No unreviewed GPU work, duplicate live runs, force pushes or secret disclosure. Confirm the current owner approvals and exact plan before irreversible release actions.

## Takeover sequence

1. Fetch the transition branch containing this file, both manager handoffs and their referenced WIP refs. Confirm each full SHA on the remote; local worktrees, processes, logs and virtualenvs may not exist on the new machine.
2. Verify which previous workers and tests actually stopped, and any CI still running. Treat interrupted tests as interrupted. If a needed artifact was not transferred, reconstruct or rerun the required proof under the plan's restrictions.
3. Resume the two tracks from their manager handoffs, delegate ready work and keep the plans' progress records current. Relay cross-track dependencies and obtain Astra advice when needed.
4. Set up the check-in mechanism as above and tell the owner the actual status. Do not infer delivery from schedule creation alone.

## Starter messages

Copy the three concise messages from [the session startup messages](2026-11-10-release12-start-messages.md). The orchestrator message is also reproduced here.

> Take over Release 12 as orchestrator. Read this handoff, the release overview and both track pages, then the two transition handoffs. Check for live existing owners and reconstruct the exact pushed work. Run one manager per track, delegate work, unblock and escalate hard or high-stakes questions to Astra. Use Check-in Companion if this session has a real scheduler: test same-chat delivery first, then arrange hourly updates and a deeper Astra review every two hours. Follow the release gates and paid-work limits; report any missing access or unverified wake-up.
