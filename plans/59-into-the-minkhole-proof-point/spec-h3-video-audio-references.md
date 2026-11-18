# Spec: H3 video and audio references ("start image + a reference video of the speaker")

Ticket: banodoco/astrid-dev#890. Status: spec, 18 Nov 2026. Read against `origin/release/14/plan-59` (`astrid/packs/h3_av/shared/`).

## Goal
A recast agent can write one H3 request that says: start from this image, make the character say this line, and take the voice and speaking manner from this reference video of them talking. No continuation trick, and no second mouth pass.

Example (02c, "Into the Minkhole"): start image = the corrected lens frame (the old man and Morpheus's hands with the mink and the blue pill); reference video = 3–10 s of Morpheus speaking in the film; line = "tuning workflows by hand,".

## What exists today
- **The node supports it.** `MiniMaxH3ReferenceToVideo` (ComfyUI `6bfaacc`) has optional inputs:
  - `ref_images` (≤9, `<Picture i>`);
  - `ref_videos` (≤3, frames at 24 fps, 2–15 s, `<Video k>`);
  - `ref_video_audios` (each video's soundtrack);
  - `ref_audios` (≤3, `<Audio j>`).
  
  The `vae` and `audio_vae` inputs make the references condition the latents, not only the text encoder.
- **The v2 request half-knows it.** References may be `image`, `video` or `audio`, and the normaliser already assigns `<Picture n>` / `<Video n>` / `<Audio n>` tags (`request_v2.py:363-381`).
- **One route already binds a video reference:** the Character Swap adapter (`compile.py` ~839-860 `_compile_character_swap_v2`; validation `request_v2.py:312-330`) binds one video reference with a range to the node. Reuse its loader and binding code; don't write a second one.
- **Every other route refuses them:**
  - source-free generate: "accepts image references only" (`compile.py` ~1065);
  - continuation: "reference ports accept image references only" (~1108);
  - masked edit: "video edits support modalities: image", and an audio guide is always a fixed replacement span.

## Scope (smallest useful)
1. **Source-free generation with references (branch `source_free`).** Allow, besides 1–9 image references:
   - up to 3 `video` references, each with an optional `range` (2–15 s after trimming, on the 24 fps grid); bind its frames to `ref_video_k` and, if it has an audio stream, its soundtrack to `ref_video_audio_k`;
   - up to 3 `audio` references with an optional `range`; bind them to `ref_audio_j`.
   
   Keep the existing refusal messages for anything over the limits, and name the limit.
2. **Start image.** Keep the starting image as a reference image (`<Picture 1>`). The prompt says the first frame matches it, which is how source-free generation is used today. Don't add a new "first frame" concept in this ticket. The source-backed "still as a short video" route (astrid-dev#863) is the separate way to pin the exact first frame.
3. **The masked edit route:** allow `video` and `audio` references as region guides only if the native edit graph reaches the same node inputs. If it doesn't, keep refusing, and say why in the message and the SKILL. Don't fake it.
4. **The continuation route:** out of scope. It already carries the voice in its source.

## Behaviour and checks
- **Validation, in the normaliser, using the same `_asset` inspection:**
  - a video reference must decode, run 2–15 s after its range, and have measurable stream durations (the error we hit today was "source stream start times and durations must be measurable");
  - an audio reference must decode at 48 kHz, or be resampled once at preparation.
- **Prompt tags:** the docs and the example use `<Video 1>` / `<Audio 1>` in the prompt. A request that defines a video reference but never mentions its tag gets a warning in the dry run, not a refusal.
- **Records:** the dry run and the result list each reference with its tag, range and node slot. This rides on the effective-settings record from `p59/h3-overrides`.
- **Digest:** existing image-only requests compile byte-identically (the same check `test_edit_inputs.py` already does).

## Files
- `shared/request_v2.py`: allow the modalities and ranges per route; per-route limits.
- `shared/compile.py`: source-free binding; reuse the Character Swap video-reference binding helper (extract it into a shared helper used by both).
- `shared/generation.py` / `stages.py`: preparation of video and audio reference assets (trim to range, 24 fps, 48 kHz).
- The workflow graph for source-free generation: add the loader nodes for `ref_videos` / `ref_video_audios` / `ref_audios`, unconnected when unused.
- `docs/SKILL.md`: a "References" table (what each route accepts) and a recipe. `docs/recast-scene/SKILL.md`: add "start image + speaker video" as the fourth "new line" method in the rubric.
- **Pack coverage note** (the principle in #890): list the node inputs the H3 pack still doesn't expose.

## Tests
- Unit tests:
  - normalisation accepts 1 image + 1 video (+ its audio) + 1 audio on source-free, and refuses a 4th video, a 16 s video, or a video without measurable durations;
  - compile binds the right node inputs (check the graph JSON);
  - image-only digests are unchanged;
  - Character Swap still compiles identically.
- **One live GPU job (the proof):** 02c, start image = the corrected lens frame, video reference = Morpheus speaking (about 5 s from the film), line = "tuning workflows by hand,". Accept it if:
  - the transcript shows the line and nothing else (`timelines transcripts run`);
  - the voice is recognisably his (owner listens);
  - the lenses still match the start image.

## Size
A few hours of build: mostly wiring and reuse, plus one install and one short GPU job.
