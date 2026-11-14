# h3real — real bicycle edit inputs, Release 13

Evidence only, 2026-11-14 UTC. Agent tree `cf49d41507f832e855630790b2e6907a11cc3947` (detached, clean). Route N; execution configuration requested by the card. No product edits, commits, pushes, network, GPU work, model downloads or paid/provider calls. Only `astrid generate ... --dry-run` was executed. Five shipped requests have fresh CPU admission results under `dryrun/`; `ready` means preparation/compilation, with target `pending_host_readiness`.

Unpack this directory, then **cd to the package root** before using commands below. Every asset map sits at the package root; its keys match request asset names and its `assets/...` values resolve relative to that map. No path rewriting is needed. Python checks require numpy plus ffmpeg/ffprobe; asset rebuilding also requires Pillow (tested here with Python 3.13.18, numpy 2.5.3, ffmpeg 6.1.1).

All five requests explicitly use **seed 42**. T3 is v2 with exact `"1/6"`; T5b is v2, steps 20 and `settings.turbo.enabled: false`. T4, T5a and T5b requests and all asset maps are unchanged from the prior package. T2 and T3 prompts now address the actual scene. Requests generate video only and keep source audio.

- This package supersedes the earlier `h3live` colour-bar package for bicycle edit tests.

**PROVENANCE:** `assets/bike.mp4` is a byte-for-byte copy of `/home/user/cells/evidence/h3real/in/T1-i2v-bike.mp4`, supplied from decision-log branch commit `1f2b181`, `releases/13/evidence/live/h3m/`. SHA-256: `bd32975e3ab3738ff248302f4647534919dda8c9d3f305a325d7043a4dfb5810`. It is the generated T1 image-to-video output, not a camera clip. The source commit attribution is supplied provenance, not independently checked against that repository here. No source remux or re-encode was needed.

## Live argv — documented, NEVER executed here

The following form is taken from `proof/h3-video-edit-README.md`. The live controller needs its already claimed RunPod lease in the same custody journal; this head has no `--machine` flag and generation does not claim a machine. `--placement runpod --consent user_env` are documented flags, not a claim of current host readiness or authorization. Replace `<FRESH_OUTPUT_ROOT>` with an absolute, writable root and use a fresh test output directory. The commands depend on the controller's installed Astrid and existing Runtime authorization. No credential files are packaged.

| Test | Request | Asset map | Exact live argv (one output-root placeholder) |
|---|---|---|---|
| T2-video-only | `requests/T2-video-only.yaml` | `T2-video-only.asset_map.json` | `astrid generate video --entry h3 --mode video-edit --input request=requests/T2-video-only.yaml --input asset_map=T2-video-only.asset_map.json --placement runpod --consent user_env --out <FRESH_OUTPUT_ROOT>/T2-video-only` |
| T3-corrected | `requests/T3-corrected.yaml` | `T3-corrected.asset_map.json` | `astrid generate video --entry h3 --mode video-edit --input request=requests/T3-corrected.yaml --input asset_map=T3-corrected.asset_map.json --placement runpod --consent user_env --out <FRESH_OUTPUT_ROOT>/T3-corrected` |
| T4 | `requests/T4.yaml` | `T4.asset_map.json` | `astrid generate video --entry h3 --mode video-edit --input request=requests/T4.yaml --input asset_map=T4.asset_map.json --placement runpod --consent user_env --out <FRESH_OUTPUT_ROOT>/T4` |
| T5a-video-only | `requests/T5a-video-only.yaml` | `T5a-video-only.asset_map.json` | `astrid generate video --entry h3 --mode video-edit --input request=requests/T5a-video-only.yaml --input asset_map=T5a-video-only.asset_map.json --placement runpod --consent user_env --out <FRESH_OUTPUT_ROOT>/T5a-video-only` |
| T5b-video-only | `requests/T5b-video-only.yaml` | `T5b-video-only.asset_map.json` | `astrid generate video --entry h3 --mode video-edit --input request=requests/T5b-video-only.yaml --input asset_map=T5b-video-only.asset_map.json --placement runpod --consent user_env --out <FRESH_OUTPUT_ROOT>/T5b-video-only` |

## Requested content

| Test | Exact prompt | Scope |
|---|---|---|
| T2 | Late afternoon turns to golden hour: the same bicycle and wall, longer softer shadows and a warmer light that grows over time. | Video frames [36,72); source audio kept |
| T3 | A person walks into frame from the right, takes the bicycle by the handlebars and wheels it away to the left. | Still-clip prefix 0–3 kept; seam at 4; audio kept |
| T4 | The bicycle frame is deep cobalt blue. Everything else is unchanged. | Approximate box x=[290,768), y=[190,526), all 72 frames; audio kept |
| T5a | Gently brighten the scene. | Frames [36,72), 8 steps, Turbo on |
| T5b | Gently brighten the scene. | Frames [36,72), 20 steps, Turbo off |

## Per-test checks after live generation

Use the **final composed candidate**, not the raw graph output. Replace `<T2_CANDIDATE>`, etc. with the actual retrieved video paths; filenames are not asserted here. These five candidates must each decode to exactly 72 frames at 24 fps, 1024x576. The checker decodes RGB frames through bounded ffmpeg pipes (`-t 3.1`, enough to reject an extra frame); it compares against the decoded source, never against the original still PNG. Both source and candidate are decoded with the same explicit Lanczos, accurate-rounding, full-chroma RGB conversion to match the composer. Ranges below are inclusive, zero-based. Exit **0 = pass / 1 = fail**, including input/tool errors.

| Test | Exact check command | Assertions |
|---|---|---|
| T2 | `python3 check_real_edit.py assets/bike.mp4 <T2_CANDIDATE> --kept 0-35 --changed 36-71` | Frames 0–35 identical; each of frames 36–71 differs. |
| T3 | `python3 check_real_edit.py assets/bike-still.mp4 <T3_CANDIDATE> --kept 0-3 --seam 4` | Frames 0–3 identical to decoded still clip; frame 4 differs (seam); 72 output frames. |
| T4 | `python3 check_real_edit.py assets/bike.mp4 <T4_CANDIDATE> --kept 0-71 --mask assets/frame-mask.png --outside-only --require-change` | Every outside-mask pixel identical on all frames; at least some inside-mask pixels differ. |
| T5a | `python3 check_real_edit.py assets/bike.mp4 <T5A_CANDIDATE> --kept 0-35` | Kept frames identical. Plan: steps 8, seed 42, Turbo on at 0.95. |
| T5b | `python3 check_real_edit.py assets/bike.mp4 <T5B_CANDIDATE> --kept 0-35` | Kept frames identical. Plan: steps 20, seed 42, Turbo off, no LoraLoaderModelOnly. |

Permitted regeneration does not guarantee visible change; a failed `--changed` or `--seam` assertion reports that the requested visible-change check was not satisfied. The seam check locates the first changed frame; it does not judge transition quality. Mask white rectangle is exactly x=[290,768), y=[190,526); black elsewhere. It is **APPROXIMATE**, not a bicycle segmentation. The drainpipe and the surrounding wall outside this box stay protected; some wall inside a rectangular box is necessarily editable.

Strict red-pixel measurements use R>140, G<90, B<90 with 8-connected components smaller than 20 pixels discarded. All boxes are half-open `[x0,y0,x1,y1]`:

| Frame | Strict red bounds | Approximate visual whole-bicycle bounds |
|---|---|---|
| 0 | [436,290,619,411] | [335,225,718,482] |
| 35 | [446,291,632,416] | [322,218,730,495] |
| 71 | [573,349,583,377] | [310,210,748,506] |
| Union | [436,290,632,416] | [310,210,748,506] |

The strict-red union plus 20 px would be [416,270,652,436], which misses darkened red frame parts, wheels, saddle and handlebars. Instead the chosen mask is the approximate visual whole-bicycle union plus 20 px: **[290,190,768,526]** (no clamping needed). This deliberate conservative adjustment is recorded in `evidence/red-bounds.json`; the observed frames and reproducible strict-red measurement are in `evidence/`.

**Checker compatibility:** `check_edit.py` and `check_plan.py` are preserved byte-for-byte from `h3live`. The former hard-codes the old mask and cannot accept this card's required new rectangle. `check_real_edit.py` differs only in the expected rectangle and its error text; every frame, pixel, timing and change assertion is identical. Use the commands in this README for the real assets. This resolves the conflicting requirements to preserve the original checker unchanged and check a newly positioned mask. `--outside-only` checks the complement; `--require-change` requires at least one changed pixel in the rectangle.

Check the archived T5 plans and captured graph node classes (exact commands, no generation):

```sh
python3 check_plan.py dryrun/T5a-video-only.output.json dryrun/T5a-video-only.workflow.vibe.json 8 on
python3 check_plan.py dryrun/T5b-video-only.output.json dryrun/T5b-video-only.workflow.vibe.json 20 off
```

`plan-checks.log` records these checks. Inspect fresh controller plans the same way if available, passing their stdout-plan and graph paths. These archived files prove the shipped input plans, not a future execution's graph.

## Assets and self-tests

`assets/bike.mp4` retains its supplied 3 s / 72 frame / 24 fps / 1024x576 H.264 yuv420p + AAC streams. `subject-bike.png` is frame 0 decoded with the same accurate RGB conversion used by the checks, saved as lossless PNG. `bike-still.mp4` holds that frame for 3 s at 24 fps, using `libx264 -crf 0 -pix_fmt yuv444p` plus silent AAC. Admission accepts yuv444p without fallback. Lossless encoding in YUV444 does not imply RGB roundtrip identity: 540,736 pixels differ from the PNG with maximum channel difference 2; see `still-frame-comparison.json`. Preserved-frame checks compare decoded MP4s. `make-assets.sh` contains bounded recipes; `asset-inventory.json` records sizes, SHA-256 and ffprobe metadata.

```sh
bash selftest.sh > selftest.log 2>&1
```

The recorded self-tests cover (1) source vs itself, kept 0–71: pass; (2) lossless copy altered only on frames 36–71, kept 0–35 and changed 36–71: pass; (3) that same copy, kept 0–71: expected fail; (4) copy altered only inside the rectangle, outside-only: pass; (5) copy altered outside the rectangle, outside-only: expected fail. An FFV1 accurate RGB copy of the real clip also passes the T4-style outside-mask check with the new real mask and maximum outside difference 0 across 72 frames, while the hidden test-only default decode fails it; the test measures both maximum differences (default 9; accurate 0). All expected exit statuses are checked. Copies use RGB-domain drawbox and lossless FFV1 to avoid a lossy re-encode contaminating protected pixels. Temporary copies are removed. The first post-restart self-test ended after 17 frames while the measurement script was recopying the source; this was an input read/write race, not an assertion change. Its raw log is retained in `proof/selftest-resume-first-failure.log`. After measurement completed and source bytes were verified, the unchanged self-test passed. `selftest.log` ends with `ALL SELF-TEST EXPECTATIONS PASSED`.

## Dry-run provenance and limits

`proof/run.sh` is the exact execution wrapper: `unshare -mn bash .../run.sh <test>`, read-only product bind mount, isolated HOME/cache/tmp, offline package flags, Git protocols disabled and lazy fetch disabled. All five stdout JSON, stderr files and exit codes are under `dryrun/`. Absolute environment/job paths in archived stdout are historical and ephemeral; portable input paths are in the asset maps. The `--out` dry-run location does not persist on this head; stdout is the plan.

Setup reused the h3live wrapper and offline fallback approach. `bash /home/user/astrid-dev/env/agent-setup.sh` failed at editable egg-info creation on the read-only tree, before fetching anything. `proof/setup-fallback.sh` installed the cached dependencies from an external source copy; actual product imports were forced to the requested worktree via PYTHONPATH. Runtime is the cached wheel (SHA-256 `1e8b9789e8ca487a1cc04dea22c1d2d0e341efe55689a62cec4b65ed4aab5968`), not a checked-out attestation of lock commit `6855dfa8df65cf8ae4c002b57134d6505493c17c`. VibeComfy local object is `dba38f8644c46f652376f2cd5112ea161e40f09b`. Setup scripts/logs, import origins and final cleanup are retained under `proof/`. The temporary environment was removed after proof capture. Compiled graph snapshots were copied from ephemeral job directories before cleanup using `proof/capture-plans.py`; their SHA-256 values are checked against stdout plans. After the container restart, all five admissions were rerun with graph capture active. The initial multi-test shell was terminated with exit 143 during T3; T2 had completed, and the remaining four admissions were then invoked individually. This infrastructure interruption is recorded in `proof/admission-restart-note.txt`. Earlier T2 stdout is retained under `proof/` as historical evidence.

Unverified here: live lease/host readiness, GPU execution and VRAM, sampling, live composition/pixel preservation, real output retrieval paths, visual quality and audio preservation in generated candidates. The live README documents lossless FFV1/PCM composed output; no generated output was produced here. The checker validates pixels/frame timing only, not audio. No `.env` files or credentials were read or packaged.
