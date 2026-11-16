Date: 2026-11-09
Kind: papercut
Source: Plan 38 Codex manager trial
Resolved by: —

Codex subagents and the manager share a filesystem; concurrent setup in one checkout collided on a Git lock, so briefs need a unique worktree and sibling environment path. The manager skill assumes Claude-specific one-repository sessions, permission allowlists and session tools that Codex does not expose; document the corresponding Codex workflow and agent lifecycle, including how to release finished thread slots. The baseline-before-work rule needs an explicit bootstrap exception when W0 supplies the baseline runner and a scoped local-versus-hosted baseline policy. The GitHub proxy appended an unrelated Claude Code attribution to a REST-created PR body; preserve the submitted body or identify its source accurately. The available smoke modes cover product repositories, not astrid-dev itself. The shared mailbox, parallel scoped workers, add-only branches and local documentation check worked.
