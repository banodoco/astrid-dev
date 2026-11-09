# Inputs — Pack extension points

[Plan](plan.md) · [Tasks](tasks.md)

## Starting code

Repository ownership, starting branch and SHA, retained dirty work, and candidate branch are **TBD at execution start**. Identify and freeze the owning repository or repositories and current refs before source changes. Historical plan text does not establish a live execution base. Verify the intended `pre-main` destination then; do not assume branches.

| Input | Why it matters | Identity / limits |
|---|---|---|
| Current VibeComfy implementation | Reveals existing workflow primitives and extension contracts to reuse (`vibecomfy.plugins`). | Reviewed at VibeComfy `e65f4941` (8 Nov 2026); re-freeze at setup. |
| Extension protocol | The registry, scopes and sidecar walker this plan switches on (`astrid/core/extensions`, commit `864179976`). | Reviewed at astrid-agent `5eac07e3f` (8 Nov 2026); Plan 32 T2 allows `side: agent`. Re-freeze at setup. |
| h3_av | The first `vibecomfy.workflows` contribution, made in Plan 32 T6b. | Reviewed at astrid-agent `5eac07e3f`, `astrid/packs/h3_av` (8 Nov 2026). |
| Sound-effects template | The base of P4's sound-on-video pack (`ready_templates/audio/hunyuan_video_foley.py`, audio output only). | Reviewed at VibeComfy `e65f4941` (8 Nov 2026). |
| h3_av and Agent generation, for the family design | The first-principles split below. | Read at astrid-agent `origin/cand/29-r12` `ff40f2c68` (9 Nov 2026), which predates Plan 32 T6b. |
| VibeComfy, for the family design | `PluginAPI`, entries, router, `InputSpec`, ready templates. | Read at VibeComfy `e65f494` (9 Nov 2026) from a shallow, blobless clone, deleted afterwards. |
| Base | Phase 1: VibeComfy's pin after Plan 32 T6b-2. Phase 2: Plan 32's landed Agent head after T6b (T6d for A4), and poms_packs `main` after Plan 06. | Pending — record the SHAs before V1 and P1. |

## References and evidence

- [Liquid Software vision](../../vision/pillars/liquid-software.md) sets the design direction.
- `merge-run/path-review/PACK-EXTENSION-PROTOCOL.md` and `H3-GENERALIZATION.md` on the merge-run desk (`banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`): the protocol review and the choice of the second pack.
- **Review rounds:** recommend at most 3 (raised from 2 on 9 Nov). The plan now changes a public VibeComfy contract (families, the router), Astrid's default resolution and the install transaction (a trust boundary). Pending owner agreement.
- This plan is CPU only; the real-GPU runs (IMG, S2, h3) belong to [Plan 34](../34-real-gpu-proof/plan.md).

## Owner direction (9 Nov, later)

**Source:** the owner, speaking on 9 Nov 2026. The orchestrating session (`session_011EzfVzreGCJJQnTuXpbib9`) paraphrased her words to the planner; this is not a verbatim quote. The framing is recorded in [plan.md](plan.md#direction-owner-9-nov-2026-later-one-route-over-a-family-of-workflows). She asked for thinking and a plan update only, with no build. **Scope decision:** Pending — the design below is the planner's proposal, not her approval. Next: put the open decisions to her.

## What the h3_av machinery is

Read at Agent `ff40f2c68` and VibeComfy `e65f494`. Class: **G** is general and moves out of h3; **H** is h3's and stays with it; **D** is plumbing that Plan 32 T6b deletes.

| Layer | Piece | Where | Class | Goes to |
|---|---|---|---|---|
| Agent contract | One tool over several workflows: `h3_av.transform` with `generation_entry {id, kind, modes, inputs}` | `h3_av/pack.yaml:487-586` (579); projected by `core/generation/entries.py:98-136` | G (shape) | VibeComfy family entry (V1) |
| | Producer-only ports (`asset_map`, `execution_request`, `worker_qualification`, `prepared_worker`, `cleanup_receipt`, `resume`) and `ASTRID_H3_*` passthrough | `pack.yaml:505-532`, `562-576` | D | deleted (Plan 32 T6b) |
| | Agent guidance: purpose, do-not-use, entrypoints | `pack.yaml:44-55`; `docs/SKILL.md:18-29` | G (idea), H (text) | variant `summary` and describe; the SKILL stays h3's |
| | Request schema and normalisation | `schemas/request.v{1,2}.json`; `shared/request_v2.py:192,248,293` | G (mechanism), H (contents) | `request` field (V1); h3 keeps the schemas |
| | Refusal `{code, field, fix}` | `shared/request.py:18-26` | G | `RequestError` (V5) |
| | Intent to variant | `branch_for`, `shared/request_v2.py:432-439`; dispatch `actions/compile/compile.py:1039-1053`, `865-916` (Character Swap 874, `audio_only` refused 908-913) | G (mechanism), H (rules) | `select` and `route` (V5); h3 keeps the rules (H1) |
| | Parallel routers | Astrid `sdk/generation.py:388-398` (`_infer_image_mode`), `402-404`, `451-466` (`_infer_video_mode`); VibeComfy `router/_rules.py:28-42,53-70`, `router/_core.py:25-34,74-94`, `extras.py:43-46` (`register_route`) | G, duplicated three ways | one router (V5, A4) |
| | Describe, per mode | `describe_entry`, `entries.py:406-475` (`mode_descriptions`); h3 special case at 447 | G; 447 is H in core | projects VibeComfy's describe (A4); 447 deleted (A3) |
| | Plan and explain | `plan_request`, `shared/planner.py:80-198` (envelope 183-196); `_timing` 26-52, `_ignored_fields` 55-77 | G (envelope), H (contents) | `plan_envelope` (V5); h3 `details` (H1) |
| | Family CLI `astrid h3` (plan, run, compose, edit) | `cli.py:12-31` | H, duplicating generic verbs | deleted (A3) |
| | Mode vocabulary | VibeComfy `entries.py:57` (closed per kind) | G | `variants[].mode`; `variants[].id` is open |
| Assembly | The three trios | `compile.py:24-26` | H | h3 |
| | Frozen bundle, managed-assets archive keyed by binding, compilation digest | `_compile_manifest`, `compile.py:272-326` | G | V2 staging and the Plan 32 T6 archive |
| | Input name to file | `_asset_bindings`, `compile.py:124-158` | G (pattern) | `file` and `file_map` inputs (V1) |
| | `producer_local` custody; input bundle | `entries.py:112,131`; `shared/input_bundle.py` | D | replaced by V2 staging |
| | 5+17k grid, 362→360 trim | `shared/timing.py:49,92`; `shared/generation.py:190` | H | h3 |
| | Multi-pass segments | `planner.py:101-132` | G (idea) | deferred |
| | Rectangle regions to masks | `actions/prepare/static_regions.py`; `planner.py:142-157` | H for now | h3 |
| Post-processing | Probe, video and audio coverage, mux, splice, sample digest | `shared/compose.py:39,120,152,1010,360,1159` | G | `vibecomfy.media` (V3) |
| | Preservation outside a mask | `compose.py:518,563-712` | G | `preserved_outside_mask` (V3), used by the image family |
| | `compose_candidate` orchestration | `compose.py:1236`, `168` | H | h3 `after_outputs` |
| Verification | Strict probe, whole-coverage, sample evidence | `actions/verify/verify.py:36,100,116` | G | V3 |
| | Provenance and `verify_candidate` | `verify.py:219,263` | H | h3 `after_outputs` evidence |
| | Four separate facts: succeeded, verified, approved, cleaned up | `docs/SKILL.md:271-274` | G (idea) | `evidence` gives "verified"; the rest are Astrid's task and lease |
| Packaging and trust | Permissions | `pack.yaml:10-24` | G | thin pack (Plan 06) |
| | Pinned LoRA and model URLs in bundles | `README.md:21-31` | H (contents) | VibeComfy `ModelAsset` already carries pins |
| | Plugin pin `{dist, version, sha256}` | new | G | A1, A2 |

**Negative findings:**
- VibeComfy at `e65f494` has no inpaint or outpaint ready template. `image/` has text-to-image templates and `z_image_img2img`; `edit/` has Flux 2 and Qwen edit graphs.
- VibeComfy's router predicates are lambdas, and `list_routes` returns only kind, verb and template, so an agent cannot read why a route is chosen.
- The extension `point.json` at `ff40f2c68` still has `side: const client`; Plan 32 T2 allows `agent`.

## Two families tested against the design

| | Image (txt2img, img2img, inpaint, outpaint) | Sound on video | Lip-sync (considered) |
|---|---|---|---|
| Author writes | Two new templates (inpaint, outpaint), one entry with four variants and `when` tests, an optional 10-line `after_outputs` for preservation | One entry with no variants, a 10-line `after_outputs` calling `media.mux` | Audio-driven: one template and a mux. Text-driven: TTS then lip-sync |
| Gets for free | Discovery, describe, routing with reasons, refusals, dry-run plan, staging of image and mask files, every placement, default slots, pinned install | The same, without routing | The same |
| Plan 17 before this change | `build` could hide the choice; one `bundle` per entry; describe showed modes but not how one is chosen | Fully covered | Audio-driven covered |
| Falls short without this change | No `variants` or `when`; an agent cannot see or override the choice; Astrid's `_infer_image_mode` would still decide first; no preservation helper | Nothing, but it does not test routing, which is why IMG is added | Text-driven needs workflows chained in sequence: out of scope, recorded as an extension need |

## Alternatives

1. **Keep the choice inside `build`** (Plan 17 as it stood). This adds no contract, but the agent cannot see variants and three routers remain. Rejected.
2. **One entry per variant** (`image-inpaint`, ...), with the agent picking. This is what happens today. It is not a single route, and the agent has to know the rules. Rejected; the variants still map to modes, so default slots keep working.
3. **A code `route` only.** Expressive, but an agent cannot read it. Kept only as an escape hatch that must return a reason.
4. **Routing by a language model** over the prompt. Not deterministic. Deferred.
5. **A new plan.** Rejected: it is the same contract, the same repositories and the same sequence as this one.
6. **The family layer in Astrid only.** Rejected by the owner's VibeComfy-first direction of 9 Nov.

**Challenge:** Pending — this changes a cross-repository contract and default resolution, so it warrants an advisor critique (planning skill). Next: brief the advisor to verify V1, V5 and A4 against the code and to build as little as possible, then record what was accepted.

## Open owner decisions

1. **Router burn-down.** Remove `register_route` from `PluginAPI` and re-express the six built-in rules as built-in families (V5)? *Recommend yes,* after a grep of known plugins; otherwise keep a shim for one VibeComfy release.
2. **`generate` with no entry.** Resolve the kind's default family first, let it route, then apply a per-mode pin (A4)? *Recommend yes:* it deletes Astrid's mode inference. The alternative keeps that inference and uses families only with `--entry`.
3. **How expressive routing is.** Declarative `when` (`present`, `absent`, `equals`) plus an optional `route` hook? *Recommend both:* h3 needs the hook. Declarative-only would force h3 to take a precomputed branch input.
4. **Where the image family lives.** A poms_packs plugin, or built into VibeComfy? *Recommend poms_packs:* it proves third-party authoring, and V5's built-in families already cover t2i and i2i.
5. **Verification.** One `after_outputs` returning evidence, or a separate `verify` hook? *Recommend one hook.*
6. **Licence and home for h3** (carried over). *Advisor recommends* Apache-2.0 in a new repo. The H3 weights and Character Swap LoRA licences are still unrecorded.
7. **How Astrid installs a wheel** (carried over): the shared venv, or a site directory per pack? *Recommend a site directory per pack,* so removing the pack removes the wheel.
8. **Who reviews VibeComfy changes** (carried over). Pending.
9. **Wan2GP** (Plan 12) gets no `build`, `after_outputs` or variants, since these live in VibeComfy (carried over). *Recommend accepting this* for now.

## Constraints

Follow repository [Astrid development skill](../../skills/astrid-dev/SKILL.md) and the shared [run contract](../../skills/astrid-dev-shared/run-contract.md) for execution, resources, routes, and publication. Confirm source identities and destination at setup.
