# SV-2a one-save diagnostic: safe stop before the save, 23 November 2026

The save session approved one attempt of the SV-2a package (astrid-dev PR #1668 head `033f1aac3f1dd02fe9ab64f4bb951f7fc29f532a`, `package.sha256` digest `0e3c506bb615edfab61a78259fb66a3215d33ad4da171a4a5cac34c6b08f1dd2`, diagnostic Runtime `5c70a11765ffee3d54652e66f998c3a0bd9493f0`, tree `5c6b2e47b12b4c799a2e362f5d939da513f70864`). It ran once on the lane box from 14:34:46Z to 14:37:33Z (host clock). **No save happened and no history GET was issued.** The attempt is spent; per the approval conditions it is not retried.

## What happened

- The candidate Runtime started from the archived diagnostic source under the retained interpreter (`candidate-daemon-module.json`, `up.json`). The module proofs, the source profile and the catalog agreed and the dependency and contract diff against the retained Runtime `77c38d03` was empty (`dependency-and-contract.diff`, 0 bytes).
- The script then stopped in the new `preview-before` step of `verify-overlay.py` (line 262) with `ValueError: port 2400 is not owned solely by the preview process group` (see `run-driver.log`). The App preview leader is `node scripts/dev-local-workspace.mjs --preview`, whose process group the check requires; the port-2400 listener is the `vite preview` child that npm starts, and its process group did not equal the leader's. The check is therefore stricter than the real process layout. This is a defect of the new B3 check, which had not been exercised on a live stack. It is not a Runtime finding.
- Cleanup worked as designed (`cleanup.json`): idle-safe stop verified, preview group empty (`preview-after.json`), no leftover Chrome, browser temp removed, **boundaries unchanged** (`boundary.json`; the one-level data-root and root listings gained new top-level entries only, recorded in `boundary-*.new-entries.txt`). The `one-root.lock` was opened for writing as noted (`size 0`, mtime changed). Free disk never went below 18.2 GiB (`free-kib.tsv`, stop at 16 GiB).
- `privacy-scan.tsv` was written by the script. A scan of this directory for email, token, key and `~/.codex` text found only file names of the form `name@runpod-snapshot.json` in the two program hash lists, which are not emails.

## What the trace shows before the stop (`timeline-memo-trace.jsonl`, 62 events, no overflow or unknown envelope)

1. `trace_runtime_source` with the archived module path and the live PID (the flush witness works at construction).
2. At Runtime start, **two memo clears with `proofs_before: 0`**: generation 1 at `clear_replay_memo` (`timeline_commit_store.py:407`), then `memo_invalidation_detected` at `_sync_replay_memo` (`:722`) with `reason: store_version_changed` and the version sample `version_sample_unavailable` (`unknown: true`), then a clear to generation 2. No write transaction appears: the trace has only `BEGIN`/`ROLLBACK` read transactions (`_read_transaction`, lines 548 and 560) and 22 `other_http_route` request scopes (health and discovery), no `timeline_history_get` and no `timeline_commit_post`. Both clears discard an empty memo, so they say nothing yet about the writer that cleared a populated proof before the first save in the earlier profile.
3. So this run answers one question only: at startup the first replay-memo clear is triggered by an unavailable store-version sample, not by a database write. The earlier profile's clears (`total_changes` and tracked-file observations changed) are not reproduced here because the run stopped before the history read.

## Next step (for the save session)

A new attempt needs a fixed package and a new approval. The fix is to relax the B3 listener check from "process group equals the leader's" to "the listener's process is a descendant of the preview leader (by parent chain) or shares its session", keeping the exact command-line and port assertions and the after-stop empty-group assertion. That change alters `verify-overlay.py` and so the package digest.
