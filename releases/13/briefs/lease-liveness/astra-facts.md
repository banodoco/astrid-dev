codex
**Evidenced:** The pack host declared the task failed while its execution path continued communicating with the pod. Release entered that same host’s single-worker queue. **Inferred:** The immediate failure was loss of *acknowledged Runtime authority*, not demonstrated failure of the paid workload.

References: **A**=`/home/user/wt/dive-ran`, **K**=`/home/user/wt/dive-k1`, **R**=`/home/user/wt/rt-42ae`; **H**=`A/astrid/core/execution/generic_host.py`. Database citations identify tables/rows because SQLite has no meaningful line numbers. All timestamps below are UTC on 13 November. Investigation was offline/read-only; three Luna/low agents extracted evidence; tests were inspected, not run.

**(a) Read → `lease_lost`**

**Evidenced:** The read originates in the **pack host**, through `RuntimeProtocolClient.task()`. The generated Runtime HTTP client raises `ApiError(status=0, code="transport_timeout")`; the host converts the observation into a lifecycle decision. The CLI subsequently displays the failed task. This is not a pod-to-provider timeout. The installed host/client files match the supplied source copies. [H:5574](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:5574), [generated.py:687](/home/user/wt/rt-42ae/packages/python/astrid_runtime_client/generated.py:687)

**Evidenced:** `astrid-pack-host` holds the attempt lease: attempt `7c133306…`, fence `1`, Runtime epoch `2`. Runtime grants **30 seconds**. The daemon thread `astrid-heartbeat-{task_id}` checks lifecycle state every **50 ms**, performs task reads approximately every **5 seconds**, then renews after successful reads. Progress changes also trigger renewal. Lifecycle HTTP calls have a **2-second timeout**, shortened by remaining validity; heartbeat-lock acquisition is also bounded by two seconds. There are **zero immediate transport retries**; eligible failures retry through subsequent loop iterations. [H:5484](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:5484), [H:11556](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11556), [H:11821](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11821), [store.py:6252](/home/user/wt/rt-42ae/runtime_protocol/store.py:6252)

**Evidenced:** **One transport timeout is not automatically fatal.** `lease_transport_fault()` tolerates it while acknowledged validity and the execution lifetime permit. Failed reads skip renewal. When acknowledged validity ends, the observer preserves the last transport diagnostic and calls `force_abort("lease_lost")`. That sets the cancellation event and sends non-retryable `attempt.fail`. [H:11439](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11439), [H:11520](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11520)

**Evidenced:** `observed_at=00:30:25.787587` timestamps the diagnostic, **not terminalization**. Failure committed at **00:30:31.610**, after the diagnostic’s acknowledged expiry **00:30:28.692**, but before the database’s newer expiry **00:30:33.723**. Runtime committed another heartbeat at **00:30:03.723**; the diagnostic’s last acknowledged heartbeat remains **00:29:58.694537**. [H:11372](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11372); DB `attempts[7c133306…]`, corresponding `command_idempotency[attempt.heartbeat/attempt.fail]`, `events[51]`.

**Inferred:** The later heartbeat committed without its acknowledgement becoming accepted host state. Subsequent observation failures exhausted the older acknowledged lease. Exact abort time, number of failed reads, and why acknowledgement failed are not recorded; “declared lost three seconds before expiry” is therefore misleading.

**Evidenced:** Abort is cooperative. `run_on_machine()` checks cancellation between operations, calls exact-job cancellation, and finally invokes release/retention settlement. `machine.start()` performs shipping and launch without receiving that callback. Detached jobs survive their client. Consequently, marking Runtime failed neither immediately stops remote work nor terminates billing; verified failures may retain an idle machine. Actual cancellation/termination of this edit is unproved. [machine_run.py:97](/home/user/wt/dive-ran/astrid/core/execution/machine_run.py:97), [machine.py:722](/home/user/wt/dive-ran/astrid/packs/runpod/machine.py:722), [machine.py:1052](/home/user/wt/dive-ran/astrid/packs/runpod/machine.py:1052)

**Evidenced:** The lease protects mutation/publication authority and execution custody using lease identity, attempt, fence and epoch. Ordinary expiry retains blockers because expiry is not stop evidence. It does not physically fence a pod process. A late successful result for this already-failed attempt is rejected; expired authority also cannot publish. [store.py:4093](/home/user/wt/rt-42ae/runtime_protocol/store.py:4093), [store.py:6133](/home/user/wt/rt-42ae/runtime_protocol/store.py:6133)

**(b) Timeline and release queue**

**Evidenced — database reconstruction:** Sources are `tasks`, `runs`, `attempts`, `reservations`, `events`, `executors`, `capabilities`, and heartbeat idempotency records in `D/flat/realm.sqlite3`.

| UTC | Recorded fact |
|---|---|
| 00:21:09.672 | Claim `b5599d43…` admitted. |
| 00:21:09.995–00:23:56.906 | Claim attempt `c841a9c4…`, fence 1, CPU reservation; completed, event 48. Result names pod `6foeue5emvt370`, idle/live. |
| 00:25:56.875 | Edit `23949ab4…` admitted, event 49. |
| 00:25:57.030–.031 | GPU reservation created; attempt `7c133306…` claimed, fence 1, event 50. |
| 00:29:58.692 | Heartbeat extends expiry to 00:30:28.692. |
| 00:30:03.723 | Last committed heartbeat extends expiry to 00:30:33.723; executor `last_seen_at` matches. |
| 00:30:25.787587 | Last saved transport diagnostic observed. |
| 00:30:31.609–.610 | Edit/run failed; attempt settled; GPU reservation released; event 51. |
| 00:30:37.656–.657 | Release `8b22cc05…` admitted, event 52; remains queued, with **no attempt or reservation**. |

**Evidenced:** Release is an ordinary `runpod.release` task submitted by `_runpod_operation()`. Both release and claim require CPU; generation requires GPU. All use executor `astrid-pack-host`, whose recorded `max_concurrency=1`. Its single-slot loop synchronously executes `claim_once()` before claiming again. [generation.py:361](/home/user/wt/dive-ran/astrid/sdk/generation.py:361), [H:13718](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:13718), [H:13997](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:13997)

**Inferred:** Release waited behind the still-unwinding edit invocation, not its GPU reservation: that reservation was already released. Continued uploads support this. The host knew about failure—it issued it—but its synchronous execution/session lock remained occupied until return. No stack capture establishes the precise blocking operation. [H:11845](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11845), [host log:1534](/tmp/claude-0/-home-user/ebe1c0ff-e4f9-56ce-9569-8dc5a5d6e26c/scratchpad/lease-dive/data/service-pack-host.log:1534)

**Evidenced:** K1 bounds successful checkpoint verification outside the owner lock, rechecks custody, retains refusal reasons, and improves observer reaping. It leaves the host claim loop and release task route unchanged. **Inferred:** K1 would not prevent this queueing mechanism; it improves later cleanup/checkpoint contention. [K/machine.py:1050](/home/user/wt/dive-k1/astrid/packs/runpod/machine.py:1050), [K/worker_owner.py:781](/home/user/wt/dive-k1/astrid/packs/runpod/worker_owner.py:781)

**(c) Why logs are silent**

**Evidenced:** The lease decision updates a diagnostic object, publishes failure, and writes the attempt receipt; those functions do not print a lease-loss log. Runtime explicitly suppresses HTTP access logging. `runtime.log` is a launch/status dump; `runtime-service.log` is empty. [H:11372](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11372), [H:11520](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11520), [server.py:194](/home/user/wt/rt-42ae/runtime_protocol/server.py:194)

**Evidenced:** Host logs contain:

- **00:29:30 onward:** successful upload chunks.
- **00:30:33.480:** upload HTTP 409 and an explicit upload-failure warning, followed by resumed uploads.
- **00:32:02.443:** job POST accepted; subsequent downloads alternate 200/400/200 through the requested window.
- **00:34:50 onward:** route 404 retries, just outside that window.

These are pod HTTP observations, not proof of successful image computation. [log:1503](/tmp/claude-0/-home-user/ebe1c0ff-e4f9-56ce-9569-8dc5a5d6e26c/scratchpad/lease-dive/data/service-pack-host.log:1503), [log:1534](/tmp/claude-0/-home-user/ebe1c0ff-e4f9-56ce-9569-8dc5a5d6e26c/scratchpad/lease-dive/data/service-pack-host.log:1534), [log:1626](/tmp/claude-0/-home-user/ebe1c0ff-e4f9-56ce-9569-8dc5a5d6e26c/scratchpad/lease-dive/data/service-pack-host.log:1626)

**(d) Liveness/custody inventory**

**Evidenced — every row below.** “Once” describes the declaration, not a unified system-wide policy. **P** denotes installed `py/lib/python3.11/site-packages/runpod_lifecycle/https.py`.

| Decision point / file:line | Timeout/interval; declaration | Failure action; reason visibility |
|---|---|---|
| CLI follow: `A/astrid/sdk/invocation.py:3425,3633` | Poll 1s; print 60s; wait 3600s, repeated defaults; capacity policy can remove deadline | Read error returns `task_status_unavailable`; wait timeout returns error, not cancellation |
| Ctrl-C: `invocation.py:3385` | One cancellation request | Requests Runtime cancellation; adds note if unconfirmed |
| Host lifecycle: `H:498,5484,11556` | 5s poll; 50ms guard; 2s HTTP/lock literals | Retry within acknowledged validity, then abort; diagnostic/DB, no direct log |
| Host registration: `H:1182,14018`; `R/runtime_protocol/store.py:462` | Refresh 30s; executor live 90s, separate constants | Blocks admission; registration/claim failures logged |
| Host claim/session: `H:11845,13997` | 50ms lock polling; claim poll 1s; failure backoff ≤30s | Session holds slot; claim failures logged |
| Runtime lease/bounds: `store.py:457` | Lease 30s; maximum 3 attempts; absolute 24h, once each | Expiry fences authority; hard bounds fail task |
| Runtime sweeps: `R/runtime_protocol/server.py:130`; `store.py:4081` | Server maintenance every 0.5s plus reads/mutations | Retains ordinary expired custody; external uncertainty/event or hard-bound failure |
| Host lifetime: `A/astrid/core/execution/guards.py:48`; `H:2942` | Default 3600s plus admitted limits | Timeout abort/failure receipt |
| Publication: `H:499,11655,11746` | 30s reconciliation; .25→5s retries | Non-failure publication can request cancellation; unresolved failure publication retains owner/retries; selective logs |
| Remote phases: `A/astrid/packs/runpod/remote_placement.py:59,422,480,525` | Defaults install 14400s, placement 21600s, exec 600s; incident prep/execution 2700/900s | Named phase deadline errors; multiple independent bounds |
| Remote job loop: `A/astrid/core/execution/machine_run.py:70,100`; `H:7268` | 15s, duplicated/default+environment | Cooperative cancel, exact stop, finally release; no stop until blocked operation returns |
| Pod HTTP: `P:182,344` | 20s default, cap 30s; two retries; .5s pauses; route grace 90s | Transport exception; upload/route warnings |
| Pod readiness/jobs: `P:442,514,590`; `target_selection.py:119` | Ready 600s versus selection 900s; launch 60s; cancel 30s | Detached work survives timeout; cancellation needs exact stop evidence |
| Capacity: `target_selection.py:561,672`; `engine_contracts.py:385` | Optional capacity/paid deadline; 5→60s+jitter, Retry-After; observation 30s | Wait reason/progress; capacity timeout or refusal |
| Provider pacing: `provider.py:139,305,330` | .05s spacing; 60s recovery; retry 5–60s | Persisted cooldown; persistence warning; release retry remains pending |
| Idle/paid expiry: `warm_hold.py:27`; `worker_owner.py:215,254` | Idle default 1800s; incident policy 3600s; independent paid expiry | Timer releases exact machine; state/release reason retained |
| Pod watchdog: `pod_watchdog.py:220` | .1–1s wall-clock checks; retries 1→30s | Attempts self-termination if authorized; typed failure output; K1 removes this mechanism |
| Verification/cleanup: `machine.py:194,1064`; `worker_owner.py:73,849` | Failure observation 120s capped by paid life; exact cleanup 30s | Stale/unsafe custody, release or pending reconciliation; journal/error type |
| Engine custody: `engine_custody.py:53,117,385,1218` | Cleanup 8s; receive .05s; connect .02s; recipe health deadline/poll | Typed cancellation, deadline, ownership/health refusal |
| Installation identity: `engine_runner.py:489`; `remote_placement.py:773` | Recipe/remaining verification bounds; identity checks immediate | `request_mismatch`/unverified installation; baseline loses some observation detail |

**(e) Shared root**

**Inferred — one-sentence architectural root:** Lifecycle decisions are distributed across observers, custody owners and queues, so failed observation or publication can become terminal task state while paid execution and cleanup remain active.

**Evidenced:** Plan 50 specifically documents stuck failure publication and silent CLI behavior caused by incorrect Runtime boundary assumptions hidden by fakes. [plan.md:62](/home/user/wt/dev-log/plans/50-recorded-boundaries/plan.md:62)

**Inferred:** Those incidents, incomplete checkpoint evidence, and failure-log collection gaps share this boundary/observability weakness. They do **not** establish one identical code defect. `request_mismatch` is an identity-validation refusal; HTTP 429 is provider pacing; Ctrl-C is cancellation propagation. Their exact causal connection to this timeout remains unproved. [engine_runner.py:500](/home/user/wt/dive-ran/astrid/core/generation/engine_runner.py:500), [machine.py:874](/home/user/wt/dive-ran/astrid/packs/runpod/machine.py:874)

**(f) Corrections and limits**

**Evidenced:** The claim began at **00:21:09**, before the stated window. The edit’s CLI command spans **00:23:58–00:30:33**; 4m35s describes task following, not the whole command. The failed attempt’s server lease had not yet expired when failure committed. [stage log:3](/tmp/claude-0/-home-user/ebe1c0ff-e4f9-56ce-9569-8dc5a5d6e26c/scratchpad/lease-dive/data/stage2h-edit.log:3)

**Inferred:** Load ~4.3/4 CPUs is a plausible contributor, not an established cause. Logs show transfer activity and later command submission, not that GPU generation was working at failure. They do not establish exact termination time, continued billed amount, or successful cancellation. The supplied `dry-pod/plan.md` was unavailable.

**(g) Smallest change locations and nearest tests**

**Inferred:** Increasing timeouts alone cannot guarantee either requested property. The smallest coherent changes are:

| Proposed location/symbol | Required behavior | Existing nearest tests — evidenced |
|---|---|---|
| `H:run_task.pump_lease`, `lease_transport_fault`, `force_abort`; `R/runtime_protocol/store.py:_reap_expired_leases`, `_settle_attempt` | Separate observation loss from paid-job failure. Retain exact custody, prohibit duplicate execution, and reconcile/reacquire publication authority after connectivity returns. Keep explicit cancellation and paid limits authoritative. | `A/tests/core/execution/test_fail_closed_g28.py::test_transient_transport_recovers_inside_last_acknowledged_validity`; `::test_sustained_transport_stops_at_last_acknowledged_expiry`; `R/tests/test_fail_closed_g28.py::test_lease_lost_owner_can_cede_only_its_exact_retained_attempt` |
| `A/astrid/sdk/generation.py:_runpod_operation`; `H:run/_run_claim_slots`; `worker_owner.py:release` | Give release a reserved control execution path reaching the retained owner independently of generation slots/session locks. Merely raising concurrency can still saturate all slots. | `A/tests/core/execution/test_generic_host_claim_loop.py::test_single_slot_and_once_keep_synchronous_compatibility`; `::test_registration_renews_in_coordinator_while_slots_are_running` |
| `machine_run.py:run_on_machine`; `machine.py:start`; retain K1 `_checkpoint_installed` changes | Propagate cancellation/control through shipping and launch; keep remote observation outside owner locks; retain custody until stop/release is reconciled. | `A/tests/packs/runpod/test_machine.py::test_cancel_stops_the_job_checkpoints_it_then_keeps_verified_machine`; `K/tests/packs/runpod/test_warm_sequence_checkpoint.py::test_success_checkpoint_verification_does_not_hold_owner_lock_during_stalled_http` |

**Inferred:** Add an integrated regression combining a committed-but-unacknowledged heartbeat, stalled transfer, and concurrent release. Existing neighboring tests do not prove that combined journey.
tokens used
147,926
**Evidenced:** The pack host declared the task failed while its execution path continued communicating with the pod. Release entered that same host’s single-worker queue. **Inferred:** The immediate failure was loss of *acknowledged Runtime authority*, not demonstrated failure of the paid workload.

References: **A**=`/home/user/wt/dive-ran`, **K**=`/home/user/wt/dive-k1`, **R**=`/home/user/wt/rt-42ae`; **H**=`A/astrid/core/execution/generic_host.py`. Database citations identify tables/rows because SQLite has no meaningful line numbers. All timestamps below are UTC on 13 November. Investigation was offline/read-only; three Luna/low agents extracted evidence; tests were inspected, not run.

**(a) Read → `lease_lost`**

**Evidenced:** The read originates in the **pack host**, through `RuntimeProtocolClient.task()`. The generated Runtime HTTP client raises `ApiError(status=0, code="transport_timeout")`; the host converts the observation into a lifecycle decision. The CLI subsequently displays the failed task. This is not a pod-to-provider timeout. The installed host/client files match the supplied source copies. [H:5574](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:5574), [generated.py:687](/home/user/wt/rt-42ae/packages/python/astrid_runtime_client/generated.py:687)

**Evidenced:** `astrid-pack-host` holds the attempt lease: attempt `7c133306…`, fence `1`, Runtime epoch `2`. Runtime grants **30 seconds**. The daemon thread `astrid-heartbeat-{task_id}` checks lifecycle state every **50 ms**, performs task reads approximately every **5 seconds**, then renews after successful reads. Progress changes also trigger renewal. Lifecycle HTTP calls have a **2-second timeout**, shortened by remaining validity; heartbeat-lock acquisition is also bounded by two seconds. There are **zero immediate transport retries**; eligible failures retry through subsequent loop iterations. [H:5484](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:5484), [H:11556](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11556), [H:11821](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11821), [store.py:6252](/home/user/wt/rt-42ae/runtime_protocol/store.py:6252)

**Evidenced:** **One transport timeout is not automatically fatal.** `lease_transport_fault()` tolerates it while acknowledged validity and the execution lifetime permit. Failed reads skip renewal. When acknowledged validity ends, the observer preserves the last transport diagnostic and calls `force_abort("lease_lost")`. That sets the cancellation event and sends non-retryable `attempt.fail`. [H:11439](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11439), [H:11520](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11520)

**Evidenced:** `observed_at=00:30:25.787587` timestamps the diagnostic, **not terminalization**. Failure committed at **00:30:31.610**, after the diagnostic’s acknowledged expiry **00:30:28.692**, but before the database’s newer expiry **00:30:33.723**. Runtime committed another heartbeat at **00:30:03.723**; the diagnostic’s last acknowledged heartbeat remains **00:29:58.694537**. [H:11372](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11372); DB `attempts[7c133306…]`, corresponding `command_idempotency[attempt.heartbeat/attempt.fail]`, `events[51]`.

**Inferred:** The later heartbeat committed without its acknowledgement becoming accepted host state. Subsequent observation failures exhausted the older acknowledged lease. Exact abort time, number of failed reads, and why acknowledgement failed are not recorded; “declared lost three seconds before expiry” is therefore misleading.

**Evidenced:** Abort is cooperative. `run_on_machine()` checks cancellation between operations, calls exact-job cancellation, and finally invokes release/retention settlement. `machine.start()` performs shipping and launch without receiving that callback. Detached jobs survive their client. Consequently, marking Runtime failed neither immediately stops remote work nor terminates billing; verified failures may retain an idle machine. Actual cancellation/termination of this edit is unproved. [machine_run.py:97](/home/user/wt/dive-ran/astrid/core/execution/machine_run.py:97), [machine.py:722](/home/user/wt/dive-ran/astrid/packs/runpod/machine.py:722), [machine.py:1052](/home/user/wt/dive-ran/astrid/packs/runpod/machine.py:1052)

**Evidenced:** The lease protects mutation/publication authority and execution custody using lease identity, attempt, fence and epoch. Ordinary expiry retains blockers because expiry is not stop evidence. It does not physically fence a pod process. A late successful result for this already-failed attempt is rejected; expired authority also cannot publish. [store.py:4093](/home/user/wt/rt-42ae/runtime_protocol/store.py:4093), [store.py:6133](/home/user/wt/rt-42ae/runtime_protocol/store.py:6133)

**(b) Timeline and release queue**

**Evidenced — database reconstruction:** Sources are `tasks`, `runs`, `attempts`, `reservations`, `events`, `executors`, `capabilities`, and heartbeat idempotency records in `D/flat/realm.sqlite3`.

| UTC | Recorded fact |
|---|---|
| 00:21:09.672 | Claim `b5599d43…` admitted. |
| 00:21:09.995–00:23:56.906 | Claim attempt `c841a9c4…`, fence 1, CPU reservation; completed, event 48. Result names pod `6foeue5emvt370`, idle/live. |
| 00:25:56.875 | Edit `23949ab4…` admitted, event 49. |
| 00:25:57.030–.031 | GPU reservation created; attempt `7c133306…` claimed, fence 1, event 50. |
| 00:29:58.692 | Heartbeat extends expiry to 00:30:28.692. |
| 00:30:03.723 | Last committed heartbeat extends expiry to 00:30:33.723; executor `last_seen_at` matches. |
| 00:30:25.787587 | Last saved transport diagnostic observed. |
| 00:30:31.609–.610 | Edit/run failed; attempt settled; GPU reservation released; event 51. |
| 00:30:37.656–.657 | Release `8b22cc05…` admitted, event 52; remains queued, with **no attempt or reservation**. |

**Evidenced:** Release is an ordinary `runpod.release` task submitted by `_runpod_operation()`. Both release and claim require CPU; generation requires GPU. All use executor `astrid-pack-host`, whose recorded `max_concurrency=1`. Its single-slot loop synchronously executes `claim_once()` before claiming again. [generation.py:361](/home/user/wt/dive-ran/astrid/sdk/generation.py:361), [H:13718](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:13718), [H:13997](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:13997)

**Inferred:** Release waited behind the still-unwinding edit invocation, not its GPU reservation: that reservation was already released. Continued uploads support this. The host knew about failure—it issued it—but its synchronous execution/session lock remained occupied until return. No stack capture establishes the precise blocking operation. [H:11845](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11845), [host log:1534](/tmp/claude-0/-home-user/ebe1c0ff-e4f9-56ce-9569-8dc5a5d6e26c/scratchpad/lease-dive/data/service-pack-host.log:1534)

**Evidenced:** K1 bounds successful checkpoint verification outside the owner lock, rechecks custody, retains refusal reasons, and improves observer reaping. It leaves the host claim loop and release task route unchanged. **Inferred:** K1 would not prevent this queueing mechanism; it improves later cleanup/checkpoint contention. [K/machine.py:1050](/home/user/wt/dive-k1/astrid/packs/runpod/machine.py:1050), [K/worker_owner.py:781](/home/user/wt/dive-k1/astrid/packs/runpod/worker_owner.py:781)

**(c) Why logs are silent**

**Evidenced:** The lease decision updates a diagnostic object, publishes failure, and writes the attempt receipt; those functions do not print a lease-loss log. Runtime explicitly suppresses HTTP access logging. `runtime.log` is a launch/status dump; `runtime-service.log` is empty. [H:11372](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11372), [H:11520](/home/user/wt/dive-ran/astrid/core/execution/generic_host.py:11520), [server.py:194](/home/user/wt/rt-42ae/runtime_protocol/server.py:194)

**Evidenced:** Host logs contain:

- **00:29:30 onward:** successful upload chunks.
- **00:30:33.480:** upload HTTP 409 and an explicit upload-failure warning, followed by resumed uploads.
- **00:32:02.443:** job POST accepted; subsequent downloads alternate 200/400/200 through the requested window.
- **00:34:50 onward:** route 404 retries, just outside that window.

These are pod HTTP observations, not proof of successful image computation. [log:1503](/tmp/claude-0/-home-user/ebe1c0ff-e4f9-56ce-9569-8dc5a5d6e26c/scratchpad/lease-dive/data/service-pack-host.log:1503), [log:1534](/tmp/claude-0/-home-user/ebe1c0ff-e4f9-56ce-9569-8dc5a5d6e26c/scratchpad/lease-dive/data/service-pack-host.log:1534), [log:1626](/tmp/claude-0/-home-user/ebe1c0ff-e4f9-56ce-9569-8dc5a5d6e26c/scratchpad/lease-dive/data/service-pack-host.log:1626)

**(d) Liveness/custody inventory**

**Evidenced — every row below.** “Once” describes the declaration, not a unified system-wide policy. **P** denotes installed `py/lib/python3.11/site-packages/runpod_lifecycle/https.py`.

| Decision point / file:line | Timeout/interval; declaration | Failure action; reason visibility |
|---|---|---|
| CLI follow: `A/astrid/sdk/invocation.py:3425,3633` | Poll 1s; print 60s; wait 3600s, repeated defaults; capacity policy can remove deadline | Read error returns `task_status_unavailable`; wait timeout returns error, not cancellation |
| Ctrl-C: `invocation.py:3385` | One cancellation request | Requests Runtime cancellation; adds note if unconfirmed |
| Host lifecycle: `H:498,5484,11556` | 5s poll; 50ms guard; 2s HTTP/lock literals | Retry within acknowledged validity, then abort; diagnostic/DB, no direct log |
| Host registration: `H:1182,14018`; `R/runtime_protocol/store.py:462` | Refresh 30s; executor live 90s, separate constants | Blocks admission; registration/claim failures logged |
| Host claim/session: `H:11845,13997` | 50ms lock polling; claim poll 1s; failure backoff ≤30s | Session holds slot; claim failures logged |
| Runtime lease/bounds: `store.py:457` | Lease 30s; maximum 3 attempts; absolute 24h, once each | Expiry fences authority; hard bounds fail task |
| Runtime sweeps: `R/runtime_protocol/server.py:130`; `store.py:4081` | Server maintenance every 0.5s plus reads/mutations | Retains ordinary expired custody; external uncertainty/event or hard-bound failure |
| Host lifetime: `A/astrid/core/execution/guards.py:48`; `H:2942` | Default 3600s plus admitted limits | Timeout abort/failure receipt |
| Publication: `H:499,11655,11746` | 30s reconciliation; .25→5s retries | Non-failure publication can request cancellation; unresolved failure publication retains owner/retries; selective logs |
| Remote phases: `A/astrid/packs/runpod/remote_placement.py:59,422,480,525` | Defaults install 14400s, placement 21600s, exec 600s; incident prep/execution 2700/900s | Named phase deadline errors; multiple independent bounds |
| Remote job loop: `A/astrid/core/execution/machine_run.py:70,100`; `H:7268` | 15s, duplicated/default+environment | Cooperative cancel, exact stop, finally release; no stop until blocked operation returns |
| Pod HTTP: `P:182,344` | 20s default, cap 30s; two retries; .5s pauses; route grace 90s | Transport exception; upload/route warnings |
| Pod readiness/jobs: `P:442,514,590`; `target_selection.py:119` | Ready 600s versus selection 900s; launch 60s; cancel 30s | Detached work survives timeout; cancellation needs exact stop evidence |
| Capacity: `target_selection.py:561,672`; `engine_contracts.py:385` | Optional capacity/paid deadline; 5→60s+jitter, Retry-After; observation 30s | Wait reason/progress; capacity timeout or refusal |
| Provider pacing: `provider.py:139,305,330` | .05s spacing; 60s recovery; retry 5–60s | Persisted cooldown; persistence warning; release retry remains pending |
| Idle/paid expiry: `warm_hold.py:27`; `worker_owner.py:215,254` | Idle default 1800s; incident policy 3600s; independent paid expiry | Timer releases exact machine; state/release reason retained |
| Pod watchdog: `pod_watchdog.py:220` | .1–1s wall-clock checks; retries 1→30s | Attempts self-termination if authorized; typed failure output; K1 removes this mechanism |
| Verification/cleanup: `machine.py:194,1064`; `worker_owner.py:73,849` | Failure observation 120s capped by paid life; exact cleanup 30s | Stale/unsafe custody, release or pending reconciliation; journal/error type |
| Engine custody: `engine_custody.py:53,117,385,1218` | Cleanup 8s; receive .05s; connect .02s; recipe health deadline/poll | Typed cancellation, deadline, ownership/health refusal |
| Installation identity: `engine_runner.py:489`; `remote_placement.py:773` | Recipe/remaining verification bounds; identity checks immediate | `request_mismatch`/unverified installation; baseline loses some observation detail |

**(e) Shared root**

**Inferred — one-sentence architectural root:** Lifecycle decisions are distributed across observers, custody owners and queues, so failed observation or publication can become terminal task state while paid execution and cleanup remain active.

**Evidenced:** Plan 50 specifically documents stuck failure publication and silent CLI behavior caused by incorrect Runtime boundary assumptions hidden by fakes. [plan.md:62](/home/user/wt/dev-log/plans/50-recorded-boundaries/plan.md:62)

**Inferred:** Those incidents, incomplete checkpoint evidence, and failure-log collection gaps share this boundary/observability weakness. They do **not** establish one identical code defect. `request_mismatch` is an identity-validation refusal; HTTP 429 is provider pacing; Ctrl-C is cancellation propagation. Their exact causal connection to this timeout remains unproved. [engine_runner.py:500](/home/user/wt/dive-ran/astrid/core/generation/engine_runner.py:500), [machine.py:874](/home/user/wt/dive-ran/astrid/packs/runpod/machine.py:874)

**(f) Corrections and limits**

**Evidenced:** The claim began at **00:21:09**, before the stated window. The edit’s CLI command spans **00:23:58–00:30:33**; 4m35s describes task following, not the whole command. The failed attempt’s server lease had not yet expired when failure committed. [stage log:3](/tmp/claude-0/-home-user/ebe1c0ff-e4f9-56ce-9569-8dc5a5d6e26c/scratchpad/lease-dive/data/stage2h-edit.log:3)

**Inferred:** Load ~4.3/4 CPUs is a plausible contributor, not an established cause. Logs show transfer activity and later command submission, not that GPU generation was working at failure. They do not establish exact termination time, continued billed amount, or successful cancellation. The supplied `dry-pod/plan.md` was unavailable.

**(g) Smallest change locations and nearest tests**

**Inferred:** Increasing timeouts alone cannot guarantee either requested property. The smallest coherent changes are:

| Proposed location/symbol | Required behavior | Existing nearest tests — evidenced |
|---|---|---|
| `H:run_task.pump_lease`, `lease_transport_fault`, `force_abort`; `R/runtime_protocol/store.py:_reap_expired_leases`, `_settle_attempt` | Separate observation loss from paid-job failure. Retain exact custody, prohibit duplicate execution, and reconcile/reacquire publication authority after connectivity returns. Keep explicit cancellation and paid limits authoritative. | `A/tests/core/execution/test_fail_closed_g28.py::test_transient_transport_recovers_inside_last_acknowledged_validity`; `::test_sustained_transport_stops_at_last_acknowledged_expiry`; `R/tests/test_fail_closed_g28.py::test_lease_lost_owner_can_cede_only_its_exact_retained_attempt` |
| `A/astrid/sdk/generation.py:_runpod_operation`; `H:run/_run_claim_slots`; `worker_owner.py:release` | Give release a reserved control execution path reaching the retained owner independently of generation slots/session locks. Merely raising concurrency can still saturate all slots. | `A/tests/core/execution/test_generic_host_claim_loop.py::test_single_slot_and_once_keep_synchronous_compatibility`; `::test_registration_renews_in_coordinator_while_slots_are_running` |
| `machine_run.py:run_on_machine`; `machine.py:start`; retain K1 `_checkpoint_installed` changes | Propagate cancellation/control through shipping and launch; keep remote observation outside owner locks; retain custody until stop/release is reconciled. | `A/tests/packs/runpod/test_machine.py::test_cancel_stops_the_job_checkpoints_it_then_keeps_verified_machine`; `K/tests/packs/runpod/test_warm_sequence_checkpoint.py::test_success_checkpoint_verification_does_not_hold_owner_lock_during_stalled_http` |

**Inferred:** Add an integrated regression combining a committed-but-unacknowledged heartbeat, stalled transfer, and concurrent release. Existing neighboring tests do not prove that combined journey.
__ASTRA_DONE__ 0
