Date: 2026-11-10
Kind: papercut
Source: Orchestrator handoff of Plans 20, 32, 34 and 40 to another machine
Resolved by: [2026-11-10 orchestrator handoff](../handoffs/2026-11-10-orchestrator.md) and each plan's `handoff.md` (manual)

Moving four live Codex managers to another machine showed that a run's recovery state lives only on the machine that ran it. `.otto/runs/` is gitignored, worktrees hold commits that are on no remote, and the owner's rules from the conversation exist only in the session.

The CI freeze made this worse: integration heads couldn't be pushed to `int/**`, so the work had to go to non-int share branches. The handoff was assembled by hand. Each manager pushed its commits and wrote `plans/<plan>/handoff.md`, and the orchestrator wrote a top-level handoff.

The manage skill should define this as a routine step, a "handoff-ready" checkpoint:
- every commit reachable from a remote (`git log --branches --not --remotes` is empty);
- the recovery state from the run contract copied into a tracked `handoff.md`;
- `tasks.md` progress cells carrying exact pushed SHAs.

The orchestrate skill should keep a running owner-rules file, not rely on scheduled check-in prompts to carry them.
