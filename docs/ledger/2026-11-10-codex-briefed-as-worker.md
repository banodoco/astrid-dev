Date: 2026-11-10
Kind: fix
Source: Plan 32 orchestrator, 9 Nov night
Resolved by: —

The orchestrator briefed a Codex run for Plan 32's review must-fixes from its own worker-style prompt ("never push to int/32 or main"), not from `manager-brief.md`. It then told the run by mailbox to manage and integrate. Codex correctly refused, because its authority comes from its starting prompt, so the orchestrator spent the night relaying branches between Codex and a Claude manager and steering each fix. The codex-in-cloud README's Oversight section ("read the fixes, check it's heading the right way") encouraged that. Fix: the orchestrate skill and the README now say to brief every Codex manager from `manager-brief.md`, to change a running Codex's role only by a checkpoint and a fresh manager run, and that the orchestrator stays the advisor.
