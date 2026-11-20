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

## Where sub-packs live, who owns them and which loader handles them

**Key distinction: an author's source tree, an installed package identity, a pack's dependencies, an extension-point contribution, and how a toolkit presents the result are five different things.** A folder is not a dependency graph; a dependency graph is not a workflow. "Sub-pack" should be a *relationship in packaging and discovery*, not a new untrusted loader or a source-code import shortcut.

### Three concrete actors and a transitive example

- **Original H3 provider:** \`h3_av\` publishes the H3 workflow-family/compiler interface and the extension point (for example \`h3_av.levers\`, version 1). It already depends on \`vibecomfy\`.
- **Independent add-on author:** \`h3_nkd_steering\` has its own pack ID, publisher, version, origin pin, permissions, tests and lifecycle. It declares a *hard dependency* on compatible \`h3_av\`, and a contribution to the H3 lever point. A missing or incompatible base leaves this add-on unavailable; it cannot substitute its own H3 implementation or bypass admission.
- **Another creator's toolkit:** \`cinematic_recast\` (published by someone else) requires both \`h3_av\` and \`h3_nkd_steering\`, contributes its *own* recast recipes/skills, and can show the NKD add-on under its toolkit in discovery. It **does not** own the NKD add-on or overwrite its package identity. A second toolkit may share that exact installed package and version.

The dependency graph is \`cinematic_recast -> h3_nkd_steering -> h3_av -> vibecomfy\`, plus \`cinematic_recast -> h3_av\`. The graph can extend to any finite depth so long as it is acyclic, resolves to compatible single selected IDs, and has no ambiguous version/provenance conflicts. A toolkit's required add-ons must be dependencies; *suggested/optional* add-ons can be advertised separately and must not make the toolkit unusable when absent. Avoid a second authoritative \`includes\` list that silently disagrees with \`requires\`.

\`\`\`yaml
# Illustrative, proposed pack schema — NOT executable in the current Astrid schema.
# Independent add-on, which could be maintained in a separate Git repo.
id: h3_nkd_steering
version: 0.1.0
requires:
  packs:
    h3_av: ">=0.2,<0.3"
  extension_points:
    h3_av.levers: "^1"
contributes:
  - point: h3_av.levers
    id: h3_nkd_steering.phased_guides
    entry: lowering.py:register
\`\`\`

\`\`\`yaml
# Illustrative, proposed toolkit declaration by a different author.
id: cinematic_recast
version: 1.0.0
requires:
  packs:
    h3_av: ">=0.2,<0.3"
    h3_nkd_steering: ">=0.1,<0.2"
recommends:
  packs: [h3_controlnet] # optional, never silently installed
resources:
  - docs/recast/SKILL.md
  - recipes/voice-and-motion.yaml
\`\`\`

These examples deliberately separate *pack version* from *extension-point API version*. A provider could work across many \`h3_av\` releases as long as the typed lever API remains compatible. Existing \`dependencies.packs\` is a simple list of IDs, not these version-range mappings: implementing this requires a compatible schema migration, resolver and tests, not just writing new YAML.

### Source tree layout versus installed layout

**Recommended authoring layout:** multiple independent packs may be published from one repository, as sibling roots. For example:

\`\`\`text
my-creative-tools/                    # source repository, not one installed pack
  packs/
    cinematic_recast/
      pack.yaml                       # id: cinematic_recast
      docs/recast/SKILL.md
    h3_nkd_steering/
      pack.yaml                       # id: h3_nkd_steering
      extensions/h3_av.levers/...
\`\`\`

Each root is selected, validated, pinned and installed *as its own pack*. Astrid already accepts a Git source plus a \`subpath\` when adding a pack and can stage several explicit pack IDs/subpaths from one source revision through its group transaction. That is a useful foundation; it **does not** imply recursive discovery of every nested \`pack.yaml\` or general multi-source dependency solving.

**If an author insists on a child folder inside another pack's source folder**, treat it as a separately selected pack root only through an explicit manifest/source-subpath reference and the same canonical validation, ID and provenance checks. Do **not** import it merely because a folder is named \`subpacks\`, or automatically execute its \`pack.yaml\` when the parent loads. Prefer sibling roots: a child embedded in the parent's checksum and also separately pinned introduces ambiguous upgrades, source ownership and double accounting. A child folder used as ordinary code or assets is *not* an independently installed pack and must not pretend to have a separate lifecycle.

**Installed layout:** the dependency resolver should publish one selected pack per unique ID within the admitted collection (or a single explicitly selected source root for managed sources), each with an independent pinned origin/digest and version. No arbitrary \`<parent>/subpacks/<child>\` runtime root is required. In the current code, the pack loader scans a configured root's immediate pack children or one explicitly selected root with its own \`pack.yaml\`; the extension registry then walks recognized manifest locations *inside each admitted pack*. Keep that model.

**Presentation layout:** a toolkit UI may show \`cinematic_recast / Steering / NKD\`, and the H3 UI may simultaneously show \`H3 / Steering / NKD\`. These are two *views of the same installed package*. Present membership can be derived from explicit declared requirements and provided contributions; it is not a unique physical parent, security owner, mutable package path or a duplicate installation. One add-on can appear under multiple toolkits without having two copies.

### End-to-end loader and activation path

The desired sequence uses existing owners and one new typed seam, rather than two overlapping extension registries:

1. **Install/resolve (Astrid pack host):** locate selected source roots by explicit ID/subpath and approved repository origin; parse manifests as data, calculate transitive required dependencies and version/point constraints, detect cycles and collisions, plan exact compatible revisions, show the trust/permission/disk/network implications, obtain consent, then stage and publish the full accepted selection atomically. A library/project open never silently installs a missing dependency.
2. **Discover (existing pack loader):** \`astrid/core/pack/loader.py\` and \`discovery.py\` enumerate admitted pack roots and their \`pack.yaml\` records; they do not recursively interpret arbitrary subfolders. Preserve collision handling and managed source identity.
3. **Register metadata (existing Astrid extension registry):** \`astrid/core/extensions/sidecar.py\` and \`registry.py\` find point and contribution YAML sidecars of admitted packs, check API/schema and disable/quarantine/shadow status **without importing contributor Python during discovery**. Add/finish Plan 17's install-time owner-dependency, point compatibility and staged contribution validation before claiming that a contribution is ready.
4. **Activate on demand (owning H3/VibeComfy point):** once the selected H3 workflow-family is described/dry-run, retrieve the resolved eligible contribution for \`h3_av.levers\` (or its future VibeComfy-owned equivalent), then load/check the provider *through the existing lazy-entry and protocol-verification hook*. The host owns admission and trust; H3 owns semantics, typed lever registration and graph-lowering compatibility. **A generic extension registry cannot itself know how to insert H3 graph nodes.**
5. **Compile (H3):** freeze a per-job selection of provider identities/versions/digests; validate all control schemas, order/conflicts, resource needs and timing; combine lowerings only through H3's admitted six mechanisms. No provider directly overwrites another provider's ComfyUI graph or changes the lowering of an unrelated control. Duplicate qualified lever IDs, incompatible chains or an unavailable model patch are reported before claim.
6. **Execute (VibeComfy/worker):** the VibeComfy workflow family builds one graph and derives its *reachable* custom-node, model and plug-in requirements. The selected local/remote machine receives the exact pinned plug-in distributions and node sources it needs; the worker's attested inventory must match the compiled job. A provider installed on the controller but missing on the worker remains unavailable, rather than falling back silently.
7. **Finish/reconcile:** VibeComfy's \`after_outputs\` path and H3's composition/verification produce output and provenance tied to the resolved provider closure. The receipt states which provider lowered which controls, which spans were exact versus soft, and the installed source/pins. An update affects only future admitted work; active jobs retain their selected immutable generation.

**Current versus proposed:** Astrid already has a scan-based pack loader, source selection, a sidecar extension registry with lazy \`entry()\`, a package dependency ID validator, and group install machinery. The complete range solver, arbitrary embedded child-pack installs, H3 lever-provider extension point, VibeComfy family bridge and worker plug-in custody are **proposed or Plan 17 work**, not shipped capabilities of this design note.

### Dependency reconciliation, version selection and uninstallation

For each install/update/disable/removal request:

- Compute the **entire selected dependency graph**, not just the newly added pack. Intersect all hard version constraints, point API ranges, supported platform/python/engine/runtime constraints and release pins. Choose *one* selected version per pack ID for this admitted environment; refuse an unsatisfiable graph with the exact two constraints and owners. A user explicitly selected release pin is not silently replaced by a toolkit.
- Resolve packages from *approved sources* and record a lock/receipt for exact commits, artifacts and digests; a semantic version alone does not prove byte identity. A multi-repository aggregate requires multi-source resolution and staging beyond today's single-source group transaction. Implement that as one trusted transaction extension, not repeated live \`packs add\` calls or a custom toolkit installer.
- Give optional suggestions different semantics from hard requirements. Missing optional ControlNet does not break an NKD-only recipe; a recipe that explicitly selects ControlNet must fail with an actionable install/enable suggestion. Avoid eagerly installing every optional custom node/model on every machine.
- **Disable** an add-on: contributions disappear from new describes/dry runs; depending recipes become unavailable and explain why, but existing media and historical receipts remain. **Remove/update** a pack: compute reverse dependencies and require an explicit plan/consent if other installed toolkits need it. Do not remove a shared dependency just because one toolkit was removed. Rollback restores the previous *whole admitted graph* and extension inventory, not a mismatched collection of individual folders.
- Preserve source trust and permission boundaries. A toolkit cannot claim ownership of an independent provider, edit its PIN, load unapproved Python during discovery or vendor GPL-3.0 NKD source into Apache-licensed Agent merely by naming it as a child.
- Resolve conflicting contributions before execution. Stable qualified contributor/kind IDs avoid accidental collisions; explicit point cardinality/conflict rules and deterministic ordering replace filesystem-order or "last loaded wins". The user-facing catalog should show effective provenance, version, disabled/quarantined reason and the owner of each capability.

### Focused proof that exercises an actual *sub-pack inside someone else's toolkit*

1. Install H3 as the base dependency, an independently sourced \`h3_nkd_steering\` child provider, and \`cinematic_recast\` from a third publisher that declares both dependencies. Confirm one selected pack per ID, an exact combined lock, one admitted provider contribution and two valid presentation paths (H3 capabilities and cinematic toolkit).
2. Install a second toolkit sharing \`h3_nkd_steering\`. Disable the first toolkit: the shared provider remains available for the second. Remove or upgrade the provider with reverse dependents present: either compute a compatible new graph and consent, or refuse without changing the admitted state.
3. Publish both \`cinematic_recast\` and another independently installable pack from one source repository through explicit subpaths. Prove discovery *does not* interpret a nested \`pack.yaml\` under a selected pack by default, and that a deliberately selected child subpath retains its own independent ID/PIN.
4. Change H3 to an incompatible pack version/point API while both toolkits are installed: dependency resolution fails with an intelligible conflict. A provider disabled or quarantined by an invalid manifest never reaches the H3 lowering hook; a missing node on the worker refuses before inference.
5. A single H3 request selects native still preservation plus NKD soft guidance; the dry run and receipt distinguish exact output from model influence, map delivered to sampled frame indices, and enumerate only the actually used node requirements. The base generation still works unchanged with no NKD pack installed.

**Decision boundary:** this closes the missing loader/ownership explanation in the research, not in the shipped pack system. An implementation task should explicitly name the current source files, whether Plan 17's mirror is available, which APIs change, and a migration path for preexisting simple ID-list dependencies. Do not let “nested folders” silently become a second package manager.

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
