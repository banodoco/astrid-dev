# Rounds — Saving holds on a heavy timeline

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Handover](handover.md)

One section per round, newest last, written by the coordinator under the [live-loop workstream](../../skills/roles/astrid-dev-manage/workstreams/live-loop.md#the-round). Each holds: the stack versions; a table of scenario, outcome (saved or refused with the reason shown), time to Saved, head count, anything vanished; The strategist's advice (evidence, not a verdict); the fixes picked and their PRs; and **Plan deltas** for [Plans 63, 75 and 76 and 18](inputs.md#references).

Round 1 records the partial baseline below. The full fixture is required for Rounds 2 and 3. The 18 November sweep (14 edit kinds, 3 saved, 11 refused, on the owner's copied timeline with the old timer) is earlier evidence, not a baseline: [evidence/results.jsonl](evidence/results.jsonl).

## Setup checks on 21 November 2026

No timed baseline yet. On App `7fc14d2f`, Agent `c00721de`, Runtime `e43bfccc`, a nine-track SDK commit advanced the public head. Fresh SDK reopen was refused with `accepted commit inputs changed during verification`, and Runtime logged a WAL move. A one-track control reopened, as did the nine-track control on App `e576c7fe`, Agent `efccee92`, Runtime `162500fe`. One subsequent bounded shot seed advanced a public head while the SDK reported its outcome unknown. Plan 77 now owns the checkpoint repair in Release 15. [Runtime PR #81](https://github.com/banodoco/astrid-runtime/pull/81)

The deliberate no-op probe on App `75120d7c`, Agent `c00721de`, Runtime `e43bfccc` produced three expected failed rows, one unchanged publication per row, and zero successful commits. It used an empty sandbox timeline. The heavy fixture must qualify before measuring Round 1.

## Local WAL development probe on 21 November 2026

This setup probe used disposable local pins and leaves the baseline round count at zero. App used launcher base `75120d7c`; Agent used `c00721de` with local pin-only commit `ceed78eb`; Runtime was built from `8be4f258`. The nine-track SDK commit advanced the public timeline from version 1 to 2. The public head matched the accepted receipt, and a fresh SDK session reopened it. The Runtime emitted zero WAL warnings for that probe. The Release 15 product repair is tracked below. [Runtime PR #79](https://github.com/banodoco/astrid-runtime/pull/79)

## SL-0 pacing comparison on 21 November 2026

The unpushed `8be4f258` Runtime development stack imported and selected 616 generated assets in 131.5 s. It then accepted 108 clips across nine 12-command SDK batches. The public index confirmed version 11 and publication `txn-469ff762ca1a41e9ad1d7f98675c9417` after the seed stopped. Batch wall times in seconds were 3.2, 10.1, 16.8, 23.6, 31.6, 41.4, 49.7, 57.7 and 70.7. These were accepted seed batches, distinct from the November 18 one-edit warm median and editor time to Saved. The full fixture, canonical byte count and warm comparison remain open.

The comparison used the same App fixture script and media digests with App `e576c7fe`, Agent `efccee92` and Runtime `162500fe` from Plan 69. It imported and selected 616 assets in 132.1 s and accepted the first 12 clips in 3.6 s. The public index confirmed version 3 and publication `txn-2fc61a3d1a414c21bb517441d766f8be`. Before the second batch could submit, a pinned source read refused because the SQLite WAL moved. A read-only SDK reopen after the writer stopped returned the same verification refusal. The two runs separate the nine-track WAL result from the heavy seed's performance. The older tuple stopped too early to attribute the batch-time growth to Release 14 or to existing history costs.

Both are pre-baseline development runs. The Release 14 App and Agent forwards are held. FIX-16 and FIX-21 are outside the baseline App. Plan 77 proceeds on its own branches. The shipped candidate still needs the full synthetic fixture and the live matrix.

### Matched checkpoint guard

The same generated media and public SDK seed ran with the earlier Plan 69 Runtime `162500fe` plus only the two checkpoint changes from Runtime PR #79. The disposable Runtime `15f0fef` and pin-only Agent `5cb9fccd` were used with App `e576c7fe`. Nine accepted 12-command batches took 4.455, 4.388, 5.421, 6.339, 8.013, 8.944, 10.333, 12.517 and 13.266 s. The public head was version 11, publication `txn-be71171a630449f498f6dad7d5f36986`, and a fresh SDK session reopened 108 clips. The full integration tuple took 70.691 s at batch 9, 5.33 times the matched-guard run. The checkpoint changes alone cleared the earlier false refusal. Multiple product changes distinguish the full tuple, so this comparison does not identify an individual commit as the cause. Both are pre-baseline development measurements.

**Plan deltas.** Plan 75 owns the pre-existing history cost. After the first batch, the older line grew by about 1 s per successive 12-command batch. Plan 77 owns the larger-slope investigation and any loop fix. No new evidence for Plans 63, 76 or 18.

### Release 15 ownership

On 21 November the owner assigned the false checkpoint refusal and commit-cost investigation to Plan 77. The checkpoint repair is a setup fix because a routine checkpoint can block the seed and reopen. The first baseline round will record that repair and its regenerated Runtime, Agent and App pins. The App and Agent Release 14 forwards remain held. The component split and first-parent investigation are development evidence for the first loop candidate. The baseline round count remains zero.

### Component split and landed setup fix

The same first four SDK batches ran with the newer App and Agent and older patched Runtime, then with the older App and Agent and newer Runtime. All four variants accepted 48 clips on 9 tracks, and the two swaps reopened their exact public heads.

| Runtime and client tuple | 12 clips | 24 clips | 36 clips | 48 clips |
| --- | --- | --- | --- | --- |
| Older App and Agent, older patched Runtime | 4.455 s | 4.388 s | 5.421 s | 6.339 s |
| Newer App and Agent, newer development Runtime | 3.185 s | 10.065 s | 16.826 s | 23.562 s |
| Newer App and Agent, older patched Runtime | 3.611 s | 4.041 s | 5.273 s | 6.834 s |
| Older App and Agent, newer development Runtime | 4.433 s | 9.702 s | 15.495 s | 22.090 s |

The tested steeper slope follows the development Runtime. The actual Plan 77 branch excludes the later integration tip used in that probe, so an exact repaired-lane retime follows. Runtime `86e1b832` landed the checkpoint repair here; Agent `210cad35` and App `8e619302` pin it. The exact installed tuple and fix will be recorded in Round 1's versions. These timing samples remain development evidence. [Runtime PR #81](https://github.com/banodoco/astrid-runtime/pull/81)

### Exact checkpoint-repaired seed

The baseline stack installed App `8e619302`, Agent `210cad35` and Runtime `86e1b832`. It imported all 616 generated assets in 130 s. The first four accepted 12-command SDK batches took 3.940, 4.891, 6.243 and 12.911 s. Batch 12 took 75.251 s. Estimates from the observed batches put clip seeding near two hours. The owner authorized the full seed with a new report if the projection for clips and shots rises above about three hours.

Two interruptions lost response waiting after Runtime accepted the requests. The public index and canonical composition revision verified the exact contiguous 168-clip prefix and its 168 selected media IDs before continuation. Same-key media imports returned the original receipts. The next two accepted batches reached 192 clips in 23.812 and 72.030 s, respectively. The synthetic timeline is still seeding. Round 1 requires the complete fixture and editor matrix on this tuple.

## Round 1: baseline on plan-77 as cut plus #81, partial fixture of 288 of 616 clips (seed stopped at the three-hour projection)

**Stack.** App `8e619302`, Agent `210cad35`, Runtime `86e1b832`. The seed paused before clip 289 after a public receipt, with 288 exact clip and media identities and nine tracks. One public SDK transaction added the ten shot occurrences required for the existing matrix. The exact root clip rows stayed identical. The editor started at public version 27, publication `txn-7fb668679a4b4943866530767d8edf03`.

Recent fits across 6, 8, 10 and 12 measured batches projected 193–220 minutes for clips plus shots. The fit using the full series was 162 minutes because the early batches were faster. Shot costs were extrapolated from equal-size clip batches.

### Accepted seed batches

These are public SDK commit elapsed times for 12 clip commands per batch. The two missing client replies were independently checked against the exact accepted public revisions.

| Batch | Cumulative clips | Commit seconds |
| --- | --- | --- |
| 1 | 12 | 3.940 |
| 2 | 24 | 4.891 |
| 3 | 36 | 6.243 |
| 4 | 48 | 12.911 |
| 5 | 60 | 7.296 |
| 6 | 72 | 22.349 |
| 7 | 84 | 30.812 |
| 8 | 96 | 37.419 |
| 9 | 108 | 27.503 |
| 10 | 120 | 34.830 |
| 11 | 132 | 33.348 |
| 12 | 144 | 75.251 |
| 13 | 156 | Unmeasured after accepted receipt |
| 14 | 168 | Unmeasured after accepted receipt |
| 15 | 180 | 23.812 |
| 16 | 192 | 72.029 |
| 17 | 204 | 83.292 |
| 18 | 216 | 162.520 |
| 19 | 228 | 93.573 |
| 20 | 240 | 103.887 |
| 21 | 252 | 115.630 |
| 22 | 264 | 40.033 |
| 23 | 276 | 266.674 |
| 24 | 288 | 153.621 |

### Editor matrix

The harness recovered startup by using a short owned browser directory and the installed editor's ordinary `connect=1` link. A fresh browser then reached the actual Saved badge at 41.211 s with the synthetic fixture visible. That figure measures startup. The single longer measurement reached Saved with the fixture visible in 171.612 s. A fixture target first appeared at 13.997 s. The observation did not establish when the first 15 s became editable. CPU seconds were unmeasured for this initial matrix. [App harness PR #330](https://github.com/banodoco/astrid-app/pull/330)

| Scenario | Outcome | Gesture end to POST | Time to Saved | Public evidence |
| --- | --- | ---: | --- | --- |
| Same-track video move, first repetition | Failed. The browser reported an unconfirmed save and showed Try again and Discard | 17.465 s | No Saved captured | One accepted advance from v27 to v28. The moved video start changed from 0 to 0.5667 s. All 288 clip IDs survived, with one stable current head. |
| Remaining 84 scenarios and the other two repeats of the first | Unattempted. The sweep stopped at guarded cleanup | — | — | The timeline metadata and revision index sampled different heads around the advance. The follow-up snapshot timed out, so the harness refused to restore without a verified after-head. |

The host accepted this as the failing baseline. Three diagnostics used the same installed tuple and the same synthetic project. They leave the initial matrix outcome intact.

| Diagnostic | Wall and CPU | Public result and sampled work |
| --- | --- | --- |
| One commit-history GET at v28 | 5.191 s HTTP, 5.190 Runtime process CPU s | HTTP 200, 120,023,350 bytes for 28 items. Compact encodings of `records`, `receipt` and `steps` total 112.84 MB. The request thread samples cover history assembly, detachment, finite-JSON validation and response encoding. |
| Fresh profile on the warm stack, followed by one same-track move | Warm startup reached Saved with a fixture target visible at 34.421 s. Matched Chrome renderers used 24.57 CPU s and Runtime used 24.41 CPU s. The move took 11.243 s to send and another 33.086 s to receive HTTP 200. Across the gesture-to-response observation the corresponding CPU use was 25.22 and 42.23 s. | The one public head advanced v28 to v29, with all 288 IDs preserved. The 10.999 s between the trace's gesture-end mark and its POST included about 3.39 sampled s in outbox detachment and 1.75 s in renderer garbage collection. First-15-seconds editability, a whole-timeline open witness and gesture-to-Saved stayed unmeasured. |
| One accepted 12-command SDK commit from v29 | 61.744 s for the SDK call and 57.79 Runtime CPU s during that window. The handler took 49.402 s including 38.056 s in the provider. Store acceptance took 27.379 s within that span. Post-provider durable reconciliation took another 11.000 s. | One public head advanced to v30 with all 300 expected IDs. The reservation scan accounted for 3.98 leaf sample seconds. The sampler also saw schema validation and history hashing and included some overlapping requests. Retained-row checks were prominent on concurrent writes. Their role in the measured commit remains unresolved. |

**Round 2 batch.** The advisor ranked batching Runtime reservation scans, removing redundant App outbox copies, and using compact authenticated history for editor open and undo. Preserve fixed-head and old-client behavior on the history producer and consumer, exact durable retry keys and bytes, and collision/refusal semantics. Each fix has its own paired profile. Combine qualified fixes for one fresh full-standard round. The host selected the existing-contract App lazy-read path for Round 2 and held the compact Runtime projection for Round 4 if measured opening or undo cost warrants it. The owner approved the device-saved and opening badge change, which can follow in Round 4 if it shares active save-path work.

**Plan deltas.**

- Plan 63 gets the accepted-once move that was unconfirmed in the browser. Its lost-reply witness should check public reconciliation and badge agreement.
- Plan 75 gets the heavy history read and batch series, alongside all three open/save spans. Separate history depth from clip count if the first profile leaves attribution unclear.
- Plan 76 keeps its two-writer witness outstanding. This run exercised one writer and a temporary read disagreement.
- Plan 18 gets the same-track gesture-to-POST span for its gesture-to-operation comparison.

## Round 2 (partial 288)

The fresh standard run installed App `22780a7a`, Agent `da212f2a` and Runtime `712d9754`. It imported all 616 generated assets in 120.088 s. The host capped this counted saving round at 288 root clips and ten shot occurrences to compare against Round 1. The seed stopped at the exact accepted v26 receipt `txn-ec9906fd`. A separate accepted ten-command transaction, `txn-b76015f8`, published v27 with the same 288 clip and media identities, nine tracks and exactly ten shot occurrences. It took 144.165 s and returned a 242,234-byte canonical document. The 616-clip, 2.6 MB and warm-ratio qualifications remain open. This tuple includes the three ranked fixes and current Plan 69 save mirror. The Agent pack/source set is unchanged from the Plan 77 baseline. The optional large-shots variant is available separately through [App #343](https://github.com/banodoco/astrid-app/pull/343) and does not gate the standard run.

Per-change comparisons remain in Round 1's context. [App #340](https://github.com/banodoco/astrid-app/pull/340) reduced four-capture emulated outbox time from 92.173 to 57.557 ms with identical request bodies. [Runtime #84](https://github.com/banodoco/astrid-runtime/pull/84) reduced the 12-claim warm synthetic SQL stage from 212.20 to 53.46 ms and from 94.03 to 25.79 ms across its two histories, with unchanged filtered results. [App #342](https://github.com/banodoco/astrid-app/pull/342) moves the full-history fetch off the editor's readiness path. On the old exact v30 stack the head-only read took 2.462 s and 2.45 Runtime CPU s for 2,162 bytes. The full read took 5.687 s and 5.69 Runtime CPU s for 133,585,133 bytes. The full history still loads later. These change-level diagnostics remain separate from the live wall, CPU, head and refusal measurements. At 180, 192, 204, 216, 228, 240, 252, 264 and 276 root clips, the latest accepted 12-command batch took 56.844, 70.790, 77.114, 154.868, 90.410, 98.762, 108.209, 254.708 and 133.806 s. The seed curve measures the product’s actual commit cost. The exact latest Runtime still shows growth large enough to put a complete fixture at risk of taking several hours. The short SQL stage improvement does not explain the dominant wall time.


The last ten matched 12-command batches had a median of 98.730 s in Round 1 and 103.486 s in Round 2. The matched 277–288 batch took 153.621 s and 284.529 s respectively. Both runs reached v26 at that clip count. The batch curve measures setup and multi-command commit cost. The ordinary save target is gesture-to-Saved in the matrix.

### Editor matrix

| Measurement | Round 1 partial | Round 2 partial |
| --- | --- | --- |
| Opening | A fixture target appeared at 13.997 s. The browser reached Saved with the target visible in 171.612 s. First-15-second editability and a whole-timeline witness were unmeasured. | First-15-second clips visible in 22.070 s, first usable with selection and writable track label at 30.484 s, all expected UI clips and tracks plus stable Saved at 31.517 s. The last observation agreed with one unchanged public v27 head. The editor did not expose its rendered head ID. Both opening targets missed. |
| Opening CPU and history transfer | The separate warm diagnostic reached the target and Saved in 34.421 s with 24.41 Runtime and 24.57 matched-renderer CPU s. A separate full history GET transferred 120,023,350 bytes. | Runtime 18.86 CPU s and browser tree 24.83 CPU s over the 31.52 s opening window. The successful head-only history GET transferred 2,162 body bytes. A later full-history request failed without a captured body. |
| Same-track video move, first repetition | Unconfirmed in the editor. The primary page sent one POST 17.465 s after the gesture. It advanced the public head once to v28. No Saved time was captured. | Unconfirmed in the editor. The primary row saw no POST and still read one unchanged v27 head. Its scenario interval, which includes public snapshot reads, took 160.605 s and used 153.83 Runtime and 40.13 browser CPU s. No Saved time was captured. |
| After the move row | The guarded restore stopped when public timeline metadata and revision listing disagreed. | Guarded cleanup timed out after 83.674 s with 78.98 Runtime and 52.04 browser CPU s. The independent transfer observer saw a later second-tab POST start 177.342 s after the gesture and return HTTP 200 in 5.589 s with 1,181,896 body bytes. The public head advanced once to v28 `txn-8b610a82`. All 288 clip IDs and ten shots remained, with the intended video start changing from 0 to 0.5667 s. |

One repeat failed in each round. The other 84 scenarios and 254 repeats remained unattempted in Round 2, including the deliberate clash. This counted partial round failed the saving criterion. The late acceptance did not supply a confirmed Saved badge. The fresh browser profile was removed after the runner's cleanup error. The duplicate run identity rows in this exact App build agree. [App #346](https://github.com/banodoco/astrid-app/pull/346) removes that duplicate from later runs.

The host directed subsequent rounds to restore the authenticated synthetic backup, with the restored clip count and qualification described in each result.

**Plan deltas.**

- Plan 63 gets the edit that was unconfirmed in the primary tab and accepted once later through a second tab. Show how pending ownership, late acceptance and recovery agree with the public receipt and the badge.
- Plan 75 gets the separate 5.589 s delayed single-move response, the multi-command seed curve and the cold-opening CPU. Measure repeated verification separately from stored record size before deciding how much needs a new format.
- Plan 76 gets a passive second-tab write following a primary action. Identify the outbox owner during recovery and retain a distinct simultaneous-writer clash witness.
- Plan 18 gets the late-POST span and the 30.484 s partial opening affordance. Keep browser readiness, actor handoff and gesture-to-request timestamps separate.


### C11 local development comparison

The same authenticated synthetic v30 started both independent arms with 300 root clips, 300 media identities and ten shot targets. App `76c58ee3` was constant. The strict arm used Agent `da212f2a` and Runtime `712d9754`. The local inverse used Agent `007b6123` with regenerated pins to Runtime `0e1711a2`. Its only Runtime change was the local inverse of the `c11cf75` snapshot comparison. The inverse stayed off the plan branches.

| Twelve-command SDK diagnostic | Strict | Local inverse |
| --- | ---: | ---: |
| SDK open | 151.817 s | 141.574 s |
| SDK commit | 32.374 s | 33.029 s |
| Runtime service wall | 23.139 s | 23.524 s |
| Runtime request thread CPU | 22.873 s | 23.219 s |
| Runtime process CPU | 22.977 s | 23.307 s |
| RealmStore mutex acquisitions | 104 | 104 |
| Total acquisition wall | 0.557 ms | 0.128 ms |
| Accepted replay calls | 1 | 1 |
| Memo clears | 0 | 0 |

Both arms accepted exactly the twelve one-frame audio moves, preserved the full fixture identities and published one current v31 head. The canonical revision and digest matched, and the canonical response document was 253,434 bytes on each arm. Each instrumented replay observed 18,156,125 metadata bytes, 1,916,699 record bytes and 474,427 result bytes in the persisted JSON fields. Startup and SDK warm-up differed. This comparison did not reproduce the suspected replay invalidation spike and gives no basis to relax the guard. Both diagnostic stacks were stopped and removed. This local SDK batch does not count toward the editor saving rounds or opening targets.

### Retained-history forward import measurement

Runtime [#88](https://github.com/banodoco/astrid-runtime/pull/88) carried Plan 77's retained-history verification into the current forward. Its candidate `52df1a13` passed all five unchanged ancestry tests, including the concurrent write during validation. The same 23 cost, WAL, history and descriptor IDs passed on the candidate and both parents. The shared timestamp oracle remains two verifications under Plan 77's strict invalidation, where current Release 15 main pins one.

The local measurement on `52df1a13` and exact Release 15 Runtime `2cf5890b` used the same captured film and deterministic WAV sequence. Five traced imports and five additional untraced imports per side and depth settled, with one stable head.

| Warm history entries | Plan 77 primary SQL statements per import, median | Main primary SQL statements per import, median | Plan 77 untraced seconds per import, median | Main untraced seconds per import, median |
| --- | ---: | ---: | ---: | ---: |
| 3 | 190 | 146 | 0.1311 | 0.1017 |
| 30 | 514 | 146 | 0.1215 | 0.1159 |

The additional statements increase with this history depth. The small elapsed samples include local decode and do not establish a production latency cost. The incoming Runtime revert `05d1ad88` reported about 1,450 extra statements per import on its own workload. This measurement uses the actual local media import. The unchanged concurrent-write ancestry witness separately checks the retained proof while validation is underway. Both are development evidence. The import tradeoff is recorded for the owner before release landing.
## Round 3 attempt — 22 November 2026, no result

The direct Linux installation used App `c5272db09d715bd38332f07e872aa53f6d65947a`, Agent `70d2a0f4c1aa1d7e90ddbd84669f4187f260447c` and Runtime `0bb855c364285b15828bbc9cd99dd6389dc54b36`. The App and Runtime passed normal local startup after the authenticated restore finished. The public preflight confirmed the exact v30 revision, publication `txn-a3dbef5643ae4893bbe8d7fe5ffb1bbf`, 300 root clips and media identities, ten shot targets and one active head. The one-clip control exists. The 616-clip and approximately 2.6 MB fixture requirements and the warm commit ratio remain unqualified.

| Measurement | Round 3 |
| --- | --- |
| Opening | The browser's fetch failed before the opening report. The App proxy recorded nine Runtime requests reaching its existing 60 s idle deadline. They include commit history, object reads, events, pack inventory, inspect, handshake and the project read. First usable and full open times are unavailable. |
| Saving and refusal | The matrix did not reach a gesture. All 85 scenarios and 255 repeats were unattempted. The sidecar saw no timeline commit POST. There is no time to Saved or clash result. |
| Integrity | Public preflight and postflight report the same v30 revision, publication, digest, one active head and all 300 root and media identities and ten shots. |
| CPU | The matrix stopped before emitting a qualified opening or scenario CPU interval. The Runtime and browser CPU figures are unavailable for this round. |

The primary tab emitted a basis-ready and saved-session handoff during startup, then a lifecycle cancellation. The complete opening and readiness assertions did not finish. The scratch sidecar preserved the original matrix assertions and recorded existing browser phases only. The browser was stopped and its temporary profile removed.

The host classified this attempt as **no result: setup and transport failure before any gesture** on 22 November. The initial retry direction was superseded by the independent cold-start diagnosis and the reduced Round 4. The deferred history call began about 0.13 s after handoff-ready. Existing activity remained stalled for approximately 125–157 s. The evidence identifies the interval and the associated request. Source inspection attributes the stall to full history replay under the shared Runtime store mutex.

Round 4 will record authenticated Runtime readiness separately from cold and warm browser opening, sample when a cheap read responds in under 1 s after the initial UI is ready, and exercise three existing one-clip gestures three times each. It will use guarded Undo or inverse cleanup and retain the original scenario assertions. The 85-scenario matrix remains incomplete. Its current restore cleanup repeats integrity verification per row. Round 5 repeats the reduced selection with the bounded fixes and CPU sampling. This fixture has yet to establish a warm single-save time, and the observed cold stall prevents a two-second any-time save claim.

**Plan deltas.**

- Plan 63 should cover the save affordance after authenticated reads time out during startup. Keep a separate Runtime receipt requirement for any later edit.
- Plan 75 should measure the shared Runtime work during concurrent authenticated reads, including history and objects. This round supplies no gesture or commit duration.
- Plan 76 still needs a two-tab overlap witness that starts from a verified writable timeline. Round 3 did not open the second tab.
- Plan 18 should measure which asynchronous calls gate first usable opening. The existing phase events can show a temporary handoff, and the public-head and readiness assertions still need to complete.


## Round 4 — 22 November 2026, reduced opening and save

The fresh direct-route stack used App `183ae4cf457cb02ec3db434cfeb225644d17af61`, Agent `70d2a0f4c1aa1d7e90ddbd84669f4187f260447c` and Runtime `0bb855c364285b15828bbc9cd99dd6389dc54b36`. The authenticated v30 synthetic restore exposed 300 root clips, 300 media references, nine tracks, ten shot targets and one active head at publication `txn-a3dbef5643ae4893bbe8d7fe5ffb1bbf`. A one-clip control is present on this realm. It supplies no paired warm ratio for this round.

| Interval | First usable | Corroborated full opening | Runtime CPU | Browser CPU |
| --- | ---: | ---: | ---: | ---: |
| Fresh restore and fresh browser | 42.381 s | 43.334 s | 20.53 s | 41.21 s |
| Same Runtime, fresh browser after harness correction | 42.526 s | 43.582 s | 20.63 s | 28.21 s |
| Same-profile reload in the continuation | 29.615 s | 30.493 s | 20.29 s | 41.57 s |

The initial browser sampled 13 timed-out metadata reads. The fourteenth got HTTP 200 in 3.338 s and the harness rejected the valid unwrapped response. It produced no subsecond-read timing or gesture. [App #356](https://github.com/banodoco/astrid-app/pull/356) landed the one-line harness decoder correction as `408c927195694731f511cec943d0f9eb7e936ffb`. The new browser used the same owned Runtime and verified v30 head. In that continuation, the first complete metadata read under one second arrived 152.779 s after the provisional full UI marker. The fifteenth sample took 20.325 ms. Warm-reload public corroboration retried twice after transport errors. The opening results corroborate UI and public identities. The rendered document does not independently expose its head identity.

The only attempted row was the first of nine, `video-move-same-track`. Saving appeared 0.786 s after the gesture, and “The save has not been confirmed” appeared at 31.071 s with Try again and Discard. No scoped commit POST was observed before the recorder sampled its after-head. Both immediate public reads failed with a transport error. The entire row, including those reads, took 183.739 s and used 179.77 Runtime CPU s and 20.09 browser CPU s. This interval supplies neither commit execution time nor a warm gesture-to-Saved time. Guarded Undo refused before editing. Eight rows were unattempted. An independent later public read verified the exact original v30 revision, publication and content digest, one active head and all 300 clip and media identities and ten shot targets. Both fresh profiles were removed, and the owned stack shut down and was deleted. This round counts as the reduced opening round.

The independent advisor kept the same v30 restore, opening/readiness probes, three existing gestures with three repetitions, timing thresholds and receipt-bound Undo for the Round 5 repeat. [App #354](https://github.com/banodoco/astrid-app/pull/354) yields between authenticated deferred pages of size two, with head-only and foreground targets preserved. [Runtime #89](https://github.com/banodoco/astrid-runtime/pull/89) preserves the live verification hook across transient integrity and historical-render stores. The combined run can measure their joint effect. If cheap reads and writes still stall behind authenticated history work, the result goes to the owner for a design decision.

The full 85-scenario matrix remains unfinished because its per-row restoring cleanup repeats the expensive history verification. The standard 616-clip, approximately 2.6 MB fixture, warm ratio, two consecutive passing full rounds and two-second any-time save claim remain open.

- **Plan 63:** use the observed unconfirmed move to specify evidence across the local durable queue, first dispatched request, receipt and Saved. Keep the known accepted-but-unconfirmed case from Round 2 distinct.
- **Plan 75:** measure cheap-read availability, warm opening, verification and row CPU separately. The large Runtime CPU interval here includes two failed verification reads.
- **Plan 76:** retain the simultaneous-writer test. This reduced round used one writing tab, so it gives no contention result.
- **Plan 18:** keep first usability distinct from transport and durable save readiness. Trace the observed gap between the allowed gesture and an actual dispatch.


## Round 5 — 22 November 2026, blocked save at the round cap

App [#358](https://github.com/banodoco/astrid-app/pull/358) `be9cc2407306eff06252c0d54be1c7f5afcacf3f`, Agent [#506](https://github.com/banodoco/astrid-agent/pull/506) `18adee8034973837a97fcd7392cd67f4566fa992` and Runtime [#92](https://github.com/banodoco/astrid-runtime/pull/92) `d7be2f0458a55c1f26e1138a125ffefe382f56f4` are the exact tuple. Generated pins select these two downstream inputs. The installed hook, history and Agent source identities matched Git. The setup used the same verified synthetic v30 restore with 300 roots, 300 media references, nine tracks and ten shots. The public preflight checked one head and the control timeline. The installer materialized the realm and its final claim timed out. The normal authenticated editor became ready on that same Runtime before public preflight and the fresh browser.

| Interval | Round 4 | Round 5 |
| --- | ---: | ---: |
| Fresh cold first usable | 42.381 s | 42.669 s |
| Fresh cold corroborated full opening | 43.334 s | 43.727 s |
| Cold opening Runtime / browser CPU | 20.53 / 41.21 s | 20.67 / 29.25 s |
| First complete authenticated metadata read under 1 s after UI marker | 152.779 s, same-Runtime continuation | 205.452 s, fresh run |
| Warm reload first usable / corroborated full opening | 29.615 / 30.493 s | 27.586 / 28.564 s |
| Warm opening Runtime / browser CPU | 20.29 / 41.57 s | 19.31 / 40.41 s |
| First move to unconfirmed save | 31.071 s | 30.960 s |
| Whole first row wall | 183.739 s | 451.819 s |
| Whole first row Runtime / browser CPU | 179.77 / 20.09 s | 447.99 / 28.44 s |

The original Round 4 cold browser stopped before its availability result. Its comparison value comes from a fresh browser on the already-running Runtime. Round 5 combined the two deferred-page and hook changes. Ten slower complete metadata responses arrived during the Round 5 availability probe before attempt 24 qualified at 347.988 ms. Cheap reads still timed out after warm reload. The reported row CPU covers the complete observation including authenticated reads and retries. Individual commit cost remains unmeasured.

The only attempted row was `video-move-same-track`. Saving appeared 0.421 s after the gesture, and the badge showed “The save has not been confirmed” with Try again and Discard at 30.960 s. The recorder observed zero scoped timeline commit POSTs before verification. Both after-head reads failed with transport errors. Guarded Undo refused before issuing an edit, leaving eight unattempted repetitions. Independent public postflight recovered the original v30 publication `txn-a3dbef5643ae4893bbe8d7fe5ffb1bbf`, exact revision and content digest, single active head and complete fixture inventory. The owned editor and Runtime shut down, and the fresh browser profile and stack were removed.

The fifth scheduled slot ends the loop. Cold and warm opening missed their provisional targets, and the comparison produced no verified warm save. The full 616-clip fixture and 85-scenario matrix, matched one-clip ratio and two consecutive passing full rounds remain open. The advisor found that two-item pages still drive a complete deferred history walk. Shared history and verification load are consistent with the measured delays. The paired batch and sampled CPU leave the exact work and source of delayed dispatch unresolved. The owner decision through the host is whether to hold this work for a larger redesign or consider a narrower set of demonstrated changes through exact review and release qualification. The retained-history import-cost decision is separate.

The advisor's next design removes the automatic whole-history walk after handoff, and resolves inverse targets on demand against the authenticated current revision and publication. Keep authenticated explicit complete history access, stale-head refusal, receipt checks and content proof. Further wide history or verification changes belong in Plan 75 or a separately accepted plan.

- **Plan 63:** pair the unconfirmed editor symptom with durable local queue, scoped request and authoritative receipt witnesses. Round 5 postflight kept v30, while Round 2 had a late single accepted receipt. Exercise both states distinctly.
- **Plan 75:** isolate whole-history work, authenticated-read waits and commit service in the profile. Round 5's 447.99 Runtime CPU s include competing reads and repeated verification. A first subsecond read at 205.452 s leaves subsequent service availability unqualified.
- **Plan 76:** continue to require a verified two-writer overlap and a real rejected clash. Round 5 attempted one writing tab.
- **Plan 18:** measure first usable UI, authenticated service access and gesture-to-request separately. The editor exposed the affordance and entered Saving while this edit had no observed dispatch.


### Loop closure and evidence archive

The host held promotion of the product changes, including the small deferred pages, hook repair and reinstated retained-history behavior, pending the owner's scope decision. The plan branches retain the measured tuple. The separately authorized save-loop tooling, fixture and README landed in App Release 15 as `ba34e184` after independent scope review and a matching exact Vitest comparison. All 14 paths are under `scripts/save-loop/`. [App #360](https://github.com/banodoco/astrid-app/pull/360)

The recorded seed curves and the authentication-required history reads show that accepted operations can grow far more expensive with the accumulated document and history. The unpaged Round 3 run observed a transport stall of roughly 125–157 s after deferred history began. Round 4's qualifying read arrived about 2.5 minutes after full UI. The Runtime serves its ordinary routes through shared store access while history verification is in progress. Round 5 admitted some slow reads earlier and still took 205.452 s for the first subsecond response. The live evidence supports separating history work, blockage and commit service in the redesign. It leaves the exact cause of the unsent gesture open.

Once the checkpoint and source witnesses are in place, a redesign can consider a persisted verification checkpoint or serving authenticated reads during verification. The proposed checkpoint still requires an owner decision and exact identity and freshness rules. The run archive holds this ready card at `round4-prep/persisted-verification-checkpoint-card.md` and the retention-cost measurements at `release-forward-0354/import-overhead/`.

| Evidence in the run archive | Path |
| --- | --- |
| Round 1 real editor and postflight | `sl-0/checkpoint-retime/round1-partial-288-connected-sweep.log` and `sl-0/checkpoint-retime/after-round1-attempt-composition-index.json` |
| Round 2 paired seed and partial matrix | `round2/paired-seed-curve.csv` and `round2/partial-288-results.jsonl` |
| Round 3 no-result and transport diagnosis | `round3/observed-round.md` and `ux-strategy/fable-round3-open-diagnosis.md` |
| Round 4 cold and continued rows | `round4/results.jsonl` and `round4/continuation/results.jsonl` |
| Round 5 exact rows and postflight | `round5/results.jsonl` and `round5/postflight-public-head.json` |

## Authorized Round 6 follow-up

The owner approved a persisted verification checkpoint and one measured follow-up on 22 November. The original five-slot results above stand. The separate quick indicator first measures unchanged product at empty, 10, 100 and restored v30 sizes. The checkpoint comparison uses the same restored v30 and reports startup to a subsecond cheap read, cold and warm opening, warm edit to authoritative Saved, and Runtime CPU. Independent verification review precedes the measurement. No current product promotion is approved.

Runtime checkpoint implementation [#96](https://github.com/banodoco/astrid-runtime/pull/96) and forward [#97](https://github.com/banodoco/astrid-runtime/pull/97) reached Plan 77 Runtime `86343f3b`. The 25 matched checkpoint cases passed on both sides of that forward and 118 project-element cases passed on the combined Runtime. These are development checks. The exact hosted workflow was cancelled and its single retry is underway. The exact Release 14 Agent reproduced the Windows VibeComfy path witness refusal in a matched long local scratch path. The Plan 77 old and new Agent pass the same 51 cases in a shared short scratch path with the original assertions. The App forward preserves Plan 77 save paths and the exact Plan 69 test file, including the five additive cases. The development tuple is App `5607d00f`, Agent `fda01977` and Runtime `86343f3b`. No Round 6 opening, save or CPU observations have been recorded.

### Local qualification during the CI freeze

[Runtime #99](https://github.com/banodoco/astrid-runtime/pull/99) reached `0dc004be` with the executing-verifier guard. The independent pair passed all 25 shared IDs and seven new installed cases. Exact hosted work was cancelled during the CI freeze.

The last local repair, Runtime `db81cd55`, identified two more ways the installed verifier's behavior could differ. The independent pair passed 32 shared IDs and two new drift cases. An unchanged installed restart reused the checkpoint with zero semantic replays. The final source review blocked reuse because a required digest format check reaches a Python helper whose behavior can change while the stored verifier version remains the same. In that case a full check could refuse a history the checkpoint would accept. This last finding comes from source review. The host withheld the checkpoint from release and kept full semantic replay. Round 6 was not measured. The final verdict and the plain-language explanation are in the run archive at `round6/checkpoint/safety-review/final-local-effective-verdict.md` and `round6/checkpoint/owner-integrity-note.md`.

The corrected quick indicator passed independent local source review and all 13 named checks on App tooling commit `a0339fe7`. It measures the unchanged Round 5 product separately from the held checkpoint. The empty fixture was built and verified through the installed public interface. Its first setup stopped before timing because the operator had pre-created the empty support parent. The ordinary backup wrapper then created and marked its own support parent, made the authenticated backup, and the run proceeded from the same stopped fixture.

The managed launch then refused the different data root of the restored fixture. The host approved the existing direct restore and adopt route. It uses a fresh Chrome profile after Runtime adoption and leaves launch-to-read unobserved. On unchanged Round 5 App `be9cc240`, Agent `18adee80` and Runtime `d7be2f04`, the empty timeline reached the writable V1/A1 control in 24.146 s, outside the quick opening bands. The stable UI marker took 25.014 s and used 0.23 Runtime CPU s and 17.04 Chrome CPU s. The first track rename reached confirmed Saved in 1.329 s and the quiet repeat in 0.752 s. The two guarded Undo steps passed.

An additional read-only opening trace reached the same empty control in 19.906 s. HTML had loaded at 0.125 s. The first workspace configuration fetch began at 17.465 s after a large source-module fan-out. The first Runtime health and handshake began at 18.058 s. Pack inventory and project-element requests took 56 ms and 68 ms. The longest completed fetch took 227 ms. These are Linux Vite source-dev observations. They do not establish packaged App opening times or the cost of rendering a heavy timeline. The run archive holds both receipts at `quick-baseline/direct/empty/results.jsonl` and `edit-dispatch-trace/empty-opening/summary.md`.

The host deferred the remaining quick sizes to trace a single video move, first on an isolated one-clip timeline and then from two fresh restores of one authenticated v30 backup. The second heavy arm skips automatic deferred history reads for diagnosis while preserving verified head and source reads, commit validation and authoritative acceptance proof. A change to the product's history scheduling needs a separate owner decision.

The unchanged one-clip control dispatched and saved. The exact verified handoff preceded pointer-up by 767 ms. Capture started at 5 ms and resolved at 334 ms. Saving appeared at 588 ms, the one matching commit POST started at 738 ms, and its HTTP 200 response arrived at 905 ms. The accepted head was adopted at 918 ms. The badge reached confirmed Saved at 1.001 s, with the independent public head read complete at 1.170 s. One active head and the exact clip and media inventory remained. The clip moved from 10.0000 to 10.5667 s on V1. The first tool left append, pump and outbox reservation unobserved. See `edit-dispatch-trace/one-clip/summary.md` in the run archive.

The standard installer sends users to the compiled hosted editor. The documented fully local route for changing the editor serves Vite source modules. The Round 3 opening attempt and the Rounds 4–5 cold and same-profile opening intervals were measured on the source-dev route. They do not establish installed hosted opening times. The subsecond metadata wait times retain their original UI-marker start, and the gesture results retain their original clocks. The empty compiled preview is a separate local comparison with the same Runtime proxy.

### First restored v30 move and compiled empty control

These are diagnostics on the unchanged Round 5 product and its verified synthetic fixtures. The 300-clip Vite source-dev run used the same authenticated v30 backup, with deferred history enabled, one fresh profile and 19 verified tracer anchors. A single same-track V6 parent clip move entered capture 22 ms after pointer-up and was refused at 243 ms with `child-ownership-unavailable`. Saving appeared at 0.899 s. The outbox pump found zero intents at 1.339 s and 74.840 s. The badge showed “The save has not been confirmed. Your changes are kept.” at 31.587 s.

| Interval | Observation |
| --- | --- |
| Gesture to commit POST | Unobserved within 90 s |
| POST to response | Unobserved |
| Response to confirmed Saved | Unobserved |

The independent preflight verified the original public v30 head. The App observed original publication `txn-a3dbef5643ae4893bbe8d7fe5ffb1bbf` on both later adoptions. The after-query only ran after HTTP success, so there is no independent terminal public read for this refused edit. The historical Runtime does not emit default HTTP request logs. The browser saw no matching POST. One deferred history page was in flight at pointer-up, and a separate full read started after the refusal. The pre-editor one-minute load was 0.99. The stack and profile were removed.

The trace shows no gesture-specific move basis at capture. App `useClipDrag.helpers.ts:342–345,366–373,501–510` forwards that basis only when the resolved drag meets the single-clip, object identity and same-row conditions. With child data present, `timelineLocalSaveHandoff.ts:517–552` checks an unnamed edit via the synchronous guard at `:110–208`. It reads the verified current parent, child occurrences, pinned groups and before/after editor state. It imposes no clip-count cutoff and does not consult history pagination. The original v30 has nine tracks, ten shot/internal dependencies and ten occurrences on V1. The target was ordinary V6 parent media. This first trace does not identify which drag predicate or ownership guard branch refused, or whether the profiled real timeline shares the relevant layout.

A separate local compiled preview from the same authenticated empty fixture reached writable UI at **1.585 s**. It requested 21 scripts and 64 fetches. The workspace configuration request began at 0.429 s and Runtime health at 0.461 s. Pack inventory took 35 ms and project elements took 53 ms. The distinct source-dev breakdown reached the corresponding control at 19.906 s with 2,055 script requests. The compiled comparison has no heavy timing or hosted latency sample. The Round 3–5 source-dev times keep their original scope.

The owner authorized a separately measured App-only opt-in to fetch verified history on demand. Local candidate `08c0fe11` starts at the exact Round 5 App tree with byte-identical downstream pins and preserves the existing automatic-read assertions in default mode. Independent source review blocked it on incomplete or duplicate ancestry, cancellation visibility after changing timeline, responsiveness when an obsolete request hangs, and test fixture isolation. The candidate remains unmeasured and unpromoted. The Runtime checkpoint stays withheld.

The run archive holds the v30 timeline and source proof at `edit-dispatch-trace/v30/on-vite-retry/{summary,capture-boundary}.md` and the compiled control at `edit-dispatch-trace/empty-opening/packaged/summary.md`.

The source-dev ten-clip control used the same Round 5 tuple, a separate authenticated backup and the same named same-track video move. First usable took 23.985 s. The stable UI marker took 24.867 s with 0.73 Runtime CPU s and 18.43 Chrome CPU s. The qualifying post-open read returned in 0.059 s. Launch-to-read is unobserved on the direct restore route.

| Ten-clip move | Gesture to POST | POST to response | Response to confirmed Saved | Gesture to confirmed Saved |
| --- | ---: | ---: | ---: | ---: |
| After first usable | 713.8 ms | 1,829.3 ms | 751.5 ms | 3.295 s |
| After qualifying read and first Undo | 684.9 ms | 353.2 ms | 374.8 ms | 1.413 s |

Each move issued one matching HTTP 200 POST and independently advanced the public head with no clip, occurrence or media ID loss. Both guarded Undo receipts restored the original revision. This control has no shots, so the difference from the 300-clip fixture varies both the document size and the ownership shape. See `quick-baseline/direct/10/results.jsonl` in the run archive.

### Tiny same-shape move and compiled v30 opening

The source-dev control at the same Round 5 tuple had six generated parent clips, one SDK-created V1 shot occurrence and the ordinary parent video on V6. Its same-track pointer move captured with a verified move basis and confirmed Saved in **1.4847 s**. The split was 881.3 ms to commit POST, 216.4 ms to HTTP response and 387.0 ms to confirmed Saved. The independent public read completed at 1.8229 s and verified one exact CAS advance with one active head. The V1 occurrence's ID, owner and track and both immutable child pins stayed the same, with all root clip and media IDs preserved.

All five history pages observed in that run were settled at pointer-up and the trace recorded zero walks in flight. That tool did not mark successful same-head installation. The small fixture shows that a V1 occurrence and ordinary V6 parent move can save together. It leaves the exact failing drag predicate on the larger fixture open, with both layout and concurrent work possible. An initial preflight stopped before navigation because the generic decoder expected a different occurrence ID field. The retry verified the raw occurrence and both scoped child revisions and ran the sole gesture. Both setups cleaned their profiles and stack. Receipts are under `quick-baseline/diagnostics/tiny-same-shape-decoder-retry/`.

On a separate fresh restore from the exact v30 backup, the local compiled preview showed all 300 expected root clip IDs, nine rows and the writable V6 control at **22.994 s**. It made 21 compiled script requests and 269 fetches through that marker. Runtime health began at 0.760 s and the Runtime host process used 19.89 CPU s. Chrome recorded 6.26 s of task time, including 2.918 s of script time. Several object and commit-history reads lasted about 17.8 s in overlapping intervals. After the marker, the independent public read verified the original v30 revision, one active head, 300 root clips and ten occurrences. The probe sent no edit and observed zero timeline commit POSTs. The owned stack and fresh profile were removed.

This is one compiled local preview with the full 300-clip inventory marker. The empty compiled control measured its writable V1/A1 marker. The earlier Rounds 1–5 and SL-2 browser figures used source-dev. SL-0's native SDK commit timing has a separate clock. No hosted latency or compiled heavy save has been measured. The separate opening receipts are under `edit-dispatch-trace/v30/compiled-opening/`.

## Compiled drag at first readiness and after history

This development comparison follows the five scheduled rounds. Both fresh restores used the same authenticated 300-clip v30 backup, Round 5 App `be9cc240`, Agent `18adee80`, Runtime `d7be2f04`, and one locally compiled App artifact with output SHA-256 `30cb2a430734ebf836d85b4b3a6ad505dc2c9d351fdc0ccb55252ce9bd285d25`. The target was `fixture-video-0154` on V6. Each browser received a trusted horizontal drag of 18 px from the clip centre.

| Timing point | Full writable | From writable to pointerdown | Capture refusal after pointerup | Generic waiting notice after pointerup | Independent public postflight |
| --- | ---: | ---: | ---: | ---: | --- |
| First writable | 22.858 s | 0.178 s | 0.229 s | 31.607 s | Browser snapshot reached its deadline |
| History installed and GETs idle | 22.572 s | 323.537 s | 0.231 s | 31.573 s | Separate public read verified original v30, one active head, all 300 clip IDs and all ten occurrence IDs |

Both gestures requested the source track. The planner resolved another track and the App withheld its same-track move basis. The ownership guard recorded the destination as shot-occupied and refused capture. Both outboxes stayed empty. There was no commit POST, response or confirmed Saved, so all three save timing segments are unobserved. The settled arm verified the installed exact-head ancestry and all 15 successful deferred pages, with none in flight and 1.152 s of network idle at pointerdown. Other opening GETs included failures.

The settled trace recorded a 1700×1500 viewport, fixed V6 and V1 row boxes, constant scroll, and a V6 hit at down, every move and up. The clip itself remained at its original V6 position through the sampled frames up to 1.107 s after release. Drag-ghost motion was unobserved. Both sampled row edges still hit V6 outside the clip body. The first arm did not record absolute coordinates or row boxes.

The existing collision-planner test expects a search for another compatible row when the requested interval overlaps its sibling. The handoff separately tests refusal on a shot-occupied track. The mounted editor reported dirty and then saving before the generic “The save has not been confirmed. Your changes are kept.” message. It showed the generic message about 31.6 s after a capture rejection and no durable edit. That user-visible refusal is a separate product finding. The next diagnostic selects a collision-free interval from the verified document before the gesture. [Collision planner test](https://github.com/banodoco/astrid-app/blob/be9cc2407306eff06252c0d54be1c7f5afcacf3f/src/tools/video-editor/lib/clip-drag-planner.test.ts#L307), [Shot occupancy test](https://github.com/banodoco/astrid-app/blob/be9cc2407306eff06252c0d54be1c7f5afcacf3f/src/tools/video-editor/hooks/timelineLocalSaveHandoff.unnamed.test.ts#L317)

These arms used App be9cc240, which predates Release 14's save fixes; the generic 31 s notice and the deferred history walk (344 s) describe that older save path and are re-measured on App e3dbad64 / Agent 8807f820 / Runtime 23310dc8 in the following section.

## Stock compiled opening on the landed Release 15 tuple

The stock installed comparison used App `e3dbad64`, Agent `8807f820` and Runtime source `3c28211f`, whose tree equals the landed Runtime `23310dc8`. It used a fresh restore of the same signed synthetic v30 fixture with 300 clips, nine tracks and ten shot occurrences.

Authenticated restore preserved the realm ID and verified the original database SHA-256 `c0b27bb02c33d5b1e72699749c07adc769dda0c0eb2ceaceab222b630c6e132d` byte-for-byte. The direct adopt command reached its final claim timeout. The selected catalog, exact authenticated live instance and safe stop corroborated adoption. The stopped database SHA-256 was `c11cfb8f67e91feac4819f5a0ebc3603d4f4c4d7116978f51fbbd126f1fbd28d`. Restore and adopted database both report schema 33. This run leaves the cause of the post-adoption digest change open.

The exact stock compiled App reached the navigation marker in 0.062 s and stopped at the writable gate after 480 s. The observer recorded 1,737 same-origin request starts and zero timeline commit POSTs. The first history GET began at 1.842 s and the second at 62.541 s. Neither had a recorded response. The proxy logged 60 s upstream idle deadlines on several other routes. The browser never verified all 300 clip controls and nine writable rows, and the terminal public snapshot remained unobserved. The owned stack stopped safely and the browser profile was removed. These measurements establish an opening failure in the timed synthetic run. They leave collision refusal, first-writable save and quiet save on the landed tuple unmeasured. [Stock observation](evidence/2026-11-22-release-15/current-stock-failed-observed.json)

On this App, the initial authoring basis awaits the full paginated same-head history at 50 items per page, then reads the immutable document dependencies. The App awaits the verified basis before it hands off editing. That path uses the default history option. The former deferred walk number remains an observation of the Round 5 App. [History read](https://github.com/banodoco/astrid-app/blob/e3dbad64d402724ac5a35fb6447f18e432c64b78/src/integrations/runtime/dataProvider.ts#L909), [Authoring basis](https://github.com/banodoco/astrid-app/blob/e3dbad64d402724ac5a35fb6447f18e432c64b78/src/tools/video-editor/hooks/useTimelineSave.ts#L391)

### Cold profile and same-process reopening

A second fresh restore on the landed tuple used the same stock compiled App and a read-only opening. The browser reached the writable marker in 306.552 s. The Runtime host process used 291.80 CPU s from birth to navigation and 295.62 CPU s from navigation to writable. A fresh browser profile on the same Runtime process reached writable in 13.744 s and used 6.17 Runtime CPU s. Both terminal browser reads verified the original public v30 revision, one active head, all 300 clips and ten occurrences. The observer recorded zero timeline commit POSTs and removed both profiles. [Cold opening](evidence/2026-11-22-release-15/runtime-a-cold.json), [Same-process reopen](evidence/2026-11-22-release-15/runtime-a-warm.json)

The cold browser tried a limit-50 history request without a cursor at 1.907 s, 122.440 s and 243.142 s. The first two attempts timed out around 60 s after dispatch. The third finished with HTTP 200 at 300.446 s. The warm browser requested the same first page at 1.762 s and received HTTP 200 at 8.802 s. Both writable markers showed zero history GETs in flight. Each marker followed the initial history response by several seconds.

The cold 30 s stack snapshot showed one active Python thread in semantic history replay while holding the shared store mutex. Five object reads, a pack lease prune and two other operations were at the same mutex acquisition. The 120 s snapshot showed ten object reads at that call site. The 300 s snapshot sampled a response write. The Runtime disables its default request access log. The browser request tape and App proxy supplied the HTTP observations. [History mutex](https://github.com/banodoco/astrid-runtime/blob/3c28211f3cb7ac4867ad744d8cdeeb38dd4484c5/runtime_protocol/service.py#L3464), [Object read mutex](https://github.com/banodoco/astrid-runtime/blob/3c28211f3cb7ac4867ad744d8cdeeb38dd4484c5/runtime_protocol/service.py#L6247)

Among 26,862 decodable weighted py-spy samples, 59.90% included `list_timeline_commits`, 56.23% included `_history_page` and 40.60% included `_verify_accepted_replay`. JSON-schema validation's `descend` accounted for 27.26% of leaf samples, followed by schema `type` at 10.79% and JSON `iterencode` at 7.54%. The scratch py-spy 0.4.1 capture sampled at 100 Hz and reported 3,008 acquisition errors. The archived ranking records the further losses in decoding the raw output. [Profile index](evidence/2026-11-22-release-15/runtime-a-cold-profile-index.json)

After the timed warm run, the standard-size 1440×900 browser showed the V6 target at its original position. Seven rows had visible area, with A2 and A3 below the visible timeline. The viewport check sent no gesture.

### Disposable paired Runtime

Runtime B `c3f811cbddcddb88a5fbae2114c134198265375f` merged the current Runtime release with the nine Round 5 Runtime commits. The SQLite WAL custody guard was included. The later persisted replay checkpoint was withheld. The install used the same App `e3dbad64` and Agent `8807f820`, the same 355 compiled files and a fresh authenticated restore of the same v30 database. The three changed installed Runtime modules matched their Git source bytes. The local Runtime source remained unpushed. [Restore and build identity](evidence/2026-11-22-release-15/runtime-b-reuse-and-restore.json)

B reached the exact writable marker in 176.179 s. The Runtime process used 306.85 CPU s from birth to navigation and 166.78 CPU s from navigation to the marker. Its first limit-50 history request began at 1.984 s and failed near the proxy deadline. Its second began at 122.548 s and completed with HTTP 200 at 169.724 s. The single browser verified the original public v30 with one active head, 300 clip IDs and ten occurrences. The run observed zero timeline commit POSTs and removed the owned stack and profile. [B opening](evidence/2026-11-22-release-15/runtime-b-disposable.json)

B took 130.373 s less than the profiled A cold opening. It made one fewer history attempt. The successful history request took 47.176 s on B and 57.304 s on A. This one-trial pair leaves the individual commit effects and cold-open variability unresolved.

A repeat on the same B Runtime process reached writable cold in 162.362 s, with 287.67 Runtime CPU s before navigation and 153.08 s during the browser interval. Its two limit-50 history attempts took 60.244 s without a completed reply and 8.059 s to HTTP 200. The browser verified one active original v30 head with 300 clips and ten occurrences, and recorded zero timeline commit POSTs. A same-process reopen then stopped at 600.048 s without writable: it used 440.87 Runtime CPU s before navigation and 320.75 s during the browser interval; two history attempts took 60.379 s and 155.389 s without completed replies, with no third attempt and no terminal head. The two openings matched Runtime PID and birth identity. Cleanup closed three ports and left zero new profiles. B repeat therefore does not establish reliable warm reuse or which memo invalidation path ran. [Sanitized receipt](evidence/2026-11-22-release-15/runtime-b-repeat.json)

C cold and same-process openings used separate browser profiles on the same Runtime process and both reached writable, in 165.019 s and 170.095 s. They verified the original head and observed zero timeline commit POSTs. C therefore supplies a warm qualified opening but does not explain B repeat's stopped warm attempt. [C openings](evidence/2026-11-22-release-15/runtime-c-openings.json)

For the historical 22.994 s opening on the full Round 5 tuple, file timestamps place navigation approximately 19m00s after installation began, 17m28s after restore began, and 12m14s after direct adoption began. The Runtime used 19.89 CPU s during the timed browser interval. The pre-navigation process CPU and replay cache state remain unobserved.

The nine Runtime commits used in B are out of the Round 7 cut and any earlier landing proposal. Their combined same-process reopen did not qualify. Any future reuse needs a separately measured change with the stock warm-read and import comparisons. The socket timeout and the Runtime proof transitions have separate code paths. [Source audit](evidence/2026-11-22-release-15/runtime-b-memo-audit.md)
