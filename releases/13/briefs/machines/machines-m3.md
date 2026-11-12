difficulty: terra (X, write)

# M3: machines have names; `generate --machine NAME` (or the one live machine) runs on that machine

**Repo:** Astrid. **Clone:** `/home/user/wt/c-m3` (branch `r13/machines-m3`, base `r13/machines` at `__BASE__`, which includes M1 and M2). Work in this clone only.

Read first (binding): `/home/user/wt/briefs/wave3/machines-design.md` (owner decision O5: "should machines have names, so we can say `astrid generate … bjork`"; O6: jobs queue on their machine) and `/home/user/wt/briefs/wave3/machines-plan.md` (rows **M3** and "Reuse: Names", "Queue").

## Outcome
1. **A claimed machine has a name.** `machines claim --name NAME` sets it. Without `--name`, a short memorable name is generated, unique among this account's machines (a word list in code, no network). It is stored on the lease record and shown in `lease_row` (`astrid/packs/runpod/machine.py:lease_row` about 1354).
2. **`generate … --machine NAME`** (name or id) pins the job to that machine. It reuses SDK `Placement.machine` (`astrid/core/generation/placement.py` about 71, 250) and the host pin check (`machine.py` about 590-599); add no new mechanism. `--machine` implies RunPod placement: no `--placement runpod` alongside it.
3. **A bare `generate` with no placement requested or saved, and exactly one live claimed machine, uses that machine** (manager ruling, owner-overrulable) and the first output line says `running on NAME`. With two or more, it refuses in one line listing their names and asking for `--machine`.
4. **A name that is gone or ended** refuses in one line, with the ended reason and the live names. It never rents a replacement. The detailed ended-machine diagnostic test (`test_machine.py`, `test_a_job_pinned_to_an_ended_machine_is_refused_with_the_reason`) keeps passing.
5. **Queue:** in Release 13 there is one lease per account, so the Runtime queue at concurrency 1 with the `gpu` key is the machine's queue. Add nothing; state it in your report.

## Tests (must fail before, pass after)
New `tests/core/generation/test_placement_machine_name.py`, plus cases in `tests/packs/runpod/test_machine.py`:
- (a) claim with `--name bjork`, then `generate --machine bjork` attaches;
- (b) a generated name is unique and is shown;
- (c) one live machine with a bare `generate` uses it, and prints `running on NAME`;
- (d) two live machines with a bare `generate` refuses, listing the names;
- (e) an ended name refuses with its reason and never allocates.

Proof, from `/home/user/wt/c-m3`, before and after:
```
TMPDIR=$PWD/.tmp-tests PYTHONPATH="$PWD:/home/user/wt/vibecomfy-fe92ac7" /home/user/astrid-agent.env/venv/bin/python -m pytest -q tests/core/generation/test_placement_machine_name.py tests/packs/runpod/test_machine.py tests/packs/runpod/test_job_on_claimed_machine.py tests/core/test_machines_claim.py tests/core/generation/test_cli.py --basetemp=$PWD/.tmp-tests/pt
```
Then ruff and `git diff --check`. Save the diff to `/home/user/wt/briefs/wave3/machines-m3.diff`.

Out of scope: idle (M5), datacenter (M6), list/show layout (M7, M8), docs (M9).
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
