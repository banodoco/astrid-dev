# W203 fifth-candidate check attribution

Snapshot 2026-11-15 16:44 UTC; the 90-minute observation window has ended; some checks are queued or running. This is a partial report. App PR #268 has moved to `adad82f07cf35007f96fa44adea9211a09117391`, so the specified App SHA is no longer the PR head. The new head is one commit ahead and changes `QuietUpdateNotice.tsx` and its test; its checks do not establish the specified candidate. App PR #268 head `54b435d869c6e17c6618518600377c4ff741e7cc`; Agent PR #347 head `37bd5e069492446bd62d94ff7aa40eb3143d8f85`. Both PRs report mergeable. Journey-row and boot-manifest review gate evidence has not been assessed here.

App PR event Tests 43728682193 and Dockerfile 43728682200; push Tests 43728676624, E2E 43728676616, Lanes 43728676633; direct-journey dispatch 43728683352. All are on App head as reported by the run list. A pull request run uses a merge ref; its actual checkout SHA must be confirmed from its log when available. `gh pr checks` failed with GraphQL 403; REST check-runs used. Main baselines: Tests 43703109315, E2E 43703109324, Lanes 43709054148, Direct Journey 43707235824, Dockerfile 43703109391.

| App job | Main | Fifth candidate | Verdict |
|---|---|---|---|
| release-guard | pass | PR cancelled without steps; push skipped | pending |
| Dockerfile checks | pass | PR cancelled | pending |
| boundary | pass | push pass; PR skipped | pass |
| vitest | pass | push pass; PR skipped | pass |
| release-tooling-macos | pass | push pass; PR skipped | pass |
| extension-accessibility | fail | same 9 cases :114 and :156 | preexisting |
| extension-visual | fail | same :154 | preexisting |
| extension-cross-browser | fail | same six cases :76 and :97 | preexisting |
| playwright-timeline-chrome-export | fail | same :304, :412, :231 | preexisting |
| playwright-timeline | fail | same 36 failure-context IDs | preexisting |
| playwright-default | fail | 27 shared IDs plus one additional ID | pending; different IDs |
| checkout-lanes | fail | same runtimePackRefresh test and missing Chromium | preexisting |
| installer-posix (ubuntu-latest) | pass | push pass | pass |
| installer-posix (macos-latest) | pass | push pass | pass |
| installer-powershell | pass | push pass | pass |
| quick-journey | fail | same :3419 source-tuple assertion | preexisting |
| direct-journey | pass | dispatch cancelled | pending |
| three-products | fail :3674 | dispatch cancelled | pending |

No new App check name observed. Release-guard was cancelled without steps; its 12-to-13 and pins/required verification cannot yet be reported. Direct Journey attempt 1 was cancelled; its three-products job had no steps, so all 14 tests lack recorded outcomes. No additional attempt was recorded. PR-event workflows at this head are Tests and Dockerfile; neither has a three-products job.

Agent PR 347 PR-event Windows task host journey 43728675122 reports the candidate head; the Both jobs checked out merge SHA `18d67cc875c582ee56c6f31c68eda8a7f5226954`. Push CI 43728670712, Lanes 43728670644, Chat service 43728670674 use the Agent head. A'' CI 43713785559 and Lanes 43713785564 used `34fee0cf`; R12 main used `0e1543e0`.

| Agent job | Fifth candidate | A'' | R12 main |
|---|---|---|---|
| Windows task host journey (pwsh.exe) | fail, SDK settlement exit 2 | no corresponding job in CI/Lanes | fail at bootstrap |
| Windows task host journey (powershell.exe) | fail, SDK settlement exit 2 | no corresponding job in CI/Lanes | fail at bootstrap |
| fast checks | fail, Ruff baseline improved by 1 | fail | fail |
| boundary | pass | pass | pass |
| darwin native | fail; same 13 IDs | fail | fail |
| release wheel / Python 3.11 | pass | pass | pass |
| release wheel / Python 3.12 | pass | pass | pass |
| windows-native-and-installer | pass | pass | pass |
| unit shards 1–8 | shards 3, 4, 5 and 8 fail; 1, 2, 6 and 7 running | fail | shards 1 and 5 cancelled; others fail |
| installed wheel | pass | pass | pass |
| opt-in | fail; same 12 IDs | fail | fail |
| integration shards 1–4 | shard 1 fails with same 36 IDs; shard 2 has one additional ID; shards 3–4 running | fail | fail |
| chat | pass | pass | not compared |
| windows-launchers | pass | pass | not compared |

Both PR jobs failed SDK settlement `journey-packs-list.json: exit 2`, like the previous PR head; R12 failed earlier at bootstrap. Integration shard 2 has one additional ID versus A'': `tests/editing_conformance/test_historical_shared_redo_authority.py::test_shared_redo_rechecks_source_archive_at_acceptance`; it was also observed on the previous PR head. Fast checks: setup, checkout, fixture pins/checkouts, cache restore, Python, media tools, dev package and pinned Runtime/client, engine checkout/install all passed; Ruff failed (current 2009, baseline 2010; baseline update requested), mypy stub installation and mypy gate skipped, Import cycles gate skipped, collection gate passed; cache save and cleanup reported success (cache reservation warned). Darwin native has the same 13 failure/error IDs as A''; `tests/packs/test_audio_render.py::AudioRenderTest::test_rendered_mp4_contains_audio_stream` and `tests/packs/test_text_card_render.py::TextCardRenderTest::test_text_card_render_smoke` both passed. Unit shard 3 has 31 failure IDs identical to both prior candidates, and no failing regression or no-baseline IDs. Unit shard 4 has 47 distinct failure/error IDs identical to `8e0006f5` and `34fee0cf`, and no failing regression or no-baseline IDs. Unit shard 5 has 202 distinct failure/error IDs identical to `8e0006f5` and `34fee0cf`; its partial attribution reports no failing regression or no-baseline IDs. Unit failure deltas for other shards and `test_installer_has_no_lazy_third_party_imports` remain pending. The previous candidate `candidate/8e0006f5/ci` attribution files are present; fifth-candidate attribution remains pending. A preexisting watcher for the fifth candidate is running. GitHub access was read-only.

## App playwright-default failure-context IDs

Main has the following 27 IDs; the candidate has these same 27 plus the extra ID below. These are log context identifiers, not a claim about root cause.

- `test-results/extension-harness-Extensio-19c58-vation-without-page-refresh-chromium-condensed/error-context.md`
- `test-results/extension-harness-Extensio-19c58-vation-without-page-refresh-chromium-desktop/error-context.md`
- `test-results/extension-harness-Extensio-19c58-vation-without-page-refresh-chromium-mobile/error-context.md`
- `test-results/production-widget-scope-pr-afeb9-t-action-different-project--chromium-desktop/error-context.md`
- `test-results/production-widget-scope-pr-b777e-output-action-same-project--chromium-desktop/error-context.md`
- `test-results/production-widget-scope-pr-c745c-a-dialog-of-another-project-chromium-desktop/error-context.md`
- `test-results/production-widget-scope-pr-da9d0--with-background-completion-chromium-desktop/error-context.md`
- `test-results/production-widget-scope-pr-e1980-t-and-captures-pending-load-chromium-desktop/error-context.md`
- `test-results/public-astrid-integrated-A-491c4--disclosure-and-live-motion-chromium-condensed/error-context.md`
- `test-results/public-astrid-integrated-A-491c4--disclosure-and-live-motion-chromium-desktop/error-context.md`
- `test-results/public-astrid-integrated-A-491c4--disclosure-and-live-motion-chromium-mobile/error-context.md`
- `test-results/public-astrid-vision-hiera-2c92f--border-only-hover-feedback-chromium-condensed/error-context.md`
- `test-results/public-astrid-vision-hiera-2c92f--border-only-hover-feedback-chromium-mobile/error-context.md`
- `test-results/public-astrid-vision-hiera-b3fdd-ders-gains-a-full-hover-box-chromium-condensed/error-context.md`
- `test-results/public-astrid-vision-hiera-b3fdd-ders-gains-a-full-hover-box-chromium-mobile/error-context.md`
- `test-results/public-astrid-vision-hiera-de46c-thout-underlining-the-title-chromium-condensed/error-context.md`
- `test-results/public-astrid-vision-hiera-de46c-thout-underlining-the-title-chromium-mobile/error-context.md`
- `test-results/public-astrid-vision-sigil-03bc0-and-respects-reduced-motion-chromium-condensed/error-context.md`
- `test-results/public-astrid-vision-sigil-03bc0-and-respects-reduced-motion-chromium-mobile/error-context.md`
- `test-results/public-astrid-vision-sigil-18cf8-ve-and-one-second-to-return-chromium-condensed/error-context.md`
- `test-results/public-astrid-vision-sigil-18cf8-ve-and-one-second-to-return-chromium-mobile/error-context.md`
- `test-results/public-astrid-vision-sigil-899e1-ir-readable-cue-stays-solid-chromium-condensed/error-context.md`
- `test-results/public-astrid-vision-sigil-899e1-ir-readable-cue-stays-solid-chromium-mobile/error-context.md`
- `test-results/video-editor-instance-life-db737-nds-selection-and-renderers-chromium-desktop/error-context.md`
- `test-results/video-editor-workflow-pari-2afde--media-from-the-same-editor-chromium-condensed/error-context.md`
- `test-results/video-editor-workflow-pari-2afde--media-from-the-same-editor-chromium-desktop/error-context.md`
- `test-results/video-editor-workflow-pari-2afde--media-from-the-same-editor-chromium-mobile/error-context.md`

Candidate-only: `test-results/public-astrid-vision-polis-15867-oving-its-snapshot-at-390px-chromium-condensed/error-context.md` (`public-astrid-vision-polish.spec.ts:288`, chromium-condensed; outgoing 480, expected greater than 500).

Separate same-SHA push runs appeared on `int/r13.1`: CI 43735351050, Lanes 43735350969 and Chat service 43735351036. They were not initiated by this observation and are distinct from the specified runs.


Unit shard 8: 97 distinct failure/error IDs. Against `8e0006f5`, four candidate-only IDs:

- `tests/test_installer_transaction_authority.py::test_cli_recovers_completed_stop_with_fresh_controller[stop-return-app]`
- `tests/test_installer_transaction_authority.py::test_cli_recovers_completed_stop_with_fresh_controller[stopped-app]`
- `tests/test_pinokio_platform_adapter.py::test_cli_help_and_local_receipt_is_never_hosted`
- `tests/test_pinokio_platform_adapter.py::test_real_local_start_http_readiness_snapshot_stop_and_port_free`

Against `34fee0cf`, the two installer-transaction IDs above are candidate-only; `tests/test_pinokio_platform_adapter.py::test_secret_never_appears_in_receipt_state_or_cli_output` is A''-only. The R12 attribution labels the real-local-start ID flaky on R12, zero regressions, and these two failing IDs no-baseline:

- `tests/test_onboarding_one_home.py::test_shipped_skills_run_astrid_through_the_launcher_not_python_m`
- `tests/test_setup_skill_branches.py::test_runpod_setup_from_pristine_settings_preserves_choices_and_quotes_without_claim`

The installer-import test is not in the four completed shard logs; its outcome remains pending. No R12 regression is reported in the completed shard attributions; unfinished shards cannot be assessed.

Direct Journey attempt 1: `three-products.spec.ts` tests :417, :611, :1558, :1691, :1917, :2098, :2355, :2437, :2629, :3200, :3504, :3674, :2904, :2996 all have no recorded outcome because the job was cancelled before its first step. The PR Tests and Dockerfile runs contain no three-products job.
