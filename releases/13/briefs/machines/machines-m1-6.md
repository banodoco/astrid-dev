difficulty: sol (S, write; custody)

# M1 part d: restart recovery for every journalled state, and preparation-expiry cover (Astra's final M1 check)

**Clone:** `/home/user/wt/c-m1` (branch `r13/machines-m1`, HEAD `2ef923df5`, clean). M1: `git diff 22e5a13e5 2ef923df5`. Briefs: `machines-m1.md`, `machines-m1-4.final.md` and `machines-m1-5.md`, with the manager's rulings. Astra's final check, binding: `/home/user/wt/briefs/wave3/machines-m1-final-review.log` (its final report comes after the last line that is exactly `codex`). All four original findings are closed. Fix the new ones, as ruled by the manager:

1. **Blocking, custody: interrupted journals must reach recovery.** `adapter.py:_claimed_preferences` (about 470) refuses every journal whose root state is not `claimed` before it builds the owner. Example: release records `cleanup_pending`, the host crashes, a job reaches the restarted host, and no owner or cleanup timer exists to stop billing. A journal that has recorded claim settings and any interrupted state (cleanup or release pending, active, allocating) must build its owner and go through `recover_job()` → `recover()`, which reconciles or releases the exact pod. The job is then refused in one line that names the state. Test: exact-pod cleanup with no replacement allocation.
2. **Blocking, custody: an incompatible idle claim must still be cleaned up.** In `worker_owner.py:recover_job` (about 297), `_owned()` can raise on a recipe, model or source compatibility mismatch after an upgrade before reaching the `recover()` fallback. Adapter construction then closes the new owner without releasing the pod or re-arming its timers. On a mismatch, refuse adoption and take the exact-custody recovery path (release or reconcile). Test that upgrade case.
3. **Blocking: replace the deleted preparation-expiry cover.** The guard at `generation.py` about 170 has no live-path test equivalent to the deleted `test_preparation_expiry_never_admits_worker` (see it in `git show 22e5a13e5:tests/packs/runpod/test_generation_preparation.py`). Convert it to claim first: preparation starts inside the paid window and finishes after expiry. Assert refusal before execution, no replacement allocation, and exact cleanup custody kept.
4. **Should fix:** when cleanup is pending, `worker_owner.py` about 404 says "no machine: run `astrid machines claim`", and that claim then refuses the existing custody. Name the unresolved preparation instead: `` machine <id> has an unresolved preparation: run `astrid machines release <id>`, then claim again ``.

Proof, from `/home/user/wt/c-m1` (new tests must fail before and pass after):
```
TMPDIR=$PWD/.tmp-tests PYTHONPATH="$PWD:/home/user/wt/vibecomfy-fe92ac7" /home/user/astrid-agent.env/venv/bin/python -m pytest -q tests/packs/runpod/test_job_on_claimed_machine.py tests/packs/runpod/test_failed_job_keeps_warm.py tests/packs/runpod/test_failure_receipt.py tests/packs/runpod/test_keep_warm_evidence.py tests/packs/runpod/test_target_selection.py tests/packs/runpod/test_generation_preparation.py tests/packs/runpod/test_acquisition_gates_provider_fields.py --basetemp=$PWD/.tmp-tests/pt
```
Then ruff (baseline 2117) and `git diff --check`. Save the diff to `/home/user/wt/briefs/wave3/machines-m1d.diff`. List every function you changed in `machine.py`, `adapter.py`, `generation.py` and `worker_owner.py`.

**Authorisation:** tests that build a recovery owner by hand, or that assert the old "no machine" text for pending cleanup, may be converted, keeping every money, custody and release assertion. Stop only if one of those cannot be kept.
## Rules (all apply)
- do not push or commit (the manager commits);
- never weaken, skip or delete a test, except one that encodes behaviour the owner ordered removed (generate-time allocation, per-job consent, the paid consent flag, `--until-release`); convert such a test to the new behaviour and list it with a one-line reason. If any other existing test conflicts with this brief, do not edit it: stop and report which test and why;
- no RunPod or paid calls: never call api.runpod.io, rest.runpod.io or any other RunPod endpoint, and never run any `astrid generate` or `astrid machines` command (the network proxy would act on the real paid account); drive the CLI only through `main([...])` in tests with fakes. Package registries, GitHub and Hugging Face reads are allowed;
- never read `.env`, credential files or ~/.codex;
- start no long-lived services (loopback test servers inside tests are fine);
- ruff must not rise (`python -m scripts.reshape.compare_ruff_baseline`; baseline 2117);
- no AI model or product names in code, comments, tests or text meant for commits;
- stop after three failed attempts at any one problem and report it;
- Python is `/home/user/astrid-agent.env/venv/bin/python` with `PYTHONPATH="$PWD:/home/user/wt/vibecomfy-fe92ac7"`;
- other workers run on this machine: run pytest with `TMPDIR=$PWD/.tmp-tests` and `--basetemp=$PWD/.tmp-tests/pt`, and delete `.tmp-tests` at the end;
- run only the proof this brief names: no full suite, no `pytest tests/` and no extra suites. A separate test lane compares the full suite on hosted CI, and on this shared 4-CPU machine extra runs cause failures from load alone;
- Use your Luna sub-agents for reading, inventories, call-site and test searches, mechanical edits and running checks; keep your own effort for the design and judgment; run independent sub-agents in parallel. Every sub-agent follows these same rules;
- run only the test commands this brief names; no full-repository suite;
- return the diff (`git diff --stat` and where the full diff is saved), the before and after results with counts, and every converted test with its reason.

## Owner principles (binding)
As simple as possible, one path for each thing; declared once, with sensible defaults; no shims or interim steps; minimal safety ceremony (keep real money and custody safety, drop bureaucracy); every failure or wait understandable from the product. If something looks muddled, say so in your report rather than building around it.
