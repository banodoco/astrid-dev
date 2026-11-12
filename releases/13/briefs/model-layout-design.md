# Model layout design (Fable, 12 Nov; owner direction attached)

## Owner direction (Hannah, 12 Nov)
- No shims and no interim steps: build the proper thing in Release 13. The shortcuts (symlinks) go.
- Models are declared once. Use the expected default (`ComfyUI/models`) unless changed, in one place, and never re-declared per run.
- People with an existing ComfyUI: their models stay where they are.
- Setup starts from the expectation that models are in the normal path. The agent can change that, in one place.

## Headline
The pinned ComfyUI (`6bfaacc6`) has `--models-directory`, which sets `folder_paths.models_dir` (`comfy/cli_args.py:259`, `folder_paths.py:19-22`). Both failing packs read `folder_paths.models_dir` directly: `hunyuan_foley.py:121,125,176,284` and `AILab_QwenTTS.py:318`. So one launch flag replaces the symlinks, the generated search-path file and the clean-source exemption.

## Concepts
- **Model declaration:** what is needed (relative path, bytes, sha256, source). Astrid's lock `destination` (`engine_recipe.py:460-500`) or a workflow's `subdir/name`.
- **Models directory:** the one directory ComfyUI calls `models_dir`, and the only place downloads are written. Default `<ComfyUI>/models`. RunPod: `<mount>/astrid/engines/<engine>/models` (`packs/runpod/generation.py:137-141`). Standalone VibeComfy: `VIBECOMFY_MODELS_ROOT` if set.
- **ComfyUI root:** the checkout; the only authority for `target_path` (`custom_nodes/<pack>/…`).
- **Extra model places:** read-only search paths (a person's own folder or `extra_model_paths.yaml`), declared once and never written.

VibeComfy owns `ModelLayout{comfyui_root, models_dir, extra_places}`. The resolver just landed as V1 (VibeComfy `r13/models-root` `e4118ccf`, `/home/user/wt/c-vcroot`): `fetch.py` resolves the models root plus the ComfyUI root.

## Flow
- **Astrid → VibeComfy, once:** `VIBECOMFY_COMFY_CONFIGURATION` `{runtime_root, comfy_root, models_root, python}` (`managed_preparation.py:536-539`).
- **VibeComfy → ComfyUI:** `--models-directory <models_dir>`, plus one `--extra-model-paths-config` per extra place. The directory must exist first.
- **Deleted in Astrid:**
  - the symlinks and the `models-config`, `models-config-check` and `models-source-check` operations (`engine_runner_target.py:30-31,43-58,450-486`);
  - their callers (`engine_runner.py:429-431,541-545,757-772`; `asset_alignment.py:110`);
  - the `{models_config}` placeholder (`engine_platforms.py:105`, `engine_runner.py:515`);
  - the recipe's `--extra-model-paths-config {models_config}`, replaced by `--models-directory {models_root}`.
- **Deleted in VibeComfy:** the `ComfyUI/models` joins (done in V1) and the generated file in `runpod_setup.py:129-190`.

## Migration
- The volume layout is unchanged.
- The next start on an existing install removes exact-match legacy links.
- The recipe hash changes, so installs re-plan.
- `models/configs` (the checkout's tracked yaml) is unverified.
- **Hazard:** Astrid's align downloads using `target_path: '<models_root.name>/<relative>'` with `root=models_root` (`asset_alignment.py:219-223`), relying on `target_path` being authorized against `models_root.parent`. Align should pass `subdir/name` instead.

## Tasks (Release 13: V1 → A1 → A2 → A3 → G1)
| id | outcome | scope | size |
|---|---|---|---|
| V1 | Two-root resolver; preparation honours the configured models directory | VibeComfy fetch, prepared, dependencies | X (DONE, `e4118ccf`) |
| A1 | Align stops using the `target_path` parent trick | `astrid/core/generation/asset_alignment.py:219-223` | N |
| A2 | ComfyUI launches with `--models-directory`, the directory created first | the RunPod and Windows recipes `start.argv`; `engine_platforms.py:start_request` | X |
| A3 | Links, generated yaml and source exemption removed; legacy links cleaned up | `engine_runner_target.py:_MODEL_OPERATIONS`, `engine_runner.py:start,check_health,source`, `asset_alignment.py:110` | S |
| G1 | Live proof: TTS, SFX and image, on a volume pod and a disk pod | GPU validation | X |
| Later | V2 (extra places → launch args); A4 (reuse a person's models folder, declared once); A5 (no ComfyUI-specific model code in Astrid core); D1 (a "Where models live" docs page) | | |
