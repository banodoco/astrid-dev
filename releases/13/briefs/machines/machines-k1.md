difficulty: sol (S, write; custody)

# K1: a job that succeeds on a warm machine after earlier failed jobs is checkpointed and returned

**Repo:** Astrid. **Clone:** `/home/user/wt/c-k1` (branch `r13/machines-k1`, base ``r13/machines` at `22e5a13e5``). Work in this clone only.

## Live finding (Stage 1 on `f9214240`, 16:19 UTC, one warm pod `o33u3hp1g3gfft`, generation 4)
Job sequence on one claim:
1. TTS failed in execution.
2. SFX failed at admission.
3. t2i SUCCEEDED.
4. Edit generated its image on the pod (`Qwen_image_2.1.png`; execution 213 s, `done` at 1794500293.56). The host then failed it at fetch with `MachineError: completed job has no verified canonical installation`.

The error comes from `RunPodMachine._checkpoint_installed` (`astrid/packs/runpod/machine.py` about 1001-1017): `placement._canonical_installed(state)` (`remote_placement.py` about 709) returned False. The check just before it, `preparation["state"] != "prepared"`, did not fire. Afterwards the machine record shows `preparation_state: stale_after_failure`. Evidence (read only): `/home/user/wt/briefs/wave3/live-s1/edit-failure/failure-receipt.json` and `cli-stderr.txt`. The receipt does not record *why* verification failed: `state.install_unverified` is set but dropped.

## Outcome
A job that succeeds on a warm machine after earlier failed jobs is checkpointed and its output returned. Find the cause and fix it there. Candidates to rule in or out, with evidence:
- (a) **The verification budget:** on the success path `_canonical_installed` uses `self._remaining()` (the job's execution timer). After a long job that can be at or near 0, giving `install_unverified = "status_deadline_exhausted"` before `astrid engines status` even runs. The failure path is bounded by the paid lease instead (comment about 721).
- (b) **Re-preparation after `stale_after_failure`** (`generation.py` about 95, 163, 197; `machine.py` about 677, 1154-1209) does not record the installation it re-verified, so the snapshot no longer matches what `engines status` reports.
- (c) **The successful t2i in between** changed the installed state (the receipt or managed alignment refresh, per the `_checkpoint_installed` docstring), and edit's checkpoint compares against the stale snapshot.
- (d) **The edit template's preparation.**

Owner rules (binding):
- A failure that is not terminal keeps the machine.
- A success always returns its output.
- Never weaken a custody check: the checkpoint must still refuse a truly changed or unverified installation, with a different job, epoch or expired lease.

Also make the refusal name its reason in one line (carry `state.install_unverified` into the error and the receipt), so the next live failure explains itself.

## Tests (must fail before, pass after)
New `tests/packs/runpod/test_warm_sequence_checkpoint.py`, with the existing fakes in `tests/packs/runpod/test_machine.py`, `test_failed_job_keeps_warm.py` and `test_keep_warm_evidence.py`:
- (a) one claim and a fake provider. Replay: a job failing in execution, a job failing at admission, a success, then a second success. The fourth job's output is returned and the machine is kept, with no create;
- (b) the reproduction of the cause you identify (for example, a long fourth job that uses up its execution timer);
- (c) a truly changed installation at the checkpoint is still refused, with its reason in the message.

Proof, from `/home/user/wt/c-k1`, before and after:
```
TMPDIR=$PWD/.tmp-tests PYTHONPATH="$PWD:/home/user/wt/vibecomfy-fe92ac7" /home/user/astrid-agent.env/venv/bin/python -m pytest -q tests/packs/runpod/test_warm_sequence_checkpoint.py tests/packs/runpod/test_failed_job_keeps_warm.py tests/packs/runpod/test_keep_warm_evidence.py tests/packs/runpod/test_failure_receipt.py tests/packs/runpod/test_machine.py --basetemp=$PWD/.tmp-tests/pt
```
Then ruff (baseline 2117) and `git diff --check`. Save the diff to `/home/user/wt/briefs/wave3/machines-k1.diff`. In your report:
- name the cause in two sentences;
- say which of (a)-(d) you ruled out, and how;
- list every function you changed in `machine.py`, `generation.py` and `remote_placement.py`. Other lanes touch these files (M1 changes `RunPodMachine.claim`, M1 part c deletes the dead `RunPodGenerationPreparer`, and T9 changes success-path log collection), so keep the diff small and local.
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
