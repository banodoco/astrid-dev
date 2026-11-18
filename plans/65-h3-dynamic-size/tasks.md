# Tasks — H3 dynamic output size

[Plan](plan.md) · [Inputs](inputs.md)

**Task ids:** `DS-1` … `DS-6`.

**Critical path:** DS-1 → DS-4 → DS-6.

**Test inventory:**
- `tests/packs/h3_av/test_edit_inputs.py` (digests);
- `tests/packs/h3_av/test_conform*.py`;
- `tests/packs/h3_av/test_non16x9_masked_edit_cpu.py`;
- `tests/packs/h3_av/test_character_swap*.py`;
- `tests/v10/test_media_mask.py`;
- `tests/test_pack_declared_skills.py`.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| DS-1 Request field and one carried value: `output.size` (D1), validated against the node's 32–16384 / step-32 rules; the normalised request carries it; default 1024×576 | N | D1 | `astrid/packs/h3_av/shared/request_v2.py` (output normalisation), `schemas/` for the v2 request | New tests: valid sizes accepted, an off-grid or tiny size refused at dry run; size-free requests normalise unchanged | [ ] |
| DS-2 Conform, preflight and preparation use the carried size | N | DS-1 | `astrid/packs/h3_av/shared/conform.py` (fill/fit ~180-225), `prepare.py` (~243-267, 452, 477-478) | New tests: a non-default size conforms and is recorded in the manifest; existing conform tests unchanged | [ ] |
| DS-3 Generation and compiler use the carried size: ReferenceToVideo width/height, the preserved-tail mask, full-frame regions | N | DS-1 | `astrid/packs/h3_av/shared/generation.py` (~367-376, 424-425), `compile.py` (~487, 499, 568, 570, 594) | New test: the compiled graph binds the requested width/height; `test_edit_inputs.py` digests byte-identical for size-free requests | [ ] |
| DS-4 Size-independent masks resolved once (D2): `static_regions.resolve_static_region` resamples an image mask, or scales boxes, to the working size, and its result is reused by generation and composition (no second resampling); `media mask --preview-on` previews at the request's size | X | DS-1 | `astrid/packs/h3_av/shared/static_regions.py`, `compose.py` (~661-675 reuse the resolved mask), `astrid/core/media_mask.py` | New tests: a 1024×576 mask resolves correctly at 768×432 and 256×144 (binary, aligned); composition uses the resolved mask; preview at the request's size | [ ] |
| DS-5 Docs: `output.size` and its rules, the mask coordinate space, a small-size note for voice-only takes, the continuation limit if any | T | DS-2, DS-3, DS-4 | `astrid/packs/h3_av/docs/SKILL.md`, `astrid/packs/h3_av/docs/recast-scene/SKILL.md` | `tests/test_pack_declared_skills.py` | [ ] |
| DS-6 Live proof: (a) voice-only continuation at 256×144 vs 1024×576, same request otherwise; (b) a lens edit at 768×432 | N | DS-2, DS-3, DS-4 | read-only; receipts under the plan's `evidence/` | Two to three RunPod jobs (≤ $1.50): (a) transcripts match, GPU time lower; (b) `timelines visualize --compare-media` MATCH outside the mask | [ ] |
| R Review rounds (at most 1, agreed with the owner) | S | all other tasks | read-only | Rounds per the [run contract](../../skills/shared/run-contract.md): findings become rows `R1.<n>` added directly below this one; publishing waits for them | [ ] |

The continuation route compiles a captured graph. If DS-3 finds it can't take a size without a graph change, that route keeps 1024×576 and refuses another size with a clear message, and the limit is recorded in DS-5. Checks use astrid-dev's [shared worker environment](../../env/README.md). Re-check the file:line references against the code at dispatch.
