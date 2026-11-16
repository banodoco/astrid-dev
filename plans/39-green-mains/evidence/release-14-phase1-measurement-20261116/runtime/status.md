# Runtime G2 initial evidence snapshot

- Repository: `banodoco/astrid-runtime`
- Exact head SHA: `4fe2c0b847cf83771b2f3ce4e4fba0934f64f6ce`
- Tree: `3fff009d7cb8c46a1a1df21f3f541596b98480bd`
- Branch: `release/14/plan-39`
- Attempt: 1 for both exact-head runs.
- Captured: 2026-11-16 19:28:52 UTC
- Sources: [CI](https://github.com/banodoco/astrid-runtime/actions/runs/43938386357) (run 43938386357) and [Nightly](https://github.com/banodoco/astrid-runtime/actions/runs/43938386391) (run 43938386391); full API source URLs are recorded in the snapshot JSON.
- CI job 133548963269 `darwin-native`: completed success.
- CI jobs: 133548963680 `sandbox-process-control`, 133548963714 `portability-lifecycle (ubuntu-latest)`, 133548963731 `unit (ubuntu-latest)`, 133548963772 `typescript-client`, 133548963837 `portability-lifecycle (macos-latest)`, 133548963918 `boundary`, and 133548963937 `unit (macos-latest)`: queued.
- Job 133548964030 `windows-realm-publication`: queued.
- Job 133548965036 `landing reference`: skipped.
- Nightly job 133548961758 `integration`: queued.
- The run's current API state is in [initial-snapshot.json](../initial-snapshot.json) and [snapshot-20261116T1928Z.json](../snapshot-20261116T1928Z.json).

No failing completed jobs or downloadable job logs existed in these snapshots, so no failure totals, literal failure messages, or test-row ownership are asserted here. The run contract binds N to `gpt-6-luna`, high reasoning effort. The worker did not run local tests, edit source, dispatch/cancel/re-run workflows, or mutate GitHub.

The applicable ownership inventories are Plan 38's [test inventory](https://github.com/banodoco/astrid-dev/blob/2770aa79e8d9325c7891294609c746963cc4776e/plans/38-one-process-identity/tasks.md) and Plan 55's Runtime test-inventory statement in [tasks](https://github.com/banodoco/astrid-dev/blob/2770aa79e8d9325c7891294609c746963cc4776e/plans/55-local-speed/tasks.md). Exact WAITING memberships must be assigned only after matching completed-job node IDs to those inventories and existing G1 R-triage rows. Plan 38's listed Runtime inventory families include native-boundary tests, stale-owner bootstrap tests, local-composition host-only/legacy-worker tests, real-bootstrap identity cases, and selected Windows shutdown-owner behavior. Plan 55 names Runtime task-lifecycle and publication tests, but ownership is test-specific; broad lane names are not sufficient evidence.

