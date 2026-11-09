Date: 2026-11-09
Kind: fix
Source: Plan 38 Codex manager trial (orchestrator session)
Resolved by: —

The first Codex manager run was killed by a Claude worker restart, which kills every process in the container. Nothing restarted it, because codex-in-cloud had no keep-alive; the retired merge kit's hold.sh had done that job. codex-in-cloud now has codex-hold.sh. It keeps the session busy, restarts a dead runner (up to three times), and wakes the orchestrator on mailbox messages or a finished run. The runner now saves its arguments, resumes the same Codex session after a restart, skips the git-repo check, and takes CODEX_EFFORT and CODEX_MAX_THREADS. The README gains the Codex skills install, the shared-filesystem and worktree rule, no nested codex exec, the proxy notes and one branch per PR. The orchestrate skill now requires every check-in to re-arm the keep-alive. The manage skill's baseline is now scoped (plan inventory and focused proofs locally, the full suite only on CI) and has a "Managing under Codex" rule. The plan skill asks for a test inventory and per-task proof files. Follows: 2026-11-09-codex-manager-trial
