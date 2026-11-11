# Release 12 H3 CPU evidence record

This record preserves static and CPU-side evidence for Agent candidate [`6a2351d95bb7eabc8b0ff6f988163fe420fcb3d7`](https://github.com/banodoco/astrid-agent/commit/6a2351d95bb7eabc8b0ff6f988163fe420fcb3d7). It records sampled graph construction and source-schema checks only. It does not establish target compatibility, model availability, GPU support, or successful H3 execution.

## Pinned sources

- Agent candidate: `6a2351d95bb7eabc8b0ff6f988163fe420fcb3d7`
- VibeComfy: [`8d065a8fef3dd602d5462e27d8eca088cf4e8262`](https://github.com/banodoco/vibecomfy/commit/8d065a8fef3dd602d5462e27d8eca088cf4e8262)
- ComfyUI: [`ee71d5c4993f29086b27fde1629a945ae48425bf`](https://github.com/Comfy-Org/ComfyUI/commit/ee71d5c4993f29086b27fde1629a945ae48425bf)
- H3 extension source: [`361624fb406b63eb6694442eac6c895fc1533a70`](https://github.com/seitanism/ComfyUI-H3-Motion-Context-MultiRef/commit/361624fb406b63eb6694442eac6c895fc1533a70)
- VideoHelperSuite: [`4ee72c065db22c9d96c2427954dc69e7b908444b`](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite/commit/4ee72c065db22c9d96c2427954dc69e7b908444b)

## Preserved API graph samples

These JSON files were inspected before inclusion. Prompt strings are synthetic (`A scene.` and `Continue the source.`); the reference filename is synthetic. The H3 extension source audit covered the direct-builder generation sample and the two continuation samples. The separate orchestrated generation sample came through normalize, prepare, compile, and current Vibe load/compile; it uses a one-second, source-free request with one image reference and raw-frame length 39 (5 + 2×17).

| Artifact | SHA-256 | Sample |
|---|---|---|
| [`generation-orchestrated.json`](api/generation-orchestrated.json) | `77cef8a741c370716cdc6f07efb67c6f4555d55550800f7ffa995e7116bd5661` | Orchestrated source-free, one-reference generation |
| [`generation-direct-builder.json`](api/generation-direct-builder.json) | `e62eff756149696fd90102e2a66cdd3821beded3d1dccf842e726fe56c01169f` | Direct-builder generation capture used in extension audit; not the orchestrated sample |
| [`continuation-zero-reference.json`](api/continuation-zero-reference.json) | `2619f4181dd198ecb0e30890d974ea2aaa21faa6e507ee4c514160d2c4bd5a32` | Source-backed continuation, zero references |
| [`continuation-one-reference.json`](api/continuation-one-reference.json) | `16b305fffc70f296f8ae10f4428fab6105b127cd3e7035a8375017cc3dbbbfff` | Source-backed continuation, one reference |

The two continuation samples share the same H3 nodes and settings. The one-reference sample adds two dynamic reference links. The direct-builder capture has 24 raw frames; it is distinct from the orchestrated sample's 39-frame request.

## Findings

The source-only audit mapped 12 included H3 classes in the immediate extension-audit captures, excluding `MiniMaxH3ReferenceToVideo` and `MiniMaxH3SigmaShift` as specified for that audit. Captured H3 enum values and checked literal values matched the pinned extension declarations. H3 output indices/types matched the inspected H3-to-H3 links. The core/VHS audit found source definitions or mappings for sampled core/VHS classes and checked selected inputs and output links, including the orchestrated generation graph. These checks were partial static source analysis; they did not execute node registration or prove exhaustive schemas.

A reproducible pre-existing defect remains in the one-reference continuation sample: `MiniMaxH3ReferenceToVideo` node `110` binds `ref_image_0` to managed image node `1020`, but binds `ref_image_1` to node `1021`, whose `image` value is empty. The exact P40 parent `d8931c281cf705273c3c7c01346b6f2722733cca`, with VibeComfy `e65f4941d09b1cb4d1dd5aae6171c73e648706f4`, emits the same binding, so the evidence does not attribute it to the candidate. Repair ownership of emitted image bindings and test zero, one, and two actual references before relying on this path.

Other open checks:

- The `comfy kitchen attention` enum is conditional on ComfyUI's GPU-support flag; target capability and registered options are unverified.
- Named model files and staged input files were not checked against a target inventory or byte manifests.
- Installed node registration and exhaustive input types, enum choices, bounds, dynamic sockets, and all link schemas remain unproven. The historical ComfyUI object-info overlay has a baseline-reproduced SHA-256 mismatch; it is not treated as current schema evidence.
- Linked runtime values such as expression-computed frame length and selected canvas dimensions were not verified against actual media.
- Regenerated-audio, live-starter, extra extension slots, two distinct references, and masked/edit variants are outside these samples.
- The exact managed install/doctor selector was not validated in its intended installed environment; supplementary Python checks do not replace that proof.

Release 12 explicitly excludes H3 GPU qualification. No provider call, GPU run, target compatibility claim, or H3 pass is asserted here. Separately observed baseline test failures remain routed to Plan 39; this record does not suppress or reinterpret them.

## Bounded frame and canvas CPU probe

The archived [`frame-canvas-proof.py`](frame-canvas-proof.py) and its [`captured output`](frame-canvas-proof.log) record a bounded CPU probe. The source methods were read from these exact pins:

- Agent `6a2351d95bb7eabc8b0ff6f988163fe420fcb3d7`: [`plan_continuation`](https://github.com/banodoco/astrid-agent/blob/6a2351d95bb7eabc8b0ff6f988163fe420fcb3d7/astrid/packs/h3_av/shared/timing.py#L92).
- ComfyUI `ee71d5c4993f29086b27fde1629a945ae48425bf`: [`MathExpressionNode.execute`](https://github.com/Comfy-Org/ComfyUI/blob/ee71d5c4993f29086b27fde1629a945ae48425bf/comfy_extras/nodes_math.py#L86), and [`ResolutionSelector.execute` plus aspect-ratio table](https://github.com/Comfy-Org/ComfyUI/blob/ee71d5c4993f29086b27fde1629a945ae48425bf/comfy_extras/nodes_resolution.py#L18).
- H3 extension `361624fb406b63eb6694442eac6c895fc1533a70`: [`MiniMaxH3CropTo32.crop_to_32` and `MiniMaxH3StartCanvasSelector.select`](https://github.com/seitanism/ComfyUI-H3-Motion-Context-MultiRef/blob/361624fb406b63eb6694442eac6c895fc1533a70/h3_auto_crop32.py#L26).

Eight requests used a 24-frame source and total requested output lengths of 25, 26, 41, 42, 48, 120, 240, and 362 frames. The planner/evaluated node values were respectively `(requested new, workflow seconds, raw extension, trim tail)`: `(1, 2.33333333333, 56, 16)`, `(2, 2.33333333333, 56, 15)`, `(17, 2.33333333333, 56, 0)`, `(18, 3.04166666667, 73, 16)`, `(24, 3.04166666667, 73, 10)`, `(96, 5.875, 141, 6)`, `(216, 10.8333333333, 260, 5)`, and `(338, 15.7916666667, 379, 2)`. Each raw extension met the probe's `5 + 17k` rule and its explicit `5..3600` assertion.

Five fake image shapes exercised the crop and existing-video canvas methods: `1024×576 → 1024×576`, `1920×1080 → 1920×1056`, `641×479 → 640×448`, `32×32 → 32×32`, and `16385×8193 → 16384×8192`. A separate `ResolutionSelector` sample (`16:9`, `0.5` megapixels, multiple `32`) returned `960×544`. Edge checks showed `31×100` refused as too small, while `16416×8192` remained `16416×8192`, above the `generated_width` input declaration's 16384 maximum. The existing-video source dimension inputs have no corresponding maximum in the inspected schema, and the selector itself does not enforce a returned-canvas bound.

This is deliberately a bounded source-method probe, not node execution: the expression evaluator accepts only the arithmetic/name/call AST subset used by the captured expression, rather than exercising the installed `simpleeval`; `io.NodeOutput` is inert, and the fake image reports dimensions while its slice operation returns a marker instead of slicing real pixels. The probe does not test installed registration, all inputs, actual media, actual model files, or GPU/runtime behavior. The UI/source numeric bounds checked here do not define the model's trained resolution range; treat sizes as advisory and consult target/model guidance for quality-sensitive use. The archived script retains the execution-time checkout paths, so rerunning it requires those exact source revisions and the candidate package that provides `plan_continuation`.
