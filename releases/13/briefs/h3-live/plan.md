# h3 live on the claim path: verdict, argv and rulings

Fable lead, 14 Nov. Candidate `r13/compose` `21dacd488` (the installed `65b1d45c` differs only in `.github/workflows/lanes.yml`). Explored by eleven Luna helpers (briefs and results: `/tmp/claude-0/-home-user/ebe1c0ff-e4f9-56ce-9569-8dc5a5d6e26c/scratchpad/h3/`); every fact below that a ruling rests on I checked in the source or by a CPU dry run. Nothing paid was run.

## 1. Verdict

**With `--entry h3` and a request document, all three modes should run on `21dacd488` as is.** Nothing structural stops them. **h3 has never run on a real GPU on any revision** (Plan 34 handoff.md:42 and inputs.md:9 say "unrun"), so the first run is a first run, not a re-run.

What is proven:

- **CPU dry runs, all `status: ready`, `issues: []`** on the installed candidate with `--placement runpod`: i2v 37 s, v2v 97 s, video-edit 48 s. Each resolves the five locked models with digests and sizes and the two pinned custom nodes.
- **h3 has no path of its own.** It goes through the same claim-only path as image t2i (`sdk/generation.py:1415-1600`, `runpod/machine.py:837-905`), and the pod re-runs h3's `build` and runs `after_outputs` before copy-back (`vibecomfy/local_job.py:219-338`). `h3_release.py` can rent, but nothing on the generate path calls it.
- **The pod-side path is covered on CPU** for h3 (`tests/integrations/test_runpod_dry_live_seam.py:82`, cell `video/h3`).
- **Media bindings can't diverge between controller and pod.** They are byte-derived names, but the controller doesn't ship them (`sdk/generation.py:1777`); the pod's own archive supplies them.
- **Engine matches h3's constraints.** One Linux recipe for every cell; ComfyUI `6bfaacc6` is 0.36.0 (decisions.md:452); torch 2.10.0+cu130, comfy-kitchen 0.2.35, comfy-aimdo 0.5.5 match `profiles/native-v1.yaml:18-23`; both custom nodes are in the recipe.
- **Models fit the volume.** The five h3 files (53.5 GB) are already inside the 110.4 GB RunPod lock on the 200 GB volume.
- **LanPaint is not needed.** The LanPaint graph is unreachable (`compile.py:1042-1056`; `test_edit_binding.py:187` asserts so). Edit compiles to the native masked-edit graph.
- **The two red CI rows are not live-path faults.** The overlay-integrity row is a test fixture nothing reads at run time; the `pod workflow member is not a regular file` row is a test that writes only a stub `workflow.py`, and a real h3 build emits all three members.
- **`--consent user_env` is not needed on RunPod.** It is accepted and passed through (`sdk/generation.py:246`, `runpod/adapter.py:368`), but nothing on the RunPod path reads it; it gates only attached launch and `generate align --apply`. The other live cells ran without it. Leave it off.

What is not proven, and only a live run can show: ffmpeg/ffprobe on the pod image, 32 GB VRAM (Plan 34 planned an A6000, 48 GB), and how long a cold run takes.

## 2. The three runs

Synthetic inputs I made, all dry-run green, in `/home/user/wt/install-r13b/inputs/h3/`: `source.mp4` (1024×576, 24 fps, 60 frames, AAC), `first-frame.png`, `mask.png` (unused), and a request and asset map per mode. Cells' inputs replace these where they exist. **A source clip must be exactly 1024×576 at 24/1 CFR** (`prepare.py:239-242`); the local `sfx-first-look.mp4` (1280×720) is refused until conformed.

```
I=/home/user/wt/install-r13b/inputs/h3
astrid generate video --entry h3 --mode i2v        --input request=$I/i2v.request.json  --input asset_map=$I/i2v.assets.json  --placement runpod --recovery-path <file> --json
astrid generate video --entry h3 --mode v2v        --input request=$I/v2v.request.json  --input asset_map=$I/v2v.assets.json  --placement runpod --recovery-path <file> --json
astrid generate video --entry h3 --mode video-edit --input request=$I/edit.request.json --input asset_map=$I/edit.assets.json --placement runpod --recovery-path <file> --json
```

| Mode | Request | Graph | Expected output |
|---|---|---|---|
| i2v | `generate`, one reference image, 3.0 s, 8 steps, seed 42 | reference generation | 1024×576, 24 fps, 72 frames, generated audio |
| v2v | `continue`, source 0–2.5 s, output 5.0 s | native continuation | 120 frames; first 60 are the source, audio continues |
| video-edit | `edit`, whole 2.5 s, full frame | native masked edit | 60 frames, picture regenerated, source audio kept |

**Need:** 53.5 GB free on the volume for the first run; a 32 GB card should hold the 21 GB int8 model with the 27 GB text encoder offloaded to RAM, so pod RAM matters (community reports int8-convrot running on 12 GB cards with dynamic VRAM, and a 5090 with 96 GB RAM: Banodoco `minimax_h3_chatter`, 29 Sep and 17 Oct).

**Time, estimated, not measured:** the first run downloads 53.5 GB under a one-hour preparation deadline (`local_job.py:139`), so it needs about 15 MB/s sustained; a timed-out download resumes from its `.part` file on the next run. First load from the network volume was measured at about 28 MB/s (decisions.md:836); at that rate loading h3 takes up to 30 minutes per run. Sampling is minutes. Plan on 40–80 minutes cold and 10–35 minutes for later runs. **Claim for the full 2 h.**

## 3. Problems beneath the problems

| # | Problem | Root cause | Now | Follow-up | Owner | Blocks live |
|---|---|---|---|---|---|---|
| 1 | **The video default is h3 in name only.** `generate video "…" --edit img` skips h3 and picks `ltx-2.3`, which on RunPod fails with a traceback (`managed model has no declared digest`) | h3's only inputs are `request` and `asset_map`; the selector skips a default whose required inputs are missing (`sdk/generation.py:1521-1533`) | Branch `r13/h3/plain-inputs` `5fe9ed7a0`: `build` writes the same request.v1 from a prompt with `image_ref` (i2v) or `video_ref` (v2v). 46 lines, no second path. Dry-run green for both; 48 focused tests pass | The uncaught traceback on the ltx fallback; Plan 32 | cells | No for `--entry h3`. **Yes for "h3 is the default"** |
| 2 | **`--video-ref` alone infers `t2v`** | `_infer_video_mode` knows only image refs (`sdk/generation.py:513-527`); `entries.py:777` already maps `video_ref` to v2v | Pass `--mode v2v` | One line so both inferences agree; Plan 32 | cells | No |
| 3 | **i2v is reference-guided, not first-frame.** Hannah asked for "feeding first frame" | The `generate` graph is `MiniMaxH3ReferenceToVideo` on the ref2va model; images are conditioning, never frame 0 (README; `generation.py:223`) | Say so in the record; judge the output as "matches the reference", not "starts on it" | A first-frame route: a guide frame at index 0, or the fl2va model. Community practice: ref2va alone gives poor motion from a first frame, a start or guide frame is much better (Banodoco, MysteryShack 6 Oct, QuintForms 24 Sep, Stef 11 Sep); Plan 34 | cells | No, but it decides whether i2v "does what it should" |
| 4 | **ffmpeg and ffprobe on the pod are assumed.** For i2v the first use is in `after_outputs`, after the paid run | h3 finds them with `shutil.which` (`prepare.py:47`, `compose.py:835`); the pod image and recipe neither install nor check them | Same branch: `build` refuses to start without both, so a missing tool costs seconds. Until it lands, **run v2v first**: its build probes the source before any download | Declare the tools once on the pack and have pod preparation check them; Plan 32 | cells (check); machines (install, if absent) | Only if absent |
| 5 | **A cold run can outlast the waits** | 53.5 GB under a one-hour preparation deadline; the CLI's wait is a fixed 3600 s with no flag (`sdk/generation.py:1233`); the job is cut at lease expiry (`machine.py:758`) | Claim 2 h; pass `--recovery-path`; on `task_wait_timeout` the job is still running, re-attach with `--resume`; on a preparation deadline, rerun (it resumes) | Preparation deadline sized from bytes to fetch; Plan 32 | machines | No |
| 6 | **"5/24" is refused for video-edit** (`not representable on the native clock`) | v2 normalisation stores each edit time twice, a float and exact ticks (`request_v2.py:62-63, 84`); `spec.py:518` passes the float and `spec.py:218` rechecks it exactly | Use windows that are exact in binary: multiples of 3 frames (0.125 s) | `spec.py:518` builds `during` from `edit["resolved"]["range"]` as `n/d` text, which `_interval` already accepts; Plan 34 | cells | No |
| 7 | **h3's evidence dies with the job** | `build` and `after_outputs` write plan, compose and verify evidence into a temp job directory that `local_job.py:338` deletes; none is declared | None needed to run | Declare them with the existing `run_logs.declare(out, LogDecl(...))` (as `engine_custody.py:825` does) so `astrid tasks logs <task>` returns them. No new mechanism; Plan 32 | machines | No |
| 8 | Turbo LoRA is the `fl2v` 8-step on a `ref2va` base | pinned in the graph; dedicated `ref2v` turbo LoRAs exist (Banodoco, Draken 20 Oct) | Run as pinned; check the picture | Evaluate the ref2v turbo; Plan 34 | cells | No |
| 9 | Dead LanPaint graph, and `describe h3` prints required inputs as optional | unreachable route kept; display reads a different flag from validation (`entries.py:263` vs `763`) | None | Delete the trio; one source for "required"; Plan 32 | cells | No |

**One decision in row 1 that is cells' or Hannah's, not mine:** the branch makes h3 the real default on every placement, so `generate video "…" --edit img` on a local or attached target would also choose h3 (53.5 GB) where it chose `ltx-2.3` before. It also widens h3's declared inputs, so two tests that pinned `request`/`asset_map` as the only, required inputs are updated in the same commit. I pushed it; I did not merge it.

## 4. Order, and when to stop

1. **v2v first** (fails in seconds if ffprobe is missing; otherwise it pays the one download for all three).
2. **video-edit**, then **i2v**, on the same pod.
3. Optional, if row 1 lands: `astrid generate video "<prompt>" --edit <png> --placement runpod` with no `--entry`.

Stop and send me the evidence if:

- the pod reports `ffmpeg` or `ffprobe` missing (machines installs it in pod preparation; do not work around it);
- a storage refusal (under 53.5 GB free on the volume);
- CUDA out of memory, or the job killed while loading the text encoder (pod RAM): do not retry on the same shape; the fallback is a 48 GB card;
- an `adaln_proj` or LoRA key error (a full/pruned LoRA mismatch is a known community failure, Banodoco daily summary 24 Sep);
- `after_outputs` fails in compose or verify after a good generation: that is an h3 fault, not a machine fault;
- two preparation-deadline failures in a row (the download is not resuming).

A first `task_wait_timeout` or a first preparation-deadline failure is not a stop: re-attach or rerun.
