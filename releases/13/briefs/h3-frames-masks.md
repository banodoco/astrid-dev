# h3_av: frames at positions, masks, precise first frame (advisor, 19:00 Sat 14 Nov)
Source: three Luna passes over Agent cf49d415, ComfyUI 6bfaacc and VibeComfy dba38f86. Nothing was run.

## Short answer
1. The model takes frames at chosen positions (ComfyUI `MiniMaxH3ImageToVideo` with `first_frame`/`last_frame`, and `MiniMaxH3AddGuide(image, frame_idx)`, chainable; comfy_extras/nodes_minimax_h3.py:115-187) and a per-frame, per-region `denoise_mask` [T,H,W], where 1 means generate (comfy/ldm/minimax/model.py:77-85,639-652). **Our pack doesn't expose positioned frames.**
2. Our "i2v" builds `MiniMaxH3ReferenceToVideo` with the image as `ref_image_1` (astrid/packs/h3_av/shared/generation.py:305-346): a look reference, not a pinned frame (README.md:74-78).
3. The round 6 video-edit used a full-frame mask at 1 step: the wrong test. The default is Turbo at 8 steps.

## Declared inputs
- **Entry:** request, asset_map, prompt, image_ref, video_ref, frames, seed, steps (h3.yaml:7-26).
- **Plain flags carry no mask:** image_ref means reference generation; video_ref means regenerate the whole picture and keep the audio (hooks.py:70-95).
- **Request v1:** operation (edit, continue, generate); source.range; changes.video[] with `during`, `area` (full_frame, mask_asset or geometry) and `action` (generate or preserve); references[] with purpose; overrides.steps 1–200. `keyframe` is rejected for generate (request.py:272-277).
- **Request v2:** media[] with `at`; edit[] with a mask (asset, rectangle, polygon, polarity) and strength. `hard`/`latent_pin` are rejected in conversion (request_v2.py:379-382).
- **Mask polarity:** white = regenerate, black = keep.
- **Open contradiction:** compile.py:183-226 (a LanPaint mask path; CPU tests pass for static and moving masks) vs README.md:44-53 ("regional spatial masks fail before execution"). A dry run settles it.

## Precise first frame
- Through i2v: no pin exists.
- Probably through a source-backed edit of a still clip that keeps the first frames (T3). Unproven live; the VAE packs 4 frames per latent step, so watch for a seam.
- The proper fix: build i2v on `MiniMaxH3ImageToVideo.first_frame` or `AddGuide` at frame_idx 0, and allow keyframe purposes with positions. About half a day plus one live round.

## Tested today
| | CPU | Live |
|---|---|---|
| Reference "i2v" | contract, 8 steps | r6 PASS (no frame-0 comparison) |
| v2v | binding tests | r6, 1-step pipeline only |
| Temporal full-frame edit | compile and compose | r6, 1 step; prompt not followed |
| Regional or moving mask | compose and verify (no inference) | never |
| Continuation | compile | never |
| Positioned frames | rejected | never |

## Live requests for the final repeat (dry-run each first)
- **T1:** i2v bicycle at 8 steps; SSIM of frame 0 against subject-bike.png.
- **T2:** temporal edit of the 3 s bicycle clip, `during: [1.5, 3.0]`, a dusk prompt, steps 8, seed 42. Frames 0–35 identical to the source; 36–71 changed.
- **T3:** first frame via a still-clip edit, `during: [0.1667, 3.0]`. Frame 0 equals the image; check for a seam at frame 4.
- **T4:** regional `mask_asset` (white over the bicycle frame), "frame deep cobalt blue", steps 8. Pixels outside the mask identical.
- **T5:** round 6's brighten redone as T2's shape, at 8 steps, and again at 20 steps with Turbo off.

(The full YAML is in the advisor's message; cells has it.)
