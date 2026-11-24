# Editor preview turns sub-pixel motion into jitter and a flickering edge line

The editor preview shows motion that the film does not have.

## Repro
- Editor: http://localhost:2400/tools/video-editor?project=801a01b3a87941a1ab25958c488afdbf&timeline=77f906f3242c48179ab86ca7c3e62eb4 (release-14-plan-69 stack).
- Revision: authoring-parent-revision-7cf9153c… (before the fix 606c2a92…), window 108.07–110.27 s (frames 3242–3307), clip `d-typing`. It is an `am-footage` element with zoom 2.4 → push.to 2.46 and focus (1, 1). The source is a 1920x1080 static UI recording with a vertical divider at source x 1619.74 (std 0.01 px over the window).
- Seek: walk the React fiber from `[data-preview-revision]` up to `RemotionPreview`'s `useRef<PlayerRef>`, then call `pause()` and `seekTo(f)` for each frame. `getCurrentFrame()` matched the target on all 318 captures.
- Viewports tested:
  - 1440x900: the Player is 742x417.4 inside a 742x477.8 box, `matrix(0.386458)`, with 30 px cream letterbox bars top and bottom.
  - 3840x2160: the Player is 2283x1284 inside a 3142x1284 box, `matrix(1.18912)`, with 429 px side bars. These are the "white bars" the owner saw. They are editor layout, not film.

## Measured (divider x, darkness-weighted centroid)
| Path | Divider motion over 66 frames | Frame-to-frame | Edge line |
|---|---|---|---|
| Expected (am-footage maths) | 1200.0 → 1182.0 comp px, linear | −0.277 px every frame | none |
| Render path (Chrome harness, `<img>` at 1:1, like OffthreadVideo in render) | 1200.33 → 1182.38, monotonic, 0 sign flips | −0.10 … −0.41 | last column 234 and last row 205, constant |
| Preview at 1440 | 462.42 → 455.70 screen px | ±0.3–0.85 screen px alternating, 42 sign flips in 65 steps | last row (y 447) flips between 205 and **85** from frame to frame |
| Preview at 3840 | 1200.3 → 1182.2 comp px in stair steps (hold 2 frames, jump 0.84) | 8 flips | last column (x 2712) flips between 235 and **117** in a 3-frame pattern |

## Cause
- Remotion's `OffthreadVideo` draws a `<video>` in the Player (`remotion/dist/cjs/video/OffthreadVideo.js:39-43` → `VideoForPreview`). In render it draws an `<img>` of the exact frame (`OffthreadVideoForRendering`).
- In the preview, the fractional `left/top/width/height` that change every frame sit under the Player's CSS scale. Chrome snaps the composited video layer to device pixels, which matches the measured steps. The snapped video edge then misses the box edge by a sub-pixel, and the `background` (#0C0906) shows through as a 1 px dark line that flickers.
- This is inferred from the measurements and the code path. I did not read Chromium.

## Second preview/render mismatch
- When an asset has no registry resolution and a non-16:9 aspect (RAW-H3, 1344x768), am-footage falls back to a 1920x1080 box.
- The preview `<video>` (object-fit contain) then pillarboxes it, about 15 px per side by calculation. Render `<img>` (fill) stretches it 1.6 %.
- This is inferred from the code. I did not capture it.

## Suggested fixes (editor/element side, not done)
- A 1:1 "actual size" preview toggle.
- `?frame=N` and a debug `seekTo` handle.
- In am-footage, snap `rect` to whole composition pixels when nothing is animating, or round `x/y` while keeping `w/h`. That would be a Personal/project-pack variant, not an edit to the built-in.
- Read `videoWidth/videoHeight` when the registry has no resolution.
