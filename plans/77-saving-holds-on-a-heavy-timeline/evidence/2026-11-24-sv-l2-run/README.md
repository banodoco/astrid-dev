# SV-L2: App PR #377 timing marks on a real drag save, 24 November 2026

Run exactly as sent by the Plan 89/77 orchestrator: package astrid-dev branch `release-15/p77-svl2-measure-clean` head `fe3e8a5c22ffb036e4837caabe97824f15564e41` (manifest digest `8c9216ef37a630bcdf648521f0134a8643f1f22b3fe651bc4fa8ce2695366696`, 11 files, all manifest-covered, `sha256sum -c` clean), App `7705ebd478368e8de82b80523c2a3eb87868b710` (PR #377, built on the box from a new worktree with the reference `node_modules` symlinked, `vite build` took 42 s, 357 files, 140 MB, `build-svl2.log`), Runtime `eb4e8644e3549c88d5d836cd5738ca75e76d311a` (instrumented, same as the combined run), Agent `096a2fb3536192785fabd33e6673ba8ab4ef5ead` two-file overlay. One attempt, one repetition, 05:07Z to 05:25Z, **exit status 0**. The build left the reference `node_modules` tree metadata unchanged and the Vite config restored (`build-node-modules-guard.json`); the dist inventory was identical before and after the run (`dist-files.sha256`, `dist-files.after.sha256`). Idle-safe stop verified, ports closed, no Chrome, boundaries unchanged (`cleanup.json`, `boundary.json`); disk minimum 16.61 GiB (`free-kib.tsv`, stop 16 GiB). `daemon-startup.stderr` empty. Limits: Agent authoring and generation are a stub, the marks are not independent HTTP receipts, burst attribution of the marks is ambiguous, and the numbers are instrumented.

## Result

**The #377 App opened the heavy timeline against the `eb4e8644` Runtime (S0: verified-head 200, editor writable after 33 s on this first start after a build, verified-head request 10.3 s), all 34 commit POSTs returned 200 and reached Saved, no refusal, and the tape worked: all 19 sequential drags carry the four `astrid.save.<n>.{gesture-end,post-sent,200,saved-badge}` marks with no ambiguity** (`rep-1/browser-sv3-measure.json`, `save_marks_after_saved` per drag).

Client and Runtime time per save from the marks (page clock, `performance.getEntriesByType('mark')` read after each Saved), medians (warm = the 18 warm sequential saves, cold = the first save):

| Interval | Cold | Warm median | Warm max |
| --- | --- | --- | --- |
| gesture end to POST sent | 1.13 s | 1.08 s | 1.40 s |
| POST sent to 200 | 9.66 s | 4.61 s | 5.29 s |
| 200 to the Saved badge rendered | 0.36 s | 0.44 s | 0.61 s |
| **gesture end to Saved badge** | **11.16 s** | **6.15 s** | **6.85 s** |

- **The marks agree with the independent measurements:** POST-sent-to-200 equals the Runtime's own `runtime_wall_ms` (timing line, same save) plus a median 22 ms (range 17 to 38 ms) and the driver's POST-to-200 plus 16 ms; the driver's release-to-POST exceeds the marks' gesture-end-to-POST by a median 23 ms (the release-to-gesture-end gap) and the driver's release-to-Saved exceeds the marks' gesture-end-to-Saved by 28 ms. The Runtime's per-stage lines account for 99.5 % or more of POST-to-200 as before.
- **Client side is about 1.5 s of a 6.15 s warm save:** 1.08 s between the end of the gesture and the POST being sent, 0.44 s from the 200 to the rendered Saved badge. The Runtime is about 4.6 s (warm exclusive medians: `provider_commit` 2.33 s, `port_store_accept` 1.54 s, durable reconciliation 0.40 s, handler 0.28 s). What the 1.08 s before the POST consists of (the 500 ms save debounce plus the request build) is not broken down by the marks.
- Release to Saved per scenario (driver): cold 11.2 s; S1 6.24 s; S2 6.05 s (2 saves); S3 6.19 s (10); S4 6.40 s (5). The gate (2 s median, 4 s maximum) is still not met.
- Bursts (marks cannot attribute each Saved badge to one drag in a burst; `ambiguity: burst_snapshot_cannot_associate_each_saved_badge_to_a_drag`): B5 5 of 5 edits, 5 POSTs, last edit to Saved 26.4 s, 5 of 5 in the document, final start 241.3333 s against 241.3062 expected, matches; B10 10 of 10 edits, 10 POSTs, 49.3 s, 10 of 10 in the document, final start 262.1333 s against 262.0833 s expected (0.050 s, exactly the 0.05 s tolerance, reported `false`). No refusal.

## Not established

- The split of the 1.08 s between gesture end and POST sent.
- The instrumentation overhead of the Runtime counters and of the marks themselves.
- Behaviour on a second repetition or a restarted App (one repetition only).
