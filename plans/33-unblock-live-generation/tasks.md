# Tasks — Unblock live generation on RunPod and locally

[Plan](plan.md) · [Inputs](inputs.md)

Routes: `N` is the default, `X` very hard, `S` super hard ([run contract](../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings)). An `X` or `S` lead delegates reading, mechanical edits and running checks to `N` helpers and keeps the judgment and the final change.

**Run state (2026-11-08):** run `plan33-2026-11-08-m1`, integration branch `int/33-unblock-live-generation` at `5eac07e3f`, plan pinned at astrid-dev `ccc421e` (plan files identical to `36ca5d9`). Progress rows above are current to 2026-11-08. The lead runs check-ins every 60 min until this plan's completion PR merges.

**Rules for every task:**
- Start from the source identities in [inputs.md](inputs.md#source-identities) and re-check every cited line before editing; line numbers are at Agent `5eac07e3f`.
- Write each new test first and see it fail on the base.
- Run only the selectors named in the task. A check that fails follows the run contract: keep the first failure, repair the cause, rerun the same check.
- **CPU only** (owner, 8 Nov): no paid pod, no GPU, no real model download, no provider call, no credential read.
- Add no new `pack.extensions.*` key, `engine-index.json` row or backend descriptor; interim code uses existing seams only. Extension points belong to [Plan 17](../17-vibecomfy-extensibility/plan.md) and Plan 32.
- Do not touch h3_av's `input_bundle`, receipts or stage graph; [Plan 32](../32-generation-placement-targets/plan.md) T6b deletes them.
- Only the Agent changes (U9 also repins the App). If a task finds it needs a VibeComfy, Runtime or lifecycle change, stop and report.
- A task that turns out much larger than its row stops and reports back; that work moves to [Plan 32](../32-generation-placement-targets/plan.md).
- Start only on the owner's go.

**Base and line.** One Agent candidate branch from `5eac07e3f` (record its name). The merge order is U1, U2, U3, U4, U6, U5, U7. Each task starts from the head the previous task left on that branch, and records its own head SHA. U5 and U7 both start from the U6 head; their scopes are disjoint, so U5 lands first and U7 rebases onto it. VibeComfy `e65f4941`, Runtime `b983b04` and lifecycle `f2948817` do not change.

**Check commands.** These use the worker-env scripts in the Agent checkout itself, `scripts/worker-env/` on `int/33-unblock-live-generation` (from 543c298; copies of astrid-dev [env/](../../env/README.md)). A single-repo cloud worker must run its own repository's code: auto mode refuses scripts cloned from another repository, even with an allow rule. Run each command by itself, from the Agent checkout root, with nothing chained onto it. Run `bash scripts/worker-env/agent-setup.sh` once. Then:
- `PYT <selectors>` means `bash scripts/worker-env/agent-pytest.sh -q <selectors>`.
- The Agent's `pyproject.toml` addopts deselect `integration` tests, so pass `-m integration` for any selector in an integration-marked file: `PYT -m integration <selectors>`. A later `-m` overrides the addopts one.
- `PYT_POD <selectors>` means `bash scripts/worker-env/agent-pytest-pod.sh <selectors>`, for the pod-path harness. It sets the extra variables `tuple_sources` (`tests/integrations/test_runpod_host_endpoint_r5.py:33`) needs.
- Before a run's first task, `bash scripts/worker-env/smoke.sh agent tests/core/generation/test_runpod_engine_selection.py` checks the environment.

`agent-setup.sh` also fetches runpod-lifecycle at the revision pinned in `astrid/packs/runpod/pins.json` into `<checkout>.env/lifecycle` (int/33 3e551fd), so no lifecycle worktree is made by hand.

CI's integration lane (`.github/workflows/lanes.yml:190`, `-m integration`) sets no `ASTRID_TEST_LIFECYCLE_CHECKOUT`. The new harness therefore errors there, as `test_runpod_cpu_path.py` already does, until a lane sets the variable.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| [U1](#u1-cpu-test-of-the-real-pod-path) CPU test of the real pod path, every default slot and h3_av | X | — | New `tests/integrations/test_runpod_slot_path_cpu.py`; `tests/core/generation/test_cli_gold_075b.py` (the voice STOP only) | `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py`: red on the base for RunPod voice with "workflow-local model is not present locally"; every other case's result recorded | [x] merged to int/33 at 16fd2f86c (PR-free --no-ff; independent verify 4f7349f matched 5 failed / 2 passed case by case) |
| [U2](#u2-interim-inventory-wire-and---align-checktrust) Interim: the pod's receipt rows reach readiness; one `--align check\|trust` flag | X | U1 | `astrid/packs/runpod/{adapter,remote_placement,generation}.py`, `astrid/core/execution/generic_host.py`, `astrid/packs/vibecomfy/local_server_engine.py`, `astrid/sdk/generation.py`, `astrid/core/generation/cli.py`, and their tests | U1 RunPod voice green; the receipt, URL and refusal nodes below; attached voice passes with `trust`, fails with `check` | started 2026-11-08 20:57Z: session `session_011EzfW1GR1a3Hb33owbdPin` (X, claude-sonnet-5-5), from int/33 at 16fd2f86c; in progress. Also: local-managed voice (same error as RunPod voice) must go green or be shown a test-setup artifact |
| [U3](#u3-sound-effects-runs-like-any-other-slot) Sound effects runs like any other slot | N | U2 (same SDK and CLI files) | `astrid/sdk/generation.py` (`_refuse_runpod_foley` and its calls), `astrid/core/generation/cli.py:405-407`, and the tests that pin the refusal | U1 sfx case green on RunPod and attached, video uploaded and audio fetched over `/view`; the flipped nodes below; `git grep` finds no refusal | not started; waits on U2 (2026-11-08) |
| [U4](#u4-h3_av-like-everything-else-minimax-h3-the-video-default) h3_av reaches the pod like everything else; MiniMax H3 is the video default | N | U3 (same SDK file) | `astrid/packs/h3_av/{cli.py,actions/transform/run.py}`, `astrid/packs/runpod/remote_placement.py` (`run_remote_placement` only), `astrid/sdk/generation.py` (`_DEFAULT_ENTRIES`, video resolution), `astrid/packs/generation/{pack.yaml,actions/generate_video/STAGE.md}`, and their tests | U1 h3_av case green on RunPod; the default-video nodes below; no h3 pod command remains (grep) | not started; waits on U3 (2026-11-08); also: fixture provenance says vibecomfy 01f38461, pin is e65f4941 |
| [U5](#u5-delete-the-dead-runpod-preparation-binder) Delete the dead `_bind_runpod_preparation` | N | U6 (merge order) | `astrid/sdk/generation.py` (`_bind_runpod_preparation` only) | No caller or definition remains (grep); `test_runpod_engine_selection.py` stays green | not started; waits on U6 (2026-11-08) |
| [U6](#u6-models-on-the-storage-volume) Models on the storage volume: downloaded once, not per pod | N | U4 (same `remote_placement.py`) | `astrid/packs/runpod/remote_placement.py` (`prepare_claimed`, `_install`), `astrid/packs/runpod/generation.py` (`prepare_retained_generation`), the storage probe (`scripts/pod_storage_probe.py`, reused), and their tests | The install command carries the volume cache root, device and mount id only when a volume is saved; the existing cache and probe nodes stay green | not started; waits on U4 (2026-11-08) |
| [U7](#u7-reuse-a-live-pod-for-the-next-job) Reuse a live pod for the next job | S | U2, U6 (same `adapter.py`, `generation.py`); starts from the U6 head | `astrid/packs/runpod/adapter.py` (`TargetProviderBindings.get`), `astrid/packs/runpod/target_selection.py` (reuse window ~436-452), and their tests | Two sequential generates on one engine use one claim and one install (U1 case); the reuse nodes below; no orphaned pod | not started; waits on U2 and U6 (2026-11-08) |
| [U9](#u9-land) Land | N | U1–U7, R, owner's go to promote | App candidate; destination mains; astrid-dev completion PRs for Plans 02 and 06 | Mains equal the tested and reviewed SHAs; the App pin check passes; the completion PRs are merged | not started; waits on U1–U7, R, and the owner's go to promote (2026-11-08) |
| [U8](#u8-music-runs-on-the-pods-comfyui) Music runs on the pod's ComfyUI: find which pin is stale | N | U1 (runs in parallel with U2) | diagnosis only: VibeComfy and runpod-lifecycle pins and the pod snapshot's CLIPLoader schema; no fix until the stale pin is known | the stale pin named with evidence; the music case's first failing line recorded | started 2026-11-08 20:57Z: session `session_011EzfVzG9bhczmmdyjjnqGQ` (N, claude-haiku-5-5). Diagnosis done: the stale piece is the U1 stand-in's CLIPLoader snapshot, not the pins. Revised card in flight: serve CLIPLoader at the pod pin, PR into int/33 |
| R Review rounds (at most 2, owner-agreed); first focus: U7's paid-consent change | S | U1–U7 | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; publishing or closing waits for them | not started; waits on U1–U7 (2026-11-08) |

**U8 (live proof). Deferred:** the real-GPU proof moves to [Plan 34](../34-real-gpu-proof/plan.md), which follows this plan on CPU and runs before [Plan 32](../32-generation-placement-targets/plan.md). The owner decided on 8 Nov that this plan is CPU only; see [inputs.md](inputs.md#owner-decisions). U9 does not wait for it.

If a CPU case shows another controller-versus-pod bug that needs more than the wires listed here, stop and move the RunPod route to Plan 32's remote-machine model instead of adding another wire.

## U1 CPU test of the real pod path

**Outcome:** one CPU test that drives every default slot and h3_av through the real RunPod host bind, so a controller-versus-pod bug shows up on CPU instead of on a paid pod.

**Input:** the existing harness `tests/integrations/test_runpod_cpu_path.py::test_cpu_runpod_http_journey`, which already drives the real SDK, Runtime, host, lease owner and `EngineBridge`. Its doubles sit only at HTTP I/O (`ProviderHTTP`, line 186). It uses a synthetic `cpu-image` entry (lines 435-484). **Deliverable:** the new file `tests/integrations/test_runpod_slot_path_cpu.py`, with `pytestmark = pytest.mark.integration`. **Authority:** CPU only.

**Delegate to N helpers:** extracting the `ProviderHTTP` and fixture setup into a shared helper (or importing it), building each slot's stand-in schema, and running the checks.

1. Reuse `ProviderHTTP` and the fixtures `real_runtime` (`tests/conftest.py:45`) and `tuple_sources`. The stand-in ComfyUI serves `/object_info`, `/prompt`, `/history` and `/view`, plus `/upload/image` for media. Unlike today's stand-in, which accepts any prompt (`test_runpod_cpu_path.py:369-371`):
   - `/prompt` validates against the object_info it serves: every class is present, required inputs are set, and combo values are in the menu;
   - loader combos are filled from the stand-in pod's receipt rows, so a model that is not in the menu fails the way it would on a pod;
   - `/history` returns the real output keys for each output type (`images`, `audio`, and the video key the workflow's save node uses), so retrieve is exercised.
2. Build the stand-in's object_info from real node schemas, not invented ones: VibeComfy's packaged offline cache `vibecomfy/porting/cache/object_info/` (for example `comfy_core@runpod-snapshot.json`, `AILab_QwenTTS@runpod-snapshot.json`, `ComfyUI-HunyuanVideo_Foley@source-b94f7ac.json`), and, for H3, `tests/fixtures/h3_cpu/object_info_h3_runpod_graph_closure.json`. Serve only the classes each workflow uses.
3. Parametrize over `sorted(generation._DEFAULT_ENTRIES)` (image/t2i, image/edit, audio/tts, audio/music, audio/sfx), plus `h3` with the Matrix request, plus local-managed voice (the managed target from `tests/packs/vibecomfy/test_installed_child_path.py::test_installed_qwen_managed_child_path`). Use the real ready templates. Keep model files absent on the controller, and make the stand-in pod's install receipt list them. For h3, copy the request (desk `merge-run/live/h3av/request.v2.json`) into `tests/fixtures`, and synthesize its 57-frame, 24 fps, 1024x576 source clip with ffmpeg lavfi, following `tests/packs/h3_av/test_cpu_rehearsal.py:125`. The desk's asset path does not exist.
4. For each case, assert the outputs come back over `/view` and that the task settles. For sfx, also assert that the source video was uploaded to the stand-in. The attached-voice STOP in `test_cli_gold_075b.py:274-280` (`AUTO_ASSET_REFUSALS`) is already asserted in the default mode (lines 582-585); keep it. U2 adds the `check` and `trust` cases.
5. Record each case's result on the base in the commit body. The expected reds are RunPod voice ("workflow-local model is not present locally", M-72), sfx (`foley_runpod_unsupported`) and h3_av (see U4). Music has never produced an output live, so record its CPU result rather than assuming it.

**Proof:** `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py` (red as recorded) and `PYT tests/core/generation/test_cli_gold_075b.py::test_auto_dry_run_resolves_the_slot_default`.

## U2 Interim inventory wire and `--align check|trust`

**Interim: Plan 32 T5 deletes it.** **Input:** WIP `e003778be` (donor; fetch steps in [inputs.md](inputs.md#source-identities)). Take its plumbing: the host pops and sets `ASTRID_TARGET_MODEL_ASSETS` (`generic_host.py` ~9413-9422, ~12205-12213), and `_live_preflight` takes a target custody argument. Take its tests except the three `test_bound_release_*` nodes in `tests/packs/runpod/test_generation_preparation.py`, which test the rejected lock source. Do not take its inventory source or its receipt check. **Deliverable:** a reworked commit on the line. **Authority:** CPU only.

**Delegate to N helpers:** porting the WIP hunks, writing the test nodes and running the checks. The lead keeps the attestation check and the `trust` semantics.

1. **Inventory from the receipt, not the lock.** `RemotePlacement._canonical_installed` (`remote_placement.py:721-758`) already parses the pod's receipt with `engine_runner._parse_receipt`, which checks every model row's sha256, bytes and path against the plan (`engine_runner.py:938-950`). Keep the parsed `models` rows in memory on the prepared state (`RemoteRun` or `PreparedRunPodLease`), and split each `path` into subdir and name under `root/models`. Do not add them to `astrid.runpod.installed-snapshot.v1`, which is strictly validated.
2. **One host-owned document, checked in the host.** The WIP compares `binding["installed_receipt_sha256"]` with the value it was copied from. The child cannot read the lease record, so a child-side comparison would be circular as well. Instead:
   - the host compares, right after `bind()` returns, the prepared state's `installed["receipt_sha256"]` (rebuilt by `_canonical_installed` on every prepare, including reuse) with the binding's `installed_receipt_sha256` (`adapter.py` ~242), and refuses on a mismatch;
   - only then does it build one JSON value, `{"mode", "comfy_url", "models"}`, and set it in the existing env channel after popping any inherited value;
   - the child (`local_server_engine.run_local_server`) refuses the document unless its `comfy_url` equals its own.
3. **Refuse before the claim** when no engine lock covers the entry. `entries.runpod_engine` already refuses on dry runs (`test_runpod_engine_selection.py::test_uncovered_entry_refuses_before_any_task`). Check that the live path refuses before `prepare` too, so no paid install happens first. Use an explicit `entry='ltx-2.3'`, which stays valid after U4 changes the video default.
4. **`--align check|trust`** on `astrid generate` (CLI and SDK), with `check` the default. The name is the one Plan 32 keeps.
   - `check`: today's behaviour, judged against the placement's inventory (RunPod: the receipt rows; managed: the model-root receipt; attached: this disk).
   - `trust`: VibeComfy's target custody is fed the workflow's own declared model rows. Approval then skips the presence check, which uses the existing mechanism (`workflow_bundle.py` ~2561-2607, `auxiliary_model_custody="target"`) with no VibeComfy change. The result JSON carries `"alignment": {"mode": "trust", "verified": false}`.
   - `trust` works on every placement.
5. If U1's local-managed voice case is red, carry the managed model-root receipt through the same document. Change nothing else.

**Proof:**
- `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py`: voice green on RunPod and local-managed.
- `PYT tests/core/generation/test_target_asset_declaration.py tests/core/generation/test_runpod_engine_selection.py tests/packs/runpod/test_generation_preparation.py` and `PYT -m integration tests/packs/vibecomfy/test_local_server_run.py`. These include the WIP's ported nodes, renamed to say what they check:
  - `test_runpod_bound_model_absent_locally_passes_as_available_on_target`;
  - `test_runpod_bound_model_missing_from_inventory_fails_approval` (it must name the place);
  - `test_local_comfy_url_without_inventory_keeps_the_local_disk_check`;
  - `test_host_inventory_channel_is_absent_for_local_and_strict_when_present`.
- Also these new nodes:
  - `test_inventory_is_the_parsed_receipt_rows_not_the_lock`;
  - `test_child_refuses_inventory_for_another_comfy_url`;
  - `test_host_refuses_bind_whose_receipt_differs_from_the_prepared_install`;
  - `test_uncovered_entry_refuses_before_prepare` (live path, `NoPodClient`, explicit `entry='ltx-2.3'`).
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
3. **Video default.** With no `--entry` and no `--model`, `generate video` given an H3 `request` and `asset_map` resolves to `h3` on every placement. `ltx-2.3` becomes explicit-only (add it to `_EXPLICIT_ONLY_ENTRIES`, `sdk/generation.py:36`). Prompt-only video keeps its refusal (`_prompt_only_video`, line 247). `--image-ref` with no entry refuses with guidance to `--entry h3`, until Plan 32 T6b gives h3 declared media inputs. The owner decided this (M-79, Plan 33 D1 in [inputs.md](inputs.md#owner-decisions)). Step 0: `git grep -n "ltx-2.3" tests` and list each test that asserts ltx as the selected default. Change only those, and name them in the commit body. `test_registry.py` catalog listings are not defaults; leave them. Two tests change without naming ltx:
   - `test_runpod_engine_selection.py::SLOTS` includes `('video', 'i2v')` with an image. Add the new refusal's code (name it `video_entry_required`) to `REFUSALS` (line 25).
   - `test_uncovered_entry_refuses_before_any_task` (line 163) relies on i2v auto-resolving to ltx. Repoint it to an explicit `entry='ltx-2.3'`.
4. Update the help text (`packs/generation/pack.yaml` ~1600, ~1697; `actions/generate_video/STAGE.md`). Note there that local H3 needs a source video or reference images.

**Proof:**
- `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py`: h3_av green on RunPod.
- `PYT tests/core/generation/test_h3_action_entry.py tests/core/generation/test_runpod_engine_selection.py tests/core/generation/test_ltx_t2v_catalog_template.py tests/packs/runpod/test_remote_placement.py tests/packs/h3_av/test_operation.py tests/packs/h3_av/test_cli.py tests/packs/h3_av/test_planner.py`.
- New nodes in `tests/core/generation/test_cli_gold_075b.py`:
  - `test_video_without_entry_resolves_to_h3` (for `auto` and `runpod --dry-run`);
  - `test_image_ref_video_without_entry_refuses_with_h3_guidance`.
- `! git grep -n "run_remote_placement\|_run_remote_placement" -- astrid tests`.

## U5 Delete the dead RunPod preparation binder

**Input:** the U6 head. **Deliverable:** `_bind_runpod_preparation` (`sdk/generation.py:341`) deleted; it has no caller. **Authority:** CPU only.

The rest of the legacy route moves to [Plan 32](../32-generation-placement-targets/plan.md) T6b, which deletes prepared workers and so the route's last caller. That covers `runpod_route` and `endpoint_checkout` in `run.py`, `endpoint_checkout.py`, the legacy branch of `resolve_workflow_descriptor` and the `placement` parameter of `workflow()`. On `5eac07e3f`:
- `generic_host.py` imports `endpoint_checkout` at five sites (1400, 9412, 9795, 11697, 17156);
- h3's `legacy_prepared` route (`transform/run.py:1947-1952`) still calls `workflow(placement="runpod")`.

Deleting them here would touch both and unblocks nothing on the CPU candidate. `comfy_wrap` and `comfyui` stay in this plan: Plan 32 T2b owns their deletion (M-79).

**Proof:** `! git grep -n "_bind_runpod_preparation" -- astrid tests`, and `PYT tests/core/generation/test_runpod_engine_selection.py`.

## U6 Models on the storage volume

**Input:** the U4 head. **Code fact:** a verified, mounted model cache already exists. `astrid engines install --model-cache-root` (`astrid/core/engine_cli.py:48`) feeds `validate_model_cache_root` (`engine_runner.py:180-197`) and `model_downloader`. That downloader copies a verified cached row into `models/`, or downloads, verifies and publishes it to the cache. Entries are keyed by the full lock row (`model_downloader.py:173-177`). `scripts/pod_session.py:97-98,458` already uses it. **Deliverable:** the generate route uses it. **Authority:** CPU only.

1. When the saved RunPod preferences name a volume (`RunPodPreferences.volume_id` is not `None`; `target_selection.py` ~125-175), `prepare_retained_generation` passes `<mount_path>/astrid/engines/comfyui/models` to `prepare_claimed`. `_install` (`remote_placement.py:703-719`) then adds `--model-cache-root <that path> --model-cache-device <device> --model-cache-mount-id <mount id>`, as `scripts/pod_session.py:458-460` does. Without the device and mount id, `_CacheBinding` does not pin the mount, and a volume that failed to mount would silently cache onto container disk.
   - Obtain both values the way `pod_session.py` ~1056-1110 does: run `scripts/pod_storage_probe.py` on the claim before install, and keep the values out of logs.
   - Step 0: check that the probe source is available to `remote_placement` in an installed Agent. If it is not, move it into `astrid/packs/runpod/` unchanged. The directory name `comfyui` is the engine's future contribution key (Plan 32 T2). The rows inside are keyed by identity, so both of today's engines share one cache and merging them later forces no re-fill.
2. Leave models on container disk as they are, so the receipt's `models_root == root/models` (`installed_session.py:93`) and the container-disk free-space guard stay correct. Correct the "FUSE is ephemeral" comment (`remote_placement.py:54-59`) to say the volume holds only the model cache. The datacenter and storage pins (`remote_placement.py:52-53`) belong to h3's deleted route; delete them if nothing else uses them.

**Proof:**
- New nodes in `tests/packs/runpod/test_remote_placement.py`:
  - `test_prepare_claimed_install_uses_the_volume_model_cache_when_saved`;
  - `test_prepare_claimed_install_has_no_cache_without_a_volume`.
- The existing cache nodes: `PYT tests/core/generation/test_model_downloader.py::test_first_download_publishes_verified_atomic_cache_and_second_launch_rehashes tests/core/generation/test_model_downloader.py::test_verified_mounted_cache_is_copied_locally_without_network_or_cache_writes tests/core/generation/test_model_downloader.py::test_cache_key_binds_every_exact_lock_entry_field tests/core/generation/test_model_downloader.py::test_failed_writeback_cannot_publish_a_valid_cache_entry tests/core/generation/test_engine_runner.py::test_cache_binding_preserves_lock_models_local_receipt_readiness_and_sanity_order`.
- A tampered row is refused: `test_model_downloader.py` nodes `test_unsafe_mounted_cache_entries_fail_closed_without_network` and `test_cache_revalidates_mount_device_and_path_during_copy`.
- The probe stays green: `PYT tests/scripts/test_pod_storage_probe.py`.

**Limit:** each fresh pod still copies the rows from the volume to its container disk. U7's reuse avoids that copy for a warm pod. Whether the cache's directory checks accept RunPod's network volume is not provable on CPU; [Plan 34](../34-real-gpu-proof/plan.md) proves it. A cache hit is recorded as `action="downloaded"` (`model_downloader.py:585`), so the install receipt cannot show "copied, not downloaded". Plan 34 needs another signal, such as network bytes or the time of the install step.

## U7 Reuse a live pod for the next job

**Input:** the U6 head (which includes U2). **Deliverable:** a later `generate` with its own paid consent runs on a live claim. **Route S:** it changes paid-consent semantics, because a new invocation spends against a claim an earlier consent made. It is the first focus of the review. **Authority:** CPU only.

**Delegate to N helpers:** the test nodes and the checks. The lead keeps the consent and lifetime rules.

1. **Provider signature.** `TargetProviderBindings.get` (`adapter.py:446-464`) keys on `[kind, engine, preferences]`, and the preferences include `idle_timeout_seconds` and `budget_cap_usd`. Key it on the custody fields only: provider account, image, volume id and mount, GPU choices, `datacenter_id` and `credential_ref` (both in `RunPodPreferences`), plus the engine id. The engine id is the base-environment key that Plan 12 needs.
2. **Engine change.** When the signature differs only by engine and the retained pod is idle (no operation, no active invocation), release it through the existing owner before the new claim, instead of raising "target policy differs from the retained provider owner".
3. **Reuse window.** In `target_selection.py` ~446-449, a new invocation (different `invocation_id`, its own consent) may reuse a live claim whose remaining lifetime covers the new job's execution and idle seconds. Do not count preparation already done. The same-invocation refusal at ~450-452 stays.
4. The existing idle timeout (`warm_hold.py:27`, 1800 s) and PodGuard release the pod. If this needs more than these three changes, stop and move it to Plan 32 T5.

**Proof:**
- `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py`: a new case, two sequential image generates, one claim, one install, released at the end. It runs in one process. Reuse across two separate `astrid generate` processes is not proven on CPU, because `TargetProviderBindings` is in-process.
- **Limit:** a mixed session that switches between image (engine `comfyui`) and voice (`vibecomfy-h3`) still pays a new pod per switch, until Plan 32 T2b merges the engines.
- New nodes:
  - `tests/packs/runpod/test_target_selection.py::test_new_invocation_reuses_live_claim_without_counting_preparation`;
  - `tests/packs/runpod/test_generation_preparation.py::test_retained_provider_signature_changes_with_datacenter_or_credential`;
  - `tests/packs/runpod/test_generation_preparation.py::test_retained_provider_ignores_idle_and_budget_preference_changes`;
  - `tests/packs/runpod/test_generation_preparation.py::test_engine_change_releases_idle_retained_pod_before_new_claim`.
- These existing nodes stay green: `PYT tests/packs/runpod/test_target_selection.py::test_refused_reuse_never_reaches_create_or_reconcile tests/packs/runpod/test_target_selection.py::test_denied_reuse_does_not_change_custody_or_extend_hold tests/packs/runpod/test_warm_session.py::test_reuse_cancels_stale_idle_only_after_fresh_consent tests/packs/runpod/test_warm_session.py::test_expired_idle_cannot_be_renewed_by_new_consent_after_restart tests/packs/runpod/test_warm_session.py::test_idle_expiry_uses_warmholds_and_preserves_volume`.

## U9 Land

**Input:** the reviewed Agent head after R, and App `-16` `2191d866f`. **Deliverable:** the tested tuple promoted, with Plans 02 and 06 completion PRs. **Authority:** the owner's explicit go to promote to main, under the [release workflow](../../skills/astrid-dev-release/SKILL.md); poms_packs `main` is already authorized (decision 4).

1. App `-17`: pin the final Agent and Runtime. Use `rendering.video-editor`, `rendering.end-spanning-layer` and `rendering.frame-overlay` from core (Plan 06 Decision 8 as amended; no effect deleted). Step 0: confirm in the Agent head that `astrid/packs/rendering` provides all three; if not, that move is a Plan 06 task, so stop. From the App checkout, run `npm ci`, `node scripts/installer/pin.mjs <Agent head SHA>`, `node scripts/installer/pin.mjs --check` and `node --import tsx --test scripts/installer/manifest.test.mjs` (both files exist at `2191d866f`).
2. Fast-forward Runtime, VibeComfy, lifecycle, Agent and App to the tested SHAs, and create poms_packs `main` from `2379ab5`. Never force-push.
3. Write the Plan 02 and Plan 06 completion PRs with this plan's CPU evidence. State that the real-GPU proof is [Plan 34](../34-real-gpu-proof/plan.md).

**Proof:** each destination `main` equals its tested SHA (`git rev-parse`); the App pin check and manifest test pass; the completion PRs are merged.


## U8 Music runs on the pod's ComfyUI

**Outcome:** find which pinned component is stale. U1's independent run failed music with `CLIPLoader input type value 'minimax' is not one of the declared choices (pod-snapshot comfy schema lacks 'minimax')`, so the RunPod base ComfyUI may be older than the music workflow needs. **Route N, diagnosis only.** No fix until the stale pin is named.
