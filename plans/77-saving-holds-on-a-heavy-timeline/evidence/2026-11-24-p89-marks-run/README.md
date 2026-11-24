# Plan 89 per-stage save marks (SV-L13 instrumented App), one repetition, 24 November 2026

Package: astrid-dev `release-15/p89-marks-command` head `108c0fb145d4a90c7a51216755bf6cd73d053ec6` (tree `db6207388af72cebf0576c4061f28303032d42e5`, digest `cc56d2a546a0a1e2d610f0cc3a8b17c7e3116f35d526588cfa09cfde0286b137`), reviewed before running: it differs from `ee89f2ed` only in the App SHA (`build-app-svl2.sh`, `run-sv3-overlay.sh`, `browser-sv3-measure.mjs`, README). App `092013f3b88e9d49e48102630951a40a450c4868` (astrid-app draft PR #395, branch `p89/SV-L13`, tree `5195e52b2ccfd52e2679c06e6912ea1ddfb063e9`; `package.json`, `package-lock.json` and the vite config byte-identical to `9f26112d`; the diff is marks-only, 7 files). Runtime `c8b861c770aa58fd0392fe2dcefbda9ce23c84d1`, Agent `096a2fb3536192785fabd33e6673ba8ab4ef5ead` two-file overlay, `SV3_REPETITIONS=1`, no sampler. Phase `verified`, 34 commit POSTs, 0 failed drags, 0 refusals, all HTTP 200, 18 warm saves and one cold, no ambiguous trace; idle-safe stop verified, ports closed, no Chrome, boundaries unchanged; disk minimum 16.58 GiB. The script exits 1 at the missing timing sink after the measurement, as in the earlier runs (`run-stdout.log`).

## The main finding: 24 of the 46 new marks never recorded (App defect, not a run problem)

Every save's trace holds the same 22 marks: the four baseline marks and 18 new ones (`snapshot-*`, `draft-write-*`, `capture-*`, `debounce-*`, `attempt-build-*`, `capture-wait-*`, `accepted-decode-*`, `hook-ack-start`, `hook-status-update`). **None of the marks recorded inside the flush path are present** (`handoff-flush-*`, `local-flush-start`, `outbox-read-*`, `request-build-*`, `request-reserved`, `request-parse-*`, `accepted-value-*`, `accepted-durable`, `prepare-display-*`, `adopt-*`, `local-status-saved`, `flush-basis-*`, `handoff-adopted-read-*`, `handoff-copy-*`). Cause, read from the App source at `092013f3`: `useTimelinePersistence.ts:509` calls `documentSave.flush(traceId)`, but the `documentSave` it receives is the wrapper in `useTimelineSave.ts:206-210` (`async flush() { ... handoff.flush() }`), which takes no argument and drops the trace id; every mark inside `handoff.flush` and `session.flush` then has `traceId === undefined` and is skipped. So the two stretches the instrumentation was meant to open stay closed:

- **capture-wait end to post-sent, median 475 ms** (361 to 837): handoff flush, outbox read, request build and reservation, none visible inside;
- **200 to hook-ack, median 399 ms** (197 to 774): the accepted-value, durable accept, prepare-display, adopt and handoff-copy steps, none visible inside.

Together about 0.87 s of the 5.9 s sits in these two unopened stretches. A one-argument pass-through in the wrapper (and any other wrapper between) would open them; I did not change anything (the App SHA is the approved one).

## Stage medians over the 18 warm saves (ms; overlapping stages marked, do not sum)

| Stage | Median | Min to max |
| --- | --- | --- |
| gesture-end to debounce-armed | 0.2 | 0.1 to 0.3 |
| (snapshot, draft queue and capture start, before gesture-end) | -2.2 to -1.5 | |
| debounce-armed to debounce-fired (the fixed debounce) | 536 | 502 to 774 |
| attempt-build (start to end) | 0.7 | 0.5 to 4.3 |
| capture-wait (start to end) | 140 | 103 to 544 |
| capture-wait end to post-sent (flush path, no inner marks) | 475 | 361 to 837 |
| **gesture-end to post-sent** | **1176** | 981 to 1663 |
| post-sent to 200 (the Runtime POST) | 4270 | 3959 to 4596 |
| accepted-decode (start to end) | 0.9 | 0.7 to 1.3 |
| 200 to hook-ack-start (flush path, no inner marks) | 399 | 197 to 774 |
| hook-ack-start to hook-status-update | 0.1 | 0 to 0.3 |
| hook-status-update to saved-badge (render) | 45 | 37 to 53 |
| **200 to saved-badge** | **441** | 243 to 824 |
| **gesture-end to saved-badge** | **5913 (5.91 s)** | 5550 to 6451 |

Overlapping: **draft write** runs beside the debounce (queued to start 174 ms, start to ready 238 ms, ready at about 407 ms after gesture-end); **capture** (`capture-start` to `capture-settled`, 671 ms) runs beside the debounce and ends after it, so the capture-wait of 140 ms is the part of the capture that outlasts the debounce. The route to post-sent is therefore debounce 537 ms, then the capture tail 140 ms (ending at about 671 ms), then the unmarked flush path 475 ms; the draft write (ready at 407 ms) is not on the critical path.

Driver release to Saved median for this run: 5.95 s; marks (gesture-end to saved-badge): 5.91 s, against the 6.23 s pooled median of the three `c8b861c7` runs (run medians 5.95, 6.37 and 6.42 s) on the same box: within the spread between those runs, so no sign that the marks cost time.
Bursts (one sample each, the extra marks record only the first occurrence per trace): **B5 last edit to Saved 23.9 s, B10 46.0 s**, 0 refusals, against about 25 s and 52 s in the three earlier runs (B10 51.0, 51.7, 52.9 s). The B10 figure is 5 s lower than every earlier B10; one repetition cannot say whether this is real.
Cold first save (not in the warm figures): gesture-end to post-sent 1.50 s, post-sent to 200 9.73 s, 200 to saved-badge 0.20 s.

## Not established

- Anything inside the two unmarked stretches (above).
- One repetition: the 0.9 s of the pre-POST path between runs can vary by 0.3 s (the earlier runs' medians 1.25 to 1.30 s against 1.18 s here).
- Whether the lower B10 is real.

`analyze-marks.py` produces `results-marks.txt` from `rep-1/browser-sv3-measure.json` (which holds the raw `astrid.save.*` entries after each of the 19 saves).
