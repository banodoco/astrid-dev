# SV-3 measurement, fourth run: completed, 3 repetitions, 23 November 2026

Approved for exactly: package head `53bbbda5b297ab82e640ed7cc885c77a77b42339`, `package.sha256` digest `6eaaa32f1b894f9808ca1b481802f6f083c8e10c20a6390941b101591c516138`, candidate Runtime `f2da02e1dcf02439ee149f1412310c72aa4bf0bb` (tree `533503fa4c3639faafc185c34f8be8a39b6452c4`; the SV-2 fix on top of SV-2b and SV-2d, dependency and contract diff against the retained Runtime empty). One run, three repetitions, 15:56Z to 16:04Z. Exit 0; idle-safe stop verified each repetition, ports closed, no leftover Chrome, boundaries unchanged (`cleanup.json`, `boundary.json`: signed backup, owner files and the original `direct-data` listing unchanged). Free disk never went below 18.2 GiB (`free-kib.tsv`, stop at 16 GiB). The Runtime start took about 2.5 minutes each time and is not counted in any save time.

## Plain summary

**The fixture does not meet the gate: every save took about 20 s from POST to 200, cold or warm.** The gate is a median release-to-Saved of at most 2 s and none over 4 s. Release-to-Saved (release of the drag to the Saved badge) per scenario, over the 3 repetitions (`summary.tsv`, `measurements.jsonl`):

| Scenario | Saves | Median | Max |
| --- | --- | --- | --- |
| Cold first save after Runtime start | 3 | 24.8 s | 25.2 s |
| S1 one edit alone (warm) | 3 | 22.7 s | 24.8 s |
| S2 two edits, one after the other | 6 | 22.5 s | 23.9 s |
| S2o two edits, the second released without waiting for Saved | 3 | 21.3 s | 24.8 s |
| S3 ten edits, one after the other | 30 | 21.6 s | 24.4 s |
| S3o ten edits, released 150 ms apart | 3 | 22.3 s | 22.8 s |
| S4 five drags, each waited to Saved | 15 | 21.6 s | 24.4 s |

- **Where the time goes:** POST to 200 is 16 to 23 s in every save, release to POST is 1.0 to 2.0 s, 200 to Saved is 0.6 to 1.0 s. Warm saves are no faster than the cold first save (cold 22.2 s median POST-to-200, warm 17 to 23 s). For comparison the earlier first-cut profile of two consecutive saves on the same fixture was 55.5 s for the first and 17.7 s for the second, so the first save is about 2.4 times faster and the repeated saves are not faster.
- **Refusals: none.** Every commit POST answered HTTP 200 and the badge reached Saved. `refusals` in `summary.tsv` and `refusal_count` in the JSON count drags marked failed by the driver's own post-condition, not Runtime refusals: after the cold save every sequential drag failed the driver's assertion `commit.status === 200 && commit.outcome === 'accepted' && commit.exactCas && commit.exactAcceptedCas && commit.receipt` although the POST returned 200 and Saved (`failed_reason` in each repetition JSON; `refusals: []`, `non_2xx_runtime: none`). The save timings are valid; the exact-CAS and receipt checks after the first save are not established by this run. The Runtime log delta has no `head_busy` or `moved total_changes` line in any repetition.
- **S0, the verified-head read right after the cold start on the 300-clip fixture:** page ready in 6.0, 5.9 and 5.0 s, verified-head status 200, not refused.
- **Overlapped edits were coalesced:** the editor sent one POST for each of S2o and S3o (21 POSTs per repetition in total, 19 expected from the sequential scenarios plus those two). The later drags of S2o and S3o are recorded as failed drags: the tape did not accept a drag released while a save was in flight.
- **Pack host:** `pack-host.json` says `pack host running` in all three repetitions: the stack's pack-host log grew by 2841 bytes with no crash line (the Runtime's own supervisor started it from the rewritten service declaration `rep-N/services.json`). The idle claim poll itself is not logged, so polling is inferred, not proven. No `head_busy` occurred.
- **Agent authoring commit:** not measured (`agent-commit: not established`).

## Caveats

- Eighteen of the 21 sequential drags per repetition are flagged `failed` by the driver's own check, so the per-scenario `n_posts`, `failed_drags` and `refusals` columns in `summary.tsv` should be read as described above; the timing columns are from the observed POST and response.
- The scenario 5 (edit while a generation runs) was dropped by decision; no local generation exists.
- The work copy, not the retained data, was written; the pristine and work copies were removed by the script.
