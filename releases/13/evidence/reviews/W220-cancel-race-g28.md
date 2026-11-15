# W220: test_cancel_completion_error_propagates_and_retains_pending_evidence[False] on 401dbd78

## Verdict: (a) flaky timing race that also exists on R12 main

The same test fails on R12 main 0e1543e0 in 5/40 idle runs and 11/40 loaded runs, with the same
`AssertionError: assert 2 == 1`. It is not an R13 regression, and the attribution bucket REGRESSION is a
false positive. The attribution rule matched on commit 29753ea1b154, which touches the file but not this test.
The test body, including the `len(attempts) == 1` line, is identical on R12 and 401dbd78. The race is a
product-side race (see Mechanism), so this is not a test-only assumption. The test only makes it likely by
shrinking the lease poll to 0.05 s. Recommendation: defer, with an R12 row.

## Run-to-run nondeterminism

37bd5e06..401dbd78 is one file, scripts/reshape/baselines/ruff_astrid.json (2 insertions, 2 deletions), a Ruff baseline JSON.
It cannot change test behaviour. The one-test pass/fail flip between the 37bd5e06 CI run and the 401dbd78 CI
run is therefore pure run-to-run nondeterminism: the test fails about 12 to 45 percent of the time on every
tree tested, and the earlier candidates passed by chance. Passing in "every earlier candidate" was a single
sample each.

## Mechanism (401dbd78 line numbers, astrid/core/execution/generic_host.py)

There are two independent callers of `client.cancel`, and nothing makes them mutually exclusive.

1. Run path, `_run_task_impl`, lines 12901-12915. After `HostCancelled`, `collect_terminal_evidence("cancelled")` runs
   and then `completion_call(self.client.cancel, task_id, **cancel_kwargs)` is called with stop_observed=True.
   If it raises, line 12914 sets `_terminal["evidence_pending"] = True` and re-raises (this is what the test asserts).
   `completion_call` (11612-11657) only sets `terminal["recorded"]` after a successful call (11656), and it holds
   `completion_lock` only for the pre-check and the post-update, not during the Runtime call.
2. Lease pump thread, `pump_lease` (11947 on). It starts with `next_poll = now + poll_seconds` and runs `task_snapshot()`
   on each poll. In this test the fixture patches `_LEASE_POLL_SECONDS` to 0.05 (tests/core/execution/test_fail_closed_g28.py:57).
   If the status is `cancel_requested` or `cancelled` (11984), it calls `force_abort("cancelled")` (11990).
   `force_abort` (11905-11940) returns early only if `terminal["recorded"]` or `terminal["forced"]` (11908).
   Otherwise it sets forced and calls `completion_call(self.client.cancel, ..., outputs=[], stop_observed=(stage == "admission"))`
   at 11928.

The pump is stopped from only two places. One is the outer wrapper after `_run_task_impl` returns or raises
(12295-12297, `stop.set()` plus `join`). The other is `if _terminal.get("recorded"): pump_stop.set()` at 13813,
which is skipped when the cancel failed.

- One call: `_run_task_impl` raises and the wrapper stops the pump before the first poll fires at 0.05 s after pump start.
  This is the usual case on an idle machine, since the run path gets through its cleanup in about 0.004 s to a few tens of ms.
- Two calls: the run path's cancel fails (the test's fake raises `OSError`). That leaves `recorded` unset and `forced` unset.
  If the run path has not yet been unwound and joined when the pump's first poll fires, the pump reads the still-`cancel_requested`
  task (the failed fake never moved it to cancelled), takes the `forced` slot and issues a second `cancel`.
  The captured stderr in the CI log shows exactly this. `category: cancel_requested` at elapsed 0.004 s is the `cancelled()`
  closure in the run path (12717-12718). `category: cancelled` at elapsed 0.051 s is `force_abort("cancelled")` from the
  pump's first poll (11911-11913). So the run path took more than 0.05 s to unwind. On a loaded runner this happens in
  roughly a third of the runs.

There is no lock or flag around "a cancel for this attempt has been started". `recorded` is set only on success and
`forced` is set only by the pump. Neither is set by the run path before its call, nor after its failure.

## User-visible impact (product)

Not test-only. In production `_LEASE_POLL_SECONDS` is `authority_window_seconds / 60` = 5 s (R12: 5.0), so the window is
far smaller but real: whenever the Runtime cancel call fails or is still in flight at a poll boundary, a second cancel is issued.

- The second request is different from the first. It has `outputs=[]` and `stop_observed=False` (not in admission), against the
  run path's collected evidence outputs and `stop_observed=True`. The idempotency key includes `-stop-<0|1>` (astrid/core/execution/generic_host.py:6120-6122), so
  the two requests are distinct keys. The Runtime can therefore receive an evidence-less cancel alongside (or ahead of) the
  evidence-bearing one.
- A failure of the second call is swallowed into `terminal["reporting_error"]` (11940-11941).
- Bounded, not catastrophic: the run path's `evidence_pending` is still set and the retained attempt root keeps the evidence.
  The documented behaviour is a duplicate or racing cancel request, and a possible evidence-less cancel acknowledged first.
  The pending evidence is not lost on the host.

## Reproduction

401dbd78 and R12 main were each run in a venv with that tree's pinned Runtime (scripts/ci_install_runtime.py).
401dbd78 used Runtime 6855dfa8df65; R12 used Runtime 42ae24aff8d2. Python 3.13 on 4 CPUs.
The command was one pytest process per run: `timeout 120 python -m pytest -p no:cacheprovider -q <node id>[False]`,
40 runs per condition, in a plain shell loop.
Load was 2 `python3 -c 'while True: pass'` processes (killed afterwards; none remain).

| Condition | Pass | Fail | Failure reason |
|---|---|---|---|
| 401dbd78, idle | 30 | 10 | `assert 2 == 1` (all 10) |
| 401dbd78, 2 CPU-burn processes | 22 | 18 | `assert 2 == 1` (all 18) |
| R12 main 0e1543e0, idle | 35 | 5 | `assert 2 == 1` (all 5) |
| R12 main 0e1543e0, 2 CPU-burn processes | 29 | 11 | `assert 2 == 1` (all 11) |

An earlier 401dbd78 idle loop ran while a background pip install was competing for CPU, and gave 21 pass / 19 fail. I discarded it
as confounded (moved to /tmp/w220/confounded/); it is consistent with the load effect. The `[True]` (caller-owned) variant was not
run, because the card names only the [False] id.
The idle gap between 401dbd78 (10/40) and R12 (5/40) is within run-to-run noise at n=40. The code between them changed `_LEASE_POLL_SECONDS` plumbing
(R12 uses 5.0 constant; the 401 pump scales by `authority_window_seconds`), but the fixture pins 0.05 on both, so the pump timing in the test is the same.

## Recommendation

- Defer. Add an R12 row: "test_fail_closed_g28::test_cancel_completion_error_propagates_and_retains_pending_evidence[False] is flaky on R12 main
  (5/40 idle, 11/40 loaded)." Do not count it against the R13 candidate. The attribution bucket should read preexisting-flaky.
- Do not retry CI as proof either way: the failure rate is 12 to 45 percent, so one green re-run proves nothing.
- Follow-up (own card, either side of the release): make the cancel single-flight. Set a `cancel_started` marker (under `completion_lock`)
  in the run path before its `completion_call(self.client.cancel ...)` and check it in `force_abort` and `reconcile_publication`, or stop the pump
  before the run path issues its cancel. If the test is kept as is, it needs the pump parked (a large `_LEASE_POLL_SECONDS` for this test),
  but that would hide the product race rather than fix it.

Evidence files: /tmp/w220/{a_401_idle,c_401_load,b_r12_idle,d_r12_load}.results and `.runN.log`; loop script /tmp/w220/loop.sh.
No tracked file was edited, no pushes, no dispatch, no paid calls; the two scratch git worktrees were removed.
