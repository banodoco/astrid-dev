# Unknown is not dead: one verdict owner, one deadline, a control lane

Facts: Astra's report is `astra-report.md` in this folder (full log `astra.log`). **A** = `/home/user/wt/dive-ran`, **H** = `A/astrid/core/execution/generic_host.py`, **R** = `/home/user/wt/rt-42ae/runtime_protocol`. Nothing here was run live; line references were read, not executed.

## 1. The structural cause

The attempt lease is a takeover mechanism in a system that has no takeover. The Runtime grants 30 s (`R/store.py:457`) and, when it expires, reassigns the work to nobody: it keeps custody "because expiry is not stop evidence" (`R/store.py:4139`) and only locks the rightful owner out of renewing and publishing (`R/store.py:6265`). So the lease's one live effect is self-harm. The host's observer thread keeps a private copy of the expiry (`lease_valid_until`), and when it cannot *hear* the Runtime for that long it publishes a non-retryable failure for its own paid job (`H:11567`, `H:11520`). **Absence of observation is treated as a verdict.** The thread that decides isn't the thread that works, so "failed" is published while the work carries on; the worker's only slot stays occupied; and release, being an ordinary task on that slot, queues behind the corpse. Each decider has its own clock (30 s lease, 5 s poll, 2 s HTTP, 90 s executor liveness, 20 s pod HTTP, 15 s job loop), and none writes its reason to a log.

## 2. The end state

**Rule: only a positive signal ends paid work.** Three signals exist, each with one owner:

| Verdict | Sole owner | Signal |
|---|---|---|
| The attempt has lost authority | Runtime | a typed answer: state, attempt or fence changed; cancel requested; renewal refused |
| The work has run out of time | the admitted work deadline (`_AttemptLifetime`) | the clock the user declared (preparation, execution, paid cap) |
| The host is gone | executor registration (already 30 s refresh, 90 s liveness, in the coordinator thread) | one signal per process, not per attempt |

A transport timeout, a stalled process or a missed poll is none of these. It means "unknown": the host keeps working and keeps asking.

What this removes or changes:

- **Remove the host's private lease clock.** `lease_valid_until` and its four abort sites go. The host cannot out-guess the store of record, and in this incident it guessed wrong (section 5).
- **Size the lease to the work; the worker renews it.** The heartbeat already accepts `lease_seconds` (`R/service.py:10077`) and the Runtime already caps it at the attempt deadline (`R/store.py:4034`). The end state asks for the remaining work lifetime, so the lease and the deadline become one clock and the heartbeat becomes a progress report.
- **Abort means stop.** The cancel signal reaches every blocking step (shipping, launch, polling), so a stopped attempt frees its slot within one chunk and its pod job is cancelled, not orphaned.
- **Release is control, not work.** Control capabilities (release, status, cancel) are claimed by a reserved lane that job slots can never fill. Release of a busy machine sets that job's cancel signal and proceeds: the owner's command wins.
- **Every verdict writes its reason once,** where it is decided: the host log, the task event and the CLI's `waiting=` line. A queued task always says what it waits for.
- **Declare once.** The poll interval and HTTP timeout derive from the one lease window in the execution policy.

Rejected:

- **Longer timeouts alone:** a stall longer than any number still kills the job.
- **More slots alone:** two long jobs fill two slots and release waits again.
- **Release outside the Runtime** (CLI straight to the provider): a second path, and it bypasses custody.
- **A pod-side dead-man switch for liveness:** K1 removes the pod watchdog; spend safety stays with the host's paid and idle expiry.

## 3. R13 slice: "a slow host never kills a paid job, and release never waits"

Agent-only; no Runtime pin bump. Routes are N/X/S as I read them (S hardest). All tests offline, on fakes or the real local Runtime; nothing paid.

**T1. Unknown is not dead** (engine lane, S)
- Scope: `H:run_task.pump_lease`, `lease_transport_fault`, `completion_call`, `renew_progress`.
- Change: when local validity lapses or a lifecycle call times out, record the reason and keep polling. Call `force_abort("lease_lost")` only on a typed Runtime answer or when the work lifetime expires. Settle is attempted regardless; the Runtime's fence decides.
- Proof, in `A/tests/core/execution/test_fail_closed_g28.py`:
  - convert `test_sustained_transport_stops_at_last_acknowledged_expiry` to `test_sustained_transport_keeps_work_until_runtime_verdict_or_deadline` (it encodes the behaviour this removes);
  - new `test_committed_but_unacknowledged_heartbeat_does_not_fail_attempt` (the incident: the Runtime commits, the reply is dropped for 25 s, the job completes and settles);
  - `test_transient_transport_recovers_inside_last_acknowledged_validity` stays green.

**T2. A lease window sized to the work** (engine lane, N)
- Scope: `H:RuntimeProtocolClient.heartbeat` (`H:5495`), `_lifecycle_client` (`H:5484`), `_LEASE_POLL_SECONDS` (`H:498`); one new field in the execution policy (`A/astrid/core/execution/guards.py`).
- Change: one declared `authority_window_seconds` (300 for R13), sent as `lease_seconds` on every heartbeat; the poll and HTTP timeout derive from it. A stall of several minutes no longer expires the lease on the Runtime's side. 300 is chosen over the full lifetime until T6 confirms how restart recovery depends on expiry.
- Proof: new `test_heartbeat_requests_declared_authority_window`; in `R/tests/test_fail_closed_g28.py` terms, an Agent integration test against the pinned Runtime that a heartbeat with 300 moves `lease_expires_at` by 300 s.

**T3. Abort stops the work and frees the slot** (machines lane, X)
- Scope: `A/astrid/packs/runpod/machine.py:Machine.start` (line 722), `A/astrid/core/execution/machine_run.py:run_on_machine` (line 97); keep K1's `_checkpoint_installed` change.
- Change: `start` takes the same `cancelled` callback `claim` already takes (line 553) and checks it between upload chunks and before launch.
- Proof: new `tests/packs/runpod/test_machine.py::test_cancel_during_shipping_stops_within_one_chunk_and_launches_nothing`; `test_cancel_stops_the_job_checkpoints_it_then_keeps_verified_machine` stays green.

**T4. A control lane for release** (machines lane, S)
- Scope: `H:run` and `_run_claim_slots` (lines 13997, 14153), `claim_once` (line 13642, which already filters by `capability_ids`); the registration's `max_concurrency` and resource keys; `A/astrid/packs/runpod` capability declarations for `runpod.release`, `runpod.status`; `worker_owner.py:release`.
- Change: register job slots + 1. The extra slot claims only capabilities declared `control`, which reserve a `control` key (not `cpu`, so release doesn't wait behind a capacity wait either). Release of a machine with a job in flight sets that job's cancel signal first.
- Proof, in `A/tests/core/execution/test_generic_host_claim_loop.py`:
  - new `test_release_is_claimed_while_the_job_slot_is_busy`;
  - new `test_control_slot_never_claims_a_generation`;
  - `test_registration_renews_in_coordinator_while_slots_are_running` stays green;
  - new `tests/packs/runpod/test_machine.py::test_release_during_running_job_cancels_then_releases`.

**T5. Say why** (engine lane, N)
- Scope: `H:record_lease_diagnostic` (line 11372), `force_abort` (line 11520), `A/astrid/core/execution/host_log.py`; the CLI follower `A/astrid/sdk/invocation.py:3425`.
- Change: one host-log line per verdict and per change of diagnostic category (task, attempt, category, last acknowledged heartbeat, elapsed). A task queued longer than 10 s prints what holds the slot.
- Proof: new `test_lease_verdict_is_logged_with_reason`; new `tests/sdk/test_invocation_follow.py::test_queued_task_reports_what_it_waits_for`.

**Journey proof for the slice** (T1–T4 together): one row in `tests/integrations/test_remote_machine_cpu.py`, `test_runtime_silent_for_one_lease_then_release`: the Runtime's replies are held for 40 s mid-upload; the job completes; a release admitted during the silence completes in under 5 s.

Order: T1 and T3 first (either alone would have saved this job or freed this slot), then T2, T4, T5.

## 4. After R13

- **T6 (Runtime, Plan 50 RB-4):** lease = remaining work lifetime; delete the 30 s default; restart recovery keyed on executor liveness and epoch, not on expiry. Queued tasks get a Runtime-written `waiting_reason` (`executor_busy`, `executor_not_seen`).
- **Plan 50 fault matrix:** add rows for "reply lost after commit", "host stalled for N s", "release during a job", "release after a failed job"; a slow-transport injector at the recorded boundary; and the candidate lint against silent wait loops becomes a commitment, widened to "every abort site logs".
- **Machines plan (O6, O8):** the control lane becomes the per-machine queue's control channel; `machines show` displays the current verdict and reason.
- **One timing declaration:** fold the inventory's remaining clocks (pod HTTP 20 s, job loop 15 s, ready 600 s vs selection 900 s) into the execution policy.

## 5. What contradicts the incident summary

- **The CLI timed out nothing.** The pack host's observer made the read and published the failure; the CLI only displayed it.
- **The lease had not expired.** The Runtime committed a heartbeat at 00:30:03.723, valid to 00:30:33.723; the failure was committed at 00:30:31.610. The host acted on its stale copy (00:30:28.692). `observed_at` 00:30:25 is the last failed read, not the abort.
- **One timeout isn't fatal in the code;** about 25 s of them was. Lifecycle calls time out at 2 s with no immediate retry.
- **The pod was probably not yet generating.** Seven short jobs had run by 00:27:34 (preparation, inferred); at the failure the host was mid-upload (148 MB sent). It then posted six more jobs between 00:32:02 and 00:33:13, up to 2m 40s *after* the task had failed: the failed attempt kept driving the paid pod.
- **The stall was wider than the Runtime.** One pod upload hung from 00:30:00.7 to 00:30:33.5 in the same window, so the host process or the container stalled as a whole (inferred). Load is a plausible cause, not a proven one.
- **Release did not wait behind a job in the queue.** The GPU reservation was already released; it waited behind the failed attempt's still-running thread in the only slot. K1 would not have prevented it.
- **The logs weren't empty,** only reasonless: the 409 at 00:30:33 and the upload trail are there; the Runtime suppresses access logs.
- **Not one identical root for the week.** Stuck publication, the silent CLI, the missing observation and failure-log gaps share "a verdict without evidence, unreported". `request_mismatch`, the 429 loop and Ctrl-C are separate defects.
- `../dry-pod/plan.md` does not exist.
