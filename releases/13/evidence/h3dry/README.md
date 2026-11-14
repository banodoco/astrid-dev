# h3live — admitted edit inputs, Release 13

Evidence only, 2026-11-14 UTC. Agent tree `cf49d41507f832e855630790b2e6907a11cc3947` (detached, clean). Route N; execution configuration requested by the card. No product edits, commits, pushes, network, GPU work, model downloads or paid/provider calls. Only `astrid generate ... --dry-run` was executed. Five shipped requests have fresh CPU admission results under `dryrun/`; `ready` means preparation/compilation, with target `pending_host_readiness`.

Unpack this directory, then **cd to the package root** before using commands below. Every asset map sits at the package root; its keys match request asset names and its `assets/...` values resolve relative to that map. No path rewriting is needed. Python checks require numpy plus ffmpeg/ffprobe (tested here with Python 3.13.18, numpy 2.5.3, ffmpeg 6.1.1).

All five requests explicitly use **seed 42**. Added it only where absent: T5a and T5b (their prior v1/v2 defaults differed: 0 vs 123456789). T2 and T3 already used 42. T4 is byte-for-byte unchanged. T3 is v2 with exact `"1/6"`; T5b is v2, steps 20 and `settings.turbo.enabled: false`. Only admitted variants are included. Unsupported audio generation was removed in the previously admitted video-only corrections; these preserve source audio. The synthetic test-pattern clips are not real bicycle footage.

## Live argv — documented, NEVER executed here

The following form is taken from `proof/h3-video-edit-README.md`. The live controller needs its already claimed RunPod lease in the same custody journal; this head has no `--machine` flag and generation does not claim a machine. `--placement runpod --consent user_env` are documented flags, not a claim of current host readiness or authorization. Replace `<FRESH_OUTPUT_ROOT>` with an absolute, writable root and use a fresh test output directory. The commands depend on the controller's installed Astrid and existing Runtime authorization. No credential files are packaged.

| Test | Request | Asset map | Exact live argv (one output-root placeholder) |
|---|---|---|---|
| T2-video-only | `requests/T2-video-only.yaml` | `T2-video-only.asset_map.json` | `astrid generate video --entry h3 --mode video-edit --input request=requests/T2-video-only.yaml --input asset_map=T2-video-only.asset_map.json --placement runpod --consent user_env --out <FRESH_OUTPUT_ROOT>/T2-video-only` |
| T3-corrected | `requests/T3-corrected.yaml` | `T3-corrected.asset_map.json` | `astrid generate video --entry h3 --mode video-edit --input request=requests/T3-corrected.yaml --input asset_map=T3-corrected.asset_map.json --placement runpod --consent user_env --out <FRESH_OUTPUT_ROOT>/T3-corrected` |
| T4 | `requests/T4.yaml` | `T4.asset_map.json` | `astrid generate video --entry h3 --mode video-edit --input request=requests/T4.yaml --input asset_map=T4.asset_map.json --placement runpod --consent user_env --out <FRESH_OUTPUT_ROOT>/T4` |
| T5a-video-only | `requests/T5a-video-only.yaml` | `T5a-video-only.asset_map.json` | `astrid generate video --entry h3 --mode video-edit --input request=requests/T5a-video-only.yaml --input asset_map=T5a-video-only.asset_map.json --placement runpod --consent user_env --out <FRESH_OUTPUT_ROOT>/T5a-video-only` |
| T5b-video-only | `requests/T5b-video-only.yaml` | `T5b-video-only.asset_map.json` | `astrid generate video --entry h3 --mode video-edit --input request=requests/T5b-video-only.yaml --input asset_map=T5b-video-only.asset_map.json --placement runpod --consent user_env --out <FRESH_OUTPUT_ROOT>/T5b-video-only` |

## Per-test checks after live generation

Use the **final composed candidate**, not the raw graph output. Replace `<T2_CANDIDATE>`, etc. with the actual retrieved video paths; filenames are not asserted here. These five candidates must each decode to exactly 72 frames at 24 fps, 1024x576. The checker decodes RGB frames through bounded ffmpeg pipes (`-t 3.1`, enough to reject an extra frame); it compares against the decoded source, never against the original still PNG. Ranges below are inclusive, zero-based. Exit **0 = pass / 1 = fail**, including input/tool errors.

| Test | Exact check command | Assertions |
|---|---|---|
| T2 | `python3 check_edit.py assets/bike.mp4 <T2_CANDIDATE> --kept 0-35 --changed 36-71` | Frames 0–35 identical; each of frames 36–71 differs. |
| T3 | `python3 check_edit.py assets/bike-still.mp4 <T3_CANDIDATE> --kept 0-3 --seam 4` | Frames 0–3 identical to decoded still clip; frame 4 differs (seam); 72 output frames. |
| T4 | `python3 check_edit.py assets/bike.mp4 <T4_CANDIDATE> --kept 0-71 --mask assets/frame-mask.png --outside-only --require-change` | Every outside-mask pixel identical on all frames; at least some inside-mask pixels differ. |
| T5a | `python3 check_edit.py assets/bike.mp4 <T5A_CANDIDATE> --kept 0-35` | Kept frames identical. Plan: steps 8, seed 42, Turbo on at 0.95. |
| T5b | `python3 check_edit.py assets/bike.mp4 <T5B_CANDIDATE> --kept 0-35` | Kept frames identical. Plan: steps 20, seed 42, Turbo off, no LoraLoaderModelOnly. |

Permitted regeneration does not guarantee visible change; a failed `--changed` or `--seam` assertion reports that the requested visible-change check was not satisfied. The seam check locates the first changed frame; it does not judge transition quality. Mask white rectangle is exactly x=[384,640), y=[144,432); black elsewhere. `--outside-only` checks the complement; `--require-change` requires at least one changed pixel in the rectangle.

Check the archived T5 plans and captured graph node classes (exact commands, no generation):

```sh
python3 check_plan.py dryrun/T5a-video-only.output.json dryrun/T5a-video-only.workflow.vibe.json 8 on
python3 check_plan.py dryrun/T5b-video-only.output.json dryrun/T5b-video-only.workflow.vibe.json 20 off
```

`plan-checks.log` records these checks. Inspect fresh controller plans the same way if available, passing their stdout-plan and graph paths. These archived files prove the shipped input plans, not a future execution's graph.

## Assets and self-tests

`assets/bike.mp4` is the unchanged h3dry 3 s / 72 frame / 24 fps / 1024x576 H.264 yuv420p source with AAC audio. `subject-bike.png` and `frame-mask.png` are unchanged. `bike-still.mp4` was regenerated from the PNG with `libx264 -crf 0 -pix_fmt yuv444p`, 24 fps, 3 s, and silent AAC. CPU admission accepts yuv444p: no yuv420p fallback was needed. This codec setting is lossless **in YUV444**, not RGB bit identity: RGB→YUV→RGB conversion still changes 483,361 pixels in frame 0, maximum absolute channel difference 2. See `still-frame-comparison.json`. Compare preserved frames to decoded MP4. `make-assets.sh` contains bounded recipes; do not run it over the packaged assets without rerunning admission. `asset-inventory.json` records sizes, SHA-256 and ffprobe metadata.

```sh
bash selftest.sh > selftest.log 2>&1
```

The recorded self-tests cover (1) source vs itself, kept 0–71: pass; (2) lossless copy altered only on frames 36–71, kept 0–35 and changed 36–71: pass; (3) that same copy, kept 0–71: expected fail; (4) copy altered only inside the rectangle, outside-only: pass; (5) copy altered outside the rectangle, outside-only: expected fail. All expected exit statuses are checked. Copies use RGB-domain drawbox and lossless FFV1 to avoid a lossy re-encode contaminating protected pixels. Temporary copies are removed. `selftest.log` ends with `ALL SELF-TEST EXPECTATIONS PASSED`.

## Dry-run provenance and limits

`proof/run.sh` is the exact execution wrapper: `unshare -mn bash .../run.sh <test>`, read-only product bind mount, isolated HOME/cache/tmp, offline package flags, Git protocols disabled and lazy fetch disabled. All five stdout JSON, stderr files and exit codes are under `dryrun/`. Absolute environment/job paths in archived stdout are historical and ephemeral; portable input paths are in the asset maps. The `--out` dry-run location does not persist on this head; stdout is the plan.

Setup reused h3dry and warmrel4-diff's offline approach. `bash /home/user/astrid-dev/env/agent-setup.sh` failed at editable egg-info creation on the read-only tree, before fetching anything. `proof/setup-fallback.sh` installed the cached dependencies from an external source copy; actual product imports were forced to the requested worktree via PYTHONPATH. Runtime is the cached wheel (SHA-256 `1e8b9789e8ca487a1cc04dea22c1d2d0e341efe55689a62cec4b65ed4aab5968`), not a checked-out attestation of lock commit `6855dfa8df65cf8ae4c002b57134d6505493c17c`. VibeComfy local object is `dba38f8644c46f652376f2cd5112ea161e40f09b`. Setup scripts/logs, import origins and final cleanup are retained under `proof/`. The temporary environment was removed after proof capture.

Unverified here: live lease/host readiness, GPU execution and VRAM, sampling, live composition/pixel preservation, real output retrieval paths, visual quality and audio preservation in generated candidates. The live README documents lossless FFV1/PCM composed output; no generated output was produced here. The checker validates pixels/frame timing only, not audio. No `.env` files or credentials were read or packaged.
