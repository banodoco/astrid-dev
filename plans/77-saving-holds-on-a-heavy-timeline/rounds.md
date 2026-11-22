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

The harness recovered startup by using a short owned browser directory and the installed editor's ordinary `connect=1` link. A fresh browser then reached the actual Saved badge at 41.211 s with the synthetic fixture visible. That figure measures startup. The unchanged edit-timing matrix is in progress. No scenario result or qualified-heavy claim is recorded yet. [App harness PR #330](https://github.com/banodoco/astrid-app/pull/330)
