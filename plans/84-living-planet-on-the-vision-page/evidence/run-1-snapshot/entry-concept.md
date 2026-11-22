# The planet's entrance: concept

Read from the mock-up's code (`src/planetEngine.ts`), the plan (PL-4, PL-10, Completion) and the sky session (`publicAstridSkySession.ts`). Nothing was built or run; every number is a starting value to tune by eye.

**The idea in one line.** The words are there, the sky settles, and then the camera comes down out of the sky toward a small, whole planet, swings round its shoulder in the direction the day turns, and stops where the planet rests. Only the camera moves. The planet's own rotation, which is the hour, is never touched.

## Facts the concept rests on

- The engine's camera never moves. It is set once to position `(0, 1.45, 12.6)` looking at `(0, 0, 0)` (lines 6706–6707). In orbit terms the rest pose is: target origin, radius 12.68, azimuth 0°, elevation 6.57°.
- Everything a visitor "spins" is `planetGroup.quaternion` (drag, inertia, idle drift, `rotateToLandmark`, `setTimeOfDay`). Under PL-10 that quaternion is the hour.
- The lights are fixed in the world, not on the planet or the camera, and the sun always sits on the resting camera's side. So orbiting the camera changes which part of the lit face is seen; rotating the planet does not.
- Field of view is computed from a constant `dist = 12.6` (line 8349), not from where the camera really is. So moving the camera back makes the planet smaller by exactly `12.68 / radius`, and the view offset keeps the planet's centre on the same screen point throughout.
- A later hour moves the surface right to left on screen. A camera whose azimuth rises from negative to 0 makes the surface drift the same way.

## 1. Beats

Times are from the page's first paint. `G` is the moment the entrance starts.

| When | Words | Sky | Planet |
| --- | --- | --- | --- |
| 0 | Rise as today (70–780 ms). Untouched | Reveal starts (1,800 ms, cubic ease-out), unless already done on an earlier page | Nothing drawn. Canvas is transparent and at opacity 0. The engine's code starts downloading at once |
| ~1,000 | Settled | 90% revealed; what remains is slow | Engine is built now, not earlier: its build is one long block of work and the sky's reveal is drawn frame by frame, so building sooner would make the sky stutter. One hidden warm-up frame is drawn at the rest pose (compiles every shader and shadow), then the camera is put at the start pose |
| `G` ≈ 1,300–1,600 | Still | Finishing | **Appear, 0–260 ms:** canvas opacity 0 to 1 while already moving. The planet is small (about half size), whole, seen from above and from the left |
| `G` + 0–900 | Still | Done at 1,800 | **Approach:** most of the distance is covered; it grows fast, then slower |
| `G` + 600–2,000 | Still | Still. The hour does not change | **Arc:** the camera swings round and comes down to eye level. The lit face rolls into view; the planet grows past the hero's top edge and becomes a place, not an object |
| `G` + 2,000–2,200 | Still | Still | **Settle:** the last two or three degrees, slowing to nothing. At `G` + 1,950 the minks nearest the centre glance up once |
| `G` + 2,200 | | | Landed. Spinning is fully live. Idle drift waits its usual 3.6 s |

Total move: 2,200 ms on a laptop; lands about 3.6 s after first paint.

**The first frame and the poster.** The entrance's first visible frame is the live planet, small and far, at 0% opacity over the already-revealed sky. It is not the poster. A poster at rest that then gives way to a planet flying in from far away cannot be made invisible, so in the normal case the poster is never shown: the sky is what is there until the planet appears, and the sky is not an empty box.

The poster appears only where it is the end state (reduced motion, no WebGL, failed load, lost context) or when the engine is late: if the planet is not ready 3,000 ms after first paint, the poster fades in over 400 ms at rest. When a late engine then becomes ready, it takes over with a **wake**, not a fly-in: the live camera starts at rest radius and elevation but azimuth −14°, so the globe's outline sits exactly on the poster's; the canvas fades in over 240 ms, the poster fades out from 200 to 360 ms, and the camera eases the last 14° over 900 ms (cubic ease-out). The outline never changes, and the motion hides the difference in surface and light between the poster's hour and the real one. A fade without motion would show two planets.

## 2. The camera path

Add an orbit state to the engine: `target` (origin), `radius`, `azimuth` (about world Y, 0 at rest, positive toward +X), `elevation`. Position is `target + radius · (cos e · sin a, sin e, cos e · cos a)`, then `lookAt(target)`. The entrance writes offsets on top of the rest pose and reads the rest pose every frame:

- `radius = rest.radius · (1 + kR · (1 − Er(u)))`
- `azimuth = rest.azimuth + a0 · (1 − Ea(u))`
- `elevation = rest.elevation + e0 · (1 − Ee(u))`

`u` is 0 to 1 over the duration. At `u = 1` every offset is zero, so it lands on whatever framing PL-3 gave that size, and a resize or rotation of the device mid-move just works. Field of view, zoom and view offset are not animated.

Laptop values: `kR = 1.1` (start radius 26.6, planet at 48% of its resting size; keep radius under about 38 because the far plane is 45), `a0 = −64°`, `e0 = +17.5°` (start elevation 24°).

Easing, one continuous move with three channels that overlap, never three moves end to end:

- `Er` (distance): quartic ease-out, `1 − (1 − u)^4`. Fast in, long glide. No easing in: the planet appears already under way.
- `Ea` (the swing): `cubic-bezier(0.45, 0, 0.15, 1)` on `u`. Slow to start, most of the turn between 30% and 85%, long tail.
- `Ee` (the descent): sine ease-in-out over `u` from 0.15 to 1.

So it reads: come in, then swing round the planet's left shoulder and down, anticlockwise seen from above, 64° in all. No overshoot, no spring, no roll, no change of field of view. It flies past nothing staged; the balloon and castle may cross, and that is enough.

## 3. Per size, and when to shorten or skip

| Size | `kR` | `a0` | `e0` | Duration |
| --- | --- | --- | --- | --- |
| Wide, laptop | 1.1 | −64° | +17.5° | 2,200 ms |
| Tablet | 0.9 | −52° | +15° | 2,000 ms |
| Phone sideways | 0.7 | −44° | +8° | 1,800 ms |
| Phone upright | 0.6 | −36° | +10° | 1,600 ms |

Phones get less swing because the planet sits closer to the words, and less time because the engine is ready later. Sideways gets little descent because there is little height. Use PL-3's size classes, not new breakpoints.

- **Reduced motion:** poster only, no engine, no move.
- **Late engine (after 3,000 ms), slow device** (warm-up frames over about 40 ms, software drawing, or PL-5's lowest tier): the 900 ms wake, or a plain 300 ms fade at rest if there is no poster up.
- **Visitor acts mid-move** (pointer down, touch, wheel, scroll, any key): hurry. The rest of the path plays in at most 320 ms with an ease-out. Never snap, never swallow the input: the page scrolls and the drag starts at once.
- **Three frames in a row over 50 ms mid-move:** hurry, the same way.
- **Tab hidden** at `G`: wait. Hidden mid-move: finish at rest silently.
- **Page not at the top** (scrolled past about a third of the hero at `G`, or opened on a section link): no move; fade in at rest over 300 ms.
- **Second time in the same visit** (back from another page): fade in at rest. Keep the "played" flag beside the sky session, which already lives for the whole visit and already makes its own reveal happen once.
- **A pillar card, Pause or Still pressed mid-move:** hurry to rest, then do what was asked.

## 4. Minks, the place, and the authored touches

The minks and places do nothing special; the world is already going about its day when the camera arrives, and that is the point. Two touches only:

1. **They notice.** About 250 ms before landing, the two or three minks nearest the centre of the visible face glance toward the viewer once, using the existing `setGlanceToward` (the same glance the pointer causes). Nothing else reacts.
2. **The turn agrees with the day.** The swing moves the surface the way a later hour does, so it looks like the world rolling forward to now and stopping. And because the lights stay with the world, the lit face rolls into view as the camera comes round: in the morning the planet visibly waxes; in the evening it is lit all the way. Neither costs any code beyond moving the camera, not the planet.

## 5. How to tell it is right

Look for:

1. The planet's centre stays on one screen point for the whole move (within a few pixels). Only its size, its facing and its light change.
2. Size only ever grows; speed only ever falls in the last 400 ms; the last frame of the move equals the fixed-pose resting picture within PL-1's tolerance; idle drift does not start with a kick.
3. The hour never moves: `onTimeChange` and the session's hour are not called or changed, and the sky's pixels are the same before, during and after.
4. A drag started mid-move takes hold within one frame and the planet is spinnable from where it is; the headline's rectangle is identical in every frame and measured layout shift is zero.

It is wrong if:

1. It reads as a picture being scaled up: no change of facing, no light rolling across, or the light glued to the surface (a sign the planet was rotated, not the camera).
2. There is a blink at the start: one frame at rest before the jump to the far pose, the poster and the live planet both visible as a double image, or a square of canvas colour.
3. It bounces, overshoots or stops dead and then lurches into idle drift; or the sky or page colours shift during the arc.

## 6. What in the code makes this hard

- **There is no camera state.** The position is set once and `dist = 12.6` is a separate constant in the projection code. Introduce one rest pose (radius, azimuth, elevation, target) that both use, and keep field of view tied to the rest radius, not the live one: if someone "corrects" that, the fly-in disappears. Pin it with a test.
- **Drag assumes the camera is on +Z.** Yaw is about world Y (fine at any azimuth), pitch about world X (wrong mid-arc). Use the camera's right vector for pitch; at rest it is the same axis. `rotateToLandmark` also assumes the rest view: queue it until landing.
- **The first frame.** `onReady` fires after the first draw, and the mock-up fades its placeholder on that. Set the start pose before the first visible draw, keep the canvas at opacity 0 for the warm-up frame, and start the clock only after two frames under 34 ms.
- **The clock.** `dt` is zero when paused and 0.35× under reduced motion, and `rawDt` is unclamped. Drive the entrance from its own clamped real time, so Pause cannot freeze the camera mid-arc and a hitch slows the move without making it jump.
- **Software drawing** runs on a timer loop at a low rate, and CI uses it. The entrance is skipped there, so recordings need a test hook: force `full`, `wake` or `none`, and set `u` directly for still pictures at 0, 0.3, 0.6 and 1.
- **Idle drift and inertia rotate the planet,** which under PL-10 is the hour. Hold both off until landing; whether drift should move the hour at all is PL-10's question.
- **The engine's build blocks the main thread** while the sky's reveal is drawn frame by frame. Hence building at about 1,000 ms; measure it, and split the build if it is still felt.
- **One poster, many hours.** The poster has one rotation and one light; the live planet arrives at the sky's hour. The wake hides this for a late engine, but the still cases will show a planet lit for an hour the sky may not be showing.
