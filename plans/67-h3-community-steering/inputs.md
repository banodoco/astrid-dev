# Inputs — H3 community steering

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — in the Plan 59 session on 18 November 2026 the owner asked that Plans 64–66 stay focused on the existing tools, with "a follow-up project for some of the stuff that we don't do right now… centred around Nekodificador, or what we need to service that". They also asked how NKD's speech scheduling would work with a master frame. Next: the owner greenlights this scope.

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

**Challenge:** Not needed — this plan adds lever kinds on the Plan 66 contract, which has its own independent critique, functional review and red-team review recorded in Plan 66's inputs. The plan reuses those findings. An independent critique is recommended before dispatch, once Plan 66 has landed.

**Proof and limits:** CPU only (D1). Proof covers compiled graphs, table status, refusals, dry-run strings and bindings, and recipe admission. How well timed prompts, guide phase, curves, ControlNet and two-actor direction are followed needs the owner's live test.

**Review rounds:** Recommend 1 at the end. Next: the owner confirms.

**Run start:** Pending — No run is authorized. Next: the owner starts a run after Plans 64–66.

## Owner decisions

- **D1 — CPU only (decided 18 Nov 2026, owner in the Plan 59 session, as for Plans 64–66).** No task claims a machine or spends money. Live sessions during the work are pending as [Plan 66 D6](../66-h3-composable-core/inputs.md#owner-decisions).
- **D2 — use NKD Basic Tools as a pinned external node pack (decided 18 Nov 2026, owner: "Astrid is fully open source, so we can use it").**
  - Pin commit `c157722a` and declare it in the worker recipe or node set, the same way the GPL-3.0 motion pack and ComfyUI already are.
  - Astrid calls NKD's nodes through graphs, like any other node pack.
  - Do not copy NKD source into astrid-agent: astrid-agent is Apache-2.0, and vendoring GPL-3.0 code into it would change its licence.
  - The reimplement-first route is dropped. The curve tool is a thin Astrid wrapper around NKD's Event Curve node.

## Source identities

Planning snapshot: astrid-dev main after Plan 66's merge; `astrid-agent` `origin/release/14/main` (`9f614dff`); ComfyUI `6bfaacc`; the H3 motion pack `361624fb`; NKD Basic Tools `c157722a2b484d80dee6b6d3f166c90d9ec197b8`. At dispatch, record the release, its `release/<NN>/main` SHA, the Plan 64–66 merge SHAs and the `release/<NN>/plan-67` head.

## References

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
