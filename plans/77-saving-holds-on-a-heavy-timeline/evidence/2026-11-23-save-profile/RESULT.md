# Two profiled saves on the signed 300-clip fixture

The exact compiled App confirmed two same-page saves in **57.498 s** and **19.712 s**. Each sent one compare-and-swap commit, got HTTP 200, showed Saved, and passed an independent public revision, publication, and one-clip diff check. The same `fixture-video-0190` on `V6` moved right twice through free space, from 187.2000 to 189.3000 to 191.3667 seconds. Each head had 300 clips and ten occurrences. There was no navigation, restart, or Undo between the saves. This is one instrumented pair, so it does not establish stock speed, a repeat distribution, or the 616-clip save target.

Exact installed trial source was App `148eaf381e3f02dc0f0d5dfc61e61ebf37dbc715`, Agent `5e301956dc49c8b9ba4d23a7ce96c6564bd74d2f`, Runtime `77c38d037f98f744bd8f41c15d95429c124a8003`. It used the verified compiled App inventory and signed v30 SQLite source SHA-256 `c0b27bb02c33d5b1e72699749c07adc769dda0c0eb2ceaceab222b630c6e132d`. Adoption materialized the correct selected realm, then reported the expected transport timeout. An independent health check and idle-safe stop preceded the instrumented direct restart, which returned in about 147 s.

| Save | Release → POST | POST → 200 | 200 → Saved | Release → Saved | py-spy samples / errors |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 1.238 s | 55.524 s | 0.736 s | 57.498 s | 68,426 / 2 |
| 2 | 1.263 s | 17.733 s | 0.716 s | 19.712 s | 18,988 / 0 |

## Runtime HTTP request thread

Each attached `py-spy` 0.4.1 at 100 Hz with `--threads --idle`, Python frames, default blocking mode, before pointerdown through scoped HTTP 200. Both raw files parsed and contain one qualifying commit request thread. The sums cover 100% of the sampled weight in that thread. With `--idle` this is weighted sampled time, not thread or process CPU time. The separate Runtime process CPU deltas across the sampler scopes were 48.02 and 15.93 s. The installed Agent provider/schema/SDK validation frames were sampled in those Runtime threads, so no separate Agent process profile was needed for these requests.

| Save | Old-history verification | This edit's validation | Durable-write frames | Other | Selected thread total / commit-active |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 38.130 s | 5.970 s | 0.160 s | 10.420 s | 54.680 / 54.640 s |
| 2 | 3.640 s | 3.880 s | 0.120 s | 9.830 s | 17.470 / 17.380 s |

Old history includes `_history_chain`, `_verify_accepted_replay`, and the `_check_context` history read. Other includes 0.040 / 0.090 s outside commit frames on the same thread and substantial Python record copying. The durable-write bucket counts only stacks under the named write paths. The transaction contains additional verification and processing. The 34.490 s decline in old-history sampled weight accounts for most of the 37.791 s decline in observed POST time in this pair. The second save still spent nearly ten sampled seconds outside the three specifically named groups.

| Rank | Save 1 frame | Seconds | Save 2 frame | Seconds |
| ---: | --- | ---: | --- | ---: |
| 1 | `iterencode` (`encoder.py:258`) | 6.00 | `value_equal` (`timeline_commit_producer.py:67`) | 1.26 |
| 2 | `check` (`timeline_commit_store.py:344`) | 2.03 | `_deepcopy_dict` (`copy.py:231`) | 1.16 |
| 3 | `is_type` (`_types.py:116`) | 1.77 | `value_equal` (`timeline_commit_producer.py:69`) | 0.95 |
| 4 | `digest` (`timeline_commit_validation.py:96`) | 1.71 | `<genexpr>` (`timeline_commit_producer.py:67`) | 0.88 |
| 5 | `value_equal` (`timeline_commit_producer.py:67`) | 1.42 | `<genexpr>` (`timeline_commit_producer.py:69`) | 0.81 |
| 6 | `raw_decode` (`decoder.py:353`) | 1.35 | `deepcopy` (`copy.py:138`) | 0.74 |
| 7 | `_deepcopy_dict` (`copy.py:231`) | 1.33 | `deepcopy` (`copy.py:146`) | 0.68 |
| 8 | `type` (`_keywords.py:285`) | 1.27 | `_deepcopy_dict` (`copy.py:230`) | 0.67 |
| 9 | `_read` (`timeline_commit_store.py:288`) | 1.15 | `value_equal` (`timeline_commit_producer.py:62`) | 0.67 |
| 10 | `<genexpr>` (`timeline_commit_producer.py:67`) | 1.15 | `deepcopy` (`copy.py:144`) | 0.62 |

## Replay proof and stage receipts

- Save 1 (`bc0858a046ccaf08bdcbbdd224e5cb0a`) did seven accepted-record checks, three history-chain calls and three semantic replays. `_sync_replay_memo` cleared at line 686 twice, with `total_changes` and tracked file observations changed both times. The first clear had zero cached proofs after a pre-POST `_error` clear. The second discarded one proof. The append rebuilt one proof and completed at generation 5. The version-field observations explain the clear, but do not identify a particular upstream writer.
- Save 2 (`cf89ca37f3944c6f080f75a991c29b26`) also did seven accepted-record checks, with one history-chain call and one semantic replay. It stayed at generation 5, with two proofs at entry to and after acceptance and no observed clear between the saves. The nine intervening scoped HTTP 200 reads included the harness's public postflight and ordinary timeline, revision and listing routes. Their endpoint records are retained. The only emitted verified-head counter line recorded one selected-record cache hit and zero selected-record verification, reads, retries or replay-key hits. This aggregate is separate from the request-matched memo observations.
- The product's per-stage INFO records are **missing** from the captured sinks. The startup probe confirmed the explicit INFO level and the request hook witnessed both `CommitTiming.emit` entries. The Runtime log, controller, and saved stderr had no accepted commit timing line, so `commit-stage-timings.jsonl` is empty. The stage durations below use the separately captured acceptance boundaries and browser POST/200 timestamps on the same host. They cannot supply the official per-stage splits.

| Save | Browser POST → accept context entry | Accept entry → committed | Commit → browser 200 |
| --- | ---: | ---: | ---: |
| 1 | 46.568 s | 5.736 s | 3.220 s |
| 2 | 9.271 s | 5.324 s | 3.138 s |

## Custody

The one authorized retry ran 11:49:29.819–12:09:20.393 UTC on 23 November 2026. Disk started at 25.220 GiB, bottomed at 19.567 GiB, and ended at 19.968 GiB. The 16 GiB stop guard stayed active. The other local timing job was paused and its exact three processes resumed. Exit 0 and `cleanup.json` prove the preview closed, the fresh browser profile was removed, and ports 2400, 17500 and 17501 refused. `direct-down.json` records `stopped` and `idle.safe=true`.

The copied fixture and installed stack are retained stopped under `wt/astrid-app-p77-quick-indicator.env/quick-indicator/baseline/large/round7-candidate-two-save-profile-20261123-retry/stack`. Its sandbox holds both accepted edits. The original signed fixture is preserved separately. No additional startup, edit, or measurement is authorized by this handoff.

- Save 1 raw SHA-256 `9b35de4d36b05c937825242c19866ad3aa0ea529bec4b6a60601040b75ac490b`
- Save 2 raw SHA-256 `3aa216d4b1580e96db28f3866c40d7258112f616844bf82ddf0e8ddee77e8658`
- Raw originals, scope and sampler receipts, browser/public proof, memo events, and sample attribution are adjacent. `SHA256SUMS` includes them and the controller receipts. The first attempt's independent disk-stop report is in `../candidate-two-save-profile-20261123/RESULT.md`.
