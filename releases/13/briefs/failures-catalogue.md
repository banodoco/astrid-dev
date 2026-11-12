# Release 13: every live and offline failure, 11–12 Nov (for a root-cause synthesis)

Status: FIXED (merged into the rehearsal), IN FLIGHT, or OPEN. Evidence paths are under `/home/user/wt/`.

## Live GPU runs (RunPod)
1. **TTS crash:** the pack's `@check_model_inputs()` was incompatible with transformers 5.22.1. Fixed with a recipe source patch, but VibeComfy `nodes restore` then refused the patched pack as dirty. FIXED: declared patches, VibeComfy `c7a47e36`.
2. **TTS and SFX model folders invisible on the volume:** Astrid's models-folders change added symlinks `ComfyUI/models/<folder>` → the volume. Then VibeComfy preparation refused them: "resolves outside its authorized root" (`prepared.py:218` hard-coded `ComfyUI/models`, while fetch used `VIBECOMFY_MODELS_ROOT`). IN FLIGHT: V1 resolver `e4118ccf` done; the model-layout design (`briefs/wave3/model-layout-design.md`: `--models-directory`, delete the symlinks) is under Astra review. Failure logs: `install-r13b/data-b6/generation/failures/{65a6c375…,caf04bb1…}/logs/`.
3. **Music:** preparation refused "model asset entry requires 'subdir' or 'directory'". Model declarations come in more than one shape across templates and locks. IN FLIGHT: Terra, `briefs/wave3/music-declaration.md`. Logs: `…/failures/1517d183…/logs/`.
4. **Edit:** `astrid generate image "…" --entry edit/qwen_image_2_1_turbo_edit --mode edit --edit <png>` is always refused: "requires: image_ref". OPEN: the first worker stopped because duplicate CLI and JSON keys are deliberately rejected (`tests/core/generation/test_entry_cli_contract.py:146`); the image never arrives either way.
5. **Text-to-image PASSED,** but took 6m38s with no downloads: 15 s host preparation, 4m17s on the pod, 54 s collecting one PNG, 24 s reset. The reset restarts ComfyUI, so every job reloads its models from the volume. A success's engine logs are not captured ("the ComfyUI server owns its logs").
6. **Machine deleted after a failed job** (`unsafe_job_state`) because a legitimate receipt refresh failed strict equality. Also deleted on first-preparation failure. FIXED: keep-warm passes 3–6.
7. **SFX refused reuse of the kept machine:** "target policy differs from the retained provider owner". Its per-run limits (preparation, execution, idle, cap) differed from TTS's, and they're re-declared on every generate. OPEN: the machines redesign (`briefs/wave3/machines-plan.md`; M1 in flight).
8. **No 5090/4090 in the volume's datacenter for 13 minutes.** The volume pins the datacenter, and the CLI said nothing while the host logged "no stock yet". OPEN: machines plan M6; the wait line.
9. **Fresh install has no project:** `generate` refused "project is required". OPEN: a default project.
10. **Failure publication rejected forever:** an empty log was already in the CAS unscoped, the Runtime refused hash-verified inline bytes, and the host replayed the rejected fail forever, holding the GPU slot. FIXED: Runtime `6855dfa8` plus Agent terminal-reconcile `56284e6c`.
11. **The `generate` CLI was silent for 40 minutes:** it read `spec.inputs`, but the Runtime returns `spec.spec.inputs`. Its heartbeat now prints but says only "running waiting=-". PARTLY FIXED: `980b2c9a`.
12. **`insufficient_storage` masked the real blocker** (a held slot); the Runtime reports only the first blocker. OPEN: the Runtime full blocker list is on a branch and changes the schema.
13. **Earlier, the same week:**
    - ComfyUI pin predated the Qwen Image 2.1 nodes;
    - the setuptools lock had a double hash;
    - the music template id lost its category;
    - engine install command output was discarded;
    - `tasks logs` read the wrong source;
    - `networkVolumeId` versus REST `networkVolume` field drift;
    - a 429 storm on release;
    - capacity reasons collapsed into one;
    - a bare False from install verification.

    All fixed.

## Offline
14. **The CPU journey** `tests/integrations/test_remote_machine_cpu.py` had never run on CI; locally it failed 24/25 on bug 10. Now 21 pass, 3 fail, 2 errors:
    - "host graph cleanup remains unresolved";
    - "bounded pod operation deadline expired";
    - "the cancelled machine was not released";
    - receipt `unavailable` vs `not_collected`.

    OPEN. Log: `/tmp/claude-0/-home-user/ebe1c0ff-e4f9-56ce-9569-8dc5a5d6e26c/scratchpad/journey.log`.
15. **Codex workers ran in a sandbox that broke their sub-agents.** FIXED: astrid-dev #557.

## Plans already recorded
- Plan 50: recorded boundaries and the offline harness.
- The machines redesign: claim-only spend; named machines; no consent flag; the idle timer.
- The model layout.
- The usability log: `briefs/wave3/usability-log.md`.
