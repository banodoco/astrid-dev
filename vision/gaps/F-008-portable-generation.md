# F-008 — Generation isn't yet one portable, extensible path across machines and inference engines

**Applies to:** [Eliminate needless technical wrangling](../principles/eliminate-needless-technical-wrangling.md) (primary) · [Local-first, cloud-capable](../principles/local-first-cloud-capable.md) (supporting) · [Open by design](../principles/open-by-design.md) (supporting) · [Agent-Powered Liquid Software](../pillars/liquid-software.md) (supporting) · **Assessment:** Partially evidenced; Plan 32 CPU proof, with hardware and extension proof still required (2026-11-10).

## Desired state

Any generation, in any modality (image, edit, video, voice, music, sound effects and composed workflows such as h3_av), runs through **one path**:
1. Declare what the request needs: custom nodes and models.
2. Choose where it runs once: this machine and a chosen local GPU, a user's own server, or a rented GPU machine such as RunPod. There is a default the creator sets and can change per generation.
3. Optionally bring that machine in line with the needs (align, only check, or trust what is there).
4. Run it on the chosen inference engine. ComfyUI through VibeComfy comes first; others such as Wan2GP follow.
5. Get the result back.

A rented machine behaves like any other machine: it runs the same path. It can be reused while warm, and it keeps models on attached storage so they are downloaded once. **Every level is a replaceable piece**, extended through a declared contract rather than a core change:
- **workflows:** a VibeComfy plugin adds templates such as h3_av;
- **engines:** ComfyUI, Wan2GP;
- **machines and providers:** local GPU, a user's server, RunPod, another rented-GPU provider.

Adding one reuses the rest of the path rather than adding per-modality or per-pack routes.

## Current state

- **The shared path has CPU evidence.** [Plan 32](../../plans/32-generation-placement-targets/plan.md)'s [task record](../../plans/32-generation-placement-targets/tasks.md) records the managed-local, attached and real shipped-job RunPod stand-ins, including h3_av, dry/live graph and manifest invariants, host preparation and explicit trust. Those results apply to the exact revisions named there. The [current integrated candidate](../../plans/32-generation-placement-targets/inputs.md#integrated-cpu-candidate-for-completion-review) is Agent `43ba77ccb609e0a6b26ed1e3f36fccda3ec31ff9`; reviewed repairs through literal pod-job routing and audio placement help have scoped passing CPU proof on the candidates and exact integrated head. Final-head CI comparison remains pending. The earlier i2v bootstrap heartbeat failure's cause remains unknown under Plan 34's liveness-family follow-up; same-marker altered imports before reset remain unproven.
- **Placement and the machine lifecycle are exercised on CPU.** The integrated work carries the chosen local device into launch and receipts, carries RunPod policy into admission and lease settlement, and caps retention at the disclosed paid bound. Progress, cancel, warm reset, mounted-cache checks and verified output retrieval have scoped CPU proof. This is no claim about a real GPU, real downloads or a real pod's volume.
- **h3_av is a workflow contribution.** The retired h3 route is removed; the core/SDK grep permits only the owner's unrelated HTML, channel and vendor-model literals. Real H3 node and GPU compatibility is [Plan 34](../../plans/34-real-gpu-proof/plan.md)'s proof.
- **Extensibility remains incomplete.** Wan2GP is not yet a proven second engine. The test machine's full facade/host route and the two remaining alignment implementations are explicit post-T8 follow-ups (Plan 32 F3/F4). The separate provider-API route also remains outside Plan 32.

The earlier path review and live attempts on 7–8 Nov are the baseline, not proof of this candidate: image and edit produced live outputs, while voice and music did not. Plan 34 supplies new hardware evidence against the exact revision it tests.

## Gap

The shared generation path is not yet proven to give the same real result across machines, and its workflow, engine and machine levels are not yet independently extensible end to end. Creators still lack qualified evidence that they can freely choose and change where generation runs, or which inference engine runs it, and get the same behaviour, setup and result every time. Distinct from [F-003](F-003-creative-execution.md), which is about one creative job being dependable end to end on a stated setup, and from [F-005](F-005-local-files-cloud-assist.md), which is about the local-data and cloud-execution product boundary.

## Closure evidence

**Same request, different machines.** The same generation request, for every default slot plus h3_av, produces its result through the same code path on:
- a local GPU;
- a user's own ComfyUI;
- a rented RunPod machine.

**Placement is one decision.** A default placement is set and overridden for a single generation.

**Rented machines are efficient.**
- A second job reuses a warm machine.
- Models already on attached storage are not downloaded again.
- Align, check and trust behave the same everywhere.

**Each level extends independently.**
- A second inference engine (Wan2GP) runs a generation through the same placement, lease and machine route, adding only its own setup and run step.
- A workflow added as a VibeComfy plugin (h3_av) runs with no plugin-specific code in Astrid's core.
- A further kind of machine or provider can be added behind the same placement and lease contract, shown at least with a test provider, without changing the path.

**One path in the code.** Source inspection shows one placement decision site, one submit and one retrieve, and no per-modality branch on the path.

**Negative cases:** a missing model fails before submit, naming the machine; an expired lease releases the machine; no orphaned machine remains.

## Closure approach

**The idea.** Generation is one short path with replaceable pieces. VibeComfy already knows what each workflow needs and how to set up and run ComfyUI. A rented RunPod pod is just another machine. So the strategy is to stop the controller from reaching into remote machines, and instead run the same local path wherever the work runs: declare needs, choose the machine once, align it if asked, run, and bring the files back. Each level then becomes a slot that can be extended without touching the others:
- workflows (`vibecomfy.workflows`);
- engines (`generation.engine`);
- machines and providers (`generation.machine`).

Each is a point in Astrid's existing pack extension protocol, which packs fill and can combine.

**Why this order.** Plan 33 supplies the short-term route and CPU characterization. Plan 32 replaces it with the shared path, also on CPU: placement is decided once, the pod runs the local path itself, each job declares its models, and h3_av is a workflow contribution. The owner's later direction puts Plan 34's first hardware pass on that path, instead of qualifying the route Plan 32 removes. Wan2GP and a second plugin then exercise the extension contracts. Plan 32's full-machine facade and alignment-consolidation follow-ups remain explicit work rather than evidence of independent extensibility.

**What creators notice at each stage.**
- First, the same request follows one path with a default placement the creator can override; CPU stand-ins establish the contract.
- Second, real-GPU proof establishes actual outputs on their own GPU, their own ComfyUI or a rented machine, with model-cache and warm-reuse evidence.
- Third, new engines and community workflows appear without Astrid changing its core.

**Deliberately out.** Out of scope: new cloud APIs (everything runs on our own compute), attaching a user-owned Wan2GP instance, multi-pass h3 requests, and Astrid-wide composability beyond generation ([LS-003](LS-003-full-stack-contributions.md), [LS-004](LS-004-cross-modal-foundations.md)).

## Route to closure

| Step | Plan | Contributes (closure evidence it delivers) | Milestone |
|---|---|---|---|
| 1 | [Plan 33](../../plans/33-unblock-live-generation/plan.md) | On RunPod: a warm machine reused, models on attached storage not re-downloaded, `--align check\|trust`, a missing model failing before submit and naming the machine | A: every default slot and h3_av produce results on RunPod |
| 2 | [Plan 32](../../plans/32-generation-placement-targets/plan.md) | The same request through the same path on managed-local, attached and RunPod CPU stand-ins; a default placement overridden per generation; align, check and trust; one placement site, one submit and one retrieve; h3_av as a workflow contribution; lease cleanup; a test machine exercising the contract below the facade | B on CPU: one path across placements |
| 1b / 2b | [Plan 34](../../plans/34-real-gpu-proof/plan.md) | Every default slot and h3_av on the Plan 32 path, proven with real outputs across placements, models downloaded once to the volume and a warm pod reused | A and B on hardware |
| 3 | [Plan 12](../../plans/12-multiple-inference-routes/plan.md) ∥ [Plan 17](../../plans/17-vibecomfy-extensibility/plan.md) | A second engine (Wan2GP) on the same path (Plan 12); the pack extension protocol switched on and proven with a second, non-h3 composite pack (Plan 17) | C: extensible at every level |
| — | unplanned | Full third-party machine facade/host proof (Plan 32 F3); one shared CLI/engine alignment implementation (F4, coordinated with Plan 12); provider APIs on the common placement path; paid consent once per lease rather than per job; VibeComfy owning ComfyUI's installation. Splitting the host file belongs to Plan 13, outside this closure evidence | — |

Critical path: Plan 33's CPU route → Plan 32's integrated CPU path and review → Plan 34's hardware proof. Plan 12 and Plan 17 use the Plan 32 contracts for a second engine and plugin. Independent extensibility also needs the named machine-facade follow-up; CPU evidence alone does not close this gap.

## Sources and reassessment

- **Path review:** `merge-run/path-review/` in `banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`: VISION, HOLISTIC, PLAN-SENSE-CHECK, H3-AS-VIBECOMFY-EXTENSION, EXISTING-MACHINERY and INFERENCE-ROUTES-SEQUENCING.
- **Related:** [Plan 25](../../plans/25-cloud-assist-v1/plan.md) reuses the result.
- **10 Nov CPU reassessment:** [Plan 32 task evidence](../../plans/32-generation-placement-targets/tasks.md) and [exact candidate/dependency identities](../../plans/32-generation-placement-targets/inputs.md#integrated-cpu-candidate-for-completion-review). Completion and hardware qualification remain separate claims.

Reassess from tested revisions and live runs, updating the assessment and the route as each plan lands. A plan alone does not close this gap.
