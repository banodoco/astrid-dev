# r6 tool defects: index (banodoco/astrid-dev unless noted)

| Pri | Defect | Issue | Fix branch / fixer |
|---|---|---|---|
| 1 | One-param edit / nudge / draft edit folds hundreds of unrelated clip rewrites (1.9 MB patch, 354-clip nudge, 1216-clip draft diff) | #1401 (new) | none; X/S fixer |
| 1 | Dry run reported "may or may not have been committed"; advised retry contradicts ("immutable"); 1 MiB Runtime body cap surfaces as Broken pipe; stuck flight cannot be retired | #1246 (2 comments) | none; X fixer (SDK + Runtime) |
| 2 | Asset swap / timing edit on word-anchored clip inside a shot refused ("missing exact word binding") | #1403 (new + comment) | none; X fixer |
| 2 | Imported media cannot be put on an occurrence clip (capture_mismatch, "outside Runtime-verified inputs", handle vs path rules) | #1404 (new) | none; X fixer |
| 2 | Legacy registry entries without generation/variant pin block every rebind; document `check` passes what `publish` refuses | #1405 (new) | none; X fixer |
| 2 | Item-scoped `list.remove` refused by Runtime commit auth ("provider list effect lacks a full collection observation") | #1409 (new) | none; X fixer (Agent+Runtime contract) |
| 3 | One shared outbox per actor+timeline: agents block/replay each other; stale `Timeline.open().head` | #1402 (new + comment) | none; X fixer |
| 4 | `clip.delete` refused whenever `app.astrid.slots` exists | #1406 (new) | none; N fixer (scoped guard) |
| 4 | Project-pack element clips in shots: `ElementPackNotInstalled`, `elements` needs `--realm` and lists parent only, `update-element` parent only, `place-element` no params, `packs list --project` | #1407 (new) | none; X fixer |
| 4 | Project-pack CLI unreachable via run-astrid; default root ignores data root; `validate` passes what `admit` rejects; admit traceback | #1408 (new) | none; N fixer (root default + validate check are small) |
| 4 | `nudge()` reflows 354 clips | in #1401 | |
| 5 | Composed visualize: one stale registry entry fails the whole timeline (#1238); editor's own-object route refused | #1238 (comment) | astrid-agent `release/14/fix-1238-stale-registry-asset`, PR banodoco/astrid-agent#525 (render path) |
| 5 | Composed visualize on an install: "installed registry discovery refuses explicit import or pack roots" (host adds PYTHONPATH/ASTRID_PACKS_PATH) | #748 (comment) | none; X fixer |
| 5 | Render refused | #1253 (not reached, no comment) | |
| 5 | No `?t=`/`?frame=`/seek handle or 1:1 preview; ruler stops ~35 s | #1410 (new) | none; N fixer for `?t=` |
| 5 | Preview vs render: sub-pixel jitter and flickering edge line | #1411 (new) | none; T/X (element + editor) |
| 5 | Videos imported with "size unknown"; preview/render framing differs | #1412 (new) | none; N fixer (reuse ffprobe) |
| 5 | No CLI route to an asset's bytes | not filed: `media open <ref> --materialize --max-bytes 104857600` exists (default cap 10 MiB); help could say so | |
| 5 | No audio excerpt of a timeline range/clip | #1392 (new) | none |
| 5 | `timelines show --json` ignores `--page/--page-size` (JSON itself reports continuation) | #1394 (new) | |
| 5 | `timelines words`, `assets`, `history` lack JSON / head | #1393 (new + comment) | none; N fixer |
| 5 | Editor preview pack load times out at 30 s under load | not filed: message already includes the timeout; low value | |
| 6 | `generate_audio` FAL_KEY not declared | #1254 (existing; not touched) | none |
| 6 | No text-to-SFX mode | #1395 (new) | |
| 6 | No listening/understanding capability on an install | #1396 (new) | |
| 6 | Action failure buries the error under 3 tracebacks | #1397 (new) | |
| 6 | Transient Runtime timeout reported as identity failure + "run the install line again" | #1413 (new) | none; N fixer (small) |
| - | Synced skill hard-codes another install's python | #1234 (existing) | |
| - | No `run-astrid python <script>`; unstamped SDK caller told "An older Astrid is still running" | #1398 (new + comment) | |


## Additional filings (2026-11-22)

| Defect | Issue / comment | Related PR |
|---|---|---|
| Restore removed clips or revert a time range to an earlier revision | [#1430](https://github.com/banodoco/astrid-dev/issues/1430) | #1403, #1404, #1405; astrid-agent#526 |
| Outgoing edit payloads do not distinguish targets from broad assertions | [#1431](https://github.com/banodoco/astrid-dev/issues/1431) | #1409, #1401 |
| Timeline.add footage is hidden beneath overlapping shot media | [#1432](https://github.com/banodoco/astrid-dev/issues/1432) | #1404, #1407 |
| Editor preview pack loading times out under load with misleading recovery state | [#1433](https://github.com/banodoco/astrid-dev/issues/1433) | #1403-#1405 |
| Editor preview playback advances only a few frames in ten seconds under load | [#1434](https://github.com/banodoco/astrid-dev/issues/1434) | #1262, #1268 |
| Editor playback time labels truncate and mis-round centiseconds | [#1435](https://github.com/banodoco/astrid-dev/issues/1435) | #1141 |
| New evidence on #1403 | [comment](https://github.com/banodoco/astrid-dev/issues/1403#issuecomment-7082486028) | astrid-agent#526 |
| New evidence on #1404 | [comment](https://github.com/banodoco/astrid-dev/issues/1404#issuecomment-7082486211) | astrid-agent#526 |
| New evidence on #1407 | [comment](https://github.com/banodoco/astrid-dev/issues/1407#issuecomment-7082486359) | none |
| New evidence on #1401 | [comment](https://github.com/banodoco/astrid-dev/issues/1401#issuecomment-7082486511) | none |
| New evidence on #1413 | [comment](https://github.com/banodoco/astrid-dev/issues/1413#issuecomment-7082486653) | none |
| New evidence on #1262 | [comment](https://github.com/banodoco/astrid-dev/issues/1262#issuecomment-7082486841) | none |
| SDK dry-run diff crashes after Runtime preview success | [#1436](https://github.com/banodoco/astrid-dev/issues/1436) | #1246, #745 |
| New generic media-window validation evidence on #683 | [comment](https://github.com/banodoco/astrid-dev/issues/683#issuecomment-7082499649) | none |


## Render findings (2026-11-22)

| Defect | Issue / comment | Related PR |
|---|---|---|
| Editor preview and render resolve different revisions of the same element pack | [#1469](https://github.com/banodoco/astrid-dev/issues/1469) | #1411, #1412; astrid-agent#530 |
| Bundler cannot resolve collection-pack element imports; pack-root ownership mismatch | [#1470](https://github.com/banodoco/astrid-dev/issues/1470) | #748, #1253; astrid-agent#530 |
| Collection-pack elements cannot import shared rendering contracts by relative path | [#1471](https://github.com/banodoco/astrid-dev/issues/1471) | #748; astrid-agent#530 |
| Long render loses execution lease while Runtime heartbeat is unanswered | [#1472](https://github.com/banodoco/astrid-dev/issues/1472) | #1320; astrid-agent#530 |
| Custody capture failure aborts a live long-running render | [#1473](https://github.com/banodoco/astrid-dev/issues/1473) | #1320; astrid-agent#530 |
| Failed render leaves managed session slot occupied | [#1474](https://github.com/banodoco/astrid-dev/issues/1474) | #1320; astrid-agent#530 |
| Failed render scratch is not reclaimed and blocks admission | [#1475](https://github.com/banodoco/astrid-dev/issues/1475) | astrid-agent#530 |
| Render task failures and frame progress are invisible outside invoking command | [#1476](https://github.com/banodoco/astrid-dev/issues/1476) | #1433, #1434; astrid-agent#530 |
| Render export hint passes unsupported `--to` | [#1477](https://github.com/banodoco/astrid-dev/issues/1477) | astrid-agent#530 |
| New command-worker readiness and empty `ASTRID_PACKS_PATH` evidence on #1253 | [comment](https://github.com/banodoco/astrid-dev/issues/1253#issuecomment-7085505413) | astrid-agent#530 |
| New source-edit identity-message evidence on #759 | [comment](https://github.com/banodoco/astrid-dev/issues/759#issuecomment-7085505572) | astrid-agent#530 |
| Related task execution-lease evidence on #1320 | [comment](https://github.com/banodoco/astrid-dev/issues/1320#issuecomment-7085505714) | #1472; astrid-agent#530 |
| Stopgap branch warning and new issue list on astrid-agent#530 | [PR comment](https://github.com/banodoco/astrid-agent/pull/530#issuecomment-7085513411) | astrid-agent#530 |


## Plan filing follow-up (2026-11-22)

We searched open and closed issues before filing these distinct defects. Proposed Plan 87 keeps the decisions open.

| Defect | Issue | Planned task |
|---|---|---|
| Preview accepts fade with explicit easing; composition render throws | [#1500](https://github.com/banodoco/astrid-dev/issues/1500) | RW-25 |
| Task inventory JSON exceeds 4 MiB | [#1501](https://github.com/banodoco/astrid-dev/issues/1501) | RW-26 |
| Orphaned queued render claimed after restart (reported; stale-work policy unverified) | [#1502](https://github.com/banodoco/astrid-dev/issues/1502) | RW-27 |
| Changed node_modules dependency reported as Remotion not ready until restart | [#1503](https://github.com/banodoco/astrid-dev/issues/1503) | RW-28 |
| Tiny out-of-bounds range rejected only after admission | [#1504](https://github.com/banodoco/astrid-dev/issues/1504) | RW-29 |

The dead-task active count and blocked host slot remain with [#1474](https://github.com/banodoco/astrid-dev/issues/1474) / RW-24: lease expiry is not native stop proof, so recovery must reconcile custody rather than zeroing occupancy. The abrupt heartbeat stoppage augments [#1472](https://github.com/banodoco/astrid-dev/issues/1472), and the excluded pid_for_task retry substage augments [#1473](https://github.com/banodoco/astrid-dev/issues/1473).
