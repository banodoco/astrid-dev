difficulty: sol (S, write)

# M5: the idle timer is the one lifetime mode; idle counts only while nothing runs or is queued; `keep NAME --for` extends; `--idle never`

**Repo:** Astrid. **Clone:** `/home/user/wt/c-m5` (branch `r13/machines-m5`, base `r13/machines` at `__BASE__`, which includes M1, M2 and M4: a claim has a lifetime (`--for`, the paid expiry) and a separate idle time (`--idle`); the cap bounds both). Work in this clone only.

Read first (binding): `/home/user/wt/briefs/wave3/machines-design.md` and `/home/user/wt/briefs/wave3/machines-plan.md` (row **M5**). **Owner decision, 12 Nov:** the idle timer is the only lifetime mode; idle counts only while nothing is running or queued on the machine; `machines keep NAME --for` extends it; `--idle never` replaces `--until-release`; the budget cap still bounds everything (Plan 40 D1: a forgotten machine must not bill all night).

## Outcome
1. **The idle clock** (`astrid/packs/runpod/worker_owner.py`: `settle`, `_expire`, the idle timer) runs only while the machine has no running job and no Runtime task queued for it. It restarts from the full idle time when the last job settles and the queue is empty. Use the Runtime queue that already exists; add no scheduler.
2. **`machines keep NAME --for DURATION`** extends the lifetime (paid expiry) by DURATION and raises the cap by rate × DURATION. It needs no `--max-usd`, and refuses in one line, naming `--max-usd`, only when that would pass the saved budget cap (`machines_cli.py:_keep`; `worker_owner.py:keep`).
3. **`--idle never`** (on claim and keep) turns off idle release. The machine ends at its lifetime or cap, or on `machines release`. `--until-release` is deleted everywhere (`machines_cli.py` about 516); convert its tests (owner removed it) and list them.
4. **Host shutdown still releases** (Plan 40 D12/D13), unchanged.

## Tests (must fail before, pass after)
New `tests/packs/runpod/test_idle_with_queue.py`:
- (a) a queued task keeps the idle clock stopped;
- (b) after the last job settles with an empty queue, the idle clock starts from the full idle time and releases on expiry;
- (c) `keep NAME --for 1h` extends the lifetime and the cap by rate × 1h;
- (d) `keep` past the budget cap refuses in one line;
- (e) `--idle never` keeps the machine until the lifetime or cap, and `release` ends it;
- (f) paid expiry still releases even with a queue (money safety).

Keep every reset, custody and expiry test passing. Every `tests/packs/runpod/test_warm_session.py` test must pass (M4 fixed the five paid-expiry failures).

Proof, from `/home/user/wt/c-m5`, before and after:
```
TMPDIR=$PWD/.tmp-tests PYTHONPATH="$PWD:/home/user/wt/vibecomfy-fe92ac7" /home/user/astrid-agent.env/venv/bin/python -m pytest -q tests/packs/runpod/test_idle_with_queue.py tests/packs/runpod/test_failed_job_keeps_warm.py tests/packs/runpod/test_warm_session.py tests/core/execution/test_warm_hold.py tests/core/test_machines_claim.py --basetemp=$PWD/.tmp-tests/pt
```
Then ruff and `git diff --check`. Save the diff to `/home/user/wt/briefs/wave3/machines-m5.diff`.
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
- candidate gates (binding): read `/home/user/wt/briefs/wave3/machines-gates.md`. In the files you edit, bring mypy to net zero over Release 12 and never raise the core/pack boundary ratchet, and report both measurements;
- Use your Luna sub-agents for reading, inventories, call-site and test searches, mechanical edits and running checks; keep your own effort for the design and judgment; run independent sub-agents in parallel. Every sub-agent follows these same rules;
- run only the test commands this brief names; no full-repository suite;
- return the diff (`git diff --stat` and where the full diff is saved), the before and after results with counts, and every converted test with its reason.

## Owner principles (binding)
As simple as possible, one path for each thing; declared once, with sensible defaults; no shims or interim steps; minimal safety ceremony (keep real money and custody safety, drop bureaucracy); every failure or wait understandable from the product. If something looks muddled, say so in your report rather than building around it.
