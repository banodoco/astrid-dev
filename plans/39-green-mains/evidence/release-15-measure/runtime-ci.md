# astrid-runtime CI on release/15/main: why it is red (read-only analysis, 2026-11-24)

Latest run 45259255785 (CI, push, 24e2c929, 23 Nov 20:25Z): failure. Agent pin `tests/astrid-agent.pin` = 0e1543e0 (12 Nov), unchanged since e7e7d52 (16 Nov).
Logs: logs/*.log (raw), clusters.md + failing-ids.tsv (run 45259255785, all 5 failing jobs), out_nightly/, out_mainunit/ (main).

## Workflows on release/15/main (only two)
- CI (ci.yml): triggers push [main, release/*/main, int/**, release/14/plan-39], pull_request, workflow_dispatch(agent_sha). Concurrency group per workflow+PR/ref; cancel-in-progress false on main and release/*/main.
- Nightly (nightly.yml): schedule `0 3 * * *`, push [release/14/plan-39], dispatch. Job `integration`: `pytest -q -rA --junitxml -m integration`. Schedules only fire from the default branch (main); release/15/main's copy never runs on cron.
- main also has diag-darwin-custody, failure-ceiling, ls7-packet workflows; not on release/15/main.

CI jobs / pytest command: windows-realm-publication (`pytest -q -rP -m ""` test_windows_runtime_launch + other pytest -q steps, Agent ff40f2c6 shallow), unit [ubuntu, macos] (`pytest -q -rA --junitxml -n 2`, full Agent pin checkout via `git fetch`, `pip install -e` Agent), darwin-native (`pytest -q -m darwin_native`, Agent 4866090e hard-coded), typescript-client (npm test), boundary (`pytest -q tests/test_second_client_e2e.py -m ""`), sandbox-process-control (`sh tests/seccomp/run-suite.sh -rA --junitxml` = whole suite in a container), portability-lifecycle [ubuntu, macos] (`-rA --junitxml -m ""` on a file list; Agent via actions/checkout), landing-reference (PR only).
Per-test lines (-rA) and JUnit artifacts (90-day) now exist; a "Summarize test result XML" step prints tests/failures/errors/skipped.

## Job inventory, run 45259255785 (all counts from pytest summary lines in logs)
| job | concl | failed | errors | passed | skipped | note |
|---|---|---|---|---|---|---|
| unit ubuntu | failure | 111 | 367 | 9348 | 26 | 12m26 |
| unit macos | failure | 110 | 367 | 9245 | 130 | 23m |
| sandbox-process-control | failure | 125 | 371 | 9254 | 26 | whole suite in container |
| portability ubuntu | failure | 7 | 0 | 610 | 45 | |
| portability macos | failure | 8 | 0 | 595 | 59 | |
| darwin-native, typescript-client, boundary, windows-realm-publication | success | | | | | |
| landing reference | skipped | | | | | PR-only |
NO-RESULT jobs in this run: none (all jobs produced counts/XML). Earlier cancelled runs on release/15/main: 45014120874, 44981470520, 44978086185 (22 Nov; reason not determined).
Flips: runs 45158253276, 45146039810 (and 5 more since 06:02 on 23 Nov) show identical counts (111F/367E ubuntu, 110/367 mac, 7/8 portability). No job flipped; failures are deterministic. main CI 22 Nov (45028831485, 5120462d) unit ubuntu: 111F/367E, same set. So release/15 inherited main's red; no release/15-specific regression.

## Failing ids (run 45259255785)
Distinct failing ids across 5 failing jobs: 508 (ubuntu unit 479, mac unit 478, sandbox 497, portability 7/8). 474 are common to ubuntu+mac unit. Sandbox adds 18 container-only (pidfd/custody: test_real_bootstrap 10, test_linux_runtime_boundary_native 4, test_linux_listener 2, test_process_control 2...). Ubuntu-only 5 (test_bootstrap StaleOwnerTests); mac-only 4 (test_v33_protected_acceptance R0_ROLLBACK x3, test_profile_services node env).

## Causes by cluster (unit ubuntu, 479 ids)
| # | ids | raise site / first product frame | what | class | files |
|---|---:|---|---|---|---|
| C1 | 232 | runtime_protocol/v33_lifecycle.py:300 require_ready via service.py:999 _assert_mutation_admitted | precut-v31 fixture realm is migrated (leaves `.v33-activation.json` not "ready"); tests that open it with no Timeline provider ("neutral"/service/http params) are fenced. "astrid" param (provider registered) passes. | stale tests vs product fence (fence added c0043f6, 1 Nov; tests last edited 28 Oct) | tests/test_timeline_effect_authority.py (106), test_timeline_document_authority.py (62), test_timeline_reference_authority.py (38), test_project_reference_catalog.py (13), test_realm_admission_hardening.py |
| C2 | 126 | runtime_protocol/daemon.py:320 | same marker; RuntimeDaemon starts with provider None (`_load_installed_timeline_commit_provider` returns none for default authoring_profile) -> "migrated realm requires fresh Timeline provider registration" | same root as C1 | test_timeline_effect_authority.py[http] (106), test_timeline_authority_door.py, test_timeline_shot_authority.py, test_streaming_media_io.py |
| C3 | 28 | tests/test_timeline_inverse_sequential_authority.py:30 | after inverse/restore to empty, `config.tracks` is [V1,A1 default tracks], test expects [] | Agent behaviour vs stale expectation (not verified which side) | that file; also test_timeline_forward_created_authority.py (C7, 8), test_timeline_legacy_authority |
| C4 | 20 | test_timeline_render_publication.py:187 | `import astrid.packs.video_editing...` ModuleNotFoundError | Agent pin 0e1543e0 has no video_editing pack (verified: git ls-tree; no history for that path in Agent) -> env/pin wiring or stale test | test_timeline_render_publication_authority.py (17), test_timeline_render_publication.py (3) |
| C5 | 12 | astrid-agent astrid/sdk/timeline_address.py:520 ElementPackNotInstalled "image" | element `image` needs an installed pack (docs: "not installed by default") | env wiring (packs not installed in CI) | tests/test_timeline_native_asset_union.py |
| C6 | 10 | astrid/sdk/timeline/_recording.py:175 CommandError "created identity is occupied" | Agent/Runtime contract mismatch (not investigated) | possible product/Agent bug | test_timeline_commit_sequential_verifier.py |
| C8 | 12(sbx) | astrid_runtime/custody_broker.py:1864 "Linux pidfd custody is unavailable" | sandbox container lacks pidfd | CI wiring (container caps), sandbox job only | test_real_bootstrap, test_linux_runtime_boundary_native |
| rest | ~40 | 40+ singletons/pairs (bootstrap stale-owner, diagnostics, portable lifecycle, hard-coded path, backup integrity) | individually small | mixed | see clusters.md |
C1+C2 = 358/479 = 75% of ubuntu failures; with C3, C4, C5, C6, C7 = ~90%.
Portability (7): `No module named 'astrid'` from stage1 venv built in tests/conftest.py:146 (contains Runtime + client only, no Agent) for test_portable_lifecycle (5) and test_profile_services installed_run/up (2). Test-fixture wiring.

## R-a / R-b / R-c status
- R-a (no Agent checkout): GONE. Every job checks out the pin (unit logs: "Agent: 0e1543e0...").
- R-b (hard-coded scratch path): STILL PRESENT but small. tests/test_p2_commit_phase_capture.py:62 `work/app/scripts/testing/sitecustomize.py` (3 ids, unit+sandbox); tests/test_wc10_installed_launcher.py:26 `/home/user/work/wt/agt-pin-6efc8150` (nightly, 1 id). Verified in code.
- R-c (git archive on shallow checkout): GONE in CI jobs (0 occurrences). In Nightly it is 20 ids, but cause is different: tests/test_snapshot_legacy_certification.py:37 archives Agent 321cef4b which GitHub says "not our ref" (not fetchable at all), so even fetch-depth 0 will not help. Verified in nightly log line 3519.
Share of current ubuntu failures: R-b 3/479 (<1%), R-a/R-c 0.

## Nightly
Schedule only runs from main. Last 15 main Nightly runs (12-23 Nov) all failure. Latest 45166036353 (23 Nov, 5120462d): 124 failed, 28 errors, 499 passed, 20 skipped, 9748 deselected (-m integration), 152 distinct ids. Top: test_timeline_commit_crash 21 (assertion at :78; plus 5 v33 fence), test_snapshot_legacy_certification 20 (unfetchable Agent SHA), test_timeline_history_assembly 23 (DID NOT RAISE), restore/input integration 9, runtime_boundary 6 ("process control is already strict", test isolation), wc10 launcher 1 (R-b). release/15/main nightly.yml has never fired from cron there; dispatch is the only way.

## Agent / pins
tests/astrid-agent.pin = 0e1543e0da22 (Agent merge of r12 fix-round, 12 Nov). Agent main is 959da732 (15 Nov), Agent release/15/main 514499de (24 Nov); pin is older than both. CI: `Select pinned Agent revision` (dispatch input agent_sha overrides) -> git init + `fetch --no-tags origin SHA` -> `pip install -e $ASTRID_CHECKOUT` (unit, sandbox), tests/astrid_checkout.py fails (not skip) without ASTRID_CHECKOUT. Other hard-coded Agent SHAs: windows ff40f2c6, darwin-native 4866090e, nightly historical 321cef4b (unfetchable). No packs are installed in any job.

## Verified vs inferred
Verified by reading code at cited lines: C1 (v33_lifecycle.py:296-300, service.py:999 trace), C2 (daemon.py:289-320), C3 test line + log diff, C4 (import at test :187; pack absent in pin tree), C5 (timeline_address.py:495-525), R-b lines, portability venv (conftest.py:146-200), CI yml. Inferred from logs only: why precut fixtures leave the marker un-"ready" for neutral (upgrade.py migrate_canonical_to_current path partly read), C3 direction (Agent vs test), C6, C7, bootstrap/custody clusters, sandbox-only 18.
Unknown: whether bumping pin to Agent release/15/main fixes C3-C7 (needs a dispatch with agent_sha; I did not dispatch); whether C1/C2 ever passed (last test edits predate fence by 4 days, no green run in last 15 on either branch); why 22 Nov runs were cancelled.

## Effort (worker-days, rough)
C1+C2 (358 ids, one root): 1.5-3 (make precut fixture helper finish activation/register provider or mark migrated fixture ready, or a test-only provider; broad but mechanical). C3/C7/C34-35 (~45): 1-2 after deciding Agent vs test; C4 (20): 0.5-1 (pack install in CI or rewrite to core contract); C5 (12): 0.5 (install/declare pack); C6 (10): 1 investigate; portability (7): 0.5 (add Agent to stage venv or PYTHONPATH); sandbox pidfd (18): 1 (container caps); R-b: 0.25; bootstrap/other singletons (~40): 2-3; Nightly (152 ids): 3+ incl. unfetchable SHA decision. Total roughly 10-15 worker-days for green CI, ~3-5 for CI to drop below 100 failures.
