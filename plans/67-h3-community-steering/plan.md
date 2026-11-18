# H3 community steering

**Project:** H3 community steering

**Goal:** An agent can time what happens and what's said in an H3 shot, steer it with guides, curves, LoRAs and ControlNet at chosen points in the model's denoising, and see honestly which voice and reference each character is bound to, all through the Plan 66 lever model with no new mechanism.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 9.5 days (CPU only; the live test is separate and comes after)

**Waiting on:** Owner greenlight of scope, and Plans 64, 65 and 66.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

Plan 66 gives every H3 job one shape: three families of levers (Output, Context, Process), a capability table keyed by lever kind, six compile mechanisms and composition. This plan adds the nuanced, community-proven ways of steering a shot on top of that, each as a lever kind, a table row, one lowering function and a recipe. It adds no new request structure and no seventh mechanism.

**Included:**
- **Timed prompts.** `prompt` may be a list of `{during, text}`. It lowers to one prompt in H3's own timed shot format and is soft: it biases when things happen, and never guarantees it.
- **`phase` on guides.** A guide can act only during part of the denoising (`phase: [0, 0.2]`). It lowers through NKD's MiniMax Guides node, whose `until` is that phase.
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

**NKD Basic Tools** is used as a pinned external ComfyUI custom-node pack on the worker, like the motion pack and ComfyUI itself (D2). Astrid calls its nodes through graphs, and no NKD source is copied into astrid-agent.

**Not in this plan. Do not build these:**
- a GPU or live run (D1). The owner tests afterwards;
- hard word timing: no node enforces when a word is spoken;
- hard per-actor routing of voices or references within one pass;
- stem separation, or editing one voice under music;
- take selection, shot workflow, budgets or approvals;
- passing a take's internal latent between jobs (for example an exact upscale of a winning take);
- windowed long generation coordinated inside the sampler;
- per-step LoRA ramps, IC-LoRA, camera trajectories, negative prompts and guidance schedules.

Each of these is a one-line later issue in [inputs.md](inputs.md#references).

## Existing work and decision

The H3 node already accepts what this plan needs:
- timed shot text in the prompt;
- timed guide rows (`MiniMaxH3AddGuide`);
- the Fun ControlNet patch with start and end percent.

NKD's MiniMax Guides node schedules each guide over denoising progress, and its Event Curve node synthesizes a clip-time audio guide. Neither schedules real words ([research/nkd-speech.md](research/nkd-speech.md)). The ten-capability check found every item fits the Plan 66 model without a seventh mechanism ([research/extension.md](research/extension.md)). The two-actor case fails in one pass, because references and text are shared across the whole frame. So this plan reports bindings honestly and promises only soft direction ([research/breaking-cases.md](research/breaking-cases.md)). The evidence and owner decisions are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Plans 64, 65 and 66 land first; this plan uses Plan 66's capability table, dry-run view, guide lowering and recipe format.

Order:
1. CS-1 pins NKD on the worker.
2. CS-2 (timed prompts), CS-3 (guide phase) and CS-6 (signals) run in parallel.
3. CS-4 (curve audio guides) follows CS-3.
4. CS-5 (ControlNet) and CS-7 (LoRA phase) follow CS-2.
5. CS-8 adds the recipes and skill sections.
6. The final review.

[Task cards](tasks.md)

## Interfaces and handoff

**Consumes:**
- Plan 66's job, lever-kind table, dry-run view, guide lowering, recipe format and skills;
- Plan 64's reference rows and audio rule;
- NKD Basic Tools at commit `c157722a2b484d80dee6b6d3f166c90d9ec197b8`.

**Produces:**
- the timed `prompt` form;
- `phase` on guides (and on LoRAs, if proven);
- `role: control`;
- the curve tool;
- the per-tag binding report;
- recipes and skill sections for each;
- table rows with honest status.

## Completion

CPU tests prove each of these:
- A two-segment timed prompt serializes, in time order, into H3's timed shot format, and the dry run shows the final string.
- A guide with `phase: [0, 0.2]` compiles through NKD's MiniMax Guides with that `until`, at the right frame.
- The curve tool writes an audio file from an Event Curve recipe, and that file works as an audio guide at frame 0.
- A pose control video with `phase: [0, 0.6]` compiles to `MiniMaxH3FunControlNetApply` with matching start and end percent.
- `describe` shows each new kind's status.
- A LoRA `phase` either compiles through a proven hook, or is refused from the table as `unavailable`.
- For a two-speaker request, the dry run names which occurrence and soundtrack each `<Audio n>` tag is bound to, and marks per-actor binding as soft.
- Every recipe fills, dry-runs and compiles, and a small-model cold read reaches a dry run for the speech-timing recipe.

Review then closes the plan. How well timing, guides, curves and ControlNet are followed is judged in the owner's live test afterwards.
