# SV-4 combined (attempt 3): full candidate Runtime `eb4e8644` with the Agent two-file overlay, three repetitions, 24 November 2026

Run exactly as sent by the Plan 89/77 orchestrator: package astrid-dev branch `release-15/p77-sv4-combined-package` head `9667048eb3f6b0e5decb4735a92d7c60ce5fd289` (manifest digest `9a012700e773c31a9827d4245e7dea31dfea6064d0567c8ee95f97231dea1a3c`, clean `sha256sum -c`), Runtime `eb4e8644e3549c88d5d836cd5738ca75e76d311a` (tree `01a93de2cf578c62c7c9804b2ff758f449340c00`: release `24e2c929` with the SV-2 fence fix, SV-L1 spans, daemon timing sink, the SV-4 covers index and the covers counters and timer; dependency and contract diff against `77c38d03` empty), Agent `096a2fb3536192785fabd33e6673ba8ab4ef5ead` (only `_commit_patch.py` and `_doc_patch.py`; `rep-N/agent-loaded.json` `failures: []`). One attempt, three repetitions, 02:15Z to 02:37Z, **exit status 0**. Idle-safe stop verified in every repetition, ports closed, no leftover Chrome, boundaries unchanged (`cleanup.json`, `boundary.json`). Free disk fell to 16.45 GiB at the lowest point (`free-kib.tsv`, stop at 16 GiB). `daemon-startup.stderr` is empty in every repetition. The supervised pack host ran in all three (`rep-N/pack-host.json`: `pack host running`). **The Runtime carries the covers counters and timer, so all numbers are instrumented.** The Agent authoring step is a stub and the run does not prove a save during a generation.

## Result

**No refusal anywhere: S0 (the verified-head read after the cold start) returned 200 in all three repetitions (verified-head request 5.2, 2.2 and 1.8 s; editor writable after 15.3, 6.2 and 6.6 s), all 34 commit POSTs per repetition returned 200 and reached Saved, and the driver's post-condition passed on every save. Warm saves take about 5.1 s from POST to 200 and about 6.8 s from release to Saved; the gate (2 s median, none over 4 s) is still not met.**

Release-to-Saved (`summary.tsv`, per save in `summary-per-save.tsv`):

| Scenario | Saves | Median | Max |
| --- | --- | --- | --- |
| Cold first save after Runtime start | 3 | 13.0 s | 15.6 s |
| S1 one edit alone (warm) | 3 | 6.8 s | 6.8 s |
| S2 two edits, one after the other | 6 | 6.9 s | 7.2 s |
| S3 ten edits, one after the other | 30 | 6.7 s | 7.1 s |
| S4 five drags, each waited to Saved | 15 | 7.0 s | 8.0 s |
| All 54 warm saves | 54 | 6.8 s | 8.0 s |

Of a warm save: release to POST 1.2 s (median), POST to 200 5.1 s, 200 to Saved 0.5 s. Cold POST to 200 is 10.7, 13.9 and 10.6 s. For comparison, `c9e535bd` with the same Agent overlay had warm POST to 200 of about 10.4 s and 12.5 s release to Saved; this candidate roughly halves both again.

## Per-stage breakdown from the Runtime's own timing lines (`rep-N/timing-sink/commit-stage-timings.jsonl`)

All 34 lines of each repetition were captured and matched one to one with the 34 POSTs (`commit-timing-summary.json`: `lines_matched: 34`, `mismatch: false`). `runtime_wall_ms` equals the sum of `exclusive_timings_ms` and is 99.5 to 100 % of POST to 200 on every one of the 57 sequential saves (median 99.9 %): the Runtime accounts for essentially all of the POST-to-200 time and the wire and proxy add about 0.1 %.

| Exclusive stage, median | Cold save (3) | Warm sequential save (54) |
| --- | --- | --- |
| Runtime wall | 10.7 s | 5.08 s |
| `provider_commit` | 8.27 s (max 11.7 s) | 2.56 s (max 2.9 s) |
| `port_store_accept` | 1.70 s | 1.71 s |
| `durable_reconciliation` | 0.37 s | 0.41 s |
| `handler` | 0.30 s | 0.30 s |
| `initial_replay_lookup`, `wire_response`, `service_admission`, `unattributed` | 0.02 s together | 0.02 s together |

Request body 207,558 bytes and response body 1,216,486 bytes in every save. The covers counters: warm saves make about 6,000 `covers` calls with 70,000 `value_equal` calls and spend a median 104 ms (max 138 ms) there; the cold saves 8,664 calls, 101,599 `value_equal` calls and 172 ms. The `covers` copy and compare that was 5.7 s of a warm save in the profile of `c9e535bd` is therefore about 0.1 s now.

## Bursts (edits made faster than a commit takes, overlapped, plain mouse drags)

| Burst | Edits accepted | POSTs | Refusals | Last edit release to Saved (3 repetitions) | Edits in the document | Final state vs expected |
| --- | --- | --- | --- | --- | --- | --- |
| B5, 5 edits within 3 s | 5 of 5 | 5 | 0 | 26.6, 26.2, 30.3 s | 5 of 5 | start 241.3333 s against 241.3062 expected: matches |
| B10, 10 edits within 5 s | 10 of 10 | 10 | 0 | 52.8, 53.7, 53.1 s | 10 of 10 | start 262.1333 s against 262.0833 expected: 0.050 s, exactly the 0.05 s tolerance, reported `false` (all 10 edits present, as in earlier runs) |

As before every edit is its own commit and the commits are processed one after another (about 5.3 s each), so the last edit of a burst is Saved about 27 s (5 edits) and 53 s (10 edits) after it was made, down from about 60 s and 120 s. No refusal, nothing lost.

## Not established

- Why `provider_commit` is 2.6 s warm and 8.3 s cold, and what `port_store_accept` (1.7 s) spends: the timing lines have stage spans only, no profile was taken in this run.
- The instrumentation overhead of the counters and timer (not measured; numbers are labelled instrumented).
- Release-to-POST (about 1.2 s) and 200-to-Saved (about 0.5 s) are client-side times measured in the browser and are not part of the Runtime breakdown.

## Text for the 'Saving a heavy timeline' section of `docs/speed.md`

> **24 November 2026, SV-4 combined on Runtime `eb4e8644` with Agent PR #560 (instrumented):** on the 300-clip fixture a warm save takes about 5.1 s from POST to 200 and 6.8 s from release to Saved (median over 54 saves, maximum 8.0 s); the first save after a Runtime start takes about 10.7 s and 13.0 s. That is half of the previous candidate (10.4 s and 12.5 s), but the gate (2 s median, 4 s maximum) is not met. The Runtime's own per-stage timing accounts for 99.9 % of the POST-to-200 time: warm saves spend 2.6 s in `provider_commit`, 1.7 s in `port_store_accept`, 0.4 s in durable reconciliation and 0.3 s in the handler; the `covers` copy and compare is now 0.1 s. No refusal in any save, burst or first read. Receipts: `plans/77-saving-holds-on-a-heavy-timeline/evidence/2026-11-24-sv4-combined-run/`.
