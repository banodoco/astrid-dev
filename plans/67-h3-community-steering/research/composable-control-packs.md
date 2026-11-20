# Exploration: composable H3 control substrate and optional packs

> **Design exploration, 20 November 2026 — not an approved change of scope or a product implementation.** This note records the owner's question about using Plan 67 as a test case for independently installed sub-packs, and potentially splitting Plan 66/68/70 capabilities into composable units. It does not supersede their accepted task cards. An independent architecture critique and owner scope decision are required before changing product contracts.

[Plan 67](../plan.md) · [Plan 66](../../66-h3-composable-core/plan.md) · [Plan 68](../../68-h3-guides-and-stills/plan.md) · [Plan 70](../../70-h3-continuation-bridges-inserts/plan.md) · [Plan 17](../../17-vibecomfy-extensibility/plan.md) · [Pack lifecycle, Plan 06](../../06-packs/plan.md)

## What the proposal actually means

Instead of making H3_AV one ever-growing collection of special cases, let a creator or agent describe **what they want** in one timeline/control grammar, while small optional packages provide ways to translate those intentions into model-specific ComfyUI nodes. A recast toolkit can combine the H3 engine, NKD curves, ControlNet, masks and a voice pack without copying their code.

This has **four different kinds of composition** that must not be confused:

1. **Control composition within a generation job:** exact placements and edit grants, timed/untimed soft context, model/sampler controls. This is Plan 66's six mechanisms, not a second workflow engine.
2. **Extension composition:** independent packages register validated lever kinds, source preprocessors or lowerings with a host's extension point.
3. **Package dependency composition:** a package requires a compatible host pack, plug-in API version, ComfyUI node classes and pinned model assets. Dependency presence alone does not define an execution chain.
4. **Creative workflow composition:** a recipe or explicit multi-job pipeline connects outputs to inputs (e.g., voice -> video -> lip sync, or upscale after H3). This belongs *above* the one-job compiler, not disguised as a lever kind.

A “sub-pack” is therefore a **normal, versioned, independently installed pack whose contribution appears under another pack in discovery/UI**, not a physically nested child directory with a separate installation mechanism. An aggregate/collection pack may depend on several packs while contributing its own recipes and skills.

## Proposed architecture and ownership

| Layer | Responsibility | Candidate home | Not its job |
| --- | --- | --- | --- |
| Astrid pack host | Discover packages and contributions, verify declared dependencies/versions, trust/permissions, pin and install/rollback, availability | Existing `astrid/core/pack` + `astrid/core/extensions` (Plans 06, 17, 47) | Interpret H3 frames or rewrite graphs |
| General VibeComfy workflow family | One entry with variants, describe, deterministic dry-run, build, after-outputs/media helpers; model/node inventory | **VibeComfy**, per the owner direction in Plan 17 | Become an H3-specific request engine |
| H3 base pack / compiler plug-in | One H3 job contract; resolved timeline, frame/sample mapping, ownership and exact composition, capability admission, six lowering mechanisms, graph family; H3 compatibility and refusals | H3 plug-in proposed by Plan 17; thin Astrid `h3_av` pack installs and pins it | Hard-code every optional creative technique |
| H3 capability providers | Additional named kinds, preprocessing tools and lowerings that use supported H3 mechanisms: NKD, Fun ControlNet, possible motion/context adapters | Independently installed add-on packs contributing to an **H3-owned typed extension point** | Modify H3 internal state or silently create job routes |
| Creative compositions | Recast, speech-on-still, cinematic toolkit, task skills and recipes; separate explicit multi-pass workflows | Ordinary packs / recipes, potentially depending on multiple providers | Become a competing compiler |

**Do not create a universal “frame-by-frame ComfyUI core” now.** The **authoring concepts** (frame/time, ownership, guide, reference, phase, source mapping and exact/soft guarantees) are broadly reusable. The *actual H3 lowering* is not: H3 has specific latent timing, joint audio/video conditioning, context nodes, reference slots, control hooks, frame lattices and trim rules. Extract proven generic media/receipt helpers into VibeComfy per Plan 17; generalize the control interface beyond H3 only after a second, materially different model family demonstrates it.

“Plug into the base Comfy workflow” is a convenient mental model, but the implementation likely needs **a family of emitted graphs**, not one immutable graph plus optional branches. A continuation, bridge, insert, source-free generation and masked edit need distinct preparation/assembly. Plan 70 explicitly compares potential shared preparation before choosing lowerings; preserve that evidence-based decision.

## Control contract: time, guarantees and lowering

A request has a stable **authoring timeline**. At minimum it distinguishes:

- **Clip/output time:** frames, audio ticks and spans (`at`, `during`, `range`). A delivered frame identifier is not necessarily a sampler frame; the resolved job records the mapping. The delivery clock and sample clock must be separate.
- **Sampling/denoising time:** `phase: [start, end]` in normalized denoising progress; not a clip-time interval. A node's unrelated “phase” parameter may need a different public name, as Plan 67 already does for NKD Event Curve's offset.
- **Ownership:** placed media and explicitly kept spans are the *exact-output* side, enforced by post-generation composition and verification. Context (guides/references/prompts) and Process (LoRA/ControlNet/sampler settings) only *influence* the model and cannot guarantee precise motion, speech or imagery at every frame.
- **Declared capability and actual support:** a grammar that can express a control does **not** prove H3/node compatibility. Each kind carries schema, defaults, bounds, conflict rules, required node classes/assets and source revision, plus a status `unavailable`, `compiles` or `live-tested` with dated render evidence.
- **Combination:** a pure deterministic planner validates all controls, assigns them to the existing six mechanisms, checks ordering, overlap, incompatible masks/ownership, scarce reference slots, and whether sampled frames can represent requested guides. It refuses impossible combinations *before* renting/claiming GPUs. No last-loaded-wins mutation of arbitrary ComfyUI graphs.

The H3 examples make the frame distinction essential: delivered output runs at 24 fps, H3 native lengths follow a 5 + 17k frame grid, Plan 70's continuation context uses 39 + 51k, and interior insert offsets are restricted to multiples of 51 for safe joint audio/video alignment. “I can author a control for frame 34” does not mean “the H3 sampler can satisfy exact frame 34.” The dry run must name a refusal, legitimate hold span or explicit crop/mapping rather than silently snapping.

### Sketch: extension point, not finalized manifest syntax

```yaml
# Illustrative only. Not currently supported in pack.yaml.
id: h3_nkd_steering
version: 0.1.0
requires:
  packs:
    h3_av: ">=0.2,<0.3"
  points:
    h3_av.levers: "^1"
  comfy_nodes:
    nkd_basic_tools:
      revision: c157722a2b484d80dee6b6d3f166c90d9ec197b8
contributions:
  - point: h3_av.levers
    kinds: [nkd_phased_guide]
  - point: h3_av.tools
    tools: [event_curve_audio]
```

Whether `h3_av.levers` is a new H3-specific point directly, or a **typed point schema hosted by VibeComfy** for every compatible workflow family, needs a source-level Plan 17 decision. Reuse `astrid/core/extensions` for discovery and validation; don't create another generic registry. The H3 plug-in must own the semantic interpretation of H3 lever kinds and enforce its point protocol.

### Distribution/installation is not workflow execution

The current `h3_av/pack.yaml` already has `dependencies.packs: [vibecomfy]`. The existing `astrid/pack_validation.py` reads pack dependencies as a **list of IDs**, checks presence, cycles and applicable pins, but does not resolve version-range constraints between pack IDs. The current transaction framework admits dependency groups but does not automatically download undeclared packages. The hypothetical `requires` and version examples above are a **future contract**, not something that works today.

A collection pack should produce a visible dependency graph, compatible version solution, explicit user consent and one locked selection of exact pack commits/digests. It must not silently replace an installed dependency that another pack needs. Independent sources and versions need a trusted resolver and compatible transaction plan; do not mistake today's same-source group operation for a full package solver. Missing or conflicting requirements should leave the previous environment intact and report a targeted fix.

Remote execution is also part of package correctness: the actual job graph's reachable node classes and model assets determine worker requirements; only those extras are shipped, pinned and attested. Installing NKD to use an NKD curve should not make every ordinary H3 job depend on NKD. The graph/capability/worker inventory and exact pin receipts must agree.

## Which existing H3 features should really become separate packs?

**Recommended split (provisional):**

| Feature | Likely home now | Reason |
| --- | --- | --- |
| General request grammar, timing/mappings, capability table, compiler mechanisms, output ownership/exact composition | **Base H3 compiler**, reusable media mechanics lifted into VibeComfy as Plan 17 allows | Every H3 route needs the same semantics and correctness |
| Timed prompt serialization, reference binding report | Base H3 compiler | Native H3 behavior, cheap, no external node requirement |
| Plan 68 guides and exact stills | **Probably base H3** initially | Fundamental authoring behavior, closely tied to H3 latent frame holds and exact composer; extraction would add coupling without clear independent reuse |
| Plan 70 continuation, bridge, insert | **Probably base H3 provider module** initially; optional external H3 motion pack remains pinned | Deeply coupled to H3 context/audio assembly, preservation and the specific model lattice; split the module internally before independent installation |
| NKD curve-to-audio tool | **Optional `h3_nkd_steering` pack** (or cross-model NKD tool pack if proven) | External GPL-3.0 nodes, optional dependency, reusable output is a plain audio guide |
| NKD phased guides | Optional provider **only if stock ComfyUI guide scheduling is not sufficient** | Plan 67 explicitly tries stock `ConditioningSetTimestepRange` first; don't create a pack for a redundant wrapper |
| H3 Fun ControlNet | Optional `h3_controlnet` provider **only after** compatible pinned weights/Ref2VA support are proven | Different assets/node requirements, compatibility risks, distinct feature lifecycle |
| Character Swap adapter / optional LoRAs | Candidate separate pack *if* they have genuinely independent model dependencies and extension interface | A simple model-chain lowering may remain a built-in kind; versioning its assets does not automatically require a new Astrid pack |
| Recast recipes and composed cinematic toolkits | Ordinary recipe/collection packs | Dependencies + creative orchestration, separate from execution engine |

Avoid turning **every kind** into an installable pack; that is granularity for its own sake. Use a pack when it has independent authoring, dependencies, trust, testing, distribution or lifecycle. A table row/lowering in the base plug-in is usually best for a tightly coupled native H3 feature. “Sub-pack” is a distribution/ownership boundary, **not** the compiler's basic abstraction.

## Alternatives

- **A. Keep all new capabilities inside H3_AV.** Smallest near-term change and fastest delivery, but optional NKD/ControlNet nodes and user-contributed techniques remain tied to H3 releases. Appropriate until extension demand is real.
- **B. Move the entire control compiler into Astrid core now and build every H3 function as a sub-pack.** Attractive superficially, but freezes H3-specific constraints into the wrong layer, duplicates Plan 17's VibeComfy direction and creates high-coupling package boundaries. **Not recommended.**
- **C. Keep H3 semantic compiler as a thin host, expose one typed lever-provider point, extract only a genuinely optional provider, and validate that existing Plan 17/06 machinery can install it.** Best initial experiment. Broaden the contract only after a second different model/host uses it. **Recommended.**
- **D. Keep everything as internal modules until Plan 17 is complete, then extract an optional pack.** Lowest immediate coordination cost, but postpones verification of extensibility. A reasonable staging of C if Plan 17 is blocked.

## Smallest meaningful vertical proof

1. **Existing H3 unchanged:** a plain source-free H3 request and an edit still compile/dry-run without any optional node package.
2. **Install optional provider:** an independently sourced, pinned `h3_nkd_steering` pack contributes an Event Curve tool and, *only if actually needed*, an H3 guide lowering. A normal H3 job still lists no NKD dependency. A job using it lists the exact node classes and pinned source revision.
3. **One shared request:** source still + soft guide + optional curve steer goes through the same `compile_job`, with transparent time mapping and one exact-versus-soft report; no new request grammar, hidden job route or graph copy.
4. **Real composition:** an aggregate pack requiring H3 and the optional provider contributes one creative recipe that dry-runs and compiles. The recipe cannot silently install or update other packs when a project opens.
5. **Negative cases:** incompatible H3/point versions; missing NKD; wrong node revision; unavailable Fun ControlNet weights; duplicate/conflicting lever kinds; control outside sampled frame domain; reference-slot overflow; discontinuous time mapping; dependency cycle; disable/upgrade/rollback with a dependent pack. Each fails with a useful explanation and preserves prior admitted state.
6. **Second provider and second consumer:** validate a materially different control contributor (not just another NKD function) and, eventually, a second workflow family/model to decide which time/lever semantics can truly move into general VibeComfy APIs.

The first proof should be CPU-only in the spirit of Plans 66–70, followed by an independently authorized GPU observation for *adherence/quality*. A passing graph compile is not evidence that motion, words or pose followed the instruction. A cross-repository contract requires independent architecture review before an implementation go.

## Relationship to existing projects and next decisions

- **Plan 66:** Preserve the one compiler, one job shape, six mechanisms, capability table, guard/refusal semantics and exact composition. Explore a *typed registration seam* but do not widen existing tasks without reviewing their execution order and evidence.
- **Plan 68:** Provide the guide lowering that later providers can wrap; keep core exact-still correctness local until there is a reason to extract it.
- **Plan 70:** Preserve its evidence-first comparison of context preparation and its special frame/audio lattices. It is **not** the NKD/ControlNet feature project.
- **Plan 67:** This is the natural optional-provider experiment. Its current tasks build NKD and ControlNet inside `h3_av`; changing to a separately installed provider changes scope, dependency tests and merge ownership. Treat as a **proposed revision**, not as already authorized.
- **Plan 17 (paused):** Owns the generic workflow-family/plug-in contract, H3-to-VibeComfy extraction and Astrid extension-point bridge. Review its scope before inventing `h3_av.levers`.
- **Plans 06 / 47:** Pack lifecycle and demanding install/upgrade/rollback proof. Add semver range solving only as a justified extension of existing dependency validation.
- **Plan 45:** Typed creative component connections are a related but *different* level (binding UI/back-end components), not the H3 in-job control grammar.
- **Plan 71 is already assigned to gap definition and reconciliation**; it must not be repurposed. If the extension/sub-pack outcome is independently useful and too big for Plan 67, create a separately scoped future project (next currently unused number: 74) with a Plan 17 dependency, not a new “71”.

### Questions requiring owner/advisor decision

1. Do we want **independently installable NKD-based H3 steering now**, or internal modularity followed by extraction after Plan 17?
2. Should the provider point be **H3-owned** first, or belong to a general VibeComfy workflow-family control API? The answer must follow a code-level Plan 17 review and avoid generic promises H3 cannot prove.
3. Is the goal *separate distribution* for ControlNet/motion context/keyframes, or *one stable public way to describe controls* with internal providers? We should not confuse the two.
4. Do version-range resolution and multi-source aggregate installation belong in the first experiment or in a separate pack-lifecycle phase?
5. Which accepted Plan 67 task outcomes can remain untouched, and who owns a revised plan and the independent architecture critique?

**Recommendation:** Start with C, use Plan 67 as the real design test, keep Plan 66 and Plan 70 intact until their existing contract is demonstrably ready, and do not turn every frame feature into a different physical pack. Record a follow-up Plan 74 only after reviewing the revised scope and Plan 17's paused state.
