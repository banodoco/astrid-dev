difficulty: sol (S, write)

# M2: `generate` never rents and takes no paid flags; with no live machine it refuses in one line

**Repo:** Astrid. **Clone:** `/home/user/wt/c-m2` (branch `r13/machines-m2`, base `r13/machines` at `__BASE__`, which includes M1: a job attaches to a live claimed lease, never allocates, and no longer compares the job's preferences). Work in this clone only.

Read first (binding):
- `/home/user/wt/briefs/wave3/machines-design.md`: owner decisions O2 (generate only uses an existing machine), O3 (no automatic claim), O4 (no consent flag) and the target experience.
- `/home/user/wt/briefs/wave3/machines-plan.md`: rows **M2**, "Deletions" and "Merges".

## Manager rulings (follow these)
- **Delete from `generate`** (`astrid/core/generation/cli.py:_common_options` about 85-98, plus their wiring in `main`):
  - `--max-usd`, `--max-hourly-usd`, `--deadline`, `--offer-digest`, `--preparation-seconds`, `--execution-seconds`, `--idle-seconds`, `--capacity-timeout`, `--no-wait-for-capacity`;
  - the `paid` consent scope (`--consent user_env` stays);
  - **`--gpu` and `--datacenter`:** GPU, datacenter and volume are claim-time choices only.
- **Delete the SDK's paid controls** (`astrid/sdk/generation.py:_runpod_paid_controls` and the paid half of `_runpod_placement_policy`, about 257-345), and the job's `preferences` snapshot. M1 made the job path accept and ignore them; now nothing sends them. Remove M1's accept-and-ignore shims in `astrid/packs/runpod/adapter.py:prevalidate_task`, `machine.py` and `target_selection.py`, so there is one path.
- **The job's time:** a RunPod job has no per-job paid limits; its time is bounded by the lease's remaining lifetime and budget (M1). Execution and preparation timeouts default from the entry or recipe as today, never from flags the user must type.
- **With no live claimed machine,** `generate --placement runpod` refuses before admission, in one line: `no machine: run \`astrid machines claim\``, with zero provider calls. `generate describe` keeps its quote role (it may still accept `--gpu`/`--datacenter` to quote a claim), and it says that `machines claim` is how you rent.
- **MCP:** tools are generated from the generate parser (`astrid/mcp_server.py` about 570). Update `tests/test_mcp_generation_parity.py` (about 188-209) to the new property set; it pins the removed flags, so converting it is allowed.

## Tests (must fail before, pass after)
- (a) `generate` with any removed flag is a usage error naming `astrid machines claim`;
- (b) `generate --placement runpod` with no live machine refuses in one line, with zero provider calls;
- (c) a job on a claimed machine needs no paid flags, and the job's policy carries no `preferences`;
- (d) the SDK `generate(...)` accepts no paid keyword arguments;
- (e) the MCP parity.

Convert the tests that pass the removed flags or a per-job consent (O2–O4), and list each. Candidates:
- `tests/core/generation/test_cli.py`, `test_cli_gold_075b.py`, `test_runpod_engine_selection.py`, `test_sdk_entry_contract.py`, `test_target_launch.py`;
- `tests/sdk/test_generation_target.py`, `test_generation_workflow.py`, `test_modality_controls.py`, `test_runpod_front_door.py`, `test_generation_defaults_075a.py`;
- `tests/test_mcp_generation_parity.py`.

Proof, from `/home/user/wt/c-m2`, before and after:
```
TMPDIR=$PWD/.tmp-tests PYTHONPATH="$PWD:/home/user/wt/vibecomfy-fe92ac7" /home/user/astrid-agent.env/venv/bin/python -m pytest -q tests/core/generation/test_cli.py tests/core/generation/test_cli_gold_075b.py tests/core/generation/test_runpod_engine_selection.py tests/core/generation/test_sdk_entry_contract.py tests/core/generation/test_target_launch.py tests/sdk/test_generation_target.py tests/sdk/test_generation_workflow.py tests/sdk/test_modality_controls.py tests/sdk/test_runpod_front_door.py tests/sdk/test_generation_defaults_075a.py tests/test_mcp_generation_parity.py tests/packs/runpod/test_job_on_claimed_machine.py --basetemp=$PWD/.tmp-tests/pt
```
Then ruff and `git diff --check`. List (grep, don't fix) every script, skill, doc and integration test that passes a removed flag to `generate`; M9 and M10 handle them. Save the full diff to `/home/user/wt/briefs/wave3/machines-m2.diff`.

Out of scope: `machines claim` (M4), names (M3), idle (M5), the datacenter override (M6), list/show (M7), wording (M8), docs (M9), integration tests and scripts (M10).
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
