Date: 2026-11-12
Kind: fix
Source: Owner, at the start of Plan 48's Phase 2 run
Resolved by: —

Asked to manage Phase 2 with Codex doing the bulk of the work, the manager session started a Codex manager process and waited on it, when the owner meant for it to manage and send each card to Codex. Three things told it to. The orchestrate skill's only Codex section, the run contract's table and the manage skill's Codex rules all described a Codex manager; the simpler shape, one `codex exec` per card under a Claude manager, existed only as a later section of the runner's README. The plan's dispatch notes were written for a Codex manager. And the orchestrator's own start message said "run the Codex manager".

Now the orchestrate skill, the README, the run contract and the manage skill present Codex workers under a Claude manager as the default, and a Codex manager as a choice that needs a reason on the plan's Run start line: one long self-directed job, more tracks than the session can supervise, or the owner asking. The Codex manager brief says it is not the default. Plan 48's dispatch notes are corrected.

Follows: 2026-11-11-nobody-answered-for-the-run
