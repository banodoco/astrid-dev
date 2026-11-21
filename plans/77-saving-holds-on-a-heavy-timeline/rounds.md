# Rounds — Saving holds on a heavy timeline

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Handover](handover.md)

One section per round, newest last, written by the coordinator under the [live-loop workstream](../../skills/roles/astrid-dev-manage/workstreams/live-loop.md#the-round). Each holds: the stack versions; a table of scenario, outcome (saved or refused with the reason shown), time to Saved, head count, anything vanished; The strategist's advice (evidence, not a verdict); the fixes picked and their PRs; and **Plan deltas** for [Plans 63, 75 and 76 and 18](inputs.md#references).

No round has run yet. Round 1, on the plan branches as cut, is the baseline. The 18 November sweep (14 edit kinds, 3 saved, 11 refused, on the owner's copied timeline with the old timer) is earlier evidence, not a baseline: [evidence/results.jsonl](evidence/results.jsonl).

## Setup checks on 21 November 2026

No timed baseline yet. On App `7fc14d2f`, Agent `c00721de`, Runtime `e43bfccc`, a nine-track SDK commit advanced the public head. Fresh SDK reopen was refused with `accepted commit inputs changed during verification`, and Runtime logged a WAL move. A one-track control reopened, as did the nine-track control on App `e576c7fe`, Agent `efccee92`, Runtime `162500fe`. One subsequent bounded shot seed advanced a public head while the SDK reported its outcome unknown. Release 14 owns the fix. [Release 14 integration issue](https://github.com/banodoco/astrid-dev/issues/796)

The deliberate no-op probe on App `75120d7c`, Agent `c00721de`, Runtime `e43bfccc` produced three expected failed rows, one unchanged publication per row, and zero successful commits. It used an empty sandbox timeline. The heavy fixture must qualify before measuring Round 1.

## Local WAL development probe on 21 November 2026

This setup probe used disposable local pins and leaves the baseline round count at zero. App used launcher base `75120d7c`; Agent used `c00721de` with local pin-only commit `ceed78eb`; Runtime was built from `8be4f258`. The nine-track SDK commit advanced the public timeline from version 1 to 2. The public head matched the accepted receipt, and a fresh SDK session reopened it. The Runtime emitted zero WAL warnings for that probe. Release 14 still owns the product integration. [Runtime PR #79](https://github.com/banodoco/astrid-runtime/pull/79)

## SL-0 pacing comparison on 21 November 2026

The unpushed `8be4f258` Runtime development stack imported and selected 616 generated assets in 131.5 s. It then accepted 108 clips across nine 12-command SDK batches. The public index confirmed version 11 and publication `txn-469ff762ca1a41e9ad1d7f98675c9417` after the seed stopped. Batch wall times in seconds were 3.2, 10.1, 16.8, 23.6, 31.6, 41.4, 49.7, 57.7 and 70.7. These were accepted seed batches, distinct from the November 18 one-edit warm median and editor time to Saved. The full fixture, canonical byte count and warm comparison remain open.

The comparison used the same App fixture script and media digests with App `e576c7fe`, Agent `efccee92` and Runtime `162500fe` from Plan 69. It imported and selected 616 assets in 132.1 s and accepted the first 12 clips in 3.6 s. The public index confirmed version 3 and publication `txn-2fc61a3d1a414c21bb517441d766f8be`. Before the second batch could submit, a pinned source read refused because the SQLite WAL moved. A read-only SDK reopen after the writer stopped returned the same verification refusal. The two runs separate the nine-track WAL result from the heavy seed's performance. The older tuple stopped too early to attribute the batch-time growth to Release 14 or to existing history costs.

Both are pre-baseline development runs. Keep FIX-16 and FIX-21 out of the baseline App until the integrated Release 14 tree lands. The Release 14 App and Agent forwards are held for that integration. The shipped candidate still needs the full synthetic fixture and the live matrix.

### Matched checkpoint guard

The same generated media and public SDK seed ran with the earlier Plan 69 Runtime `162500fe` plus only the two checkpoint changes from Runtime PR #79. The disposable Runtime `15f0fef` and pin-only Agent `5cb9fccd` were used with App `e576c7fe`. Nine accepted 12-command batches took 4.455, 4.388, 5.421, 6.339, 8.013, 8.944, 10.333, 12.517 and 13.266 s. The public head was version 11, publication `txn-be71171a630449f498f6dad7d5f36986`, and a fresh SDK session reopened 108 clips. The full integration tuple took 70.691 s at batch 9, 5.33 times the matched-guard run. The checkpoint changes alone cleared the earlier false refusal. Multiple product changes distinguish the full tuple, so this comparison does not identify an individual commit as the cause. Both are pre-baseline development measurements.

**Plan deltas.** Plan 75 owns the pre-existing history cost. After the first batch, the older line grew by about 1 s per successive 12-command batch. Route the larger slope in the full integration tuple to the Release 14 Lead. No new evidence for Plans 63, 76 or 18.

### Release 15 ownership

On 21 November the owner assigned the false checkpoint refusal and commit-cost investigation to Plan 77. The checkpoint repair is a setup fix because a routine checkpoint can block the seed and reopen. The first baseline round will record that repair and its regenerated Runtime, Agent and App pins. The App and Agent Release 14 forwards remain held. The component split and first-parent investigation are development evidence for the first loop candidate. The baseline round count remains zero.
