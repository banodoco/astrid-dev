# Tasks — H3 one compiler

[Plan](plan.md) · [Inputs](inputs.md)

**Task ids:** `CC-1.1` … `CC-1.4`, `RS1`, `CC-2`, `CC-3`, `CC-9`, `CC-10`, `CC-5`, `CC-6`, `CC-13a`, `CC-13b`, `CC-14`, `CC-15`; the closing review is the H3 programme's integrated review, [Plan 67 R](../67-h3-community-steering/tasks.md). Ids are labels kept from before the split, so research files and other plans still resolve; the critical path below is the order. CC-4 and CC-8 moved to [Plan 68](../68-h3-guides-and-stills/tasks.md); CC-7a to CC-7d moved to [Plan 70](../70-h3-continuation-bridges-inserts/tasks.md).

**Critical path:** refreshed 59/64/65 baseline → CC-1.1 with CC-9 → RS1 job-record half → CC-1.2 → CC-2 → CC-13a → RS1 contract half, with CC-1.3 → CC-1.4 beside it → Plans 68, 70 and 67. After RS1: CC-13b (also needs CC-1.3 and CC-15), CC-14, CC-3, CC-10 and CC-5 → CC-6. Plans 68, 70 and 67 wait only for RS1 and the specific cards their own Depends name (28 Nov 2026).

Each CC-1 card can be merged on its own and leaves the public invocation working. Shared functions (the job record, table, view writer, compositor) have one writer at a time; a shared filename alone is not a dependency. This plan adds no new creative capability, so its live check is a clean regression check.

**Provider contract for CC-13/CC-3:** Review at dispatch against current Agent and the [67 dependency assessment](../67-h3-community-steering/inputs.md#provider-boundary-and-plan-17-dependency-27-nov-2026). Keep the seam inside H3 (e.g. `shared/` next to `LIMITS` and `compile_job`); the reviewer fixes exact module names and versioned typed signatures before execution. Provider metadata declares stable qualified ID, capability rows, admitted fields/limits/conflicts, mechanism(s), dependency IDs and pinned node/model requirements. A provider returns typed lowering inputs, never arbitrary graph mutation, private host state, a second route or exact-delivery overrides. It may also declare validated references to its ordinary pack-owned input-making actions/recipes, projected in the same discovery view. Such an action is not a lever and its outputs enter normal bindings. No direct imports of third-party pack internals by H3; the approved existing extension host maps contributions into the seam in 67. Preserve the stricter existing `tests/packs/h3_av/test_no_astrid_imports.py` guard unchanged (all Astrid imports prohibited in kept H3 modules, not merely private imports); carry the admitted snapshot through the existing host workflow hook/engine-facts boundary, with no global lookup in H3. The host supplies the input; the H3 pack owns its semantic contract. Assemble one deterministic validated snapshot, reject incompatible API, duplicate kind/ID and conflicts without last-loaded-wins, and bind identity/provenance to resolved job, dry run and receipt. Schema admits the supported structure; the snapshot remains the authority for semantics. Unit proof uses a separately authored fixture with no changes to H3 route dispatch, and baseline requests without it. No generic loader or distribution API; 67 maps admitted existing-registry contributions into this seam. Add the provider contract and author-facing limits to `docs/design.md`; no new creative behavior. Review 66/67 together before freezing this contract.

**Test inventory:** Bare test filenames are under `tests/packs/h3_av/` in astrid-agent. Run them from the Agent checkout with the pinned worker command `env/agent-pytest.sh <paths>`. Run only the files a card names, not the whole suite. Product paths are under `astrid/packs/h3_av/` unless given in full. Cards name functions, not line numbers: find each function with `grep -n` at dispatch, and re-check each caller and test list against the integrated code then. Every task is CPU only (D1). No task claims a machine, rents a GPU or spends money. Request identity was already broken once, in Plan 64 SR-1 (D4). When a task changes an emitted graph, regenerate its fixtures in the same commit and list each change with its reason. Do not add code to preserve an old digest.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| CC-1.1 Freeze one resolved job after measuring inputs | S | Plans 59, 64, 65 | `shared/prepare.py` (`prepare_request`: measurement, ownership and overlap validation); the job type, which is Plan 64's `GenerationInputs` in `shared/generation.py`, extended only with the fields below; `shared/compose.py` reads the job's intervals and grants; `shared/planner.py` keeps its ordered passes above the compiler; `shared/stages.py` persists and reloads the prepared job. Today's compile entry points stay and temporarily adapt the job to their existing inputs. Also carry `passes[]` (one entry) and `branches[]` (one entry, the existing Omni encoder) in the job record, unchanged for today's requests (28 Nov 2026). | `test_edit_inputs.py`, `test_real_media_preflight.py`, `test_planner.py`, `test_handle_build_compose.py`. Preparation measures each input once. It refuses two exact owners of the same stream and span, and two grants needing different shared sampler settings, before compilation, naming both grants and the conflicting field. The job serializes and reloads unchanged, its request digest is checked on reload, and composition reads its intervals and grants. No path or generated file appears in the request identity or the job's intent. Occurrence bindings, and conflicts checked after stream resolution, follow [Occurrences](#functional-additions-occurrences). | [ ] |
| CC-1.2 Make `compile_job(job, bindings, out_dir)` the only compiler entry point | S | CC-1.1, RS1 job-record half | `shared/compile.py` (`compile_job`; the former `_compile_generation`, `_compile_native_masked_edit` and `_compile_character_swap_v2` become feature lowerings it calls); `shared/generation.py` builder interface only as needed. The normalized request and the hook and CLI inputs stay as they are in this card; adapters at the compiler boundary turn them into a job. v1 stays for now. | `test_native_masked_edit.py`, `test_character_swap.py`, `test_character_swap_cpu_boundary.py`, `test_compile_generalized.py`, `test_handle_build_compose.py`. Each supported lowering is reached through `compile_job`. Bindings and graph inputs match today's for source-free prompt-and-reference generation, masked edit and Character Swap. The latent and its masks follow [One AV mask pair](#functional-additions-masks); each lowering declares which mechanisms it feeds and depends on, and `compile_job` resolves and checks those once. | [ ] |
| CC-1.3 Route every public and lifecycle caller through `compile_job` | X | CC-1.2 | Also settle the interim controller hooks added during the Release 14 Plans 59/64/65 integration (owner ruling, 21 Nov, REVIEW): the optional `inspect_inputs(inputs) -> InputRequirements` hook, the build result's optional `transport: BuildTransport` with the `publish_source` callback, and the entry-port flag `allow_output_handle_keys`. These hooks repaired Plan 59's core and SDK imports of `astrid.packs.h3_av` without naming the pack. Keep the generic `InputRequirements`/`BuildTransport`/`RemoteBuildTransport` contract: it has real public, local and remote consumers in `core/generation/workflows.py`. Have the host inject the factories and helpers H3 needs, so `hooks.py`, `shared/conform.py` and `shared/handoff.py` import nothing from Astrid and the unchanged no-Astrid-imports guard passes (it fails at `4a2bad18` today). Remove only duplicate request interpretation and flags with no consumer (28 Nov 2026). The boundary check and `tests/core/test_core_sdk_pack_neutral.py` must pass unchanged. `extensions/vibecomfy.workflows/hooks.py` (builds v2 instead of v1); `shared/stages.py` (`_sealed_plan` and the compile call); `shared/planner.py` (`plan_request` ordered passes); `astrid/core/generation/cli.py` only if it dispatches H3 compilation directly (trace the normal generate call first). Callers to migrate are listed below. | `test_native_v2_contract.py`, `test_planner.py`, `test_handle_build_compose.py`, `test_character_swap_cpu_boundary.py`, and the hook and CLI tests found at dispatch. Trace normalize → prepare → `compile_job` → compose → receipt for the public prompt-and-image invocation, a masked edit, a fixed-audio redub and Character Swap. A repository search shows no per-route compiler is called outside `compile_job`. One combined request that no former route accepted (a placed clip with a region grant and an audio grant, three image references and a speaker clip) compiles. Assert the concrete graph inputs for the source, region mask, reference slots and tags, speaker clip, audio grant and composition intervals. Every part of this request is Plan 64 behaviour, so it compiles. `compile_job` chooses lowerings from the features present, never from a classified shape. **One sampler survives the planner:** compatible simultaneous AV and regional grants are one sampling pass; keep sequencing only for explicitly ordered passes. Inspect the public plan and the emitted sampler count for the combined Recast job, including its one global seed and reference set. Ship the plain-input hook's v2 migration in this card, with the first public v1 refusal in CC-1.4. | [ ] |
| CC-1.4 Remove v1 and route classification | S | CC-1.3 | `shared/request.py` (v1 schema, profile and normalizer); `shared/request_v2.py` (`branch_for` and route classification); `shared/spec.py` (delete `H3Spec` and `canonical_spec` once their callers have moved; keep only helpers used elsewhere); `shared/compile.py` (delete obsolete route compilers and the CC-1.2 adapters); `schemas/request.v1.json` and the v1 profile files; hooks, CLI, planner, stages, and every test and fixture still using v1 or `H3Spec`. Keep `SamplingPass` and `sampling_passes` (moved out of `shared/spec.py` if that file is deleted): Plan 107 builds on them. | `test_request_contract.py`, `test_native_v2_contract.py`, `test_spec.py` (migrated or deleted, with each assertion's fate listed), `test_planner.py`, `test_compile_generalized.py`, `test_character_swap.py`, `test_handle_build_compose.py`, `test_cli.py`, `test_skill_examples_admitted.py`, `test_edit_binding.py`, `test_runtime_declaration_sync.py`. A v1 request is refused at the public request loader, before preparation, with: `Request version 1 is no longer supported; rewrite it as request v2.` There is no v1-to-v2 conversion. No route selector or `branch_for` remains. Every supported example compiles through `compile_job`. | [ ] |
| RS1 Review stop after the job contract | S | CC-1.1, CC-9 (job-record half); CC-1.4, CC-2, CC-13a (contract half) | Read-only. One round. | Job-record half: review the head with CC-1.1 and CC-9, including `passes[]` and `branches[]`. Contract half: review the integrated head with CC-1.1 to CC-1.4, CC-2 and CC-13a, and add the socket, footprint and admission boundaries to the trace; record its commit and the Plan 59, 64 and 65 bases. Trace input document → normalized intent → measured bindings → resolved job → compilation → composition → settled result. For each boundary list the fields allowed, the fields forbidden, the digest checked and where refusals happen. Confirm v1 is refused everywhere and nothing v1 is reachable. Confirm each grant keeps its stream, interval, occurrence, optional region raster and polarity, strength, seed and reference identity through prepare, compile and compose. Trace at least one generated-only, one placed-with-edit, one fixed-audio and one adapter job. Review the code; don't run checks. Each finding becomes a row `RS1.<n>` with owner, scope, proof and a dependency on RS1. CC-1.2 waits for the job-record half's last finding; Plans 68, 70 and 67 wait for the contract half's. | [ ] |
| CC-2 Capabilities in `describe`, refusals from one table | X | CC-1.2 | Extend the `LIMITS` table Plan 64 SR-2 added in `shared/generation.py`; do not create a second table. Key it by **lever kind** (place, edit, guide, reference, prompt, LoRA, control, settings). Each kind lists its family (Output, Context or Process), the shared fields it accepts (`asset`, `at`, `during`, `range`, `stream`, `mask`, `strength`, `phase`) with their defaults, its own `params`, its limits and its conflicts, and the node pack it needs (repository, commit and node classes; none for stock ComfyUI). A graph's node requirements are the union over the kinds it uses, so a job never requires a pack it doesn't use. `describe` prints kinds in that shape. `control` and the `phase` field are listed as `unavailable`: a request using either is refused from the table. Every kind carries a status: `compiles` by default, `live-tested` only with a run reference and date, and `unavailable` if no lowering exists. Each later card that adds a kind, field, limit or pair adds its rows and its `describe` fixture in that card. The `describe` capability format contains nothing specific to H3. Every row gets `source_kind` (`node_schema`, `model_card` or `astrid_rule`) and `source_ref` (a pinned schema path and property, a model-card section, or a task or rule id). A row without a verifiable source is an Astrid rule. An unsupported combination is a row naming a pair of request features (for example `adapter=character_swap` plus `audio_guide`), with a reason and a fix. `astrid/core/generation/cli.py`: add a `capabilities` object to the existing JSON from `generate describe --entry h3 --json`, holding exactly the rows and refusal pairs admission uses; keep the existing entry metadata and help. Adapter ids come from the table: the pack validator checks table membership, and the checked-in JSON Schema keeps only a structural string rule (JSON Schema can't read the Python table). Remove the hard-coded adapter refusal in the masked compiler; the table decides that pair. Also own the move deferred from Plan 64 SR-3 (18 Nov, REVIEW): replace `astrid/packs/runpod/h3_release.py` `release_inputs`' hard-coded node-pack list with one read from the worker pins, keeping or deliberately changing the Linux/Windows parity rule in `tests/packs/runpod/test_h3_release.py`, with proof on both platforms. | `test_edit_inputs.py`, `test_real_media_preflight.py`, `test_request_contract.py`, new `test_capabilities.py` (table and admission agree; CLI JSON serialization). Each numeric row is tested at its limit and one value past it, with its `source_ref` in the assertion message. Each unsupported pair is refused, naming both features by their request labels and giving one fix. `capabilities` in `describe` equals the table admission uses. No refusal an agent sees names an internal class or route (`LanPaint`, `SPEC-MIN`, node class names). Malformed, missing and corrupted inputs keep their own messages where they're read. Reserved paths and pre-claim refusals follow [Refusals and discovery](#functional-additions-refusals). The independently authored fixture and native controls use the same validated snapshot; base parity, provider provenance, exact used requirements and deterministic duplicate/version/conflict/absence refusals are proved before claim. A provider with no custom lowering can advertise a valid preprocessing action without changing base compiler behavior; reject dangling/unadmitted references. `test_no_astrid_imports.py` and the existing pack-neutral core/SDK guard pass unchanged. No default-add-on installer or special H3 loader in 66. | [ ] |

- REVIEW: public v2 source fit (crop/letterbox) at dynamic size: deferred from Plan 65 E4, 21 Nov

| CC-3 The dry run and the settled result show one resolved-job view | N | CC-1.3, CC-2 | Also owns the settled-result receipt rows moved from Plan 64 SR-6 (19 Nov, REVIEW). They go through a pack-neutral producer-hook evidence mechanism. Core and SDK carry one private, bounded, authenticated, fail-closed evidence object behind a capability or entry opt-in from the CC-2 table, and never name a pack. The pack owns its schema and interpretation. `tests/core/test_core_sdk_pack_neutral.py` passes unchanged. `shared/stages.py` `_sealed_plan`: serialize the resolved job as the single view, keeping every existing field used for publication selection, workflow checksum checks, the plan handle and the compilation handle; the workflow hooks; `astrid/sdk/results.py` result reconstruction (`_reconstruct_generation_result`, read by `astrid/sdk/generation.py`). This extends the view Plan 64 SR-6 started and replaces Plan 65 DS-4's size reporting. At dispatch, compare the merged `_sealed_plan` and both earlier proofs; keep their asserted fields unless replaced here, and list each changed fixture field with its reason. Carry selected provider IDs, API versions and pinned identities via the existing bounded pack-owned view, not a second receipt mechanism. | `tests/core/generation/test_catalog_entries_dry_run.py`, `test_parent_receipt_readback.py`, `tests/sdk/test_generation_result_refs.py`, and a hook test showing the dry run and the submitted result use the same serializer. All intervals are half-open: video in frame indices `[start, end)`, audio in sample indices `[start, end)`, with any seconds shown with units. A fixture whose grant crosses the frame-4 boundary shows three separate fields: the requested grants; the effective video latent spans, from H3's chunk rule (one 1-frame chunk, then 4-frame chunks, repeating every 17 frames); and the delivered ownership. It also shows the requested canvas, the raw sampled frame count, the delivered frame count after trimming (from the existing timing helpers), and each reference occurrence with its tag, modality, purpose and mechanism, without local paths, plus the final prompt string as sent to the text encoder. The settled result stores the view before scratch is deleted, and reconstructing it afterwards gives the same view without reading deleted paths. It also reports, per occurrence, the actual binding of each tag and the resource estimate ([Resources](#functional-additions-resources)), and persists the sealed intent view with request and compilation digests in the settled result manifest. A dry run lists expected frames and dimensions; decoded measurements come only from the settled result. Prove describe/admission/compile and the settled receipt agree on the selected provider snapshot; no scratch paths or H3 imports in neutral core. | [ ] |
| CC-9 End-relative time | X | CC-1.1 (same unit) | `shared/request_v2.py` normalization and `schemas/request.v2.json`: negative numbers and `end` in `at`, `during` and `range`. Keep typed frame, second and sample expressions through normalization. `at`/`during` resolve against the job's `duration`, and `range` against the measured stream clock of the source, inside CC-1.1's resolve step. A point `end` resolves to frame N−1; an interval `end` resolves to N (exclusive). The dry run shows every resolved time. Prompt tags (`<Picture n>` and so on) are given to references only, never to placed items or guides. Timed prompts are not in this plan; they are [Plan 67](../67-h3-community-steering/plan.md). See [Clocks](#functional-additions-clocks). | `test_native_v2_contract.py`, `test_request_contract.py`, new `test_time.py`. Cases: `range: [-2, end]` on a 6.3 s file resolves on each stream's own clock (video on the 24 fps grid, audio at 48 kHz), and the dry run shows both; `at: -2` and `at: end` on a 7 s job (`at: end` is frame 167); `during: [-2, end]` is `[120, 168)`; a time past the end is refused naming the item; a tag naming a placed item is refused. | [ ] |
| CC-10 Composition by occurrence and exact delivery | S | CC-1.1, CC-1.2 | `shared/compose.py`: paste each placed item from its own source at its own destination span and source offset, keyed by occurrence, instead of one source at one offset; generated frames fill uncovered spans; video clips, stills and fixed audio use the same paste, each on its own stream. The exact-delivery verifier described in [Exact delivery](#functional-additions-exact). Moved here from CC-8 because every later plan relies on it. | `test_handle_build_compose.py`, `test_native_masked_edit.py`, `test_native_v2_contract.py`. Two occurrences of one asset at different offsets each paste their own bytes; asymmetric stereo impulses, off-by-one samples and both signs of 40 Hz rounding are byte-identical per channel in the decoded published file; two exact owners of one stream and span are refused, naming both.  H3 is the only writer of `noise_mask`: contributions send mask claims (regenerate, freeze, strength, per stream) and composition restores kept content from the source, never from a pass's output. | [ ] |
| CC-5 Templates: list, show, fill, write, submit | X | CC-1.3, CC-2, Plan 59 | Ship the template machinery and recipes for the capabilities that exist after this plan (source-free generation, masked edit and redub, fixed-audio redub, Character Swap, speaker reference, frame-0 start still, and the captured-bundle continuation). Plans 68 and 70 add their own recipes. The template commands contain nothing specific to H3. Recipe files under `astrid/packs/h3_av/docs/recipes/`, plus each installed skill's own `recipes/` folder; `astrid/core/generation/cli.py`: `generate templates list`, `generate templates show NAME`, and `generate video --entry h3 --template NAME (--set hole=JSON … \| --from-shot SHOT) [--write FILE] [--dry-run]`. Fill contract below. No shot-plan schema change and no automatic take recording. | `test_skill_examples_admitted.py` rewritten to load the installed recipe files instead of extracting YAML from the skill, keeping its compiled-graph and mask-byte assertions. Each recipe is filled with typed fixture values (a quoted line of dialogue, a list of references, a numeric duration, one reused shot with an explicit occurrence), then normalizes, dry-runs and compiles. Refusals, each naming the hole and its declared source: a missing fill, an unknown hole, a duplicate fill, a type mismatch, a leftover marker. An ambiguous bare name is refused, listing the qualified choices. A `--write` file submits unchanged through the ordinary request path. | [ ] |
| CC-6 Rewrite the general H3 skill and thin Recast | N | CC-1.4, CC-5 | `docs/SKILL.md` takes its structure and length from [research/skill-draft.md](research/skill-draft.md) (families, ladder, time, shared fields, kinds), which a small model learned cold in two rounds ([research/haiku-tests.md](research/haiku-tests.md)). Write it for what exists after this plan, with the three skill guards in [Skill guards](#skill-guards); Plans 68 and 70 each add one short section. Rewrite every field name and example to match the shipped schema: `settings.adapters`, no `role: control`, no `phase`, recipes as JSON files with `{"$hole": …}` markers, and stills holding one or four frames. Do not copy an unsupported field into the skill. Also `docs/reference.md`, `pack.yaml`, `docs/recast-scene/SKILL.md`, `docs/recast-scene/brief.md`. Details below. | `test_skill_examples_admitted.py` (reads the installed recipe files, not YAML copied from either skill), `tests/test_pack_declared_skills.py`. Cold read: re-run the five asks in research/haiku-tests.md with a small model that can now call `describe` and `--dry-run`, and record each result. Then one more: a new agent with no context uses the skill to find the right recipe for a described shot, fills it, hits one missing hole, fixes it from the refusal and reaches a dry run. Record the shot description, chosen recipe, the refusal and its named source, the corrected fill and the dry-run handle. Keep the transcript free of secrets and machine claims. | [ ] |
| CC-13a Contribution schema, footprints, snapshot and admission | S | CC-2 | `shared/` beside `LIMITS` and `compile_job`; the H3 provider point's contribution schema in the existing extension registry; `docs/design.md`. Publish the contract every built-in and pack contribution uses (see [Extension contract](#extension-contract)). Every table row and contribution carries a footprint; admission computes compatibility from footprints, and a named pair conflict remains only for an observed model-level failure with its evidence. Built-ins and a separately authored fixture enter through one deterministic, immutable per-job snapshot; provider-owned action references are metadata. | Schema fixtures for each socket, including one contribution filling two; footprints named by ComfyUI's patch surface; refusals for two exclusive writers, a refused feature, a missing requirement, a failed `admit()` and excess cost; the fixture appears with its provenance and used requirements in the snapshot. Estimate 2–3 days. | [ ] |
| CC-13b Socket assembly in `compile_job` | S | CC-13a, CC-1.3, CC-15 | `shared/compile.py`, `shared/generation.py`, `shared/timing.py`, `shared/stages.py`, `astrid/core/generation/cli.py`: wire the guider, loop, sampler-wrap, model-anchor and post-join conditioning slots into `compile_job`; encode N branches; check a loop's declared length and arrangement; convert clock-typed parameters through the time map; route mask claims to H3's sole `noise_mask` writer; `describe --intent`; the dry run's verified, untested and cost labels read from test-kit receipts. | A fixture per socket compiles into asserted graph inputs; a two-branch job compiles; a wrong declared loop length and an undeclared mask write are refused; a clock-typed fixture parameter lands at the converted frame; `describe --intent` groups a built-in and a fixture by intent. Estimate 2–3 days. | [ ] |
| CC-14 The pack test kit | S | CC-13a | A CPU test kit packs run against their contributions: build each on a tiny real `MiniMaxH3Model`, run one step, and record object patches, keyed wrappers (including runtime `SAMPLER_SAMPLE` and `PREPARE_SAMPLING`), `patches_replace`, weight patches, denoise-mask functions, forward hooks, model-call counts, conditioning keys, and module- or class-attribute changes in `comfy.ldm.minimax`, latent `noise_mask` writes, registered HTTP routes and environment or user-folder reads. It runs in one marked `engine_deps` CPU lane with pinned ComfyUI and torch; that command is the programme's reusable proof workflow for every unit and pack. Compare with the declared footprint. | A fixture pack whose declaration matches passes; one that hides a wrapper, one that patches `MiniMaxH3Model` at class level, one that writes outside managed scratch, a `noise_mask` writer and an environment-read fixture are each refused with the exact finding. Passing runs write receipts that mark combinations `verified compiles`. Estimate 2–3 days. | [ ] |
| CC-15 First-frame branch encoder | X | CC-1.2 | `shared/generation.py`: a first-frame branch encoder through `MiniMaxH3ImageToVideo`, beside the existing Omni `MiniMaxH3ReferenceToVideo`; capability rows; no captured bundle. | A one-branch first-frame request compiles with the asserted graph inputs; existing Omni requests are byte-unchanged; the encoder appears in `describe`. Estimate about 1 day. | [ ] |
| R Closing review: combined into the H3 programme's integrated review, [Plan 67 R](../67-h3-community-steering/tasks.md) (28 Nov 2026) | S | — | — | Plan 67 R checks this plan's completion list on the joined head of Plans 66, 68, 70 and 67. RS1 remains this plan's own review stop. | [ ] |

## Extension contract

Owner direction, 28 November 2026, after three independent reviews against NKD, Kent's H3 Experiments, Matlow's Dials and MAINodes de-rope. The design and its alternatives are in [#2065](https://github.com/banodoco/astrid-dev/issues/2065) and the H3 guidance redesign document.

- **Sockets.** Contributions plug into typed sockets named by ComfyUI wire types. One contribution may fill several.

  | Socket | Signature | Rule |
  | --- | --- | --- |
  | actions | graph → media, curve or data asset; before the job, or `after:` a pass | Stack |
  | conditioning | CONDITIONING → CONDITIONING, per branch or after the branch join | Stack |
  | model | MODEL → MODEL at a published anchor | Ordered chain |
  | guider | (MODEL, CONDITIONING[]) → GUIDER | One per pass |
  | sampler wrap | SAMPLER → SAMPLER | Stack |
  | loop | (GUIDER, SAMPLER, LATENT, SIGMAS, NOISE) → LATENT, with a declared time map and length | One per pass |
  | media | IMAGE, AUDIO or LATENT → same type, at a pass's `init` or after decoding; declares whether it emits or inverts a time map, and whether it is exact or soft | Stack; executed by [Plan 107](../107-h3-passes/plan.md) |

  **Data points** hold content packs, such as dial libraries and presets, with pinned-asset and licence fields shown at consent.
- **H3 keeps:** branch encoding, arrangement (unless a loop declares its own), guide-position and phase-schedule assembly unless a contribution declares that write, the only write of `noise_mask`, composition and verification.
- **The job record** carries `passes[]` (one executed here; Plan 107 runs more) and `branches[]` (each with `encoder`, optional `region` and `transform`), plus `guider`, `sampler`, `model[]` and rows. Kinds are namespaced `<pack>.<key>` with schema-validated `params`.
- **A contribution** is one YAML file: its socket or sockets, nodes and pinned repository, port mapping, a parameters schema with clock-typed fields, a footprint, an optional pure `admit(job_facts)`, and intent metadata (intent line, "choose when", "gives up", recipe).
    - **Clocks:** clip time, frame range, mask over time (`frames` or `latent`), audio time, denoising progress, block depth, reference-media time and out-of-canvas position, each with a policy for kept or unsampled spans. H3 converts them through its time map.
    - **Footprint:** writes named by ComfyUI's patch surface (`wrapper:<TYPE>/<key>`, `object_patch:<path>`, `patch_replace:<key>`, `weights:<key>`, `denoise_mask_fn`, `forward_hook:<module>`), each `exclusive`, `additive`, `chain` or single instance. It also declares requirements and refusals (features and other contributions), per-branch or global scope, cost (evaluations per step, possibly step-dependent), runtime-installed hooks, self-clocking, and node classes provided.
- **Refused outright:** module- or class-level patches, writes outside managed scratch, contributions whose behaviour depends on an HTTP route (routes a pack registers at import are recorded and must be unreachable on workers), and behaviour read from environment variables or user folders instead of a pinned data point.
- **How units land:** each execution unit may land as several ordinary PRs, with no review gate between them. CC-14's `engine_deps` lane is the one reusable proof workflow every unit and pack uses.
- **Two label sets:** a kind's status (`compiles`, `live-tested`, `unavailable`) is unchanged; `verified` and `untested` label *combinations* from test-kit receipts.
- **Compatibility** is computed from footprints and `admit()`, and is checked by CC-14's measurements. A combination is `verified` only from receipts; otherwise it is `untested`, allowed and labelled.

## Execution units

Units of at most three human engineering days, including focused proof, replace the earlier 21-packet queue. Card details below remain the acceptance record. Estimates are planning figures, not measurements.

| Unit | Cards | Days | Depends on | Route |
| --- | --- | ---: | --- | --- |
| 66-U1 Measured, clock-resolved, persisted job | CC-1.1, CC-9 | 2–3 | baseline | S |
| 66-RS1a Job-record review | RS1 (first half) | 0.5 | 66-U1 | S |
| 66-U2 One compile orchestration | CC-1.2 | 2–3 | 66-RS1a | S |
| 66-U3 Callers and host injection | CC-1.3 | 1.5–2.5 | 66-U2 | X |
| 66-U4 v1 and route retirement | CC-1.4 | 1.5–2.5 | 66-U3 | S |
| 66-U5 Capability table and describe | CC-2 | 1.5–2.5 | 66-U2 | X |
| 66-U6a Contribution schema, footprints and admission | CC-13a | 2–3 | 66-U5 | S |
| 66-U6b Socket assembly in `compile_job` | CC-13b | 2–3 | 66-U6a, 66-U3, 66-U8 | S |
| 66-U7 Pack test kit and proof lane | CC-14 | 2–3 | 66-U6a | S |
| 66-U8 First-frame encoder | CC-15 | 1 | 66-U2 | X |
| 66-U9 One view and receipt | CC-3 | 1–2 | 66-U3, 66-U5 | N |
| 66-U10 Composition by occurrence, sole mask writer | CC-10 | 2–3 | 66-U2 | S |
| 66-U11 Templates and base recipes | CC-5 | 1.5–2.5 | 66-U3, 66-U5 | X |
| 66-RS1b Contract review | RS1 (second half) | 0.5–1 | 66-U4, 66-U6a | S |
| 66-U12 Skill | CC-6 | 1–1.5 | 66-U4, 66-U11 | N |

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
- `conditioning`: reference rows, and guides from Plan 68 CC-4;
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
| Guides | Reserved seam: guides enter through one function that takes ordered guides and returns conditioning. [Plan 68](../68-h3-guides-and-stills/tasks.md) CC-4 implements it; [Plan 67](../67-h3-community-steering/tasks.md) wraps it. Until then `role: guide` is an `unavailable` table row. |
| Generated suffix after a placed prefix | Chosen from the features present: one unchanged video prefix at frame 0 and uncovered time after it. In this plan it calls the captured bundle; [Plan 70](../70-h3-continuation-bridges-inserts/tasks.md) CC-7a swaps in the ported stage. From CC-1.2 the `continuation` flag is accepted but selects nothing; Plan 70 CC-7d removes it from the schema. No recipe or skill text uses it. |

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

## Reservations for Plans 67, 68 and 70

So that later plans add rows and functions without reshaping this one:

1. **`unavailable` rows** in the capability table for `role: guide`, a placed still off frame 0, two placed clips with a gap (bridge) and a placed clip at a later offset (insert). Each later plan flips its row and adds a lowering.
2. **One function reads how placed items are arranged.** In this plan it knows two arrangements, a source covering the canvas and a prefix through the captured bundle, and refuses the rest from the table.
3. **A slot in the dry-run view for the delivered-to-sampled frame map.** Here it is the identity plus the tail trim. Plan 70 fills it for continuations.
4. **The guide seam:** guides enter through one function that takes ordered guides and returns conditioning (see the lowering table above).
5. **The extension contract** is now its own cards: CC-13a (schema, footprints, admission), CC-13b (socket assembly), CC-14 (test kit) and CC-15 (first-frame encoder). See [Extension contract](#extension-contract).

## Design file

Ship the one-page design in [plan.md](plan.md#outcome-and-scope) as `astrid/packs/h3_av/docs/design.md` in this plan. It's the contract: Plans 67, 68 and 70 cite that file and amend it in the same change as their code. A closed plan is history, so the contract lives in the pack.

## Skill guards

Several plans add lines to one skill page, so three tests keep it from drifting:

1. **Skills contain no request text.** Every example is a recipe file named in the skill and loaded by `test_skill_examples_admitted.py`. A test fails if the skill names a recipe that doesn't exist.
2. **The kinds list is checked against `describe`.** A test fails if a kind whose status isn't `unavailable` is missing from the page, or if the page names a field the schema doesn't have.
3. **A length cap and a standing cold read.** The page has a line limit. Each plan re-runs the same small-model asks plus one for its new capability.

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

## Functional additions

These come from the functional review ([research/functional-review.md](research/functional-review.md)), and each is linked from its card.

### Functional additions masks

**One AV mask pair (CC-1.2, Plan 64 SR-5).** Select one paired-latent initializer. Resolve every raw cell to *uncovered*, *kept*, *released* or *padding*, and state the padding policy per stream. Initialize uncovered cells to generate, exact cells to keep and released cells to their effective weight. Pre-splice fixed PCM into `source_audio` before the VAE encode, so the model hears the supplied audio. Emit the R-frame scalar audio MASK from the measured sample overlap per frame, and show the actual linear-resampled 40 Hz ticks in the dry run. Preserve a context node's complete masks and its 8-tick feather, unless a supported replacement derives both in local coordinates. Assert the actual values at a gap, a grant starting between frames, fixed PCM, padding and both feather edges. Reject unsupported combinations before build. If generation influence for a grant starting between frames must be refused or snapped, say so separately from exact sample ownership. Give the audio mask a producer: name the CPU artifact format, the managed binding, the loader and the conversion to an R-sample MASK, and verify the decoded values and frame count through the same binding used for submission.

### Functional additions two masks

**Permission and strength are two masks (CC-1.2, Plan 65 DS-3).** Rasterize each occurrence's binary permission once. Union the active permissions for paste-back. Separately, derive a time×space sampler mask from the maximum active strength times support, with outside = 0 and inside = 1. Define what a zero-strength grant keeps. Fail, naming the grant, when a nonempty grant's effective token footprint vanishes (a tiny mouth can vanish when reduced to the model's grid). Refuse conflicting seeds or reference sets between simultaneous grants. Test overlapping 0.25 and 0.75 grants at different times, a tiny mouth between sample centres, a moving red-channel mask, and exact source and candidate pixels on both sides of the permission edge. State the mask weight precision: an 8-bit intermediate can't hold arbitrary values. Report the precision that applies rather than promising continuous control.

### Functional additions occurrences

**Occurrences (CC-1.1, Plan 65 DS-2).**
- Keep the authored intent and the original asset bytes unchanged.
- Measure each original track once per digest: start PTS, exclusive end, frame or sample count, and channel layout.
- Give each occurrence a binding to its selected track and range, conform transform, prepared bytes, prepared-local offset and destination span.
- Verify the resolved job and its bindings against their own digest on reload, and report exactness against the named prepared RGB/PCM baseline.
- Test two trims of one asset plus a voice reference to the original's tail, across a remote rebuild and composition.
- Refuse missing soundtrack coverage. Explicitly downmix, or reject, unsupported channel layouts; a center-channel-only 5.1 reference tells a deliberate downmix from dropped channels.
- Check conflicts after stream resolution: subtract authorized grants, work out the effective owners per stream and the expanded model holds, then check intersections. Admit disjoint picture and PCM owners that start at the same time. Test partly overlapping clips, and conflicting stills in one latent chunk, separately from exact delivery conflicts.

### Functional additions exact

**Exact delivery (CC-10, Plan 64 SR-5).**
- Name the canonical rate, channel layout, sample representation and RGB conversion.
- Use integer absolute destination boundaries and source offsets.
- Conform only generated audio to the required sample count.
- Restore each owner's untouched PCM and RGB after every lossy stage. Deliver a lossless stream wherever exactness is promised, then decode the final published file.
- For every kept or supplied span and all protected pixels, compare the count and the bytes per channel.
- Test asymmetric stereo impulses, off-by-one samples, both signs of 40 Hz rounding (a 5-frame run gives 9,600 samples where the output needs 10,000), and a generated-only clock case.
- A permitted one-sample duration tolerance is a different claim from exact sample identity.
- Today's verifier tolerates about 2% sample-count difference and a 0.985 similarity, so it can't establish this.
- Update the verifier with the raster handoff: verify composition and post-mux evidence against the prepared binary mask and each occurrence's own prepared offset.

### Functional additions clocks

**Clocks (CC-9, CC-7, CC-8).** Map delivered spans into sampled segments explicitly. In a 120 + 24 continuation, delivered frame 143 is raw frame 62, because raw 0 is delivered 81; a guide at delivered 80 is outside the sampled segment and is refused, cropped or kept as stated. Infer the shot duration from measured placements, or require `duration` for circular expressions. Record the local frame and tick, and rebase guides. Derive stored and selected take spans from ownership: the default drop on 120 + 24 selects `[120,144)` from the stored `[0,144)`, and keep selects the whole file. Bridges and inserts don't inherit prefix drop. The Plan 59 take reader currently identifies continuation from the flag CC-7d deletes; move it to ownership in CC-7d.

Segment mapping for continuations (delivered span to sampled segment, guides inside a continuation) is [Plan 70](../70-h3-continuation-bridges-inserts/tasks.md)'s; this plan reserves the slot and resolves end-relative time.

### Functional additions resources

**Resources (CC-3, Plan 64 SR-2, Plan 65 DS-4).** For each selected occurrence, report:
- the requested trim, bound file and tracks;
- a conservative, labelled retained-picture-frame estimate from metadata in the dry run; the settled result and receipt report a count labelled `derived (pinned node rule)` from the measured prepared-media frame count and the pinned node cap and rounding rule, never as an observed H3 count. If a path is not conformed, identify it and use the probe; report audio duration separately (a 48-frame reference can bind 39 visual frames and its whole soundtrack);
- slot, tag and effective size.

Bind standalone audio ports as AUDIO. Estimate raw RGB bytes and target, reference and guide rows without decoding, and bound source loads to the windows needed before resizing. Admission refuses a metadata bound clearly over the 15-second clip or modality limit and warns near a boundary; it does not require a provenance-controlled or otherwise restricted video subset. At 16384×16384 a 141-frame job is about 423 GB of raw frames: that is a tensor-size calculation, not a memory measurement. Separate schema-valid, resource-qualified and observed. Apply the node's length limit (3592 is the largest 5 + 17k value within its 3600 maximum) to the actual bound input.

### Functional additions refusals

**Refusals and discovery (CC-2, CC-3, CC-7d).** Choose and publish the reserved control and adapter-phase paths. Structural validation recognizes them, and capability admission rejects them, naming the item, the `unavailable` row and the remedy. Three requests are refused before claim, with no build:
- a LoRA with `phase` (late LoRA);
- a mouth edit inside a continuation prefix, with the two-job recipe as the remedy;
- `role: control`.

Exercise each through CLI file, template and SDK. `describe_entry` projects the same pack table admission uses; after capture removal, resolve the catalog entry from a fresh install. Compare the local dry run, a managed submission and a scratch-free fresh readback. An outputs-only fallback doesn't count as a match. Add a sealed fixture from before SR-1: verify its stored bytes using their recorded format and return the settled result; give the rebuild refusal only on active resume.

### Functional additions bindings

**Bindings and dependencies (Plan 64 SR-3, CC-1.2).** Each lowering declares the mechanisms it feeds, the artifacts it needs and its interactions; `compile_job` resolves and checks them once. Report which occurrence and soundtrack each tag actually identifies. Finding the requested number in the prompt doesn't catch a wrong-but-valid binding, for example after a video soundtrack takes an audio number. Refuse per-grant seeds or reference sets that differ inside one pass.

### Functional additions templates

**Templates and review (CC-5, CC-6, R).** `--write` emits only the filled request and doesn't submit; specify how the asset map is replayed. Using installed skills and a reused shot: select an occurrence, fill the shot and CLI holes, correct a missing hole, dry-run, then reopen the written request through normal admission. The cold-read rubric includes the expected refusal and the two-job decomposition. Keep Recast's transcript, mask, take-range and owner checks, with no automatic take mutation.
