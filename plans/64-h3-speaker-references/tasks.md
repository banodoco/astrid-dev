# Tasks — H3 speaker references

[Plan](plan.md) · [Inputs](inputs.md)

## Rulings

**Now (2026-11-18):** Agent plan branch `release/14/plan-64` at `b50371baf101d6f706269fab38cdf3a7a5eb2013`; smoke passed (48 tests). Scoped baseline: 198 passed, 3 pre-existing failed, 31 deselected ([evidence PR #921](https://github.com/banodoco/astrid-dev/pull/921)). SR-1 is in progress; SR-2 onward depend on it. CPU only; spend $0.

- SR-1 requires the owner-approved clean identity break recorded in inputs D3. Update the pinned v2 digest values to the new author-intent identity in one commit, retaining semantic-equality assertions and adding proof of historical sealed-byte verification and actionable in-flight refusal. List each digest change and its reason.
- **REVIEW — SR-1 mask lowering deferred to SR-3:** shared seed/reference validation remains in SR-1. Separate permission and sampler-strength masks and failure when a grant vanishes on the model grid require `compile.py` and `generation.py`, which SR-3 owns, and proof in its `test_native_masked_edit.py` selection. SR-3 must deliver and test them before landing.
- **REVIEW — SR-1 mixed round trip deferred in part to SR-5:** the unguided audio-generation interval is currently rejected by the explicit fail-closed test `test_unimplemented_sampling_combinations_fail_closed[audio-regenerate]`. Preserve that check until SR-5 implements generated audio; SR-5 must add the mixed round trip and positive admission proof alongside its end-to-end audio proof. SR-1 still covers typed conditioning and replacement occurrences.
- Release 14 now includes Plan 64 ([#912](https://github.com/banodoco/astrid-dev/pull/912)); the branch row is in [PR #918](https://github.com/banodoco/astrid-dev/pull/918).

**Task ids:** SR-1 through SR-7.

**Critical path:** SR-1 → SR-2 → SR-3 → (SR-5, SR-6 in parallel) → SR-4 → SR-7 → R.

**Test inventory:** Bare test filenames are under `tests/packs/h3_av/` in astrid-agent. Run them from the Agent checkout with the pinned worker command `env/agent-pytest.sh <paths>`. Run only the files a card names, not the whole suite. Product paths are under `astrid/packs/h3_av/` unless given in full. Cards name functions, not line numbers: find each function with `grep -n` at dispatch. Every task is CPU only (D2). No task claims a machine, rents a GPU or spends money. Request identity breaks once, in SR-1 (Plan 66 D4). After that, no task preserves an old digest: when a graph changes, regenerate its fixtures in the same commit and list each change with its reason.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| SR-1 Carry typed reference occurrences through the request and spec | X | Owner scope | `shared/request_v2.py` normalization; `shared/spec.py` only as far as the record needs. Details below. | `test_spec.py`, `test_native_v2_contract.py`, `test_request_contract.py`. One round-trip fixture with a guided fixed replacement clip, a separate unguided audio-generation interval and a separately named conditioning clip. Assert each occurrence keeps its identity, modality, trim, paired-soundtrack choice and `use`. Assert two trims of one asset stay two occurrences. Old fixtures are regenerated once, in one commit that lists every changed digest and why. v1 requests still work in this plan: the plain-input hook builds v1 internally until Plan 66 CC-1.3 migrates it, and CC-1.4 then refuses v1. A sealed build from before SR-1 still reads: its stored bytes are verified in their recorded format and the existing settled result is returned. Resuming an old in-flight build gives an actionable error rather than a silent mismatch. | [ ] In progress; identity ruling and mask-lowering deferral recorded above. |
| SR-2 Add one limits table and refuse over-limit references before claim | N | SR-1 | A `LIMITS` table in `shared/generation.py` beside `IMAGE_REFERENCE_CAPACITY` (which then reads from it); measurement in `shared/prepare.py`; existing hand-written slot refusals in `shared/compile.py` rewritten to read the table. Details below. | `test_edit_inputs.py`, `test_real_media_preflight.py`, `test_generation.py`. Boundary-test every table entry at the limit and one past it. Also: clips that are each valid but sum past 15 seconds; unreadable metadata; a trim past the end of the file; a requested soundtrack that's missing; a silent video accepted with audio off. Compare node slot counts and size rules to the cached node schema. Per occurrence, also report the retained picture frames, audio duration, slot, tag, effective size and a resource estimate, and bind standalone audio ports as AUDIO ([Resources](../66-h3-composable-core/tasks.md#functional-additions-resources)). | [ ] |
| SR-3 Lower every route once through one `GenerationInputs` record | X | SR-2 | `shared/generation.py` (`GenerationInputs`, `build_generation_workflow`); `shared/compile.py` source-free, masked and Character Swap compilers. Removes the source-free v2→v1 translation. Details below. | `test_generation.py`, `test_native_masked_edit.py`, `test_character_swap.py`, `test_character_swap_cpu_boundary.py`, `test_compile_generalized.py`, `test_edit_inputs.py`. Compile the same mixed image/video/standalone-audio request on source-free and masked routes. Inspect each node input and prompt tag. Test stale or forged request tags, and a prompt naming a tag no row has. Today's image-only source-free graph, masked-edit graph and Character Swap bindings are unchanged node for node, apart from listed differences. Report which occurrence and soundtrack each tag actually identifies ([Bindings](../66-h3-composable-core/tasks.md#functional-additions-bindings)). | [ ] |
| SR-4 Make a frame-0 timeline image the exact first frame | X | SR-3, SR-5 | `shared/request_v2.py` admission of `role: timeline` images; `shared/compile.py` lowering of a placed still to the existing source-backed path; `shared/compose.py` frame-0 paste. Details below. | `test_native_masked_edit.py`, `test_handle_build_compose.py`, `test_native_v2_contract.py`. The compiled graph feeds the still as the source's frame 0, with video generated from frame 1 and the whole soundtrack generated: V2V `audio_strength` 0, plus an all-one SR-5 time mask through `MiniMaxH3SetAVNoiseMask`. Assert that effective all-one audio mask in this fixture. Composed over a visibly different stand-in clip: decoded frame 0 equals the prepared still pixel for pixel; frame 1 equals the stand-in; the soundtrack is the stand-in's. A timeline image at frame 1 is refused from the limits table. | [ ] |
| SR-5 Generate new audio inside a masked edit's window and keep source audio outside it | X | SR-3 | `shared/compile.py` masked-audio selection; `shared/generation.py` (V2V `audio_strength` bound to 0, plus a `MiniMaxH3SetAVNoiseMask` audio-only time mask after V2V); `shared/compose.py` audio segment selection. Details below. | `test_native_masked_edit.py`, `test_edit_inputs.py`, `test_handle_build_compose.py`. Lossless partial-window fixture with distinct tones before and after the window and a stand-in generated clip. Decoded PCM before and after the window equals the source; inside equals the stand-in. Picture outside the mouth mask equals the source. The fixed-clip splice is unchanged within one sample. A mixed fixture (supplied clip on one interval, generated audio on another) delivers each on its interval. | [ ] |
| SR-6 Show the same reference rows in the dry run and the settled result | N | SR-3 | `shared/stages.py` `_sealed_plan`; the H3 workflow `hooks.py`; `astrid/sdk/results.py` `_reconstruct_generation_result`, read by `astrid/sdk/generation.py`. Persist one self-contained view of the requested occurrences and their effective reference bindings and tags. It must not depend on scratch files. Plan 66 CC-3 extends this same view; do not build a second one in `compilation.json`. | `test_generation.py`, `test_parent_receipt_readback.py`, `tests/sdk/test_generation_result_refs.py`. Read one mixed request through the dry run and through result reconstruction from a settled CPU fixture. Every row (occurrence, tag, trim, slot) matches the graph, and the view reads the same after scratch cleanup. | [ ] |
| SR-7 Add both recipes as request fixtures, with short notes | T | SR-3, SR-4, SR-5 | Two complete request files that the admission test loads: start image plus speaker clip; mouth mask plus speaker clip. Plan 66 CC-5 later turns them into recipe files by adding holes. In `docs/SKILL.md` and `docs/recast-scene/SKILL.md` add only short notes: the limits from the table, the frame-0 rule, and that room tone inside the window is regenerated. Do not write long prose recipes; Plan 66 CC-6 owns the final skill wording. Describe voice tags only as an unverified model prompt convention, of the form `<Audio 1> is the voice-timbre reference for <Subject 1> (S1)`. Do not say it binds a voice to a face, and do not imply that CPU admission proves the effect. | `test_skill_examples_admitted.py` loads and admits both request files. `tests/test_pack_declared_skills.py` passes. | [ ] |
| R Review rounds (at most 1, recommended) | S | SR-1 through SR-7 | Read-only integrated result; high-judgment reviewer (Astra or Opus). | Check the CPU proofs above against the plan's completion list and owner decisions. Findings become rows `R1.<n>` under the [run contract](../../skills/shared/run-contract.md) and close before completion. | [ ] |

## Terms

- **Occurrence:** one use of one asset in the request. Two trims of the same file are two occurrences.
- **`use: conditioning | replacement`:** set once per audio occurrence at normalization. An audio clip named by a replacement edit is `replacement`; every other audio clip is `conditioning`. One occurrence with both uses is refused. Every later step reads this field and never recomputes it.
- **`audio_strength`:** the V2V node's single audio value for the whole clip. `0` keeps the source audio latent unchanged; `1` regenerates all of it. In this plan it stays bound to `0`. Time-varying audio comes from a separate audio mask applied after V2V with `MiniMaxH3SetAVNoiseMask` (SR-5).
- **Audio mask value:** 0 means keep (the model hears it); 1 means fully generate; values between are partial and untested.
- **Effective rows:** the references in the order the node actually receives them, which fixes their prompt tags (`<Picture n>`, `<Video n>`, `<Audio n>`).

## SR-1 detail

- At normalization, give each media-list item a stable occurrence key from its authored list position, not its asset id. Repeated assets and repeated trims stay separate occurrences.
- Give each reference occurrence its modality, trim and, for audio, its `use`. A video reference contributes its soundtrack only when the node binding includes it. Record that as one video occurrence with its video input and an optional soundtrack input, not as a second authored audio occurrence.
- Carry all of these through normalization into the record. Touch `spec.py` only where the record needs it, including `sampling_passes` and `sampling_request_document`.
- **The clean break (Plan 66 D4):** request identity is derived from author intent: modality, role, trim or range, placement, edit and `use` intent, occurrence order, model and sampling settings. Resolved paths, measured metadata and generated files never enter identity.
  - Derived prompt tags (`model_tags`, and each occurrence's `model_tag`) leave the identity and the normalized request. SR-3 derives tags from the effective rows.
  - v1 requests are not refused here. The plain-input hook still builds v1 until Plan 66 CC-1.3, and Plan 66 CC-1.4 then refuses v1.
  - Already-sealed builds and settled receipts still read: the reader verifies the stored bytes in their recorded format instead of renormalizing them. Add a pre-SR-1 sealed fixture that proves it.
  - Resuming an old in-flight build refuses with "rebuild this request", rather than comparing against a new digest.
- Plan 66 CC-1.1 owns the final job type. Do not add a second, parallel record definition here.
- Regions in one pass share one seed and one reference set, because there is one sampler and conditioning is global. They may differ in interval and strength. Keep two masks: a binary permission mask for paste-back, and a separate sampler-strength mask ([Permission and strength](../66-h3-composable-core/tasks.md#functional-additions-two-masks)). A grant whose footprint vanishes on the model's grid fails, naming the grant. Refuse per-grant seeds or reference sets that differ. Several audio windows are allowed (SR-5).

## SR-2 detail

One table, in one place. Plan 65 adds no second copy:

| Entry | Value |
| --- | --- |
| Builder images / videos / standalone audio | 9 / 3 / 3 |
| Character Swap adapter | needs the Ref2VA base, at least one video (`<Video 1>`, the performance) and at least one image (`<Picture 1>`, the character); further references are allowed but untested |
| Continuation images / videos | 2 / 0 |
| Per clip | 2–15 seconds |
| Per modality total | 15 seconds. A video's enabled soundtrack and standalone audio clips share the 15-second audio total; soundtracks need no slot limit of their own, because each belongs to one of at most three videos. |
| Conditioning files | 12 |
| Audio grant strength | 0 to 1 (values between untested) |
| Regions per pass | one seed, one reference set |
| Width and height | 32–16384, multiples of 32 (Plan 65 reads this) |

Keep two blocks in the table: **model limits** (the node's facts: 9/3/3, the clip times, 12 files, size) and **lowering limits** (what an Astrid lowering can't do yet: the Character Swap 1/1 and continuation 2/0 rows). Remove each lowering restriction only when its replacement lowering has a positive test. Measured-media errors (unreadable file, trim past the end) stay with the probe that finds them.

- Before claim, `prepare.py` measures each conditioning occurrence's real file with the existing probe and per-stream coverage routines in `compile.py`.
- Count image, video and standalone-audio effective inputs separately against the 9/3/3 slots.
- Each supplied image, video and standalone-audio occurrence counts once toward the 12-file limit, including repeats with different trims. A video's enabled soundtrack counts toward audio time but not as a second file.
- For duration, measure the selected trimmed interval after probing the file. Reject an unreadable stream, or a trim whose end goes past the measured stream duration. Sum the selected durations per effective modality.
- Fixed replacement audio is a placed item, so it counts toward no conditioning limit.
- Every refusal message names the table entry it broke.
- Give the table a source column (node, model card or Astrid). Per clip 2–15 seconds, per modality 15 seconds and 12 conditioning files come from the model card. Replace the masked edit's own 15-second refusal with one duration row for all jobs, which warns outside 124–362 frames.

## SR-3 detail

`GenerationInputs` is a frozen dataclass in `shared/generation.py` with exactly these fields. Add a field only when a test needs it, and name that test in the PR:

- `canvas`: size and frames (size is 1024×576 until Plan 65);
- `placed`: placed items (source clip, still, fixed audio) with their spans;
- `grants`: each grant keeps together its stream, interval, source occurrence, optional region raster (white means *edit*, as today), strength, seed and associated references. Composition keeps everything no grant covers;
- `conditioning`: the effective reference rows;
- `prompt`, `model` (base, and adapter for Character Swap), `sampling` (today's controls, passed through unchanged).

The fields are named by the core model, not by route, so [Plan 66](../66-h3-composable-core/plan.md) builds on them without a rename.

Rules:
- All three compilers build the record from the normalized v2 request and `build_generation_workflow(inputs)` takes only the record.
- Each effective reference row is `{occurrence, modality, trim, input_binding, tag}`. Derive the rows once, in the exact order they're passed to node slots, keeping the request order within each modality.
- A video's enabled soundtrack takes its audio tag before any standalone clip, because that's the order the node receives them (`ref_video_audios` before `ref_audios`). Even so, assert the order from the emitted graph, not from this sentence.
- Replace Character Swap's hard-coded tags in `compile.py` with lookups in the rows.
- Build the graph's custom-node requirements from the lowerings used. Replace the two-pack list in `astrid/packs/runpod/h3_release.py` `release_inputs` with one read from the pins, so a new pinned pack needs no code change there.
- Check only generated reference labels (`<Picture n>`, `<Video n>`, `<Audio n>`): a prompt naming a reference tag that no row has is refused. Don't scan or reject other angle-bracket text in the prompt.
- Adapter and mask combinations are decided by the limits table, not by fixed compiler refusals.

## SR-4 detail

- This is a special case of a placed exact still, implemented through the job's placed-item and grant rules. Don't add a separate frame-0-only compiler path. Plan 66 CC-8 owns exact stills at other frames, and keeps this case as a compatibility fixture.
- A `role: timeline` image with `at: {frame: 0}` is a placed still. Lower it to the existing source-backed path: the still becomes the source's frame 0, video is generated from frame 1, and audio is generated: the SR-5 audio mask is 1 over the whole clip, with V2V `audio_strength` 0. That way the model sees the still, so frame 1 continues from it.
- **This is more than a paste.** Preparation must build the source from the still: a full-canvas-length video whose frames all hold the still (the builder needs a source as long as the output), plus silent audio that nobody supplied and that is entirely generated. Use a CPU fixture with only the still and no user audio.
- Composition writes the prepared still over decoded frame 0, through the existing paste-back.
- A placed still at any other frame is refused from the limits table, as a lowering limit. [Plan 66](../66-h3-composable-core/plan.md) adds soft guides at other frames (CC-4) and exact stills at any frame (CC-8).
- No new node. See [research/first-frame.md](research/first-frame.md).

## SR-5 detail

Two kinds of audio, kept apart:
- **Generated audio:** any number of audio windows is allowed. Wire it like this (resolved from the pinned motion pack, `existing_video_extension.py` `MiniMaxH3SetAVNoiseMask`):
  1. Build a time MASK of shape `[F, 1, 1]` over the full target duration, one value per video frame. Each frame is 0 outside generated-audio grants and on supplied-audio spans, and the grant's audio strength inside generated grants.
  2. Keep source audio connected to `H3V2VGranularFractionalDenoise.source_audio`, and bind its `audio_strength` to `0`.
  3. Connect V2V's output LATENT to `MiniMaxH3SetAVNoiseMask.latent`, and the time MASK to its `audio_mask`. Leave its `video_mask` disconnected: that keeps V2V's video mask unchanged.
  4. Connect `MiniMaxH3SetAVNoiseMask`'s output LATENT to the sampler's `latent_image`.
  5. Pre-splice supplied fixed PCM into `source_audio` before the VAE encode, so the model hears it.
  6. Give the mask a producer: name the CPU artifact format, its managed binding, the loader and the conversion to an `[F, 1, 1]` MASK. Verify the decoded values and frame count through the same binding used for submission. Build it from the measured sample overlap per frame, following the ordered cell rules in [One AV mask pair](../66-h3-composable-core/tasks.md#functional-additions-masks).
- **Order matters.** The node replaces V2V's constant audio mask; it doesn't combine with it. Never put it before V2V, because V2V would then overwrite the time mask. Never supply its `video_mask` in this task.
- **What the model hears.** The model hears kept and supplied audio while it generates the rest. A clip-wide `audio_strength` of 1 would make it ignore kept audio and lip-sync to invented sound.
- **Boundaries (D4).** The node averages each frame's mask, then linearly resamples the F frame values onto H3's 40 Hz audio latent steps, so a sharp edge can become a short ramp in what the model sees. That is accepted. Delivered audio stays exact, because composition decides it, not the mask. The dry run shows the resampled mask.
- **Supplied audio (a fixed replacement clip):** a placed audio item in the record, even though the request spells it as it does today. On its own interval its samples win over anything generated, spliced exactly. Exactness is checked per channel and per sample on the decoded published file ([Exact delivery](../66-h3-composable-core/tasks.md#functional-additions-exact)). A one-sample duration tolerance is a separate, weaker claim, and never stands in for exact identity. The fixed-clip path with no generated audio keeps strength 0, its splice and its fallback.
- **The mixed case** (one interval with supplied audio, another generating audio) is allowed. The audio mask is 0 on the supplied interval, so the model hears it. Composition splices the supplied samples exactly on their interval, and generated samples are used on the other.
- **Composition** keeps source audio outside every audio grant, using the existing per-stream audio segments.
- Record three things separately in the dry run, because they're different evidence: the requested audio grants, the effective (resampled) audio mask, and the delivered sample spans.

## Existing tests that change

- `test_edit_inputs.py`:
  - the image-only video-guide refusal becomes selection of a separately named audio conditioning occurrence;
  - the two "only two image slots" masked refusals become affirmative cases: one conditioning clip, three images;
  - the invalid fixed-audio guide refusal stays.
- `test_compile_generalized.py`: the captured continuation's two-slot refusal stays.
- All other fixed-audio and image-only fixtures stay.
