# Opus craft pass: result

Read with the v2 engineering guide (superseded by `PLAN.md`) and `OPUS-REVIEW-RESULT.md`. This builds on the decisions made since: the stack is the live panels in a third pose, T0 and H0 exist, all media are placeholders, and the preview is an Artifact. Paths use the guide's prefixes (`H/`, `V/`, `J/`). Every number here goes into T0, and T0 may tune any of them by up to ±20% without coming back to this pass.

## Craft principles

1. **One set of objects.** Everything that moves below the hero is the hero's own panels, re-posed. Anything new comes from somewhere: the Agent layer opens out of the launcher or the conversation, the Runtime rises from below, a tag is stamped by the agent.
2. **One motion vocabulary, all from the hero:** three easings, one accent and four durations (table below). Nothing in `J/` writes a millisecond or a curve of its own.
3. **Scroll picks the place; time plays the moment.** Poses are timed transitions fired at a line on the screen. Only the sky follows the scroll. Poses always retarget and never queue, so a fast scroll is a shorter path, not a pile-up.
4. **One lead at a time.** At any moment there is one primary motion (a pose or an edit), at most one secondary (text, tag or chip), and the mink, who leads only when she is the agent doing the edit.
5. **The agent is pixel, the human is vector.** The mink and her glyphs step in whole device pixels on a 70 ms tick. The "You" cursor and the UI glide. They never swap styles.
6. **Cause, then receipt.** Every agent action follows the same order: the request, then the action (mink or edit), then the system lighting up, then the receipt (tag or chip) stamping. That stamp is the only thing that overshoots.
7. **Every end state is a composed frame.** Phones, reduced motion, fast scrolling and scrolling back up all land on the same designed endpoints. None of them is a lesser version.
8. **Then stillness.** After each demo, nothing loops except the 3D view's slow sway while its tab is open, the sky's existing twinkle and a rare blink.

### Motion values (feed T0 → `J/journeyMotion.ts` and matching CSS custom properties)

| Token | Value | Hero source (reused, not invented) | Used for |
|---|---|---|---|
| `ease.pose` | `cubic-bezier(.5,0,.15,1)` | `--astrid-surface-ease`, `H/PublicAstridShell.css:418` | Every surface move, clip move, cursor move, conduit draw |
| `ease.settle` | `cubic-bezier(.22,.61,.36,1)` | Assembly transition `:411`; layout glide `H/usePublicAstridLayoutGlide.ts:18`; Vision reveal | Assembly tilt, frame fade, colour and opacity changes, small lifts |
| `ease.enter` | `cubic-bezier(.16,1,.3,1)` | `astrid-callout-in` `:1194`, `astrid-surface-in` `:1902` | Anything appearing: panels, cards, readouts, labels, History rows |
| `ease.land` (accent) | `cubic-bezier(.34,1.5,.64,1)` | Connector end-dot land `:1211` | **Only** the agent-action stamp and the lit-layer dot |
| `ms.quick` | 260 | Composer note `:818`; mink hop `PublicAstridSky.css:97` | Fades out, stamps, chip slides, tab swaps |
| `ms.enter` | 520 | Callout text and connector draw `:1196,:1203`; layout glide 520 | Entrances, clip moves, conduit draws |
| `ms.travel` | 720 | `publicAstridMotion.ts:43`, `THEME_WASH_MS` | Every pose change, assembly tilt, palette crossfade |
| `ms.ping` | 900 | `astrid-dot-ping` `:1219` | Stamp ping, "changed" flash on clips |
| derived | stagger 60 · floor 120 · fade 360 · label point 0.7 · sprite tick 70 · pending 600 · receded opacity .55 | Phone callout stagger `:1826`; retarget floor `publicAstridMotion.ts:80`; `CALLOUT_CONTENT_FADE_OUT_MS`; `labelDelay` `:50`; MinkRunner 770 ms / 11 frames; director "Thinking"; Agent backdrop `:1369` | — |
| `linear` / `steps(n)` | — | — | The sky (scroll) / sprites, typed text |

**Floor rule:** any secondary effect of a pose (frame fade, labels, mink, tray) starts at least 120 ms after the pose begins. A pose replaced within 120 ms therefore never flashes its extras.

## 1. Transitions

### 1.1 Shared mechanics (they shape the feel, so they're written down)

- **Trigger lines.** On desktop and tablet a section activates when its header's top crosses **66%** of the viewport height. It deactivates on the way back when the header drops below **72%**. On phones the line is at **78%** (back at 83%), because the top 45svh is the stage. "Leave hero" is a separate, earlier line: scroll ≥ **10%** of the viewport (back at 4%).
- **Same function lists.** Write every assembly pose as `rotateX() rotateY() rotateZ() scale()`, putting zeros where a value is unused. Hero: `rotateX(5deg) rotateY(-8deg) rotateZ(0) scale(.9)`. Stack: `rotateX(58deg) rotateY(0) rotateZ(-8deg) scale(.84)`. Mismatched lists fall back to matrix interpolation and wobble.
- **Keep `transform-origin: 35% 42%`.** Changing it mid-move jumps. Re-centre through the existing `translate: var(--astrid-centre-x)` channel, adding a y term.
- **Transforms and opacity only** for moving poses. The single exception is the App chat growing out of its launcher circle, which reuses today's geometry move (its content is already hidden while it grows).
- **Labels and conduits are siblings of the surfaces inside `.astrid-editor-surfaces`, not children.** Surfaces use `overflow:hidden`, which would clip and flatten them. Labels are counter-rotated (`rotateZ(8deg) rotateX(-58deg)`) so they face the viewer and move with their layer for free. Conduits are 2 px divs rotated 90° about X, standing between two layers; they draw with `scaleY 0→1`. Nothing is measured per frame. If the H0 2× still shows soft label text, fall back to flat labels measured once after the stack settles.
- **Anything flat that points into the stack** (the beat-sync cable, the mink's §2 spots) reads one 1 px anchor element inside the layer **once, after settle** and again on resize. Never per frame.

### 1.2 Leaving the hero (scroll ≥ 10%)

| t (ms) | Beat |
|---|---|
| 0 | Callouts retract with today's vacuum: connectors 450 ms (`CALLOUT_VACUUM_RETRACT_MS`); cards fade 360 ms ease-in, −4 px, scale to .94. Last-in leaves first, 60 ms apart. |
| 0 | Pointer tilt eases to 0 over 480 ms (`settle`), then the loop stops. Don't unmount mid-tilt, or the inline transform snaps. |
| — | The preview keeps playing and the stage frame stays. The hero is resting, not broken. |
| Back above 4% | Today's reconnect sequence: extend 380 ms, 140 ms stagger, 900 ms ping. Tilt resumes on the next pointer move. |

### 1.3 Hero → §2: the pull-apart (the page's biggest single motion, ~1.3 s)

**Stack pose (desktop D, starting values for T8).** Assembly as in §1.1. Layer depths in assembly space: Preview **+250**, Panels **+125**, Timeline **0**, Agent **−125**, Runtime **−250**. That gives about 89 px of screen separation per layer at D. All five are centred on one axis. Scales: player 1.0, inspector 1.2, timeline .8, Agent band 1.0, Runtime (new HTML) laid out at 72% × 30% of the stage. The Agent layer is the chat surface clipped to its composer band: `clip-path: inset(calc(100% - 64px) 0 0 0 round 10px)`. Clip-path costs paint, not layout.

**From App** (the editor is already apart, so it tips back and fans out; the Agent layer opens out of the launcher):

| t (ms) | Beat |
|---|---|
| 0 | The preview pauses on its current frame. The assembly tips, 720 `settle`: it starts fast, so the stage answers the scroll at once. The launcher fades, 260. |
| 120 | The stage frame dissolves (border, panel fill and shadow → transparent), 520 `settle`. From here the panels hang in the sky. The music clip is published now and fades onto the timeline over 360, hidden inside the larger motion. |
| 180 / 240 / 300 | Preview, Panels, Timeline travel to their depths, top-down: 720 `pose` each, 60 ms apart. |
| 360 | The chat grows out of the launcher circle into the Agent band (today's App→Agent geometry, 720 `pose`). Its content fades in 160 ms after it settles, as it does today. |
| 600 | Runtime rises from depth −420 to −250, opacity 0→1, 720 `pose`. |
| 0.7 of each layer's travel (684, 744, 804, 864, 1104) | Its label fades in, 260 `enter`, sliding 6 px from the left. |
| 1320 | Settled. 200 ms of nothing, then the §2 demo (§4.2). |

**From Agent** (the visitor was reading the conversation, so the conversation leads):

| t (ms) | Beat |
|---|---|
| 0 | Assembly tips (same). The conversation folds: its clip closes top-down to the composer band, 520 `pose`. Messages wipe away and the composer remains. |
| 120 | The frame dissolves (same). The three backdrop panels brighten from .55 to 1, 520 `settle`. |
| 180 / 240 / 300 | Preview, Panels, Timeline rise to their depths (720 `pose`). They're above the band on screen before they pass it in depth, so no plane cuts through another. |
| 420 | The band sinks from depth +70 to −125, 720 `pose`. It starts only once its clip is mostly closed, so it never crosses a full panel. |
| 600 → 1320 | Runtime and labels as from App. Settled at 1320. |

**The headline.** The §2 header scrolls in from below in normal flow while the hero copy leaves the top. The headline and sub never animate: they're the stable thing to read while the stage moves. At the trigger the eyebrow (`02 / MAKE IT YOURS`) **types on**: `steps(n)` over its width in `ch`, 16 ms a character, about 290 ms. That is the agent's pixel voice announcing the section. It types once per visit and is never re-typed.

**How it feels:**

| Scroll | Behaviour |
|---|---|
| Slow (≈400 px/s) | Callouts lift away, then a long beat of the hero at rest. When the header reaches two-thirds of the way up, the editor tips back and fans out while the header keeps rising. The stack settles about when the header reaches its sticky spot. |
| Fast (flick past §2) | The pull-apart starts and is immediately retargeted to the destination pose. The 120 ms floor means the frame never blinks and no labels or tags flash. §2's endpoint is committed in the data only. |
| Back up into the hero | The reverse runs bottom-up: Runtime sinks and fades (360). The band returns to the launcher (App) or opens back into the conversation (Agent: clip reopens 520, rises to +70). Timeline, Panels and Preview follow 60 ms apart (720 `pose`), and the assembly tips forward (720 `settle`). The frame re-forms at 480 (360). Callouts reconnect once the surfaces settle. Playback resumes after the callouts land. The music clip fades out (hero projection). |

### 1.4 §2 → §3: the stack folds back into the live timeline (~0.84 s)

| t (ms) | Beat |
|---|---|
| 0 | The example panels, cable, tabs and labels fade, 260 `settle`; panels drift 8 px right. The mink pops out (160). |
| 0 | Runtime sinks to −420 and fades (520 `pose`). The Agent band sinks and fades (360 `settle`, starting 60). |
| 120 / 180 | Preview, then Panels, lift a further 120 px of depth and fade out (520 `pose`). |
| 120 | **The timeline leads.** The assembly un-tips to flat (`rotateX(0) rotateY(0) rotateZ(0) scale(1)`, 720 `pose`). The timeline lands as the bottom strip at `scale(.84)`, flat, so its text renders crisp. It keeps its hero box (transform only). |
| 840 | The stage frame re-forms (360 `settle`): it dissolved when the editor came apart and returns now that it's back together. If the fit changes, clips glide to it (520 `pose`). |
| 1200 | §3 demo. |

Slow: as in the table. **Fast** (into §4): the timeline goes straight to the edit pose, the tray never appears, and the lake clips are on `V2` when the timeline lands (260 fade). **Back up**: the tray fades first (260). `V2` fades (260) before the §2 projection drops it. The frame dissolves (360). The timeline tips back into the stack (720 `pose`). The others return from where they left (Preview and Panels from above, Agent and Runtime from below, 60 ms apart). The examples show the last-selected tab's end state, with Replay.

### 1.5 §3 → §4: the timeline grows (~0.72 s, a dolly-in)

| t (ms) | Beat |
|---|---|
| 0 | Readouts lift 8 px and fade (260). The route pills and machine icons fade (260). The tray fades (260). The mink pops out (160). |
| 120 | The timeline grows: `scale(.84) → scale(1)` and rises from the bottom strip to centre-low, 720 `pose`. No zoom change, so no clip reflows. Text gets bigger as if the camera moved in. |
| 120 | `V2` (lake source track) recedes to .55 (520 `settle`). Above `V1` it becomes the mink's stage. |
| 600 | The History panel enters top-right, holding only its header: −8 px, 520 `enter`. |
| 840 | The mink pops back in on `V2` above First light (3-step hop, 210 ms), where she landed at the end of §3. |
| 1100 | §4 demo. |

**Fast**: §4's endpoint state appears, and History rows and chips appear without stamps. **Back up**: History fades (260), `V2` returns to 1 (360), the timeline shrinks to the strip (720 `pose`) and the tray shows its end state.

### 1.6 §4 → finale

The sticky stage simply scrolls away. Nothing animates. The finale's eyebrow, headline, line and link reveal with the Vision `[data-reveal]` values (`opacity`, 14 px, 560 ms `settle`, stagger 0/90/180/270 ms; `H/PublicAstridVision.css:554`), moved to the shared module the guide names.

## 2. Micro-animations

| Moment | What it does | Duration · easing | Avoid |
|---|---|---|---|
| **Agent-action stamp** (`built by your agent`, `installed by your agent`, `set up by your agent`) | Departure Mono 11 px (its grid size), orange. It appears 120 ms after the thing it labels settles: scale 1.12→1, opacity 0→1, then one 1 px outline ring expands 6 px and fades | 260 `land`; ring 900 (ping curve `(.2,.7,.3,1)`) | Shimmer, glow, typing the tag, a second bounce, re-stamping when a tab is revisited (it's simply there) |
| **Lit stack layer** | Label → orange (260 `settle`); its dot fills from a ring (scale .4→1, 260 `land`); the plane gets an orange rim `0 0 0 1.5px` plus a 28 px soft glow at 35% (360 `settle`). Text plus dot, never colour alone | as given | Pulsing, breathing glow, more than one lit layer except during "Runtime → all layers" |
| **Conduits** | Pillars draw layer to layer with `scaleY 0→1`, one hop after another; the end dot lands; one 4 px "packet" travels the path **once** | 520 `pose`, 120 ms per hop; dot 380 `land`; packet 600 `pose` | Looping packets, dashes marching forever |
| **Typed readout / install log** | Monospace lines (Departure Mono 11 px, 16 px line) reveal by `steps(chars)` over `ch` width at 18 ms a character. The line's pixel check (`PixelCheckIcon`) pops in 2 steps when the line ends. Next line after 120 ms. A 1ch orange caret rides the typing line, blinks twice at the end (530 ms), then goes. Title and tag appear whole first | 18 ms/char; check 2 × 70 ms | Jittery speeds, spinners or progress bars implying real compute, re-typing on scroll-back, measured numbers (placeholders say "Example") |
| **Code panel** (3D tab) | First 4 lines of the real module type at 12 ms a character; caret as above; the "● live" dot is static | ≈600 ms | A blinking or pulsing "live" dot |
| **Thinking** | "Thinking" plus a pixel ellipsis (3 × 3 px squares) replaces the `Loader2` spinner, through host CSS only | `steps(4)` 960 ms loop, for the 600 ms pending | The round spinner on this page |
| **Spine bubble** | Today's `astrid-rise` (14 px, 500 ms ease). The previous turn recedes to .55 | 500 ease; recede 360 `settle` | Sliding whole threads; layout shift (reserve the spine's final height) |
| **Tool-call chip** (receipt) | Lands when the edit it describes **finishes**, not when the reply appears. It slides 6 px down from under its reply; its 16 px pixel wrench turns −30°→0 in 2 steps. `beat-sync` then floods its fill left to right | 260 `enter`; wrench 2 × 70; flood 360 `settle` | Chips before the change, chips re-animating when older turns recede |
| **Clips settling** | `left`/`width` glide. On arrival an overlay rectangle over the clip shows a 1.5 px orange outline that fades out (no editor DOM touched). Moved clips lift 4 px with a shadow before moving and drop after | glide 520 `pose`; flash 900 `settle`; lift and drop 120 `settle` | Overshoot or bounce on clips, motion blur, several clips moving in one beat (stagger 120) |
| **Stills develop** (§3) | Card opacity 0→1, scale .96→1; the image sharpens from `blur(6px) saturate(.4)` | 520 `enter`; image 720 `settle`; 400 ms apart | A loading bar, shimmer skeletons |
| **Reframe** (§3) | Explicit card `width`/`height` to 9:16 (`aspect-ratio` doesn't transition); the image crossfades to the 9:16 file at the midpoint | 720 `pose`, 60 ms left to right; crossfade 260 | Stretching the 16:9 image |
| **Card → clip** (§3) | The card stays in the tray. Its play glyph pops (2 steps), the video fades over the poster and plays **once**, then a dashed drop line draws from the card to its `V2` slot and the clip appears there with a "changed" flash | glyph 2 × 70; video fade 260; line 520 `pose`; clip fade 260; 600 ms apart | Flying cards (no clones), five looping videos at once |
| **Beat markers** (§4) | Three orange lines grow up from `A1` to the top of `V1`, each topped by a dot | `scaleY` 360 `enter`, 90 ms apart; dot 260 `land` | Markers pulsing to the music |
| **"You" cursor** | Glides between targets. Press: scale .9 for 80 ms. Drags with the handle on the same curve. Release: 120 `settle`. Idle after 1.5 s: fades to .55 | 720 `pose` long moves, 520 short | Idle jitter, wandering, teleporting |
| **Level line, crossfade wedge, 0.6× dimension** | Overlay strokes draw (dimension line `stroke-dashoffset`); the wedge grows from 0 to 1.5 s width | 520 `pose` | Labels popping before the stroke reaches them |
| **History row** | Appends at the bottom (four rows visible). Icon (vector cursor or 16 px mink head from `astrid-favicon.svg`) pops in 2 steps; text appears whole; the new row tints orange 10% → 0. On a fifth row the list shifts up one row and the top row fades | row 260 `enter` from +6 px; tint 1200 linear; shift 360 `settle` | Typing, counters, reordering, two tinted rows at once |
| **Example tabs** | A real 3-segment control. Hover: fill ink 6% (dark: white 8%), icon up 1 px, 120 ms ease. Press: scale .97 for 80 ms, release 160 `settle`. **One orange pill slides** between segments (360 `pose`); text colour swaps at its midpoint. While auto-cycling, a 2 px line fills under the selected tab (linear, over the tab's 6 s). The first click stops cycling and the line fades (260). Focus: today's 2 px `#ed6b23`, offset 2 | as given | Layout change on hover; progress lines under reduced motion |
| **Tab swap** | Outgoing panel, cable and mink out (260, 8 px toward the old side); layer unlights; the new tab's sequence starts at +260 | 260 `quick` | Crossfading two examples on top of each other |
| **Replay** (`↺ Replay`, bottom-right of the stage on desktop, under the spine on phones) | Fades in 800 ms after a demo ends, or at once when the visitor scrolls back up. Hover: ↺ turns −180°. Press: the section fades to its base (260), then replays after 360 | glyph 520 `pose` | A rewind or scrub animation; showing it during play; moving it |

## 3. The mink

### 3.1 Rules

- **Pixels.** Strips are drawn at the existing density: the run cycle's 81×44 frame (`src/shared/components/MinkRunner/astrid-mink-run.png`, 11 frames) and the Vision juggler's 47×77 frames, about 70 art px nose to tail. Render one art pixel as a **whole number of device pixels**, the way `MinkRunner` sizes itself:
  - desktop: 3 device px at DPR ≥ 2, 2 at DPR 1 (1.5 or 2 CSS px; the runner shows at about 121 px wide);
  - phone: 2 device px;
  - finale: 2 device px everywhere ("small mink, big sky").
  - `--px = devicePx / devicePixelRatio`, set by JS once and again on DPR change. Rest positions snap to whole device pixels. Never put her inside a scaled or 3D-transformed element: she lives on the flat overlay layer.
- **Palette.** Mink: exactly `#FF7A2E`, `#D9531E`, `#F7E6CF`, `#151311`, as sampled from the runner, front, juggler and tinkerer art. Props use the tinkerer's set (`#A5B2B2`, `#7E989F`, `#3C5F66`, `#F3D27D`, `#B46D30`). 1 art px outline in `#151311`. No partial alpha.
- **Timing.** Every sprite advances on the runner's **70 ms** tick (slow loops at 140). Position moves are either attached to a gliding UI object (same curve and duration, unsnapped in flight) or a hop: a 3-step arc at 70 ms a step, rising 4 then 6 art px.
- **The existing hop** (`astrid-mink-hop`: 1 art px, 260 ms `steps(2)`) is her "pop in". "Pop out" drops 1 art px and disappears over 2 steps (160 ms). She appears and disappears between spots, like a pixel-game character; she doesn't run across 3D layers.

### 3.2 Cue sheet (all she does on the page)

| Where | Beat | Pose | What she does | Glyph |
|---|---|---|---|---|
| Hero | — | — | Nothing new. The brand mink and the launcher are enough | — |
| §2 · 3D view | tab +1400 | `sit` f0, clipped by the panel's top edge | Pops up behind the 3D panel and peeks over it. Blinks at +3600 | — |
| §2 · Beat-sync | +1400 | `plug` | Appears at the Agent band's right end with the cable's plug; 5-frame push-in (350 ms) as the cable reaches the beat-sync socket; holds the last frame. The conduit lights from the connection | — |
| §2 · New model | +1400 | `push` | Pushes the LTX-Video block into its Runtime slot along the block's projected path (720 `pose`, matched to the block). Hops on arrival | **sparkle** (the page's only one) |
| §3 | 0.3 s | `sit` + 1 art px bob (2 steps × 140 ms) | Pops in beside the Local machine icon and "types" while the readout types; stops when it stops | thought dots on "Thinking" |
| §3 | 10.1 s | `sit` → hop | Pops onto lake-05's card, follows its drop line down in a 3-step hop and sits on the new `lake-05` clip. **That's where §4 finds her** | — |
| §4 | 1.6 s | `sit` | The visitor's cursor starts trimming; she notices | **"!"** (the page's only one) |
| §4 · arrange | 3.1 s | `carry` (6 f, 420 ms loop) | Hops onto Passing shapes and walks with it as it slides left, matched to the clip's 520 `pose` glide | thought dots before |
| §4 · beat | 5.9 s | `run` (existing) → `snip` (4 f, 280 ms) ×3 | Scampers to each cut and snips as the edge snaps to its marker, 500 ms apart | thought dots before |
| §4 · retime | 10.4 s | `push` (4 f, 560 ms loop) | Pushes the stretching Passing shapes; stops when the stretch lands | thought dots before |
| §4 end | 12.6 s | `sit` | Sits on `V2` near the crossfade. Blinks | — |
| Finale | always there | `lookup` f0 → f1 | Stands small at the horizon, about 72% across, facing the horizon. When sky progress reaches ≥ .98 (the opposite peak) she lifts her head (2 frames, 140 ms) and blinks once 1.2 s later. Scrolling back below .9 swaps her back to f0 without animation | — |

### 3.3 When she holds back

- One mink on screen at a time, and never during a pose change: she pops out at its start and back in after it settles.
- She never covers a clip label, tag, chip, the cursor or History. She stands on `V2` (dimmed source track) or on a panel's edge.
- While the visitor's cursor edits she watches; she doesn't act.
- She reacts to beats, never to scroll. On fast-forward she is simply placed at the section's end spot as a static frame.
- Idle is a blink every 3.6/4.4/4.0/4.8 s (seeded, so H0 is deterministic). No breathing loop, tail wag or wandering.
- **Glyphs:**
  - "!" once on the page;
  - one sparkle on the page (§2 LTX);
  - thought dots (the existing `astrid-north-star-adapt-thought0/1/2`, 140 ms apart) only while the spine shows "Thinking" and she is on stage; they vanish when the reply lands;
  - motion lines and snip lines are baked into the `carry`, `push` and `snip` frames, not separate glyphs.

### 3.4 Make vs reuse (frame counts; A5 tasks in §6)

| Strip | Frame (art px) | Frames | Playback | Placeholder now (existing art, no resampling) |
|---|---|---|---|---|
| `run` | 81×44 | 11 | 70 ms loop | **Final:** the MinkRunner strip as it is |
| `sit` | 40×56 | 2 (rest, blink) | blink 140 ms | `astrid-mink-front.png` reduced by exactly 4× nearest-neighbour to its 32×32 grid |
| `carry` | 80×56 | 6 | 70 ms loop | `run` at 70 ms |
| `push` | 81×44 | 4 | 140 ms loop | `run` frames 6–9 at 140 ms |
| `snip` | 56×56 | 4 (raise, open, close + 3 snip lines, open) | 70 ms one-shot | `sit` plus the `astrid-north-star-adapt-snap` glyph (5×7) |
| `plug` | 48×64 | 5 (hold, lean, push, connect, recoil) | 70 ms one-shot, hold f4 | juggler frame 1 (47×77) plus an SVG plug |
| `lookup` | 48×80 | 3 (horizon, up, blink) | on cue, blink 140 ms | juggler frames 1 and 2 (they already look up) |
| `!` mark | 5×12 | 3 (small, up 2 art px, rest) | 3 × 70 ms, hold 490 ms, off | Departure Mono "!" at 11 px, `#FF7A2E` |
| sparkle | 7×7 / 5×5 | 3 | 100 ms each, once | **Final:** `astrid-north-star-knowledge-spark0/1/2` |
| thought dots | 3, 4, 6 px | 3 | appear 140 ms apart | **Final:** `astrid-north-star-adapt-thought0/1/2` |
| peek, type, notice | — | — | — | **No new art:** `sit` clipped, `sit` + bob, `sit` + "!" |

That's **27 new frames in 7 strips**. Each strip keeps the same feet-contact anchor in every frame, has no gutters, and is checked with `pixel.strip`/`pixel.sprites` against the palette and the runner's density.

## 4. Restraint and rhythm

### 4.1 Page rhythm

| Section | Arrives with | First key beat after the trigger | Demo | Then | Scroll length (T6 tunes) |
|---|---|---|---|---|---|
| Hero | — | — | live hero | — | 100svh |
| §2 | 1.3 s pull-apart | stack formed 1.3 s; first tag 3.5 s | 3 tabs × 6 s, **one cycle**, resting on New model | still; Replay at +0.8 s | 220svh |
| §3 | 0.84 s fold | first still 2.5 s | ≈ 12 s | still | 180svh |
| §4 | 0.72 s grow | trim 2.7 s | ≈ 12.6 s | still; cursor dims | 180svh |
| Finale | the stage leaves | the sky reaching its peak | — | the mink looks up | 120svh |

Demos are front-loaded: the best beat lands in the first 3–4 s, and the rest rewards readers of the header and spine. Visitors who flick still get composed end states.

**Fast-forward when leaving early:** within 600 ms, overlays (mink, cursor, glyphs) pop out (160). The endpoint snapshot publishes. Clips glide once to the final positions (520 `pose`). History, chips, tags and readouts appear complete without stamps.

### 4.2 Section beat sheets (for T0; t is from demo start)

**§2, each tab** (tab k starts at k × 6000):
- **+0:** the request rises.
- **+150:** layer lit.
- **+300:** "Thinking" (600).
- **+900:** reply plus the example panel enters (520 `enter`, from 12 px right) and builds (≤ 800):
  - 3D view: code types; the canvas fades in (360); the camera sways ±18° yaw around the playhead on an 8 s sine.
  - Beat-sync: workflow card; waveform reveals left to right (720 `pose`); 5 markers drop (260 `enter`, 90 ms apart).
  - New model: install log types.
- **+1400:** mink cue.
- **+1750:** conduits light.
- **+2300:** tag stamps.
- **+2600 → 6000:** still.

**§3:**
- **0.0:** carried LTX pair at .55.
- **0.3:** "Make five stills…"; machine icon and the `Local · Flux · ComfyUI` route enter (260 `enter`); the mink pops in.
- **0.7:** "Your machine" readout enters, then its tag stamps at +260.
- **1.0–2.6:** lines type.
- **1.3–2.9:** five stills develop, 400 ms apart.
- **3.8:** "Make them vertical."
- **4.2:** Thinking.
- **4.8–5.9:** reframe; the readout line "reframed to 9:16" types.
- **5.9:** "Reframed to 9:16."
- **6.8:** "Animate them in the cloud with Wan."; cloud icon, the `Cloud · Wan · Wan2GP` route, and a dashed Local→Cloud line draws (520).
- **7.2:** Cloud readout.
- **7.8:** `V2` track fades in (260).
- **8.0 + 0.6k (k = 0…4):** card k plays once and drops to its clip.
- **10.1:** the mink rides down.
- **11.2:** "Five stills, reframed and set in motion."
- **12.0:** end; Replay at 12.8.

**§4:**
- **0.4:** the request.
- **0.9:** the cursor enters from the stage's right edge (720 `pose`).
- **1.6:** press, drag First light's right handle, release; "!".
- **2.2:** History "You · trimmed First light".
- **2.4:** Thinking.
- **3.0:** Astrid's reply.
- **3.1:** Passing shapes, then A quiet finish 120 ms later, lift, slide and drop; the mink carries.
- **3.9:** History row and chip `arrange · 3 clips`.
- **4.6:** "Cut every clip on the downbeat."; markers rise.
- **5.2:** Thinking.
- **5.8:** "Done. Every cut lands on a beat."
- **5.9–7.3:** three snips and snaps.
- **7.4:** History row and the `beat-sync · 3 downbeats` chip with its flood.
- **7.9:** the cursor drags the music level to 0.6.
- **8.6:** History row.
- **9.2:** "Slow the middle scene and crossfade into the last frame."
- **9.8:** Thinking.
- **10.4:** "Slowed to 0.6× with a 1.5s crossfade."; stretch, dimension line and wedge; the mink pushes.
- **11.2:** History row and chip `retime · crossfade`.
- **11.6:** the cursor extends A quiet finish.
- **12.2:** History row (the list shifts).
- **12.6:** end; Replay at 13.4; the cursor dims at 14.1.

**Copy this pass proposes to T0:**
- **§4's opening** should show co-editing and must not repeat the hero:
  - User: "I'll shorten the opening. Close the gap behind me."
  - Astrid: "Closed the gap. It runs N seconds now." (T1 states N from the snapshot)
- **Pending:** "Thinking".
- **Replay:** "↺ Replay" (label: "Replay this section's example").
- **Reduced motion:** "Show the steps" / "Pause".
- **Placeholder honesty:**
  - No usage counts ("2.4k uses") and no GPU specs;
  - the workflow card reads "Community workflow · adapted by your agent";
  - readouts carry "Example" and the install log is marked illustrative.

### 4.3 Where to breathe, and what's cut

- **Breathe:**
  - 200 ms after each pose settles, before anything else;
  - ≥ 2.7 s of stillness after each §2 example;
  - 0.9 s between the last still and "Make them vertical";
  - 0.8 s at every demo's end before Replay;
  - the finale has no demo at all.
- **Cut:**
  1. The orange page rail and the dots on bubbles.
  2. The brand repeated at the top of each section.
  3. Connectors from spine bubbles to the stage (the lit layer and the stamp carry the link).
  4. Endless tab cycling (one cycle).
  5. Looping conduit packets.
  6. Mink idle loops (blink only).
  7. A full 3D orbit (sway ±18°).
  8. Five looping lake videos (each plays once; desktop hover replays one).
  9. The big 3D LTX box beside the stack in mockup 02c (the block in Runtime is enough).
  10. Pointer tilt and callouts below the hero.
  11. Horizon lights (as the review said).
  12. More than one sparkle or one "!" on the page.

## 5. Phones (390 px) and reduced motion

### 5.1 Phones

- **The handoff.** When the stacked hero's stage reaches the top it pins. As the pull-apart starts, its content scales into the top 45svh (`transform: scale`, top-centre origin, 720 `pose`). Text below is never covered and never jumps; T5 owns the mechanism, and its done-when is "no jump".
- **§2: an orthographic stack in a flat parent.** Each surface gets `rotateX(58deg) rotateZ(-10deg)` with no perspective, so the slabs look isometric. They take the top 60% of the stage, 40 px apart, about 260 px wide. Today's phone hero is flat, so this is the first tip it has ever had: the same 720 `pose`, 60 ms top-down stagger and Agent clip-fold as desktop, settling at about 1.3 s.
  - Labels sit to the left of the slabs in Departure Mono 11 px.
  - Conduits are plain 2D lines between slab centres (rotated pillars vanish in a flat parent).
  - The bottom 40% of the stage is the selected example as one compact card: the 3D view at DPR ≤ 2, the waveform with markers, or the install log.
  - The tabs are the 3-segment control in the text below, labelled "3D view", "Beat-sync" and "New model".
- **§3.**
  - The tray is a row of five cards 62 px wide (16:9 at 35 px tall, reframed to 110 px: the reframe reads even better here) above the timeline strip at scale .84.
  - Readouts move into the flow text under the spine: title, stamp, the first line typed, the rest appearing whole 120 ms apart.
- **§4.**
  - The timeline only (`V2` at .55), fitted with the 56 px touch gutter.
  - History becomes a one-line ticker at the stage's top, crossfading each new row (260).
  - The spine shows the latest two turns below, chips under them.
- **The mink on phones** appears only in §3's ride, §4 and the finale, at 2 device px. §2 and §3's typing cue are cut: those stages are full.
- **Tablet (641–1099)** uses the desktop poses and mink size, and the phone's pin-and-scale handoff (its hero is stacked too).

### 5.2 Reduced motion

| Item | Under reduced motion |
|---|---|
| Leaving the hero | Callouts disappear (today's behaviour); no tilt |
| Pose changes | Geometry switches in one frame inside a 200 ms opacity dip: the stage goes to .2 over 100 ms and back over 100 ms (`settle`). The stack keeps its **static** 3D: it's the picture, not motion |
| Demos | Never auto-play. Endpoints appear at once: tags present, readouts complete, all checks, History full, chips present, eyebrow already typed |
| Tabs | Manual only, no progress line; the pill and panel swap with a 150 ms opacity crossfade |
| Mink | One static frame per section: §2 `sit` beside the LTX block; §3 `sit` on the lake-05 clip; §4 `sit` on `V2` by the crossfade; finale `lookup` f1. No glyphs |
| Sky | One step per section boundary |
| Replay | Replaced by **"Show the steps"**: a slideshow of the beat sheet's endpoints, 1.6 s each, 200 ms opacity crossfades, no transforms, pausable. It only plays on request, so reduced-motion visitors get the whole story without unasked motion |

## 6. Tasks

H0 names the evidence. Recordings are `h0/<id>-<D|P>.webm`; stills are `h0/<id>-<D|P>-<ms>.png` at 2× DPR. Scroll profiles: **slow** 400 px/s, **flick** 3000 px/s, **back** 600 px/s. Opus judges at 2× against the named round 4 frame, not from contact sheets. Every TASTE-HIGH task has two passes, the second after the owner's phone look. T8, T18, T20, T22 and M1 share one Opus notes lineage seeded by this file.

| ID | Tier | New / amended | Craft scope | Deps | Done when (by looking) |
|---|---|---|---|---|---|
| T0 | TASTE-HIGH | amended | Adopt this pass's tokens (the "Motion values" table) as `J/journeyMotion.ts` plus CSS custom properties; beat sheets §4.2; the copy in §4.2 | — | Each token names its hero source line; a grep of `J/` finds no `ms` or `cubic-bezier` literal outside the tokens; the §4 opening doesn't repeat the hero |
| H0 | NORMAL | amended | Capture ids: `pull-app`, `pull-agent`, `pull-interrupt` (App→Agent switch, then scroll at 300 ms), `back-2-1`, `fold`, `back-3-2`, `grow`, `back-4-3`, `flick` (hero→§4), `s2-demo`, `s3-demo`, `s4-demo`, `finale`, each also `-rm`. The three scroll profiles; deterministic blink seeds | P1 | All ids record at D and P from one command; reruns give identical stills |
| S2 | XHARD (+Opus) | amended | §1.1 mechanics: same function lists, origin kept, chat clip-path band, launcher growth reuse, Agent-route ordering with no depth crossing, sibling labels and pillars, phone ortho slabs, reduced-motion static stack plus dip | T0 | `pull-agent-D-480` shows no plane cutting another; `pull-interrupt-D` has no jump or blank frame; one WebKit run of `pull-app-D` matches Chromium |
| T3 | XHARD | amended | Trigger lines 66/72% (phone 78/83%) and leave-hero 10/4%; retarget, never queue; the 120 ms floor for secondary effects; fast-forward rules (§4.1); a stepped "Show the steps" mode on the beat data | T0 | `flick-D` and `flick-P` show no stack, tray or label flash; `back-2-1-D` lands on §2's end state with Replay |
| T5 | XHARD | amended | Leave-hero beat (§1.2: vacuum retract, tilt eased to 0 before unmount, preview playing); stage frame dissolve and re-form hooks; phone pin-and-scale with no jump | S2, T3 | `pull-app-P` shows no jump of the stage or the text below; slow scroll between 10% and the trigger shows the hero at rest, still playing |
| T6 | TASTE-HIGH | amended | Headers: the eyebrow types on; headline and sub never animate; section scroll lengths (§4.1); phone composition of every section (§5.1) | T5 | `pull-app-D-1320` and `pull-app-P-1320`: header readable and sticky beside the settled stack; no title or spine collision at D, P, N and S |
| T8 | TASTE-HIGH | amended | The pull-apart and its reverse (§1.3), from App and Agent, at D and P, plus the reduced-motion dip | S2, T6, H0 | Signs off `pull-app-D-0/240/600/1320`, `pull-agent-D-0/300/600/1320`, `pull-app-P-1320`, `back-2-1-D` and `pull-app-D-rm` against `night/02a` and `day/02b` at 2×. It reads as the hero coming apart, not a cut to a new scene |
| T10 | NORMAL | amended (restored) | One flat overlay layer with computed positions (mink, cursor, markers, flash rectangles, cable), plus `PixelSprite`: strips, the 70 ms tick, one-shot/loop/hold, device-pixel `--px`, rest snapping, hop arc, pop in/out, reduced-motion frame, glyphs | T0, A5a | `s4-demo-D` and `-P` stills at DPR 2: every sprite pixel is a uniform k×k block in the 4 mink colours (Playwright pixel check); the mink stays with a gliding clip in `s4-demo-D` |
| T11 | NORMAL | amended | Spine: `astrid-rise` entrances, older turns at .55, a pixel ellipsis replacing the spinner (host CSS), reserved height, chip slot timed to the edit's end | T1, T3, T28 | `s4-demo-P` shows no spinner and no layout shift as turns arrive |
| T12 | TASTE-LOW | amended | The look of every primitive: stamp, lit layer, chip receipt and flood, typed line and check, History row, tabs, Replay, the Departure Mono 11 px device | T11, T28, H0 | `s2-demo-D` at the stamp peak, `s4-demo-D` at the flood, and the `-P` equivalents are legible in both palettes; the highlight is text plus dot |
| T14 | NORMAL | amended | Auto-cycle **once** (6 s a tab), rest on New model, first click stops it; progress line; pillar conduits; the cable from an anchor measured once | T3, T8, T28 | `s2-demo-D` ends on New model and stays still; resizing re-anchors the cable once |
| T15 | TASTE-LOW | amended | Example panels: 3D camera sway ±18° on an 8 s period, code typing, waveform reveal, markers, install log, tab-swap motion, the conduit order (cause → light → stamp) | T13, T14, T12 | `s2-demo-D` and `-P`, one still per tab at +2600, against `02a`, `02b` and `02c` at 2× |
| T17 | NORMAL | amended | Tray: cards stay; develop, reframe (explicit width and height), play once, drop line, then the clip appears; offscreen videos stop | T1, T3, T28 | `s3-demo-D-9200` shows drop lines and no flying clones; only one video plays at a time |
| T18 | TASTE-HIGH | amended | The fold (§1.4) and every §3 beat (§4.2) at D and P | T8, T15, T17, T10 | Signs off `fold-D-0/420/840/1200`, `s3-demo-D` stills (3rd still in, mid-reframe, 3rd landing, mink on clip) and `fold-P`, against `03a` and `03c` at 2× |
| T19 | NORMAL | amended | Cursor states; History append, shift and tint; the phone ticker; marker rise; flash rectangles; wedge, level and dimension strokes | T1, T3, T10, T11, T28 | Each History row matches its snapshot in `s4-demo-D` and `-P`; the ticker shows one row at a time |
| T20 | TASTE-HIGH | amended | The grow (§1.5) and the §4 beats, starting right after the foundation | T9, T19 (the grow after T18) | Signs off `grow-D-0/420/840`, `s4-demo-D` stills (trim, mid-carry, 2nd snip, flood, mid-retime, end) and `s4-demo-P`, against `04a`, `04b` and `04c` at 2× |
| T21 | XHARD | amended | Sky progress quantised to 1/48 steps; the held palette committed at section boundaries with a 720 ms `settle` colour transition on journey text and panels (no view transition during scroll); reduced motion steps once per section | S4, T3, T5 | `finale-D` shows visible pixel steps and no colour pop at boundaries; `finale-D-rm` steps per section |
| T22 | TASTE-HIGH | amended | The finale: the reveal reused, the mink at the horizon, look-up at progress ≥ .98, no sparkle | T6, T21, M1 | Signs off `finale-D` and `finale-P` at the peak and the look-up frame against `05-finale` at 2× |
| T24 | NORMAL | amended | "Show the steps" / "Pause" button and its focus; the segmented tab keys; Replay labelling | T3, T28 | `s4-demo-P-rm` shows the stepped story with only opacity changes; keyboard tab order checked in a recording |
| R2 | TASTE-HIGH (review) | amended | Adds the §4.3 cut list and the reduced-motion "Show the steps" to its three checks | all above | Each cut item is confirmed absent; findings tiered |
| **T28** | NORMAL | **new** | Shared motion primitives reading only T0 tokens: typed line, stamp, chip receipt, flash, History row, pixel ellipsis, Replay, the reduced-motion slideshow | T0 | Unit tests for step counts, timings and reduced-motion paths; first visual check is T12's stills |
| **M1** | TASTE-HIGH | **new** | Every mink cue and glyph (§3.2), placement and frame choice at D and P, holding back (§3.3); pass 1 on A5a placeholders, pass 2 on A5b–A5h | T10, A5a; cue slots from T15, T18, T20 | One still per cue in `s2/s3/s4-demo-D` and `-P` and `finale-D`: charming, never covering a label, chip or cursor; "!" and the sparkle appear once each across the full recordings |
| **A5a** | ASSET | **new** (replaces A5) | Placeholder kit from existing art with no resampling (§3.4): front ÷4 nearest, juggler crops, the run strip, spark and thought glyphs; a JSON per strip (frame size, count, anchor, ms) | — | Every cue in §3.2 has a mapped placeholder rendered in H0 at D and P |
| **A5b** | ASSET | **new** | `sit`: 2 frames, 40×56 | A5a | `pixel.strip` passes (density matches the runner, 4-colour palette, 1 px outline, fixed anchor); seen at 2× in `s4-demo-D` and `-P` |
| **A5c** | ASSET | **new** | `carry`: 6 frames, 80×56 | A5a | Same check, in the carry still |
| **A5d** | ASSET | **new** | `push`: 4 frames, 81×44 (the runner's frame) | A5a | Same check, in the §2 New model and §4 retime stills |
| **A5e** | ASSET | **new** | `snip`: 4 frames, 56×56, snip lines baked in | A5a | Same check, in the 2nd-snip still |
| **A5f** | ASSET | **new** | `plug`: 5 frames, 48×64, plug from the prop palette | A5a | Same check, in the beat-sync still |
| **A5g** | ASSET | **new** | `lookup`: 3 frames, 48×80 | A5a | Same check, in `finale-D` and `-P` |
| **A5h** | ASSET | **new** | "!" mark: 3 frames, 5×12 | A5a | Same check, in the §4 trim still |
| **A9** | ASSET | **new** | Pixel icons as 16×16 grids in `H/PublicAstridPixelIcons.tsx` format: monitor (Local), cloud, wrench (chip) | — | Crisp at D and P in `s3-demo` and `s4-demo` stills; both palettes |

**Count:** 11 new (1 TASTE-HIGH, 1 NORMAL, 9 ASSET) and 20 amended (7 TASTE-HIGH including R2, 2 TASTE-LOW, 7 NORMAL, 4 XHARD). The original A5 line is replaced by A5a–A5h. **Phase placement:**
- phase 0: T0, H0, A5a, A9;
- phase 1: T28, A5b–A5h;
- with §2 and §4: T10, then M1 pass 1;
- M1 pass 2 once A5b–A5h have landed and the owner has looked on a phone, before R2.
