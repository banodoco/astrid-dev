# Tasks — H3 composable core

[Plan](plan.md) · [Inputs](inputs.md)

**Task ids:** `CC-1.1` … `CC-1.4`, `CC-2` … `CC-6`, `CC-7a` … `CC-7d`, `CC-8`, review stop `RS1`, final review `R`. CC-8 was added later and runs between CC-4 and CC-5.

**Critical path:**
- **Phase 1:** Plans 59, 64 and 65 → CC-1.1 → CC-1.2 → CC-1.3 → CC-1.4 → RS1 → CC-2 → CC-3 → CC-9 → CC-4 → CC-8 → CC-5 → CC-6.
- **Phase 2:** CC-7a → (CC-7b, CC-7c in parallel) → CC-7d → R.

Each CC-1 card can be merged on its own and leaves the public invocation working. CC-2's table and CC-3's dry-run view are shared by everything after them, so those tasks run in order, not in parallel.

**Test inventory:** Bare test filenames are under `tests/packs/h3_av/` in astrid-agent. Run them from the Agent checkout with the pinned worker command `env/agent-pytest.sh <paths>`. Run only the files a card names, not the whole suite. Product paths are under `astrid/packs/h3_av/` unless given in full. Cards name functions, not line numbers: find each function with `grep -n` at dispatch, and re-check each caller and test list against the integrated code then. Every task is CPU only (D1). No task claims a machine, rents a GPU or spends money. Request identity was already broken once, in Plan 64 SR-1 (D4). When a task changes an emitted graph, regenerate its fixtures in the same commit and list each change with its reason. Do not add code to preserve an old digest.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| CC-1.1 Freeze one resolved job after measuring inputs | S | Plans 59, 64, 65 | `shared/prepare.py` (`prepare_request`: measurement, ownership and overlap validation); the job type, which is Plan 64's `GenerationInputs` in `shared/generation.py`, extended only with the fields below; `shared/compose.py` reads the job's intervals and grants; `shared/planner.py` keeps its ordered passes above the compiler; `shared/stages.py` persists and reloads the prepared job. Today's compile entry points stay and temporarily adapt the job to their existing inputs. | `test_edit_inputs.py`, `test_real_media_preflight.py`, `test_planner.py`, `test_handle_build_compose.py`. Preparation measures each input once. It refuses two exact owners of the same stream and span, and two grants needing different shared sampler settings, before compilation, naming both grants and the conflicting field. The job serializes and reloads unchanged, its request digest is checked on reload, and composition reads its intervals and grants. No path or generated file appears in the request identity or the job's intent. | [ ] |
| CC-1.2 Make `compile_job(job, bindings, out_dir)` the only compiler entry point | S | CC-1.1 | `shared/compile.py` (`compile_job`; the former `_compile_generation`, `_compile_native_masked_edit` and `_compile_character_swap_v2` become feature lowerings it calls); `shared/generation.py` builder interface only as needed. The normalized request and the hook and CLI inputs stay as they are in this card; adapters at the compiler boundary turn them into a job. v1 stays for now. | `test_native_masked_edit.py`, `test_character_swap.py`, `test_character_swap_cpu_boundary.py`, `test_compile_generalized.py`, `test_handle_build_compose.py`. Each supported lowering is reached through `compile_job`. Bindings and graph inputs match today's for source-free prompt-and-reference generation, masked edit and Character Swap. | [ ] |
| CC-1.3 Route every public and lifecycle caller through `compile_job` | X | CC-1.2 | `extensions/vibecomfy.workflows/hooks.py` (builds v2 instead of v1); `shared/stages.py` (`_sealed_plan` and the compile call); `shared/planner.py` (`plan_request` ordered passes); `astrid/core/generation/cli.py` only if it dispatches H3 compilation directly (trace the normal generate call first). Callers to migrate are listed below. | `test_native_v2_contract.py`, `test_planner.py`, `test_handle_build_compose.py`, `test_character_swap_cpu_boundary.py`, and the hook and CLI tests found at dispatch. Trace normalize → prepare → `compile_job` → compose → receipt for the public prompt-and-image invocation, a masked edit, a fixed-audio redub and Character Swap. A repository search shows no per-route compiler is called outside `compile_job`. One combined request that no former route accepted (a placed clip with a region grant and an audio grant, three image references and a speaker clip) compiles. Assert the concrete graph inputs for the source, region mask, reference slots and tags, speaker clip, audio grant and composition intervals. If a pair can't be combined yet, it gets a named capability refusal rather than a claim of composition. | [ ] |
| CC-1.4 Remove v1 and route classification | S | CC-1.3 | `shared/request.py` (v1 schema, profile and normalizer); `shared/request_v2.py` (`branch_for` and route classification); `shared/spec.py` (delete `H3Spec` and `canonical_spec` once their callers have moved; keep only helpers used elsewhere); `shared/compile.py` (delete obsolete route compilers and the CC-1.2 adapters); `schemas/request.v1.json` and the v1 profile files; hooks, CLI, planner, stages, and every test and fixture still using v1 or `H3Spec`. | `test_request_contract.py`, `test_native_v2_contract.py`, `test_spec.py` (migrated or deleted, with each assertion's fate listed), `test_planner.py`, `test_compile_generalized.py`, `test_character_swap.py`, `test_handle_build_compose.py`, `test_cli.py`, `test_skill_examples_admitted.py`, `test_edit_binding.py`, `test_runtime_declaration_sync.py`. A v1 request is refused at the public request loader, before preparation, with: `Request version 1 is no longer supported; rewrite it as request v2.` There is no v1-to-v2 conversion. No route selector or `branch_for` remains. Every supported example compiles through `compile_job`. | [ ] |
| RS1 Review stop after the job contract | S | CC-1.4 | Read-only. One round. | Review the integrated head containing CC-1.1 to CC-1.4 after all four merge, not an intermediate adapter state; record its commit and the Plan 59, 64 and 65 bases. Trace input document → normalized intent → measured bindings → resolved job → compilation → composition → settled result. For each boundary list the fields allowed, the fields forbidden, the digest checked and where refusals happen. Confirm v1 is refused everywhere and nothing v1 is reachable. Confirm each grant keeps its stream, interval, occurrence, optional region raster and polarity, strength, seed and reference identity through prepare, compile and compose. Trace at least one generated-only, one placed-with-edit, one fixed-audio and one adapter job. Review the code; don't run checks. Each finding becomes a row `RS1.<n>` with owner, scope, proof and a dependency on RS1. CC-2 waits until no contract defect is open: it depends on the last finding row, or on RS1 if there are none. | [ ] |
| CC-2 Capabilities in `describe`, refusals from one table | X | RS1 | Extend the `LIMITS` table Plan 64 SR-2 added in `shared/generation.py`; do not create a second table. Key it by **lever kind** (place, edit, guide, reference, prompt, LoRA, control, settings). Each kind lists its family (Output, Context or Process), the shared fields it accepts (`asset`, `at`, `during`, `range`, `stream`, `mask`, `strength`, `phase`) with their defaults, its own `params`, its limits and its conflicts. `describe` prints kinds in that shape. Every row gets `source_kind` (`node_schema`, `model_card` or `astrid_rule`) and `source_ref` (a pinned schema path and property, a model-card section, or a task or rule id). A row without a verifiable source is an Astrid rule. An unsupported combination is a row naming a pair of request features (for example `adapter=character_swap` plus `audio_guide`), with a reason and a fix. `astrid/core/generation/cli.py`: add a `capabilities` object to the existing JSON from `generate describe --entry h3 --json`, holding exactly the rows and refusal pairs admission uses; keep the existing entry metadata and help. Adapter ids come from the table: the pack validator checks table membership, and the checked-in JSON Schema keeps only a structural string rule (JSON Schema can't read the Python table). Remove the hard-coded adapter refusal in the masked compiler; the table decides that pair. | `test_edit_inputs.py`, `test_real_media_preflight.py`, `test_request_contract.py`, new `test_capabilities.py` (table and admission agree; CLI JSON serialization). Each numeric row is tested at its limit and one value past it, with its `source_ref` in the assertion message. Each unsupported pair is refused, naming both features by their request labels and giving one fix. `capabilities` in `describe` equals the table admission uses. No refusal an agent sees names an internal class or route (`LanPaint`, `SPEC-MIN`, node class names). Malformed, missing and corrupted inputs keep their own messages where they're read. | [ ] |
| CC-3 The dry run and the settled result show one resolved-job view | N | CC-2 | `shared/stages.py` `_sealed_plan`: serialize the resolved job as the single view, keeping every existing field used for publication selection, workflow checksum checks, the plan handle and the compilation handle; the workflow hooks; `astrid/sdk/results.py` result reconstruction (`_reconstruct_generation_result`, read by `astrid/sdk/generation.py`). This extends the view Plan 64 SR-6 started and replaces Plan 65 DS-4's size reporting. At dispatch, compare the merged `_sealed_plan` and both earlier proofs; keep their asserted fields unless replaced here, and list each changed fixture field with its reason. | `tests/core/generation/test_catalog_entries_dry_run.py`, `test_parent_receipt_readback.py`, `tests/sdk/test_generation_result_refs.py`, and a hook test showing the dry run and the submitted result use the same serializer. All intervals are half-open: video in frame indices `[start, end)`, audio in sample indices `[start, end)`, with any seconds shown with units. A fixture whose grant crosses the frame-4 boundary shows three separate fields: the requested grants; the effective video latent spans, from H3's chunk rule (one 1-frame chunk, then 4-frame chunks, repeating every 17 frames); and the delivered ownership. It also shows the requested canvas, the raw sampled frame count, the delivered frame count after trimming (from the existing timing helpers), and each reference occurrence with its tag, modality, purpose and mechanism, without local paths. The settled result stores the view before scratch is deleted, and reconstructing it afterwards gives the same view without reading deleted paths. | [ ] |
| CC-9 End-relative time and timed prompts | X | CC-3 | `shared/request_v2.py` normalization and `schemas/request.v2.json`: negative numbers and `end` in `at`, `during` and `range`. `at`/`during` resolve against the job's `duration`, and `range` against the measured source length, inside CC-1.1's resolve step. `prompt` may be one string or a list of `{during, text}`; the list lowers to one prompt in H3's own timed shot format (`[Shot n] At 00:03.000, …`, checked against the model's prompt guide at dispatch). Capability rows say timed prompts are soft. The dry run shows every resolved time and the final prompt string. Prompt tags (`<Picture n>` and so on) are given to references only, never to placed items or guides. | `test_native_v2_contract.py`, `test_request_contract.py`, new `test_time_and_prompt.py`. Cases: `range: [-2, end]` on a 6.3 s file resolves to [4.3, 6.3]; `at: -2` and `at: end` on a 7 s job; `during: [-2, end]`; a time past the end is refused naming the item; a two-segment prompt serializes in time order; a tag naming a placed item is refused. | [ ] |
| CC-4 Guides: soft image, clip or audio at a frame | X | CC-9 | `schemas/request.v2.json` and `shared/request_v2.py`: a new `role: guide` (timeline items stay exact; `hard` and `latent_pin` are read as today); `shared/generation.py`: one function that chains `MiniMaxH3AddGuide` per guide; capability rows; the guide's dry-run fields. Details below. | `test_generation.py`, `test_native_v2_contract.py`. Separate cases: a last-frame still; an interior clip; a 1-frame image guide; a clip that would overrun the canvas (refused); audio cropped to the remaining ticks; an audio guide starting past the audio track (refused); image and audio guides at the same frame; a guide beside an exact placement. An off-lattice shot where the sampled and delivered ends differ binds `at: -1` to the last delivered frame. The dry run lists each guide as soft. | [ ] |
| CC-8 Exact stills at any frame | X | CC-4 | `shared/prepare.py` (build a full-canvas source from placed stills and gaps); `shared/generation.py` (freeze each still's H3 time chunk in the noise mask); `shared/compose.py` (paste kept pixels from each placed item at its own span and offset, keyed by occurrence, instead of from one source at one offset); capability rows; the still's dry-run fields. Details below. | `test_native_masked_edit.py`, `test_handle_build_compose.py`, `test_native_v2_contract.py`. Separate cases: a still at frame 0; a still at frame 51 (a single-frame chunk); a still at frame 61; a still at the last delivered frame, in a request whose rounded H3 length is longer than the delivered length; stills at both 0 and the end with generated time between. Use different first, last and stand-in pixels. Decoded output equals each still on its held frames; generated frames come from the stand-in; audio is generated. The dry run shows each still's requested frame, snapped chunk, delivered hold, occurrence and source offset. Two exact items over the same frames on the same stream are refused. | [ ] |
| CC-5 Templates: list, show, fill, write, submit | X | CC-8, Plan 59 | Recipe files under `astrid/packs/h3_av/docs/recipes/`, plus each installed skill's own `recipes/` folder; `astrid/core/generation/cli.py`: `generate templates list`, `generate templates show NAME`, and `generate video --entry h3 --template NAME (--set hole=JSON … \| --from-shot SHOT) [--write FILE] [--dry-run]`. Fill contract below. No shot-plan schema change and no automatic take recording. | `test_skill_examples_admitted.py` rewritten to load the installed recipe files instead of extracting YAML from the skill, keeping its compiled-graph and mask-byte assertions. Each recipe is filled with typed fixture values (a quoted line of dialogue, a list of references, a numeric duration, one reused shot with an explicit occurrence), then normalizes, dry-runs and compiles. Refusals, each naming the hole and its declared source: a missing fill, an unknown hole, a duplicate fill, a type mismatch, a leftover marker. An ambiguous bare name is refused, listing the qualified choices. A `--write` file submits unchanged through the ordinary request path. | [ ] |
| CC-6 Rewrite the general H3 skill and thin Recast | T | CC-5 | `docs/SKILL.md` starts from [research/skill-draft.md](research/skill-draft.md), which a small model learned cold in two rounds ([research/haiku-tests.md](research/haiku-tests.md)); keep it at about that length. Also `docs/reference.md`, `pack.yaml`, `docs/recast-scene/SKILL.md`, `docs/recast-scene/brief.md`. Details below. | `test_skill_examples_admitted.py` (reads the installed recipe files, not YAML copied from either skill), `tests/test_pack_declared_skills.py`. Cold read: re-run the five asks in research/haiku-tests.md with a small model that can now call `describe` and `--dry-run`, and record each result. Then one more: a new agent with no context uses the skill to find the right recipe for a described shot, fills it, hits one missing hole, fixes it from the refusal and reaches a dry run. Record the shot description, chosen recipe, the refusal and its named source, the corrected fill and the dry-run handle. Keep the transcript free of secrets and machine claims. | [ ] |
| CC-7a Prefix continuation: one unchanged video prefix at frame 0 plus one generated suffix | S | CC-6 | `shared/generation.py` (one function for the prefix case, porting only the captured graph's active `start_mode='existing_video'` path: source frames and audio → `MiniMaxH3ExistingVideoMaskedContext` with `insert_frame=0` → `MiniMaxH3AssembleExtension`; not the generated-starter branch); `shared/timing.py` (reuse); `shared/prepare.py` and `shared/compose.py` continuation intervals. The captured workflows stay in place until CC-7d. Details below. | `test_continuation_timing.py`, `test_compile_generalized.py`, `test_native_v2_contract.py`. Cases listed below. Assert node inputs and edges, one shared size and 24 fps across source decode, target, assembler and mux, reference tags, the source audio binding, and exact prefix pixels and PCM through composition against a contrasting stand-in. No claim of output-quality parity. | [ ] |
| CC-7b Bridge between two placed clips | S | CC-7a | `shared/generation.py` (bridge lowering with `MiniMaxH3MaskedAVBridge` and `MiniMaxH3AssembleBridgeAudio`; not routed through the existing-video context node); `shared/prepare.py` (the gap and two kept intervals); `shared/compose.py`. | `test_compile_generalized.py`, `test_handle_build_compose.py`, `test_native_v2_contract.py`. The smallest symmetric bridge: a 39-frame kept tail of clip A, 63 generated frames, then a 39-frame kept head of clip B, for a 141-frame target. Verify the placement and ownership intervals, the generated middle, the bridge audio wiring and the exact composition of both clips. Refusals: either kept context not 39 + 51k frames; no generated middle; a timeline that can't map onto a valid H3 run. Never silently enlarge or shrink the user's gap. With the Character Swap adapter on, the graph has both the adapter LoRA and the Turbo LoRA in the model chain feeding the sampler, and the bridge nodes are unchanged. Inspect the graph only; no inference-quality claim. | [ ] |
| CC-7c Insert a placed clip between generated time | S | CC-7a | `shared/generation.py` (insert lowering: `MiniMaxH3ExistingVideoMaskedContext` with a nonzero `insert_frame`, sharing CC-7a's context helper, then `MiniMaxH3AssembleInterior`); `shared/prepare.py`; `shared/compose.py`. | `test_compile_generalized.py`, `test_handle_build_compose.py`, `test_native_v2_contract.py`. An insert at frame 51 compiles, with the node's snapped `insert_frame` and `preserved_frames` outputs wired into `MiniMaxH3AssembleInterior` and the same crop, fps and source mapping as the context. Generated time exists on both sides. Exact source pixels and PCM are delivered over the insert. A requested offset that isn't a multiple of 51 (for example 34, or 50) is refused before compilation, with no silent snapping. A clip that doesn't fit the target is refused. | [ ] |
| CC-7d Delete the captured continuation workflows and the `continuation` flag | S | CC-7a, CC-7b, CC-7c | `workflows/native_h3_continuation*/`; the captured-workflow dispatch in `shared/compile.py`; the `continuation` field in `schemas/request.v2.json` and `shared/request_v2.py`; `test_workflow_pair.py`, `test_workflow_model_urls.py`, `test_runtime_declaration_sync.py`, `test_release_runtime_guard.py`; continuation fixtures and their references. Deletion follows CPU proof alone (D3). Remove the flag only after a repository search shows no live caller depends on it. | Those four test files, plus `test_continuation_timing.py` and `test_native_v2_contract.py`. List every old assertion as kept, replaced or dropped. Keep the assertions that still protect runtime declarations and bundle integrity, now against the new graph. No captured bundle is selectable afterwards. Prefix, bridge and insert all compile through the shared lowerings. | [ ] |
| R Review rounds (at most 1, recommended) | S | CC-7d | Integrated result, read-only, high-judgment reviewer. | Check the CPU proofs against the plan's completion list and the owner decisions. Findings become rows `R1.<n>` under the [run contract](../../skills/shared/run-contract.md); closing waits for them. | [ ] |

## CC-1 detail

**Lifecycle.**
- **Normalize:** turns the author's request into intent. It holds no paths and no generated files.
- **Prepare:** measures the inputs and resolves the job once.
- **Compile:** reads the job, the prepared file bindings and an output directory.
- **Compose:** reads the job's intervals and grants.

Paths and generated artifacts never enter the request identity.

**The job** is Plan 64's `GenerationInputs`, the only shared measured-input record. Extend it only with the fields the compiler needs:
- `canvas`;
- `placed`: exact items, with their occurrence, span and source offset;
- `grants`: each grant keeps together its stream, interval, occurrence, optional region raster (white means *edit*, as today), strength, seed and associated references;
- `conditioning`: reference rows, and guides from CC-4;
- `prompt`, `model` (base and adapters), `sampling`.

**Conflict checks in preparation.** Move or reuse the interval and ownership checks that `shared/compose.py` uses today, so that preparation refuses two exact owners of the same stream and span. Compare the effective model, steps, sampler, scheduler, guidance or Turbo setting, and any per-grant seed. If two modifying grants need different shared sampler settings, refuse before compilation, naming both grants and the field. Composition keeps its final paste-back.

**Lowerings, as ordinary functions `compile_job` calls.** No lowering picks a whole request route or sorts the request into one exclusive shape; each adds the nodes and bindings for features present in the job. They run in one fixed order:
1. load the model and adapters;
2. bind the source and references;
3. apply the video and audio grant masks;
4. sample;
5. compose the exact placements.

Only conflicts named in the capability table are refused; otherwise every independently valid feature may be combined.

| Job feature | Mechanism |
| --- | --- |
| References | `MiniMaxH3ReferenceToVideo` slots and prompt tags |
| Placed video or still with video grants | source latent and `H3V2VGranularFractionalDenoise` noise mask, then composition paste-back |
| Audio grants | V2V `audio_strength` bound to 0, then an audio-only time mask from the union of generated audio grants through `MiniMaxH3SetAVNoiseMask` after V2V, exactly as Plan 64 SR-5 wires it. Supplied fixed audio is spliced exactly on its own interval. Video grants are never audio grants. |
| Adapters | Each `settings.adapters` entry is a LoRA in the model chain, applied in request order. Its table row declares the base model, default strength, required references by tag, prompt template and tested settings. Masks, grants, audio and extra references follow the ordinary rules. Character Swap is the first row; keep its reference order, binding and verification. |
| Guides | CC-4 |
| Generated suffix after a placed prefix | Chosen from the features present: one unchanged video prefix at frame 0 and uncovered time after it. In phase 1 this calls the captured bundle; CC-7a swaps in the ported stage. From CC-1.2 the `continuation` flag is accepted but selects nothing; CC-7d removes it from the schema. No recipe or skill text uses it. |

**The planner.** `plan_request` stays responsible only for expanding ordered passes, preview metadata and deferred source lineage. Each executable pass is prepared as a job and sent to `compile_job`; the planner never chooses among lowerings. Keep today's rule that a later preview isn't executable until the previous composed candidate is verified.

**Callers to migrate (pinned base; re-check at dispatch):**
- `branch_for` is defined in `shared/request_v2.py` and called from `shared/prepare.py` (twice), `shared/stages.py` and `shared/compile.py`.
- **Per-route compilers** in `shared/compile.py`: `_compile_native`, `_compile_lanpaint`, `_compile_native_masked_edit`, `_compile_character_swap_v2`, the `_compile_native_v2` dispatch, `_compile_generation`, and the public dispatch.
- **The public hook** calls `normalize_request` in `extensions/vibecomfy.workflows/hooks.py`; the dispatch after it is the route selector to remove.
- **Other callers:**
  - `shared/planner.py` calls `canonical_spec`;
  - `shared/stages.py` imports `branch_for`, seals the plan, invokes prepare and compile, persists build state and reloads the prepared request;
  - `shared/request.py` exposes `H3Spec` through `H3Request.canonical`.
- **Before deleting anything,** `git grep` for `H3Spec`, `canonical_spec`, `.canonical`, the v1 schema and profile names, and the normalizers. Migrate every runtime caller and fixture in CC-1.4. Remove `spec.py` only when that list is empty, apart from helpers deliberately kept.
- **Tests that touch these:** `test_native_v2_contract.py` (`branch_for`); `test_spec.py` (v1, v2, `H3Spec`); `test_cli.py` (canonical conversion, `H3Spec.capabilities`); `test_skill_examples_admitted.py` (`canonical_spec`); `test_edit_binding.py` (route compiler, v1 against v2); `test_runtime_declaration_sync.py` (v1). This list isn't complete; search at dispatch.

Trace `_compile_lanpaint`. If nothing reaches it after Plans 64 and 65, delete it. If something does, give it a positive CPU case or replace it with a refusal from the table.

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
- **Recipes this enables:** a guided end, or soft keyframes. For exact stills at any frame, see CC-8.

## CC-8 detail

- **How H3 chunks time.** The model's video latent uses frame chunks of 1, 4, 4, 4, 4, repeating (`comfy/ldm/minimax/model.py` `FRAME_PER_TOKEN`). The chunks are `[0,1)`, `[1,5)`, `[5,9)`, `[9,13)`, `[13,17)`, then the pattern repeats from 17. So frames 0, 17, 34, 51, … are single-frame chunks, and every other frame sits in a 4-frame chunk; frame 61, for example, is in `[60,64)`. The V2V mask takes the maximum over each chunk, so the model can only be told to keep a whole chunk.
- **`hold: chunk` (the default).** A placed still at a single-frame chunk holds one frame. At any other frame N, it snaps to the chunk containing N and holds for 4 frames, about 1/6 s. At the end of the output, the delivered hold is clipped to the last delivered frame, while the full latent chunk stays frozen.
- **`hold: frame`.** The chunk is still frozen during sampling, because the latent mask can't freeze less. Composition pastes the still on frame N alone; the other frames of the chunk are generated, and the dry run warns that a small jump is possible.
- **Preparation** builds a full-canvas source at the target size, from the placed stills and any declared source media. Gaps can hold stand-in pixels, because composition supplies the final generated pixels there. Keep the requested, H3-rounded and delivered frame counts separate, and never treat padding frames as delivered.
- **Composition** pastes each placed item from its own source at its own destination span and source offset, keyed by occurrence. This replaces "one authoritative source at one offset". A still's one frame repeats over its delivered span. Generated frames fill uncovered spans. Video clips, stills and fixed audio use the same paste, each on its own stream; a still never owns audio.
- **Refusals.** Two exact owners of the same stream are refused, even if they come from the same asset.
- **The dry run** lists each still's requested frame, snapped chunk, delivered hold, occurrence and source offset.
- **Recipes this enables:** start and end on exact images; exact keyframes mid-shot.
- **Not in this task:** exact stills inside a continuation prefix (CC-7a).

## CC-5 fill contract

- **A recipe** is one UTF-8 JSON file holding a `template` object and a `request` object, which is an ordinary v2 request. For example: `{"template": {"name": "redub", "purpose": "...", "holes": [{"name": "line", "type": "string", "help": "...", "source": {"set": "line"}}]}, "request": {"version": 2, "prompt": {"text": {"$hole": "line"}}}}`.
- **A hole** has:
  - a unique name;
  - a JSON type (`string`, `number`, `integer`, `boolean`, `object` or `array`);
  - optional units, and whether a range is relative to the media or to the shot;
  - help text;
  - exactly one source: `--set NAME=JSON`, or a named shot field or occurrence.
- **Markers.** In the request, a hole is the marker object `{"$hole": "name"}`, used as a whole JSON value. Never substitute inside strings.
- **Filling.** `--set` values are parsed as JSON. There are no defaults, expressions, conditionals, type coercion or string formatting; a variant is another recipe file.
- **`--from-shot`** requires project, timeline and shot. It selects the exact occurrence when a hole's media depends on the occurrence's trim or placement, and resolves assets through the ordinary asset-map path. The dry run shows the chosen occurrence and resolved asset.
- **Editorial choices stay with the agent:** which voice slice, and drawing the mouth mask.
- **Names and discovery.**
  - Recipes have qualified names, `h3:NAME` and `<skill-id>:NAME`. A bare name works only when it's unique.
  - `NAME` may also be a file path, so an agent-written file is filled and checked the same way.
  - `templates list` shows pack and skill recipes, with name and one-line purpose.
  - `templates show NAME` prints the request and its hole declarations.
- **A filled template is just a request.** `--write FILE` writes only the fully filled v2 request, without the `template` object, and it submits like any other request, through ordinary normalization, admission and build. There is no separate template path, and writing or submitting never updates shot takes.

## CC-6 detail

- **`docs/SKILL.md`** becomes the short general H3 guide, v2 only. It covers:
  - the canvas, exact placed items, soft guides and references, and grants;
  - the three default rules;
  - how to read `describe`;
  - how to list, show and fill a recipe;
  - how requested, effective and delivered fields differ in the dry run;
  - how to recover from named refusals.

  Keep command examples in step with CC-5. Link `docs/reference.md`, which receives the runtime, resume, attestation and checksum material moved out of the guide.
- **`pack.yaml`** required context points at the new guide and at the reference and recipe discovery. Remove links that teach v1 or route names.
- **`docs/recast-scene/SKILL.md`** keeps Recast's judgment:
  - the order of shots;
  - choosing cuts;
  - checking the last spoken word;
  - inspecting mask edges;
  - avoiding doubled lead-in;
  - the approval point.

  It also keeps the silent-reaction workaround (#863), unless a shipped, admitted recipe reproduces a four-frame hold with silent delivered audio. Request-building instructions are replaced by exact recipe names from CC-5.
- **`docs/recast-scene/brief.md`** is a prose checklist, one entry per shot: its ordered steps, template names, required hole values and editorial checks. It adds no shot-plan fields and records no takes.

## CC-7a detail

**Outcome.** A continuation is one video timeline item at frame 0 whose end comes before the canvas end. Astrid generates one audio-video suffix:
- the prepared prefix is delivered exactly;
- it uses the existing timing function, the requested canvas and the effective references;
- incompatible edits are refused before claim, naming the offending item.

The prefix's video and audio are exact, and no grant modifies either stream. Soft image, video or audio conditioning may be present if admitted on its own. Source audio is required in this first port. No route flag is added or kept.

**The node.** Prefix continuation is `MiniMaxH3ExistingVideoMaskedContext` with `insert_frame=0`. The captured graph's `MiniMaxH3StartMaskedContext(start_mode="existing_video")` is only a wrapper that calls it. The prefix output uses `MiniMaxH3AssembleExtension`.

**Lattice.** The kept prefix context is a joint audio-video boundary of 39 + 51k frames (39, 90, 141, …), chosen no larger than the requested, usable source and target lengths. Fewer than 39 usable frames is an error. The target's video length separately follows H3's 5 + 17k frame rule.

**Before writing code,** list each difference between the ported graph and the captured graph's active Existing Video path. Compare inputs, edges, weights, settings, seeds and outputs, and give each difference a reason. Bypassed branches and preview nodes don't count. Intended differences:
- **References:** every declared reference is bound once, in declared order and tags, keeping the speaker-video binding. The capture duplicates one image into two slots, and the port doesn't.
- **Size:** the 0.5 MP selector goes; the requested canvas is used for the target latent, source decode and resize, assembler and mux.
- **Audio feather:** keep the captured 8-tick audio feather for model conditioning. Composition still restores the original prefix PCM exactly; never feather delivered source audio.

**Refusals, all before claim, naming the item:**
- no source audio: `prefix continuation requires source audio`;
- a source trim that doesn't start at the prefix origin: suggest an explicit timeline placement;
- a region edit, full-frame regeneration, regenerated prefix audio or fixed replacement on the prefix: name the grant and suggest two jobs;
- a timed guide that can't be mapped to the sampled segment: name the guide and why;
- no hidden padding and no silent substitution.

A still-only start belongs to Plan 64 SR-4 and CC-8.

**Cases.**
- The existing 120-frame prefix plus 24 new frames: a 73-frame raw extension, 39 context frames, 34 frames of capacity, 10 trimmed.
- 38 and 39-frame usable prefixes.
- One image versus two independent references.
- Three images plus a speaker clip at 512×288.
- **Character Swap with continuation:** a 39-frame prefix, 24 generated frames, one image reference with Character Swap's tag and order, and the Character Swap adapter plus the existing Turbo adapter. Assert:
  - both LoRAs are in the model chain, in the declared order, and the sampler receives that model;
  - `MiniMaxH3ExistingVideoMaskedContext` has `insert_frame=0` and shares the target latent;
  - the assembler receives the preserved count;
  - the reference binding is unchanged.

  Use tiny mock graph assets; load no LoRA weights and run no ComfyUI. If CC-1.2 hasn't generalized adapters, this pair is a capability refusal instead.

**Not in this task:** more than one extension block per job. An endless-continuation skill submits bounded jobs one after another.

## CC-7 lattice summary

| Placement | Nodes | Lattice (Astrid's rule) |
| --- | --- | --- |
| Prefix at frame 0, then generated time | `ExistingVideoMaskedContext` (`insert_frame=0`), `AssembleExtension` | context 39 + 51k frames |
| Clip A, generated gap, clip B | `MaskedAVBridge`, `AssembleBridgeAudio` | each kept context 39 + 51k; target a valid 5 + 17k run; non-empty middle |
| Clip inside generated time | `ExistingVideoMaskedContext` (nonzero `insert_frame`), `AssembleInterior` | offset a multiple of 51 (where video and 40 Hz audio line up exactly); refused otherwise |

The node itself accepts insert offsets on multiples of 17 and rounds the audio position. Astrid's multiple-of-51 rule is deliberately stricter, so audio is never shifted.
