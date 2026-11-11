# Aggregate census timing, 11 November 2026

Under an orchestrator-granted exclusive 30-second host window, a one-shot read-only probe started at 09:31:22 UTC and completed by 09:31:39 UTC with exit 0. It ran the R10 checkout's `ps -axo pid=,ppid=,pgid=,lstart=` followed by its `_parse_census`, retaining process rows in memory only. Output: `ps_seconds=0.271655 parse_seconds=0.660897 live_entries=25 exited_entries=8782`. The post-probe cgroup reported `cpu.max` `400000 100000`, `pids.current` 8890 and `pids.max` `max`.

The combined measured work was approximately 0.933 seconds, close to the relevant one-second readiness wait. This single probe does not include the observer thread's scheduling or lock wait, cannot establish the process population during earlier failures, and does not prove their cause. No processes were changed or raw process rows recorded. The host window was released immediately. See the [proposal](continuation-proposal.md) for the method and limits.
