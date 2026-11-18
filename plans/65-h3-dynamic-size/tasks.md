# Tasks — H3 dynamic output size

[Plan](plan.md) · [Inputs](inputs.md)

**Task ids:** `DS-1` … `DS-5`.

**Critical path:** Plan 64 SR-3 → DS-1 → (DS-2, DS-3 in parallel) → DS-4 → DS-5 → R.

**Test inventory:** Bare test filenames are under `tests/packs/h3_av/` in astrid-agent. Run them from the Agent checkout with the pinned worker command `env/agent-pytest.sh <paths>`. Run only the files a card names, not the whole suite. Product paths are under `astrid/packs/h3_av/` unless given in full. Cards name functions, not line numbers: find each function with `grep -n` at dispatch. Every task is CPU only (D2). No task claims a machine, rents a GPU or spends money. Request identity already broke once, in Plan 64 SR-1 (Plan 66 D4); when a graph changes here, regenerate its fixtures in the same commit and list each change with its reason.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| DS-1 Accept `output.size` and resolve it once | N | Plan 64 SR-3 | `shared/request_v2.py` `normalize_v2`; `schemas/request.v2.json`; `GenerationInputs.canvas` (from Plan 64); one `DEFAULT_SIZE = (1024, 576)` constant in `shared/generation.py`. Remove the separate default width/height parameters in `shared/prepare.py` `prepare_request`, so it reads the record. | `test_native_v2_contract.py`, `test_edit_inputs.py`, `test_lead_in.py`. Accepted: 32×32, 512×288, 768×448, 16384×16384. Refused before claim, naming the rule: 256×144, 768×432, 0, 16416, 512.5, `"512"`, `true`, a one-element or three-element list. No size and explicit 1024×576 give identical normalized bytes and digest; 512×288 differs and survives readback. Size is accepted on every route except continuation, where a non-default size is refused until Plan 66 CC-7; lead-in stays continuation-only. | [ ] |
| DS-2 Conform sources to the requested size | N | DS-1 | `shared/stages.py` `compile_stages`; `shared/prepare.py` source preflight and the frozen-source check; `shared/conform.py` fill, fit, pad, manifest and its hard-coded 16/9 aspect comparison (becomes width/height). Keep source DAR/SAR, audio and timing rules. | `test_automatic_conform.py`, `test_source_frame_fit.py`, `test_remote_prepared_source_handoff.py`. Decode 768×448 fill and fit frames from a source whose display aspect lies between 768/448 and 16/9; check crop, pad, landmark position, measured size and manifest. A remote build reuses frozen bytes of the matching size without reconforming, and refuses a size mismatch. Default-size cases unchanged. | [ ] |
| DS-3 Rasterize each static mask once at the target size and give composition that file | X | DS-1 | `shared/static_regions.py` `resolve_static_region`; `shared/compile.py` `_union_static_masks` and `_compile_native_masked_edit`; `shared/compose.py` `_spatial_video_masks`; mask schema plus `shared/spec.py` round trip for `mask.canvas`. Moving masks: no change. Details below. | `test_static_regions.py`, `test_static_mask_preflight.py`, `test_non16x9_masked_edit_cpu.py`, `test_mask_contract.py`, `test_spec.py`, `test_moving_masks.py` (unchanged and passing). The still-image exact-size refusal in `test_static_regions.py` and the original-size refusal in `test_non16x9_masked_edit_cpu.py` become decoded-coordinate checks. Fixtures below. | [ ] |
| DS-4 Bind size at every generation entry point except continuation | X | DS-2, DS-3 | `shared/generation.py` `build_generation_workflow` (canvas and tail mask read `inputs.canvas`); `shared/compile.py` generation, masked, full-frame and Character Swap entry points Do not touch the captured continuation workflows (D1). Effective size in `shared/stages.py` `_sealed_plan` and the workflow hooks. | `test_generation.py`, `test_native_masked_edit.py`, `test_character_swap.py`, `test_character_swap_cpu_boundary.py`, `tests/core/generation/test_catalog_entries_dry_run.py`, `tests/core/generation/test_local_job_h3_evidence.py`. At 1024×576 and 512×288, every width/height binding in every emitted graph equals the request. Dry run and the retained `h3.plan` result show the size, also after scratch cleanup. Default-size graphs are unchanged node for node. | [ ] |
| DS-5 Document size | T | DS-4 | `docs/SKILL.md`, `docs/recast-scene/SKILL.md`, the default and route descriptions in `profiles/native-v2.yaml`, the workflow input description in `extensions/vibecomfy.workflows/h3.yaml`. State the rule (32–16384, multiples of 32), the 1024×576 default, `mask.canvas`, that quality is only known at tested sizes, and the voice-only use from [#885](https://github.com/banodoco/astrid-dev/issues/885). | `test_skill_examples_admitted.py` admits a 512×288 image-guided speech example and a 768×448 masked-edit example. `tests/test_pack_declared_skills.py` passes. | [ ] |
| R Review rounds (at most 1, recommended) | S | DS-1 through DS-5 | Integrated result, read-only, high-judgment reviewer. | Check the CPU proofs against the plan's completion list and owner decisions. Findings become rows `R1.<n>` under the [run contract](../../skills/shared/run-contract.md); closing waits for them. | [ ] |

## DS-3 detail

**Rectangle masks.**
- A box may state `mask.canvas: [w, h]`, its authored canvas. Without it, the canvas is 1024×576, which is what every existing box was drawn on.
- Validate the half-open box inside its canvas, then scale the left/right edges by `target_w / canvas_w` and the top/bottom edges by `target_h / canvas_h`.
- Round each scaled edge with `ceil(edge - 0.5)` and clip it to the target. This keeps today's pixel-centre inclusion.
- Coordinates describe the prepared view, fit bars included.

**Still-image masks.**
- The still's own pixel size is its canvas.
- Check it's grayscale and binary (or apply the existing threshold), then resample it to the target with nearest-neighbour.

**The handoff.**
- The masked compiler rasterizes each static mask once at the target size, combines compatible masks by pixel maximum, and uses the existing bounded-frame encoding for a partial window.
- It binds that file to generation and passes the same file to composition through the existing managed artifact handoff.
- Composition reads the file. It no longer redraws rectangles, falls back to the original asset or resizes a second time.
- Keep today's union rules (same interval, strength, seed and references) and every existing refusal: polarity, threshold, invalid box, and moving-mask codec, size and clock.

**Fixtures.**
- A non-16:9 source with a small off-centre landmark, cropped and letterboxed at 768×448.
- A 1024×576 authored box used at 512×288.
- Adjacent fractional edges, and a two-region union.
- Compare decoded output with the prepared source outside the mask. Change candidate pixels both inside and outside, so a wrong mask fails.
- For `media mask --preview-on`, `--size` stays the target (default: the stored raster). The stored bytes and recipe are identical after a preview.
