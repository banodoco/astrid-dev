# Fix: music refused, "canonical first-build semantic digest differs from admitted candidate"

You are a Codex worker with full access. Deploy Luna sub-agents (as many as are useful) for all reading, searching and mechanical checks. You judge and write the fix.

## What happened (live, Release 13 Stage 1, 12 Nov 16:21 UTC)
The music cell, Astrid entry `audio/ace_step_1_5_t2a_song` (ready template `ready_templates/audio/ace_step_1_5_t2a_song.py`), was refused before submission:
```
input_rejected: canonical first-build semantic digest differs from admitted candidate
```
This is VibeComfy's own check, at `vibecomfy/workflow_bundle.py:1722`. The candidate pinned VibeComfy `87d5e825`, which changed that template to declare its models. Since then `a8a7be7c` (your base) changed it again: every ready template's models are now explicit records. Raw CLI output: `/home/user/wt/briefs/wave3/live-s1/music-cli-stderr.txt`.

## Your clone
`/home/user/wt/c-musicfix`, VibeComfy, branch `r13/musicfix` at `a8a7be7c`.

## Outcome
1. **The cause, named.** Which admitted digest the first build is compared with, where that digest is stored (companion `.vibe.json`, the template index, or something Astrid sends), and why it went stale when the template's model declarations changed. Reproduce the refusal on CPU at `87d5e825` and at `a8a7be7c`, with no GPU and no ComfyUI server.
2. **One structural fix.** If the admitted digest is a stored copy of something derivable, it has two owners, so remove the copy or regenerate it from one source, with a check. If it's a legitimate pin, regenerate it with the repository's own tool, and make the template-change path regenerate it.
3. **A CPU check over every ready template:** its canonical first build matches its admitted candidate. The check must fail at `87d5e825` for the music template, and pass after the fix for all ready templates. It belongs in the default test run, so a template edit can never again ship this mismatch to a GPU. Name which other ready templates it caught, if any.

## Proof
- The new check fails before and passes after, on every ready template.
- These pass with no new failures against `a8a7be7c`: `tests/test_workflow_bundle.py`, `tests/test_ready_templates.py`, and the test file for the module you change. Known base failures (compare ids): `test_native_wan_animate_template_declares_frame_count_binding`; in `test_workflow_bundle.py`, the three `test_derived_template_live_identity_requires_package_lock_and_checkout[...]` cases, `test_v2_companion_keeps_generated_python_small_and_round_trippable`, `test_v2_source_contract_rejects_whole_file_integrity_mutations`; `test_porting_emitter.py::test_ideogram_fixture_native_boundary_is_materialized`; `test_ready_template_helpers.py::test_ready_template_root_supports_packaged_install`. If a workflow-bundle base failure turns out to share this cause, say so and fix it too.
- `python -m tools.refresh_template_index --check` and `git diff --check` pass.

## Rules
- Do not commit or push. Leave the change in the working tree.
- Never weaken, skip or delete a test. If an existing test pins the old behaviour on purpose, stop and report it.
- **No RunPod or paid services of any kind:** no calls to api.runpod.io, rest.runpod.io or any RunPod endpoint, no `astrid generate`, no `astrid machines`. The network proxy injects a real key, so a call spends real money. Package registries, GitHub and Hugging Face reads are allowed.
- No `.env`, credential files or `~/.codex`.
- **No full test suites,** only the files named above. The machine has 4 CPUs shared with other workers, and about 3 GB of disk is free. Use `TMPDIR=$PWD/.tmp-tests` and `--basetemp=$PWD/.tmp-tests/pt`, and delete them at the end.
- Start your Luna helpers at low effort.
- Python: `/home/user/astrid-agent.env/venv/bin/python` with `PYTHONPATH=$PWD`.
- No AI model or product names in code or comments. Stop after three failed attempts at the same thing, and report.

## Return
The cause in two sentences, the diff summary, before and after test ids, which other templates the new check caught, and anything that needs an Astrid change, with file and line.
