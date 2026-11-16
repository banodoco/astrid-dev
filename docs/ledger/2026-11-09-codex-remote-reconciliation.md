Date: 2026-11-09
Kind: idea
Source: Plan 38 Codex manager second restart
Resolved by: —

The mailbox, run record and worktrees again allowed recovery after a container restart. The mailbox still described progress and ledger pull requests as open after they had merged, so recovery required separate GitHub queries and a check of main. A runner that reconciles recorded pull requests against their remote state at restart would make the durable status quicker to trust.
