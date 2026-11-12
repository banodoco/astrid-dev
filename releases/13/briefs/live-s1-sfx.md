# Fix: SFX blocked before execution (CHOICE versus COMBO)

You are a Codex worker with full access. Deploy Luna sub-agents (as many as are useful) for all reading, searching and mechanical checks. You judge and write the fix.

## What happened (live, Release 13 Stage 1, RunPod RTX 5090, 12 Nov 16:03 UTC)
The SFX cell (ready template `ready_templates/audio/hunyuan_foley_v2a.py`, Astrid entry for Hunyuan Foley video-to-audio) prepared fine, then VibeComfy refused the run before submitting:
```
public_input_incompatible: public input 'node:11.model_path_name' type 'CHOICE' is incompatible with 'COMBO'
```
Also printed: `using live target schema for HunyuanFoleyModelLoader (11) because offline object-info identity did not resolve` (same for nodes 12, 14, 22).
The full failure bundle is in `/home/user/wt/briefs/wave3/live-s1/sfx-failure/`, including the declared logs, `generation.stdout.json` and `failure-receipt.json`.

## Your clone
`/home/user/wt/c-sfxfix`, VibeComfy, branch `r13/sfxfix` at `a8a7be7c`. This is the next VibeComfy pin for Release 13: every template declares its models as records.

## Outcome
1. **The cause, named:** where VibeComfy compares a public input's declared type with the target schema's type, and why `CHOICE` (VibeComfy's enum kind) is not treated as compatible with ComfyUI's `COMBO`. Fix it once, in the comparator or the type model, so every enum input works. Don't special-case this node.
2. **Why the offline object-info identity didn't resolve** for these four nodes, so VibeComfy fell back to the live schema. Either fix it, if it's a VibeComfy defect in this repo, or state exactly what's missing and where it should come from. The point: this mismatch should have been caught offline on CPU, not on a rented GPU. If a CPU check could have caught it, add that check (for example a test that type-checks every ready template's public inputs against its declared or offline schema).
3. **A regression test** that fails before the fix and passes after: the Foley template's `model_path_name` public input admits against a `COMBO` schema entry.

## Proof
- The new test(s) fail on `a8a7be7c` and pass after.
- These pass with no new failures against `a8a7be7c`: `tests/test_ready_templates.py`, and the test files for the module you change and its direct callers (name them). Known base failures: `test_native_wan_animate_template_declares_frame_count_binding` and seven in `test_workflow_bundle.py`/emitter/helpers. Compare against those ids.
- `python -m tools.refresh_template_index --check` and `git diff --check` pass.

## Rules
- Do not commit or push. Leave the change in the working tree.
- Never weaken, skip or delete a test. If an existing test pins the old behaviour on purpose, stop and report it.
- **No RunPod or paid services of any kind:** no calls to api.runpod.io, rest.runpod.io or any RunPod endpoint, no `astrid generate`, no `astrid machines`. The network proxy injects a real key, so a call spends real money. Package registries, GitHub and Hugging Face reads are allowed.
- No `.env`, credential files or `~/.codex`.
- **No full test suites,** only the files named above. The machine has 4 CPUs shared with other workers. Use `TMPDIR=$PWD/.tmp-tests` and `--basetemp=$PWD/.tmp-tests/pt`, and delete them at the end.
- Python: `/home/user/astrid-agent.env/venv/bin/python` with `PYTHONPATH=$PWD`.
- No AI model or product names in code or comments. Stop after three failed attempts at the same thing, and report.

## Return
The cause in two sentences, the diff summary, before and after test ids, and anything that needs an Astrid change, with exact file and line.
