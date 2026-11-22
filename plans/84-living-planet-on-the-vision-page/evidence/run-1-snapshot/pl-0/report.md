# PL-0 donor trial evidence

**Result:** unchanged donor copy builds and runs. This is a local software-GL trial, not a phone or laptop hardware measurement. It does not select a phone rendering policy. The manager opened and judged the five DPR-2 captures in [manager-verdicts.md](manager-verdicts.md).

## Source and copy

- Donor repository: `/home/user/codex/planet84/planet`, `main` at `037293dedf932cd12eb7ef2568017b9196b76c32`, clean status at start and end.
- Task copy: `/home/user/codex/planet84/worktrees/pl-0`; created with `git archive` from that exact SHA. All 19 tracked donor blobs match the copy exactly; see [source-integrity.json](source-integrity.json). Npm created an untracked lockfile and installed build dependencies only in this copy. Its static build is [`dist/`](/home/user/codex/planet84/worktrees/pl-0/dist).
- Dependency cache/log location: `/home/user/codex/planet84/worktrees/pl-0.env`.
- Donor source files were not changed; no product code was added.

## Build and preview commands

| Command | Exit | Result |
|---|---:|---|
| `git -C planet archive 037293dedf932cd12eb7ef2568017b9196b76c32 \| tar -x -C worktrees/pl-0` | 0 | Isolated source copy |
| `npm install --legacy-peer-deps --cache /home/user/codex/planet84/worktrees/pl-0.env/npm-cache` (cwd `worktrees/pl-0`; there is no `package-lock.json`, only `bun.lock`) | 0 | 189 packages added; audit reported 0 vulnerabilities |
| `npx vite build` (cwd `worktrees/pl-0`) | 0 | Vite 8.3.8 production build; JS 979.03 kB (266.22 kB gzip), CSS 21.97 kB (5.71 kB gzip) |
| `npm run preview -- --host 127.0.0.1` | started | Local preview `http://127.0.0.1:4173/`; logs at `worktrees/pl-0.env/logs/preview.log` |
| `node run/evidence/pl-0/capture.cjs` | 0 | Five full-page DPR-2 screenshots |
| `node run/evidence/pl-0/measure.cjs` (resumed missing phases from persisted JSONL) | 0 | 12 timed conditions; exact current results in `measurements.json` and raw arrays in `measurements.jsonl` |

The successful install and build logs and statuses are under `worktrees/pl-0.env/logs/` and `run/evidence/pl-0/`. A previous screenshot launch failed because Playwright's expected headless-shell cache was absent; no browser was installed. Under the manager's instruction, the final runs used the existing `/usr/bin/google-chrome` executable directly. The brief's initial default-path launch attempt and the corrected run are recorded in `capture-attempt-1.json` and `browser-launch.*`.

## Runtime and measurement method

- Host: Intel Xeon Processor @ 2.10 GHz, 4 online CPUs / threads, KVM; `MemTotal` 16,473,744 kB, `MemAvailable` 15,163,080 kB at capture. See [lscpu.txt](lscpu.txt) and [memory.txt](memory.txt).
- Browser: Google Chrome for Testing 153.0.8010.12 (`/usr/bin/google-chrome`), Playwright 1.60.0.
- Pinned flags: `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist` (plus `--no-sandbox` for this headless container).
- Actual renderer reported by WebGL: `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)`.
- Performance viewports: 390×844 phone portrait and 1440×900 laptop, DPR 1. At each viewport, CDP `Emulation.setCPUThrottlingRate` was set to 1, 4 and 6. Each scrolling and spinning/dragging condition ran for about 15–16 seconds.
- Scrolling alternated wheel input over the page/canvas; observed page scroll range was 0–300 px. Spinning held a mouse drag on a canvas hit-tested point for the measurement interval. Rows include pointer-down/move/up counts and the hit-test. Laptop 1x drag delivered 22 canvas moves over 16.07s; the manager accepted it as a valid drag sample, and the low input delivery is retained as a limitation.
- The page's own `requestAnimationFrame` callbacks and actual renderer submissions are distinct. The donor schedules its software-GL frames via `fenceSync` + polling + an 80 ms `setTimeout` floor (`src/planetEngine.ts` around 8400–8417 and 8863), after an initial RAF. Therefore no page-owned RAF intervals were observed in the timed windows; these are reported as **no samples**, not as a zero-ms frame time. Actual-frame intervals are consecutive target-canvas WebGL2 `fenceSync` submission timestamps. Fence signal latency is separately recorded and is quantized by the donor's 5 ms polling. Draw calls per rendered fence are counted by instrumenting WebGL2 draw methods. This did not change donor source code.
- The measurement script records its raw arrays, counts, CPU rate, duration, pointer proof and scroll range before evaluating interaction checks. Summary percentiles use nearest-rank p50/p90/p95/p99 and report sample counts.

## Actual render-frame distributions

Times are milliseconds from one actual WebGL frame submission to the next. Draw calls/frame are intercepted WebGL draw calls, not Three.js `renderer.info` values.

| Viewport | CDP CPU rate | Activity | Seconds | Frames | p50 | p90 | p95 | max | Draw calls/frame p50 |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| phone-portrait | 1x | scroll | 15.29 | 44 | 348.8 | 386.5 | 391.8 | 416.6 | 1530 |
| phone-portrait | 1x | spin | 15.73 | 44 | 346.9 | 383.1 | 390.0 | 410.4 | 1514 |
| phone-portrait | 4x | scroll | 15.38 | 34 | 446.6 | 497.5 | 506.4 | 516.8 | 1559 |
| phone-portrait | 4x | spin | 15.69 | 35 | 448.6 | 484.7 | 492.8 | 517.4 | 1556 |
| phone-portrait | 6x | scroll | 15.36 | 32 | 475.3 | 513.6 | 549.7 | 559.8 | 1668 |
| phone-portrait | 6x | spin | 15.38 | 32 | 477.4 | 519.6 | 553.7 | 554.7 | 1678 |
| laptop | 1x | scroll | 15.60 | 20 | 775.5 | 838.7 | 865.9 | 1057.1 | 1311 |
| laptop | 1x | spin | 16.07 | 21 | 760.1 | 800.9 | 835.3 | 850.3 | 1291 |
| laptop | 4x | scroll | 15.14 | 15 | 1035.8 | 1124.9 | 1140.0 | 1140.0 | 1338 |
| laptop | 4x | spin | 16.67 | 16 | 1039.3 | 1087.8 | 1102.7 | 1102.7 | 1343 |
| laptop | 6x | scroll | 15.41 | 15 | 1058.2 | 1164.5 | 1167.4 | 1167.4 | 1225 |
| laptop | 6x | spin | 16.01 | 15 | 1052.7 | 1110.5 | 1242.3 | 1242.3 | 1201 |

Phone p50 was about 347–349 ms at 1x, 447–449 ms at 4x and 475–477 ms at 6x. Laptop p50 was about 760–776 ms at 1x, 1,036–1,039 ms at 4x and 1,053–1,058 ms at 6x. These values reflect this host's software GL, headless browser, and donor's built-in 80 ms scheduling floor; they are not equivalent to a physical phone's or laptop's frame rate. No per-device thermal readings exist. The app's GPU-memory totals were not exposed without modifying the donor engine; browser JS heap/GPU residency is not claimed. Draw-call counts were obtainable and are reported above.

## Pictures and motion

Full-page DPR-2 captures: [`phone-portrait-dpr2.png`](phone-portrait-dpr2.png), [`phone-landscape-dpr2.png`](phone-landscape-dpr2.png), [`tablet-dpr2.png`](tablet-dpr2.png), [`laptop-dpr2.png`](laptop-dpr2.png), [`wide-dpr2.png`](wide-dpr2.png). Measurement-only DPR-1 spin before/after captures are named `<viewport>-cpu<rate>-spin-before.png` and `...-after.png`.

### Real-time motion clips and workload supplement — 2026-11-22

Two additional diagnostic clips were recorded from live CDP screencast frames at CPU 1x, DPR 1. Frame timestamps are retained in `screencast.json`; there is no interpolation or sped-up synthesis. The script issued wheel input before dragging the canvas, but did not record scroll offsets. In the manager-opened samples the title is at effectively the same position in both scroll-labeled frames, so page movement is unproven. The phone clip is [`motion-phone-portrait-cpu1x.mp4`](motion-phone-portrait-cpu1x.mp4) (8.48 s by ffprobe); its three samples are [`key-1-scroll`](recordings/phone-portrait/key-1-scroll.jpg), [`key-2-scroll`](recordings/phone-portrait/key-2-scroll.jpg), and [`key-3-spin`](recordings/phone-portrait/key-3-spin.jpg). The laptop clip is [`motion-laptop-cpu1x.mp4`](motion-laptop-cpu1x.mp4) (8.48 s by ffprobe); its samples and full raw screencast frames are retained under `recordings/laptop/`. A first laptop pass at 11.76 s was retained under `attempts/laptop-overlong-pass1/` before making the in-range replacement. The manager opened all six keyframes: spin motion visibly moves the lake, windmill, and balloons while preserving the world; copy overlap persists. These are donor diagnostics only, not owner visual-quality recordings and not evidence of smoothness or native-GPU performance; see `manager-verdicts.md`.

The short motion run also collected an instrumented workload sample: phone p50 was 1,700 intercepted WebGL draw calls and 127,896 estimated triangles per submitted frame; laptop p50 was 1,704 draw calls and 128,008 estimated triangles. Intercepted texture allocation calls summed to an estimated 4,299,772 bytes for the phone session and 19,920,892 bytes for laptop. These are call-derived estimates, not GPU residency or total texture memory; formats or allocations outside the interception may be absent. Runtime renderbuffer estimates are also recorded in `screencast.json` and are not GPU-memory totals.

The source workload sets hardware renderer pixel ratio to `min(devicePixelRatio, 2)` and forces 1 for recognized software GL (`src/planetEngine.ts`, lines 6676–6700). The source configures the sun shadow map to 2,048×2,048, but the software-GL path disables shadow rendering and sun casting, so that configured size was not an active shadow allocation in this trial. Its optional pixel-filter render target is 260 px high, with width derived from stage aspect and clamped to at least 160 px (`src/planetEngine.ts`, lines 8144–8153 and 8363–8375); runtime allocation/residency was not measured. Therefore neither the software-GL timing matrix nor this workload probe predicts absolute phone performance.

**Phone policy revision, 2026-11-22:** default to a lighter live planet, with renderer pixel ratio capped around 1.5, reduced or no shadows, fewer draw calls, and lower-cost mink rendering. PL-5 should step quality down and then fall back to the still poster if measured device frame time remains poor for a few seconds. Keep the still path for reduced motion, unavailable/lost WebGL, data saver, and a slow first frame. This revision supersedes the earlier still-by-default ruling, which used absolute SwiftShader timings incorrectly. The owner asked us to proceed without named-phone measurements; those values were replaced by local 1x/4x/6x CPU profiles, so actual owner-phone behavior remains unmeasured. The software-GL timings are only a relative cost meter between variants on the same backend and pose.

## Preserved attempts and limits

- The first meter draft rejected a 47-frame/15-second phone sample due to an arbitrary 50-frame gate. Its log and disposition are in `measure.log` and `attempt-1-failure.json`; it did not persist raw arrays.
- The next run persisted eight conditions, then stopped on an arbitrary 30-pointer-move gate after the validated laptop 1x drag delivered 22 moves. The manager ruled that sample valid. It is recorded in `measure-rerun.log`, `attempt-2-failure.json`, and `measurements.jsonl`. The resumed run skipped existing valid rows and collected the remaining laptop rates; final status 0.
- There are no real owner-device numbers, no thermal measurements, and no conclusion here about phone rendering policy. Static donor visuals show the donor's own phone/nav/copy overlap defects; the manager's review records what to preserve and what not to copy.
