# Tasks — Unblock live generation on RunPod and locally

[Plan](plan.md) · [Inputs](inputs.md)

Routes: `N` is the default, `X` very hard, `S` super hard ([run contract](../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings)). An `X` lead delegates reading, mechanical edits and running checks to `N` helpers and keeps the judgment and the final change.

**Rules for every task:**
- Start from the source identities in [inputs.md](inputs.md#source-identities) and re-check every cited line before editing; line numbers are at Agent `5eac07e3f`.
- Write each new test first and see it fail on the base.
- Run only the selectors named in the task. A check that fails follows the run contract: keep the first failure, repair the cause, rerun the same check.
- **CPU only** (owner, 8 Nov): no paid pod, no GPU, no real model download, no provider call, no credential read.
- Add no new `pack.extensions.*` key, `engine-index.json` row or backend descriptor; interim code uses existing seams only. Extension points belong to [Plan 17](../17-vibecomfy-extensibility/plan.md) and Plan 32.
- Only the Agent changes (U9 also repins the App). If a task finds it needs a VibeComfy, Runtime or lifecycle change, stop and report.
- A task that turns out much larger than its row stops and reports back; that work moves to [Plan 32](../32-generation-placement-targets/plan.md).
- Start only on the owner's go.

**Base and line.** One Agent candidate branch from `5eac07e3f` (record its name). Each task starts from the head the previous task on that branch left, and records its own head SHA. VibeComfy `e65f4941`, Runtime `b983b04` and lifecycle `f2948817` do not change.

**Check commands.** Set `ENV=<astrid-dev checkout>/plans/02-consistent-generation/env` and run `bash "$ENV/agent-setup.sh"` once from the Agent checkout root ([env README](../02-consistent-generation/env/README.md)). Then:
- `PYT <selectors>` means `bash "$ENV/agent-pytest.sh" -q <selectors>`.
- `PYT_POD <selectors>` is for the pod-path harness. `agent-pytest.sh` wipes the environment, and `tuple_sources` (`tests/integrations/test_runpod_host_endpoint_r5.py:33`) needs three more variables. Its source gate (`remote_placement.py:177-190`) needs clean checkouts at the pinned Runtime and VibeComfy commits, which setup already fetched. `LC` is a clean runpod-lifecycle checkout at `f2948817`:

```text
E="$(pwd -P).env"; env -i PATH="$E/venv/bin:$(cat "$E/uv-dir"):/usr/local/bin:/usr/bin:/bin" HOME="$E/home" TMPDIR="$E/tmp" XDG_CACHE_HOME="$E/cache" LANG=C.UTF-8 PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$E/vibecomfy" VIBECOMFY_SOURCE="$E/vibecomfy" ASTRID_RUNTIME_CHECKOUT="$E/runtime" ASTRID_VIBECOMFY_CHECKOUT="$E/vibecomfy" ASTRID_TEST_LIFECYCLE_CHECKOUT="$LC" "$E/venv/bin/python" -m pytest -q -p no:cacheprovider <selectors>
```

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| [U1](#u1-cpu-test-of-the-real-pod-path) CPU test of the real pod path, every default slot and h3_av | X | — | New `tests/integrations/test_runpod_slot_path_cpu.py`; `tests/core/generation/test_cli_gold_075b.py` (the voice STOP only) | `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py`: red on the base for RunPod voice with "workflow-local model is not present locally"; every other case's result recorded | [ ] |
| [U2](#u2-interim-inventory-wire-and---align-checktrust) Interim: the pod's receipt rows reach readiness; one `--align check\|trust` flag | X | U1 | `astrid/packs/runpod/{adapter,remote_placement,generation}.py`, `astrid/core/execution/generic_host.py`, `astrid/packs/vibecomfy/local_server_engine.py`, `astrid/sdk/generation.py`, `astrid/core/generation/cli.py`, and their tests | U1 RunPod voice green; the receipt, URL and refusal nodes below; attached voice passes with `trust`, fails with `check` | [ ] |
| [U3](#u3-sound-effects-runs-like-any-other-slot) Sound effects runs like any other slot | N | U2 (same SDK and CLI files) | `astrid/sdk/generation.py` (`_refuse_runpod_foley` and its calls), `astrid/core/generation/cli.py:405-407`, and the tests that pin the refusal | U1 sfx case green on RunPod and attached, video uploaded and audio fetched over `/view`; the flipped nodes below; `git grep` finds no refusal | [ ] |
| [U4](#u4-h3_av-like-everything-else-minimax-h3-the-video-default) h3_av reaches the pod like everything else; MiniMax H3 is the video default | N | U3 (same SDK file) | `astrid/packs/h3_av/{cli.py,actions/transform/run.py}`, `astrid/packs/runpod/remote_placement.py` (`run_remote_placement` only), `astrid/sdk/generation.py` (`_DEFAULT_ENTRIES`, video resolution), `astrid/packs/generation/{pack.yaml,actions/generate_video/STAGE.md}`, and their tests | U1 h3_av case green on RunPod; the default-video nodes below; no h3 pod command remains (grep) | [ ] |
| [U5](#u5-delete-the-legacy-second-runpod-route) Delete the legacy second RunPod route | N | U4 | `astrid/packs/vibecomfy/actions/run/run.py` (runpod_route, endpoint_checkout), `astrid/packs/vibecomfy/endpoint_checkout.py`, `astrid/core/generation/backends/registry.py` (`resolve_workflow_descriptor` legacy branch), `astrid/sdk/generation.py` (`_bind_runpod_preparation`, `workflow(placement=)`), and their tests | No caller remains (grep); U1 and `test_runpod_engine_selection.py` stay green | [ ] |
| [U6](#u6-models-on-the-storage-volume) Models on the storage volume: downloaded once, not per pod | N | U4 (same `remote_placement.py`) | `astrid/packs/runpod/remote_placement.py` (`prepare_claimed`, `_install`), `astrid/packs/runpod/generation.py` (`prepare_retained_generation`), and their tests | The install command carries the volume cache root only when a volume is saved; the existing cache nodes stay green | [ ] |
| [U7](#u7-reuse-a-live-pod-for-the-next-job) Reuse a live pod for the next job | X | U2, U6 (same `adapter.py`, `generation.py`) | `astrid/packs/runpod/adapter.py` (`TargetProviderBindings.get`), `astrid/packs/runpod/target_selection.py` (reuse window ~436-452), and their tests | Two sequential generates on one engine use one claim and one install (U1 case); the reuse nodes below; no orphaned pod | [ ] |
| [U9](#u9-land) Land | N | U1–U7, R, owner's go to promote | App candidate; destination mains; astrid-dev completion PRs for Plans 02 and 06 | Mains equal the tested and reviewed SHAs; the App pin check passes; the completion PRs are merged | [ ] |
| R Review rounds (at most 2, owner-agreed) | S | U1–U7 | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; publishing or closing waits for them | [ ] |

**U8 (live proof). Deferred:** the real-GPU proof moves to the GPU-tests plan that follows this plan. It is written after Plan 33 completes on CPU and runs before [Plan 32](../32-generation-placement-targets/plan.md). The owner decided on 8 Nov that this plan is CPU only; see [inputs.md](inputs.md#owner-decisions). U9 does not wait for it.

If a CPU case shows another controller-versus-pod bug that needs more than the wires listed here, stop and move the RunPod route to Plan 32's remote-machine model instead of adding another wire.

## U1 CPU test of the real pod path

**Outcome:** one CPU test that drives every default slot and h3_av through the real RunPod host bind, so a controller-versus-pod bug shows up on CPU instead of on a paid pod.

**Input:** the existing harness `tests/integrations/test_runpod_cpu_path.py::test_cpu_runpod_http_journey`, which already drives the real SDK, Runtime, host, lease owner and `EngineBridge`. Its doubles sit only at HTTP I/O (`ProviderHTTP`, line 186). It uses a synthetic `cpu-image` entry (lines 435-484). **Deliverable:** the new file `tests/integrations/test_runpod_slot_path_cpu.py`, with `pytestmark = pytest.mark.integration`. **Authority:** CPU only.

**Delegate to N helpers:** extracting the `ProviderHTTP` and fixture setup into a shared helper (or importing it), building each slot's stand-in schema, and running the checks.

1. Reuse `ProviderHTTP` and the fixtures `real_runtime` (`tests/conftest.py:45`) and `tuple_sources`. The stand-in ComfyUI serves `/object_info`, `/prompt`, `/history` and `/view`, plus `/upload/image` for media.
2. Build the stand-in's object_info from real node schemas, not invented ones: VibeComfy's packaged offline cache `vibecomfy/porting/cache/object_info/` (for example `comfy_core@runpod-snapshot.json`, `AILab_QwenTTS@runpod-snapshot.json`, `ComfyUI-HunyuanVideo_Foley@source-b94f7ac.json`), and, for H3, `tests/fixtures/h3_cpu/object_info_h3_runpod_graph_closure.json`. Serve only the classes each workflow uses.
3. Parametrize over `sorted(generation._DEFAULT_ENTRIES)` (image/t2i, image/edit, audio/tts, audio/music, audio/sfx), plus `h3` with the Matrix request (desk `merge-run/live/h3av/request.v2.json`, a 57-frame CPU stand-in clip), plus local-managed voice (the managed target from `tests/packs/vibecomfy/test_installed_child_path.py::test_installed_qwen_managed_child_path`). Use the real ready templates. Keep model files absent on the controller, and make the stand-in pod's install receipt list them.
4. For each case, assert the outputs come back over `/view` and that the task settles. For sfx, also assert that the source video was uploaded to the stand-in. For the attached-voice STOP in `test_cli_gold_075b.py:274-280` (`AUTO_ASSET_REFUSALS`), replace the comment with an assertion: under `--align check` it fails with the existing message, and U2 adds the `trust` case.
5. Record each case's result on the base in the commit body. The expected reds are RunPod voice ("workflow-local model is not present locally", M-72), sfx (`foley_runpod_unsupported`) and h3_av (see U4). Music has never produced an output live, so record its CPU result rather than assuming it.

**Proof:** `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py` (red as recorded) and `PYT tests/core/generation/test_cli_gold_075b.py::test_auto_dry_run_resolves_the_slot_default`.

## U2 Interim inventory wire and `--align check|trust`

**Interim: Plan 32 T5 deletes it.** **Input:** WIP `e003778be` (donor; fetch steps in [inputs.md](inputs.md#source-identities)). Take its plumbing: the host pops and sets `ASTRID_TARGET_MODEL_ASSETS` (`generic_host.py` ~9413-9422, ~12205-12213), and `_live_preflight` takes a target custody argument. Take its tests. Do not take its inventory source or its receipt check. **Deliverable:** a reworked commit on the line. **Authority:** CPU only.

**Delegate to N helpers:** porting the WIP hunks, writing the test nodes and running the checks. The lead keeps the attestation check and the `trust` semantics.

1. **Inventory from the receipt, not the lock.** `RemotePlacement._canonical_installed` (`remote_placement.py:721-758`) already parses the pod's receipt with `engine_runner._parse_receipt`, which checks every model row's sha256, bytes and path against the plan (`engine_runner.py:938-950`). Keep the parsed `models` rows in memory on the prepared state (`RemoteRun` or `PreparedRunPodLease`), and split each `path` into subdir and name under `root/models`. Do not add them to `astrid.runpod.installed-snapshot.v1`, which is strictly validated.
2. **One host-owned document, not a circular check.** The WIP compares `binding["installed_receipt_sha256"]` with the value it was copied from. Instead, the host builds one JSON value after a successful bind: `{"mode", "comfy_url", "receipt_sha256", "models"}`. It sets it in the existing env channel only after it has popped any inherited value. The child (`local_server_engine.run_local_server`) refuses the document unless `comfy_url` equals its own `comfy_url` and `receipt_sha256` equals the endpoint binding's `installed_receipt_sha256`, as saved by the lease owner (`adapter.py` ~242).
3. **Refuse before the claim** when no engine lock covers the entry. `entries.runpod_engine` already refuses on dry runs (`test_runpod_engine_selection.py::test_uncovered_entry_refuses_before_any_task`). Check that the live path refuses before `prepare` too, so no paid install happens first.
4. **`--align check|trust`** on `astrid generate` (CLI and SDK), with `check` the default. The name is the one Plan 32 keeps.
   - `check`: today's behaviour, judged against the placement's inventory (RunPod: the receipt rows; managed: the model-root receipt; attached: this disk).
   - `trust`: VibeComfy's target custody is fed the workflow's own declared model rows. Approval then skips the presence check, which uses the existing mechanism (`workflow_bundle.py` ~2561-2607, `auxiliary_model_custody="target"`) with no VibeComfy change. The result JSON carries `"alignment": {"mode": "trust", "verified": false}`.
   - `trust` works on every placement.
5. If U1's local-managed voice case is red, carry the managed model-root receipt through the same document. Change nothing else.

**Proof:**
- `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py`: voice green on RunPod and local-managed.
- `PYT tests/core/generation/test_target_asset_declaration.py tests/core/generation/test_runpod_engine_selection.py tests/packs/runpod/test_generation_preparation.py tests/packs/vibecomfy/test_local_server_run.py`. These include the WIP's ported nodes, renamed to say what they check:
  - `test_runpod_bound_model_absent_locally_passes_as_available_on_target`;
  - `test_runpod_bound_model_missing_from_inventory_fails_approval` (it must name the place);
  - `test_local_comfy_url_without_inventory_keeps_the_local_disk_check`;
  - `test_host_inventory_channel_is_absent_for_local_and_strict_when_present`.
- Also these new nodes:
  - `test_inventory_is_the_parsed_receipt_rows_not_the_lock`;
  - `test_child_refuses_inventory_for_another_comfy_url`;
  - `test_child_refuses_inventory_with_a_different_receipt_sha`;
  - `test_uncovered_entry_refuses_before_prepare` (live path, `NoPodClient`).
- `PYT tests/core/generation/test_cli_gold_075b.py`: attached voice passes with `--align trust`, and fails with `--align check` and a fix that names `--align trust` and `generate align`.

## U3 Sound effects runs like any other slot

**Input:** the U2 head. **Code facts:** Foley's video is the template's `video_ref` input (`media_semantics='video'`, VibeComfy `ready_templates/audio/hunyuan_video_foley.py:36`). `apply_workflow_inputs` turns it into an asset (`entries.py:766-768`). It travels in the `managed_assets` archive and is uploaded with `upload_media` (`local_server_engine.py:323-334`). So it never uses the `source_video` input that the host (`generic_host.py:12215`) and child (`run.py:739-740`) reject; those two rejections stay. **Deliverable:** the refusal deleted. **Authority:** CPU only.

1. Delete `_refuse_runpod_foley` (`sdk/generation.py:307`), its three calls (1085, 1871, 1885) and the CLI pre-call (`cli.py:405-407`). Drop `foley_runpod_unsupported` from `REFUSALS` in `tests/core/generation/test_runpod_engine_selection.py:25`.
2. Flip these tests to positive assertions (resolves, a task is admitted with a target policy, no refusal):
   - `tests/sdk/test_generation_target.py::test_foley_runpod_refuses_before_policy_registry_or_admission`;
   - `tests/sdk/test_runpod_front_door.py::test_foley_runpod_refuses_before_owner_or_allocation`;
   - `tests/core/generation/test_cli.py::test_audio_cli_runpod_foley_refuses_before_task_admission`;
   - `tests/test_pack_gateway_routes.py::test_public_generate_audio_uses_audio_parser_and_preserves_runpod_refusal`;
   - the sound-effects branch of `tests/core/generation/test_cli_gold_075b.py::test_runpod_dry_run_resolves_the_slot_default`.
   
   Name each in the commit body.
3. If U2 ported the WIP's `test_runpod_vibecomfy_default_slots_bind_with_target_custody`, flip its final assertion so sfx is covered.

**Proof:**
- `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py`: the sfx case is green on RunPod and attached.
- `PYT` with the five flipped nodes, plus `tests/sdk/test_generation_target.py::test_public_local_foley_stages_video_submits_and_delivers_through_runtime` and `tests/packs/vibecomfy/test_local_server_media.py::test_video_is_staged_with_hash_check_and_same_namespace`.
- `! git grep -n "foley_runpod_unsupported\|_refuse_runpod_foley" -- astrid tests`.

## U4 h3_av like everything else; MiniMax H3 the video default

**Input:** the U3 head. **Code facts:**
- `generate video --entry h3 --target runpod` already sends `target_policy` into h3's single `run` stage. That stage goes through the host bind like every other workflow (`sdk/generation.py:1709-1711`, `transform/run.py:2830-2832`; `STAGES` has one `run`, ~2541-2547).
- h3's own pod route runs only when `--placement runpod` reaches `transform/run.py:1978-1980`. That happens through `astrid action run h3_av.transform` or the prepared parent (`transform/run.py:2936`). The public `astrid h3` gateway pins `--placement local` (`h3_av/cli.py:133`).
- The Matrix request (desk `merge-run/live/h3av/request.v2.json`) has one timeline video and no references. Compile therefore picks `native_h3_continuation` (`compile.py:342`, `reference_count == 0`), and its LoRA `minimax_h3_fl2v_turbo_8step` is in `packs/runpod/models.lock.json`. The `_refs` variant's ref2v LoRA is not in the lock. Record it as not covered until Plan 32 T2, and do not grow the lock.

**Deliverable:** one route for h3 and a video default. **Authority:** CPU only.

1. Delete `_run_remote_placement` (`transform/run.py:56-61`), its call (~1978-1980) and the `placement == "runpod"` inference at ~2936. Delete `run_remote_placement` and `Limits.from_env` (`remote_placement.py` ~1166-1195). Their spend limit comes from an environment variable, which bypasses paid consent. Keep `RemotePlacement.run`, `_run_job`, `_download`, `_release`, `manifest_command` and `_MANIFEST_SCRIPT`, which Plan 32 T5 generalizes. Add no new h3 code.
2. Update or delete the tests that exercise the deleted entry:
   - `tests/packs/runpod/test_remote_placement.py::test_transform_runpod_calls_the_wrapper`;
   - `tests/packs/runpod/test_remote_placement.py::test_run_remote_placement_reads_caps_from_env`;
   - `tests/packs/runpod/test_managed_source_root.py::test_installed_agent_uses_managed_root_without_env`;
   - `tests/packs/h3_av/test_operation.py::test_runpod_placement_without_prepared_worker_uses_the_remote_wrapper`;
   - the monkeypatched names in `tests/packs/h3_av/test_cli.py::test_plan_verb_equals_handwritten_and_does_not_call_execution`;
   - the monkeypatched names in `tests/packs/h3_av/test_planner.py::test_transform_dry_run_never_touches_runtime_or_worker_selection`.
   
   Record each in the commit body.
3. **Video default.** With no `--entry` and no `--model`, `generate video` given an H3 `request` and `asset_map` resolves to `h3` on every placement. `ltx-2.3` becomes explicit-only (add it to `_EXPLICIT_ONLY_ENTRIES`, `sdk/generation.py:36`). Prompt-only video keeps its refusal (`_prompt_only_video`, line 247). `--image-ref` with no entry refuses with guidance to `--entry h3`, until Plan 32 T6 gives h3 declared media inputs. This is the recommended answer to owner decision D1 in [inputs.md](inputs.md#genuine-owner-decisions); apply the owner's answer if it differs. Step 0: `git grep -n "ltx-2.3" tests` and list each test that asserts ltx as the selected default. Change only those, and name them in the commit body. `test_registry.py` catalog listings are not defaults; leave them.
4. Update the help text (`packs/generation/pack.yaml` ~1600, ~1697; `actions/generate_video/STAGE.md`). Note there that local H3 needs a source video or reference images.

**Proof:**
- `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py`: h3_av green on RunPod.
- `PYT tests/core/generation/test_h3_action_entry.py tests/core/generation/test_runpod_engine_selection.py tests/core/generation/test_ltx_t2v_catalog_template.py tests/packs/runpod/test_remote_placement.py tests/packs/h3_av/test_operation.py tests/packs/h3_av/test_cli.py tests/packs/h3_av/test_planner.py`.
- New nodes in `tests/core/generation/test_cli_gold_075b.py`:
  - `test_video_without_entry_resolves_to_h3` (for `auto` and `runpod --dry-run`);
  - `test_image_ref_video_without_entry_refuses_with_h3_guidance`.
- `! git grep -n "run_remote_placement\|_run_remote_placement" -- astrid tests`.

## U5 Delete the legacy second RunPod route

**Input:** the U4 head. **Deliverable:** one RunPod route for `vibecomfy.run`. **Authority:** CPU only.

1. Step 0, census: `git grep -n "endpoint_checkout\|checkout_from_profile\|read_host_workflow_execution_request\|_bind_runpod_preparation\|pending38"`. On `5eac07e3f` the tests that use them are:
   - `tests/core/generation/test_workflow_route.py`;
   - `tests/core/execution/test_workflow_endpoint_handoff.py`;
   - `tests/sdk/test_generation_workflow.py`;
   - `tests/sdk/test_runpod_front_door.py`;
   - `tests/core/generation/test_comfy_provenance_journey.py`;
   - `tests/core/generation/test_producer_result_recovery.py`;
   - `tests/core/generation/backends/test_vibecomfy_http_polling.py`.
   
   If the h3 prepared-worker route (`worker_qualification`, `prepared_worker`) still reaches `runpod_route` after U4, stop and report. Plan 32 T6 deletes prepared workers.
2. Delete `runpod_route` and `endpoint_checkout` (`run.py:709-726`, `1012-1036`), the legacy branch of `resolve_workflow_descriptor` (`registry.py` ~168-180), `_bind_runpod_preparation` (`sdk/generation.py:341`, no caller), and the `placement` parameter of `workflow()` (~922). U4 removed h3's use of `placement=`. Delete or narrow the tests from step 1, and name each in the commit body.
3. `comfy_wrap` and `comfyui` stay: [Plan 06](../06-packs/plan.md) PK-15B is held by owner ruling M06-4. So `_runpod_operation`'s `"engine": "comfyui"` (`sdk/generation.py:318`) stays valid.

**Proof:** `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py`, `PYT tests/core/generation/test_runpod_engine_selection.py tests/core/test_generation_backend_registry.py`, and the surviving files from step 1. Then a grep must find nothing: `! git grep -n "pending38\|_bind_runpod_preparation\|checkout_from_profile" -- astrid`.

## U6 Models on the storage volume

**Input:** the U4 head. **Code fact:** a verified, mounted model cache already exists. `astrid engines install --model-cache-root` (`astrid/core/engine_cli.py:48`) feeds `validate_model_cache_root` (`engine_runner.py:180-197`) and `model_downloader`. That downloader copies a verified cached row into `models/`, or downloads, verifies and publishes it to the cache. Entries are keyed by the full lock row (`model_downloader.py:173-177`). `scripts/pod_session.py:97-98,458` already uses it. **Deliverable:** the generate route uses it. **Authority:** CPU only.

1. When the saved RunPod preferences name a volume (`RunPodPreferences.volume_id` is not `None`; `target_selection.py` ~125-175), `prepare_retained_generation` passes `<mount_path>/astrid/engines/comfyui/models` to `prepare_claimed`. `_install` (`remote_placement.py:703-719`) then adds `--model-cache-root <that path>`. The directory name `comfyui` is the engine's future contribution key (Plan 32 T2). The rows inside are keyed by identity, so both of today's engines share one cache and merging them later forces no re-fill.
2. Leave models on container disk as they are, so the receipt's `models_root == root/models` (`installed_session.py:93`) and the container-disk free-space guard stay correct. Correct the "FUSE is ephemeral" comment (`remote_placement.py:54-59`) to say the volume holds only the model cache. The datacenter and storage pins (`remote_placement.py:52-53`) belong to h3's deleted route; delete them if nothing else uses them.

**Proof:**
- New nodes in `tests/packs/runpod/test_remote_placement.py`:
  - `test_prepare_claimed_install_uses_the_volume_model_cache_when_saved`;
  - `test_prepare_claimed_install_has_no_cache_without_a_volume`.
- The existing cache nodes: `PYT tests/core/generation/test_model_downloader.py::test_first_download_publishes_verified_atomic_cache_and_second_launch_rehashes tests/core/generation/test_model_downloader.py::test_verified_mounted_cache_is_copied_locally_without_network_or_cache_writes tests/core/generation/test_model_downloader.py::test_cache_key_binds_every_exact_lock_entry_field tests/core/generation/test_model_downloader.py::test_failed_writeback_cannot_publish_a_valid_cache_entry tests/core/generation/test_engine_runner.py::test_cache_binding_preserves_lock_models_local_receipt_readiness_and_sanity_order`.
- A tampered row is refused: `test_model_downloader.py` nodes `test_unsafe_mounted_cache_entries_fail_closed_without_network` and `test_cache_revalidates_mount_device_and_path_during_copy`.

**Limit:** each fresh pod still copies the rows from the volume to its container disk. U7's reuse avoids that copy for a warm pod. Whether the cache's directory checks accept RunPod's network volume is not provable on CPU; the GPU-tests plan proves it.

## U7 Reuse a live pod for the next job

**Input:** the U2 and U6 heads, on the same line. **Deliverable:** a later `generate` with its own paid consent runs on a live claim. **Authority:** CPU only.

**Delegate to N helpers:** the test nodes and the checks. The lead keeps the consent and lifetime rules.

1. **Provider signature.** `TargetProviderBindings.get` (`adapter.py:446-464`) keys on `[kind, engine, preferences]`, and the preferences include `idle_timeout_seconds` and `budget_cap_usd`. Key it on the custody fields only: provider account, image, volume id and mount, and GPU choices, plus the engine id. The engine id is the base-environment key that Plan 12 needs.
2. **Engine change.** When the signature differs only by engine and the retained pod is idle (no operation, no active invocation), release it through the existing owner before the new claim, instead of raising "target policy differs from the retained provider owner".
3. **Reuse window.** In `target_selection.py` ~446-449, a new invocation (different `invocation_id`, its own consent) may reuse a live claim whose remaining lifetime covers the new job's execution and idle seconds. Do not count preparation already done. The same-invocation refusal at ~450-452 stays.
4. The existing idle timeout (`warm_hold.py:27`, 1800 s) and PodGuard release the pod. If this needs more than these three changes, stop and move it to Plan 32 T5.

**Proof:**
- `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py`: a new case, two sequential image generates, one claim, one install, released at the end.
- New nodes:
  - `tests/packs/runpod/test_target_selection.py::test_new_invocation_reuses_live_claim_without_counting_preparation`;
  - `tests/packs/runpod/test_generation_preparation.py::test_retained_provider_ignores_idle_and_budget_preference_changes`;
  - `tests/packs/runpod/test_generation_preparation.py::test_engine_change_releases_idle_retained_pod_before_new_claim`.
- These existing nodes stay green: `PYT tests/packs/runpod/test_target_selection.py::test_refused_reuse_never_reaches_create_or_reconcile tests/packs/runpod/test_target_selection.py::test_denied_reuse_does_not_change_custody_or_extend_hold tests/packs/runpod/test_warm_session.py::test_reuse_cancels_stale_idle_only_after_fresh_consent tests/packs/runpod/test_warm_session.py::test_expired_idle_cannot_be_renewed_by_new_consent_after_restart tests/packs/runpod/test_warm_session.py::test_idle_expiry_uses_warmholds_and_preserves_volume`.

## U9 Land

**Input:** the reviewed Agent head after R, and App `-16` `2191d866f`. **Deliverable:** the tested tuple promoted, with Plans 02 and 06 completion PRs. **Authority:** the owner's explicit go to promote to main, under the [release workflow](../../skills/astrid-dev-release/SKILL.md); poms_packs `main` is already authorized (decision 4).

1. App `-17`: pin the final Agent and Runtime. Use `rendering.video-editor`, `rendering.end-spanning-layer` and `rendering.frame-overlay` from core (Plan 06 Decision 8 as amended; no effect deleted). Step 0: confirm in the Agent head that `astrid/packs/rendering` provides all three; if not, that move is a Plan 06 task, so stop. From the App checkout, run `npm ci`, `node scripts/installer/pin.mjs <Agent head SHA>`, `node scripts/installer/pin.mjs --check` and `node --import tsx --test scripts/installer/manifest.test.mjs` (both files exist at `2191d866f`).
2. Fast-forward Runtime, VibeComfy, lifecycle, Agent and App to the tested SHAs, and create poms_packs `main` from `2379ab5`. Never force-push.
3. Write the Plan 02 and Plan 06 completion PRs with this plan's CPU evidence. State that the real-GPU proof is deferred to the GPU-tests plan.

**Proof:** each destination `main` equals its tested SHA (`git rev-parse`); the App pin check and manifest test pass; the completion PRs are merged.
