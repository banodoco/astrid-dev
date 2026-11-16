# Agent merged-head qualification — live attempt-1 checkpoint (2026-11-16)

**Status: INCOMPLETE; not G1/G2/RS1 acceptance.** This is an additive post-PR369 observation, **not** an amendment of the frozen 17:26 UTC G1 baseline. No external run was cancelled/retried and no release-main/public-main branch was written.

**Exact source:** Agent [PR369](https://github.com/banodoco/astrid-agent/pull/369) merged only into `release/14/plan-39` at commit `6bbda788c1a62abcdda242f85c7a1cae86c57d3d`; exact reviewed tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`. [CI run 43967861168](https://github.com/banodoco/astrid-agent/actions/runs/43967861168), [Lanes run 43967861160](https://github.com/banodoco/astrid-agent/actions/runs/43967861160), both **attempt 1**. Artifact metadata explicitly states that same head SHA. Only finished jobs below were measured. No full-run result yet.

## Finished jobs and summaries

| Workflow / job ID | Observed result | Exact outer pytest summary / XML |
|---|---|---|
| CI darwin native [133651924059](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924059) | failed | `14 failed, 40 passed, 30933 deselected, 2 warnings, 1 error in 437.15s (0:07:17)`; `darwin-native.xml: tests=55 failures=14 errors=1 skipped=0` |
| CI unit shard 8 [133651924880](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924880) | failed | `94 failed, 3668 passed, 23 skipped, 27722 deselected, 5 warnings, 2 errors, 202 subtests passed in 1638.02s (0:27:18)`; `unit-shard.xml: tests=3989 failures=94 errors=2 skipped=23` (testcase count 3787; aggregate subtests are not independent testcase IDs) |
| CI fast checks [133651924367](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924367) | success | no failing pytest summary |
| CI boundary [133651924355](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924355) | success | no failing pytest summary |
| CI windows-native-and-installer [133651924610](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924610) | success | XML artifact present; not separately reconciled at this checkpoint |
| CI release wheel Python 3.11 [133651924573](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924573) | success | no failing pytest summary |
| CI release wheel Python 3.12 [133651924395](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924395) | success | no failing pytest summary |
| Lanes opt-in [133651923592](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/job/133651923592) | failed | `12 failed, 19 passed, 30959 deselected, 2 warnings in 189.62s (0:03:09)`; no `test-results-opt-in` XML artifact in first-page run inventory; raw log is available |
| Lanes integration 1 [133651923670](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/job/133651923670) | failed | `37 failed, 479 passed, 31868 deselected, 13 warnings in 1095.70s (0:18:15)`; `integration.xml: tests=516 failures=37 errors=0 skipped=0` |
| Lanes integration 2 [133651924063](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/job/133651924063) | failed | `77 failed, 267 passed, 31868 deselected, 22 warnings, 172 errors in 1870.91s (0:31:10)`; `integration.xml: tests=516 failures=77 errors=172 skipped=0` |
| Lanes installed wheel [133651923640](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/job/133651923640) | success | wheel receipt present |

CI unit shards 1–7 and Lanes integration shards 3–4 were in progress at the last read, not counted as complete. CI landing reference was skipped by design. This is a **point-in-time** snapshot, not a prediction about the jobs.

## Retrieved real XML artifacts, SHA-256 and exact-ID comparison

The hash in each line is the SHA-256 of the **actual downloaded ZIP bytes**, matching GitHub's declared digest; XML hashes are uncompressed bytes, verified separately. Comparison is on `(classname, name)` per testcase in corresponding jobs. Do not classify absent old IDs as new regression.

| New job | ZIP artifact ID, ZIP SHA-256 | Inner XML SHA-256 | Against prior-plan XML (attempt 1) |
|---|---|---|---|
| Darwin | [14277714424](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14277714424) `06a2bac5da6c594ded3ca0f5dec3f0237fc6d02bff165cebd39d39450c386df0` | `07bd706c3faced716a9a421820e8da6a2bddf099af6fdc7d1347fa574483b984` | old [14260398808](https://github.com/banodoco/astrid-agent/actions/runs/43934820640/artifacts/14260398808): 55 shared, 40 P→P, 13 F→F, 1 E→E, **1 P→F** |
| Unit 8 | [14278249808](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14278249808) `035eb0316e0ca3b3294b4eeb5ac205d78bdd0ce754b86628d090fd253ca7d891` | `adb00f44093c9f0656c1b050b4e712e83a5e31203fd72f89224af0d598885c42` | old [14265546026](https://github.com/banodoco/astrid-agent/actions/runs/43934820640/artifacts/14265546026): 3,752 shared, 3,631 P→P, 94 F→F, 23 S→S, 2 E→E, **2 F→P**; old-only 160 (157 P, 2 S, 1 F), current-only 35 (all P). **Different shard membership, not 160 missing regressions.** |
| Integration 1 | [14277479708](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/artifacts/14277479708) `33674c246e51d362e7b526f7a8f38ff643b2585a6272e39d9efd949c8d2b571f` | `94fb374cce6ea7e5694fe4cb48ec7ce51bdc519a7de437f425e89568f00c4055` | old [14260249942](https://github.com/banodoco/astrid-agent/actions/runs/43934820639/artifacts/14260249942): all 516 shared; 479 P→P, 36 F→F, **1 P→F** |
| Integration 2 | [14278972799](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/artifacts/14278972799) `4f26e9f301570707244087dfa9e65b13b2966daa1d1539fbf3c2f3a07829714e` | `17f03f1f12be6a7809a310d29f822aa12997cb0cd049252cd7ab77a9cb246991` | old [14262871202](https://github.com/banodoco/astrid-agent/actions/runs/43934820639/artifacts/14262871202): all 516 shared; 266 P→P, 172 E→E, 77 F→F, **1 F→P** |

New exact pass-to-failure IDs requiring triage (not yet established code regressions):
- Darwin: `tests.packs.test_text_card_render.TextCardRenderTest::test_text_card_render_smoke` — literal `astrid.core.rendering.errors.RendererInternalError: render service failed: candidate reconciliation budget ran out after 1.269801s (did not stabilize before its deadline)`. Other rendering timeout in same job was already red; transient resource/deadline vs product behavior remains unproved.
- Integration 1: `tests.core.execution.test_generic_host_child_bridge_d18::test_host_bridge_outer_send_diagnostic_preserves_revoke_close[False]` — literal `AssertionError: assert 2049 == 1`, at owned fd2/pipe `fcntl(F_GETFL)` equality. Preserve the diagnostic/revoke invariants; investigate fixture and runner flags, do not loosen assertion. The exact predecessor job passed this ID.

Fixed exact-red IDs (not global release regressions): unit 8 `tests.test_pinokio_platform_adapter::test_cli_help_and_local_receipt_is_never_hosted` and `::test_real_local_start_http_readiness_snapshot_stop_and_port_free`; integration 2 `tests.editing_conformance.test_historical_shared_redo_authority::test_shared_redo_rechecks_source_archive_at_acceptance`. Do not infer these fixes are caused by PR369 without a source/path proof.

## Literal failing-message inventory (finished small jobs)

**Darwin:** 15 red XML records in **12 distinct literal XML-message groups**: `AssertionError: element maths unavailable: None; assert None is not None` (2), `IndexError: tuple index out of range` (2), `AssertionError: {'error': {'message': 'neutral runtime bootstrap was not ready: Requested Runtime identity could not be verified. ...` (2), setup SHA mismatch `6855dfa8... != 9ef80871...` (1), `TS2307` missing generated effects/animations/transitions registries (1), esbuild `import.meta` not available in `cjs` output (five *different full literal messages*, 1 each, not collapsed), and `RendererInternalError` reconciliation deadlines `1.098295s` and `1.269801s` (1 each). Full literal message bodies are retained within the hashed real XML and [job log](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924059), including per-parameter esbuild differences.

**Integration 1:** 37 red XML records in **six distinct literal XML-message groups**: `KeyError: 'bridge.parent'` (21), `RuntimeError: process control is already sandbox; refusing to change it to strict` (8), `astrid.core.execution.generic_host.HostError: delegated child spec lacks admitted_source_digest; refusing before launch` (5), regex expected `evidence cap` but got `delegated child spec lacks admitted_source_digest; refusing before launch` (1), `AssertionError: assert 2049 == 1` (1), and `ModuleNotFoundError: No module named 'tests.core.test_action_cli_clip_rehearsal'` (1). Last import is in scope for SF6d's later guard but that row is Release 15; it is not silently fixed.

**Opt-in:** 12 red log cases: six parameters of `test_saved_actual_filmstrip_v2_composed_capture_readback` require `provide the saved actual public C06 frame-index artifact for affected readback replay`; six `test_onboarding_parity` cases cannot discover/inspect `editorial.arrange` (one discovery AssertionError; five `CapabilityNotFoundError: unknown executor 'editorial.arrange'; nearest matches: executor:training.pool_merge`). The six missing-artifact IDs and the six capability IDs are not waived or reclassified as passing.

**Unit 8:** 96 red XML records in **63 distinct full literal XML-message groups**, including `KeyError: 'macos-15'` (15), `R0StopError: R0 requires the copy-only upgrade boundary. Run the install line again.` (12), `StopIteration` (4), and `ImportError: cannot import name 'retime_with_ripple'` (2). The hash-linked JUnit is authoritative for all 63 groups; this partial checkpoint does not reproduce every long literal body. No group count is mistaken for a root-cause count.

**Integration 2:** 249 red XML records (77 F +172 E) across 516 exact IDs; full distinct-literal inventory remains to be incorporated in the next checkpoint. Do not call its improved 78→77 outer failures a comprehensive fix.

## Independent K1 prerequisites and safety boundaries

The prior 19-gate K1a full-policy result is still **22P/1F** at the reviewed Agent tree. Existing capability-gate assessment documents actual Windows selectors missing for two Windows-native tests, separate second-system-CPython/manual-historical-artifact prerequisites, and fixture-specific ffmpeg marking; no new test suppression or marker migration was made. These require a properly provisioned/reviewed proof, not a guessed rewrite. The two exact new red IDs above are **diagnostic-only** until repeated and source-assessed. No product branch or PR was created by this checkpoint, so no missing independent review is represented as complete.

Runtime strengthened clip test remains **25P/2F** and **uncommitted**; replay versus mandatory CAS-history integrity is an owner contract conflict. Draft Runtime PR56 is *orphan declaration metadata only*, not that clip patch. Plan 38 and 55 remain WAITING. Release 15 is excluded. Secure sign-in was aborted; no login retry or manual dispatch.

**Next bounded action:** re-read only attempt-1 CI/Lanes jobs at the same SHA, download and hash newly completed XML, compare exact `(classname,name)` sets and errors against prior-plan XML, record missing artifact/log limitations, then reassess K1 prerequisite causes without code/test contract changes. Do not advance G1/G2/RS1 (RS1 0/1), plan task checkboxes, or any public/release-main branch.

## Later completed job (same exact head and attempt, 22:49:52 UTC)

CI **unit shard 3** [job 133651924518](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924518) finished **failure**: literal summary `31 failed, 1834 passed, 29644 deselected, 2 warnings in 2099.38s (0:34:59)`; JUnit `unit-shard.xml: tests=1865 failures=31 errors=0 skipped=0`. Downloaded [artifact 14279162456](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14279162456); verified ZIP SHA-256 `6bb5af87d04b19801da97ecb6b109238d3e321979f0ec3fd40838ce1771e7f3f` (GitHub digest agrees), inner XML SHA-256 `643987abce5a08925a9ecba818036c6bd5a12ad95ce2ba2ec8f786051ac36006`. Exact old [artifact 14263779551](https://github.com/banodoco/astrid-agent/actions/runs/43934820640/artifacts/14263779551): 1,857 IDs shared, **1,826 pass→pass, 31 failure→failure, zero red/pass transitions**. Old-only four IDs and current-only eight IDs are **all passes**, showing shard-membership drift; neither is called a regression. Full literal error messages remain in this XML/log, not inferred from its aggregate count. At this later check, six CI unit shards and two Lanes integration shards remained in progress. The earlier point-in-time list above is deliberately left intact.

## Subsequent full-literal group reconciliation from downloaded XML

The counts below are **per-job exact full-message strings**, not independent causal defects and not merged across jobs; artifacts and their verified hashes appear above. The XML payload is the authority for each full literal message (including line-breaks and parameter-specific differences).

| Finished job | Failure/error XML records | Distinct full literal messages | Distinct first-line prefixes |
|---|---:|---:|---:|
| CI darwin native | 15 | 12 | not separately relied on |
| CI unit shard 3 | 31 | **10** | 9 |
| CI unit shard 8 | 96 | 63 | 62 |
| Lanes integration shard 1 | 37 | 6 | 6 |
| Lanes integration shard 2 | 249 | **51** | 50 |

For **integration shard 2**, the largest literal-message categories include 78 errors `CommandError: replacement changes provider-managed edges` during setup, 44 `FileNotFoundError` records referring to a missing scratchpad input, 21 `RuntimeErrorBase: candidate.timing: legacy word anchor is missing`, and additional distinct timing, selected-source SHA, element-pack, and merge/rebase assertion messages. These are explanatory groupings; the **51** full-message groups are enumerated by the actual attached JUnit, not conflated with these headings. All **516** direct test IDs are the same as its prior-plan run; 172 error IDs and 77 failure IDs remain red in common, with exactly one shared failure now passing.

For **unit shard 3**, 31 red XML records fall into **10** full literal groups. Examples include 15 `CommitRejected: fork native binding schema changed`, six `subprocess.CalledProcessError` cases involving `git show` of an unavailable recorded source object, and two regex mismatches; other failed assertions retain their parameter-specific full messages in the artifact. All **31 exact failing IDs** were failing in the corresponding prior-plan job; no shared prior pass became red. Different shard memberships (four old-only passes, eight new-only passes) must not be counted as regressions.

These additions do not alter the frozen G1 totals or formal acceptance: G1/G2 incomplete, RS1 **0/1**, other jobs unfinished.
