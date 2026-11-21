# Tasks — H3 guides and exact stills

[Plan](plan.md) · [Inputs](inputs.md)

**Task ids:** `CC-4`, `CC-8`, `CC-11`. CC-4 and CC-8 keep the ids they had in Plan 66, so research files and other plans still resolve.

**Critical path:** Plan 66 → CC-4 → CC-8 → CC-11.

**Test inventory:** Bare test filenames are under `tests/packs/h3_av/` in astrid-agent. Run them from the Agent checkout with the pinned worker command `env/agent-pytest.sh <paths>`. Run only the files a card names, not the whole suite. Product paths are under `astrid/packs/h3_av/` unless given in full. Cards name functions, not line numbers: find each function with `grep -n` at dispatch, and re-check each caller and test list against the integrated code then. Every task is CPU only (D1). No task claims a machine, rents a GPU or spends money. Request identity was already broken once, in Plan 64 SR-1 (D4). When a task changes an emitted graph, regenerate its fixtures in the same commit and list each change with its reason. Do not add code to preserve an old digest.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| CC-4 Guides: soft image, clip or audio at a frame | X | Plan 66 | `schemas/request.v2.json` and `shared/request_v2.py`: a new `role: guide` (timeline items stay exact; `hard` and `latent_pin` are read as today); `shared/generation.py`: one function that chains `MiniMaxH3AddGuide` per guide; capability rows; the guide's dry-run fields. Details below. | `test_generation.py`, `test_native_v2_contract.py`. Separate cases: a last-frame still; an interior clip; a 1-frame image guide; a clip that would overrun the canvas (refused); audio cropped to the remaining ticks; an audio guide starting past the audio track (refused); image and audio guides at the same frame; a guide beside an exact placement. An off-lattice shot where the sampled and delivered ends differ binds `at: -1` to the last delivered frame. The dry run lists each guide as soft. | [ ] |
| CC-8 Exact stills at any frame | X | CC-4 | `shared/prepare.py` (build a full-canvas source from placed stills and gaps); `shared/generation.py` (freeze each still's H3 time chunk in the noise mask); composition by occurrence comes from Plan 66 CC-10; capability rows; the still's dry-run fields. Details below. | `test_native_masked_edit.py`, `test_handle_build_compose.py`, `test_native_v2_contract.py`. Separate cases: a still at frame 0; a still at frame 51 (a single-frame chunk); a still at frame 61; a still at the last delivered frame, in a request whose rounded H3 length is longer than the delivered length; stills at both 0 and the end with generated time between. Use different first, last and stand-in pixels. Decoded output equals each still on its held frames; generated frames come from the stand-in; audio is generated. The dry run shows each still's requested frame, snapped chunk, delivered hold, occurrence and source offset. Two exact items over the same frames on the same stream are refused. Two stills whose holds fall in one latent chunk (for example frames 61 and 62, both in `[60,64)`) are refused, naming both. Exactness is checked as in [Exact delivery](../66-h3-composable-core/tasks.md#functional-additions-exact). | [ ] |
| CC-11 Recipes and skill section for guides and stills | T | CC-4, CC-8 | Recipe files under `astrid/packs/h3_av/docs/recipes/` for a guided end, soft keyframes, start and end on exact images, and an exact mid-shot keyframe. One short section and one kinds-table row each in `docs/SKILL.md`, within the [skill guards](../66-h3-composable-core/tasks.md#skill-guards). Flip the `role: guide` and off-zero still rows from `unavailable` in the table, and amend `docs/design.md` in the same change. | `test_skill_examples_admitted.py`, `tests/test_pack_declared_skills.py`, and the skill-guard tests. Re-run the standing cold read plus one ask for a start-and-end-image shot. | [ ] |

## CC-4 detail

- **`role: guide`** is the only soft placed item: an image, video or audio occurrence at a zero-based 24 fps frame (`at.seconds` converts to that frame grid). Timeline media stay exact, whether `hard` is omitted or false, so old requests keep their meaning.
- **`edit.guides`** keeps its existing meaning: it points at reference occurrences.
- **`at: -1`** means the last delivered frame. Preparation resolves it to `delivered_frame_count - 1` and binds that positive index. Never pass `-1` to the node: the node resolves negative indices against the sampled latent, which can include trimmed frames.
- **Wiring:** chain one `MiniMaxH3AddGuide` per guide, in normalized occurrence order. Each reuses the same target latent and feeds its output conditioning to the next. Connect the video VAE for image and video guides, and the audio VAE for audio guides.
- **Clip guides** follow the node's rules:
  - 1–4 frames use only the first frame;
  - 5 or more frames are cropped down to the largest of 5, 22, 39 and so on;
  - a retained clip that runs past the target is refused.
- **Audio guides** are cropped to the remaining 40 Hz latent ticks. One starting past the audio track is refused.
- **The dry run** records the requested position, the resolved frame, the retained image-frame count and the audio crop.
- **Exact owners.** Guides are soft conditioning only; exact delivered pixels or samples come from composition. A guide may share a frame with an exact placement. Two exact owners of the same stream and span are still refused.
- **One function.** Keep the guide lowering as one function that takes the ordered guides and returns conditioning, so a later schedule over denoising progress wraps it without changing it. Two guides of the same type on one frame are refused.
- **Recipes this enables:** a guided end, or soft keyframes. For exact stills at any frame, see CC-8.

## CC-8 detail

Composition reads the ownership map and the media files, and imports nothing else from the pack.

- **How H3 chunks time.** The model's video latent uses frame chunks of 1, 4, 4, 4, 4, repeating (`comfy/ldm/minimax/model.py` `FRAME_PER_TOKEN`). The chunks are `[0,1)`, `[1,5)`, `[5,9)`, `[9,13)`, `[13,17)`, then the pattern repeats from 17. So frames 0, 17, 34, 51, … are single-frame chunks, and every other frame sits in a 4-frame chunk; frame 61, for example, is in `[60,64)`. The V2V mask takes the maximum over each chunk, so the model can only be told to keep a whole chunk.
- **`hold: chunk` (the default).** A placed still at a single-frame chunk holds one frame. At any other frame N, it snaps to the chunk containing N and holds for 4 frames, about 1/6 s. At the end of the output, the delivered hold is clipped to the last delivered frame, while the full latent chunk stays frozen.
- **`hold: frame`.** Keep the chunk's other frames generatable: place the still as a soft guide at N and paste it exactly on frame N alone. The dry run warns that a small jump is possible. Do not freeze the whole chunk and then call its other frames generated.
- **Preparation** builds a full-canvas source at the target size, from the placed stills and any declared source media. Gaps can hold stand-in pixels, because composition supplies the final generated pixels there. Keep the requested, H3-rounded and delivered frame counts separate, and never treat padding frames as delivered.
- **Composition** uses Plan 66 CC-10 (by occurrence, with exact delivery). A still's one frame repeats over its delivered span; a still never owns audio.
- **Refusals.** Two exact owners of the same stream are refused, even if they come from the same asset.
- **The dry run** lists each still's requested frame, snapped chunk, delivered hold, occurrence and source offset.
- **Recipes this enables:** start and end on exact images; exact keyframes mid-shot.
- **Not in this task:** exact stills inside a continuation prefix ([Plan 70](../70-h3-continuation-bridges-inserts/tasks.md) CC-7a).
