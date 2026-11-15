# Release 13 journey evidence on the published tuple

Published tuple (live 20:54 UTC, 15 Nov): agent `9814193a73f606719e81883a8be197d27dd361d4` (agent main `959da732`, merge of PR 347), App `7297d266564997c460a051a7eeb63a9f1ae2278c` (App main `d7d48cfe`, merge of PR 268), Runtime `6855dfa8df65cf8ae4c002b57134d6505493c17c`, manifest sha256 `29dc13cf7c8d9e7553b4fb8a3f357199bfc80885e55775c6aea6a91e0a163483`, public artifacts `public/install` `c268a5fa…`, `install.sh` `591c4c51…`, `install.ps1` `ea581d5d…` (unchanged from the earlier candidates).

Harness: branch `harness/33-win-r12-update` `ea5c0bff6` (built on the capture harness `harness/32-r13-capture` `b46560b8`, on the R13 harness `harness/31-r13-upgrade` `60bf5056`). The matrix is 14 rows: the 13 earlier rows plus `direct-windows-r12-update`.

## Gate runs on the published tuple

| Run | Result |
|---|---|
| Journey 43757304537 (`row=direct`, 14 rows) | success; all 14 rows green; "Journey evidence (exact tuple)" passed |
| Capture row 43757315244 (`direct-linux-fresh`) | success |
| Capture row 43757326484 (`direct-linux-fresh`) | pending at publish |
| CI 43757233210 `fast checks` | success: Ruff baseline, mypy baseline, import cycles and collection errors all ran and passed |
| App PR 268 head `7297d266` (W218) | clean by name: no check that passes on App main fails on the head; `release-guard` ran and passed on the merge ref; `three-products` 14 passed in one attempt |
| Network policy (W217 on `8625a463`, W227 delta on `ff9da5d8`, re-verified on `9814193a`) | pass |

## The new gate row

`direct-windows-r12-update` (windows-2022, powershell.exe, leg `release12-then-update`): installs the pinned published Release 12 (`install.ps1` blob at App commit `ae4da5d7`) as a plain install, starts it, seeds a project and a marker, runs the candidate's `install.ps1 --update`, then checks the release (13), the frozen candidate's agent and runtime commits, health, one live Runtime, Task Scheduler ownership, `astrid doctor`, a dry-run generate (no task, provider or GPU) and that the seeded data survived. First real run: 43756097648 on the `36f04678` tuple, pass; on the published tuple: 43757304537, pass.

## What the earlier candidates taught us

- `direct-linux-fresh`: the page's "Astrid updated: Release N → Release M" line (an 8-second transient) was missed in 3 of 4 earlier runs; the capture runs showed the tab received the new Runtime instance and stored release 14 and the final Settings state was correct (the App renders the line only transiently; the journey asserts it). On the published tuple it passed. Deferred row: assert a persistent state and fix the App display defect in 13.1.
- `direct-macos-fresh`: one failure in 8 samples at the final uninstall ("launchd service did not remain stopped"), caused by a Runtime shutdown race that is byte-identical in R12's Runtime (W224, W225). Deferred, Runtime lane.
- Agent `36f04678` and `ff9da5d8` were not published: `fast checks` failed the mypy baseline gate (Windows-only attributes unresolved on Linux); fixed in `29ca1469`.
- Agent `8e8e60b1` was not published: its rebuilt `socketpair` wrapper broke `socket.socketpair()` and `asyncio.new_event_loop()` on Linux and macOS (default `family=AF_INET`); fixed in the next batch.
