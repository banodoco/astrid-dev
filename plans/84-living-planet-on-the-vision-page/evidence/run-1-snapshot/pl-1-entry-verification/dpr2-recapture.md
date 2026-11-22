# Fixed-contract poster handoff recapture

Date: 2026-11-22. This recapture supersedes the earlier handoff image settings while preserving those original files. It used Chrome for Testing `153.0.8010.12` via the same SwiftShader wrapper and the same saved feed (`feed-response.json`, SHA-256 `71ed54ff1930a69645382cb21e3578bc90c26027aa1d5f0e8905c934ca16f35d`). Both contexts used DPR 2 and `isMobile: false`; laptop had no touch and phone had touch enabled. Both navigated with `?planet-test-pose=fixed`.

The engine module request was held after title/content readiness. Before capture, the script awaited `document.fonts.ready`, all finite hero subtree animations, then required eight consecutive animation frames with stable hero/planet geometry and unchanged scroll. It recorded scroll, visual viewport, hero/copy/title/stage rects, offset positions, and computed transforms immediately before releasing the module and after the poster disappeared. The observer recorded raw layout-shift entries but no conclusion relies on CLS filtering.

| Context | Viewport | Scroll before/after | Stage before and after | Stage geometry delta | Poster removed (performance ms) | Errors |
|---|---:|---:|---|---|---:|---:|
| Laptop | 1440×900 | 0 / 0 | x=1020, y=262, 260×400 px | x=0, y=0, width=0, height=0 | 20275.7 | 0 |
| Phone | 390×844 | 0 / 0 | x=99.9375, y=438.046875, 190.125×292.5 px | x=0, y=0, width=0, height=0 | 3491.0 | 0 |

Both hero and stage transforms were `none` before and after. The poster existed before import release and was absent after `onReady` removed it; `planetEngine.ts` calls `onReady` immediately after its first `renderer.render`. Thus the earlier -14 px phone delta was not reproduced after the loading/hero state was settled. These captures show no scroll or rect movement across the poster-to-first-draw interval; this conclusion comes from the recorded geometry, not an exclusion in CLS scoring.

Final artifacts:

- Laptop: [poster frame](laptop-handoff-dpr2-poster.png), [first-draw frame](laptop-handoff-dpr2-live.png), [raw metrics](laptop-handoff-dpr2.json).
- Phone: [poster frame](phone-handoff-dpr2-poster.png), [first-draw frame](phone-handoff-dpr2-live.png), [raw metrics](phone-handoff-dpr2.json).

The earlier DPR-mismatched images remain unchanged. Intermediate DPR 2 captures with an observer setup error or without saved settle counts are retained with `observer-error` and `prior-no-stability` suffixes; use only the four final images and two final JSON files above.
