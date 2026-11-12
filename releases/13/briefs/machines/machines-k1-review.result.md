
codex
**Verdict: merge after the listed blocking fix.**

1. **Blocking — verification can hold custody and delay release past paid expiry.**  
   [machine.py:1010](/home/user/wt/c-k1/astrid/packs/runpod/machine.py:1010) holds `owner.lock` throughout verification. [remote_placement.py:713](/home/user/wt/c-k1/astrid/packs/runpod/remote_placement.py:713) computes the window at verification entry and shares it across status and receipt reading, but passes only a command timeout to the normally unbounded transport.

   The real transport [starts the command before starting that timeout](/home/user/astrid-agent.env/venv/lib/python3.13/site-packages/runpod_lifecycle/https.py:482). HTTP waits, retries and cancellation can overrun it. With two paid seconds remaining, a ten-second start request already crosses expiry while [the expiry callback waits for the same lock](/home/user/wt/c-k1/astrid/packs/runpod/worker_owner.py:244). A slow-drip response can delay release much longer. The eventual expiry check prevents saving the installation; it does not prevent billing during the overrun.

   **Smallest fix:** reuse the absolute, cancellable bounded-observer mechanism already used by failure verification. Perform remote observation outside the owner lock, retaining locked custody checks before observation and before saving. Add a success-checkpoint test covering stalled transport, paid expiry, release and absence of a late checkpoint. The new expiry test currently advances the clock **after verification returns**, so it misses this scenario.

2. **Should fix — reason propagation remains incomplete, and refusals lack a next action.**  
   [machine.py:1022](/home/user/wt/c-k1/astrid/packs/runpod/machine.py:1022) attaches `install_unverified` only when verification returns `False`. A receipt changed between status and receipt reading instead raises at [remote_placement.py:796](/home/user/wt/c-k1/astrid/packs/runpod/remote_placement.py:796), bypassing that handler. Attestation mismatches, changed-job refusals, and epoch/expiry fences likewise lack the field, so [build_receipt](/home/user/wt/c-k1/astrid/packs/runpod/failure_receipt.py:140) cannot preserve their reason.

   **Smallest fix:** attach fixed reason codes to these checkpoint refusals while preserving their exception types and custody behavior. Include the reason and an appropriate recovery action in one line. Extend the tests to assert the specific reason in both error and receipt for raised exceptions and custody changes.

The manager’s remaining questions:

- **Custody checks:** installation, job, epoch, invocation and expiry checks remain effective at checkpoint entry and save. The patch strengthens job fencing. The problem above is delayed release during observation, not acceptance of an expired lease at the final save. No allocation, lease-extension, shutdown or restart path was changed.
- **Evidence for (a)–(d):** (b) is soundly excluded as a general missing-snapshot-save defect: re-preparation persists the verified installation. (c) is excluded only as the simple stale-snapshot comparison explanation: the observed refusal precedes that comparison, and successful attested refreshes are checkpointed. Neither establishes what edit-specific preparation did; (d) remains uninvestigated.
- **Live timing:** 213.389 seconds of execution and collection starting 1.196 seconds after `done` do **not** establish timer exhaustion. The artifacts omit the configured execution allowance and verification reason. Near-expiry starvation is conditionally consistent, but unproven. Also, `_remaining()` floors at one second, so the proposed zero-budget refusal *before status runs* is not the actual default-path mechanism. The new test demonstrates a synthetic short-status-budget failure.
- **Receipt coverage:** [the new source-change test](/home/user/wt/c-k1/tests/packs/runpod/test_warm_sequence_checkpoint.py:157) checks the reason in the error, receipt and rendered output. The field validation excludes newlines. Coverage does not extend to the exception paths above; the receipt’s main message remains generic.

The five named test files ran **once: 186 passed, 1 warning**, in 1919.28 seconds. No existing tests or assertions were changed, weakened, skipped or deleted. `git diff --check` passed. `.tmp-tests` was removed and the working tree is clean. No paid calls were made.

**Final verdict: merge after the listed blocking fix.**
