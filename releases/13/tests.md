# Release 13 test table

Kept by the Release 13 test manager ([brief](test-manager-brief.md)). There is one row per failing or missing test id, or per job with no result. Results are sorted only with `env/baseline-diff.py`, by the rules in `astrid-dev-green` ([banodoco/astrid-dev#572](https://github.com/banodoco/astrid-dev/pull/572)).

## Latest comparison

**Update, 18:17 UTC:** run `43254543283` is complete. Shards 1 and 5 hit the 120-min limit, **slow, not hung** (no timeout dumps, progress at 94% and 82%), because the committed `tests/.test_durations` is badly stale (W29 is refreshing it). They are NO-RESULT. Re-sorted with shard 4 (6 of 8 unit shards): regression 41, no-baseline 28, preexisting 850, missing 5,309 (provisional). Evidence: `/home/user/wt/r13-tests/compare/agent/f9214240-b/` (to be committed with the next full comparison). The next full run is on the newest compose head, once the durations fix lands.

**PARTIAL, 17:48 UTC:** `f9214240` (Agent CI `43254543283`, `int/r13`) against R12 `main` `0e1543e0`, covering finished unit shards 2, 3, 6, 7 and 8 plus darwin and windows. Shards 1, 4 and 5 are NO-RESULT until they land (about 18:03). Evidence: [`evidence/tests/agent/f9214240-partial/`](evidence/tests/agent/f9214240-partial/summary.md).

**Baselines,** all at `0e1543e0`:
- CI `43155525231`;
- CI `43134432721`, attempts 1 and 2 (same SHA);
- shard 5 pending from CI `43264595988`, on scratch `r13/tests/baseline-r12` `5d108da7` (R12 plus `--ignore=tests/sdk/test_h3_endpoint_r4.py`, which changes coverage; the release manager rules at the binding run);
- Lanes `43155525276` and `43205560755`.

**Still to come:** `fc4b36d4` (CI `43264364443`, `int/r13-next`) and Lanes `43268483674` on `9f9db742`.

| Bucket | f9214240 (partial) | fc4b36d4 |
|---|---|---|
| 1 regression | 41 with shard 4 added (31 triaged, 7 clusters; the 10 new ones are attributed in the next comparison) | pending |
| 2 new test failing, R13 behaviour | at least 1 (`test_core_provider_neutrality`) | pending |
| 3 new test failing, defect already on R12 | 0 so far | pending |
| 4 preexisting | 553 | pending |
| 5 missing | 8,569, provisional: mostly the 3 pending shards | pending |
| 6 flaky | 4 R12 flips; 3 of them fail on the candidate, and those still block | pending |
| UNSORTED (no baseline yet) | 5 (`test_timeline_session_pair`), waiting for the shard-5 baseline | pending |
| Non-test: fast checks (mypy) | fails on both; candidate +228 against R12 +146 (82 more findings). REVIEW | pending |

## Rows

| id | bucket | candidate SHA | cause | introduced by | owner | disposition | link |
|---|---|---|---|---|---|---|---|
| Lanes: opt-in, integration 1–4 | was 1 (NO-RESULT, job-level) on f9214240, fc4b36d4; now per-test | 1f69f754 (Lanes run 43302480458) | the VibeComfy pin read is fixed; Lanes jobs now report `-rA` results. Baseline: R12 main Lanes runs 43155525276 and 43205560755 (identical counts) | — | test manager | integration 1/4: 0 regressions, 10 no-baseline, 36 preexisting. Integration 2/4: 0 regressions, 4 no-baseline, 250 preexisting. W54 is settling the 14 no-baseline ids with local R12 and candidate runs; 3/4, 4/4 and opt-in pending | `tools/lanes-attrib.py` |
| `tests/test_skip_policy.py::test_no_test_file_skips_by_hand` | 4 (49 offenders on R12) | f9214240 (57) | R13 added 5 hand skips, each hiding a test | `07ed95f3`, `9deeef5b`, `15db432f`, `09724310`, `feea4ac6` | test manager (3), engine lane (2) | 3 fixed and merged (`72a6db07` run-logs; `f9f109e7` G3 ×2); 2 relayed to the engine lane (`r13/engine-skips`) | release manager rule: run with the skip removed first |
| `tests/test_vibecomfy_pin.py::test_no_other_tracked_file_copies_the_pin` | UNSORTED | f9214240 | the pin is copied in `test_engine_cli.py`, `test_engine_recipe.py` and `test_installer_sources.py` | pending | pending | pending the comparison | — |
| `tests/integrations/test_remote_machine_cpu.py::test_resolved_runpod_policy_controls_the_claim_and_warm_hold` | UNSORTED | f9214240 (local) | teardown: `AcquisitionUnresolvedError`, then `RunPodWorkerOwnerError`, then `CustodyError` "host graph cleanup remains unresolved" (`generic_host.py:7164`) | pending | machines lane if bucket 1 or 2 | pending the comparison | W07 local run |
| `tests/sdk/test_h3_endpoint_r4.py::*` (all ids) | 5 (missing) | f9214240 | file deleted | `3079370d` (Plan 32 T6b-3, retires the h3 stage actions) | — | ruling by the release manager (12 Nov): removed on purpose. Applies once W06 Part D confirms the commit removes exactly the covered behaviour | — |

| Lint per (file, code): ruff and mypy (fast checks) | 1 (non-test check) | ruff on compose `14fa999a` + gate; mypy on `6f304c48` | owner ruling (12 Nov): only ruff F821 and BLE001 and mypy name-defined, attr-defined and call-arg block; other codes are reported. The mypy total gate is dropped; the ruff total gate is kept (2,100 = 2,100) | many | machines: ruff 9 BLE001 rows (including `sdk/invocation.py` 3→4 from `16ffaa60`), mypy 5 rows; engine 0; test manager 0 | gate `91ffac35` (`r13/tests/lint-bug-classes`) ready to merge. I001: one `ruff --select I001 --fix` commit after the lanes freeze (the stale sweep `917ba11b` conflicts). Hosted CI on the next frozen head gives the binding mypy count | [evidence](evidence/tests/mypy/REPORT.md) |
| `astrid/sdk/invocation.py` dead prepared-owner recovery code (h3) | — (cleanup) | compose `14fa999a` | 103 unreferenced lines | Plan 32 T6b-3 | test manager | `a08e14a3` (`r13/tests/h3-dead-owner`) ready: 842 tests each side, 0 regressions | — |
| `tests/packs/runpod/test_release_after_acquisition_failure.py` (A–D), `test_acquisition_catalog_id.py`, `test_acquisition_graphql_confirmation.py`, `test_warm_session.py` expectation rows | 1 | compose `6f304c48` | tests expected the pre-R13 acquisition-failure contract; the error after a confirmed exact release was untruthful; a dict gate crashed `TargetObservationError`; the recovery annotation could consume the last release retry (W33) | machines lane commits | test manager (route S) | fixed: `4b0f55c0` (`r13/tests/release-after-failure`); one Astra pass, its P2 resolved; 0 regressions, 11 fixed, 4 new tests | — |
| `test_public_sfx_route_receives_declared_inputs` | 1 (known) | compose `e42d22163` | expects `target=None`, gets `placement='auto'` | target→placement rename | engine lane | the #607 placement fix covers it | — |
| Generated artifacts: `test_cli_surface_is_current`, `test_planted_cli_surface_drift_is_named`, `test_capability_matrix_copies_are_identical`, `test_product_resources[astrid-beta-capabilities]` | 1 | f9214240, 913c6b8f | `cli-surface.json` not regenerated after `tasks logs`; packaged matrix not synced after a config-only edit | `90551c4f`, `cffffe05`; `5f531504` | test manager | fixed: `ade51fb9` (`r13/tests/artifacts`) | — |
| `tests/packs/test_audio_render.py::…test_rendered_mp4_contains_audio_stream`, `tests/packs/test_text_card_render.py::…test_text_card_render_smoke` | 6 (flaky; R12 failed each 1 of 3) | f9214240 | reentrant custody lock: a nested guard on the owning thread reports "deadline expired acquiring custody lock" after a 1.0 s budget (`process_group.py:551-577`, `custody_broker.py:2864`) | predates R12 | machines lane (core/execution) or Plan 39: ruling pending | fix direction: one guarded transaction through the nested observation | triage W18 |
| `tests/test_pinokio_platform_adapter.py::test_real_local_start_http_readiness_snapshot_stop_and_port_free` | 6 (flaky; R12 failed 2 of 3) | f9214240 | the post-ready process snapshot is one-shot, while startup polls (`scripts/pinokio_platform_adapter.py:1369`) | predates R12 | Plan 39 | ruled preexisting flake (12 Nov); deferred | [astrid-dev#621](https://github.com/banodoco/astrid-dev/issues/621) |
| `tests/test_skills_sync_registry.py::BaseHelperTest::test_env_inventory_source_is_visible_to_skill_discovery` | 2 (stale fixture, proposed) | f9214240, 913c6b8f | discovery reads `pack.documentation` (`discovery.py:231`); the fixture's fake pack has none | `812d1142` | test manager | fixed in product: `e003999c` (`r13/tests/skills-seam`); the fixture change was withdrawn | triage W18 |

## Plan 39 rows to open

- **R12 unit shard 5 never finishes.** On `main` `0e1543e0`, `tests/sdk/test_h3_endpoint_r4.py`'s tests hit the 600 s pytest-timeout in turn (leaked `serve_forever` threads). The shard is cancelled at 120 min, 43% through 4,471 tests, in all three R12 runs. The file is gone in R13.

## Plan 50 evidence (offline checks)

Stage 1 live, 12 Nov: three failures a CPU check should have caught (owned and being fixed by the release manager's lanes):
- SFX: VibeComfy refused `CHOICE` against `COMBO` on a public input.
- TTS: transformers 5 dropped `pad_token_id` from the node's config.
- Music: VibeComfy's stale first-build digest.
