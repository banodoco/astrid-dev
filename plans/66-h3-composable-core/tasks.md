# Tasks — H3 composable core

[Plan](plan.md) · [Inputs](inputs.md)

**Task ids:** `CC-1` … `CC-8`, review stop `RS1`, final review `R`. CC-8 was added later and runs between CC-4 and CC-5.

**Critical path:**
- **Phase 1:** Plans 59, 64 and 65 → CC-1 → RS1 → CC-2 → CC-3 → CC-4 → CC-8 → CC-5 → CC-6.
- **Phase 2:** CC-7 → R.

CC-2's table and CC-3's dry-run view are shared by everything after them, so those tasks run in order, not in parallel.

**Test inventory:** Bare test filenames are under `tests/packs/h3_av/` in astrid-agent. Run them from the Agent checkout with the pinned worker command `env/agent-pytest.sh <paths>`. Run only the files a card names, not the whole suite. Product paths are under `astrid/packs/h3_av/` unless given in full. Cards name functions, not line numbers: find each function with `grep -n` at dispatch. Every task is CPU only (D1). No task claims a machine, rents a GPU or spends money. Request identity was already broken once, in Plan 64 SR-1 (D4). When a task changes an emitted graph, regenerate its fixtures in the same commit and list each change with its reason. Do not add code to preserve an old digest.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| CC-1 One public path: author intent → measured inputs → one resolved job → one compile call | S | Plans 59, 64, 65 | `shared/request_v2.py` (normalization; remove `branch_for`); `shared/spec.py` (deleted, or reduced to helpers the job needs); `shared/prepare.py` (resolve the job once, after measuring inputs, reusing the existing schedule's ownership and overlap checks); `shared/compile.py` (`compile_job(job, bindings, out_dir)`; fold the per-route compilers into ordinary functions it calls); `shared/compose.py` reads intervals and grants from the job; `extensions/vibecomfy.workflows/hooks.py` builds v2 instead of v1; `shared/planner.py` keeps its ordered passes above `compile_job`. Details below. | `test_native_v2_contract.py`, `test_native_masked_edit.py`, `test_character_swap.py`, `test_character_swap_cpu_boundary.py`, `test_compile_generalized.py`, `test_handle_build_compose.py`, `test_spec.py`, `test_planner.py`. The public prompt-and-image invocation, a masked edit, fixed-audio redub and Character Swap each go through preparation, build, composition and receipt on CPU fixtures. A v1 request is refused with a message to write it as v2. The v1 schema, profile and normalizer are deleted, and the tests that used v1 documents are ported or removed, each one listed. `branch_for` and the route selector in the hook and CLI are gone. One combined request that no former route accepted (a placed clip with a region grant and an audio grant, three image references and a speaker clip) compiles, with each lowering present in the graph. `compile_job` chooses lowerings from the features present in the job, never from a classified shape. | [ ] |
| RS1 Review stop after the job contract | S | CC-1 | Read-only | Review the job's lifecycle (what exists before measurement, what preparation freezes, what compile and compose read), v1's removal and the grant fields, on the integrated CC-1 head. Findings become rows `RS1.<n>`; CC-2 onwards depend on this row. | [ ] |
| CC-2 Capabilities in `describe`, refusals from one table | X | RS1 | Plan 64's limits table in `shared/generation.py`, each row labelled by its source: node schema, model card or Astrid restriction. `astrid/core/generation/cli.py` `describe`: keep entry metadata and help, and add a `capabilities` field supplied by the pack. Unsupported combinations become rows with a concrete pair. Replace the schema's `const: character_swap_v1` with adapter ids read from the table, and remove "masked edit does not combine with an adapter". | `test_edit_inputs.py`, `test_real_media_preflight.py`, `test_request_contract.py`, new `test_capabilities.py`. Numeric limits are tested at and past the boundary. Each unsupported pair is refused naming both items and a fix. `describe --entry h3 --json` `capabilities` equals the table admission uses. No refusal an agent sees names an internal class or route (`LanPaint`, `SPEC-MIN`, node class names). Malformed, missing and corrupted inputs keep their own messages where they're read. | [ ] |
| CC-3 The dry run and the settled result show one resolved-job view | N | CC-2 | `shared/stages.py` `_sealed_plan` (extend it; keep publication selectors, workflow checksums and the plan and compilation handles); the workflow hooks; `astrid/sdk/results.py` result reconstruction. Replaces the slices Plan 64 SR-6 and Plan 65 DS-4 added. | `tests/core/generation/test_catalog_entries_dry_run.py`, `test_parent_receipt_readback.py`, `tests/sdk/test_generation_result_refs.py`. One fixture whose grant crosses the frame-4 boundary shows three separate fields: the requested grants, the effective video latent influence (token widths 1, 4, 4, 4, 4) and the delivered ownership as frame and sample intervals. The fixture also shows canvas, sampled and delivered frames, reference rows with tags and mechanisms. The settled result shows the same view after scratch cleanup. | [ ] |
| CC-4 Guides: soft image, clip or audio at a frame | X | CC-3 | `schemas/request.v2.json` and `shared/request_v2.py`: a new `role: guide` (timeline items stay exact; `hard` and `latent_pin` are read as today); `shared/generation.py`: one function that chains `MiniMaxH3AddGuide` per guide; capability rows; the guide's dry-run fields. Details below. | `test_generation.py`, `test_native_v2_contract.py`. Separate cases: a last-frame still; an interior clip; a clip that would overrun the canvas (refused); audio cropped to the remaining ticks; image and audio guides at the same frame; a guide beside an exact placement. An off-lattice shot where the sampled and delivered ends differ binds `at: -1` to the last delivered frame. The dry run lists each guide as soft. | [ ] |
| CC-8 Exact stills at any frame | X | CC-4 | `shared/prepare.py` (build the source from placed stills and gaps); `shared/generation.py` (freeze each still's H3 time chunk in the noise mask); `shared/compose.py` (paste kept pixels from each placed item at its own span and offset, instead of from one source at one offset); capability rows; the still's dry-run fields. Details below. | `test_native_masked_edit.py`, `test_handle_build_compose.py`, `test_native_v2_contract.py`. Separate cases: a still at frame 0; a still at frame 51 (a single-frame chunk); a still at frame 61; a still at the last delivered frame; stills at both 0 and the end with generated time between. Use different first, last and stand-in pixels. Decoded output equals each still on its held frames; generated frames come from the stand-in; audio is generated. The dry run shows each still's snapped hold. Two exact items over the same frames are refused. | [ ] |
| CC-5 Templates: list, show, fill, write, submit | X | CC-8, Plan 59 | Recipe files under `docs/recipes/` in the H3 pack; `astrid/core/generation/cli.py`: `generate templates list`, `generate templates show NAME`, and `generate video --entry h3 --template NAME (--set hole=value … \| --from-shot SHOT) [--write FILE] [--dry-run]`. Fill contract below. `NAME` may be a recipe name or a file path. `templates list` shows the H3 recipes and any template an installed skill ships in its own `recipes/` folder. An agent-written file is filled and checked the same way. No shot-plan schema change and no automatic take recording. | `test_skill_examples_admitted.py` rewritten to load the installed recipe files instead of extracting YAML from the skill, keeping its compiled-graph and mask-byte assertions. Each recipe is filled with fixture values (a quoted line of dialogue, a list of references, a numeric duration, one reused shot occurrence), then normalizes, dry-runs and compiles. An unfilled hole is refused with its name and where it should come from. A `--write` file submits unchanged through the ordinary request path. | [ ] |
| CC-6 Rewrite the general H3 skill and thin Recast | T | CC-5 | `docs/SKILL.md`: v2 only (the three rules, item kinds, reading a dry run and `describe`, and the recipes by template name). Runtime, resume, attestation and checksum material moves to `docs/reference.md`. Update the required context in `pack.yaml`. `docs/recast-scene/SKILL.md`: keep method choice, order of work and checks, plus its pitfalls (choosing cuts, checking the last spoken word, inspecting mask edges, avoiding doubled lead-in, getting approval); replace request mechanics with template names; ship `docs/recast-scene/brief.md`, a brief template listing each shot's steps by template name. Keep the silent-reaction workaround (#863) unless a shipped recipe reproduces a four-frame hold with silent delivered audio. | `test_skill_examples_admitted.py`, `tests/test_pack_declared_skills.py`. One cold read: a new agent with no context uses the skill to find the right recipe for a described shot, fills it, hits one missing value, fixes it from the refusal and reaches a dry run. Record the transcript. | [ ] |
| CC-7 Continue by placement through a ported motion-context stage, and delete the captured workflows | S | CC-6 | `shared/generation.py`: one function for the case "one bounded, unchanged video prefix placed at frame 0 and one generated suffix", porting the captured graph's active Existing Video path; `shared/timing.py` (reuse); `shared/prepare.py` and `shared/compose.py` continuation intervals. Delete `workflows/native_h3_continuation*/` and the `continuation` request flag. Details below. | `test_continuation_timing.py`, `test_compile_generalized.py`, `test_native_v2_contract.py`. Migrate or delete `test_workflow_pair.py`, `test_workflow_model_urls.py`, `test_runtime_declaration_sync.py` and `test_release_runtime_guard.py`, listing each assertion kept or dropped. Cases are listed below. | [ ] |
| R Review rounds (at most 1, recommended) | S | CC-7 | Integrated result, read-only, high-judgment reviewer. | Check the CPU proofs against the plan's completion list and the owner decisions. Findings become rows `R1.<n>` under the [run contract](../../skills/shared/run-contract.md); closing waits for them. | [ ] |

## CC-1 detail

**Lifecycle.**
- **Normalize:** turns the author's request into intent. It holds no paths and no generated files.
- **Prepare:** measures the inputs and resolves the job once.
- **Compile:** reads the job, the prepared file bindings and an output directory.
- **Compose:** reads the job's intervals and grants.

Paths and generated artifacts never enter the request identity.

**The job** is Plan 64's `GenerationInputs`, with these fields:
- `canvas`;
- `placed`: exact items, with their occurrence, span and source offset;
- `grants`: each grant keeps together its stream, interval, occurrence, optional region raster (white means *edit*, as today), strength, seed and associated references;
- `conditioning`: reference rows, and guides from CC-4;
- `prompt`, `model` (base and adapter), `sampling`.

Two grants that need different sampler settings are refused from the table.

**Lowerings, as ordinary functions `compile_job` calls:**

| Job feature | Mechanism |
| --- | --- |
| References | `MiniMaxH3ReferenceToVideo` slots and prompt tags |
| Placed video or still with video grants | source latent and `H3V2VGranularFractionalDenoise` noise mask, then composition paste-back |
| Audio grants | `audio_strength` 1 when any audio is generated; supplied fixed audio spliced exactly on its own interval |
| Adapters | Each `settings.adapters` entry is a LoRA in the model chain. Its table row declares the base model, default strength, required references by tag, prompt template and tested settings. Masks, grants, audio and extra references follow the ordinary rules. Character Swap is the first row; keep its reference order, binding and verification. |
| Guides | CC-4 |
| Generated suffix after a placed prefix | Selected by shape: one unchanged video prefix at frame 0 and uncovered time after it. In phase 1 this calls the captured bundle; CC-7 swaps in the ported stage. The `continuation` flag is accepted and ignored from CC-1, and removed from the schema in CC-7. No recipe or skill text uses it. |

Trace `_compile_lanpaint`. If nothing reaches it after Plans 64 and 65, delete it. If something does, give it a positive CPU case or replace it with a refusal from the table.

## CC-4 detail

- **`role: guide`** is the only soft placed item. Timeline media stay exact, whether `hard` is omitted or false, so old requests keep their meaning.
- **`edit.guides`** keeps its existing meaning: it points at reference occurrences.
- **`at: -1`** means the last delivered frame. Resolve it to a sampled index before binding the node.
- **Clip guides** follow the node's rules:
  - 2–4 frames contribute one image;
  - longer clips round down to 5, 22, 39 and so on;
  - a clip that doesn't fit from its index is refused.
- **Audio guides** need the audio VAE and are cropped to the remaining ticks. The dry run shows the crop.
- **Two exact owners** of the same stream and span are refused. A guide beside an exact placement is allowed.
- **Recipes this enables:** a guided end, or soft keyframes. For exact stills at any frame, see CC-8.

## CC-8 detail

- **How H3 chunks time.** Chunks repeat as 1, 4, 4, 4, 4 frames. Frames 0, 17, 34, 51, … are single-frame chunks; every other frame sits in a 4-frame chunk. The model can only be told to keep a whole chunk.
- **A placed still** at frame 0, or any multiple of 17, holds one frame. At any other frame N it holds N's whole chunk, snapped to the chunk containing N, so the picture holds for 4 frames (about 1/6 s). The dry run shows the snapped hold. The request can say `hold: chunk` (the default) or `hold: frame`. With `hold: frame`, composition pastes only frame N, the model generates the rest of its chunk, and the dry run warns that a small jump is possible.
- **Composition** pastes each placed item from its own source at its own span, keyed by occurrence. This replaces "one authoritative source at one offset". Video clips, stills and fixed audio all use the same paste.
- **Recipes this enables:** start and end on exact images (bridge); exact keyframes mid-shot.
- **Not in this task:** exact stills inside a continuation prefix (CC-7).

## CC-5 fill contract

- **A recipe** is a v2 request with `${name}` holes, plus a header listing each hole's type, units, help, and the brief field or `--set` argument that supplies it.
- **Ranges** say whether they're relative to the media or to the shot.
- **Filling** substitutes typed JSON values. No conditionals and no expressions; a variant is another file.
- **`--from-shot`** selects project, timeline and shot, requires an occurrence when the choice changes the time span, and resolves media through the ordinary asset-map path.
- **Editorial choices stay with the agent:** which voice slice, and drawing the mouth mask.
- **A filled template is just a request.** `--write` saves it, and it submits like any other request. There is no separate template submission path.
- **Discovery:** `templates list` shows each recipe's name and one-line purpose. `templates show` prints its holes.

## CC-7 detail

**Outcome.** Given one bounded, unchanged video prefix placed at frame 0, with usable audio-video context and a later requested end, Astrid generates one audio-video suffix:
- the prepared prefix is delivered exactly;
- it uses the existing timing function, the requested canvas and the effective references;
- incompatible edits are refused before claim, naming the offending item.

**Other placements.** Two placed clips with uncovered time between them compile to `MiniMaxH3MaskedAVBridge` and `MiniMaxH3AssembleBridgeAudio`. A placed clip at a later offset compiles to `MiniMaxH3ExistingVideoMaskedContext` with `insert_frame`, plus `MiniMaxH3AssembleInterior`. Offsets and kept lengths follow the node's lattice (multiples of 17; 39 + 51k frames) and are refused from the table otherwise. Before porting, check whether the prefix case is the same node at `insert_frame` 0. If it is, use one lowering for all three. Add cases: clip A, a 60-frame gap, clip B; a clip placed at frame 51.

**Before writing code,** list each difference between the ported graph and the captured graph's **active** Existing Video path. Compare inputs, edges, weights, settings, seeds and outputs, and give each difference a reason. Bypassed branches and preview nodes don't count. The capture duplicates one image into two slots; the port uses one effective reference, which is an intended difference. The 0.5 MP selector goes, and the canvas size replaces it.

**Refusals.**
- A region edit, full-frame regeneration, regenerated prefix audio or fixed replacement on the prefix is refused, pointing at the grant and suggesting two jobs.
- A soft reference or guide is allowed, because it grants no permission to change source pixels.
- A prefix with fewer than 39 usable frames, a prefix with no audio, or an offset source trim each has a stated result.
- A still-only start belongs to Plan 64 SR-4.
- Timed guides that can't be mapped to the sampled segment are refused.

**Cases.**
- The existing 120-frame prefix plus 24 new frames: a 73-frame raw extension, 39 context frames, 34 frames of capacity, 10 trimmed.
- 38 and 39-frame prefixes.
- One image versus two independent references.
- Three images plus a speaker clip at 512×288.

Check the effective reference tags, the sound binding, and the shared size of the source decode, target and mux input. Prove the delivered prefix pixels and PCM against a contrasting stand-in across the seam, through the existing composition path.

**Not in this task:** more than one extension block per job. An endless-continuation skill submits bounded jobs one after another.
