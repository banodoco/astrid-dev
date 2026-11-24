# Plan 39 (Runtime main green): clusters C1 and C2

Repo: astrid-runtime. Branch read: `origin/release/15/main` at `24e2c9291d5bcaface78324696286f2dc896debc` (fetched 2026-11-24). Plan source: astrid-dev `origin/main` at `bd4c3e1935a16962ad0f55929b403f026b26e670`. Read-only; nothing run, nothing pushed.

## Verdict

**The fence is correct product behaviour. The tests and fixtures are stale.** Nothing in the product should be weakened.

- The fence (`runtime_protocol/v33_lifecycle.py:297-300`, `require_ready`) refuses mutations while `.v33-activation.json` is not `ready`. It is called per mutation from `runtime_protocol/service.py:998-999` (`_assert_mutation_admitted`).
- The state only reaches `ready` through provider registration: `provider_ready()` (`v33_lifecycle.py:303-309`) runs from `RuntimeService.register_timeline_commit_provider` (`service.py:~3211`). That call verifies the baseline and writes `ready`.
- The precut fixture now migrates the realm (`tests/precut_realm_fixture.py:173-176`, added in c0043f6). `migrate_canonical_to_current` calls `lifecycle.begin()` (`runtime_protocol/upgrade.py:1043`), which writes the marker in state `backup_verified` (`v33_lifecycle.py:209`). The fixture therefore hands every consumer a migrated, fenced realm.
- Plan 39 already names this exact failure. `plans/39-green-mains/tasks.md` RT1 ("Verify migrated-realm readiness before reads or mutation", 168 verification-pending IDs) and RT2 ("Complete fresh provider registration on migrated-realm restart", 124 IDs, the `daemon.py:320` case). `plans/39-green-mains/inputs.md:53-54` marks R-d and R-e "stale, **verify**". This report is that verification.
- Plan 39 RT1 says: no test may write `.v33-activation.json` as `ready` or patch `require_ready`. Fixing the tests by hand-writing `ready` is therefore ruled out. The correct fix is to register the provider.

Why it is not a product bug: the app always passes `--authoring-profile astrid` (`astrid_runtime/runtime_boundary.py:56-66`, `:270`), so the app path clears the fence. The neutral path is fail-closed (refusal, not a bypass): `daemon.py:317-320` refuses to serve a migrated realm without a provider.

Staleness, dated: the five named test files were last touched in `8d425ea` (2026-10-27, per `git log`; the brief says 28 Oct, which I could not reproduce). The fence and the fixture migration both arrived in `c0043f6` (2026-11-01). The tests predate the fence.

## Counts (distinct IDs; `failing-ids.tsv` has 3 rows per ID, one per job; 3 distinct jobs per cluster)

- C1 = 696 rows = **232 distinct IDs**.
- C2 = 378 rows = **126 distinct IDs**.
- C1 and C2 are disjoint. Union = 358 distinct IDs.

| file | param | C1 | C2 |
| --- | --- | ---: | ---: |
| tests/test_timeline_effect_authority.py | `service` (neutral `RuntimeService`, no provider) | 106 | |
| tests/test_timeline_effect_authority.py | `http` (neutral `RuntimeDaemon`) | | 106 |
| tests/test_timeline_document_authority.py | `service` / `http` (mutates via neutral service before daemon start) | 62 (31 + 31) | |
| tests/test_timeline_reference_authority.py | `neutral` (`service_case`, `:76`) | 38 | |
| tests/test_project_reference_catalog.py | `neutral` (imports `service_case`) | 13 | |
| tests/test_realm_admission_hardening.py | - | 8 | |
| tests/test_timeline_authority_door.py | neutral `RuntimeDaemon` in `realm` fixture (`:33`) | | 12 |
| tests/test_timeline_shot_authority.py | service 1 / http 4 | 1 | 4 |
| tests/test_shot_composition_runtime.py | | 1 | 2 |
| tests/test_timeline_reads_after_cut.py, test_timeline_cutover.py, test_precut_variants.py | | 3 | |
| tests/test_timeline_visibility_generated_http.py, tests/test_streaming_media_io.py | | | 2 |

No `astrid` param ID is in either cluster (0 in the TSV), which fits "the astrid params pass". `reference_authority`'s `astrid` variant and `http_case` already use the provider and pass.

## Proposed cards

### Card P39-RT1 (C1, 232 IDs): register the provider before the first mutation; retire the neutral variant

- Repo: astrid-runtime. Kind: **stale-test**.
- Evidence: `runtime_protocol/v33_lifecycle.py:297-300` (fence); `service.py:998-999`; `tests/precut_realm_fixture.py:173-176` (migration, c0043f6); `runtime_protocol/upgrade.py:1043` (`begin`, state `backup_verified`); `plans/39-green-mains/tasks.md` RT1 and RT2 (already name this cause); `plans/39-green-mains/inputs.md:53` (R-d).
- Fix:
  1. Add one shared test helper (new file under `tests/`, e.g. `tests/migrated_realm.py`) that opens a migrated realm and calls `register_timeline_commit_provider(provider)` before any mutation. Use the real Agent provider (as `http_case` already does) or the test `PreparedProvider`. Do not write the marker.
  2. `tests/test_timeline_effect_authority.py:_seed` (`:33-50`): move `register_timeline_commit_provider` above the `register_capability` loop (currently `:39`, provider at `:47`). This ordering is the direct trigger for the 54 `same_key_changed` and similar IDs.
  3. `tests/test_timeline_reference_authority.py:seed` and `service_case` (`:38-78`): drop `neutral` from `params`. Keep one negative test: a neutral `RuntimeService` on the migrated realm refuses `create_project` with `pending; requests and fresh pins are fenced` (RT1's required negative case).
  4. `tests/test_timeline_document_authority.py:documents` (`:18-30`): register the provider before `verify_baseline` and the seed mutation (`:~55`).
  5. `tests/test_project_reference_catalog.py` inherits `service_case`; no separate change.
  6. The 8 `test_realm_admission_hardening.py` IDs and the single IDs in shot/cutover/reads_after_cut/precut_variants: same cause, but not read in detail. Re-run after the fix.
- Scope: `tests/test_timeline_effect_authority.py:_seed`, `:boundary`; `tests/test_timeline_reference_authority.py:seed`, `:service_case`; `tests/test_timeline_document_authority.py:documents`; new helper file. No file under `runtime_protocol/` or `astrid_runtime/`.
- Focused proof: `tests/test_timeline_effect_authority.py tests/test_timeline_document_authority.py tests/test_timeline_reference_authority.py tests/test_project_reference_catalog.py tests/test_realm_admission_hardening.py`, plus the new negative case.
- Route **X** (the neutral-variant decision and the helper are coupled reasoning). Size **2-3 engineering days**.
- Dependencies: none. Card P39-RT2 uses the helper.
- Confidence: cause verified in code and in the log (`logs/137989251787.log`: `_seed` at `test_timeline_effect_authority.py:39` raises via `service.py:999`). Fix outcome inferred, not run.

### Card P39-RT2 (C2, 126 IDs): daemon fixtures on migrated realms pass the astrid profile; one neutral refusal test

- Repo: astrid-runtime. Kind: **stale-test**.
- Evidence: `runtime_protocol/daemon.py:317-320` (refusal); `runtime_protocol/timeline_commit_provider.py:72-78` (neutral returns no provider); `astrid_runtime/runtime_boundary.py:56-66,270` (app always astrid); `tests/test_timeline_reference_authority.py:91` (`http_case` already uses `authoring_profile="astrid"`); `logs/137989251348.log` (`tests/test_timeline_authority_door.py:33` -> `daemon.py:320`).
- Fix:
  1. `tests/test_timeline_authority_door.py:realm` (`:33`): `RuntimeDaemon(..., authoring_profile="astrid")`.
  2. `tests/test_timeline_effect_authority.py:boundary` (`:91`) and `tests/test_timeline_shot_authority.py`, `tests/test_shot_composition_runtime.py`, `tests/test_timeline_visibility_generated_http.py`, `tests/test_streaming_media_io.py`: same profile change. Caveat: the daemon registers its own provider at start, and `register_timeline_commit_provider` is startup-only (`service.py:3187` raises `ValidationError`). So `_seed` must not re-register on `daemon.service`. The `http` boundary needs its own seed path. This is an open question (below).
  3. Add one negative test: `RuntimeDaemon(migrated_root)` with no profile refuses with `migrated realm requires fresh Timeline provider registration before readiness` (RT2's negative case).
- Scope: `tests/test_timeline_authority_door.py:realm`; `tests/test_timeline_effect_authority.py:boundary`; the four smaller files above (`daemon` constructor lines only).
- Focused proof: `tests/test_timeline_authority_door.py tests/test_timeline_effect_authority.py -k http` plus the negative test. Run the 126 IDs in the Plan 39 lane (CI runs `tests/` with the pinned Agent).
- Route **N**. Size **1-2 engineering days**.
- Dependencies: **P39-RT1** (the helper and ordering). Do after RT1, since `document_authority` `http` IDs are currently hidden behind C1 and will surface as C2 once RT1 lands. Re-count after RT1.
- Confidence: cause verified in code and log. Outcome inferred.

## Open questions for the owner

1. **`runtime_protocol replace` (`runtime_protocol/cli.py:361`)** constructs a neutral `RuntimeDaemon` with no profile. On a migrated realm it will now refuse (fail-closed). Is `replace` a user path? If yes, it needs `--authoring-profile` (this is RT2's "if a user's upgrade can hit it, open RT2.bug"). I did not verify how `replace` is invoked by the app.
2. **Neutral start default** (`runtime_protocol/cli.py:67`, `default="neutral"`). A direct `python -m runtime_protocol start` on a migrated realm refuses. That is intended, but confirm the default should stay neutral.
3. **Effect-authority `http` boundary**: should it use the real Agent provider, or the test `PreparedProvider` injected into the daemon? The daemon constructor doesn't take a provider today.

## Could not verify

- No tests were run (read-only brief; no pytest/Agent environment).
- Whether the measured run's commit equals `24e2c92` (the measurement logs are dated 2026-11-23; I did not match SHAs).
- The 8 `realm_admission_hardening` and 5 single-ID C1 files were not read in detail.
- The brief's "28 Oct" last-edit date: `git log` shows 27 Oct (`8d425ea`). Either date is before c0043f6 (1 Nov), so the conclusion is unchanged.
- The brief's "232 / 126 ids" are distinct IDs. `failing-ids.tsv` has 3 rows per ID (one per job), so raw row counts are 696 and 378.
