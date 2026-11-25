# Into the Minkhole — visual guide

[Plan](plan.md) · [Narrative outline](narrative-outline.md) · [Inputs](inputs.md)

Creative direction — 24 November 2026. Companion to the production script. This guide concerns the presenter-led explainer and its transition into the finished short. It is a proposed application of Astrid's brand, not a replacement for established brand assets.

## Creative north star

**Playful computational minimalism.** A developer's notebook come to life: part indie game, part creative engineering experiment, part beautifully designed software.

The presenter is casual; the graphic system is carefully designed. Use the tension between slick, contemporary software and a slightly mischievous pixel aesthetic. Do not make the whole explainer pixel art. The final shift to pixel art must feel like a genuine escalation.

The intended viewer is an open-source AI or creative-tools enthusiast. Let a credible experiment speak for itself. Avoid hype, overexplaining or pretending the intermediate work is perfect.

## References to study

| Reference | What to borrow |
| --- | --- |
| [Sebastian Lague — Coding Adventure: Clouds](https://www.youtube.com/watch?v=4QOcCGI6xOU) | Understated developer storytelling, visible experiments, a mishap montage (8:26) and a satisfying final demo (11:31). Study the build-up rather than the video's length. |
| [Panic — Playdate Update #1](https://www.youtube.com/watch?v=DeWGukDrc1U) | Retro-game personality with a clean modern presentation. Watch the opening and the Pulp section (10:34). |
| [Teenage Engineering — introducing OP–1 field](https://www.youtube.com/watch?v=Fab7sp30pg0) | Restrained typography, composition, simple cuts and confidence. Let an interesting object carry the frame. |
| [3Blue1Brown — But what is a neural network?](https://www.youtube.com/watch?v=aircAruvnKk) | Explain relationships through spatial, connected objects instead of slides full of words. |

These references are for particular aspects of the visual and narrative language, not templates to reproduce. Links and named videos checked on 24 November 2026.

## Design system

| Element | Direction |
| --- | --- |
| Palette | Near-black, warm off-white, Astrid orange. Proposed mockup swatches: #171816 background, #E8E6DB type, #F08A45 accent. Actual brand assets take precedence. |
| Typography | Contemporary, readable sans-serif for primary information; pixel font or compact monospace for chapter headings, shot IDs, system labels and small accents. |
| Layout | Generous margins, clear panel edges, a consistent grid. One dominant visual per moment. Support with restrained labels and thin connecting lines. |
| Motion | Smooth layout movement and window expansion; deliberately stepped, grid-aligned motion for sprites and pixel effects. Keep the technical material readable. |
| Texture | Sparse pixel grids and occasional dithering. No blanket VHS, scanline or glitch treatment. |
| Audio | Small tactile clicks, synthesized chirps, short UI sounds. Let footage and voiceover take priority. Silence and contrast are part of the rhythm. |
| Mascot | Use the existing orange pixel mink as a little inhabitant of the graphical world. It can be mischievous without becoming a constant presenter. |

## Six reusable compositions

These are low-fidelity wireframes, not final brand assets or interface screenshots. Build them as reusable motion compositions, potentially in Remotion, using real capture material.

### 01 — Introducing the experiment

```text
ASTRID / EXPERIMENT 001
┌────────────────────┐  The
│                    │  experiment.
│     PRESENTER      │
│                    │  01 / THE MATRIX
└────────────────────┘  REMIX A SCENE
                        WITH AGENTS
```

Place the presenter in a clean frame with a brief title and experiment label. Introduce original footage almost immediately; slide or expand the source window to fill the frame. Avoid a long brand intro. The audience should recognise the object being transformed.

### 02 — Establishing the complexity

```text
THE INTERCONNECTED PROBLEMS
[ STORY ]  [ SCRIPT ]  [ CHARACTERS ]
     │         │           │
[ VIDEO ]  [ AUDIO  ]  [ EDITING    ]
     └─────────┼───────────┘
          [ ONE SCENE ]
```

As the narrator names each problem, introduce a compact object representing it. Add relationships progressively. The point is the interdependence of story, script, design, video, audio and editing, not complexity for its own sake. Use the resulting network to lead into the division of labour.

### 03 — The agent takes over

```text
THE DIVISION OF LABOUR
┌────────────┐     ┌─────────────────┐
│ HUMAN      │     │ AGENTS          │
│ Direction  │ ──▶ │ Plan            │
│ Taste      │     │ Select tools    │
│ Feedback   │ ◀── │ Generate        │
│            │     │ Assemble/iterate│
└────────────┘     └─────────────────┘
```

Separate the creative responsibilities from the technical ones. When the presenter says “I'm going to leave the how to the agents,” make that boundary visibly clear. This layout can recur when showing a creative feedback note and the resulting agent action.

### 04 — The rough cut

```text
ROUGH CUT / V001
┌─────────────────────────────────┐
│     Original, serious guide     │
│     Mouth visibly unmoving      │
│        YOU HAVE TWO OPTIONS.     │
└─────────────────────────────────┘
         TEMP AUDIO · NO LIP SYNC
```

Hard cut from the polished explanation to the deliberately terrible rough cut. A flat system voice says “You have two options.” Hold for one beat. No decorative transition or narrator laughing at the joke. The early payoff is the contrast between an ambitious promise and a crude but useful sketch.

### 05 — The machinery

```text
SHOT 004 / APPROACH: INPAINTING
┌──────────┐ ┌──────────┐ ┌──────────┐
│  SOURCE  │ │   MASK   │ │  RESULT  │
└──────────┘ └──────────┘ └──────────┘
AGENT › [actual action or decision]
```

Use a consistent shot-analysis layout, adapted to the real approach: source/mask/result for inpainting; source and continuation for continuation; waveform/voice for audio; reference/result for new shots. Show model/tool labels only when they are correct. Use actual logs and footage, not decorative fake terminal output.

Include one particularly legible mini-story: first generation → actual feedback (“Make him look more annoyed”, if that is the real note) → revised shot. Show the creative correction and the agent doing the work, not just a wall of thumbnails. Keep the final transformation and magical world out of this montage.

### 06 — Everything comes together

```text
ASSEMBLY / FINAL EDIT
               [ PREVIEW ]
VIDEO  [ shot ][ shot ][  shot  ]
FX         [ effect ]       [ fx ]
VOICE  [ dialogue ][ dialogue ]
SFX       [ sound ]   [ sound ]
                 │ PLAYHEAD
```

Let the separated visual and audio pieces visibly assemble into the timeline. Use real editor/timeline evidence. Show the two edit-feedback rounds if that is what occurs, then the pack and its relationship to the underlying tools/skills. Slow the motion and let the viewer anticipate the final film.

## Transition vocabulary

| Transition | Use |
| --- | --- |
| Pixel dissolve | Break an object into grid-aligned squares that form the next composition. Reserve for conceptual transitions; avoid diluting the final transformation. |
| Window expansion | Smoothly expand footage or a UI panel into the next full-frame image. Use when moving between presenter, source footage and genuine editor capture. |
| Connection and assembly | Physically join nodes or rearrange objects into a new composition. Use for workflows, pack relationships and the timeline. |
| Mink-led transition | The sprite leaps towards a new panel or exits the frame, carrying the eye into the next composition. Use sparingly. |
| Hard cut | For jokes, surprising evidence, the rough cut and the reveal. Not every change needs animation. |

## The mink as part of the information system

Let the mink occasionally run along the edge of a window, push a clip into place, hop between cards, chase the playhead or vanish behind a panel. Treat these as little Easter eggs. Use the established mascot assets and keep animation grid-aligned. Do not reveal the mink's dramatic sad moment or the adventure in the explainer.

## Rhythm and the prestige

Use different speeds intentionally: casual opening; accelerating complexity; readable rough-cut pause; fast technical iteration; deceleration as the timeline assembles; brief silence before the film. The rough cut and a genuine feedback comparison are small payoffs within the larger magic trick.

At “And here's the final product,” cut to black. Give the Astrid wordmark a short, two- or three-second studio-ident treatment: the mink jumps onto it, then leaps forward and flies out of a lens of the guide's glasses via match cut. Let the finished scene play without explainer overlays.

Inside the short, keep the setup grave, the mink excitable and the protagonist irritated. Hold the silence at the guilt beat. On contact, pixelation spreads from the protagonist's hand across his body; the pair launch into the colourful pixel adventure. The huge change in energy, colour and medium should feel earned. End the short on the mink becoming the Astrid logo; return to the presenter/editor for the closing.

## Production checklist

- Capture real source footage, rough-cut versions, temp TTS, shot variants, feedback messages, agent actions, workflow details and timeline revisions as the experiment progresses.
- Reuse six or seven compositions and a small transition library rather than making every frame a bespoke animation.
- Prefer the established Astrid type and mascot assets where available; the palette and wireframes here are proposed direction.
- Keep text large enough to read during playback. A single clear example beats a dense screen of tiny labels.
- Avoid purple gradients, glowing orbs, generic floating prompt boxes, excessive motion blur, epic trailer music and breathless declarations about the future of creativity.
- Use actual production evidence; do not claim successful implementation before it happens. Confirm rights to footage/audio before public use.
