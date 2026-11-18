# Tasks — H3 speaker references

[Plan](plan.md) · [Inputs](inputs.md)

**Task ids:** SR-1 through SR-7.

**Critical path:** SR-1 → SR-2 → SR-3 → (SR-4, SR-5, SR-6 in parallel) → SR-7 → R.

**Test inventory:** Bare test filenames are under `tests/packs/h3_av/` in astrid-agent. Run them from the Agent checkout with the pinned worker command `env/agent-pytest.sh <paths>`. Run only the files a card names, not the whole suite. Product paths are under `astrid/packs/h3_av/` unless given in full. Cards name functions, not line numbers: find each function with `grep -n` at dispatch. Every task is CPU only (D2). No task claims a machine, rents a GPU or spends money.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| SR-1 Carry typed reference occurrences through the request and spec | X | Owner scope | `shared/request_v2.py` normalization; `shared/spec.py` forward and reverse conversion. Details below. | `test_spec.py`, `test_native_v2_contract.py`, `test_request_contract.py`. One round-trip fixture with a guided fixed replacement clip, a separate unguided audio-generation interval and a separately named conditioning clip. Assert each occurrence keeps its identity, modality, trim, paired-soundtrack choice and `use`. Assert two trims of one asset stay two occurrences. Assert today's image-only request bytes and digests are unchanged. | [ ] |
| SR-2 Add one limits table and refuse over-limit references before claim | N | SR-1 | A `LIMITS` table in `shared/generation.py` beside `IMAGE_REFERENCE_CAPACITY` (which then reads from it); measurement in `shared/prepare.py`; existing hand-written slot refusals in `shared/compile.py` rewritten to read the table. Details below. | `test_edit_inputs.py`, `test_real_media_preflight.py`, `test_generation.py`. Boundary-test every table entry at the limit and one past it. Also: clips that are each valid but sum past 15 seconds; unreadable metadata; a trim past the end of the file; a requested soundtrack that's missing; a silent video accepted with audio off. Compare node slot counts and size rules to the cached node schema. | [ ] |
| SR-3 Lower every route once through one `GenerationInputs` record | X | SR-2 | `shared/generation.py` (`GenerationInputs`, `build_generation_workflow`); `shared/compile.py` source-free, masked and Character Swap compilers. Removes the source-free v2→v1 translation. Details below. | `test_generation.py`, `test_native_masked_edit.py`, `test_character_swap.py`, `test_character_swap_cpu_boundary.py`, `test_compile_generalized.py`, `test_edit_inputs.py`. Compile the same mixed image/video/standalone-audio request on source-free and masked routes. Inspect each node input and prompt tag. Test stale or forged request tags, and a prompt naming a tag no row has. Compare today's image-only source-free bundle, masked digests and Character Swap bindings with their fixtures. | [ ] |
| SR-4 Make a frame-0 timeline image the exact first frame | N | SR-3 | `shared/request_v2.py` admission of `role: timeline` images; `shared/compose.py` one frame-0 paste step after source-free generation. Details below. | `test_handle_build_compose.py`, `test_native_v2_contract.py`. Compose a source-free request with a frame-0 timeline image over a visibly different stand-in clip. Decoded frame 0 equals the prepared still pixel for pixel; frame 1 equals the stand-in; the soundtrack is the stand-in's. A timeline image at frame 1 is refused with the message given below. | [ ] |
| SR-5 Generate new audio inside a masked edit's window and keep source audio outside it | X | SR-3 | `shared/compile.py` masked-audio selection; `shared/generation.py` `audio_strength` binding; `shared/compose.py` audio segment selection. Details below. | `test_native_masked_edit.py`, `test_edit_inputs.py`, `test_handle_build_compose.py`. Lossless partial-window fixture with distinct tones before and after the window and a stand-in generated clip. Decoded PCM before and after the window equals the source; inside equals the stand-in. Picture outside the mouth mask equals the source. The existing fixed-clip digest is unchanged. | [ ] |
| SR-6 Show the same reference rows in the dry run and the settled result | N | SR-3 | `compilation.json` (declared as `h3.compilation` by the H3 workflow `hooks.py`); `shared/stages.py` `_sealed_plan`; `astrid/sdk/results.py` `_reconstruct_generation_result`, read by `astrid/sdk/generation.py`. | `test_generation.py`, `test_parent_receipt_readback.py`, `tests/sdk/test_generation_result_refs.py`. Read one mixed request through the dry run and through result reconstruction from a settled CPU fixture. Every row (occurrence, tag, trim, slot) matches the graph, and still reads after scratch cleanup. | [ ] |
| SR-7 Document both recipes | T | SR-3, SR-4, SR-5 | `docs/SKILL.md` and `docs/recast-scene/SKILL.md`. Two recipes: start image plus speaker clip; mouth mask plus speaker clip. State the limits from the table, the frame-0 rule and that room tone inside the window is regenerated. | `test_skill_examples_admitted.py` admits each documented request. `tests/test_pack_declared_skills.py` passes. | [ ] |
| R Review rounds (at most 1, recommended) | S | SR-1 through SR-7 | Read-only integrated result; high-judgment reviewer (Astra or Opus). | Check the CPU proofs above against the plan's completion list and owner decisions. Findings become rows `R1.<n>` under the [run contract](../../skills/shared/run-contract.md) and close before completion. | [ ] |

## Terms

- **Occurrence:** one use of one asset in the request. Two trims of the same file are two occurrences.
- **`use: conditioning | replacement`:** set once per audio occurrence at normalization. An audio clip named by a replacement edit is `replacement`; every other audio clip is `conditioning`. One occurrence with both uses is refused. Every later step reads this field and never recomputes it.
- **`audio_strength`:** the masked-edit node's single audio value for the whole clip. `0` keeps the source audio latent unchanged (today's hard-coded value); `1` regenerates all of it. There is no in-between value in this plan and no time mask on it. The time window comes from composition (SR-5).
- **Effective rows:** the references in the order the node actually receives them, which fixes their prompt tags (`<Picture n>`, `<Video n>`, `<Audio n>`).

## SR-1 detail

- At normalization, give each reference occurrence its modality, trim, paired-soundtrack choice and, for audio, its `use`.
- Carry all of these through `spec.py` in both directions, including `sampling_passes` and `sampling_request_document`.
- Keep `use` out of the request's identity bytes, so today's digests don't change.
- Keep the request's `model_tags` field as is, only so digests don't change. No new code reads it (SR-3 replaces every reader).
- Keep the rules that exist today: one audio-changing window per graph, and the agreement multi-region edits already need on image guides, interval, seed and strength.

## SR-2 detail

One table, in one place. Plan 65 adds no second copy:

| Entry | Value |
| --- | --- |
| Builder images / videos / standalone audio | 9 / 3 / 3 |
| Character Swap images / videos | 1 / 1 |
| Continuation images / videos | 2 / 0 |
| Per clip | 2–15 seconds |
| Per modality total | 15 seconds |
| Conditioning files | 12 |
| Width and height | 32–16384, multiples of 32 (Plan 65 reads this) |

- Before claim, `prepare.py` measures each conditioning occurrence's real file with the existing probe and per-stream coverage routines in `compile.py`.
- Each supplied occurrence counts once toward the 12-file limit, including repeats with different trims.
- A video's soundtrack counts toward audio time but uses its video's file.
- Fixed replacement audio counts toward nothing here.
- Every refusal message names the table entry it broke.

## SR-3 detail

`GenerationInputs` is a frozen dataclass in `shared/generation.py` with exactly these fields. Add a field only when a test needs it, and name that test in the PR:

- `prompt`, `frames`, `size` (default 1024×576 until Plan 65);
- `references`: the effective rows;
- `source_edit`: optional; the mask artifact, strength and audio mode;
- `adapter`: optional; Character Swap's bindings;
- `sampling`: today's sampling controls, passed through unchanged.

Rules:
- All three routes build the record from `canonical_spec`, and `build_generation_workflow(inputs)` takes only the record.
- Derive the rows once from the node's input order, keeping the request order within each modality.
- A video's enabled soundtrack takes its audio tag before any standalone clip, even if the standalone clip came first in the request.
- Replace Character Swap's hard-coded tags in `compile.py` with lookups in the rows.
- Refuse a prompt that names a tag no row has.

## SR-4 detail

- A `role: timeline` image with `at: {frame: 0}` is admitted on the source-free route only.
- Generation runs as it does today.
- Composition then writes the prepared still over decoded frame 0. Reuse the existing `compose.py` encode path. Add one paste step, not a new compositor.
- Any other frame is refused with: `timeline images are only supported at frame 0`.
- No new node and no `MiniMaxH3AddGuide`. See [research/first-frame.md](research/first-frame.md).

## SR-5 detail

- A masked edit that asks for new audio, with no replacement clip, sets `audio_strength` to 1. Today it's refused.
- Composition keeps source audio outside the edit's time window, using the existing per-stream audio segments.
- The fixed-clip path keeps strength 0, its existing splice, its one-sample tolerance and its fallback.

## Existing tests that change

- `test_edit_inputs.py`:
  - the image-only video-guide refusal becomes selection of a separately named audio conditioning occurrence;
  - the two "only two image slots" masked refusals become affirmative cases: one conditioning clip, three images;
  - the invalid fixed-audio guide refusal stays.
- `test_compile_generalized.py`: the captured continuation's two-slot refusal stays.
- All other fixed-audio and image-only fixtures stay.
