Date: 2026-11-28
Kind: idea
Source: H3 Plan 66 hosted manager startup
Resolved by: —

The hosted manager can prepare its worktree and environment while the orchestrator's baseline CI runs, but the handoff depends on a separate mailbox notice after the CI result and board record. Consider exposing the baseline gate and its exact commit in the runner's durable state so a resumed manager can identify the prerequisite without reconstructing it from several surfaces.
