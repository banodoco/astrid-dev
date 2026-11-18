# Levers: one abstraction for everything that steers an H3 job

Design note, read-only, 18 Nov 2026. No implementation, nothing run. Built on `mc-1.md`, `mc-2.md`, `mc-3.md`, `restrictions.md` and the current Plan 66 text. Where a mechanism is unverified for H3, I say so.

## The short answer

**Yes, there is one lever concept, and the plans are one family short.** An H3 job is a sampler turning noise into a latent while a model looks at some context. There are only three things you can touch, so there are three families of lever:

| Family | It sets | Its clock | Can it be exact? |
| --- | --- | --- | --- |
| **Output** | what is in the latent and how free each cell is to change | clip time, plus region | Yes. Only this family can promise pixels and samples, because composition restores them. |
| **Context** | what the model looks at while it generates | clip time, or none | No. Always an influence. |
| **Process** | how the model and sampler run | sampling progress, or none | No. Always an influence. |

The coordinator's three mechanisms are the first two families (latent plus mask is Output; guide rows and reference rows are both Context). **Process is the missing family:** adapters, ControlNet, shift and anything else that changes the model or sampler belong to it, and it is the only family that runs on the second clock, sampling progress. So the missing axis and the missing family are the same gap seen twice.

Three smaller things were also missing:

1. **Force is not an axis.** "Soft versus exact" falls out of the family. Exactness exists only for Output. Everything else has a strength and nothing more. That removes a choice the agent would otherwise have to reason about.
2. **Not everything is a lever.** Event Curve is a tool that makes an audio file; the lever is the guide that uses it. Mask makers, voice-first takes and transcripts are the same. Keeping "tools that make lever inputs" separate from "levers" is what keeps the lever list short.
3. **The unit of extension is a lever kind, not a limit.** The capability table today is a list of limits. It should be a list of kinds, each carrying its limits.

## 1. The abstraction

### A lever has a kind and at most seven fields

| Field | Meaning | Who uses it |
| --- | --- | --- |
| `kind` | which lever | all |
| `id` | a name other things can point at; the prompt tag (`<Picture 1>`) is derived from it | all |
| source | an asset, text, or nothing | most |
| `stream` | video, audio or both | most |
| when | a span or point on **clip time** | Output, timed Context |
| where | a region of the picture | Output; ControlNet |
| `phase` | a span of **sampling progress**, 0 to 1 | Process; possibly Context later |
| `strength` | how hard it pulls: a number, later optionally a curve along the lever's own clock | all |

No kind uses all of them. Each kind declares which it accepts. An agent learns the field names once; a new kind reuses them.

### Keep and regenerate are one lever

They are the two ends of one value. Per stream there is one **ownership map** over time and region, from 0 (kept) to 1 (free):

- placing an item writes its content and sets its span to 0;
- a grant raises the value inside a placed span;
- time nothing covers is 1.

This is exactly the model's noise mask, and `mc-2.md` confirms the masked-context nodes and the V2V node are the same latent-plus-mask mechanism with different preparation. They need two **verbs** in the request, because placing brings an asset and granting does not, but they are one lever and compile to one mask.

A placed item is also the strongest context there is: the model sees the kept frames while it generates the rest. That is why continuation works. So one asset has three possible attachments, in falling force:

**place** (in the output, exact) → **guide** (a timed row, soft) → **reference** (an untimed row, soft).

That single ladder is the heart of the request, and Plan 66 already has it as `role: timeline | guide | reference`.

### Every known lever fits

| Lever | Family | Source | When | Where | Phase | Lowers to | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Keep (placed clip, still, audio) | Output | asset | span | whole frame | no | latent write, mask 0, composition paste | planned |
| Regenerate (grant) | Output | none | span | region | no | mask above 0 (video per frame and region; audio per tick) | planned |
| Reference | Context | asset | none | no | no | `MiniMaxH3ReferenceToVideo` row and tag | Plan 64 |
| Guide (image, clip, audio) | Context | asset | point | no | no | `minimax_keyframes` row via `MiniMaxH3AddGuide` | CC-4 |
| Motion context (the guide node) | Context | clip with audio | point | no | no | the same `minimax_keyframes` rows, AV-aligned | same kind as guide; a second lowering if needed |
| Event Curve | not a lever | curve → audio file | | | | a tool; its output is an audio guide | later |
| Prompt | Context | text | none | no | no | text encoder | exists |
| Timed prompt | Context | text | span | no | no | see below | later |
| Adapter (LoRA) | Process | weights | no | no | possible | model chain | planned; `phase` unverified |
| ControlNet range | Process | control video | whole clip | mask | start and end percent | `MiniMaxH3FunControlNetApply` | later |
| Audio-shift curve | Process | none | no | no | curve over progress | model patch on the audio shift | later |
| Seed, steps, sampler, shift | Process | none | no | no | no | sampler nodes | exists as `settings` |

Notes on the ones that needed thought:

- **Timed prompt.** The model's own prompt format is already timed: the official guide writes shots as `[Shot 2] At 00:03.000, …`. So the first lowering of a timed prompt is to serialize the segments into one structured prompt. That is a documented convention, not frame isolation, and untested here. A harder lowering (conditioning chosen per sampling window) could replace it later without changing the request.
- **Adapter with a phase** ("LoRA only for the first 60%"). ComfyUI has scheduled LoRA hooks in general; whether they work with the H3 model class is unverified. The grammar has the field; the adapter kind does not accept it until a lowering is proven.
- **ControlNet** is the one hybrid: it takes an asset aligned to clip time, like Context, but is applied as a model patch over a progress range, like Process. It does not matter which family it is filed under; it declares the fields it accepts (source, where, strength, phase).
- **Scalar settings** stay in `settings`. Rule of thumb: something is a lever if you can have several of it or scope it; it is a setting if a job has exactly one. A setting becomes a lever on the day someone needs a curve or a range for it (audio shift).

### What does not fit, and should not

- **Multi-pass work:** upscaling passes, chains, endless continuation. These are sequences of jobs. They belong to skills.
- **Tools that make inputs:** Event Curve, masks, a voice-first take, transcripts.
- **Prompt structure.** The structured prompt the model was trained on (`subject_definitions`, `retention_analysis`, …) is a template concern. It links levers to text through their tags, which is why every lever needs an `id`.
- **The base checkpoint.** One per job; a setting.

## 2. In the request

**Recommendation: keep the v2 shape Plan 66 already has, and make the field names uniform.** Do not rewrite it into one flat `levers:` list. The existing shape already puts each lever where an agent expects it, and a new kind lands in an existing place:

| Where in the request | Holds | A new kind here is |
| --- | --- | --- |
| `media[]` with `role` | every lever with an asset: `timeline` (place), `guide`, `reference`; later `control` | a new `role` |
| `edit[]` on a placed item | grants | (none expected) |
| `prompt` | text; later a list of `{during, text}` | (same field, list form) |
| `settings.adapters[]` | model levers | a new adapter row |
| `settings` | one-per-job values; later a value may be a curve | (same key, curve form) |

The uniform names, used the same way everywhere they appear: `at` (a point), `during` (a span of clip time), `range` (a trim of the source), `mask` (a region), `stream`, `strength`, and one reserved name, `phase` (a span of sampling progress).

### Examples

Field spellings follow Plan 66. `phase` and the list-form prompt are the reserved extensions and are marked.

**A. Recast a line in the shot's own frames, in the speaker's voice.** Place, grant, reference.

```yaml
version: 2
prompt: 'He says, "You have two options." in the voice of <Audio 1>.'
media:
  - {id: shot, asset: morpheus.mp4, role: timeline, at: {frame: 0}, range: [0, 3],
     edit: [{stream: video, during: [0, 3], mask: {asset: mouth.png}},
            {stream: audio, during: [0.5, 2.5]}]}
  - {id: voice, asset: morpheus-voice.wav, role: reference}
settings: {seed: 7}
```

**B. Exact start, guided end, speaker reference.** Place, guide, reference.

```yaml
version: 2
duration: 5
prompt: "The man in <Picture 1> turns to camera and speaks in the voice of <Audio 1>."
media:
  - {asset: start.png, role: timeline, at: {frame: 0}}
  - {asset: end.png,   role: guide,    at: {frame: -1}}
  - {asset: face.png,  role: reference}
  - {asset: voice.wav, role: reference}
settings: {seed: 7}
```

**C. Bridge two real shots, with a rhythm guide made by a tool.** Two places, a gap, an audio guide.

```yaml
version: 2
duration: 8
prompt: "He crosses the room and sits."
media:
  - {asset: shot-a.mp4, role: timeline, at: {frame: 0},   range: [10, 11.625]}
  - {asset: shot-b.mp4, role: timeline, at: {frame: 153}, range: [0, 1.625]}
  - {asset: footsteps-curve.wav, role: guide, modality: audio, at: {frame: 39}}
settings: {seed: 7}
```

**D. Character swap, with a second adapter early in sampling only.** Adapters, reference, placed performance. `phase` is reserved; today the adapter kind would refuse it.

```yaml
version: 2
prompt: "Replace the man in <Video 1> with the character in <Picture 1>."
media:
  - {asset: performance.mp4, role: reference, modality: video}
  - {asset: old-man.png,     role: reference}
settings:
  adapters:
    - {id: character_swap_v1, strength: 1.0}
    - {id: film_grain, strength: 0.8, phase: [0, 0.6]}   # reserved
  seed: 7
```

**E. Continue a take, with the action timed in the prompt.** Place, uncovered time, timed text. The list form is reserved.

```yaml
version: 2
duration: 9
prompt:                                   # reserved list form
  - {text: "A man at a desk, evening light."}
  - {during: [4, 6], text: "He stands and walks to the window."}
  - {during: [6, 9], text: 'He says, "Let''s go."'}
media:
  - {asset: take-03.mp4, role: timeline, at: {frame: 0}, range: [0, 3.75]}
settings: {seed: 7}
```

All five are one shape. None names a method.

## 3. How it is extended

### What a lever kind declares

One entry per kind, in the capability table:

| Declared | Example for `guide` |
| --- | --- |
| `kind` and family | `guide`, Context |
| Accepted fields and sources | image, clip or audio asset; `at` required; no `mask`; no `phase`; no `strength` (the node has none) |
| Limits, each with its source | clip lengths 5, 22, 39 … frames (node); must fit from its index (node) |
| Requires / conflicts | needs the video VAE for pictures and the audio VAE for sound; warn if it sits wholly inside a kept span |
| Mechanism it merges into | the timed-rows list |
| Lowering | the function name, the node classes, the pinned pack and commit |
| Dry-run line | `guide end.png → frame 119 (soft, image)` |
| Status | `compiles` / `live-tested` / `unavailable`, with a date |

An adapter row adds what Character Swap needs: base model, default strength, required references by tag, prompt template, tested sampler settings.

**Where it lives:** the one table Plan 64 SR-2 creates and Plan 66 CC-2 extends, in the H3 pack beside the lowering functions. Adding a lever is one table entry, one lowering function, and one template. No registry, no plugin loader, no class hierarchy.

### How levers compose

Levers never compose with each other directly. Each lowers into one of six **mechanisms**, and each mechanism has one merge rule. This is the whole compiler:

| Mechanism | Fed by | Merge rule | Conflicts |
| --- | --- | --- | --- |
| Latent and ownership mask (one per stream) | places, grants | write each placed item at its span; mask is 0 on kept spans, the grant strength elsewhere it is granted, 1 on uncovered time; overlapping grants take the maximum; spans snap to H3's time chunks | two places owning the same stream and span |
| Timed rows (`minimax_keyframes`) | guides | append in request order | a clip that does not fit from its index |
| Untimed rows | references | fixed node order (images, videos with their soundtracks, audio); tags derived from that order | slot counts 9 / 3 / 3 |
| Text | prompt, timed segments | one string; segments serialized in time order | a tag no row has |
| Model chain | adapters, control | applied in request order | two base models; an adapter's required references missing |
| Sampler | settings | one value each | two values for one setting |

After sampling there is one more fixed step: **composition** restores every kept pixel and sample from its source. That step is why Output can promise exactness and nothing else can.

Rules across mechanisms are few and all declared on a kind: an adapter's required references; the one-seed, one-reference-set fact of a single pass; and cost (reference rows ride every step, so the dry run should show the row count).

## 4. How an LLM finds and uses them

- **`describe --entry h3 --json`** returns the kinds, straight from the table: for each, its family, accepted fields, limits with sources, status and one example line. This is the "list of levers to pull". It cannot drift from the compiler because the compiler reads the same table.
- **The dry run** prints the job back in the same grammar: one line per lever as resolved (tag, snapped frame, effective strength), then the six merged mechanisms (ownership per stream, timed rows, untimed rows, final prompt, model chain, sampler). An agent checks its intent against one page before spending anything.
- **Refusals** name the lever, the declared limit and its source, and a fix.
- **Templates** are requests with holes, so a template is a named combination of levers. `templates show` lists which kinds it uses.
- **The general skill** teaches three sentences (output, context, process), the ladder place → guide → reference, and how to read `describe` and a dry run. It does not list levers; `describe` does.
- **Problem skills** say which combination suits which creative situation and what goes wrong.

## 5. What to change in the plans

The plans already build nearly all of this. The changes are mostly naming and one table shape. Nothing here adds a task.

### Now

1. **Plan 66 plan, "One model".** Add after the three rules: "Every control is a lever of one of three families. *Output* levers (placed items and grants) decide what is in the result and are the only ones that can be exact. *Context* levers (references, guides, the prompt) are what the model looks at. *Process* levers (adapters, sampler settings) change how the model runs. A new control is a new kind in one of these families, declared in the capability table; it does not add a structure to the request."
2. **Plan 66 tasks, CC-2.** Add: "Key the table by lever kind. Each kind has: family, accepted fields and sources, limits (with `source_kind`), requires and conflicts, the mechanism it merges into, its lowering function and nodes, a dry-run line format, and a status (`compiles`, `live-tested` or `unavailable`). `describe` prints the kinds." Plan 64 SR-2 should create the table with a `kind` column so CC-2 extends it instead of reshaping it.
3. **Plan 66 tasks, CC-1 detail, lowering table.** Head it with: "Levers lower into six mechanisms, each with one merge function: latent and ownership mask; timed rows; untimed rows; text; model chain; sampler. A lowering adds to its mechanism and never reads another lever." Then keep the existing rows.
4. **Plan 66 tasks, CC-3.** Add: "The view has one line per lever in request grammar, then the six merged mechanisms."
5. **Plan 66 tasks, CC-6.** Replace "the item kinds" in the general skill's contents with "the three families and the ladder place → guide → reference; the list of kinds comes from `describe`".
6. **Reserve two names, build neither.** In CC-2 add: "`phase` (a span of sampling progress, 0 to 1) and the list form of `prompt` are reserved. No kind accepts them yet; a request using one is refused from the table as `unavailable`."

### Later, each as its own issue

- Timed prompt segments, lowered first to the model's own timed shot format.
- `phase` on adapters, after checking scheduled LoRA hooks against the H3 model class.
- A `control` role for Fun ControlNet.
- Curves as values (audio shift; strength ramps).
- An Event Curve tool that writes an audio file for a guide.
- A second guide lowering through `MiniMaxH3MotionContext`, only if `MiniMaxH3AddGuide` proves insufficient for clips with sound.

### Do not build

- A flat `levers:` list or any rewrite of the v2 shape.
- A lever base class, registry or plugin loader.
- Curves, phases or timed text before a kind needs them.

## Not established

- Scheduled LoRA hooks, and conditioning limited to a sampling window, on the H3 model.
- Whether serialized timed shots give usable timing control.
- Whether guides placed alongside masked-context places behave well together; `mc-2.md` says they compose in principle and no node offers the combination ready-made.
