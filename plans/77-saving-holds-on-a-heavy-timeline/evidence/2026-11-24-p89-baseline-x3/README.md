# Plan 89 clean baseline, three single-repetition runs of Runtime `24e2c929`, 24 November 2026

The same package, shell, App, Agent overlay, fixture and box as the [three `c8b861c7` runs](../2026-11-24-p89-measure-x3/README.md); **only the Runtime differs**. Package: astrid-dev `release-15/p89-measure-command` head `ee89f2ed8ba6b4cb7c631b7d3a9f593c5bc01a71` (digest `1a2ee7c323fa483f9e5298a3c9a531fb5f4d1edbd13702823082db1b1d4dc6d8`, unchanged). App `9f26112d746cba7a1a3287f0b679fd6c9ca39907` (built on the box each time). Agent `096a2fb3536192785fabd33e6673ba8ab4ef5ead`, two-file overlay. Runtime `24e2c9291d5bcaface78324696286f2dc896debc` (tree `ca0a84481b9b5203bb401b313101036fac7fc3db`, branch `p89/measure-base-24e2c929`): the same code as `c8b861c7` minus Plan 89's Runtime work (dependency and contract diff against `77c38d03` empty). No sampler, no profile. Approved by the Plan 89 orchestrator as three single-repetition runs (`SV3_REPETITIONS=1` each), one attempt each.

**How it was run.** One shell (`p89base-measure.sh`, the `c8b861c7` shell with the Runtime SHA, tree and fetch ref changed) run three times in a row, each with a fresh Runtime start, fresh pristine and work copies of the data and a fresh App build. Each script exit status is 1: the package's `timing-match` step aborts at the missing timing sink (this Runtime writes none) after the measurement, as in the `c8b861c7` runs (`run1-stdout.log` etc.). Each run: phase `verified`, 34 commit POSTs, 0 failed drags, 0 refusals, all HTTP 200; idle-safe stop verified, ports closed, no Chrome, boundaries unchanged. Disk minimum 16.82, 16.70 and 16.58 GiB (stop 16 GiB).

**One earlier launch stopped before it started.** The first launch (`floor-stop-attempt-stdout.log`) stopped at the run script's 18 GiB start floor after the App build (about 17.9 GiB), before the fixture was touched. The chain then moved on by itself to its second run, which stopped at the same floor before the fixture was touched (I had not yet stopped the chain). Both are repeats of the earlier disclosed profile-launch floor stop. I reclaimed my own reproducible scratch (package-repo clones in finished command directories, the aborted App worktree; logged in `sv3-reclamation.tsv`) and relaunched identically. The three runs here are the relaunch.

## Result (54 warm sequential saves, 18 per run; cold = first save of each run)

| | Run 1 | Run 2 | Run 3 | All 54 warm | `c8b861c7`, all 54 warm |
| --- | --- | --- | --- | --- | --- |
| POST to 200, median | 9.79 s | 9.23 s | 9.49 s | **9.56 s** (p90 10.15, max 11.04) | 4.43 s (p90 4.82, max 5.13) |
| Gesture end to Saved badge (marks), median | 11.81 s | 11.19 s | 11.61 s | **11.63 s** (p90 12.34, max 12.98) | 6.23 s (p90 6.88, max 7.33) |
| Release to Saved (driver), median | 11.85 s | 11.22 s | 11.64 s | **11.67 s** (max 13.01) | 6.26 s (max 7.36) |
| Gesture end to POST sent, median | 1.26 s | 1.25 s | 1.28 s | 1.26 s | 1.28 s |
| 200 to Saved badge rendered, median | 0.76 s | 0.66 s | 0.66 s | 0.68 s | 0.43 s |
| Cold first save: POST to 200 / gesture end to Saved | 16.73 / 19.07 s | 18.15 / 21.04 s | 17.11 / 19.84 s | 16.7 to 18.2 / 19.1 to 21.0 s | 10.2 to 10.7 / 12.4 to 13.4 s |
| S0: editor writable after the cold start | 7.2 s | 7.3 s | 6.4 s | | 6.6 to 7.4 s |
| B5 last edit to Saved | 54.0 s | 49.2 s | 49.9 s | about 51 s | about 25 s |
| B10 last edit to Saved | 102.9 s | 101.4 s | 111.0 s | about 105 s | about 52 s |

Per scenario (driver release to Saved, all runs): S1 11.7 to 12.4 s, S2 11.6 to 11.9 s, S3 11.2 to 11.8 s, S4 11.0 to 12.1 s. Bursts: 0 refusals, every edit in the document, no POST after settle; B5 final state matches, B10 final start differs from expected by the same 0.05 s tolerance reported `false` in the `c8b861c7` runs. The gate (2 s median, 4 s maximum) is not met by either Runtime.

## Comparison with the `c8b861c7` runs (same package, App, Agent, box and fixture)

- **POST to 200: 9.56 s to 4.43 s, 54 % lower (2.2 times faster).** **Gesture end to Saved: 11.63 s to 6.23 s, 46 % lower.** The slowest warm save here (13.0 s) is slower than the slowest `c8b861c7` save (7.4 s) by a wide margin; the two sets do not overlap for POST to 200 (baseline fastest 8.87 s, `c8b861c7` slowest 5.13 s).
- **Cold first save and bursts show the same shape:** cold gesture end to Saved 19 to 21 s down to 12 to 13 s; B5 about 51 s down to about 25 s; B10 about 105 s down to about 52 s.
- **Unchanged by the Runtime work:** time to editor writable (6.4 to 7.4 s in both) and gesture end to POST sent (1.26 against 1.28 s). The whole difference sits between the POST and its 200.
- **Run-to-run spread inside each Runtime is small** against the difference: run medians 9.23 to 9.79 s here and 4.36 to 4.56 s on `c8b861c7` for POST to 200.

## Not established

- Single repetition per run, three runs, one box and fixture; the sampler was off but nothing else about timing was controlled (load, thermal). Bursts and cold start are one sample per run.
- Which part of Plan 89's Runtime work saves the time: this folder only measures the sum. Stage timing for `c8b861c7` is in the [profile](../2026-11-24-p89-profile/README.md); this Runtime writes no stage timing.
- Not run: `eb4e8644` baseline (the orchestrator asked not to).

`analyze.py` computes the numbers from `run-N/rep-1/browser-sv3-measure.json` (output in `results-marks-and-driver.txt`; the marks are the four `astrid.save.<n>.*` marks, "driver" values are the driver's own timestamps). The driver's POST to 200 pooled median is 9.56 s.
