# Release 12 H3 CPU evidence record

This record preserves static and CPU-side evidence for Agent candidate [`6a2351d95bb7eabc8b0ff6f988163fe420fcb3d7`](https://github.com/banodoco/astrid-agent/commit/6a2351d95bb7eabc8b0ff6f988163fe420fcb3d7). It records sampled graph construction and source-schema checks only. It does not establish target compatibility, model availability, GPU support, or successful H3 execution.

## Pinned sources

- Agent candidate: `6a2351d95bb7eabc8b0ff6f988163fe420fcb3d7`
- VibeComfy: [`8d065a8fef3dd602d5462e27d8eca088cf4e8262`](https://github.com/banodoco/vibecomfy/commit/8d065a8fef3dd602d5462e27d8eca088cf4e8262)
- ComfyUI: [`ee71d5c4993f29086b27fde1629a945ae48425bf`](https://github.com/comfyanonymous/ComfyUI/commit/ee71d5c4993f29086b27fde1629a945ae48425bf)
- H3 extension source: [`361624fb406b63eb6694442eac6c895fc1533a70`](https://github.com/banodoco/ComfyUI-Minimax-Hailuo-2.3/commit/361624fb406b63eb6694442eac6c895fc1533a70)
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
