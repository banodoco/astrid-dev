# SV-2a one-save diagnostic, second attempt: safe stop at the trace witness, 23 November 2026

The save session approved the corrected package for one attempt: astrid-dev PR #1668 head `ed8c78836cfa99c5246a95040e983796faf7c0a1`, `package.sha256` digest `7af181bdb5d58c150236105df1f8afc313d68acd49b6fd36cc4ecc0179b23cda`, diagnostic Runtime `5c70a11765ffee3d54652e66f998c3a0bd9493f0`. It ran once on the lane box from 14:44Z (host clock) with the signed backup named in `SV2A_SIGNED_BACKUP`. **No save happened: `browser-sv2a-first-save.json` records `phase: trace_witness`, `error_kind: AssertionError`, `timeline_commit_posts: 0`.** The attempt is spent and is not retried. The [first attempt](../2026-11-23-sv2a-run/README.md) stopped earlier at the preview check, which this package removed.

## What happened

- Setup now passed everything the first attempt could not reach: the candidate Runtime started from the archived source (`candidate-daemon-module.json`, `up.json`), the preflight witness agreed (`browser-preflight.json`), the preview answered the health and instance-id check, and the browser driver started (`browser-sv2a-first-save.json`).
- The driver issued the one authenticated history GET. The trace contains it as request scope 13 with route `timeline_history_get`, and no `timeline_commit_post` scope (`timeline-memo-trace.jsonl`).
- The driver then stopped on its own trace check at `browser-sv2a-first-save.mjs:410`, `assert.equal(item.unknown, false)`. The check requires every trace envelope to have `unknown: false`. 27 of the 29 envelopes have `unknown: true`: the flag turns on after the startup `memo_invalidation_detected` event whose version sample is `version_sample_unavailable`, and every later envelope carries it. So the witness check is stricter than the trace's real behaviour; it did not catch a fault at the save. The run stopped before navigation and before any write, as designed.
- Cleanup worked (`cleanup.json`): idle-safe stop verified (`down.json`), preview and proxy ports closed (`preview-after.json`), no leftover Chrome, browser temp removed, **boundaries unchanged** (`boundary.json`; the data-root and root listings gained new top-level entries only). Free disk never went below 18.1 GiB (`free-kib.tsv`, stop at 16 GiB). `exit_code: 1` in `cleanup.json` is the driver's stop. `privacy-scan.tsv` hits are the `name@runpod-snapshot.json` file names in the two program hash lists, as before.

## What the trace shows (`timeline-memo-trace.jsonl`, 29 envelopes)

1. `trace_runtime_source` with the archived module path and the live PID.
2. At Runtime start, two memo clears with `proofs_before: 0` (generation 1 at `clear_replay_memo`, `timeline_commit_store.py:407`; generation 2 after `memo_invalidation_detected` at `_sync_replay_memo`, `:722`, reason `store_version_changed`, version sample `version_sample_unavailable`). Both discard an empty memo. Only `BEGIN` and `ROLLBACK` read transactions appear (12 statement attempts); no write transaction.
3. 25 request scopes: 24 `other_http_route` and one `timeline_history_get` (request 13). **The history read cleared nothing and invalidated nothing.** Nothing in the trace after startup touches the memo.

So the run answers the narrower question: the only memo clears before the save are the two startup clears of an empty memo, triggered by an unavailable store-version sample at the first read, not by a database write. Which write clears a populated memo before the first save was not observed, because the run stopped before the save.
