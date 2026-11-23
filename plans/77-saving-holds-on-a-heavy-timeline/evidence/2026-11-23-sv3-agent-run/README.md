# SV-3 (A): Agent capture fix and SV-2f, three repetitions with bursts, 23 November 2026

Approved for exactly: package head `8f1899f28ac1890bac408ae942945a4600a600d8` (branch `release-15/p77-sv3-agent`), `package.sha256` digest `1b2cf43708fc240b5785542037be6c96fa45fbcf3a7fa4bcb3ad31987666989f`, candidate Runtime `c9e535bdd05f1e800dd864b5c91445c69dfacb4f` (tree `629b34db4d77cabd36f09245b9c0972dbbf4dd7f`: `f2da02e1` plus SV-2f and the SV-L1 stage spans; dependency and contract diff against `77c38d03` empty) and Agent `096a2fb3536192785fabd33e6673ba8ab4ef5ead` (astrid-agent PR #560, tree `8765108c2220092ded07399f8e7851fc847730c2`, only `_commit_patch.py` and `_doc_patch.py` overlaid on the retained program). One run, three repetitions, 17:53Z to 18:28Z, exit 0. Idle-safe stop verified in every repetition, ports closed, no leftover Chrome, boundaries unchanged (`cleanup.json`, `boundary.json`: signed backup, owner files and the original `direct-data` listing unchanged). Free disk never below 17.3 GiB (`free-kib.tsv`, stop at 16 GiB). The supervised pack host ran in all three repetitions (`rep-N/pack-host.json`: log grew, no crash line); the Runtime start took about 2.5 minutes each time (148 to 150 s) and is not counted in any save time.

## Overlay identity

The two Agent files were loaded from the candidate by the Runtime daemon in every repetition (`rep-N/agent-loaded.json`, `failures: []`): `_commit_patch.py` sha256 `2bcde680...`, `_doc_patch.py` sha256 `f063ebcd...`; the rest of `astrid.sdk.timeline` (including `commit.py`) still came from the installed site-packages. Before the run the installed files were byte-identical to the base blobs (`a3a7277a...`, `15cc7504...`); after the run they are unchanged (`agent-overlay.json`: `installed_unchanged: true`). Other processes (pack host, chat) keep the installed SDK.

## Plain summary

**Warm saves are about twice as fast as before; the gate is still not met.** Release-to-Saved (`summary.tsv`, per save in `summary-per-save.tsv`):

| Scenario | Saves | Median | Max |
| --- | --- | --- | --- |
| Cold first save after Runtime start | 3 | 20.7 s | 20.9 s |
| S1 one edit alone (warm) | 3 | 12.7 s | 17.7 s |
| S2 two edits, one after the other | 6 | 12.2 s | 19.6 s |
| S3 ten edits, one after the other | 30 | 12.4 s | 20.9 s |
| S4 five drags, each waited to Saved | 15 | 12.5 s | 20.4 s |
| All 54 warm saves | 54 | 12.5 s | 20.9 s |

Warm POST-to-200 is about 10.4 s (it was about 20 s on `f2da02e1`), the cold POST-to-200 about 18 s (22 to 30 s before), release-to-POST 1.0 to 2.3 s and 200-to-Saved 0.6 to 0.8 s. The gate (median 2 s, none over 4 s) is not met. The cold first save is the slowest: 19.9, 20.7 and 20.9 s. **No refusal in any of the 57 single saves or 45 burst saves**: every commit POST answered HTTP 200 and the badge reached Saved; no `head_busy`; the driver's exact-CAS post-condition (fixed in this package) passed on every save. S0 (the verified-head read right after the cold start): status 200 in all three repetitions; the editor was writable after 31.6, 18.2 and 12.2 s (the verified-head request itself took 10.3, 7.7 and 2.6 s), so the first repetition after a cold start is the slow one.

## Bursts (edits made faster than one commit takes, overlapped, plain mouse drags that bypass the tape)

| Burst | Edits made | Commit POSTs | Statuses | Last edit release to Saved (3 repetitions) | Edits in the document | Final state vs expected |
| --- | --- | --- | --- | --- | --- | --- |
| B5, 5 edits within 3 s | 5 of 5 accepted by the editor | 5 | all 200 | 63.3, 59.8, 62.4 s | 5 of 5 | start 241.3333 s against 241.3062 expected: matches |
| B10, 10 edits within 5 s | 10 of 10 accepted by the editor | 10 | all 200 | 120.3, 120.4, 116.6 s | 10 of 10 | start 262.1333 s against 262.0833 expected (0.050 s, exactly the 0.05 s tolerance, reported `false`; 10 edits present) |

The editor did **not** coalesce: every edit became its own commit POST, and the commits were then processed one after another, so the Saved badge arrived about 12 s after the previous edit's commit started: 60 s after the last of 5 edits and 2 minutes after the last of 10. In B10 repetitions 1 and 2 the driver's bounded 120 s settle wait timed out (`settle_error: TimeoutError`) although all 10 POSTs had returned 200 and the badge was Saved when it was read. Nothing was refused and no edit was lost in these three bursts of each size.

## Not available from this run

- **The per-stage timing lines of the candidate (`runtime.timeline_commit.timing`) never reached the captured Runtime log.** `runtime-log-delta.txt` of every repetition has only startup lines, and the stack's `runtime.log` has no `timeline_commit_timing` line either (`rep-N/commit-timing-summary.json`: `posts: 34`, `lines: 0`), so the per-stage breakdown for one cold and one warm save and the `exclusive_sum / POST-to-200` percentage (columns present but empty in `summary-per-save.tsv`) could not be produced. The code emits the line at INFO with `_LOGGER.info` in `timeline_commit_execution.py`; why no INFO line from the daemon reaches `runtime.log` is not established here (the daemon's `start` mode may not install the INFO handler that `_foreground_logging` installs).
- The Agent authoring commit was not measured (`agent-commit.txt`: not established).
- The sampler was not attached in this run.

## Text for the 'Saving a heavy timeline' section of `docs/speed.md` (not on `main` yet)

> **23 November 2026, SV-3 (A) on Runtime `c9e535bd` with Agent PR #560:** on the 300-clip fixture a warm save takes about 10.4 s from POST to 200 and 12.5 s from release to Saved (median over 54 saves, maximum 20.9 s); the first save after a Runtime start takes about 18 s and 20.7 s. This is about twice as fast as the 20 s of `f2da02e1`, but the gate (2 s median, 4 s maximum) is not met. Edits made faster than a commit takes are not coalesced: 5 edits in 3 s make 5 commits and the last is Saved about 60 s after the last edit, 10 edits in 5 s make 10 commits and the last is Saved about 2 minutes later; none was refused and all were applied. Receipts: `plans/77-saving-holds-on-a-heavy-timeline/evidence/2026-11-23-sv3-agent-run/`.
