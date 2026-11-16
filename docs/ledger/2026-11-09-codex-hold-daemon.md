Date: 2026-11-09
Kind: fix
Source: Plan 38 Codex manager trial (orchestrator session)
Resolved by: —

codex-hold.sh dies with the container on a worker restart, so a dead Codex runner waited for the next scheduled check-in to come back. codex-in-cloud now adds codex-hold-daemon.sh. A SessionStart hook in the user settings relaunches it every time the session resumes, and a flock keeps one copy running. It restarts the dead runner of each run in ~/codex/runs.txt within 30 seconds, at most three times. The README sets out the three layers: in-turn hold, daemon and scheduled check-in. It also notes that auto mode refuses Claude's own settings edits, so the owner adds the hook. Separately, the manage skill now says a shallow clone, not a history rewrite, is the usual cause of a "refusing to merge unrelated histories" error. Follows: 2026-11-09-codex-keepalive
