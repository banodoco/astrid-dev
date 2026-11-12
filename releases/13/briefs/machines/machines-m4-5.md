difficulty: sol (S, write; money safety)

# M4 card 5: the paid deadline holds through every acquisition phase; no lock-holding thread handoff

**Clone:** `/home/user/wt/c-m4` (branch `r13/machines-m4`, HEAD `0d152b373`, clean). Card 4 is `1d4471866..0d152b373`; brief `machines-m4-4.md`. Astra's re-check, binding: `/home/user/wt/briefs/wave3/machines-m4-recheck.log` (its final report comes after the last line that is exactly `codex`). Six of the seven earlier findings are closed. Fix the two new blocking findings, as ruled by the manager:

1. **Blocking, money: a synchronous provider lookup must not outlive the paid deadline.** `target_selection.py` about 972 calls `observed_hourly_usd()` (`adapter.py` about 242, synchronous provider HTTP) on the acquisition event-loop thread while holding the owner lock, so the deadline watcher cannot run. Example: a 30 s claim reaches rate verification at second 29, and the lookup takes another 30 s. The pod stays billable past its persisted expiry, and the resulting lifetime failure becomes `cleanup_pending` with a scheduled recovery instead of an immediate release (the immediate-release handler catches only `CapacityWaitTimeout`). Fix:
   - make every provider call made after the paid create, rate verification included, interruptible by the durable deadline (run it off the loop, or bound it by the remaining paid time);
   - send every lifetime-expiry failure during acquisition through the immediate exact-pod release, keeping the recovery retries only when that release itself fails.

   Test: a blocked rate lookup that straddles expiry starts the release at expiry and makes no second create.
2. **Blocking, custody: the thread handoff can deadlock.** `worker_owner.py` about 425 hands acquisition to another thread and waits for it, while `generation.py:prepare_retained_generation` (about 91-110) already holds `lease_owner.lock` when it calls `acquire()`. Expiry and release need the same lock. Do the handoff before any caller takes the outer lock, or keep the locked operation on one thread; never wait for another thread while holding `lease_owner.lock`. Test: embedded retained generation on a claimed machine, with a running event loop, completes, and expiry release still runs. Note: M1 part c (another branch, landing before M4) changes `prepare_retained_generation` to take only a `ClaimedJob` and stops it calling `acquire()` on the job path. Keep your change local to the handoff and the lock order, so the two branches merge cleanly.

Proof, from `/home/user/wt/c-m4`. The new tests must fail before and pass after. Run only these:
```
TMPDIR=$PWD/.tmp-tests PYTHONPATH="$PWD:/home/user/wt/vibecomfy-a8a7be7" /home/user/astrid-agent.env/venv/bin/python -m pytest -q tests/packs/runpod/test_owner_retry_gate.py tests/core/test_machines_claim.py tests/test_setup_skill_branches.py tests/packs/runpod/test_warm_session.py tests/packs/runpod/test_target_selection.py <your new test file> --basetemp=$PWD/.tmp-tests/pt
```
Then ruff (no rise from `0d152b373`) and `git diff --check`, plus the mypy count for the files you edit, before and after: it must not rise, and fix the listed Release 13 rows in those files (see the gates rule below). Save the diff (`git diff 0d152b373`) to `/home/user/wt/briefs/wave3/machines-m4-5.diff`. List every function you change.
## Rules (all apply)
- do not push or commit (the manager commits);
- never weaken, skip or delete a test, except one that encodes behaviour the owner ordered removed (generate-time allocation, per-job consent, the paid consent flag, `--until-release`); convert such a test to the new behaviour and list it with a one-line reason. If any other existing test conflicts with this brief, do not edit it: stop and report which test and why;
- no RunPod or paid calls: never call api.runpod.io, rest.runpod.io or any other RunPod endpoint, and never run any `astrid generate` or `astrid machines` command (the network proxy would act on the real paid account); drive the CLI only through `main([...])` in tests with fakes. Package registries, GitHub and Hugging Face reads are allowed;
- never read `.env`, credential files or ~/.codex;
- start no long-lived services (loopback test servers inside tests are fine);
- ruff must not rise (`python -m scripts.reshape.compare_ruff_baseline`; baseline 2117);
- no AI model or product names in code, comments, tests or text meant for commits;
- stop after three failed attempts at any one problem and report it;
- Python is `/home/user/astrid-agent.env/venv/bin/python` with `PYTHONPATH="$PWD:/home/user/wt/vibecomfy-a8a7be7"`;
- other workers run on this machine: run pytest with `TMPDIR=$PWD/.tmp-tests` and `--basetemp=$PWD/.tmp-tests/pt`, and delete `.tmp-tests` at the end;
- run only the proof this brief names: no full suite, no `pytest tests/` and no extra suites. A separate test lane compares the full suite on hosted CI, and on this shared 4-CPU machine extra runs cause failures from load alone;
- candidate gates (binding): read `/home/user/wt/briefs/wave3/machines-gates.md`. In the files you edit, bring mypy to net zero over Release 12 and never raise the core/pack boundary ratchet, and report both measurements;
- Use your Luna sub-agents for reading, inventories, call-site and test searches, mechanical edits and running checks; keep your own effort for the design and judgment; run independent sub-agents in parallel. Every sub-agent follows these same rules;
- run only the test commands this brief names; no full-repository suite;
- return the diff (`git diff --stat` and where the full diff is saved), the before and after results with counts, and every converted test with its reason.

## Owner principles (binding)
As simple as possible, one path for each thing; declared once, with sensible defaults; no shims or interim steps; minimal safety ceremony (keep real money and custody safety, drop bureaucracy); every failure or wait understandable from the product. If something looks muddled, say so in your report rather than building around it.
