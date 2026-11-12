# Machines lane: handover note (12 Nov 2026)

**From:** the machines-lane manager that ran as a fork inside the orchestrator's session (`session_011EzfW2L4ou5fDudzKLrc9d`).
**To:** the dedicated machines session. Read `releases/13/machines-session-brief.md` for your role, setup and rules. This note gives you the state.

Copies of every brief named here are in `releases/13/briefs/machines/` on astrid-dev `r13-progress/decision-log`.

## 1. Branches (astrid-agent; all pushed, nothing to main)

| Branch | SHA | State |
|---|---|---|
| `r13/machines` | `2a91ea92b` | The lane trunk. It now contains `r13/compose` `913c6b8f` (engine layout, cells pin VibeComfy `a8a7be7c`, engine-u1), merged with `--no-ff`. It was pushed as a fast-forward from `22e5a13e5` just before the orchestrator asked for the separate name below. There was no force-push. No machines card is merged into it yet. |
| `r13/machines-compose-merge` | `2a91ea92b` | The same commit, under the name the orchestrator asked for. |
| `r13/machines-k1` | `cf70c72f8` | **K1 is done and proven.** A success after earlier failed jobs on a warm machine is checkpointed and returned (this fixes edit keep-warm). Its Astra review is running (see 2). Merge it first once the review passes. |
| `r13/machines-m1` | `2ef923df5` | M1 parts a–c are committed: `a040c372` (four claim-first conversions), `f3978b08`, `bf3dd2f0` (the job attaches whatever its preferences: T6 / M1 part b) and `2ef923df` (job preparation takes only claimed-job authority). |
| `r13/machines-m1-partd-wip` | `a99c31702` | **WIP, unproven, do not merge.** A snapshot of M1 part d's uncommitted tests (`test_generation_preparation.py`, `test_job_on_claimed_machine.py`) while its worker was still running. The worker's final state replaces it (see 2). |
| `r13/machines-m4` | `0d152b373` | M4 through card 4: paid expiry is bounded by the lifetime from the paid create; a 1 s retry floor on the expiry and release path only. Astra re-check: two blocking findings, which card 5 addresses (see 4). |
| `r13/machines-m4-card5-wip` | `c78344b04` | **WIP, unproven, do not merge.** Card 5's partial diff (`generation.py`, `target_selection.py`, `worker_owner.py`, new `tests/packs/runpod/test_acquisition_deadline.py`). Its worker died when the disk filled. It was never re-run or tested. Relaunch card 5 from it with `machines-m4-5.md`. |

The same partial diffs are also stored as files: `releases/13/briefs/machines/m4-card5.partial.diff` and `m1-partd.partial.diff`.

## 2. In-flight workers at handover

- **K1 Astra review** (`machines-k1-review.md`, read-only, in `c-k1`). At last look, more than 90 cases (about 77% of the suite) had passed with no failures. Findings so far don't change the verdict.
  - One noted point: the new regressions (the near-deadline case, changed-job fencing, missing reason propagation) failed before the fix and pass after it. They support the fix, but they **don't establish the cause of the live edit failure.** The orchestrator's next live edit run is the real test.
  - **Next step:** read the final verdict (the worker's last message, after the last line that is exactly `codex`). If it says merge, merge `r13/machines-k1` into `r13/machines` with `--no-ff`.
- **M1 part d** (Sol, high effort, `machines-m1-6.md`, in `c-m1`). It closes M1's three custody gaps plus the should-fix (see 4). The earlier run, which showed 17 failed and 106 errors, overlapped the full disk and **isn't trusted.** This rerun had no setup errors at last look and was working through the sequential-job cases.
  - Its log shows two confirmed causes for the recovery gaps: journals are rejected before the owner is built, and compatibility errors escape before cleanup.
  - **Next step:** read its final message. Re-run the proof command from `machines-m1-6.md` yourself: the new tests fail before the change and pass after it, ruff passes at baseline 2117, `git diff --check` is clean, and the mypy and boundary gates pass. Commit to `r13/machines-m1`. Then run an Astra re-check (read-only, high effort) of part d alone before merging M1. If the worker never finished, start from `r13/machines-m1-partd-wip`.
- **M4 card 5:** not running (see the table).
- **Not mine:** a Codex worker in `c-mypy` (started about 18:40) belongs to the test lane's mypy work.

If I'm still alive when K1's review and M1 part d finish, I'll push their results to `r13/machines-k1` and `r13/machines-m1` (or the WIP branch) and tell the orchestrator. I won't launch any new work.

## 3. Order (ruled)

1. **K1:** merge after the Astra review passes.
2. **M1:** merge after part d is proven and Astra re-checks it.
3. **M2** (`machines-m2.md`, brief written): `generate` never rents and takes no paid flags. It deletes `--gpu`, `--datacenter` and the job preferences snapshot from generate, plus the allocation shims and preferences plumbing. With no live machine it refuses in one line.
4. **LT** (`machines-lt.draft.md`, draft): one lease transition table. Sol (high effort), clone `c-lt`, branch `r13/machines-lt`, based on `r13/machines` after M1 and M2.
   - `astrid/packs/runpod/lease_states.py` holds three things:
     - an enum of states (the reachable combinations of `record.state`, `lease.state` and `preparation.state`);
     - an enum of events;
     - a (state × event) → (next state, billing action) table.
   - Every writer goes through `transition()`.
   - Tests go in `tests/packs/runpod/test_lease_transition_table.py`:
     - (a) every state × {restart, paid expiry, idle expiry, job failure, recipe/model/source change, cancel} ends released, or kept with a deadline no later than the paid expiry;
     - (b) five required rows: cleanup-pending plus restart; idle plus an incompatible change plus restart; preparing plus paid expiry; acquiring after the paid create plus expiry mid-call; idle and active idle expiry;
     - (c) the table is the only writer.
   - One Astra review.
5. **M4:** relaunch card 5 from the WIP branch. The deadline must interrupt post-create provider calls, and no thread may wait under `lease_owner.lock`. Then merge LT into it (merge, never rebase) and run an Astra re-check.
6. **M3** (`machines-m3.md`): named machines. `generate --machine NAME`, or the one live machine, runs on that machine.
7. **M5–M10** after the first live claim-path pass. Briefs written so far: `machines-m5.md`, `machines-m6.md`, `machines-m7.md`. The rest come from `machines-plan.md`. M8 and M9 also get an Opus taste check.

## 4. Astra findings today, with status

**M1 first review** (`machines-m1-review.log`): four findings. **All closed** by M1 parts a–c (confirmed by the final review).

**M1 final review** (`machines-m1-final-review.md` and `.log`). 227 passed. Verdict: "merge after the listed blocking fixes". All of these are **open**, handled by M1 part d (running):
1. Interrupted custody bypasses restart recovery (`adapter.py:470`, `_claimed_preferences`).
2. An incompatible idle claim bypasses cleanup (`worker_owner.py:297`).
3. The preparation-expiry cover was deleted (`generation.py:170`).
4. Should fix: `worker_owner.py:404` names the wrong action for pending cleanup.

**M4 first review** (`machines-m4-review.md`): seven findings. The card 4 re-check (`machines-m4-recheck.md` and `.log`) found:
- 2–7 closed and 1 partially closed;
- the 429 conditions met;
- the 12 test conversions keep their assertions.

Two blocking findings are **open**, handled by card 5 (partial on the WIP branch, unproven):
1. The synchronous `observed_hourly_usd` call (`target_selection.py:972` → `adapter.py:242`) defeats the paid deadline. Lifetime failures also go to `cleanup_pending` instead of being released immediately.
2. A thread handoff deadlock: `worker_owner.py:425` against `generation.py:91-110`, which holds `lease_owner.lock`.

**Task 18:** five `test_warm_session` failures, caused by `f0535fef5` (the 5 s retry floor). **Closed in M4 card 4** by the ruling below.

**K1 review:** running; nothing blocking so far (see 2).

## 5. Rulings in force

- **Retry floor:** 1 s, on the expiry and release path only (M4 card 4).
- **M1's four:** the part d fixes listed in 4 above, all required before M1 merges.
- **M2:** delete `--gpu`, `--datacenter` and the job preferences snapshot from generate. GPU, datacenter and volume are claim-time choices. `describe` stays a quote tool.
- **M3:** a bare `generate` with exactly one live claimed machine uses it.
- **M4:**
  - Lifetime and idle are separate.
  - A priced stockout needs no `--max-hourly-usd`.
  - A pinned, ended machine keeps its detailed diagnostic.
- **Lifetime:**
  - `--for` is the lifetime. It and `--max-usd` are each derived from the other.
  - Idle is a preference (`--idle`). `--idle never` arrives in M5.
  - `keep NAME --for` extends both the lifetime and the cap, and refuses only when that goes past the saved budget.
- **M6:** becomes `machines claim --datacenter`, which drops the volume with a notice.
- **First claim without a TTY:** saves nothing.
- **Reviews:**
  - Astra (high effort) reviews every S and SS diff before merge.
  - An Opus taste check runs on M8 and M9.
  - Money and custody work uses Sol at high effort.
- **Merging:**
  - Cards merge into `r13/machines` with `--no-ff`.
  - Merge `origin/r13/compose` into a card before landing it.
  - Push task branches yourself, never to main.
  - Send the orchestrator the SHA and the `machine.py` functions changed.

## 6. Gates (binding; `machines-gates.md`)

1. **mypy:** net zero per file over Release 12.
   - The per-finding list is `releases/13/evidence/tests/mypy/new-findings.tsv` (153 rows; an identical copy is `briefs/machines/machines-mypy-new-findings.tsv`).
   - Measure with `python -m mypy <files> 2>&1 | grep -c ': error:'`.
   - Ownership:
     - **K1 follow-up:** `remote_placement`, `provider`, `failure_receipt`, `pod_fields`.
     - **M2:** `machine`, `adapter`, `generation`, `generic_host`, `sdk/generation`.
     - **M2 and M6:** `target_selection`.
     - **M5:** `worker_owner`.
     - **M7:** `machines_cli`, plus the boundary crossings.
     - **Test lane:** `installer/progress`.
   - The session brief says the lane owns 117; use the evidence file as the authority.
2. **Boundary ratchet:** `scripts/check_core_pack_boundary.py --check`. Never `--write-baseline`. The orchestrator lands the one-time, owner-ruled baseline update.
3. **Ruff:** baseline 2117, moving to per-(file, code) ratchets run by the test lane. Never raise BLE001 or F821 in your files.

Standard worker rules are in `machines-rules.md`. They forbid every RunPod endpoint and every `astrid generate` or `astrid machines` command, and require full access and Luna sub-agents. Copy them into every brief, and fix its paths (`PYTHONPATH` pin checkout, Python venv) for your container.

## 7. Lessons from this lane

- **Disk:** keep at least 5 GB free; a full disk killed card 5 and corrupted M1 part d's first proof. Put `TMPDIR` in the clone (`.tmp-tests`) and clear it after every proof.
- **Reading a worker's result:** read its message after the last line that is exactly `codex`, and check the process is gone. Launcher sub-agents sometimes report the brief's tail, or report too early.
- **Full access:** under `workspace-write`, Codex sub-agents fail (`~/.codex` becomes read-only). Always use full access.
