# Tasks — H3 speaker references

[Plan](plan.md) · [Inputs](inputs.md)

**Task ids:** `SR-1` … `SR-6`.

**Critical path:** SR-1 → SR-2 → SR-4 → SR-6.

**Test inventory:**
- `tests/packs/h3_av/test_edit_inputs.py` (image-only digests);
- `tests/packs/h3_av/test_character_swap*.py`;
- `tests/packs/h3_av/test_native_v2_contract.py`;
- `tests/packs/h3_av/test_request_contract.py`;
- `tests/test_pack_declared_skills.py`.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| SR-1 GPU spike: start image + one speaker reference clip, `audio_vae` connected, via the plain VibeComfy workflow route; measure voice match, transcript, time, VRAM | N | — | read-only for product code; a spike workflow file under the plan's `evidence/` | One RunPod job on an RTX 5090 (≤ $1.50): `timelines transcripts run` shows the line; the owner judges the voice; time and VRAM recorded against a no-reference baseline | [ ] |
| SR-2 One reference lowering: `media` references → image/video/audio rows for `build_generation_workflow`, used by source-free, masked edit and Character Swap; capacities in one table pinned to the node schema; delete the masked edit's two-slot limit and the per-stream `EDIT_GUIDE_MODALITIES` growth; source-free calls the builder directly | X | SR-1 (D1) | `astrid/packs/h3_av/shared/request_v2.py`, `compile.py` (source-free, masked edit and Character Swap reference paths), `generation.py:build_generation_workflow` (add the `ref_audios` loader loop) | New tests: rows and node inputs for 1 image + 1 video (+ soundtrack) + 1 audio on source-free and masked edit; the capacity table matches the `object_info` autogrow max; refusals for a 4th video, a 16 s clip, unmeasurable durations. Existing: `test_edit_inputs.py` byte-identical digests, Character Swap tests unchanged | [ ] |
| SR-3 Masked-edit audio generate: an audio edit with `action: generate` and no guides maps to audio strength 1; a reference named by an audio edit's `guides` stays the fixed clip (legacy) | X | SR-1 (D1) | `astrid/packs/h3_av/shared/compile.py` (masked-edit audio rule ~545), `generation.py` (audio strength binding ~440) | New tests: audio generate binds strength 1 in the window; fixed-clip requests compile byte-identically | [ ] |
| SR-4 Records: the dry run and result list each reference's tag, range and node slot (alongside effective settings if `p59/h3-overrides` is merged) | N | SR-2 | `astrid/packs/h3_av/shared/stages.py`, `astrid/sdk/generation.py` (settings record) | New test: the dry-run plan lists the rows for a mixed request | [ ] |
| SR-5 Docs: the references table and two recipes in the H3 SKILL; "start image + speaker reference" in the recast rubric's "new line" table; list of node inputs the pack still doesn't expose (`ref_image_size`, width/height, `first_frame`/`last_frame`, AddGuide, Fun ControlNet) | T | SR-2, SR-3 | `astrid/packs/h3_av/docs/SKILL.md`, `astrid/packs/h3_av/docs/recast-scene/SKILL.md` | `tests/test_pack_declared_skills.py` | [ ] |
| SR-6 Live proof on 02c: (a) source-free, start image = corrected lens frame + Morpheus reference; (b) masked mouth + same reference + audio generate | N | SR-2, SR-3, SR-4 | read-only; requests and receipts under the plan's `evidence/` | Two RunPod jobs (≤ $1.50): transcript shows exactly the line; the owner recognises the voice; `timelines visualize --compare-media` shows lenses or kept picture intact | [ ] |
| R Review rounds (at most 1, agreed with the owner) | S | all other tasks | read-only | Rounds per the [run contract](../../skills/shared/run-contract.md): findings become rows `R1.<n>` added directly below this one; publishing waits for them | [ ] |

SR-2 and SR-3 change different functions in `compile.py` and `generation.py`. They run in parallel, with the merge order SR-2 then SR-3. Checks use astrid-dev's [shared worker environment](../../env/README.md). Re-check SR-2's pinned-test list against the code at dispatch.
