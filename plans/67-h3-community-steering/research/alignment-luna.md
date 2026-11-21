# Plans 64–66 → Plan 67 alignment check

**Scope:** Read-only contract and source review. No tests, GPU runs, machine claims, or repository edits. Plan snapshot: the astrid-dev plans at `aee9a968825f1c7a2efa5bf8e3c2b909da6a2833`.

## Finding

Plans 64–66 establish useful extension points, but do not yet provide an exact plug-in contract for every Plan 67 task. Plan 67 introduces at least four new public fields/semantics (`prompt` segments, `phase` on guides and adapters, reference `for`, and `role: control` with extra params), a third-party node pack, and a generated media tool. These need explicit schema, capability row, lowering, report, and provenance reservations. Several task cards already call for those changes, but CC-2/CC-3/CC-4/CC-9 need compatibility language so Plan 67 extends rather than revises their contracts.

## Plan contracts to check against sources

| Plan 67 need | Existing Plan 64–66 contract | Initial alignment question |
| --- | --- | --- |
| NKD MiniMax Guides and `until` | CC-4 lowers each guide through stock `MiniMaxH3AddGuide`; lever fields include `phase` in CC-2 but guide is then reserved/unavailable. | Can a guide carry denoising `phase`, and how can NKD preserve stock guide ordering/merge behavior? |
| Event Curve audio | CC-4 supports audio guide inputs; Plan 64 SR-5/Plan 66 audio rule define fixed/generated audio handling. | Does the output contract include the metadata needed to validate `fps`, length, sample rate, and frame alignment? |
| Fun ControlNet | CC-2 currently marks `control` unavailable; CC-1 declares mechanisms and model-chain dependencies. | Are control video/mask/source, VAE and start/end supported in the job and lowering contracts? |
| Timed prompts | CC-9 explicitly reserves reference-only tags; timed prompts are deferred to Plan 67. | Does CC-9 permit tag validation inside segments and resolve `during` on the same job clock? |
| Per-tag bindings | SR-3 effective reference rows; CC-3 view reports actual tag bindings. | Does the row/view reserve intended-character `for` while keeping it explicitly soft? |
| LoRA phase | CC-2 names `phase`; CC-1 adapter contracts and model chain; LoRA phase remains unsupported/unavailable. | Does the adapter schema/table/view allow phase and a proven scheduled hook without schema reshaping? |
| NKD pin | Plan 67 says add to worker recipe or node set and VibeComfy object-info cache. | Verify actual pinning home and whether worker declaration, schemas, and provenance have a generic node-pack slot. |

## Detailed source findings

Source-level results and the consolidated reservations follow.

## Plan contract findings (67 tasks 3–7)

These are contract-level findings from a read-through of the plan cards; see the source review below before treating implementation behavior as established.

### 3. Fun ControlNet

CS-5 needs `role: control` with `asset`, clip-time `during`, `strength`, denoising `phase`, optional `mask`, and `params.source/type`, plus conform-to-canvas/24-fps behavior and an H3 patch in the model chain (67 `tasks.md:17`). CC-1's declared lowering mechanisms, model chain and adapter contracts provide a plausible hook; CC-2 explicitly reserves a `control` kind, `phase`, `params`, source references and unavailable/refusal status (66 `tasks.md:23`, `46–71`). CS-5 must replace the unavailable row with per-supported-type rows and weight-file provenance; the mere node interface does not prove arbitrary control weights work (67 `research/extension.md:11,17`).

Reserve explicitly: control-source trim and clock mapping; source video and mask semantics; VAE ownership; capability rows for weights; chain ordering when a Character Swap adapter and control patch coexist; dry-run reporting of effective source span/conformance and patch params. Current gap: CS-5 says `during` and video conformance, while source evidence describes source-time alignment; CC-1 doesn't spell a control-specific source-clock transform. Another ambiguity: adapter order is fixed in CC-1, while CS-5 says adapter and control are in “declared order”; specify whether/where the control patch participates in that order.

### 4. Timed prompts

CS-2's list of `{during,text}` builds on CC-9's time expressions and reference-only tags, and is explicitly deferred by CC-9 (66 `tasks.md:25`; 67 `tasks.md:14`). The timed shot convention remains soft: no frame isolation is promised (67 `plan.md:24`, `research/extension.md:18`). Reserve in CC-3's persisted resolved-job view the authored and resolved span for each segment, stable ordering, and final serialized prompt; CS-2 already requires tag validation inside segments. Validate tags after normalization against effective emitted reference rows, not just tag syntax (64 `plan.md:46`; 66 `tasks.md:24,283`).

### 5. Per-tag / per-character binding report

Plan 64 SR-3 defines one ordered effective reference-row list shared by builder, compilation, dry run and receipt; SR-3 identity follows emitted node order, including soundtrack bindings (64 `plan.md:46`, `tasks.md:15`; 64 `inputs.md:34–45`). CC-3 already extends the same persisted view with occurrence-level actual tag binding, modality, purpose, mechanism and resource report (66 `tasks.md:24`; binding rules `66 tasks.md:281–283`). CS-6 adds nullable `for` to typed reference occurrences and an advisory prompt association warning (67 `tasks.md:18`). Reserve `for` in the normalized occurrence and sealed/readback row; keep it advisory, never a refusal. Resolve ambiguity: if a video occurrence contributes an `<Audio n>` soundtrack tag, does its `for` label inherit, or can the paired audio label differ?

### 6. LoRA phase

CC-2 already exposes `phase` and LoRA kind as a capability row but marks phase unavailable; CC-1 models adapter LoRAs in the model chain and records adapter contracts (66 `tasks.md:23,46–71`). CS-7 properly permits either a proven lowering or an unavailable refusal (67 `tasks.md:19`). Reserve `settings.adapters[].phase` specifically, document its mapping to start/end on the pinned hook and keep adapter order and sampler path stable. If unsupported, preserve the CC-2 pre-claim refusal with a source reference and reason. No broader schema gap is apparent.

### 7. NKD pinning

CS-1 asks for a commit pin in the worker recipe/node set and VibeComfy cached object-info entry (67 `tasks.md:13`); owner decision says not to vendor GPL-3.0 source into astrid-agent (67 `inputs.md:41–45`). The actual pin paths, hard-coded runtime list, lock synchronization, workflow metadata, cache indexes and licence-record gap are detailed under “Node-pack pin and cache provenance” below.

## Pinned node source findings (items 1–2)

### 1. NKD MiniMax Guides versus CC-4

At ComfyUI `6bfaacc`, stock `MiniMaxH3AddGuide` appends one keyframe dict to `conditioning["minimax_keyframes"]`, preserving the prior list. Its keyframe stores resolved frame index and optional image/audio latents; it has no denoising interval or per-keyframe phase input (ComfyUI `comfy_extras/nodes_minimax_h3.py:151–218`, especially `200–217`). Therefore CC-4's stock per-guide chain preserves merge order but cannot make any keyframe active only during a denoising phase.

NKD `NKDMiniMaxGuides` does not add a timestep field to those keyframes. It calls stock AddGuide to reuse encoding/validation, merges same-frame image/audio guides, rejects duplicate same-frame media of the same type, and schedules guide groups by splitting the denoising schedule into conditioning stretches (`nkd_minimax_guides.py:17–38,61–129,141–221`). Each stretch contains the active keyframes and its `start_percent`/`end_percent`; its `until` is thus schedule gating, not metadata the H3 core reads from a keyframe. Its frame-group ordering follows first occurrence in declared slots, while within a frame it follows slot order; optional snap is to a 17-frame lattice except the last frame (`141–190`).

**Reservation / mismatch:** CC-2 already reserves `phase` and a guide capability row, initially unavailable (`66 tasks.md:23`), which is the right schema home. CS-3 must route the complete relevant guide set through NKD (or equivalent conditioning-stretch lowering) whenever phase is used; simply passing `phase` through CC-4's chained stock keyframes cannot work. Preserve declared/effective order and define same-frame merge, duplicate rejection, and snap policy. For unphased rows mixed with phased ones, define whether the single NKD call includes them with `until=1`; retain the stock path when no phase is present. Plan 67's restriction to phases beginning at zero matches NKD's exposed `until` shape, but not a general `[start,end]` phase.

### 2. Event Curve audio versus CC-4 and VAE

The pinned NKD Event Curve output is an `AUDIO` object with waveform `[1,2,T]` and `sample_rate: 32000`, plus a preview; it derives seconds from `length / fps` and rounds generated sample count (`nkd_event_curve.py:207–228,261–341`). CC-4's stock guide accepts audio, runs it through the audio VAE, then crops the encoded guide to remaining 40 Hz audio ticks and errors if the guide starts past the end (ComfyUI `nodes_minimax_h3.py:67–74,204–217`). So the produced audio is structurally suitable as an ordinary audio guide at frame 0; preserve requested `length`/`fps` (or seconds) and resulting sample duration through managed-asset admission and the dry-run row so frame/tick cropping is explainable.

**Inconsistency:** CS-4 specifies a saved file with requested duration at **48 kHz** (67 `tasks.md:16`), while NKD's node output is **32 kHz**. Choose and state whether the wrapper resamples on managed-asset write (and report the conversion) or preserve 32 kHz and correct the acceptance contract. Separately, Event Curve's own input named `phase` is a periodic curve offset, not the denoising `phase` field introduced for guides/LoRAs; name and document these clocks distinctly. The W-guide mode is synthetic speech-like muffled syllables, not intelligible text (`nkd_event_curve.py:190–205`), consistent with Plan 67's soft-cue framing.

## Node-pack pin and cache provenance (item 7)

The Plan 67 phrase “worker recipe or node set” is not enough to identify all synchronized homes. At `origin/release/14/main`, `astrid/packs/runpod/pins.json:9–23` pins ComfyUI and H3 motion pack; `astrid/packs/vibecomfy/pins.json:4–18` repeats those pins. The canonical worker recipe `astrid/packs/runpod/recipe.linux-cu130.json:5–7,9–39` maps source pins to checkouts; `environment.linux-cu130.json:10–24,29` currently lists only H3 and VHS under `custom_nodes`; `h3_release.py:60–72` reconstructs the runtime custom-node list from H3 and VHS explicitly. Thus adding only a pin entry is insufficient: include NKD in recipe source-to-checkout binding and release-input/runtime custom-node assembly, or replace that hard-coded adapter.

VibeComfy's `custom_nodes.lock` is another pin source: the H3 record is `astrid/packs/vibecomfy/custom_nodes.lock:31–40`, and the worker recipe pins the lock SHA at `recipe.linux-cu130.json:77–80`. `h3_release_remote.py:146–172` checks out recipe sources and cross-checks revisions against the lock; `worker_staging.py:163–194,274–280` verifies lock digest/commit/root and selected workflow requirements against a manifest-pinned checkout. Workflow metadata also declares `custom_node_packs` (e.g. `astrid/packs/h3_av/workflows/native_h3_continuation/workflow.py:63`); VibeComfy resolves metadata `custom_node_refs`/`custom_node_packs` into repository+commit requirements (`comfyui_engine.py:149–177`) and lock resolution (`:93–107,127–128`). Plan 67 should state whether NKD graphs declare this requirement, and if so, reserve this workflow-level contract as well.

The cache precedent is one per-pack object-info JSON plus entries in both `porting/cache/object_info/index.json` and `provenance.json`: H3 source provenance is in `provenance.json:106–113`; discovery uses index mapping (`porting/wrappers/discovery.py:7–16,120–145`). The current cache search did not find NKD class entries. Therefore CS-1 must include schema hash, locked commit and source kind, not merely add a JSON file. Existing lock/cache provenance has no GPL licence field (H3 lock record and provenance above); specify where the required GPL-3.0 attribution is recorded.

## Control node source check

The pinned cached ComfyUI schema (`comfy_core@cpu-runtime.json`, node records stamped with commit `6bfaacc67c2103481e5f0c84d75257cd0581d86a`) confirms the Fun ControlNet signature. `MiniMaxH3FunControlNetApply` requires model, model patch, VAE, strength, `start_percent`, and `end_percent`; optional inputs are `control_video: IMAGE`, `mask: MASK` (1 marks regeneration), and `source_video: IMAGE` (used only with a mask) (`58945–59164`). It returns a patched `MODEL` (`59154–59159`). This matches CS-5's basic lowering but means the model-chain mechanism must preserve the patched model output into the sampler, and `source` should map to `source_video`, while control video and source video remain distinct public roles. Strength is bounded 0–10, phase endpoints 0–1. Schema existence proves interface shape only, not compatibility of named weights/types; each supported type needs a pinned model source and admission row.

## Consolidated reservations before Plan 67

1. **Request schema and normalization:** `guide.phase` as denoising progress (reserved, unavailable in CC-2); `settings.adapters[].phase` (same clock); `role: control` with distinct control asset, optional mask/source, type and source-time span; `prompt` as string-or-segment list; nullable reference `for` label. Ensure JSON schema and normalized job carry these fields with pre-claim unsupported refusal.
2. **Lowering contracts:** guide schedule/stretches (not per-keyframe range); deterministic guide order/merge/snap policy; Fun patch VAE and control/source/mask mapping plus chain placement; scheduled LoRA hook only if evidenced. Define phase interval support and refusals.
3. **Time and asset contracts:** timed prompt spans resolve on job clock, retain tags and serialize deterministically; control input trim/conformance carries its own measured source clock; Event Curve output records `fps`, frame `length`, seconds, sample rate and resampling policy. Distinguish curve-shape `phase` from denoising `phase`.
4. **Capability and report contracts:** CC-2 rows and refusal pairs for each control type, guide phase, prompt segments, and conditional adapter phase; CC-3 persisted resolved view contains prompt segments/final string, each guide's phase and actual schedule semantics, control source/patch details, and `for` beside actual tag/occurrence/soundtrack binding. Character association stays soft/advisory.
5. **Dependency/provenance contract:** NKD must be pinned consistently in pack pins, worker recipe checkout map, runtime custom-node list, VibeComfy lock, workflow requirement metadata (if used), and object-info JSON/index/provenance; specify durable GPL-3.0 record location.

## Plan 65 boundary

Plan 65 contributes one resolved `GenerationInputs.canvas`, source conform to that canvas, static mask rasters at target size, and size in the retained/dry-run record (65 `plan.md:21–46`; `tasks.md:13–16`). This is enough for CS-5's requested canvas conform target and optional static mask dimensions in principle. It does not define a general control-video/source-video clock-conform contract: DS-2 explicitly preserves timing, while moving masks keep the prepared source's size and same clock (65 `plan.md:25–29`). CS-5 must state control-video fps/frame-count alignment independently. Plan 65's canvas record need not be reshaped.

## Verdict

**No: Plans 64–66 provide extension points, not exactly the contracts Plan 67 consumes.** The main structural model is reusable, and CC-2 already reserves unavailable `phase`/`control`; CC-3 and SR-3 already provide the correct shared binding view. Before dispatch, clarify or amend the reservations listed above: schedule-aware guide lowering and ordering, 32-vs-48 kHz curve output, control source clock and chain order, timed-segment/result serialization, `for` inheritance for paired soundtracks, conditional LoRA phase, and every NKD pin/lock/runtime/cache/licence home. None requires replacing the resolved-job architecture, but these details avoid schema/view/worker reshaping.
