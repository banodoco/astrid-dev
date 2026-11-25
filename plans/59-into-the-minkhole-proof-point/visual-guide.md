# Into the Minkhole — visual guide

[Plan](plan.md) · [Narrative outline](narrative-outline.md) · [Inputs](inputs.md)

Creative direction, 24 November 2026. Proposed motion-design language for the presenter/explainer portion of the demo, plus its transition into the finished short. A working visual direction, not an established new brand standard.

## Art direction: playful computational minimalism

An indie game meets a creative engineering experiment and beautifully designed software. Imagine a developer's notebook coming to life. The presenter remains casual and matter-of-fact; the graphic design is intentional, clean, playful and slightly eccentric. Show real work and leave room for the audience to draw its own conclusions. The pixel aesthetic is an accent and a storytelling device, not a filter on every frame.

### Visual references

- [Sebastian Lague — Coding Adventure: Clouds](https://www.youtube.com/watch?v=4QOcCGI6xOU): understated developer narration, intermediate attempts and earned payoff.
- [Panic — Playdate Update #1](https://www.youtube.com/watch?v=DeWGukDrc1U): retro/pixel personality paired with modern layouts; look at the opening and the Pulp section.
- Teenage Engineering — OP–1 field introduction: restrained typography, technical product photography, minimal compositions. [Official product page](https://teenage.engineering/products/op-1-field).
- [3Blue1Brown — But what is a neural network?](https://www.youtube.com/watch?v=aircAruvnKk): spatial explanations that connect concepts rather than presenting a succession of text slides.

References indicate aspects to study, not assets to copy. Confirm specific video links and timestamps before production; the visual guide is not a rights clearance.

## Design system

Use the existing Astrid brand and mink assets where available. Suggested explainer palette (from the conversation's illustrative layouts; reconcile with current brand): near-black `#171816`, warm off-white `#E8E6DB`, orange `#F08A45`, muted olive/grey supporting panels. Orange signals actions, connections and the mink rather than colouring everything. Use a contemporary readable sans-serif for substantive text, existing pixel typography for chapter markers and system labels, and a restrained monospace for technical metadata. Use generous spacing, simple grids, subtle borders and occasional dithering or dot-grid texture.

Motion grammar: smooth layout movement and panel expansion, stepped/frame-held motion for pixel sprites. Use very occasional pixel transitions. Small tactile clicks, synthesised chirps and restrained electronic sounds; avoid an epic trailer score. Let the real footage and dialogue interrupt the design. Readability is more important than decorative motion.

## Reusable compositions

Suggested layout sketches for a landscape demo frame; adapt the framing and safe area to the actual delivery format. These are schematic, not literal UI or approved artwork.

| Composition | Layout / motion | Narrative function |
| --- | --- | --- |
| 01 — Experiment | Presenter in a simple framed window at left; experiment title and metadata at right. Original footage slides in and expands to fill the screen. Use a modest `ASTRID / EXPERIMENT 001` label. | Familiar object and casual introduction, immediately. |
| 02 — Interconnected problems | Six compact cards (story, script, characters, video, audio, editing) appear on a dot grid and connect into one scene. Connections animate in time with narration. | Make the difficulty visible instead of explaining it at length. |
| 03 — Division of labour | Human column: direction, taste, feedback. Agent column: plan, select tools, generate, assemble, iterate. Move the implementation items to the agent side as the pledge is spoken. | Establish who does what. |
| 04 — Low-fidelity cut | Footage dominates the screen. Small `ROUGH CUT / V001` and `TEMP AUDIO · NO LIP SYNC` markers if needed. No fancy transition: hard cut into the unmoving mouth and flat robot voice. | Miniature payoff; intentionally terrible placeholder. |
| 05 — Shot investigation | Three aligned panels: source / mask or condition / result. Header: shot ID and chosen approach. Small evidence strip for real agent action, tool/model, or feedback. Adapt to continuation, audio or a completely new shot; show only relevant fields. | Make the agent's choice and the real before/after improvement legible. |
| 06 — Assembly | Shots, effects, dialogue and sound converge on the timeline; the real editor or an explanatory abstraction of its tracks becomes the focus. Hold long enough to recognise the timeline. Briefly show the actual pack's tools and skills. | Visual resolution of all the interdependent pieces; increase anticipation. |

A reusable composition vocabulary is preferable to dozens of bespoke animations. Implement as a small family of reusable motion components (e.g. Remotion if appropriate), using real screen recordings and assets. These are optional production techniques; no software change is required by this guide.

## Transition library

| Transition | Use |
| --- | --- |
| Hard cut | Comedy, contrast, rough-cut interruption, pause-to-black before the film. Use as the default. |
| Window expansion | A framed source/preview grows smoothly to full frame, or collapses back into the explanatory layout. |
| Connection and assembly | Cards, thumbnails and other objects physically join/rearrange into networks, shot sequences and timelines. |
| Pixel dissolve | A panel breaks into square pixels and reforms as the next composition. Reserve for a meaningful change; do not spend the major pixelation surprise early. |
| Mink-led transition | The little mink leaps toward an object or off-screen and carries the viewer to the next composition. Use sparingly. |

Suggested pacing: calm introduction; quick complexity build; readable rough cut and one awkward beat; energetic generation montage; slow assembled timeline; near-silence before the film. Within the film, stay cinematic until the sudden pixel adventure. Closing returns to the calm explainer.

## Mink as a character in the graphics

Use the existing orange pixel mink as an occasional inhabitant of the informational world. It can run along the edge of a window, nudge a clip into position, jump between cards or chase the playhead. A few brief moments are enough to familiarise viewers with it without giving away the film's joke. Keep the mink visually consistent with the brand asset and the short.

### The film ident and handoff

On “And here's the final product,” pause, cut to black, and show the Astrid wordmark. Mink jumps on top and leaps forward. Match its motion into the guide's glasses, flying out of one lens towards the viewer. Two or three seconds, like a film studio ident rather than an advertisement. The film then plays uninterrupted, without informational overlays.

The moment of contact with the mink is the biggest visual transformation: pixelation spreads from the protagonist's hand across the body, then the world expands into a colourful pixel-art adventure. Preserve that full transformation for the reveal. The mink flies toward the camera and becomes the logo at the end of the short; allow a beat before returning to the presenter for the closing.

## Practical direction and review

- Prioritise actual footage, actual agent actions and intermediate evidence. Label schematic diagrams as explanations, not product UI; never invent logs, models or results.
- Preserve the difference between the creator's direction/feedback and the agents' implementation.
- Make every technical graphic readable on a small screen. Keep overlays short enough to understand while listening; don't bury the footage.
- Show one real before/feedback/after shot. Keep the sad mink, the protagonist's reversal, the full pixel transformation, the magical world and finished sound design out of the montage.
- Avoid purple gradients, glowing orbs, gratuitous VHS/glitch effects, excess motion blur, elaborate prompt-box animations, self-congratulatory narration and constant mascot animation.
- The owner reviews visual taste and creative results. Validate the actual composition, legibility, timings and sound against a rough edit before final production; confirm media rights.

The narrative outline owns the spoken script and detailed film beats. This guide owns the explainer's visual and motion direction; it does not change Plan 59's engineering scope, status or release gates.
