# Tasks — H3 speaker references

[Plan](plan.md) · [Inputs](inputs.md)

**Task ids:** SR-1 through SR-7.

**Critical path:** SR-1 → SR-2 → SR-3 → (SR-5, SR-6 in parallel) → SR-4 → SR-7 → R.

**Test inventory:** Bare test filenames are under `tests/packs/h3_av/` in astrid-agent. Run them from the Agent checkout with the pinned worker command `env/agent-pytest.sh <paths>`. Run only the files a card names, not the whole suite. Product paths are under `astrid/packs/h3_av/` unless given in full. Cards name functions, not line numbers: find each function with `grep -n` at dispatch. Every task is CPU only (D2). No task claims a machine, rents a GPU or spends money. Request identity breaks once, in SR-1 (Plan 66 D4). After that, no task preserves an old digest: when a graph changes, regenerate its fixtures in the same commit and list each change with its reason.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| SR-1 Carry typed reference occurrences through the request and spec | X | Owner scope | `shared/request_v2.py` normalization; `shared/spec.py` only as far as v1 translation needs. Details below. | `test_spec.py`, `test_native_v2_contract.py`, `test_request_contract.py`. One round-trip fixture with a guided fixed replacement clip, a separate unguided audio-generation interval and a separately named conditioning clip. Assert each occurrence keeps its identity, modality, trim, paired-soundtrack choice and `use`. Assert two trims of one asset stay two occurrences. Old fixtures are regenerated once, in one commit that lists every changed digest and why. A v1 request still translates. Resuming an old in-flight build gives an actionable error rather than a silent mismatch. | [ ] |
| SR-2 Add one limits table and refuse over-limit references before claim | N | SR-1 | A `LIMITS` table in `shared/generation.py` beside `IMAGE_REFERENCE_CAPACITY` (which then reads from it); measurement in `shared/prepare.py`; existing hand-written slot refusals in `shared/compile.py` rewritten to read the table. Details below. | `test_edit_inputs.py`, `test_real_media_preflight.py`, `test_generation.py`. Boundary-test every table entry at the limit and one past it. Also: clips that are each valid but sum past 15 seconds; unreadable metadata; a trim past the end of the file; a requested soundtrack that's missing; a silent video accepted with audio off. Compare node slot counts and size rules to the cached node schema. | [ ] |
| SR-3 Lower every route once through one `GenerationInputs` record | X | SR-2 | `shared/generation.py` (`GenerationInputs`, `build_generation_workflow`); `shared/compile.py` source-free, masked and Character Swap compilers. Removes the source-free v2→v1 translation. Details below. | `test_generation.py`, `test_native_masked_edit.py`, `test_character_swap.py`, `test_character_swap_cpu_boundary.py`, `test_compile_generalized.py`, `test_edit_inputs.py`. Compile the same mixed image/video/standalone-audio request on source-free and masked routes. Inspect each node input and prompt tag. Test stale or forged request tags, and a prompt naming a tag no row has. Today's image-only source-free graph, masked-edit graph and Character Swap bindings are unchanged node for node, apart from listed differences. | [ ] |
| SR-4 Make a frame-0 timeline image the exact first frame | X | SR-3, SR-5 | `shared/request_v2.py` admission of `role: timeline` images; `shared/compile.py` lowering of a placed still to the existing source-backed path; `shared/compose.py` frame-0 paste. Details below. | `test_native_masked_edit.py`, `test_handle_build_compose.py`, `test_native_v2_contract.py`. The compiled graph feeds the still as the source's frame 0, with video generated from frame 1 and audio strength 1. Composed over a visibly different stand-in clip: decoded frame 0 equals the prepared still pixel for pixel; frame 1 equals the stand-in; the soundtrack is the stand-in's. A timeline image at frame 1 is refused from the limits table. | [ ] |
| SR-5 Generate new audio inside a masked edit's window and keep source audio outside it | X | SR-3 | `shared/compile.py` masked-audio selection; `shared/generation.py` `audio_strength` binding; `shared/compose.py` audio segment selection. Details below. | `test_native_masked_edit.py`, `test_edit_inputs.py`, `test_handle_build_compose.py`. Lossless partial-window fixture with distinct tones before and after the window and a stand-in generated clip. Decoded PCM before and after the window equals the source; inside equals the stand-in. Picture outside the mouth mask equals the source. The fixed-clip splice is unchanged within one sample. A mixed fixture (supplied clip on one interval, generated audio on another) delivers each on its interval. | [ ] |
| SR-6 Show the same reference rows in the dry run and the settled result | N | SR-3 | `compilation.json` (declared as `h3.compilation` by the H3 workflow `hooks.py`); `shared/stages.py` `_sealed_plan`; `astrid/sdk/results.py` `_reconstruct_generation_result`, read by `astrid/sdk/generation.py`. | `test_generation.py`, `test_parent_receipt_readback.py`, `tests/sdk/test_generation_result_refs.py`. Read one mixed request through the dry run and through result reconstruction from a settled CPU fixture. Every row (occurrence, tag, trim, slot) matches the graph, and still reads after scratch cleanup. | [ ] |
| SR-7 Document both recipes | T | SR-3, SR-4, SR-5 | `docs/SKILL.md` and `docs/recast-scene/SKILL.md`. Two recipes: start image plus speaker clip; mouth mask plus speaker clip. State the limits from the table, the frame-0 rule and that room tone inside the window is regenerated. Write each new recipe as a complete request file that the admission test loads, so Plan 66 CC-5 adds holes instead of rewriting prose. | `test_skill_examples_admitted.py` admits each documented request. `tests/test_pack_declared_skills.py` passes. | [ ] |
| R Review rounds (at most 1, recommended) | S | SR-1 through SR-7 | Read-only integrated result; high-judgment reviewer (Astra or Opus). | Check the CPU proofs above against the plan's completion list and owner decisions. Findings become rows `R1.<n>` under the [run contract](../../skills/shared/run-contract.md) and close before completion. | [ ] |

## Terms

- **Occurrence:** one use of one asset in the request. Two trims of the same file are two occurrences.
- **`use: conditioning | replacement`:** set once per audio occurrence at normalization. An audio clip named by a replacement edit is `replacement`; every other audio clip is `conditioning`. One occurrence with both uses is refused. Every later step reads this field and never recomputes it.
- **`audio_strength`:** the masked-edit node's single audio value for the whole clip. `0` keeps the source audio latent unchanged (today's hard-coded value); `1` regenerates all of it. There is no in-between value in this plan and no time mask on it. The time window comes from composition (SR-5).
- **Effective rows:** the references in the order the node actually receives them, which fixes their prompt tags (`<Picture n>`, `<Video n>`, `<Audio n>`).

## SR-1 detail

- At normalization, give each reference occurrence its modality, trim, paired-soundtrack choice and, for audio, its `use`.
- Carry all of these through normalization into the record. Touch `spec.py` only where v1 translation needs it, including `sampling_passes` and `sampling_request_document`.
- **The clean break (Plan 66 D4):** request identity is derived from author intent: placement, trims, occurrence order, model and `use`.
  - Derived prompt tags (`model_tags`, and each occurrence's `model_tag`) leave the identity and the normalized request. SR-3 derives tags from the effective rows.
  - Old raw v1 requests translate.
  - Already-sealed v2 builds and settled receipts still read, because the reader verifies stored bytes.
  - Resuming an old in-flight build refuses with "rebuild this request", rather than comparing against a new digest.
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

Keep two blocks in the table: **model limits** (the node's facts: 9/3/3, the clip times, 12 files, size) and **lowering limits** (what an Astrid lowering can't do yet: the Character Swap 1/1 and continuation 2/0 rows). Remove each lowering restriction only when its replacement lowering has a positive test. Measured-media errors (unreadable file, trim past the end) stay with the probe that finds them.

- Before claim, `prepare.py` measures each conditioning occurrence's real file with the existing probe and per-stream coverage routines in `compile.py`.
- Each supplied occurrence counts once toward the 12-file limit, including repeats with different trims.
- A video's soundtrack counts toward audio time but uses its video's file.
- Fixed replacement audio counts toward nothing here.
- Every refusal message names the table entry it broke.

## SR-3 detail

`GenerationInputs` is a frozen dataclass in `shared/generation.py` with exactly these fields. Add a field only when a test needs it, and name that test in the PR:

- `canvas`: size and frames (size is 1024×576 until Plan 65);
- `placed`: placed items (source clip, still, fixed audio) with their spans;
- `grants`: each grant keeps together its stream, interval, source occurrence, optional region raster (white means *edit*, as today), strength, seed and associated references. Composition keeps everything no grant covers;
- `conditioning`: the effective reference rows;
- `prompt`, `model` (base, and adapter for Character Swap), `sampling` (today's controls, passed through unchanged).

The fields are named by the core model, not by route, so [Plan 66](../66-h3-composable-core/plan.md) builds on them without a rename.

Rules:
- All three compilers build the record from the normalized v2 request, falling back to `canonical_spec` only for a v1 request, and `build_generation_workflow(inputs)` takes only the record.
- Derive the rows once from the node's input order, keeping the request order within each modality.
- A video's enabled soundtrack takes its audio tag before any standalone clip, even if the standalone clip came first in the request.
- Replace Character Swap's hard-coded tags in `compile.py` with lookups in the rows.
- Refuse a prompt that names a tag no row has.

## SR-4 detail

- A `role: timeline` image with `at: {frame: 0}` is a placed still. Lower it to the existing source-backed path: the still becomes the source's frame 0, video is generated from frame 1, and audio is generated (strength 1, per SR-5). That way the model sees the still, so frame 1 continues from it.
- **This is more than a paste.** Preparation must build the source from the still: a full-canvas-length video whose frames all hold the still (the builder needs a source as long as the output), plus silent audio that nobody supplied and that is entirely generated. Use a CPU fixture with only the still and no user audio.
- Composition writes the prepared still over decoded frame 0, through the existing paste-back.
- A placed still at any other frame is refused from the limits table, as a lowering limit. [Plan 66](../66-h3-composable-core/plan.md) adds a soft guide at other frames (CC-4); an exact still off frame 0 stays refused.
- No new node. See [research/first-frame.md](research/first-frame.md).

## SR-5 detail

Two kinds of audio, kept apart:
- **Generated audio:** a grant asks H3 to make sound. `audio_strength` is a single clip-wide value, so it's 1 whenever any audio grant generates sound, and 0 otherwise.
- **Supplied audio (a fixed replacement clip):** a placed audio item in the record, even though the request spells it as it does today. On its own interval its samples win over anything generated, spliced exactly, within the existing one-sample tolerance. The fixed-clip path with no generated audio keeps strength 0, its splice and its fallback.
- **The mixed case** (one interval with supplied audio, another generating audio) is allowed. Strength is 1, the supplied samples are spliced on their interval, and generated samples are used on the other.
- **Composition** keeps source audio outside every audio grant, using the existing per-stream audio segments.
- Record the clip-wide strength and the delivered sample spans separately in the dry run; they're different evidence.

## Existing tests that change

- `test_edit_inputs.py`:
  - the image-only video-guide refusal becomes selection of a separately named audio conditioning occurrence;
  - the two "only two image slots" masked refusals become affirmative cases: one conditioning clip, three images;
  - the invalid fixed-audio guide refusal stays.
- `test_compile_generalized.py`: the captured continuation's two-slot refusal stays.
- All other fixed-audio and image-only fixtures stay.
