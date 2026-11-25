---
description: Measure installed Astrid workflows in a separate session with reproducible fixtures and durable timing evidence.
---

# Run a timing in a separate session

Use a measurement session when a representative fixture takes long enough to compete with managers or test workers, or when browser, App and Runtime timings need quiet cores. A separate workspace on the same constrained machine still shares its CPU. Keep one active stack in the measurement session and put the result receipts in a durable directory. Follow the [hosting workstream](../../roles/orchestrator/codex-in-claude-cloud.md) for the manager's check-ins and restart supervision.

## Prepare one reusable fixture

1. Record the exact revisions, generated pins, installer route and workload the run will measure. For editor opening, record whether the browser serves source modules or a compiled bundle. Use the route a user actually takes for a user-facing timing claim.
2. Check `df -h` on the fixture's filesystem before every build and measurement. Use the plan's start and stop floors. Where the run calls for 20 GiB to start a seed and 15 GiB as the stop floor, reserve space for the installed stack, the backup and one disposable restore at the same time. Apply any higher floor the plan sets for a measured arm.
3. Seed the representative sandbox once, through the product interface, and record its exact selection and head. Stop the owned stack and make one authenticated backup. Verify a restore against the backup's realm ID and database digest. Keep the backup and its support directory in the same session at their original locations. The product handles authentication material. Schedule future restores in that session so verification custody stays intact.
4. If the stock backup admission deadline interrupts verification, keep the original failure and use a longer supported budget only for setup. Preserve the owner fence and every validation step. Record both deadlines and the final verified restore. Allow for setup time before promising a measurement window.

## Measure and recover

- Start the exact installed stack from the disposable restore. Wait until the owned instance and realm are visible in health, allow startup verification to settle, then start the App and confirm its authenticated proxy identifies that same Runtime. Record any setup deadline or retry separately from the measurement. Collect startup-to-ready only when the recorder observes start and readiness on the same clock.
- Use a fresh headless Chrome profile per run. Give Chrome a private short temporary directory such as one created with `mktemp -d /tmp/astrid-browser.XXXXXX`. A deep stack path can exceed the Linux singleton socket length before Chrome opens a page. Stop the browser, dispose of its profile and temporary directory, and stop the owned stack after the evidence is safe.
- Run one timed arm at a time. Pause fixture builds, installs and test workers during each arm. Keep the exact trace, exit status, revisions, verified restore receipt, disk observations, product outcomes and cleanup. Keep CPU and elapsed-time clocks separate and state the events that bound each interval.
- After a container restart, check the durable phase receipts, active ownership, ports, operation locks, disk and any browser profiles before resuming. Keep the last verified artifact and repeat only an unfinished setup step through normal product recovery. When a gesture may have occurred, verify its authoritative result before any replacement run. Mark an interrupted observation in the record.
