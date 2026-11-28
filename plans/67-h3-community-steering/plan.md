# H3 community steering

**Project:** H3 community steering

**Goal:** An agent steers H3 shots with timed prompts, guides, curves, LoRAs and ControlNet, and a standard H3 installation includes a separately pinned, removable NKD steering pack. Prove independent, shared and chained pack composition through the same compiler and existing pack lifecycle, with two real providers that stack: NKD by default and the optional H3 Experiments pack.

**Status:** queued

**Owner:** Unassigned

**Target milestone:** 0.2

**Estimate:** Prior CPU estimate 9.5 days, plus an estimated 3–5 days for the H3 Experiments provider and combined proof (CS-12, CS-13); re-estimate the bounded provider/default-companion work at CS-0. Live qualification separately authorized.

**Waiting on:** Plan 66's reviewed provider contract; verified 64/65 inputs; Plan 68 for guides; Plan 70 for continuation recipe (all allocated to Release 16 in the proposed brief); Lead run start. External activation waits only for CS-0, not all of Plan 17.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

Plan 66 gives every H3 job one shape: three families of levers (Output, Context, Process), a capability table keyed by lever kind, six compile mechanisms and composition. This plan adds the nuanced, community-proven ways of steering a shot on top of that, each as a lever kind, a table row, one lowering function and a recipe. It adds no new request structure and no seventh mechanism.

**Included:**
- **Timed prompts.** `prompt` may be a list of `{during, text}`. It lowers to one prompt in H3's own timed shot format and is soft: it biases when things happen, and never guarantees it.
- **`phase` on guides.** A guide can act only during part of the denoising (`phase: [0, 0.2]`). It lowers to a schedule over the timed rows: stock conditioning time ranges if they compile, otherwise NKD's MiniMax Guides node.
- **`phase` on LoRAs**, only if a lowering is proven to compile with the H3 model. Otherwise it stays `unavailable`, and says so.
- **Curve audio guides.** A thin Astrid tool runs NKD's Event Curve node and saves its output as an ordinary audio file, which the agent then uses as an audio `guide`. The curve is a tool that makes an input, not a lever.
- **ControlNet** as `role: control`, through the official `MiniMaxH3FunControlNetApply`: a control video, optional mask and source, strength, and `phase` as the node's start and end percent.
- **Signals.** The dry run reports, for each prompt tag, which occurrence and soundtrack it is actually bound to, and which character the author said it is for. Two-actor dialogue is supported as soft direction only, written in the prompt.
- **Recipes and skill sections:**
  - speech timing on a still master: silent, then speaking, then reacting;
  - speech timing plus a mouth-mask redub;
  - speech in a continuation;
  - two speakers alternating;
  - a curve-guided action;
  - ControlNet motion;
  - a late LoRA.
- **An honest status** on every new kind: `compiles`, `live-tested` with a cited render, or `unavailable`.

**Independent default extension proof.** Ship `h3_nkd_steering` as an ordinary, independently maintained, pinned and removable pack, with `install_tier: default`, hard dependency on `h3_av` and a contribution to H3's versioned provider point. H3 advertises NKD as a soft default companion, not a hard dependency. Reuse the existing release/default install transaction; prefer `poms_packs/h3_nkd_steering` beside the existing release-pinned `astrid_motion` so the approved default group retains one source repository and commit. NKD's tool is a real pack-owned input-maker advertised through H3's provider discovery, never a fake lever. Try stock guide scheduling first; if it fails, put the NKD lowering in the independent pack. If stock works, the real tool contribution still ships and an installed fixture proves a new lowering. Timed prompts, binding reports, native LoRA scheduling and basic guides remain H3-owned. ControlNet stays a native optional capability unless independent distribution is justified. A toolkit may depend on both; use one small diamond-shaped integration fixture: two independently installed toolkits share NKD, and one also contributes a consumed input/preset to an NKD-owned point. If stock scheduling wins, that same toolkit can supply the test H3 lowering with a distinct contribution key. No separate demo framework or unused extension point merely for the proof. No new sub-pack runtime, recursive folder scanning or cross-repository version solver.

**Default composition contract.** A host can declare default companion IDs (proposed `default_addons`; reuse an equivalent supported field if present). It is a soft, generic selection relationship, distinct from `dependencies.packs` and contribution points. Resolve only from explicitly approved, pinned candidates, through the existing default/group installation planning and atomic transaction. Default selection follows declared links from selected hosts, including a built-in host, with deterministic deduplication and cycle diagnostics; no unapproved source lookup. Hard dependency ordering and soft selection are distinct: H3 selecting NKD by default and NKD requiring H3 is the normal case, not a dependency cycle. Use one planning step against the approved candidate pins before consent/freeze; for the release, the existing manifest is the authoritative frozen exact selected default pin list. Its installer applies that list, respecting existing opt-outs, rather than discovering or expanding new package sources at runtime. For a separately installed host, offer/choose approved same-source companion pins in the existing consent preview; if none are available, report the optional companion and allow base-only installation. No silent cross-source installation. A user removal/disable survives update/rollback; only explicit re-add clears a removal preference. A default add-on remains removable unless an installed hard dependent requires it (then existing refusal/explicit group removal applies). No node/model download just because an add-on's Astrid package is installed; actual used graph requirements follow the existing approved workflow/setup path. CS-10 and CS-11 deliver this contract, not a parallel default inventory.

**NKD Basic Tools** is used as a pinned external ComfyUI custom-node pack on the worker, like the motion pack and ComfyUI itself (D2). Astrid calls its nodes through graphs, and no NKD source is copied into astrid-agent.

**Second provider: H3 Experiments (D5).** Ship [ComfyUI-MiniMaxH3-Experiment](https://github.com/Kentskooking/ComfyUI-MiniMaxH3-Experiment) (MIT, pinned at `14cc4824d965f7c900b427b4d2d0241c8e7df58c`) as a second ordinary, independently installed pack, `h3_experiments`: **optional, not a default**, installed through the existing consent path, and every contribution marked beta. It is the proof that the provider contract generalises beyond data rows. Like NKD, its nodes are a pinned external custom-node pack on the worker; no source is copied into astrid-agent. It uses Plan 66's pass stages, its two contribution kinds (actions, and graph fragments with typed ports and an optional pure `admit()` check), and its footprint vocabulary (see [Plan 66 reservations](../66-h3-composable-core/tasks.md#reservations-for-plans-67-68-and-70)). Every footprint below was checked against the pack's source at the pinned commit (see [inputs](inputs.md#h3-experiments-source-evidence-28-nov-2026)):
- **Action (stage 1):** Mask Profile, which makes complementary feathered masks as ordinary media.
- **Branch transform (stage 3): Omni Reference Blend ("context smashing").**
  - Takes two Omni branches whose reference slots match in kind and latent shape.
  - Refuses audio references and inputs that already carry guides, control or hooks. Guides attach after it.
  - B's prompt is cut or padded to A's token count, and a video reference's soundtrack comes from A only. Declare both, or refuse video references with audio.
  - Transforms nest: blend into blend, and blend into the masked guider, are allowed.
- **Row fragment (stage 4): Virtual Head Start.** Writes frame-zero guide positions on the out-of-canvas clock. It stays the pack's node, because stock `MiniMaxH3AddGuide` cannot place a guide before frame 0.
- **Model fragment (stage 5): Generated Timeline Forward Offset.** Writes `model.position_ids` additively. It is single instance: a second copy replaces the first.
- **Guider strategies (stage 6):**
  - **Masked Conditioning Guider.** Cost is counted in conditioning entries, up to N + N(N−1)/2 evaluations per step. `admit()` requires the masks to cover the frame, because uncovered regions get no update. Overlap mode refuses phase windows and video or audio references.
  - **Regional Attention / Interaction Guiders.** Exclusively patch `model.attention_forward` and `model.text_preprocess`. They need first-frame or text branches, batch size 1 and matching shared settings, and refuse Omni references, phase windows, control and hooks. Some ordering checks fire only at sample time.
- **Sampler strategy (stage 7): Continuation Sampler.**
  - Requires a regional guider, and a schedule ending at 0.
  - Brings its own `cycles` arrangement with no noise mask. The delivered length is window + (cycles − 1) × (window − context), declared and checked by H3.
  - Records per-cycle seeds. Checkpoint writing is forced off, because its files carry the prompt and workflow outside managed custody.
- **Not exposed:** Latent Composite, because the starting latent belongs to H3's arrangement.

The regional strategies need a first-frame branch encoder (`MiniMaxH3ImageToVideo`), which H3 does not lower today; CS-12 adds it to H3. Astrid makes no quality claim for any of these; the live test judges them, including whether Astrid's attention backend accepts the regional attention mask. Exactness still holds: H3 checks the delivered length and time map, no strategy touches composition, and composition restores and verifies kept content.

**Not in this plan. Do not build these:**
- a GPU or live run (D1). The owner tests afterwards;
- general VibeComfy standalone H3 extraction, automatic multi-source dependency resolution, or packaging every lever as a pack; these are not prerequisites;
- hard word timing: no node enforces when a word is spoken;
- hard per-actor routing of voices or references within one pass (H3 Experiments' regional strategies are soft and optional; Astrid builds no native version);
- stem separation, or editing one voice under music;
- take selection, shot workflow, budgets or approvals;
- passing a take's internal latent between jobs (for example an exact upscale of a winning take);
- native windowed long generation coordinated inside the sampler (H3 Experiments' cycle sampler is offered only as an optional beta strategy, and does not replace Plan 70's continuation);
- per-step LoRA ramps, IC-LoRA, camera trajectories, negative prompts and guidance schedules.

Each of these is a one-line later issue in [inputs.md](inputs.md#references).

## Existing work and decision

The H3 node already accepts what this plan needs:
- timed shot text in the prompt;
- timed guide rows (`MiniMaxH3AddGuide`);
- the Fun ControlNet patch with start and end percent.

NKD's MiniMax Guides node schedules each guide over denoising progress, and its Event Curve node synthesizes a clip-time audio guide. Neither schedules real words ([research/nkd-speech.md](research/nkd-speech.md)). The ten-capability check found every item fits the Plan 66 model without a seventh mechanism ([research/extension.md](research/extension.md)). The two-actor case fails in one pass, because references and text are shared across the whole frame. So this plan reports bindings honestly and promises only soft direction ([research/breaking-cases.md](research/breaking-cases.md)). The evidence and owner decisions are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Plans 64, 65 and 66 land first; CS-0 independently reviews the actual extension/installation/worker boundary and supplies only missing shared validation before real external activation. Plan 17 is not a whole-project dependency. Native work does not wait for external activation; this plan uses Plan 66's capability table, dry-run view and recipe format, cites the design in `astrid/packs/h3_av/docs/design.md`, and wraps [Plan 68](../68-h3-guides-and-stills/plan.md)'s guide lowering. Timed prompts, binding reports, ControlNet and LoRA phase (CS-2, CS-6, CS-5, CS-7) can start after Plan 66; guide phase and the curve tool (CS-3, CS-4) wait for Plan 68; the `speech-continue` recipe in CS-8 waits for [Plan 70](../70-h3-continuation-bridges-inserts/plan.md).

Order:
1. After 66, CS-0 reviews the narrow shared boundary and CS-2, CS-5, CS-6 and CS-7 may start on disjoint files (serialize overlapping schema/builder edits). CS-10 implements generic soft companion selection after CS-0; coordinate its writer with staged admission.
2. CS-1 pins and packages NKD after CS-0. CS-3 follows 68; try stock scheduling first, with the NKD fallback only after CS-1.
3. CS-4 implements the independent pack's curve tool after CS-1 and CS-3. CS-8 adds recipes and skills; the continuation recipe waits for 70.
4. CS-11 proves actual default release selection/installation with both pack pins and the existing installer; uses final provider and CS-10. CS-9 joins all features and default proof, then tests independent installation, shared and chained contributions, lifecycle and local/attached/RunPod CPU custody before final review.
5. CS-12 adds H3's first-frame branch encoder and packages H3 Experiments once Plan 66's fragment and strategy contract is reviewed at its R1, in parallel with the NKD work: it shares no installer or default-delivery writer. CS-13 installs both packs together and proves the stacking matrix, after CS-9 and CS-12.

[Task cards](tasks.md)

## Interfaces and handoff

**Consumes:**
- Plan 66's job, lever-kind table, dry-run view, recipe format and skills, and its design file; Plan 68's guide lowering; Plan 70 for the `speech-continue` recipe;
- Plan 64's reference rows and audio rule;
- NKD Basic Tools at commit `c157722a2b484d80dee6b6d3f166c90d9ec197b8`;
- Plan 66's pass stages, contribution kinds (action, node descriptor, strategy) and shared footprint vocabulary, for CS-12 and CS-13;
- ComfyUI-MiniMaxH3-Experiment at commit `14cc4824d965f7c900b427b4d2d0241c8e7df58c`.

**Produces:**
- the timed `prompt` form;
- `phase` on guides (and on LoRAs, if proven);
- `role: control`;
- the independently installed, default-selected `h3_nkd_steering` pack, curve tool, and conditional guide lowering; generic soft companion selection, exact existing release manifest pins, and real provider/worker custody, shared/chained composition and lifecycle evidence;
- the optional, independently installed `h3_experiments` pack with beta-labelled action, fragment, guider and sampler contributions, and H3's first-frame branch encoder;
- the per-tag binding report;
- recipes and skill sections for each;
- table rows with honest status.

## Completion

CPU tests prove each of these:
- A two-segment timed prompt serializes, in time order, into H3's timed shot format, and the dry run shows the final string.
- A guide with `phase: [0, 0.2]` compiles with proven stock scheduling, otherwise through the installed NKD provider's MiniMax Guides with that `until`, at the right frame.
- The curve tool writes an audio file from an Event Curve recipe, and that file works as an audio guide at frame 0.
- A pose control video with `phase: [0, 0.6]` compiles to `MiniMaxH3FunControlNetApply` with matching start and end percent.
- `describe` shows each new kind's status.
- A LoRA `phase` either compiles through a proven hook, or is refused from the table as `unavailable`.
- For a two-speaker request, the dry run names which occurrence and soundtrack each `<Audio n>` tag is bound to, and marks per-actor binding as soft.
- Actual fresh Release 16 installation includes NKD beside H3 and preserves other defaults; existing-user update adds the default unless removed or disabled, failed stage/rollback preserves previous state and user choices, explicit re-add works. Base H3 generates/edits without NKD, no unnecessary node/model provisioning, and NKD's real curve tool appears with source/status in normal H3 discovery. A generic non-H3 host fixture proves soft companion selection with the same transaction (including fanout, chain, duplicate and cycle/refusal cases), not an H3 hard-code. Unknown/unapproved pins do not install silently.
- Two independent toolkit fixtures share one NKD identity; another fixture contributes to an NKD-owned point through the ordinary registry, proving an extension can itself be extended. No unique parent or duplicate installation. Prove exact selected provider and reachable requirements agree on controller and worker CPU paths; refuse missing/incompatible/unshipped providers and collisions before claim. If stock guide scheduling works, use an installed lowering fixture in addition to the actual NKD tool contribution.
- Every recipe fills, dry-runs and compiles, and a small-model cold read reaches a dry run for the speech-timing recipe.
- With NKD and H3 Experiments installed together, each H3 Experiments contribution either compiles with its pinned nodes or is refused before claim with its named reason. Across the CS-13 matrix, H3's decision from footprints and `admit()` matches the cited source checks of each node. Checks that fire only inside the model are listed as live-only, not claimed. Removing either pack leaves the other working, and base H3 is unchanged without both.

Review then closes the plan. How well timing, guides, curves and ControlNet are followed is judged in the owner's live test afterwards.
