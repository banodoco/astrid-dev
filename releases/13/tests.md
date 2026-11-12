# Release 13 test table

Kept by the Release 13 test manager ([brief](test-manager-brief.md)). There is one row per failing or missing test id, or per job with no result. Results are sorted only with `env/baseline-diff.py`, by the rules in `astrid-dev-green` ([banodoco/astrid-dev#572](https://github.com/banodoco/astrid-dev/pull/572)).

## Latest comparison

**PARTIAL, 17:48 UTC:** `f9214240` (Agent CI `43254543283`, `int/r13`) against R12 `main` `0e1543e0`, covering finished unit shards 2, 3, 6, 7 and 8 plus darwin and windows. Shards 1, 4 and 5 are NO-RESULT until they land (about 18:03). Evidence: [`evidence/tests/agent/f9214240-partial/`](evidence/tests/agent/f9214240-partial/summary.md).

**Baselines,** all at `0e1543e0`:
- CI `43155525231`;
- CI `43134432721`, attempts 1 and 2 (same SHA);
- shard 5 pending from CI `43264595988`, on scratch `r13/tests/baseline-r12` `5d108da7` (R12 plus `--ignore=tests/sdk/test_h3_endpoint_r4.py`, which changes coverage; the release manager rules at the binding run);
- Lanes `43155525276` and `43205560755`.

**Still to come:** `fc4b36d4` (CI `43264364443`, `int/r13-next`) and Lanes `43268483674` on `9f9db742`.

| Bucket | f9214240 (partial) | fc4b36d4 |
|---|---|---|
| 1 regression | 31, in 7 clusters; triage W11–W13 running | pending |
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
| Lanes: all 5 test jobs (opt-in, integration 1–4) | 1 (NO-RESULT, job-level) | f9214240, fc4b36d4 | "Read the pinned VibeComfy revision" raises `UnknownEngine: vibecomfy`, so 0 tests run | `cff69d9c` moved `ci.yml` to `scripts/vibecomfy_pin.py` and missed `lanes.yml` | test manager | fixed: `895d08c8`, merged in `r13/compose` `9f9db742`; hosted proof pending, Lanes `43268483674` | agent `r13/tests/lanes-vibecomfy-pin` |
| `tests/test_skip_policy.py::test_no_test_file_skips_by_hand` | 4 (49 offenders on R12) | f9214240 (57) | R13 added 5 hand skips, each hiding a test | `07ed95f3`, `9deeef5b`, `15db432f`, `09724310`, `feea4ac6` | test manager (3), engine lane (2) | 3 fixed and merged (`72a6db07` run-logs; `f9f109e7` G3 ×2); 2 relayed to the engine lane (`r13/engine-skips`) | release manager rule: run with the skip removed first |
| `tests/test_vibecomfy_pin.py::test_no_other_tracked_file_copies_the_pin` | UNSORTED | f9214240 | the pin is copied in `test_engine_cli.py`, `test_engine_recipe.py` and `test_installer_sources.py` | pending | pending | pending the comparison | — |
| `tests/integrations/test_remote_machine_cpu.py::test_resolved_runpod_policy_controls_the_claim_and_warm_hold` | UNSORTED | f9214240 (local) | teardown: `AcquisitionUnresolvedError`, then `RunPodWorkerOwnerError`, then `CustodyError` "host graph cleanup remains unresolved" (`generic_host.py:7164`) | pending | machines lane if bucket 1 or 2 | pending the comparison | W07 local run |
| `tests/sdk/test_h3_endpoint_r4.py::*` (all ids) | 5 (missing) | f9214240 | file deleted | `3079370d` (Plan 32 T6b-3, retires the h3 stage actions) | — | ruling by the release manager (12 Nov): removed on purpose. Applies once W06 Part D confirms the commit removes exactly the covered behaviour | — |

| mypy (fast checks, "Mypy baseline gate") | 1 (non-test check; the release manager ruled it must not grow) | 913c6b8f | 2,420 against R12's 2,338 (baseline 2,192). 192 findings added, 110 removed | many; see the evidence | machines 102, engine 41, test manager 49 | each lane fixes its own while in those files; the gate is count-based | [evidence](evidence/tests/mypy/REPORT.md) |
| Generated artifacts: `test_cli_surface_is_current`, `test_planted_cli_surface_drift_is_named`, `test_capability_matrix_copies_are_identical`, `test_product_resources[astrid-beta-capabilities]` | 1 | f9214240, 913c6b8f | `cli-surface.json` not regenerated after `tasks logs`; packaged matrix not synced after a config-only edit | `90551c4f`, `cffffe05`; `5f531504` | test manager | fixed: `ade51fb9` (`r13/tests/artifacts`) | — |
| `tests/packs/test_audio_render.py::…test_rendered_mp4_contains_audio_stream`, `tests/packs/test_text_card_render.py::…test_text_card_render_smoke` | 6 (flaky; R12 failed each 1 of 3) | f9214240 | reentrant custody lock: a nested guard on the owning thread reports "deadline expired acquiring custody lock" after a 1.0 s budget (`process_group.py:551-577`, `custody_broker.py:2864`) | predates R12 | machines lane (core/execution) or Plan 39: ruling pending | fix direction: one guarded transaction through the nested observation | triage W18 |
| `tests/test_pinokio_platform_adapter.py::test_real_local_start_http_readiness_snapshot_stop_and_port_free` | 6 (flaky; R12 failed 2 of 3) | f9214240 | the post-ready process snapshot is one-shot, while startup polls (`scripts/pinokio_platform_adapter.py:1369`) | predates R12 | Plan 39 (proposed) | ruling pending | triage W18 |
| `tests/test_skills_sync_registry.py::BaseHelperTest::test_env_inventory_source_is_visible_to_skill_discovery` | 2 (stale fixture, proposed) | f9214240, 913c6b8f | discovery reads `pack.documentation` (`discovery.py:231`); the fixture's fake pack has none | `812d1142` | test manager | ruling pending: `documentation={}` in the fixture | triage W18 |

## Plan 39 rows to open

- **R12 unit shard 5 never finishes.** On `main` `0e1543e0`, `tests/sdk/test_h3_endpoint_r4.py`'s tests hit the 600 s pytest-timeout in turn (leaked `serve_forever` threads). The shard is cancelled at 120 min, 43% through 4,471 tests, in all three R12 runs. The file is gone in R13.

## Plan 50 evidence (offline checks)

Stage 1 live, 12 Nov: three failures a CPU check should have caught (owned and being fixed by the release manager's lanes):
- SFX: VibeComfy refused `CHOICE` against `COMBO` on a public input.
- TTS: transformers 5 dropped `pad_token_id` from the node's config.
- Music: VibeComfy's stale first-build digest.
