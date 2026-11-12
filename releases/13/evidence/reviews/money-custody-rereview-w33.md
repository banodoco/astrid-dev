# W33 — money and custody re-review

Reviewed 2026-11-12. **Commits 1–4 need changes under this card's requirements. `ce797451` fixes the specified blocker; no finding on that fix.** Findings below distinguish introduced defects from the shared, pre-existing retention prerequisite. No GPU, paid integration, network, RunPod-host, or `astrid` command was run. No product source was changed.

## Scope and evidence

I read each requested diff and the surrounding acquisition, preparation, settlement, release, timer, recovery, transport, and test code. References below are **file:line at the named commit**, not the unrelated checked-out HEAD. Commits 1–4 were read from Git objects in `/home/user/astrid-agent`; that checkout is clean at `0e1543e0`, and does not have a local `r13/compose` ref. The requested immutable objects are available. Commit 5 was read in `/home/user/wt/agent-w26`, clean at `ce797451`.

CPU checks used only the authorized runner in `/home/user/wt/agent-compose`, clean at `913c6b8fff8c63aeb05cb1b5ae160463f6d5e641`. Its provider implementation is identical to `f0535fef`; the reviewed machine/generation/lease-owner implementations match `9e7b2a48`. Its generic host includes subsequent log-collection changes. It does **not** contain the `ce797451` observation-transaction implementation. Thus these are composed-checkout checks, not historical-commit baseline comparisons. Findings are source-path evidence unless explicitly described as test results.

## 1. `d072cf5d` — failed job keeps warm

### Blocking — failure retention has no expiry enforcement that survives loss of the host

**Location:** `astrid/packs/runpod/machine.py:1145`; `astrid/packs/runpod/worker_owner.py:590`, `:601`, `:227`, `:270`.

**Evidence/path:** the new failure path sets `warm = True`, admits `stale_after_failure`, and settles idle. The journal records `min(now + idle_seconds, paid_expires_at)`, but `_arm()` enforces it through process-local WarmHolds and a process-local paid-deadline timer. WarmHolds uses a daemon `threading.Timer` (`astrid/core/execution/warm_hold.py:47`). Kill the host after this settlement and leave it down beyond either deadline: the journal survives, but neither timer does; nothing in this path installs an independent provider/pod billing-stop deadline. `recover()` releases only when another owner actually starts. Restart fencing prevents reuse, but cannot undo the billed interval before restart. A crash between `_save()` and `_arm()` has the same issue.

This is a **pre-existing architectural limitation newly relied on by the expanded failure-retention path**, not a claim that this commit introduced host-local timers. It blocks the card's explicit “at the latest at its disclosed idle limit, crashes included” guarantee. Even without a crash, release starts at expiry and can take its separate cleanup budget or retry through an outage; a stored expiry is not a confirmed billing stop.

**Smallest fix:** condition these new keep-warm outcomes on an independently armed, exact-pod billing-stop expiry that survives controller loss and is no later than the disclosed bound. Until that exists, do not enable the additional failure-retention cases. A restart-only test or another local timer does not close this gap.

**Missing test:** kill the settled warm owner, keep it absent past idle/paid expiry, and assert independent termination. Existing `test_small_lease_owner_process_death_releases_lock_and_recovers` immediately constructs a replacement owner; it proves recovery, not termination while no owner runs.

### Should-fix — release reasons confuse verification timeout, paid expiry, and custody change

**Location:** `astrid/packs/runpod/machine.py:1093`, `:1103`, `:1109`, `:1122`.

**Evidence/path:** with paid time remaining, let the shorter failure-verification budget expire. The combined condition assigns `paid_limit_exhausted`, although consented paid time remains. Conversely, if the lease is already paid-expired before `preparation_claim()`, that method raises; the handler sets `custody_changed`, and `rejection = rejection or "paid_limit_exhausted"` preserves the wrong cause. Neither path demonstrates a changed owner.

**Smallest fix:** distinguish the clocks and recognize an expired but otherwise exact invocation before assigning a custody reason. **This is already addressed by the subsequent `9e7b2a48`; it is a finding on this commit in isolation, not an outstanding duplicate repair.**

**Tests:** the added receipt-refresh, stale-installation, unreachable-engine and safety-reason tests cover the intended branches. The paid-expiry test advances expiry during verification, missing expiry before the first claim check. The separate verification-timeout test arrives in commit 2. None of the added tests proves crash-independent expiry. In this review's composed run, the keep-warm tests could not reach those branches because their shared fake installation failed first; see validation below.

**Other conclusions:** the installation update rechecks operation, owner epoch, invocation, generation, pod, preparation, and (where supplied) job under the owner lock. Reuse re-observes provider identity and compares custody; stale preparation is not directly executed. I found no additional introduced price-cap bypass or simultaneous-owner admission on the canonical account-journal path. The failed outcome remains failed when the pod is kept.

**Verdict:** do not accept the crash-inclusive retention guarantee. The reason defect is fixed by commit 2; the shared expiry prerequisite remains open.

## 2. `9e7b2a48` — failed preparation keeps warm

### Blocking — newly retained preparation failures inherit the same crash-expiry gap

**Location:** `astrid/packs/runpod/generation.py:196`; `astrid/packs/runpod/machine.py:677`, `:685`; `astrid/packs/runpod/worker_owner.py:606`.

**Evidence/path:** after a stopped, reachable failed installation, preparation is saved as `stale_after_failure` and settled idle instead of released. Killing the host now removes its only expiry enforcement. The expiry/cost receipt makes the bound visible, but does not enforce it independently. This is **the same shared prerequisite as finding 1**, not a second independent timer defect.

**Smallest fix/test:** gate this new retention on the same independent exact-pod billing-stop mechanism and exercise owner absence beyond the disclosed deadline.

### Blocking — the new recovery annotation can consume the final release retry

**Location:** `astrid/packs/runpod/worker_owner.py:365`–`:372` (especially `:369`).

**Evidence/path:** an idle/paid release fails, so `release()` cancels the old deadline timer and installs `_retry_recovery()` as the replacement (`:739`–`:748`). This commit adds a journal `_save(... release_mechanism="recovery")` **before** calling `release()`. If that added write raises once, for example on a transient write/fsync failure, control goes to the outer handler, which only sets `last_error_type`. `release()` never runs, so its retry scheduling never runs. The fired recovery timer is spent; the original paid timer was canceled. A still-visible pod remains `releasing` and billed with no live automatic retry, even after storage recovers. Previously this annotation write did not exist, and release's own writes were inside its retry-protected body.

**Smallest fix:** move the annotation inside the release operation's existing retry boundary, or explicitly re-arm the exact operation on any pre-release recovery failure. Do not make optional mechanism metadata a prerequisite for attempting/retrying cleanup.

**Missing test:** force the first release into pending recovery, fail only this annotation write once, restore storage, and prove the exact pod is eventually deleted without another user action. `test_recovery_preserves_release_cause` tests only a successful `_save`.

### Should-fix — the new reachability probe can run past the paid deadline while blocking expiry

**Location:** `astrid/packs/runpod/generation.py:91`, `:184`–`:197` (probe at `:193`).

**Evidence/path:** the entire preparation block holds `lease_owner.lock`. After a failure with stopped jobs and saved custody, the new handler calls `claim.ops.exec("true", timeout=10)` without checking/clipping the paid time remaining. If failure occurs just before or at paid expiry, this optional keep-warm probe can take another ten seconds while the paid timer waits for that same lock. The later `save()`/settlement check rejects expiry, but only after the extra delay. This is not the separately authorized exact-stop cleanup budget: it is a probe to decide whether to retain a pod whose retention authority may already be exhausted.

**Smallest fix:** refuse retention immediately at paid expiry; otherwise bound the probe by the remaining paid time using the existing bounded transport, and recheck exact custody after observation. Prefer not holding the owner lock over the probe.

**Missing test:** a stopped preparation failure at the paid boundary with a stalled reachability probe and a concurrently fired expiry timer.

**Tests/other conclusions:** the new tests cover repeated preparation failure/re-preparation, source-digest-only changes, refusal of stale preparations with live jobs, receipt identity/cost/expiry, verification versus paid timeout, and ordinary stale-pod timer expiry. The exact cancellation ACK now checks the job ID. Preparation saves use `preparation_claim()`, and the lock prevents a second local invocation entering during preparation. There is no new consent extension in this change: reuse still passes the existing paid-consent/rate checks and clips against the previous lifetime. The three isolated state/release-cause checks passed; the end-to-end fake-machine fixture is currently broken. No new crash-without-restart or failed-recovery-write test exists.

**Verdict:** request changes. Exact-owner admission is substantially guarded, but the release-retry loss is an introduced unbounded-billing path, and the crash-inclusive promise remains unsupported.

## 3. `56284e6c` — terminal reconcile

### Blocking — transient 408/429 responses are promoted to permanent publication rejection

**Location:** `astrid/core/execution/generic_host.py:11215`, `:11652`, `:13903`.

**Evidence/path:** the new host conditions classify every `400 <= status < 500` as rejection. The protocol layer deliberately limits definite publication rejection to `{400, 409, 422}` plus an exact nonterminal readback (`:5803`). Its tests explicitly expect 408 and 429 not to be `TerminalPublicationRejected`.

A successful producer whose settlement encounters repeated 429s enters reconciliation. A further 429 reaches `:11652`, which calls `reject_publication()` and sends an evidence-free failure with `publication_rejected` (`:11690`–`:11702`). Once that write succeeds, a valid successful job is recorded as failed. A failure publication receiving 408/429 similarly switches to ceding and drops its evidence instead of replaying it. Startup recovery has the same broad classification; it can even classify a transient **task-read** 429 as terminal-evidence rejection because the catch covers the whole loop.

**Smallest fix:** share the protocol's typed, exact-owner rejection classifier. Keep 408/429 and transport uncertainty on the unchanged-request replay path, with bounded back-off. A failed observation must not become evidence that the publication was rejected.

**Missing test:** host-level successful settlement and failed publication each receive 408/429 before recovering; verify unchanged verb/body/key and preserved result. Existing status-parameterized tests exercise only the lower-level classifier, so they pass despite the contradictory host behavior.

### Blocking — startup recovery drops an exact owner in `cancel_requested`

**Location:** `astrid/core/execution/generic_host.py:13869`–`:13873`.

**Evidence/path:** `_recover_terminal_requests()` breaks whenever `state != "running"`, even if the saved request still has the current attempt and fence. `cancel_requested` is explicitly nonterminal in the pinned Runtime. `runtime_protocol/store.py:6629` records it with `waiting_reason="provider_state_unknown"`, `remote_stop_confirmed=False`, and `billing_stop_confirmed=False`, retaining unresolved custody.

A host can persist a stopped-producer terminal request, lose its ACK/crash, and restart after an owner cancellation has moved that same external attempt to `cancel_requested`. Recovery sees the same attempt/fence but skips both replay and ceding; `run()` proceeds with the old request unhandled. A cancellation request is not proof of custody transfer or billing stop.

**Smallest fix:** stop recovery only for confirmed terminal states or a changed exact owner. Reconcile `cancel_requested` under its existing attempt/fence; use the saved stop proof where valid and the evidence-free cede path when publication authority expires. Keep unknown states explicitly unresolved instead of silently skipping them.

**Missing test:** restart with a saved fail/cancel request and the same fenced attempt in `cancel_requested`; assert terminal acknowledgement and reservation release. The added restart test uses a task still reported as running with an expired timestamp.

**Other conclusions and retry limits:** the separate `-cede` idempotency key avoids colliding with the original evidence request. In the tested definite-conflict/expiry path, the Runtime's evidence-free fail permits expired-lease ceding and actually settles the attempt. The original producer is not rerun. These acknowledgements release Runtime custody; they are not themselves provider billing-stop receipts. Unknown transport failures still retry without a total count/time bound: the live loop caps individual sleeps at five seconds, and the lease pump can keep renewing while publication is pending. Startup recovery is also unbounded until shutdown. I do not treat simply abandoning ambiguous custody as a safe fix; the “never retries forever” description must not be read as a guarantee for outages or repeatedly rejected cede requests.

**Tests:** the added tests cover definite failure rejection, exact transport replay, transient cede outage and an expired failure request on restart. The composed file produced **22 passes, 1 failure**: `test_conflict_fails_exact_owner_without_conflicting_evidence` expected a RuntimeError but none was raised. No historical baseline was run, so this is not classified as this commit's regression. There is no added cancel-request restart test, host 408/429 test, or permanently unavailable cede/changed-epoch liveness test.

**Verdict:** request changes for the broad rejection classifier and nonterminal recovery skip. The tested happy cede path works; the stronger universal custody/liveness claim does not.

## 4. `f0535fef` — account provider gate

### Blocking — interrupted gate-state writes can permanently block cleanup or erase cooldown

**Location:** `astrid/packs/runpod/provider.py:145`–`:152`; consumers at `:242`, `:269`; `astrid/packs/runpod/worker_owner.py:773`.

**Evidence/path:** every `_state()` call reads JSON, truncates the same locked file, writes JSON in place, and only flushes it. This includes read-like operations and the credential-to-account alias. There is no atomic replacement, fsync durability, schema validation or malformed-state recovery. A process crash between truncate and flush leaves an empty file, which is treated as a fresh gate and discards the account cooldown/alias. A partial/failed write or storage crash can leave invalid JSON, after which every caller raises at `json.loads` indefinitely.

If that is the account gate or alias for an already rented pod, `_release()` cannot even pass `account_gate(...)`. Its retries read the same unrepaired bytes forever; restart does not repair them. This turns auxiliary pacing state into a persistent barrier to terminating a billable pod. File locking prevents simultaneous writers, not torn-state recovery.

**Smallest fix:** hold a stable separate lock file and durably atomically replace validated state. Handle missing/invalid state with a bounded conservative recovery policy that preserves cleanup liveness; do not silently treat a torn cooldown as success. Replacing the currently locked inode without a separate lock would introduce a different cross-process race.

**Missing test:** kill/fail a writer at truncate/write/flush, reopen from another process, and prove both conservative pacing and eventual exact cleanup.

### Should-fix — important product provider calls bypass the claimed shared gate

**Location:** `astrid/packs/runpod/worker_preparation.py:535`, `:579`, `:1413`, `:1768`; `astrid/packs/runpod/provider.py:269`.

**Evidence/path:** this patch gates inventory and REST machine reads, but `confirm_acquired_machine()` still calls `lifecycle_graphql.get_pod()` directly and catches failures before retrying every three seconds. GPU-count reads and the GPU catalog also call GraphQL directly. `acquire_target()` calls `launch_when_available()` without the gate. These are reached from ordinary paid selection. A 429 on one of these calls neither observes an existing shared cooldown nor updates it; the machine-confirmation loop continues its fixed polling while the account is throttled. The new gate is not one admission point for all product provider traffic.

**Smallest fix:** route these remaining observation/create operations through the same account gate, retaining the existing write-ahead create record and ambiguous-create rules. Do not add an unjournaled automatic POST retry. Carry the acquisition's deadline/cancellation through admission.

**Missing test:** an existing account cooldown blocks actual acquisition/GraphQL entrypoints, and a GraphQL 429 slows another process's inventory/release admission. Current tests exercise the gate abstraction and selected cleanup seams.

### Should-fix — stable-account binding is installed in a decorator that paid selection bypasses

**Location:** `astrid/packs/runpod/worker_preparation.py:239`; `astrid/packs/runpod/target_selection.py:864`, `:874`; `astrid/packs/runpod/provider.py:223`, `:227`.

**Evidence/path:** the new acquisition account binding sits in `_exclusive_target_owner`. Normal `RunPodSelectionOwner._select()` already holds the custody lock and deliberately invokes `acquire_target.__wrapped__` / `reconcile_target.__wrapped__`, bypassing that binding. Its earlier volume lookup also calls the gate without an account reference. There is no equivalent binding in `_select()`. Before release/liveness later binds the credential, the gate uses the credential hash. If another credential for the same configured account already has a cooldown, first acquisition with a rotated/new key can use a different gate and bypass it. The helper's explicit-binding unit test does not prove the product path binds.

**Smallest fix:** bind the verified configured account immediately after constructing its provider config and before any provider observation, including paths that intentionally bypass the custody-lock decorator. Ensure in-flight unbound callers cannot update an abandoned gate after migration.

**Missing test:** drive ordinary paid selection with a fresh credential against an account already cooling down under a previous credential, without manually calling `account_gate(..., account_ref=...)` in the test setup for the new credential.

### Should-fix — the advertised deadline does not bound all gate work or cancellation

**Location:** `astrid/packs/runpod/provider.py:128`, `:172`, `:201`, `:269`, `:300`–`:305`.

**Evidence/path:** `before_call()` bounds admission, but account-alias resolution and response bookkeeping each call `_state()` without the caller deadline, granting fresh 30-second lock budgets. `ProviderGate.call()` does not bound the operation itself. More seriously, when `async_provider_call()` times out it synchronously calls `account_gate(api_key).after_error()` on the event loop: alias locking and state locking can exceed the expired budget by additional waits. A caller with essentially no budget is therefore not guaranteed to return promptly.

Cancellation also does not cancel a started daemon worker: `set_running_or_notify_cancel()` runs before gate admission. If the async waiter is canceled while the worker waits in the gate, the worker can still invoke the provider operation later. The gate has no cancellation input. This is not proof of wrong-pod deletion—the exact ID is retained—but it defeats the claimed bounded/cancelable operation and permits overlapping late cleanup work with later retries.

**Smallest fix:** propagate one remaining monotonic budget through alias lookup, lock acquisition, admission and response accounting; avoid blocking post-timeout bookkeeping on the event loop. Check a cancellation signal before initiating provider I/O, and track already-started cleanup separately so later retries cannot mistake caller timeout for operation completion.

**Missing test:** deadline exhaustion while alias/response-state lock is held, cancellation during admission, and a late operation overlapping a retry. The existing timeout test intentionally lets an already-started operation continue and then manually releases it; it does not cover these cases.

**Other conclusions/tests:** shared state does serialize admission for callers using the same valid gate path. Success resets the exponent without clearing another caller's cooldown. Retry-After may exceed 60 seconds: only each sleep and reported retry-timer delay are capped; admission refuses when the cooldown cannot fit its deadline. The gate performs one operation, not an automatic retry loop. Release recovery retries until absence rather than imposing a count cap that would abandon a paid pod. The new tests use multiple objects/threads, not a killed writer or independent-process contention. Both focused suites passed: **11 + 6 tests**. They do not establish full account coverage or crash safety.

**Verdict:** request changes. The crash-unsafe state file can obstruct paid cleanup indefinitely; coverage, binding and deadline gaps prevent accepting the gate's broader claims.

## 5. `ce797451` — observation transaction construction

**No finding within the requested scope.**

**Evidence:** `astrid/core/execution/custody_broker.py:3385` supplies `transaction=None`. A non-None transaction takes the earlier continuation branch and returns. In the fresh-acquisition branch, construction is now inside the `try` at `:3413`. If construction raises, assignment has not happened and the parameter remains `None`; the `BaseException` handler preserves/records uncertainty and reraises the original error. The `finally` guards `transaction.active = False` and releases the acquired lock at `:3424`. There is no unbound-local error, double release, or bypass of the existing fail-closed uncertainty state. The transaction class uses ordinary attributes; its successful-path invalidation remains unchanged.

The added test at `tests/core/execution/test_custody_broker.py:4921` injects `MemoryError` in `__init__`, checks the original exception object and uncertainty, and acquires the lock from **another thread**. That last detail is necessary because same-thread re-acquisition of an RLock would not detect this leak. It directly addresses the blocker.

I did not run that test against a substitute implementation: the only authorized test checkout, `913c6b8f`, lacks this transaction change. This is a source-and-test review of exact `ce797451`, not a claimed execution pass.

**Verdict:** accept for the narrow question asked. The construction-time lock leak is fixed; the fix introduces no identified unsafe behavior.

## Validation record

All commands below ran sequentially, one test file at a time, from `/home/user/wt/agent-compose` at `913c6b8fff8c63aeb05cb1b5ae160463f6d5e641`. The runner supplies isolated HOME/data directories and disables bytecode/pytest cache writes. Provider/pod calls in the selected tests are fakes; the terminal tests use the in-process Runtime service. The repository RunPod guard is installed. No paid or GPU tests were selected.

1. `/home/user/astrid-dev/env/agent-pytest.sh -q -m 'not gpu and not integration' tests/packs/runpod/test_provider_gate.py` — **PASS**, exit 0, 11 passed in 1.32s.
2. `/home/user/astrid-dev/env/agent-pytest.sh -q -m 'not gpu and not integration' tests/packs/runpod/test_provider_gate_release.py` — **PASS**, exit 0, 6 passed in 0.83s.
3. `/home/user/astrid-dev/env/agent-pytest.sh -q -m 'not gpu and not integration' tests/packs/runpod/test_failed_job_keeps_warm.py` — **FAIL / interrupted**, exit 2; 6 failures reported in 107.70s before interruption. All six fail during the initial fake engine installation, before the keep/release assertions. Trace: `test_failed_job_keeps_warm._failed -> machine.claim -> prepare_retained_generation -> prepare_claimed -> _install -> RetainedPod.job_start -> engine_runner.install_engine -> FakeContext.ensure_dir -> FakeContext.record`, ending at `tests/core/generation/test_engine_runner.py:115`: `AssertionError: /workspace/astrid/engines/comfyui/models`, with `FakeContext.models_root is None` and root `/root/astrid/engines/comfyui`. I interrupted the remaining run after observing repeated failures and did not edit the fixture or rerun it unchanged. No pass is claimed for these retention paths, nor is this fixture failure attributed to a reviewed commit without a baseline.
4. `/home/user/astrid-dev/env/agent-pytest.sh -q -m 'not gpu and not integration' tests/core/execution/test_bug14_settlement_liveness.py` — **FAIL**, exit 1, 22 passed / 1 failed in 20.98s. Failure: `test_conflict_fails_exact_owner_without_conflicting_evidence`, line 221, `Failed: DID NOT RAISE <class 'RuntimeError'>`; expected message `output metadata does not match existing object`.
5. `/home/user/astrid-dev/env/agent-pytest.sh -q -m 'not gpu and not integration' tests/packs/runpod/test_keep_warm_evidence.py -k 'stale_preparation_requires_each_exact_job_stopped or recovery_preserves_release_cause'` — **PASS for selected checks only**, exit 0, 3 passed / 8 deselected in 1.48s. Selected these independent checks after diagnosing the shared fake-machine fixture failure; this does not substitute for the eight unrun paths.

No baseline, provider execution, or crash-injection experiment was performed. Missing-path tests above are requested proof for repairs, not tests claimed to have run. Review used the `astrid-dev` investigation guidance only; no delegation, integration, commits or publication. Routes used: Unknown — no route-provenance tooling was invoked under the read-only card.
