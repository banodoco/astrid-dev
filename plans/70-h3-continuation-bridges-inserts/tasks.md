# Tasks — H3 continuation, bridges and inserts

[Plan](plan.md) · [Inputs](inputs.md)

**Task ids:** `CC-7a` … `CC-7d`, `CC-12`, integrated review `R`. CC-7a to CC-7d keep the ids they had in Plan 66, so research files and other plans still resolve.

**Critical path:** Plans 66 and 68 → CC-7a → (CC-7b, CC-7c in parallel) → CC-7d → CC-12 → R. CC-7a's first step compares against Plan 68 CC-8's full-canvas source, and that check decides whether CC-7b and CC-7c need lowerings of their own, so this plan follows Plan 68 rather than running beside it.

**Test inventory:** Bare test filenames are under `tests/packs/h3_av/` in astrid-agent. Run them from the Agent checkout with the pinned worker command `env/agent-pytest.sh <paths>`. Run only the files a card names, not the whole suite. Product paths are under `astrid/packs/h3_av/` unless given in full. Cards name functions, not line numbers: find each function with `grep -n` at dispatch, and re-check each caller and test list against the integrated code then. Every task is CPU only (D1). No task claims a machine, rents a GPU or spends money. Request identity was already broken once, in Plan 64 SR-1 (D4). When a task changes an emitted graph, regenerate its fixtures in the same commit and list each change with its reason. Do not add code to preserve an old digest.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| CC-7a Prefix continuation: one unchanged video prefix at frame 0 plus one generated suffix | S | Plan 68 | `shared/generation.py` (one function for the prefix case, porting only the captured graph's active `start_mode='existing_video'` path: source frames and audio → `MiniMaxH3ExistingVideoMaskedContext` with `insert_frame=0` → `MiniMaxH3AssembleExtension`; not the generated-starter branch); `shared/timing.py` (reuse); `shared/prepare.py` and `shared/compose.py` continuation intervals. The captured workflows stay in place until CC-7d. Details below. | `test_continuation_timing.py`, `test_compile_generalized.py`, `test_native_v2_contract.py`. Cases listed below. Assert node inputs and edges, one shared size and 24 fps across source decode, target, assembler and mux, reference tags, the source audio binding, and exact prefix pixels and PCM through composition against a contrasting stand-in. No claim of output-quality parity. | [ ] |
| CC-7b Bridge between two placed clips | S | CC-7a | `shared/generation.py` (bridge lowering with `MiniMaxH3MaskedAVBridge` and `MiniMaxH3AssembleBridgeAudio`; not routed through the existing-video context node); `shared/prepare.py` (the gap and two kept intervals); `shared/compose.py`. | `test_compile_generalized.py`, `test_handle_build_compose.py`, `test_native_v2_contract.py`. The smallest symmetric bridge: a 39-frame kept tail of clip A, 63 generated frames, then a 39-frame kept head of clip B, for a 141-frame target. Verify the placement and ownership intervals, the generated middle, the bridge audio wiring and the exact composition of both clips. Refusals: either kept context not 39 + 51k frames; no generated middle; a timeline that can't map onto a valid H3 run. Never silently enlarge or shrink the user's gap. With the Character Swap adapter on, the graph has both the adapter LoRA and the Turbo LoRA in the model chain feeding the sampler, and the bridge nodes are unchanged. Inspect the graph only; no inference-quality claim. Follow the bridge contract in [Assembly](#functional-additions-assembly): one shared preserve count `n` with matching audio and video trims, and a test with longer unequal owners (120 and 90 frames, n = 39), repeated source trims and 39/12/39. | [ ] |
| CC-7c Insert a placed clip between generated time | S | CC-7a | `shared/generation.py` (insert lowering: `MiniMaxH3ExistingVideoMaskedContext` with a nonzero `insert_frame`, sharing CC-7a's context helper, then `MiniMaxH3AssembleInterior`); `shared/prepare.py`; `shared/compose.py`. | `test_compile_generalized.py`, `test_handle_build_compose.py`, `test_native_v2_contract.py`. An insert at frame 51 compiles, with the node's snapped `insert_frame` and `preserved_frames` outputs wired into `MiniMaxH3AssembleInterior` and the same crop, fps and source mapping as the context. Generated time exists on both sides. Exact source pixels and PCM are delivered over the insert. A requested offset that isn't a multiple of 51 (for example 34, or 50) is refused before compilation, with no silent snapping. A clip that doesn't fit the target is refused. | [ ] |
| CC-7d Delete the captured continuation workflows and the `continuation` flag | S | CC-7a, CC-7b, CC-7c | `workflows/native_h3_continuation*/`; the captured-workflow dispatch in `shared/compile.py`; the `continuation` field in `schemas/request.v2.json` and `shared/request_v2.py`; `test_workflow_pair.py`, `test_workflow_model_urls.py`, `test_runtime_declaration_sync.py`, `test_release_runtime_guard.py`; continuation fixtures and their references. Deletion follows CPU proof alone (D3). Remove the flag only after a repository search shows no live caller depends on it. | Those four test files, plus `test_continuation_timing.py` and `test_native_v2_contract.py`. List every old assertion as kept, replaced or dropped. Keep the assertions that still protect runtime declarations and bundle integrity, now against the new graph. No captured bundle is selectable afterwards. Prefix, bridge and insert all compile through the shared lowerings. | [ ] |
| CC-12 Recipes, skill section and final trim | T | CC-7d | Recipe files for continue, bridge, insert and a guide inside a continuation; one short section and one kinds-table row in `docs/SKILL.md`; flip the bridge and insert rows from `unavailable`; amend `docs/design.md`. Then the final trim pass over the whole skill page: wording only, within the [skill guards](../66-h3-composable-core/tasks.md#skill-guards). | `test_skill_examples_admitted.py`, `tests/test_pack_declared_skills.py`, the skill-guard tests, and the standing cold read plus one continuation ask. | [ ] |
| R Integrated review (at most 1, recommended) | S | CC-12 | Read-only, high-judgment reviewer, on the integrated result of Plans 66, 68 and 70. | Check the CPU proofs of all three plans against their completion lists, `docs/design.md` and the owner decisions. Findings become rows `R1.<n>` under the [run contract](../../agent/shared/run-contract.md); closing waits for them. | [ ] |

## CC-7a detail

**Outcome.** A continuation is one video timeline item at frame 0 whose end comes before the canvas end. Astrid generates one audio-video suffix:
- the prepared prefix is delivered exactly;
- it uses the existing timing function, the requested canvas and the effective references;
- incompatible edits are refused before claim, naming the offending item.

The prefix's video and audio are exact, and no grant modifies either stream. Soft image, video or audio conditioning may be present if admitted on its own. Source audio is required in this first port. No route flag is added or kept.

**The node.** Prefix continuation is `MiniMaxH3ExistingVideoMaskedContext` with `insert_frame=0`. The captured graph's `MiniMaxH3StartMaskedContext(start_mode="existing_video")` is only a wrapper that calls it. The prefix output uses `MiniMaxH3AssembleExtension`.

**Lattice.** The kept prefix context is a joint audio-video boundary of 39 + 51k frames (39, 90, 141, …), chosen no larger than the requested, usable source and target lengths. Fewer than 39 usable frames is an error. The target's video length separately follows H3's 5 + 17k frame rule.

**First, before porting:** check whether prefix, insert and bridge can be prepared by CC-8's full-canvas source with the V2V node and the SR-5 audio mask, instead of the three context nodes. If the latent and masks are equivalent, use that one preparation and drop CC-7b and CC-7c as separate lowerings. If not, record why, keep all preparation choices in one function, and add table rows for each pair that can't share a job (for example a continuation with an exact end still). This is unverified. Compare initial samples in kept and generated regions, VAE temporal phase, audio feather and row weights; equal mask shapes or identical final pasted frames do not show the sampler inputs are equivalent. Run this comparison after CC-8 lands. When the evidence is insufficient, keep the context lowerings and the explicit pair refusals.

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
  - the prefix assembly follows [Assembly](#functional-additions-assembly): raw AV is trimmed to the generated span before `MiniMaxH3AssembleExtension`, which has no preserved-count input;
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

## Functional additions

### Functional additions assembly

**Assembly (CC-7a, CC-7b).**
- **Map complete owners** to one raw segment.
- **Bridges:** bind a single common `n` with matching audio and video trims. Then either pass only `n`-frame windows to the bridge audio assembler, or assemble whole owners with explicit final timeline offsets. Full clips of 120 and 90 frames with n = 39 would otherwise give audio for 273 frames against 141 of video.
- **Prefix:** decode raw AV, and trim both streams to the generated span before `MiniMaxH3AssembleExtension`. For 120 + 24, select raw picture `[39,63)`, conform the decoded generated PCM to exactly 24 frames, then append, and assert 144 final frames. Preserve the exact prefix bytes after mux.
- **Port differences:** list the overlap policy and the loss of streamed decoding.
- **Trim nodes:** don't add a trim node with its defaults; select the requested span on absolute boundaries or conform explicitly.

### Functional additions clocks

**Clocks (Plan 66 CC-9, CC-7, Plan 68 CC-8).** Map delivered spans into sampled segments explicitly. In a 120 + 24 continuation, delivered frame 143 is raw frame 62, because raw 0 is delivered 81; a guide at delivered 80 is outside the sampled segment and is refused, cropped or kept as stated. Infer the shot duration from measured placements, or require `duration` for circular expressions. Record the local frame and tick, and rebase guides. Derive stored and selected take spans from ownership: the default drop on 120 + 24 selects `[120,144)` from the stored `[0,144)`, and keep selects the whole file. Bridges and inserts don't inherit prefix drop. The Plan 59 take reader currently identifies continuation from the flag CC-7d deletes; move it to ownership in CC-7d.
