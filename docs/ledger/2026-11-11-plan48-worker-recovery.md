Date: 2026-11-11
Kind: papercut
Source: Plan 48 Phase 1 shared-filesystem run
Resolved by: —

The run recovered across two container restarts from the mailbox, run record, task table and preserved diff, while worker handles disappeared. Have the runner save each worker's latest handoff beside the run record so recovery starts with the remaining work. The named smoke also needed `PYTHONPATH=scripts` and dirtied tracked bytecode; give astrid-dev's standard-library projects an explicit smoke recipe with `PYTHONDONTWRITEBYTECODE=1`. State frozen-oracle wiring and duplicate-diagnostic rules in task cards before dispatch.
