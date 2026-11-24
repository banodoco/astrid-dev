# Plan 89 measurement: Runtime `c8b861c7` (clean), App `9f26112d`, Agent two-file overlay, one repetition, 24 November 2026

Run as sent by the Plan 89 orchestrator: package astrid-dev branch `release-15/p89-measure-command` head `ee89f2ed8ba6b4cb7c631b7d3a9f593c5bc01a71` (digest `1a2ee7c323fa483f9e5298a3c9a531fb5f4d1edbd13702823082db1b1d4dc6d8`, 11 files, clean `sha256sum -c`, identical to the SV-L2 package `fe3e8a5c` except the App/out-dir pins), Runtime `c8b861c770aa58fd0392fe2dcefbda9ce23c84d1` (tree `b45215b5480017875c8db36f0ce363021d58ad57`, fetched from `p89/measure-c8b861c7`; dependency and contract diff against `77c38d03` empty; **clean production code: no profiler, no save-work counters**), App `9f26112d746cba7a1a3287f0b679fd6c9ca39907` (built on the box, `vite build` 54 s, package files and Vite config byte-identical to the reference, reference `node_modules` metadata unchanged, `build-node-modules-guard.json`), Agent `096a2fb3536192785fabd33e6673ba8ab4ef5ead` two-file overlay only (the plan-89 Agent with the rollback hook was not used and is not exercised). One attempt, one repetition, 13:44Z to 13:55Z. Retained Release-14 program with the candidate Runtime source overlaid; Agent authoring step is a stub; no PreparedCommit counter exists in this build.

**Script exit status 1, but the measurement is complete.** The package's own `timing-match` step stopped after the repetition because this Runtime wrote no commit-stage timing sink (`rep-1/timing-sink-capture.json`: `status: missing`; `ValueError: Runtime commit-stage timing sink is missing` in `run-stdout.log`); the earlier `eb4e8644` candidate had that sink and `c8b861c7` evidently does not. The script therefore ended before it combined `summary.tsv` and `measurements.jsonl`, which do not exist. Everything below is computed from `rep-1/browser-sv3-measure.json`, which was written by the driver before that step (phase `verified`, 34 commit POSTs, 0 failed drags, 0 refusals). Cleanup was clean: idle-safe stop verified, ports closed, no Chrome, boundaries unchanged (`cleanup.json`, `boundary.json`); disk minimum 16.40 GiB (stop 16 GiB); `daemon-startup.stderr` empty; the supervised pack host ran; `agent-loaded.json` `failures: []`; dist inventory unchanged.

## Result (the four App marks `astrid.save.<n>.*`, all 19 sequential saves, ambiguity none, all HTTP 200)

| Interval | Cold first save | Warm median (18) | Warm max | Warm median, first 12 |
| --- | --- | --- | --- | --- |
| gesture end to POST sent | 4.22 s | 1.37 s | 1.98 s | 1.44 s |
| POST sent to 200 | 11.18 s | 4.59 s | 5.16 s | 4.58 s |
| 200 to Saved badge rendered | 0.30 s | 0.41 s | 0.83 s | 0.41 s |
| **gesture end to Saved badge** | **15.69 s** | **6.56 s** | **7.26 s** | **6.56 s** |

- The driver's own release-to-Saved agrees (warm median 6.59 s, max 7.30 s; S1 6.44 s, S2 6.63 s, S3 6.60 s, S4 6.57 s; cold 15.76 s), POST to 200 equals the marks within 15 ms. The gate (2 s median, 4 s maximum) is not met.
- **Against the baseline of 24 November (SV-L2 on `eb4e8644`, instrumented, warm median 6.15 s gesture-end-to-Saved and 4.61 s POST-to-200): POST to 200 is unchanged (4.59 s), the total is 0.4 s longer (the pre-POST part is 1.37 s against 1.08 s and the cold save is slower: 15.7 s against 11.2 s with a 4.2 s wait before the first POST).** No saving from the SV-L5, SV-L6, SV-L9a and SV-L10 changes is visible on this fixture.
- S0 (first read after the cold start): verified-head 200 (request 8.5 s), editor writable after 31.4 s; no refusal. `up` took 125 s (`rep-1/candidate-daemon-module.json` to `up.json`); the first writes were accepted and no `realm_admission_failed` or read-only state was seen. The script waits for `up` before opening the page and does not poll `/v1/health`, so a short read-only phase before the first read would not have been observed.
- Bursts (marks ambiguous): B5 5 of 5 edits, 5 POSTs, last edit to Saved 25.6 s, 5 of 5 in the document, final start 241.3333 s against 241.3062 s expected, matches; B10 10 of 10 edits, 10 POSTs, 50.4 s, 10 of 10 in the document, final start 262.1333 s against 262.0833 s (0.050 s, exactly the 0.05 s tolerance, reported `false`). No refusal.

## Not established

- Why `c8b861c7` has no timing sink, whether its per-stage timings exist elsewhere, and why the changes did not shorten POST to 200: no profile or per-stage line was taken in this run.
- PreparedCommit schema time (no counter; the profile mode would be a second attempt).
- The slower cold first save (4.2 s before the POST, 11.2 s POST to 200) against the earlier run: one sample each.
