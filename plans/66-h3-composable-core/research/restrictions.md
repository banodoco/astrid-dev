# Restrictions review: real limit or arbitrary?

Read-only, 18 Nov 2026. Nothing was run.

**How this was done.** The Luna helpers were not launched: the `codex exec --dangerously-bypass-approvals-and-sandbox` command was blocked by the session's permission system, and I did not work around it. I did the research directly instead. Sources read:

- ComfyUI `6bfaacc` `comfy_extras/nodes_minimax_h3.py` (fetched from GitHub) and its cached schema in VibeComfy.
- Motion pack `361624fb`: `h3_v2v_fractional.py`, `KEYFRAMES_AND_INSERTS.md`, and the cached schema `ComfyUI-H3-Motion-Context-MultiRef@cpu-runtime.json` (its entries record commit `361624fb`).
- MiniMax H3 model card and `docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md` on Hugging Face.
- The Character Swap LoRA model card (`akatz-ai/MiniMax-H3-Character-Swap-LoRA`).
- Astrid `origin/release/14/main` and `origin/release/14/plan-59`.
- Seven Hivemind searches. They returned no controlled evidence on any item; I say so where it matters.

Not read: the motion pack's context and bridge node source (only their schema and documentation), and `comfy/ldm/minimax/`.

## The main finding

**Most of these limits come from Astrid using one node of the motion pack, not from the model or the pack.** The pack Astrid already pins at `361624fb` also ships:

| Node (already pinned) | What it gives |
| --- | --- |
| `MiniMaxH3SetAVNoiseMask` | Separate video and audio denoise masks; the audio mask varies over time at 40 Hz, and fractional values are allowed |
| `MiniMaxH3ExistingVideoMaskedContext` | A source clip kept at any offset that is a multiple of 17 frames (`insert_frame`), with generation around it |
| `MiniMaxH3MaskedAVBridge` | Clip A, generated middle, clip B in one sampling pass |
| `MiniMaxH3CustomKeyframesMasked` | Stills hard-pinned in the latent at chosen frames |
| `MiniMaxH3AssembleInterior`, `MiniMaxH3AssembleBridgeAudio` | Exact splice-back after decoding |

Using them needs no new dependency and no GPL code vendored; it needs their class names added to the builder's `custom_node_refs`. The real limits that remain are lattices, listed at the end.

## Verdicts

### 1. At least one image reference: arbitrary. Simplify.

- **Node:** `ref_images`, `ref_videos`, `ref_video_audios` and `ref_audios` are all optional with `min=0`. `execute` attaches `minimax_refs` only `if ref_blocks:`, so zero references runs as plain text conditioning.
- **Astrid already does it:** the masked edit accepts zero references (`0 if masked_edit else 1` in `build_generation_workflow`), and continuation's zero-reference case selects the source-only bundle.
- **Model card:** the Ref2VA checkpoint is described as "Text with reference images, videos, and/or audio". Text-to-audio-video is listed as a task of the other checkpoint, FL2VA.
- **Verdict:** audio plus text and video plus text are documented uses and should be admitted. Text only on the Ref2VA weights is accepted by the node but is outside what the card documents for that checkpoint, so admit it and have the dry run say "no references: outside the documented use of this checkpoint". Quality is unverified.

### 2. One audio-changing window per graph: arbitrary. Simplify, and do it properly.

- **Where it comes from:** `compile.py` on Plan 59: "one replacement audio span per request is supported; the graph has one replacement clip slot". The splice helper `_spliced_replacement_audio` is a plain concat chain; one clip is a choice, not a limit.
- **The scalar is not the limit either.** `H3V2VGranularFractionalDenoise` fills the audio mask with one constant, but the latent's audio mask is a per-tick tensor, and `MiniMaxH3SetAVNoiseMask` in the same pinned pack sets it over time ("Audio masks are spatially averaged, resampled over the uniform 40 Hz timeline, and broadcast over stereo").
- **Why this matters beyond counting windows.** Plan 64 SR-5 sets strength 1 for the whole clip whenever any audio is generated and lets composition restore kept samples. The delivered samples are right, but during sampling the model then hears none of the kept or supplied audio. In the mixed case (a supplied line on one interval, generated audio on another) the mouth on the supplied interval is animated against audio the model invented, and the supplied clip is spliced over it afterwards. That is a lip-sync defect by construction.
- **Verdict:** allow any number of audio windows. Build one audio mask from the grants (0 on kept and supplied spans, the grant's strength on generated spans) and apply it with `MiniMaxH3SetAVNoiseMask` after the V2V node. Composition still restores exact samples. Real residue: 25 ms mask granularity, and stereo channels cannot be masked separately.

### 3. Multi-region edits must agree on guides, interval, seed and strength: two real, two arbitrary.

| Must agree on | Verdict | Reason |
| --- | --- | --- |
| References (image guides) | Real, for one pass | References are global conditioning on the whole clip. Different references per region need separate passes, or prompt wording. |
| Seed | Real | One `RandomNoise` per sampler. |
| Strength | Arbitrary | The node computes `outside + mask × (inside − outside)` and documents that "mask values can express continuous preserve-to-generate strength". Write each region's strength as its grey level with `inside_strength` 1. |
| Interval | Arbitrary | The mask is already a per-frame video when bounded (`_bounded_edit_mask`). Union regions per frame. |

Also arbitrary: "video masks cannot be combined" in `_union_static_masks`. A per-frame maximum combines them. Composition keeps using the binary union per frame.

### 4. `audio_strength` only 0 or 1: arbitrary. Simplify, labelled untested.

The node input is a float from 0 to 1 in steps of 0.00001, and the pack's documentation says fractional mask values "allow partial denoising". I found no report of what partial audio values sound like. Give audio grants the same `strength` field video grants have, default 1, and note in `describe` that values between 0 and 1 are untested.

### 5. Continuation only from a prefix at frame 0: arbitrary. The bridge is one node.

- **Bridge:** `MiniMaxH3MaskedAVBridge` takes the end of clip A and the start of clip B with their audio, freezes `preserve_frames` at each end, and generates the middle in one pass. `MiniMaxH3AssembleBridgeAudio` joins source A, the middle and source B on sample boundaries.
- **Interior placement:** `MiniMaxH3ExistingVideoMaskedContext` has `insert_frame` ("0 is the original prefix behavior"), so a kept clip can sit anywhere on the 17-frame grid with generation before and after. `MiniMaxH3AssembleInterior` splices the exact source back.
- **Real limits:** kept context lengths are 39 + 51k frames (39, 90, 141, …); offsets are multiples of 17 (multiples of 51 also align audio exactly); the target is 5 + 17k frames and a bridge target must exceed twice the context; everything is one target latent, so the trained range of about 362 frames bounds context plus gap.
- **Effort:** less than the continuation port, because it is one node and one sampling pass, with no starter and no chained block. It reuses the same timing and exact-prefix composition. I estimate 1 to 1.5 days on top of CC-7.
- **Worth checking before CC-7 starts:** whether continuation itself is simply `ExistingVideoMaskedContext` at `insert_frame` 0 in one pass. If so, prefix, interior and bridge are one lowering ("placed clips inside one target latent") and CC-7 gets smaller. I could not confirm this without the node source.
- **Quality:** Hivemind's workflow index lists three shared workflows using the masked AV bridge; no quality reports.

### 6. Multiple speakers: the owner's belief is half right. Stop listing it as a deferral.

- **No hard binding exists.** The node pairs a soundtrack with its same-numbered video and nothing else. There is no input that ties an audio slot to a face.
- **The model documents it as a prompt convention.** The reference prompt guide says: when an `<Audio N>` "explicitly corresponds to a target speaker, reuse that speaker's global ID … `<Subject N> (Sx)`", with the example `<Audio 1> is the voice-timbre reference for <Subject 1> (S1)`. Speakers get stable `(S1)`, `(S2)` IDs, and up to three audio references are accepted. Its worked two-speaker example gives a voice reference to one speaker and describes the other in words.
- **Reliability is unknown.** I found no report of two voices bound to two faces. One community note (seitanism, 23 Sep) suggests generating a line separately with a single voice reference when binding fails.
- **Verdict:** there is nothing for the tools to build. After Plan 64 a request can already carry two or three audio references. Binding is prompt text. Remove "multiple speakers" from the non-goals of Plans 64 and 66 and treat it as a recipe to try in the live test.

### 7. Request v1: drop it.

- **No consumer outside the pack.** Nothing in `astrid/sdk`, `astrid/core` or other packs builds an H3 v1 document. The public hook's `_plain_request` builds v1, and CC-1 already changes it to v2.
- **What still uses it is internal:** `compile.py`, `stages.py`, `planner.py` and `spec.py` call the v1 `normalize_request`; `cli.py`, `pack.yaml` required context, `profiles/native-v1.yaml`, `schemas/request.v1.json` and four examples in the skill.
- **Cost of dropping:** tests. A rough pattern count finds about 44 test and fixture files with v1-style documents against 17 with v2. Those need porting or deleting in CC-1.
- **Cost of keeping:** a second schema, a second normalizer and the `operation` route field, kept alive only for callers that do not exist.
- **Verdict:** delete the v1 schema, profile and normalizer in CC-1. A v1 document is refused with "write this as a v2 request". Keep the shared helpers that live in `request.py` (`H3Request`, `H3RequestError`).

### 8. Character Swap's 1 image / 1 video, and adapters in general: Astrid's limit is tighter than the adapter's.

- **What the adapter requires** (model card): the Ref2VA base; the LoRA at strength 1.0; the source performance as `<Video 1>` and the character as `<Picture 1>`; a prompt that names both.
- **What it does not require:** exactly two references. The author's own tool "handles masks, optional scene anchors, source-audio conditioning and continuation history" on the same adapter.
- **Astrid's own additions:** exactly one image and one video; no rectangle or polygon masks; no per-grant strength or seed; no continuation; no combination with a masked edit ("native masked edit does not combine with an adapter"); the schema hard-codes `"id": {"const": "character_swap_v1"}`. Astrid also pins V1 while the card recommends V1.5.
- **General shape.** An adapter is a LoRA in the model chain plus a declared input contract. One row per adapter in the capability table:
  - `id`, file, revision, checksum, default strength;
  - base model it needs;
  - required references by role and tag (Character Swap: `<Video 1>` performance, `<Picture 1>` character);
  - whether further references are allowed (yes, marked untested);
  - a prompt template;
  - tested sampling settings.
- **In the request:** `settings.adapters: [{id, strength}]`, a list, because community use already stacks LoRAs (the BFS swap with a head-swap LoRA). Turbo fits the same row shape and can move there later.
- **Everything else is the ordinary job.** Masks, grants, audio, size and extra references follow the three rules. Character Swap becomes a table row and a template.

## Other arbitrary restrictions noticed

1. **CC-8's description of H3's time chunks is wrong.** It says "Frame 0 is its own chunk; after that, chunks are 4 frames (1–4, 5–8, …)". The node computes frames per token as `FRAME_PER_TOKEN[k % 5]`, and the pack documents the repeating pattern 1, 4, 4, 4, 4. Frames 0, 17, 34, 51, … are each a single-frame chunk. A still placed there holds one frame, not four. `MiniMaxH3CustomKeyframesMasked` states the same rule.
2. **"Native masked edit source windows are limited to 15 s"** (`compile.py`) applies to one shape only. The node accepts up to 3600 frames and notes the trained range is about 124 to 362. Make it one duration row for every job: warn outside the trained range, refuse only past the node's limit.
3. **Per-clip 2 to 15 seconds and 12 files** are model-card facts; the node enforces only a 5-frame minimum and truncates long clips. Label their source so nobody treats them as node errors.
4. **Audio references cannot be trimmed** (`request_v2.py`: `range is unsupported for … references` unless video). Nothing in the node requires this.
5. **CC-7 refuses any grant on the prefix** ("suggesting two jobs"). With masks set by `MiniMaxH3SetAVNoiseMask` this is an Astrid limit, not a model one. Fine to defer; label it a lowering limit.
6. **One continuation block per job** is a scope choice, not a model limit. Fine to keep.
7. **Moving masks are not scaled** (Plan 65), and `ref_image_size` is fixed at `match` though the node offers `max`. Both are Astrid choices; label them.
8. **The reference prompt format matters.** The model card says the hosted Context-IR step that writes structured prompts (`subject_definitions`, `retention_analysis`, …) is "critical" and is not open source. That is a skill and template concern, and probably the largest quality lever not in any plan.

## Limits that are real (keep, with the reason in the table)

- 24 fps only: the V2V and context nodes fix `source_fps` to 24.
- Output length 5 + 17k frames; trained range about 124 to 362.
- Time chunks of 1, 4, 4, 4, 4 frames: a kept span snaps to whole chunks; single-frame pins at multiples of 17.
- Kept audio-video context of 39 + 51k frames; clip offsets on multiples of 17.
- Audio mask resolution of 25 ms; no per-channel audio masking.
- One seed and one global reference set per sampling pass.
- 9 images, 3 videos, 3 standalone audio (node slots); width and height 32 to 16384 in steps of 32.
- Exactness of kept pixels and samples comes from composition, never from the latent mask alone.

## Plan text edits, in priority order

1. **Plan 64 tasks, SR-5 detail.** Replace the bullet "**Generated audio:** … so it's 1 whenever any audio grant generates sound, and 0 otherwise." with: "**Generated audio:** build one audio mask over time from the audio grants (0 on kept and supplied spans, the grant's strength on generated spans) and apply it with `MiniMaxH3SetAVNoiseMask` from the already pinned motion pack, after the V2V node. The model then hears kept and supplied audio while it generates the rest. Any number of audio windows is allowed."
2. **Plan 64 tasks, SR-1 detail.** Replace "Keep the rules that exist today: one audio-changing window per graph, and the agreement multi-region edits already need on image guides, interval, seed and strength." with: "Regions in one pass share one seed and one reference set (one sampler, global conditioning). They may differ in interval and strength: union them into one per-frame mask whose grey level is each region's strength. Several audio windows are allowed (SR-5)."
3. **Plan 66 tasks, CC-8 detail.** Replace "Frame 0 is its own chunk; after that, chunks are 4 frames (1–4, 5–8, …)." with: "Chunks repeat as 1, 4, 4, 4, 4 frames. Frames 0, 17, 34, 51, … are single-frame chunks; every other frame sits in a 4-frame chunk." And replace "At any other frame N, it holds N's whole chunk" with "At a multiple of 17 it holds one frame. At any other frame N it holds N's whole chunk". Add a test case at frame 51.
4. **Plan 64 plan, outcome.** Replace "Source-free generation still requires an image." with: "Generation needs no image: audio or video references with text are documented uses, and text alone is admitted with a dry-run note that it is outside the documented use of the Ref2VA checkpoint." Remove the matching refusal in SR-3, and add a zero-image case to its proof.
5. **Plan 66 tasks, CC-7.** Add to the outcome: "Two placed clips with uncovered time between them compile to `MiniMaxH3MaskedAVBridge` and `MiniMaxH3AssembleBridgeAudio`; a placed clip at a later offset compiles to `MiniMaxH3ExistingVideoMaskedContext` with `insert_frame` and `MiniMaxH3AssembleInterior`. Offsets and kept lengths follow the lattice (multiples of 17; 39 + 51k) and are refused from the table otherwise. Before porting, check whether the prefix case is the same node at `insert_frame` 0; if so, use one lowering for all three." Add cases: A, 60-frame gap, B; a clip placed at frame 51.
6. **Plan 66, CC-1 and completion.** Replace "a v1 request still translates" (plan completion, CC-1 proof, RS1) with "a v1 request is refused with a message to write it as v2; the v1 schema, profile and normalizer are deleted, and tests that used v1 documents are ported or removed, each listed". Change `shared/spec.py (v1 translation only)` to `shared/spec.py (deleted, or reduced to helpers the job needs)`. Make the matching change in Plan 64 SR-1 ("Old raw v1 requests translate").
7. **Plans 64 and 66, non-goals.** Delete "several speakers bound to their own voices" (Plan 64) and "multiple speakers" (Plan 66). Add to Plan 64 SR-7: "State that H3 has no voice-to-face input: binding is prompt text of the form `<Audio 1> is the voice-timbre reference for <Subject 1> (S1)`, documented by the model and untested here."
8. **Plan 64 tasks, SR-2 table.** Replace the row "Character Swap images / videos | 1 / 1" with an adapter row: "Character Swap adapter | needs the Ref2VA base, at least one video (`<Video 1>`, the performance) and at least one image (`<Picture 1>`, the character); further references allowed, untested". Add rows: "Audio grant strength | 0 to 1 (values between untested)"; "Regions per pass | one seed, one reference set".
9. **Plan 66 tasks, CC-1 lowering table and CC-2.** Replace the Adapter row with: "Adapters | each `settings.adapters` entry is a LoRA in the model chain. Its table row declares base model, default strength, required references by tag, prompt template and tested settings. Masks, grants, audio and extra references follow the ordinary rules." In CC-2 add: "Replace the schema's `const: character_swap_v1` with ids read from the table; remove 'masked edit does not combine with an adapter'."
10. **Plan 64 tasks, SR-2 table.** Add a "source" column (node, model card, Astrid) and mark "Per clip 2–15 seconds", "Per modality total 15 seconds" and "Conditioning files 12" as model card; replace the masked edit's 15-second refusal with one duration row for all jobs (warn outside 124 to 362 frames).

Edits 1 to 3 fix things that would otherwise be built wrong. Edits 4 to 9 remove arbitrary limits. Edit 10 is labelling.

## Not established

- Whether continuation at `insert_frame` 0 equals the captured graph's Existing Video path.
- The exact mask tensor shape `MiniMaxH3SetAVNoiseMask` expects for audio; the documentation describes resampling but I did not read the code.
- Quality of anything here: zero-reference Ref2VA, fractional audio strength, bridges, extra references with Character Swap, two bound voices.
