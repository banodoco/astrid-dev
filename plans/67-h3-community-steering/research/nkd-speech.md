> Historical research, not instructions. Where this differs from the current plan, inputs or tasks files, those win.

# NKD Basic Tools speech scheduling and Astrid's lever model

_Read-only source review, 18 November 2026. NKD Basic Tools commit `c157722a2b484d80dee6b6d3f166c90d9ec197b8`; official H3 implementation at `Comfy-Org/ComfyUI@6bfaacc`, `comfy_extras/nodes_minimax_h3.py`. Source/docs only: no node execution or rendered-output claim._

## Summary

NKD has two relevant nodes: **NKD Event Curve** draws or derives a clip-time envelope and synthesizes an audio guide; **NKD MiniMax Guides** packages that guide with optional image/video/audio guides and controls when during sampling each guide is active. There is no node that schedules transcript words or supplies a real spoken line with word-level timestamps.

The `W Guide (words)` mode synthesizes muffled, syllabic speech-like audio. It does not contain the requested line. The curve controls pauses and syllable rate. H3 may use that cue to place an event it infers from the prompt, but this is soft model conditioning. MiniMax Guides' `until` is denoising progress, not clip time. The docs describe intent and an example workflow, but no measured dialogue timing or fidelity evidence was found.

For Astrid, use timed prompt segments as Context that lower to prompt text; use the existing audio `guide` kind for a generated waveform, lowering to H3 timed rows. Event Curve itself is a tool that makes an input, not a lever. This does not need a new mechanism or a “speech” lever kind. Plan 66 already limits CC-9 to serializing timed text into H3's own prompt format and expressly excludes Event Curve and vendored GPL nodes, so keep this extension for a later plan unless Plan 66's owner changes scope.

## Source identity and evidence

- NKD HEAD was resolved by `git ls-remote`: `c157722a2b484d80dee6b6d3f166c90d9ec197b8`.
- Relevant implementation: `nkd_event_curve.py`, `nkd_minimax_guides.py`; docs: `docs/event-curve.md`, `docs/minimax-guides.md`; example named by docs: `example_workflows/NKD H3 Event Control.json`.
- License: NKD README identifies GPL-3.0 (`README.md:185`; `LICENSE`).
- The request pins official H3 code to `6bfaacc`; the keyframe/audio conditioning behavior is in `comfy_extras/nodes_minimax_h3.py`.

## Nodes and what they produce

### 😺NKD Event Curve (`NKDEventCurveAudio`)

**Inputs** (`nkd_event_curve.py:300-334`): `guide` preset (P punch, F flow, M motor, B blast, U uncanny, W words); `shape` (custom or periodic); `cycles`; `phase`; `length` in frames; `fps`; `strength`; editable `curve`; preview width/height; optional `source` audio or image/video. The source path derives an envelope from audio loudness or video motion; otherwise it uses the drawn or periodic curve (`:345-360`).

**Outputs** (`:336-342`, `:360-365`): stereo audio `guide` waveform at the node's sample rate, plus `preview` frames showing the curve/playhead. The audio is synthesized from the curve; W is a buzzing, muffled voice with syllabic pulses, not a transcript or voice recording (`:209-224`). At higher curve values its syllable rate increases; zero regions create pauses (`:210-224`).

The code's intent says to anchor the guide at frame 0 so the prompted event lands where the curve is high (`:1-8`). The docs recommend W with low `until` “around 0.2” (`docs/event-curve.md:32-34`) and identify an H3 Event Control example workflow (`:44-46`). The source says pure tones were followed poorly and broadband noise reliably (`nkd_event_curve.py:24-25`), but offers no measurements or speech-onset benchmark. The included `example_workflows/NKD H3 Event Control.json:2445-2449` explicitly tells users to put phrases in the prompt; its note at `:2744-2749` describes W as oscillating pitch/speed and suggests a low timestep guide (0.30) to affect only early steps. That is direct evidence of intended use, while also confirming the waveform is a timing cue rather than the line itself.

### 😺NKD MiniMax Guides (`NKDMiniMaxGuides`)

**Inputs** (`nkd_minimax_guides.py:82-107`, `:110-129`): positive conditioning; video VAE; audio VAE; H3 latent; `snap_positions`; an autogrowing list of optional guide slots accepting image, audio, or video; each slot has `position_i` (frame, negative from end) and `until_i` (0..1 fraction of sampling steps). Snapping defaults on and targets H3's 17-frame token starts (`:93-101`, `:110-117`). `until=1` keeps a guide throughout sampling; lower values stop conditioning earlier (`:122-128`).

**Outputs** (`:131-136`): updated positive conditioning, latent, video VAE, and audio VAE. The implementation anchors each guide through official `MiniMaxH3AddGuide`, gathers keyframes, then `_schedule`s conditioning stretches so a guide disappears after its `until` denoising fraction (`:192-203`, `:211-235`). Guides at the same position may combine; docs say sounds there are mixed (`docs/minimax-guides.md:27-33`).

### Official H3 lowering (`nodes_minimax_h3.py`)

`MiniMaxH3ImageToVideo` takes clip, VAE, prompt, size, length, and optional first/last image; it returns positive conditioning and AV latent (`:125-135`). It calls `clip.encode_from_tokens_scheduled` for prompt text (`:155-156`) and attaches boundary images as `minimax_keyframes` (`:142-162`).

`MiniMaxH3AddGuide` takes positive conditioning, latent, optional video/audio VAEs, optional image/audio guide, and `frame_idx`; it returns positive conditioning (`:165-187`). It encodes image and/or audio, crops audio to remaining clip duration, and adds the resulting latent(s) under a keyframe at the resolved frame (`:212-239`). H3's module description says keyframe/reference condition latents are re-injected every step and are never denoised (`:1-9`): this is model conditioning, not exact pixel/sample ownership.

## Does it schedule when words are spoken?

It schedules a **speech-like audio envelope in clip time** if the curve is authored to have silent and active regions and anchored at the clip's beginning. The waveform itself is the cue: it is not real dialogue. A prompt can name a line and describe when it should occur, but neither NKD node creates per-word prompt timestamps or enforces text/audio alignment.

Do not confuse two clocks: Event Curve's curve and generated waveform cover clip time (`length`/`fps`); MiniMax Guides' `position` anchors that waveform in clip time; `until` controls the fraction of denoising steps for which the guide stays active. `until=0.2` means early sampling influence, not “start the line at 0.2” or “speak at 2 seconds.”

Evidence for quality is limited to author-described intent, a workflow example, and qualitative implementation comments. NKD says broadband noise was followed more reliably than low pure tones; it provides no measured success rate, dialogue onset deviation, word intelligibility, voice identity, lip-sync, or comparison. H3 source confirms the conditioning path, not adherence. Do not describe the result as reliable word scheduling without a live evaluation.

## Example: still master, line at 2–4 seconds in a 6-second shot

For an exact start still, use a timeline/start image at frame 0. For a still intended only as a mid-shot visual anchor, use a guide at its frame; that remains soft. Put the six-second duration and timed prompt segments in the request: silence/setup over 0–2, the quoted line over 2–4, reaction over 4–6. Add an audio voice reference if desired, tagged in prompt text. If adding NKD's W cue, draw a curve with zero envelope for 0–2, active envelope for 2–4, zero for 4–6, set its duration/fps to the clip, and anchor its output at frame 0 in MiniMax Guides. Optionally lower `until` to let the guide affect only early denoising. This still only biases when H3 places the prompted speech-like event; it does not supply the words or guarantee the line timing.

Astrid lowering across the six mechanisms:

| Item | Lever/family | Mechanism |
|---|---|---|
| Exact start still | place / Output | latent write + ownership mask; composition restores it |
| Mid-shot still | guide / Context | timed rows (`minimax_keyframes`) |
| Voice sample | reference / Context | untimed rows, referenced by its prompt tag |
| Timed dialogue and silence/react beats | timed prompt / Context | prompt text (serialized into H3's timed shot convention) |
| Event Curve editor/synthesizer | tool, not lever | makes an audio waveform input |
| Curve waveform | audio guide / Context | timed rows; H3 encodes `audio_latent` at the guide index |
| Optional mouth/audio edits on existing footage | edit grant / Output | latent + ownership mask, then composition |
| Seed/steps/etc. | Process/settings | sampler |

No new mechanism is needed. The speech-specific timing syntax is a prompt form/kind if the capability table requires kind-level declarations; the audio guide remains the existing guide kind. If strict word onset is required, it does not fit any current H3 lever lowering or exactness promise.

## Other combinations and their lowerings

1. **Speech timing plus mouth-mask redub.** Place the source clip; grant video edits inside the mouth mask and an audio edit over the line interval; provide voice reference and timed line prompt. The grants and source feed latent/ownership mask and composition; voice reference feeds untimed rows; line feeds prompt text. A mask maker/tracker is a tool. Only pixels/samples outside the grant are exact. Plan 64 already describes this route and explicitly leaves voice likeness/lip sync to later live judgment (`plans/64-h3-speaker-references/plan.md:21-26`, `:56-61`).
2. **Speech during continuation.** Place the prefix clip, generate the uncovered tail, serialize speech/action segments in the timed prompt, optionally add audio guide after or from the seam. Placement lowers to latent/mask; prompt to text; guide to timed rows. The speech timing remains soft. Continuation is Plan 66 phase 2; don't add chain orchestration or claim exact dialogue onset.
3. **Two speakers alternating.** Put each voice sample in a separate audio reference row; use tags in ordered timed prompt segments to assign each line; optionally place two audio guides at their event starts. References lower to untimed rows, speech guide(s) to timed rows, and dialogue to prompt text. No source evidence guarantees correct speaker turns or absence of overlap; this is a recipe to evaluate, not a promised capability.

## Recommendation and plan fit

Plan 66's lever model already accommodates the useful parts: guide role and timed rows, references, timed prompt text, edit grants, and six fixed mechanisms (`plan.md:31-40`). CC-9 is specifically end-relative time and timed prompts (`:67`, `:93`); the scope excludes timed prompts beyond serialization into H3's own timed format, Event Curve, and GPL node vendoring (`:70-78`). Plan 64 also excludes dialogue lines as their own request piece and new Comfy nodes (`plans/64-h3-speaker-references/plan.md:28-34`).

Keep the Plan 66 core within that boundary. Recommend a later, small capability/recipe plan for evaluating timed dialogue prompts plus optional generated audio-guide tooling/input provenance. Reuse the existing `guide` lever kind for audio guides; do not create a separate “speech schedule” family/kind just because the tool is speech-oriented. Make Event Curve a tool that produces an asset, as the existing Astrid lever research says of curve→audio (`plans/66-h3-composable-core/research/levers.md:20-23`, `:67`, `:85`). Hard word timing remains unavailable unless a future lowering actually enforces it. If desired before Plan 66 closes, revise its explicit exclusion and acceptance proof rather than silently expanding CC-9.

NKD is GPL-3.0. Do not vendor or copy its source into Astrid without a deliberate license decision; reimplementing the abstract behavior from independently stated requirements is the safer route under Plan 66's current exclusion. Reusing NKD as an external ComfyUI dependency is a separate distribution and compatibility question and still needs license review.

## Limits

This report is source/docs research only. It establishes the node contracts and intended conditioning path, not the quality of generated media on any machine. The NKD workflow is illustrative documentation, not empirical validation.
