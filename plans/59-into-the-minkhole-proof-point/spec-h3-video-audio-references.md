# Spec: H3 video and audio references (#890), toward composable pieces

Status: spec v2, 18 Nov 2026, after a design review. Read against `origin/release/14/plan-59` (`astrid/packs/h3_av/shared/`).

## End state (owner)
A set of pieces that combine freely, each with one meaning:
- start image;
- reference images;
- speaker video or audio;
- masks or regions;
- fixed replacement audio;
- source clips or continuations;
- lines of dialogue.

The user works with them at a high level, and Astrid plugs the right ComfyUI workflow and node inputs in underneath. A route (source-free, masked edit, Character Swap, continuation) is a fact derived from the pieces, not a separate form the user has to learn.

## The three pieces v2 already has (use them as such)
- **`role: timeline` (+ `at`, `range`): fixed content at a time.** A source clip, a start image, a fixed replacement audio clip.
- **`role: reference`: tagged conditioning** (`<Picture n>` / `<Video n>` / `<Audio n>`, assigned in `request_v2.py:363-381`), bound to the node's `ref_images` / `ref_videos` / `ref_video_audios` / `ref_audios`.
- **`edit`: permission to regenerate** (stream, interval, mask, strength).

The node (`MiniMaxH3ReferenceToVideo`, ComfyUI `6bfaacc`) takes up to 9 images, 3 videos (2–15 s at 24 fps, plus their soundtracks) and 3 audio clips. `build_generation_workflow` (`generation.py:234`) is already the single builder behind source-free, masked edit and Character Swap.

## This ticket (smallest step toward the end state)
1. **One reference lowering.** One function turns the request's `reference` media into image, video and audio rows for `build_generation_workflow`, and all three builder callers use it.
   - **Capacities:** 9/3/3 sit in one table beside the builder, pinned by one test against the node schema's limits (`object_info` autogrow `max`).
   - **Delete:** the masked edit's hand-written "two image-reference slots" (`compile.py` ~612), copied from the continuation graph; the node takes 9.
   - **Character Swap:** keeps only its adapter rule (exactly 1 image + 1 video).
2. **References condition the whole pass.** An edit's `guides` only selects the pass's reference set, so any modality is allowed on any edit. Stop extending `EDIT_GUIDE_MODALITIES` per stream.
3. **One meaning per spelling, defined by structure, not by `range`:**
   - a reference named by an *audio* edit's `guides` is a fixed replacement clip. That's today's spelling, unchanged, and marked legacy;
   - every other reference is conditioning;
   - `range` on any reference is only a trim.
4. **Audio regeneration in a masked edit:** an audio edit with `action: generate` and no guides maps to audio strength 1. Today the masked edit hard-codes `audio_strength=0` (`generation.py` ~440) and refuses audio regeneration without a replacement clip (`compile.py:545`), so a voice reference would condition audio that is never generated. State the limit: audio strength is one value per window, so the sound around the line inside that window is regenerated too unless composition restores it.
5. **Source-free calls the builder directly** with v2 rows. It no longer lowers into a v1 request (`compile.py:1075`), and video and audio references are not added to v1.
6. **The builder gains a `ref_audios` loader loop.** The existing video loader already trims and resamples to 24 fps in the graph, so no new preparation stage is needed unless the 48 kHz audio check shows otherwise.
7. **Records:** the dry run and the result list each reference with its tag, range and node slot, alongside the effective settings from `p59/h3-overrides`. There's no separate "tag not mentioned in the prompt" warning. The 2–15 s check lives in the normaliser only.

## Tests
- **Unit tests:**
  - the lowering produces the right rows and node inputs for 1 image + 1 video (+ its audio) + 1 audio, on source-free and on masked edit;
  - the capacity test against the node schema;
  - refusals for a 4th video, a 16 s video, or a video without measurable stream durations;
  - existing image-only requests compile byte-identically;
  - Character Swap compiles identically.
- **Two live GPU jobs** on 02c with the line "tuning workflows by hand,":
  - **source-free:** start image = the corrected lens frame (as `<Picture 1>`), plus a video reference of Morpheus speaking (about 5 s from the film);
  - **masked edit:** mouth mask on the real close-up, the same video reference, an audio edit with `action: generate`, and the original picture elsewhere.
  
  Accept each if the transcript shows exactly the line, the owner recognises the voice, and the lenses (source-free) or the untouched picture (masked) are right.

## What it covers afterwards
| Need | After this ticket |
|---|---|
| New line in someone's voice, picture regenerated | Yes (source-free + speaker video or audio) |
| New line, original picture kept | Yes (masked mouth + speaker reference + audio generate); the sound inside the window is regenerated |
| Different person or creature in a region | Yes (image or video guides) |
| Several speakers | By capacity (3 videos + 3 audio clips); which voice goes to which face rests on prompt tags, unproven |
| Line longer than the shot | No, still continuation |
| Voice from audio only, or from video | Both |

## Later tickets (toward the end state)
- **Respell fixed content as timeline items:**
  - fixed audio becomes `role: timeline` audio;
  - the start image becomes a timeline image at frame 0, probably via `MiniMaxH3AddGuide` ("anchor an image, clip or audio at any frame"; only used in the LanPaint graph today, and unverified with ref2va). This folds in #863;
  - retire the guides-as-replacement spelling.
- **Continuation from the same builder** ("build the invocation once", #866). Then voice references and long lines compose too. Its captured graph already uses `ref_video_0` and `ref_audio_0/1`.
- **Pack coverage note:** list the node inputs the pack doesn't expose: `ref_image_size` (fixed to `match`), width/height (fixed at 1024×576, see #885), `first_frame` / `last_frame`, AddGuide, Fun ControlNet.
- **Recast skill:** add "speaker video reference" to the "new line" table only after the GPU proof. It would then replace "make the voice first" for most cases.
