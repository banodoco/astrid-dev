# Plan 89 measurement, three unprofiled repetitions of Runtime `c8b861c7`, 24 November 2026

Same package, SHAs and shell as the [first measurement](../2026-11-24-p89-measure-run/README.md): astrid-dev `release-15/p89-measure-command` head `ee89f2ed8ba6b4cb7c631b7d3a9f593c5bc01a71` (digest `1a2ee7c323fa483f9e5298a3c9a531fb5f4d1edbd13702823082db1b1d4dc6d8`), Runtime `c8b861c770aa58fd0392fe2dcefbda9ce23c84d1` (clean production code), App `9f26112d746cba7a1a3287f0b679fd6c9ca39907` (built on the box each time), Agent `096a2fb3536192785fabd33e6673ba8ab4ef5ead` two-file overlay, no sampler. Approved by the Plan 89 orchestrator as `SV3_REPETITIONS=3`. **How it was run:** the shell was launched with `SV3_REPETITIONS=3` (`run1-stdout.log`); as in the first measurement the package's `timing-match` step aborts at the missing timing sink (this Runtime writes none) after repetition 1, so the loop never reached repetitions 2 and 3. Repetitions 2 and 3 were therefore run as two further single-repetition runs of the identical shell (`SV3_REPETITIONS=1`, `run2-stdout.log`, `run3-stdout.log`, `p89-chain.log`), each with its own Runtime start, fresh pristine and work copies of the data and a fresh App build. All three script exit statuses are 1 for that sink check, after the measurement. Each: phase `verified`, 34 commit POSTs, 0 failed drags, 0 refusals, all HTTP 200; idle-safe stop verified, ports closed, no Chrome, boundaries unchanged; disk minimum 16.87, 16.72 and 16.58 GiB (stop 16 GiB).

## Result (the four App marks; 54 warm sequential saves, 18 per run; cold = first save of each run)

| | Run 1 | Run 2 | Run 3 | All 54 warm |
| --- | --- | --- | --- | --- |
| Warm POST to 200, median | 4.50 s | 4.36 s | 4.56 s | **4.43 s** (p90 4.96, max 5.13) |
| Warm gesture end to Saved badge (marks), median | 6.37 s | 5.95 s | 6.42 s | **6.23 s** (p90 6.88, max 7.33) |
| Warm release to Saved (driver), median | 6.40 s | 5.98 s | 6.44 s | **6.26 s** (max 7.36) |
| Warm gesture end to POST sent, median | 1.30 s | 1.25 s | 1.27 s | 1.28 s |
| Warm 200 to Saved badge rendered, median | 0.43 s | 0.35 s | 0.51 s | 0.43 s |
| Cold first save: POST to 200 / gesture end to Saved | 10.19 / 12.45 s | 10.62 / 13.00 s | 10.66 / 13.36 s | 10.2 to 10.7 / 12.4 to 13.4 s |
| S0: editor writable after the cold start | 7.4 s | 6.8 s | 6.6 s | |

Per scenario (driver release to Saved, all runs): S1 (3 saves) 6.45 s median, S2 (6) 6.46 s, S3 (30) 6.18 s, S4 (15) 6.42 s, max 7.36 s. The gate (2 s median, 4 s maximum) is not met. Bursts (all runs: 0 refusals, every edit in the document): B5 last edit to Saved 25.6, 25.0 and 25.5 s; B10 51.0, 51.7 and 52.9 s (final start 262.1333 s against 262.0833 s expected, exactly the 0.05 s tolerance, reported `false` as in every run).

## Comparison

- **Spread between repetitions is small:** the run medians differ by 0.2 s for POST to 200 (4.36 to 4.56 s) and 0.45 s for the total (5.95 to 6.42 s).
- **Against the 24 November SV-L2 run (`eb4e8644`, instrumented, one repetition): warm POST to 200 4.61 s, gesture end to Saved 6.15 s.** This candidate: 4.43 s (0.18 s, 4 % lower, about the spread between repetitions) and 6.23 s (0.08 s higher): no change worth reading out of these numbers.
- **Against the 24 November SV-4 combined run (`eb4e8644`, instrumented, 54 warm saves): POST to 200 5.1 s, release to Saved 6.8 s:** 0.7 s (14 %) lower and 0.5 s (8 %) lower here. Both `eb4e8644` runs carried the instrumentation and the SV-L2 run had the App marks; this one is clean production code with the marks only, so part of the difference may be instrumentation overhead, not the Plan 89 save work.
- The pre-POST part is longer in this App/Runtime pair than in the SV-L2 run (1.28 s against 1.08 s).

## Not established

- A same-session baseline of `eb4e8644`: not run here (optional request pending).
- Whether the 0.18 s difference to the SV-L2 run is real; it is within the 0.2 s spread of repetitions and the earlier run is one repetition.
