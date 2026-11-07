# Tasks: consistent generation path

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

[Project explanation](plan.md) · [Inputs and branch rules](inputs.md) · [Current project status](../../README.md)

Routes: `N` is the default (including ordinary hard work), `X` very hard, `S` super hard; see the [run contract](../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings). Run only the checks named here, with the exact selectors given; never a whole suite. A check that fails follows the run contract: keep the first failure, repair the cause, rerun the same check. Start only on the owner's go.

Selectors marked **Step 0** were not found in the repositories and must be named from the place given before the task starts. If a Step 0 lookup finds nothing, record that in the task and drop the check; do not invent a selector.

`ENV` below is the [env/](env/README.md) folder of this plan's astrid-dev checkout: set `ENV=<astrid-dev checkout>/plans/02-consistent-generation/env` once. The scripts are not inside the product checkouts. Run them from the product checkout root: `bash "$ENV/agent-setup.sh"` once, then `bash "$ENV/agent-pytest.sh" -q <selectors>` (VibeComfy: `vc-setup.sh`, `vc-pytest.sh`). They build `<checkout>.env/` beside the checkout.

## Phase 1: land the producers (can start today, any OS)

| ID | Outcome | Route | Depends on | Done when | Done |
|---|---|---|---|---|---|
| [P1](#p1-vibecomfy) | VibeComfy donor `1b2e242` is on VibeComfy `main`; record the resulting SHA. | N | none | Focused checks below pass on the tested commit, and that exact commit is what lands (fast-forward, or record that the trees are equal). | [ ] |
| [P2](#p2-lifecycle) | Lifecycle donor `c47fa76` is on runpod-lifecycle `main`; record the SHA. | N | none | Focused checks below pass on the tested commit, and that exact commit is what lands (fast-forward, or record that the trees are equal). | [ ] |
| [P3](#p3-runtime-stop) | Runtime stop change `b005394` is on Runtime `pre-main`; record the SHA. | N | none | Focused checks below pass on the tested commit, and that exact commit is what lands (fast-forward, or record that the trees are equal). | [ ] |

### P1 VibeComfy

Base: `main` (frozen at `e2905d06` on 5 Nov 2026). Donor `1b2e242ce7396442c85395d3220a2481216b57c1`.

1. Freeze `main` and confirm the donor is fetchable (`git fetch origin 1b2e242ce7396442c85395d3220a2481216b57c1`).
2. On a fresh branch from `main`, `git merge --no-ff 1b2e242ce7396442c85395d3220a2481216b57c1`. Expect exactly one conflict, `template_index.json` (checked 5 Nov 2026). That file is generated, so do not hand-merge it (keeping both sides gives invalid JSON, and `tests/test_ready_templates.py:257` requires it to equal `build_template_index()`). Resolve by regenerating it on the merged tree with `python -m tools.refresh_template_index`, then `python -m tools.refresh_template_index --check` must pass (the same check as VibeComfy's `Makefile:182`, target `template-index`). Both Foley templates stay in the index: `audio/hunyuan_foley_v2a` from `main` and `audio/hunyuan_video_foley` from the donor. Delete neither.
3. Step 0: list which of the selectors below exist on the merged tree (`git ls-files tests`). `tests/test_installed_resources.py` and `tests/test_phase2_defaults.py` come from the donor. Drop and record any selector missing from both `main` and the donor.
4. Setup `bash "$ENV/vc-setup.sh"` from the VibeComfy checkout root, then run (this is the retained RI-V and QV list, plus the Foley template test on `main`):

```text
bash "$ENV/vc-pytest.sh" -q tests/test_ready_templates.py tests/test_template_roundtrip.py tests/test_comfy_version_compat.py tests/test_phase2_defaults.py tests/test_comfy_backend.py tests/test_target_model_bundle_custody.py tests/test_target_model_approval.py tests/test_schema_target_authority.py tests/test_workflow_bundle.py::test_bundle_compile_rejects_nested_reconciliation_and_model_presence tests/test_workflow_bundle.py::test_bundle_model_gate_checks_picker_metadata_and_requirements tests/test_workflow_bundle.py::test_bundle_model_gate_rejects_metadata_model_not_registered tests/test_installed_resources.py tests/test_installed_wheel_execution.py tests/test_packaging.py tests/test_packaged_ready_trust.py tests/test_repo_relative_path_installed.py tests/test_h3_canonical_fixture.py tests/test_h3_av_audio_output.py tests/test_hunyuan_foley_v2a.py
```

5. If a node fails, run the same node once on `main` (frozen) to classify it; a failure that also fails on `main` is reported, not fixed here.
6. Land through VibeComfy's normal reviewed process, only with the owner's go, by fast-forwarding `main` to the tested commit (a pull-request merge makes a new commit; if that is the only route, record that its tree equals the tested tree, or rerun the checks on the new `main`). Record the resulting `main` SHA in [inputs.md](inputs.md).

### P2 lifecycle

Base: `main` (frozen `db79345536985c701b7aff2eb5eec36667aae204`). Donor `c47fa76be6e7c0aa661d044a0de5b3b73f6fdbac`, which contains `96360a27a53c4608f780f7b370f747a2aa3c7ca8`. It is a fast-forward of `main` (checked 5 Nov 2026).

1. Setup: `uv venv -q --python 3.13 .venv && uv pip install -q --python .venv/bin/python -e '.[dev]'`. The `dev` extra brings in `pytest-asyncio` and `pytest-mock`, and `pyproject.toml` sets `asyncio_mode = "auto"`; async tests such as `test_fake_provider_and_pod_facade` (`tests/test_https.py:218`) need them.
2. Run, using `.venv/bin/python -m pytest -q`:

```text
tests/test_https.py
tests/test_engine_bridge.py
tests/test_session_engine_proxy.py::test_session_enable_binary_http_and_no_bearer_projection
tests/test_session_engine_proxy.py::test_session_enable_and_ws_auth_before_upstream
tests/test_session_engine_proxy.py::test_session_enable_rejects_invalid_conflicting_and_observation_claims
tests/test_session_engine_proxy.py::test_session_websocket_frames_ping_close_and_header_filtering
tests/test_session_engine_proxy.py::test_session_enable_transport_rejections_are_specific_and_sanitized
tests/test_session_engine_proxy.py::test_session_prompt_relay_never_retries_or_exposes_transport_secrets
tests/test_observation_policy.py
tests/test_engine_startup_config.py
tests/test_api.py
tests/test_provider_mounts.py
```

The three K27 regressions are inside `tests/test_https.py`: `test_completed_jobs_are_evicted_after_both_streams_reach_eof` (line 78), `test_sequential_commands_reuse_the_claim_job_capacity` (107) and `test_delete_cleans_output_after_exit_and_retires_record_on_next_start` (115), at `c47fa76`. `tests/test_session_engine_proxy.py` also contains a seventh session-proxy test, `test_session_upload_image_is_bounded_and_relayed_without_client_secrets` (line 164), which the retained list does not name; leave it out unless you want it.
3. No real provider, pod or GPU run. Land by fast-forwarding `main` to the tested commit (it is a fast-forward of `main`), with the owner's go. Record the SHA.

### P3 Runtime stop

Base: Runtime `pre-main` (frozen `9fc53b771134940aaac901e4cfc5d03c1db1a20a`). Donor `b005394b06602c84e2abd4ba7eec8fa2f1dd8e94`. Merges cleanly with `pre-main` (checked 5 Nov 2026); the change touches `astrid_runtime/cli.py`, `astrid_runtime/selected_source.py` and two test files.

1. Merge the donor onto a fresh branch from `pre-main`.
2. Setup: `uv venv -q --python 3.13 .venv && uv pip install -q --python .venv/bin/python -e '.[test]'`.
3. Run `.venv/bin/python -m pytest -q tests/test_astrid_product_down.py tests/test_local_cli.py`. These are the two test files the donor changes; if they are slow or broad, narrow to the nodes covering the changed stop and ownership behavior, found with `git diff pre-main...b005394 -- tests` (Step 0).
4. Do not take the other Runtime lines (CAS `1e60e3b`, lease `33e9195a`, custody `103f9780`); they are outside this plan.
5. Land on Runtime `pre-main` with the owner's go, by fast-forwarding to the tested commit (or record tree equality if the process makes a new merge commit); record the SHA.

## Phase 2: wait for Plan 01

| ID | Outcome | Route | Depends on | Done when | Done |
|---|---|---|---|---|---|
| [W1](#w1-installer-consent-gate) | Plan 01 is on Agent and App `pre-main`. | N | [Plan 01](../01-installer-consent/plan.md) | Both ancestry checks below succeed. | [ ] |

### W1 Installer Consent gate

Check, in an Agent checkout, that the Plan 01 donors are ancestors of `origin/pre-main`: `git merge-base --is-ancestor 6087e0fbe7e2bd45c9911ff5cf1093614d715863 origin/pre-main` and the same for `19229d2325879c12e01c6bcdc604fd743b158ece`; in an App checkout, for `e97450cff0ed570cfaa077369b28c269b562bd1e` and `9ddff8efbc9e914efbe04cb49da2648c4feb4db4`. On 5 Nov 2026 none were (see [inputs.md](inputs.md)). If Plan 01 lands under different commits, check for its recorded result in the [Plan 01 file](../01-installer-consent/plan.md) and use that.

## Phase 3: compose Agent (release workflow)

| ID | Outcome | Route | Depends on | Done when | Done |
|---|---|---|---|---|---|
| [C1](#c1-compose-pins) | Agent PINS `1608dbbf` is merged onto current Agent `pre-main` on a fresh candidate branch. | X | W1 | Merge commit exists; PINS ancestry holds; conflicts resolved without new behavior. | [ ] |
| [C2](#c2-repin-agent) | Agent pins the landed P1, P2 and P3 SHAs, and its locks and digests are regenerated; the App-side output is staged on A1's branch. | N | C1, P1, P2, P3 | Repin checks below pass. | [ ] |

### C1 compose PINS

1. Freeze Agent `pre-main` (it was `40a6fd7ecf9138c6d9861631096a79820dc4c9b1` on 5 Nov 2026; Plan 01 will move it). Create a fresh candidate branch from it and record the name. Fetch PINS from its lane (`git fetch https://github.com/banodoco/astrid-agent.git 1608dbbf7036ad3c3b2b5e10956a726921bd4f9f`).
2. Step 0: dry-run the merge to list conflicts (`git merge-tree --write-tree --name-only HEAD 1608dbbf7036ad3c3b2b5e10956a726921bd4f9f`). On 5 Nov 2026 there were 22 conflicting paths against an earlier `pre-main`: `generic_host.py`, `warm_hold.py`, `gateway/dispatch.py`, `asset_alignment.py`, `asset_gaps.py`, `entries.py`, `comfyui/recipe.linux-cu130.json`, `engine-index.json`, `runpod/pins.json`, `runpod/recipe.linux-cu130.json`, `target_selection.py`, `vibecomfy/environment.windows-nvidia.json`, `vibecomfy/pins.json`, `vibecomfy/recipe.windows-cu130.json`, `sdk/generation.py`, `pyproject.toml`, `runtime.lock.json`, `scripts/vibecomfy_pin.py`, and four test files (`test_engine_cli.py`, `test_engine_recipe.py`, `test_generate_align.py`, `test_target_selection.py`). The pin and digest files are regenerated in C2, so resolve them to either side and let C2 fix them.
3. `git merge --no-ff 1608dbbf7036ad3c3b2b5e10956a726921bd4f9f`. Keep both sides of code conflicts and add no behavior; a hunk where both sides change the same statement to different results is a stop: record it and ask. Keep `pre-main`'s Plan 01 changes.
4. Put the conflict list and resolution notes in the merge commit body.
5. Done check: `git merge-base --is-ancestor 1608dbbf7036ad3c3b2b5e10956a726921bd4f9f HEAD` succeeds.

### C2 repin Agent

All commands are from the Agent candidate root.

1. VibeComfy: `python scripts/vibecomfy_pin.py <P1 SHA>`. With no argument it prints the current pin; with a 40-character SHA it changes the pin.
2. Lifecycle: edit the `runpod-lifecycle @ git+https://github.com/banodoco/runpod-lifecycle.git@<sha>` line in `pyproject.toml` (line 83 on `pre-main` on 5 Nov 2026) to the P2 SHA.
3. Runtime: `python scripts/regenerate_runtime_pins.py --runtime-sha <P3 SHA> --agent-sha <candidate head> --runtime-checkout <path to a Runtime checkout at P3> --app-checkout <path to the A1 App branch checkout> --agent-checkout .` is a dry run that prints a diff; add `--apply` to write. The first four flags are required (the script is on Agent `pre-main`, not on PINS, so it is present after C1). `--apply` writes to both repositories: in Agent, `runtime.lock.json` and the Runtime-copied consumer files; in the App checkout, its `runtime.lock.json`, the same copied Runtime files and `public/install-manifest.json` with an interim `agent.sha` (script lines ~120 to 133). Point `--app-checkout` at a checkout of the fresh App branch from `pre-main` that A1 uses, and commit that App-side output on that branch as part of A1 (A1 then sets the final `agent.sha`). `runtime.lock.json` must end at the P3 SHA (`1608dbbf` has `b005394b06602c84e2abd4ba7eec8fa2f1dd8e94` at line 71 of that file). Step 0: read the script's usage first; if `--agent-sha` cannot be the candidate head before it exists, use the head of C1's merge commit.
4. Digests and locks: PINS carries Foley and QwenTTS node sources in `astrid/packs/runpod/pins.json` and `recipe.linux-cu130.json`, a hash-locked `requirements.linux-cu130.lock`, model-lock rows, and sha256 references in the three recipes (if one is the Linux `comfyui` recipe, [Plan 06](../06-packs/tasks.md#pk-15b-delete-the-comfy-packs) deletes it later; keep it until then), `environment.linux-cu130.json` and `engine-index.json`. If the landed VibeComfy `pyproject.toml` or `custom_nodes.lock` differ from what PINS locked against, regenerate the requirements lock with the command in its own header and recompute every referencing sha256 (`sha256sum <file>` of the changed file; macOS: `shasum -a 256 <file>`; `git grep -n` the old digest and update every hit). Confirm with `python -c "from astrid.core.generation.engine_recipe import load_recipe; [load_recipe(e, p) for e, p in (('comfyui','linux-x86_64-cu130'),('vibecomfy','windows-x86_64-cu130'),('vibecomfy-h3','linux-x86_64-cu130'))]"` inside the check environment.
5. Done check: `astrid/packs/runpod/pins.json` `vibecomfy` and `vibecomfy-h3` equal the P1 SHA; `runtime.lock.json` `source_commit` equals the P3 SHA; no pin points at a lane-only commit (each SHA is contained in its repository's `main` or `pre-main`).

## Phase 4: port DEFAULTS

| ID | Outcome | Route | Depends on | Done when | Done |
|---|---|---|---|---|---|
| [D1](#d1-merge-the-defaults-donor) | Donor `9d3bb248` is merged onto the C2 head, with the Foley default per Decision 2. | X | C2 | Merge commit; K-owned files unchanged from C2; Foley default in place. | [ ] |
| [D1b](#d1b-runpod-dry-run) | `--target runpod --dry-run` resolves each default. | X | D1 | Rehearsal on the D1 head shows each slot resolving; edits stay in the named files. | [ ] |
| [D2](#d2-cli-gold-test) | `test_cli_gold_075b.py` exists and passes. | N | D1b | The CLI-GOLD test passes. | [ ] |
| [D3](#d3-installed-package-test) | The installed-package test exists under `tests/installed/`. | X | D2 | The test is written and committed; it is run in V3. | [ ] |

### D1 merge the DEFAULTS donor

1. Fetch `9d3bb24831676cbfc2a0d3dd1c7769f1937569c3` from the Agent repository and `git merge --no-ff` it onto the C2 head. Keep PINS-side bytes for the pin and recipe files: after the merge, `git diff <C2 head> HEAD -- astrid/packs/runpod astrid/packs/comfyui astrid/packs/vibecomfy astrid/packs/engine-index.json runtime.lock.json` must print nothing.
2. Step 0: list conflicts first. Against `pre-main` the donor alone had nine on 5 Nov 2026: `generic_host.py`, `warm_hold.py`, `gateway/dispatch.py`, `core/generation/preflight.py`, `runpod/target_selection.py`, `sdk/generation.py`, `test_generate_align.py`, `test_generate_target_journey.py`, `test_target_selection.py`. Keep both sides; add no behavior except step 3.
3. Foley default (Decision 2). Take the donor side for sound effects: the default is the locked template `audio/hunyuan_video_foley`. Do not change Agent `pre-main`'s explicit-only set: `astrid/sdk/generation.py` line 36 (`_EXPLICIT_ONLY_ENTRIES = frozenset({"hunyuan-foley-local", "audio/hunyuan_foley_v2a"})`, from commit `8395174a5`) keeps `hunyuan-foley-local` and `audio/hunyuan_foley_v2a` explicit-only, so only an explicit request reaches them. With no Foley installed, `generate audio` for sound effects on `auto` must fail with guidance and never fall back to another route. The RunPod refusal for Foley (`_refuse_runpod_foley`, which arrives with PINS at `astrid/sdk/generation.py` line 183; it is not on `pre-main`) stays unchanged; removing it is outside this plan.
4. Put the merge order, conflict list and the Foley choice in the commit body.

### D1b RunPod dry run

Why: in the retained run the image-on-RunPod dry run returned `input_rejected` and the other slots were "gated, not exercised" (`inputs/D076.REPORT.md:52`), and the DEFAULTS card (GOAL 3) calls this the only new behaviour. The donor head `9d3bb248` does not settle it, so it is a task.

1. Step 0: rehearse the CLI on the D1 head. For each slot in the D2 table run `python -m astrid generate ... --target runpod --dry-run --json` with the flags D2 lists, and record the exit status and JSON for each. Record which slots do not resolve and why.
2. Make `--target runpod --dry-run` resolve each default (entry and workflow in the JSON, no task admitted, no pod, no credential read). Edit only `astrid/sdk/generation.py`, `astrid/core/generation/{entries,cli,preflight}.py` and `models.yaml`. Touch no K-owned file. The sound-effects slot is the exception: its RunPod target keeps the existing Foley refusal (D2 asserts it).
3. Put the rehearsal results and each change in the commit body. D2's CLI-GOLD test then asserts the result for every slot.

### D2 CLI-GOLD test

Write the new file `tests/core/generation/test_cli_gold_075b.py` (never `pytest.skip`). Each case is a subprocess `python -m astrid generate ...` with an empty working directory and an environment of only `PATH`, `HOME`/`TMPDIR`/`XDG_CACHE_HOME` under `tmp_path`, `PYTHONNOUSERSITE=1`, plus the test process's `PYTHONPATH` and `ASTRID_RUNTIME_CHECKOUT`; no RunPod key. Assert that every flag you use appears in the subcommand's `--help`. RunPod dry-run flags in the earlier rehearsal were `--consent paid --max-usd 1 --deadline 2099-01-01T00:00:00Z`.

| Slot | Entry | Workflow or action | `--target auto` and `--target runpod --dry-run --json` |
|---|---|---|---|
| image | `qwen-image-2.1-turbo` | `image/qwen_image_2_1_turbo` | exit 0; entry and workflow appear in the JSON |
| edit | `qwen-image-2.1-turbo-edit` | `edit/qwen_image_2_1_turbo_edit` | same |
| video with references | `h3` | action `h3_av.transform` | same; copy the argv from `tests/core/generation/test_h3_action_entry.py::test_public_h3_cli_and_sdk_preserve_the_same_producer_local_inputs` |
| voice | `audio/qwen3_tts_custom_voice` | same id | same |
| music | `audio/minimax_music_3` | same id | same |
| sound effects | `audio/hunyuan_video_foley` (Decision 2) | its VibeComfy workflow | `auto`: resolves; `runpod`: non-zero exit with the existing refusal and no task admitted |

Also assert: `generate list --json` contains all six entry ids and `generate describe --entry <id> --json` exits 0 for each; no result names Z-Image, LTX, Wan or a hosted (fal) entry as selected; prompt-only `generate video "A lighthouse in gentle rain." --target <auto|runpod> --dry-run --json` exits non-zero, admits no task and substitutes no entry; with no engine installed and no RunPod configured, `generate image "A tiny blue lighthouse." --target auto --json` exits non-zero and its output contains `needs a local GPU or --target runpod`, and `generate audio --mode tts --input "text=The exact authored words." --target auto --json` contains the same text and names the Edge TTS option. Update the sound-effects row if the merged tree shows a different workflow id. The `--target runpod --dry-run` cells are asserted as D1b left them.

Existing tests that encode the old default may change an assertion only where it records the old sound-effects default; name each in the commit message.

### D3 installed-package test

Write the proof of Decision 10 as a new test under `tests/installed/` (Step 0: no `tests/installed` directory was found on `pre-main`; create it). It drives the installer entry `stage(manifest, root, data, copy_from=...)` in `astrid/installer/backend.py` (line 995 on `pre-main`; PINS and the DEFAULTS donor lack `copy_from`, so it arrives from `pre-main`). The manifest it passes needs pinned `tools.uv.version` and `tools.python.version` and the three SHAs `agent.sha`, `runtime.sha` and `vibecomfy.sha` (the last defaults to `VIBECOMFY_ENGINE_REVISION`), plus the optional `lifecycle` and `runpod` blocks when the candidate uses them. The retained INSTALLED-TEST card gives a disk peak of about 12 GB. What the test asserts is listed under V3. Never `pytest.skip`; if a stage would need a model download, the test fails with `model download needed: <stage>: <first error line>`. Writing it here keeps the head fixed during the proof phase.

## Phase 5: prove once on the final head

| ID | Outcome | Route | Depends on | Done when | Done |
|---|---|---|---|---|---|
| [V1](#v1-focused-checks) | The focused Agent checks pass on the D3 head. | N | D3 | PASS for each command, or only the nine excepted failures. | [ ] |
| [V2](#v2-linux-closure) | The Linux x86_64 closure passes. | N | D3, Linux environment | PASS. | [ ] |
| [V3](#v3-installed-package-proof) | The installed-package test from D3 passes (Decision 10). | N | D3 | PASS. | [ ] |

Record, for each, the exact command, the candidate SHA, the inputs and the inner exit status ([run contract](../../skills/astrid-dev-shared/run-contract.md#checks-and-failure-repair)). Do not claim a pass for a check not run.

### V1 focused checks

Run from the Agent candidate root. Set up once with `bash "$ENV/agent-setup.sh"`. `GEN_DESELECT_FILE` is `"$ENV/shared-failure-exceptions.txt"` (nine owner-approved shared failures; Decision 11).

```text
GEN_DESELECT_FILE="$ENV/shared-failure-exceptions.txt" bash "$ENV/agent-pytest.sh" -q tests/core/generation/test_cli.py tests/core/generation/test_entries.py tests/core/generation/test_generate_target_journey.py tests/core/generation/test_h3_action_entry.py tests/core/generation/test_preflight.py tests/sdk/test_generation_source_retention.py tests/sdk/test_generation_target.py tests/core/generation/test_engine_recipe.py tests/core/generation/test_engine_runner.py tests/core/generation/test_engine_bootstrap.py tests/core/generation/test_engine_cli.py tests/core/generation/test_release_python.py tests/test_installer_wheel.py tests/packs/runpod tests/integrations/test_runpod_cpu_path.py tests/integrations/test_runpod_host_endpoint_r5.py tests/core/generation/test_generate_align.py tests/core/generation/test_model_root_binding.py tests/core/generation/test_engine_local_model_root.py tests/core/generation/test_engine_local_endpoint.py tests/core/generation/test_entry_readiness.py tests/core/generation/test_preflight_managed_fix.py tests/core/generation/test_preflight_installed_target.py tests/core/generation/test_targets.py
bash "$ENV/agent-pytest.sh" -q "tests/core/generation/test_generate_target_journey.py::test_public_image_command_registers_view_bytes_and_canonical_receipt[saved]"
bash "$ENV/agent-pytest.sh" -q "tests/core/generation/test_engine_runner.py::test_old_environment_identity_refuses_then_clean_root_installs_after_owned_stop"
GEN_DESELECT_FILE="$ENV/shared-failure-exceptions.txt" bash "$ENV/agent-pytest.sh" -q tests/core/generation/test_phase2_audio_discovery.py tests/sdk/test_generation_defaults_075a.py tests/core/generation/test_target_asset_declaration.py tests/core/generation/test_cli_gold_075b.py
bash "$ENV/agent-pytest.sh" -q tests/packs/vibecomfy/test_installed_child_path.py
```

Notes: the `[saved]` parameter, `tests/sdk/test_generation_defaults_075a.py` and `test_phase2_audio_discovery.py` exist only after the DEFAULTS donor is merged (D1), so they cannot be found on `pre-main` or on PINS alone. `tests/packs/vibecomfy/test_installed_child_path.py::test_installed_qwen_managed_child_path` and the engine-runner node arrive with PINS. Step 0: confirm each selector exists on the candidate with `git grep`; a node missing there means a merge dropped it. Shared failures outside the nine: run the node once on the frozen `pre-main` to classify it, then report it (Decision 11).

Also check the K-owned bytes (D1 step 1) and that the pins still match C2. The head must not move between V1, V2 and V3; V3 only runs what D3 wrote.

### V2 Linux closure

Needs a Linux x86_64 environment (see [plan.md](plan.md#prerequisites)); about 6 GB of engine environment plus the checkout and virtual environments, so use at least 40 GB of disk. On a RunPod CPU pod, record the owner-approved spend and the stop. Run:

```text
bash "$ENV/agent-pytest.sh" -q tests/core/generation/test_closure_install_cpu.py
```

The test is `test_linux_x86_64_h3_environment_closure_before_model_stages`. It installs the `vibecomfy-h3` engine for `linux-x86_64-cu130` into fresh roots, CPU only, with `HF_HUB_OFFLINE=1`, stops after the `environment:comfy` stage, and imports the Foley and QwenTTS node packages (`HunyuanFoleyModelLoader`, `HunyuanFoleySampler`, `DACHunyuanVAEDecode`, `LoadDACHunyuanVAE`, `AILab_Qwen3TTSCustomVoice`). The retained run recorded an earlier version of this check cancelled with no verdict (exit 143); a cancellation is neither a pass nor a product failure. A result is valid only for the exact head tested.

### V3 installed-package proof

Run the test D3 wrote (`bash "$ENV/agent-pytest.sh" -q tests/installed`; about 12 GB of disk at peak). Outcome (Decision 10): a fresh, non-editable install of the candidate through the supported installer, with no checkout or user site visible to the installed program, shows: import origins of `astrid` and `vibecomfy` inside the installed environment; `vibecomfy.utils.find_repo_root()` raising `CheckoutRequiredError`; the `generate list` inventory with the six defaults; a dry run per default; and fail-closed guidance (`needs a local GPU or --target runpod`) with no engine and no RunPod. Together with `test_installed_qwen_managed_child_path` (the installed child driving a stand-in `/prompt`, `/history`, `/view` server), this is the proof. No weights, GPU, provider call or model download. If an installer stage needs a model download, stop and record `model download needed: <stage>: <first error line>`; never fetch weights. V3 writes no code; a failure that needs a code change returns to D3 and reopens the proof phase.

Not proven, by design: a full managed Qwen generation through readback. Record it as an open gap in the review.

## Phase 6: App repin

| ID | Outcome | Route | Depends on | Done when | Done |
|---|---|---|---|---|---|
| [A1](#a1-app-repin) | App's install manifest names the Agent head and its Runtime, on a pushed App branch. | N | D3, C2 | `--check` and the manifest test pass. | [ ] |

### A1 App repin

A1 needs only the Agent head pushed, so it runs before the review and R1 reviews both heads. From an App checkout on the fresh branch from App `pre-main` (with Plan 01) that C2 used for its App-side output:

```text
npm ci
node scripts/installer/pin.mjs <Agent head SHA>
node scripts/installer/pin.mjs --check
node --import tsx --test scripts/installer/manifest.test.mjs
```

`npm ci` comes first because `tsx` is a dev dependency (`pin.mjs` itself uses only Node built-ins and runs under plain `node`). `pin.mjs` rewrites only `public/install-manifest.json` (`agent.sha`, `runtime.sha`, `runtime.schema_digest`, `release`) and reads the Agent's `runtime.lock.json` from GitHub, so the Agent head must already be pushed to a candidate branch (it does not need to be promoted). `--check` is read-only. The Agent SHA must be 40 hex characters. The manifest test is `manifest pins its agent Runtime and schema digest` in `scripts/installer/manifest.test.mjs`. The branch carries C2's committed App-side output plus this pin. No App feature donor exists.

## Phase 7: review once

| ID | Outcome | Route | Depends on | Done when | Done |
|---|---|---|---|---|---|
| [R1](#r1-integrated-review) | One integrated completion review of the exact Agent and App heads. | — (completion-reviewer role; reviews have no route) | V1, V2, V3, A1 | Uncontested PASS, or the round budget is used and the owner decides. | [ ] |

### R1 integrated review

Use the completion-reviewer role from the [run contract](../../skills/astrid-dev-shared/run-contract.md#review-and-promotion-boundaries): one review after all scoped checks, at most five rounds, stop on an uncontested PASS. Give the reviewer the Agent and App candidate heads, the producer SHAs, the check outputs and these items to confirm: PINS and the DEFAULTS donor are ancestors; K-owned files are unchanged; the six defaults resolve as in Decision 2, including the `--target runpod --dry-run` results from D1b; no pin points at a lane-only commit; the Plan 01 changes survive; the Foley default and its fail-closed behavior; the App manifest names the Agent head; V1 to V3 results are attached to these exact heads; no GPU, provider call, model download or credential read appears in the logs, except V2's owner-approved RunPod CPU pod, whose recorded spend and stop are expected there. Real inference and Foley hardware qualification are listed as deferred, not dropped. A repair returns to the same iterate loop and reruns the failed check. The final rebase (RB1) is re-checked, not re-reviewed in full.

## Phase 8: rebase and promote

| ID | Outcome | Route | Depends on | Done when | Done |
|---|---|---|---|---|---|
| [RB1](#rb1-final-rebase) | The reviewed candidates sit on current `pre-main`, with proof carried forward or rerun. | N (X if conflicts) | R1 | Rebased heads recorded; affected checks pass; delta checked. | [ ] |
| [PR1](#pr1-promote) | The rebased heads are on `pre-main`. | N | RB1 | `pre-main` equals the rebased heads; receipts recorded. | [ ] |

### RB1 final rebase

1. Re-freeze each destination: Agent, Runtime and App `pre-main`; VibeComfy and runpod-lifecycle `main`. Record the SHAs.
2. Rebase the reviewed Agent and App candidates onto them. If nothing moved, record that and go to PR1.
3. If the rebase is clean, rerun only the checks whose inputs changed (a moved target invalidates only the proof that depends on it, per the [run contract](../../skills/astrid-dev-shared/run-contract.md#checks-and-failure-repair)) and record why the rest carries forward. A rebased Agent head has a new SHA, so push it and rerun A1's pin on it.
4. If it conflicts, resolve the conflicts (route X), rerun the affected checks, and ask the completion reviewer for a delta review of the resolution. This counts against R1's five-round budget; it adds no stage.
5. PR1 promotes the rebased heads by fast-forward. Never force-push.

### PR1 promote

Follow the release workflow's pre-main integration lane ([release skill](../../skills/astrid-dev-release/SKILL.md)): recapture each destination `pre-main` immediately before, and promote the exact rebased heads (Agent, then App) by ordinary fast-forward or create operations. Never force-push; never publish to Agent, Runtime or App `main`, `int/r1` or `release-1`. If a destination moved again, repeat RB1 for what moved. Only with the owner's explicit authority.

Order: Agent is promoted first, then App, so App's manifest never names an Agent head that is not yet on `pre-main`.
