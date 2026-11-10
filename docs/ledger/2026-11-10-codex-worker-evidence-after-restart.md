Date: 2026-11-10
Kind: issue
Source: Plan 32 Codex manager, repeated container restarts
Resolved by: —

Subagent messages and active test sessions disappeared on restart, while committed worktrees survived; a reported passing result could not always be recovered with its exact command and log. Have the runner persist each worker's exact candidate, command, inner exit and log path in the run directory before reporting it, and mark interrupted checks as no result on resume. This would preserve evidence without rerunning long CPU journeys or trusting an incomplete transcript.
