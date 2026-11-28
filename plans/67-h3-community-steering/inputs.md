# Inputs — H3 community steering

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — Owner agreed in ChatGPT on 27 Nov 2026 to the revised first real, default-installed but removable NKD companion, generic composable packs, and full delivery of 66/67 in Release 16. The brief also allocates required 68/70 producer plans, preserving their existing scopes. Next: independent critique of the exact default/activation interface and Lead run start; no execution or publication claimed by this planning PR.

**Prior art:**
- **NKD Basic Tools** (commit `c157722a2b484d80dee6b6d3f166c90d9ec197b8`, GPL-3.0) has two relevant nodes ([research/nkd-speech.md](research/nkd-speech.md)):
  - **Event Curve** (`NKDEventCurveAudio`) draws or derives a clip-time envelope and synthesizes an audio guide. Its `W Guide (words)` mode makes muffled, speech-like audio that sets pauses and syllable rate. It doesn't contain the line.
  - **MiniMax Guides** (`NKDMiniMaxGuides`) anchors image, video and audio guides through the stock `MiniMaxH3AddGuide`. Its `until` controls the fraction of denoising during which each guide stays active.

  Neither schedules real words; the evidence is the author's description and an example workflow, with no measurements.
- **The official H3 node** (ComfyUI `6bfaacc`) exposes the following ([research/extension.md](research/extension.md)):
  - timed guide rows;
  - first and last keyframes;
  - reference slots;
  - `MiniMaxH3FunControlNetApply`, which takes a model patch, VAE, strength, `start_percent`, `end_percent`, and an optional control video, mask and source.
- **H3's prompt guide** writes timed shots as `[Shot n] At 00:03.000, …`. That is a documented convention, not frame isolation.
- **The ten-capability check** found every item fits the Plan 66 lever model without a seventh mechanism. Multi-pass upscaling sits above a single job.
- **The red-team review** ([research/breaking-cases.md](research/breaking-cases.md)) found that two actors with independent voices can't be routed within one pass, because references and text are shared across the frame. The owner set most of that list aside for later; only honest binding reports come into this plan.
- **Plan 66's design** is in [its research/levers.md](../66-h3-composable-core/research/levers.md) and [plan](../66-h3-composable-core/plan.md).

**Approach:** each capability is a lever kind with a table row, one lowering function into an existing mechanism, and a recipe. Alternatives considered:
- **(a)** A "speech schedule" lever family. Rejected: speech timing is a timed prompt plus an optional audio guide.
- **(b)** Reimplementing Event Curve in Astrid. Dropped once D2 was decided.
- **(c)** Hard per-actor routing now. Rejected: no H3 lowering exists.

**Challenge:** Reviewed — the alignment review of 18 November 2026 ([research/alignment-review.md](research/alignment-review.md)), backed by a source check of each task against the NKD, ComfyUI and Astrid code ([research/alignment-luna.md](research/alignment-luna.md)), found Plans 64–66 largely aligned with this plan. All twelve of its edits are accepted: guide `phase` is tried first with stock conditioning time ranges, so no NKD node enters job graphs unless needed; `phase` is allowed on any kind the table permits; node packs are declared per lever kind and the worker's pack list is read from the pins; the dry run shows the final prompt string; the guide lowering stays one function; the curve tool uses the node's 32 kHz and names its offset `--offset`; ControlNet starts by proving pinned weights exist and stays `unavailable` otherwise; signals report labels without reading the prompt; CS-5 and CS-7 depend only on CS-1. The review found the source check's call for broad compatibility wording overstated. Plan 66's own critique, functional review and red-team review are recorded in its inputs. An independent critique is still recommended before dispatch, once Plan 66 has landed.

### Provider boundary and Plan 17 dependency (27 Nov 2026)

Source-only assessment at Agent `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5`; refresh at dispatch. Existing assets to reuse:
- [`core/extensions/registry.py`](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/extensions/registry.py), `model.py` and `sidecar.py`: metadata discovery, versioned points, schema/effects checks, quarantine/shadow/disable and lazy entry import/protocol check. Registry exists and production generation engine/machine callers use it. H3 must use effective admitted contributions, not scan raw folders or call `entry()` on a stale/untrusted record; inspect the actual trust/custody path before activation.
- [`vibecomfy/extensions/points/workflows.yaml`](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/packs/vibecomfy/extensions/points/workflows.yaml), H3 workflow hooks and `core/generation/entries.py`: already supply the workflow entry/controller build and after-output paths. H3's provider point is not a second workflow family. No VibeComfy native plugin extraction needed.
- [`core/pack/transaction.py`](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/pack/transaction.py) and `pack_validation.py`: existing explicit ID dependency checks and staged group install/rollback, but no observed extension registry parse in the staged transaction, nor point-owner dependency enforcement there. This is Plan 17 P1's concrete gap. Reuse its proof and bring forward only the missing staged validation/owner-dependency/trust slice via CS-0; coordinate a bounded shared PR and record the accepted head for P17 P1 so later work does not duplicate it. Do not claim P1 complete without its actual proof.
- [`packs/runpod/machine.py`](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/packs/runpod/machine.py) ships the active installed pack selection with revision/tree digest and file hashes and refuses unshipped workflow entries. A built-in H3 entry using an outside provider may need additional pre-claim selected-provider custody validation: prove the controller/worker identity and requirements rather than assuming this is already handled. No full P17 A2 wheel/plugin transport needed for an ordinary installed Astrid pack; a missing custody check is a bounded CS-0/CS-9 repair, not a new transport.

**Ruling for the revised scope:** Plan 66 has no dependency on 17. Native 67 tasks have no dependency on 17. For the external proof, CS-0 requires only the source-confirmed missing part of P17 P1 and any narrowly proven activation/custody gap; no dependency on V1–V5, A1–A4, H1, C1–C3, IMG or S2. P2/P3 full CLI/docs are not gates; use the existing pack action discovery and H3 describe, with bounded docs for the new point. Plan 17 remains paused and owns the eventual generic VibeComfy family/standalone H3 migration. Its H1 still references v1 and `branch_for`; refresh it after 66 before running it. No claim that 17 has been amended. Existing ID-list hard dependencies and independent installs suffice for the first proof. The owner's follow-up requires a soft default-companion relation and real default installation, scoped below; version-range/multi-source automatic solving is deferred. Keep the H3-owned point first, not a premature universal control API. Provider code is trusted by the existing install policy, not a sandbox; no loading at metadata discovery. Verify no new core H3 imports.

**Focused elegance check (27 Nov; source-only, not independent review):** [`test_no_astrid_imports.py`](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/tests/packs/h3_av/test_no_astrid_imports.py) forbids all Astrid imports in kept H3 modules except its CLI; keep the guard unchanged and inject the admitted provider input through the existing host hook/facts boundary. `core/extensions/model.py` qualifies a contribution by pack ID and key, and `registry.py` selects winners by that ID; a pack contributing to several points uses distinct keys under the current contract. Do not add a second registry or change identity semantics for this proof. `transaction.py` already preserves current removal tombstones even on rollback. Use that owner instead of a companion-specific opt-out store. Merge the extension-of-extension witness and any synthetic lowering into one of the two already-needed toolkit fixtures, so the integrated proof is one actual shared dependency graph, not a catalogue of demo packs. Keep the generic companion selector proof in CS-10, exact default delivery in CS-11, and actual contribution consumption/worker custody in CS-9; consume the prior receipts and rerun only invalidated inputs under the release contract.

Independent architecture critique and exact selected release baseline are pending, not performed here. Review 66's typed seam, real registry invocation, dependency/install custody and the task boundary before dispatch; if a generic prerequisite exceeds CS-0's narrow bounds, record a separately scoped prerequisite and block external activation only. Do not block native work or silently widen product scope. The older exploratory research is retained as history; this decision supersedes its recommendation to consider a separate project for this first proof.

### Default companion source evidence and decision (27 Nov 2026)

The published [Release 15 manifest](https://github.com/banodoco/astrid-app/blob/main/public/install-manifest.json) pins `astrid_motion` at `banodoco/poms_packs` `2379ab54aca522019ff4f869cfdf9375bdb56dfc` (also observed `main`); that repo has independent pack roots. Agent `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5` has [`core/pack/defaults.py`](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/pack/defaults.py), `release_manifest.py`, `transaction.py`, and `installer/tools.py`: exact default `repo/commit/digest_rule/digest` pins, same-source/same-commit atomic group, default reconciliation, current removal tombstones, no undeclared dependency fetch. `tests/core/pack/test_defaults.py` and `test_release_manifest.py` cover user-owned packs, rollback and removal preferences. `docs/packs/pack-taxonomy.md` already defines removable `install_tier: default`. No observed pack-specific default-companion selector. H3 currently ships inside Agent, declares hard dependency `vibecomfy`, and must remain functional without NKD. The first-party default list is the exact release pin authority, not a version resolver. `poms_packs` is an external pinned input (not one of astrid-dev's six recognized release-branch-table repositories); the Lead records its actual reviewed source PR/commit and both pack tree digests rather than creating an unsupported branch-table entry.

**Choice:** make a small generic soft companion selection in the existing pack/default planner, preserving the one transaction and one frozen release pin list. Keep the selector a pure projection of declared companion IDs, approved pin candidates and user choice; no second resolution at execution. Validate hard dependency cycles on hard edges only: the normal H3 soft selection of NKD and NKD hard dependency on H3 must not be rejected as circular. Soft traversal deduplicates and reports its own cycles. Use the release pin-preparation step to select/check exact companion rows, then the existing installer applies the frozen list. For the first release, use one repo/commit group for default NKD and `astrid_motion`. Declare companion IDs in the owning pack, not a hard reverse dependency; distinguish requested host roots from approved candidate pins in the selection/consent input (not a new persistent ledger). No auto-discovery of nested pack.yaml or new multi-source resolver. Unknown/removed/disabled optional companion leaves base working and is explained; explicit re-add is the only way to clear removal; hard dependents still use existing graph checks. Existing setup consent remains the only owner of installing actually used nodes/models; default Astrid pack presence is not permission to mutate ComfyUI. Plan 31 remains the only release manifest writer. CS-10 proves generic selection, CS-11 proves default delivery and CS-9 proves real composition. Validate actual source before implementing exact field/API; if any needed broader generic solver or unsafe trust relaxation is discovered, stop that boundary and return to the Lead, not a parallel package manager.

**Proof and limits:** CPU only (D1). Proof covers compiled graphs, table status, refusals, dry-run strings and bindings, and recipe admission. How well timed prompts, guide phase, curves, ControlNet and two-actor direction are followed needs the owner's live test.

**Review rounds:** Recommend 1 at the end. Next: the owner confirms.

**Run start:** Pending — no product execution or release authorized. Next: confirm independent boundary review, Plan 66 contract, release placement and owner run authorization.

## Owner decisions

- **D1 — CPU only (decided 18 Nov 2026, owner in the Plan 59 session, as for Plans 64–66).** No task claims a machine or spends money. Live sessions during the work are pending as [Plan 66 D6](../66-h3-composable-core/inputs.md#owner-decisions).
- **D2 — use NKD Basic Tools as a pinned external node pack (decided 18 Nov 2026, owner: "Astrid is fully open source, so we can use it").**
  - Pin commit `c157722a` and declare it in the worker recipe or node set, the same way the GPL-3.0 motion pack and ComfyUI already are.
  - Astrid calls NKD's nodes through graphs, like any other node pack.
  - Do not copy NKD source into astrid-agent: astrid-agent is Apache-2.0, and vendoring GPL-3.0 code into it would change its licence.
  - The reimplement-first route is dropped. The curve tool is a thin Astrid wrapper around NKD's Event Curve node.

- **D4 — default companion, complete programme (owner direction, 27 Nov 2026, ChatGPT follow-up).** NKD ships by default with H3 but is not required by it, is independently removable/upgradable and shares existing default install/reconciliation; generic soft selection, real tool discovery, two consumers and extension-of-extension are acceptance proof. Include 68 and 70's existing producer work in R16 so every original 67 outcome remains in scope. Keep one source group for initial default delivery and no all-of-P17 requirement. This is scope direction, not GPU or publication authorization. See CS-10/11 and CS-9.

- **D3 — first external provider (owner direction, 27 Nov 2026).** Use ordinary independently installed `h3_nkd_steering`, not a nested loader. Base H3 owns semantics, native kinds and exact composition. Separate NKD-specific tool and only necessary lowering; ControlNet packaging is conditional, not a new mandatory pack. Use CS-0 to close the proven shared prerequisite, without starting the full paused Plan 17. Preserve D1/D2 and review the exact extension protocol before execution.

- **D5 — second real provider: H3 Experiments (owner direction, 28 Nov 2026, Claude Code session).** Add [ComfyUI-MiniMaxH3-Experiment](https://github.com/Kentskooking/ComfyUI-MiniMaxH3-Experiment) beside NKD, so the plan proves two real providers stacking rather than one. It is optional (not a default) and beta-labelled, uses the same pinned-external-node rule as D2 (MIT licence, nothing copied into astrid-agent), and is the test case for Plan 66's strategy and node-descriptor contract. The design and its alternatives are in [#2065](https://github.com/banodoco/astrid-dev/issues/2065#issuecomment-7238057362) and the H3 guidance redesign document. See CS-12 and CS-13. This is scope direction, not GPU or publication authorization.

- **D6 — third real provider: Dials (owner direction, 28 Nov 2026, Claude Code session).** Add Matlow's ComfyUI-Dials as an optional beta pack and design the contract for all four reviewed packs, with MAINodes de-rope in [Plan 107](../107-h3-passes/plan.md). Licensing is settled by the owner: all components used are open source. Pin standalone ComfyUI-Dials, not MAINodes, on workers. See CS-14.

### Dials source evidence (28 Nov 2026)

Read at `a0a8a8f6ebe3f2b78904a6a106501f1bfdcb3a0c`; nothing was run.
- A post dial is a `DIFFUSION_MODEL` wrapper (`ContextShift`, key `mai_dial_post`) that adds a BF16 [5376] vector to the refined context each call (`dials/core.py:105-118, 148-154`).
- A pre dial is a `diff` patch on `diffusion_model.condition_proj.bias`.
- Rack envelopes are per-sampler-call `SAMPLER_SAMPLE` wrappers reading `transformer_options["sigmas"]` (`dials/envelopes.py:180-196`).
- Block strengths chain `patches_replace` entries on `("dit","double_block",i)` (`dials/blocks.py:110-117`).
- Time curves run an undialled and a dialled call on the first k steps and blend per latent frame. Rows sharing a curve share one branch. The clock comes from the latent's own shape, so it cannot be rebased (`dials/timecurve.py:160-176, 189-207`).
- ComfyUI-Dials and ComfyUI-MAINodes register the same rack node ids, resolved by `ownership.py`.

### H3 Experiments source evidence (28 Nov 2026)

Read at `14cc4824d965f7c900b427b4d2d0241c8e7df58c`; nothing was run. The pack registers 11 nodes (`__init__.py`):
- **Omni Reference Blend** (`conditioning/reference_blend.py`) takes two complete `ReferenceToVideo` conditionings, lerps their Qwen embeddings and reference latents (optionally along a time curve), and refuses inputs that already carry `control`, `hooks`, `gligen`, `model_conds` or `minimax_keyframes`. Guides must therefore be attached after it.
- **Regional Attention Guider** (`sampling/regional_attention.py`) joins branch contexts into one sequence and object-patches every block's `attn.forward` and `preprocess_text_embeds`. It refuses `minimax_refs` (Omni references) and `area`, `hooks`, `control`, `gligen`, `start_percent` and `end_percent`.
- **Masked Conditioning Guider** (`sampling/masked_guider.py`) blends per-branch predictions, with an embedding-overlap mode for pairs.
- **Continuation Sampler** (`sampling/continuation.py`) replaces `SamplerCustomAdvanced` and accepts only a regional guider (`:306`). It requires a schedule ending at 0 (`:312`), seeds each cycle as seed + index, and runs cycles that protect the previous AV latent tail without the arrangement's noise mask after cycle 1. The output is longer than the input: window + (cycles − 1) × (window − context). It adds a `DIFFUSION_MODEL` wrapper offsetting position IDs per cycle, and by default saves checkpoints under `output/h3_continuation` that embed the prompt and workflow (`:236–242`).
- **Generated Timeline Forward Offset** (`timeline/timeline_offset.py`) is a `DIFFUSION_MODEL` wrapper shifting generated position IDs. It removes its own earlier wrapper by key, so a second copy replaces the first (`:43–47`).
- **Virtual Head Start** (`timeline/virtual_head_start.py`) rewrites frame-zero keyframes' `resolved_frame_index` to a negative value. Stock `MiniMaxH3AddGuide` resolves negative indices from the end and rejects out-of-range ones, so this needs the pack's node.
- **Masked Conditioning Guider** overlap mode (`conditioning/overlap_conditioning.py`) refuses branch-specific `control`, `hooks`, `gligen` and `model_conds`, and strips `start_percent`/`end_percent`.
- **Mask Profile** and **Latent Composite Masked** are mask and latent utilities.

The author labels the regional guiders and the sampler beta, with full-model quality unverified.

## Source identities

Planning snapshot: astrid-dev main after Plan 66's merge; `astrid-agent` `origin/release/14/main` (`9f614dff`); ComfyUI `6bfaacc`; the H3 motion pack `361624fb`; NKD Basic Tools `c157722a2b484d80dee6b6d3f166c90d9ec197b8`; ComfyUI-MiniMaxH3-Experiment `14cc4824d965f7c900b427b4d2d0241c8e7df58c` (added 28 Nov 2026). ComfyUI-Dials `a0a8a8f6ebe3f2b78904a6a106501f1bfdcb3a0c` (added 28 Nov 2026). The Release 16 programme baseline is Agent `release/16/main` `4a2bad187f12e7b0d1ba5bd1164b4a076787516a`. At dispatch, record the release, its `release/<NN>/main` SHA, the Plan 64–66 merge SHAs and the `release/<NN>/plan-67` head.

## References

- **Historical architectural exploration (20 Nov 2026; direction superseded in part by D3):** [Composable control substrate and optional packs](research/composable-control-packs.md). Tests the owner's idea of H3 as a base frame/timeline control compiler with separately installed NKD, ControlNet and higher-level toolkit contributions; distinguishes model-specific lowering from generic VibeComfy machinery, and notes that Plan 71 is already occupied. This remains exploratory evidence; D3 and the revised task cards define the accepted direction, not every proposal in that note. Independent critique and run authorization remain required.

- [NKD speech scheduling research](research/nkd-speech.md), [ten-capability extension check](research/extension.md), [red-team cases](research/breaking-cases.md).
- **Later issues, not in this plan:**
  - **hard word timing:** needs a node that enforces when a word is spoken;
  - **per-actor routing:** independent voice and reference per character in one pass;
  - **stem separation:** replacing one voice under music and other voices;
  - **take and shot workflow:** selection, lineage, budgets, approvals;
  - **latent exchange between jobs:** exact upscale of a winning take, and sampler resume;
  - **windowed long generation:** coordinated inside the sampler;
  - **per-step LoRA ramps;**
  - **IC-LoRA;**
  - **camera trajectories;**
  - **negative prompts and guidance schedules;**
  - **original-master delivery outside a patch.**
