# Runtime tail: singleton clusters (CI, release/15/main) and Nightly (main run 45166036353)

Plan 39 helper output, read-only. Mirrors Plan 91 Wave C (`plans/91-agent-main-green/tasks.md`, "Triage rules" 0-6, D5/D12 in `inputs.md`). Every card gets a **first-reading kind**, not a verdict; a card's kind is confirmed only at its reproduce step (triage rule 1).

Sources read: `runtime-green/clusters.md`, `failing-ids.tsv`, `out_nightly/clusters.md`, `out_nightly/failing-ids.tsv`; Runtime `origin/release/15/main` = `24e2c929` (2026-11-23 21:25, current head; the CI measurements were on `5120462d`, 2026-11-22); Agent pin `tests/astrid-agent.pin` = `0e1543e0`; Agent `origin/release/15/main` = `FETCH_HEAD` at fetch time (checked out only for reading). Line numbers below are at those heads.

## 1. Coverage

| Area | Clusters | Unique IDs | Cards |
| --- | ---: | ---: | --- |
| CI singletons in scope (this doc, CI-1 to CI-10) | 39 of 59 | 46 | 10 |
| Nightly, all 50 clusters (N-1 to N-17) | 50 | 152 (all mapped) | 17 cards |
| Pointers, not carded here | - | 8 | R-b (1 nightly ID, `test_wc10_installed_launcher.py:26`), portability (7 nightly IDs; CI C15, C41, C43-C46) |

CI clusters excluded because another helper owns them: C1-C7 (Timeline authority, precut and v33 fence), portability (C15, C41, C43-C46), sandbox/platform (C8 pidfd custody; C55 and C56 Linux listener; C57 Darwin custody; C58-C59 process control), and R-b (C22 `test_p2_commit_phase_capture.py:62`).

Overlap to resolve at dispatch: CI-5 (`test_bootstrap.py` StaleOwnerTests) fails in both the sandbox job and unit-mac; the sandbox side belongs with the sandbox helper if it owns pidfd and owner identity.

Nightly is a separate job (`-m integration`), so its 152 IDs are reported separately from the CI rows.

## 2. How Nightly runs on release/15/main (answers the dispatch question)

- `.github/workflows/nightly.yml` (identical at release/15/main and in the SCRATCH copy) has `on.schedule` cron `0 3 * * *` and `on.push.branches: ["release/14/plan-39"]`, plus `workflow_dispatch` with input `agent_sha` (`nightly.yml:1-17`). GitHub fires scheduled workflows only from the default branch, so **release/15/main gets no automatic Nightly**. It must be dispatched: `gh workflow run nightly.yml --repo banodoco/astrid-runtime --ref release/15/main` (optionally `-f agent_sha=<40-hex>`). The push trigger names a stale release branch and needs a `release/15/main` entry to run on push.
- The job runs `pytest -q -rA --junitxml=... -m integration` with **no `--process-control` flag** (`nightly.yml`, "Run nightly integration tests"). That matters for N-6.
- Agent checkout: the pin (`0e1543e0`) unless `agent_sha` is given (`nightly.yml`, "Select Agent revision"). The step "Check historical Agent archive input" only warns when `321cef4b` is missing (`HISTORICAL_AGENT_SHA`), so it does not fail the run.
- The latest run (45166036353) was on `5120462d`. Re-dispatch on `24e2c929` before carding, because some IDs may already have changed.

## 3. Card overview

First-reading kinds: env, stale-test, retired, redundant, product-bug (suspected), flaky, unknown. "Route" is N (ordinary), X (coupled reasoning) or S (correctness, data safety, security). Size is engineering days.

### CI singletons (release/15/main, unit ubuntu/mac, sandbox)

| Card | Title | IDs | First-reading kind | Route | Days |
| --- | --- | ---: | --- | --- | ---: |
| CI-1 | Precut-v31 and shot-layering fixture digests and hashes | 8 | unknown (suspected stale fixture) | X | 1.5 |
| CI-2 | Clip and forward-created expectations that predate `blendMode` | 5 | stale-test (inferred) | N | 0.5-1 |
| CI-3 | Legacy formats and routes: v28 inline spec, legacy timeline write, v31 migration | 4 | retired (candidates) | N | 0.5 |
| CI-4 | R0 install-boundary rollback acceptance | 3 | retired (candidate) | N | 0.5 |
| CI-5 | Bootstrap stale-owner messages (unit-mac; sandbox side) | 5 | stale-test (mac); unknown (sandbox) | N | 1 |
| CI-6 | Diagnostics and operator lifecycle messages | 3 | unknown | N then X | 1 |
| CI-7 | Fail-closed rejections, credentials and fresh-state polling | 6 | unknown (product-bug suspected) | S | 1.5 |
| CI-8 | Timeline commit authority: sqlite authorizer, verified media, CAS, producer checkpoint, recorder bindings | 7 | unknown (product-bug suspected for verified media) | S | 2 |
| CI-9 | Gates and harness: skip policy, rename audit, `check_it.py` | 3 | env (check_it); stale-test (skip registry); unknown (rename review) | N, rename review S | 0.5 |
| CI-10 | Test doubles and spec dedup | 2 | stale-test (double); unknown (dedup) | N | 0.25 |

Sizing: the brief asks for about ten IDs per card. Exceptions, each one change: N-3 (20, one deleted file), N-4 (15, one parametrised test function).

### Nightly (main run 45166036353, job `integration`)

| Card | Title | IDs | First-reading kind | Route | Days |
| --- | --- | ---: | --- | --- | ---: |
| N-1 | Commit crash: host-boundary and real process death (`test_timeline_commit_crash.py:78`) | 12 | unknown (shared fixture root with CI-1) | X | 1.5 |
| N-2 | Commit crash: retained-input process death (same root as N-1) | 12 | unknown (same) | X | 1 |
| N-3 | Legacy certification, M1 captures (`test_snapshot_legacy_certification.py`) | 20 | **retired (prune candidate)** | N | 0.5 |
| N-4 | History: inputs changed after ancestor check (`test_timeline_history_assembly.py:300`) | 15 | unknown (product-bug suspected) | S | 2 |
| N-5 | History: other unverified-dependency and lookup refusals (`:359`, `:398`, `:172`, graph lookup) | 12 | unknown (product-bug suspected) | S | 1.5 |
| N-6 | Process control: strict versus sandbox (`platform.py:1226`) | 6 | env | N | 0.5 |
| N-7 | Visual fields: provider acceptance and refusals (`test_timeline_visual_fields.py`) | 7 | unknown (contract drift with Agent) | X | 1 |
| N-8 | Visual refusals before publication (`test_timeline_commit_integration.py`) | 7 | unknown (contract drift with Agent) | X | 1.5 |
| N-9 | Native clip replacement (`test_timeline_clip_replacement.py`) | 6 | stale-test (3 regex IDs); unknown (2 IDs) | N then X | 1 |
| N-10 | Historical render admission (`test_render_historical_admission.py`) | 7 | unknown | X | 1.5 |
| N-11 | Capture candidate binding (`test_capture_candidate_binding.py`) | 6 | unknown | X | 1.5 |
| N-12 | Legacy word anchor refused by Agent (`native_word_anchor.py:172`), plus two related | 9 | stale-test or retired (C4) | X | 2 |
| N-13 | Corrupt local timing cache; migrated realm needs provider registration | 4 | unknown (cache); env (registration, shares CI C2 root) | N then X | 1 |
| N-14 | Contract and CLI drift: schema digest pin skew, public CLI 410, saved-revision hydrate | 4 | env (digest); unknown or retired (410) | N | 1 |
| N-15 | Timeline repair, redo, mixed helper undo, source identity (WAL and foreground) | 10 | unknown | X | 2 |
| N-16 | Update jobs: sibling `../astrid-agent` assumption (`test_update_jobs.py:1058-1078`) | 3 | env | N | 0.5 |
| N-17 | Launch and pack fixtures: moved function, removed Darwin knob, pack IndexError | 4 | stale-test (2 IDs); unknown (2 IDs) | N | 1 |

Dependencies: N-1 and N-2 share the precut root with CI-1 (one fix, dispatched once). N-13 shares the provider-registration root with CI C2 (`daemon.py:320`), which is in another helper's scope. N-7 and N-8 both test visual refusals, so one may be redundant after the other is decided.

## 4. Card details

### CI-1 Precut-v31 and shot-layering fixture digests (8 IDs)
- Repo: astrid-runtime. Files: `tests/test_precut_variants.py` (3, `:117` assert False), `tests/test_precut_realm_fixture.py` (1, `:97` hash mismatch), `tests/test_shot_layering_fixture.py` (1, `:97` hash mismatch), `tests/test_direct_render_admission.py` (2, `backup.py:481` "realm failed integrity checks"), `tests/test_restore_history_fixture.py` (1, same).
- Evidence: the fixture is the committed `tests/fixtures/precut-v31.tar.gz` and its pins, loaded by `tests/precut_realm_fixture.py:19-37` (schema 31, `FIXTURE_LABEL`). The current schema is 33 (`runtime_protocol/store.py:46`). The message is a hash mismatch, not a version error, so the fixture or its pins have drifted from what the Runtime now writes.
- Kind: unknown (suspected stale fixture). Confidence: inferred from messages and layout; not reproduced.
- Fix: regenerate or re-pin the fixture from the same backup code path, as a test-data change with the provenance recorded. Do not weaken the integrity check (`backup.py:481`).
- Scope: `tests/fixtures/precut-v31*.tar.gz` and `tests/precut_realm_fixture.py` (pins). Do not change `runtime_protocol/backup.py`.
- Proof: `pytest -q tests/test_precut_variants.py tests/test_precut_realm_fixture.py tests/test_shot_layering_fixture.py tests/test_direct_render_admission.py tests/test_restore_history_fixture.py`, plus the hosted run.
- Route X, 1.5 days. Deps: N-1, N-2. Open question: is the committed archive authentic (regenerated by the owner's tool), or should it be re-captured?

### CI-2 Clip and forward-created expectations that predate `blendMode` (5 IDs)
- Files and IDs (cluster numbers): `test_timeline_forward_created_authority.py:124` (C32); `test_timeline_legacy_authority.py:476` (C34) and `:522` (C35); `test_timeline_recorder_abi_authority.py:216` (C36, `assert False`) and `:233` (C37, `assert N == N`). Total 5.
- Evidence: the actual output contains `blendMode` (`[{'blendMode'...}]` against `[]`). `2d49061` "Add timeline appearance edit fields" (2026-11-16 17:38 +0000) is an ancestor of `release/15/main`, so it postdates the expectations that omit the field. Confidence: inferred; to be stale-test under triage rule 2, the test's last change must predate `2d49061` (not checked per file).
- Kind: stale-test (inferred). The two `assert False` / `N == N` rows (`:216`, `:233`) need a read before they are grouped.
- Fix: update the expected lists to the appearance fields that `2d49061` defines.
- Proof: `pytest -q tests/test_timeline_forward_created_authority.py tests/test_timeline_legacy_authority.py tests/test_timeline_recorder_abi_authority.py`.
- Route N, 0.5-1 day. Deps: none.

### CI-3 Legacy formats and routes (4 IDs; prune candidates)
- `tests/test_spec_reference.py` (C27, `runtime_protocol/v33_manifest.py:111`): a v28 inline spec migration. Retired under D5 ("older formats") unless v28 was a published release.
- `tests/test_spec_reference.py:323` `test_parent_receipt_compaction_preserves_publication_integrity` (C28, `service.py:467`, "legacy timeline writes are retired; submit EditCommands through commitTimeline"): the test drives the retired legacy path. Its fix is to **assert the refusal** (retired route), not to delete it (rule 3, retired row).
- `tests/test_timeline_commit_acceptance.py:847` and `:866` (C29, C30): v31 schema-migration and "legacy v31 fixture remains a distinct migration source" tests. Retired under D5 if v31 was not a published release. Owner question.
- Kind: retired (candidate). Confidence: inferred from the message (the test body was not read in full). The retirement source: D5 in Plan 91 `inputs.md:85`, and Plan 39 `p39-inputs.md:52`/`:57` R-h ("Tests still driving the retired legacy timeline writer ... stale. A 200 where 410 is expected would be a bug", RT4).
- Fix: delete the v28 and v31 tests with citation to D5; convert the C28 test to assert `RetiredRouteError` (or 410 `retired_route`) at the route.
- Scope: `tests/test_spec_reference.py`, `tests/test_timeline_commit_acceptance.py` (two functions).
- Proof: deleted IDs listed with citation; the refusal test passes; X reviewer reads the list.
- Route N, 0.5 day. Open question: which schema was the last published release (D5 needs it for v31).

### CI-4 R0 install-boundary rollback acceptance (3 IDs; prune candidate)
- `tests/test_v33_protected_acceptance.py:33` `R0 = "6d53a190..."`, `:79` "immutable R0 scene", `:112` labels R0, R1, M32. The failing IDs are the R0 rollback full-set case (`test_V33_ACTUAL_R0_ROLLBACK_FULL_SET_BEFORE_EXECUTABLE_LAUNCH`, unit-ubuntu, `:627` "RN daemon did not report startup" x2, `:653` x1).
- Kind: retired (candidate). D5 names "the R0 and R1 install boundaries" as retired. Plan 91 `inputs.md:85` is the source.
- Fix: delete the R0 rollback case with citation; keep any refusal the user could reach.
- Proof: list of deleted IDs; the remaining `test_v33_protected_acceptance.py` cases pass.
- Route N, 0.5 day. Open question: is R0 a "previous published release" the owner wants supported? Default per D5: no.

### CI-5 Bootstrap stale-owner messages (5 IDs; unit-mac, plus sandbox)
- `tests/test_bootstrap.py::StaleOwnerTests` (`test_down_reclaims_reused_pid_without_signalling`, `test_reused_pid_birth_change_before_manager_refuses`, `test_reused_pid_cleanup_waits_for_fenced_manager`, `test_up_reclaims_reused_pid_without_signalling`, `test_up_reclaims_stale_lock_without_discovery`).
- Evidence: unit-mac messages expect "reused process identity changed" and "manager failed", but the product now says "Runtime interruption refused: owner endpoint or process identity failed validation." (`astrid_runtime/bootstrap.py`). That wording came in with `ee28cd6` (2026-11-01 "preserve live runtime discovery and verify recovery") and `4456b61` (2026-11-04 "Run installer stop callback inside Runtime fence").
- Kind: stale-test (mac, inferred: the product fails closed, a stronger behaviour). Sandbox side: no traceback, needs the junit line.
- Fix: update the expected messages and the reclaim expectations to the verified-identity behaviour; keep the refusal assertions.
- Route N, 1 day. Dep: sandbox owner for the sandbox side.

### CI-6 Diagnostics and operator lifecycle messages (3 IDs)
- `tests/test_diagnostics.py:110` ("Last update result: Updated to release N." absent; output says "no installer run recorded"), `:211` (expects "rolled_back"), `tests/test_operator_lifecycle_sol_closures.py:208` (expects a busy headline; gets None).
- Kind: unknown. The likely cause is a fixture that never writes the installer journal (env), but it is unconfirmed.
- Fix: diagnose for up to two hours (triage rule 6 "unknown"); then route to env or product.
- Route N then X, 1 day.

### CI-7 Fail-closed rejections, credentials and polling (6 IDs)
- `tests/test_production_worker_credentials_luna.py` (2, `runtime_protocol/daemon.py:183`, `'NoneType' object has no attribute 'store'`: the daemon is not started before the bearer rotation). Security: worker bearer rotation before HTTP start.
- `tests/test_root_generation_query.py` (2, `store.py:4619` "unsupported settlement effect_type"; the malformed kind is expected to refuse, not raise).
- `tests/test_imported_media_catalog.py:227` (1, "DID NOT RAISE ConflictError" on permission and size rejections).
- `tests/test_fail_closed_g28.py:61` (1, sandbox only: "failed" == "queued").
- Kind: unknown (product-bug suspected for the rejections). Route S, because these are credentials, data-safety and fail-closed paths.
- Fix: diagnose the daemon ordering and the refusal paths; fix the product if small, otherwise an X check and an issue (D6).
- Proof: the four files above.
- Route S, 1.5 days.

### CI-8 Timeline commit authority (7 IDs)
- `tests/test_shot_composition_runtime.py` (1) and `test_timeline_recorder_abi_authority.py` (1): "fork native binding schema changed" (`astrid/core/timeline/authoring_bundle.py`, Agent) and "CommitRejected: revision content digest mismatch" (`service.py:3421`).
- `tests/test_timeline_commit_acceptance.py` (2): `sqlite3.DatabaseError: not authorized` at `timeline_commit_execution.py:498` (an authorizer refusal, possibly a missing grant or env).
- `tests/test_timeline_producer_checkpoint.py` (C33, 1): "managed output association conflicts with existing immutable output" (`runtime_protocol/store.py:6110`). Unknown until read.
- `tests/test_timeline_text_legacy_custody.py` (1): CAS "failed hash verification" (`cas.py:217`) on a corrupt legacy reuse; the test expects a different refusal (unconfirmed).
- `tests/test_timeline_verified_media.py:98` (1): "a metadata read must not request mutation admission". The product routes a read through mutation admission.
- Kind: unknown; `verified_media` is the product-bug candidate. Route S (commit outcome, custody, data safety).
- Fix: diagnose; for `verified_media`, an X check that a read requesting mutation admission is a real defect.
- Route S, 2 days.

### CI-9 Gates and harness (3 IDs)
- `tests/test_skip_policy.py:264` (1): "mark the test with an entry from tests/lanes.py instead of skipping by hand: test_deadline.py:N ...". The Plan 39 ceiling (`p39-inputs.md:152`, D10) fixes the 16 gate sites; the test fails on any unlisted site. Kind: stale-test (registry), route N: list the site in `tests/lanes.py` or remove the hand skip (never add to a list that only grows).
- `tests/test_rename_semantics.py:22` (1): `found == allowed`. `astrid_runtime/workspace_copy.py:298` (`os.rename(copied_realm, target_realm)`) is not in the allow-list. Kind: unknown (a new raw rename needs review, not a test edit). Route S for the review: the rename must target a fresh destination.
- `check_it.py::test_gap` (1 ID across unit-mac, unit-ubuntu, sandbox): `tests/test_skip_guard.py:72-93` builds a synthetic gap and asserts the XPASS text, so the ID is a nested pytest output line parsed as a failure. Kind: env (harness parser). Proof: the junit XML `testcase` list in the unit and sandbox artifacts. Route N, 0.5 day.

### CI-10 Test doubles and spec dedup (2 IDs)
- `tests/test_timeline_commit_sequential_verifier.py` (C31, 1): reads `db_path` from a `types.SimpleNamespace` double (`runtime_protocol/timeline_commit_store.py:375`). Stale double, route N.
- `tests/test_spec_dedup.py:57` (1): `assert N == N` in offline migration and compaction of duplicate render specs. Unknown until read. Route N.
- Route N, 0.25 day.

### N-1 and N-2 Commit crash (24 IDs in `tests/test_timeline_commit_crash.py`: N-1 12, N-2 12)
- N-1: host-boundary first capture (3 transcript in nightly C1, 3 config in nightly C7) and real process death at acceptance (6, C1). N-2: retained-input process death (12, C1).
- Evidence: `test_timeline_commit_crash.py:78` `assert identity["version"] == 31` inside `_migrate_duplicate_realm`, after `inspect_canonical_schema`. The fixture docstring says "schema 31 / pre-cut" (`tests/timeline_commit_film_fixture.py:31`). The product is schema 33 (`store.py:46`). The message is a version assertion, so the duplicate restored from the archive is no longer at 31 when the test checks.
- Kind: unknown (shares the precut root with CI-1). Route X, 1.5 days (N-1), 1 day (N-2). Deps: CI-1. The C7 config IDs also hit the v33 fence (`v33_lifecycle.py:300`), which the C7 owner should confirm.
- Proof: `pytest -q tests/test_timeline_commit_crash.py -m integration` on a hosted run (needs `requires_posix_process_groups`, so not the Windows worker).

### N-3 Legacy certification, M1 captures (20 IDs, retire)
- File: `tests/test_snapshot_legacy_certification.py` (pytestmark integration). Constants: `RUNTIME_M1 = 4bb1d0f7...` (`:21`) and `AGENT_CAPTURE = 321cef4b8c89a4a938cb9ede41ba6a5444cf1b62` (`:22`). The test archives both (`:48-58`) and fails at `:37` when `git archive 321cef4b` fails.
- Evidence: GitHub API `commits/321cef4b...` returns **422 "No commit found for SHA"** (unfetchable from the public history). The nightly's step "Check historical Agent archive input" warns about it (`nightly.yml`, the `HISTORICAL_AGENT_SHA` step). The Runtime M1 commit `4bb1d0f7` is dated 2026-10-20 (merge of `tl/rt-m1-null-speed-retained-read`), before Release 12 (Agent D8, 10 Nov).
- Kind: **retired** (prune candidate). Source: the Agent Plan 91 decision D12 (Hannah, 24 Nov 2026): "restoring projects from before Release 12 is not needed (we have no users rn)" and the tests are retired under D5 (`plans/91-agent-main-green/inputs.md`, D12 row). D5 itself: "tests that rebuild a historical commit's state ... historical commits ... are retired" (`inputs.md:85`).
- Confidence: verified (the SHA is unfetchable and the test names the historical captures) for the fetch failure. The retirement is inferred from D5/D12 and must be ratified for the Runtime by the owner, because D12 is an Agent decision.
- Fix: delete `tests/test_snapshot_legacy_certification.py`, citing D5 and D12; remove the nightly warning step only if no other test uses `321cef4b` (check `tests/`).
- Proof: deleted IDs listed (20); the nightly no longer fails on this file; if any user path accepts M1 captures today, add a refusal test instead (D5 rule), which needs the owner's answer.
- Route N, 0.5 day.

### N-4 History: inputs changed after ancestor check (15 IDs, one parametrised test)
- `tests/test_timeline_history_assembly.py:300` (`test_provider_refuses_inputs_changed_after_ancestor_check`, 15 cases: abi, closure, deleted-row, event, file, ledger, metadata, owner, parent, pin, queued-cycle, realm, records, sequence, source collection). The test mutates a row after `_verify_accepted_record` and expects `RuntimeErrorBase`; it gets none ("DID NOT RAISE").
- Kind: unknown (product-bug suspected: a fail-closed check that no longer refuses a post-check mutation). The test is a real TOCTOU check, and it is not stale-looking.
- Fix: an X check first: confirm whether the provider now reads through a memo that the mutation misses (`clear_replay_memo`, `commits.verification_scope`). If the product is wrong, fix it (S route). If the memo makes the read safe, the test needs a new assertion, not deletion.
- Route S, 2 days. Scope: `astrid/...`/`runtime_protocol/timeline_commit*.py`, not the test file, unless the check is stale.
- Proof: `pytest -q tests/test_timeline_history_assembly.py -k after_ancestor` on hosted CI.

### N-5 History: other refusals (12 IDs)
- `test_timeline_history_assembly.py:359` (6 "retained inputs changed after check": config and transcript binding, content, link), `:398` (1, "mutation after dependent history reads [head]"), `:172` (2, "unverified dependencies cannot escape the graph": indirect-cycle, queued-row), and C14 (3, `test_provider_history_lookup_authenticates_each_graph_node_once[2|4|8]`, `set() == {txn...}`, `service.py:3325`).
- Kind: unknown (product-bug suspected, same family as N-4). Route S, 1.5 days. Dep: N-4 (decide the family once).

### N-6 Process control: strict versus sandbox (6 IDs)
- `tests/test_runtime_boundary.py` (5: `test_down_without_discovery_cannot_report_live_owner_stopped[False|True]`, `test_failed_candidate_pid_alias_cannot_retire_live_publication`, `test_foreign_pid_observation_cannot_reclaim_live_publication`, `test_separate_failed_start_preserves_live_discovery`) and `tests/test_astrid_product_down.py::test_down_waits_for_selected_generic_host_exit` (1).
- Evidence: `runtime_protocol/platform.py:1219-1226` fixes the mode once and raises "process control is already strict; refusing to change it to sandbox". `tests/conftest.py:25-41` sets sandbox only when `--process-control=sandbox` is passed. The sandbox job runs `tests/seccomp/run-suite.sh` (`ci.yml:361`). The nightly command has no flag (`nightly.yml`), so the process stays strict. `tests/test_runtime_boundary.py:730` writes a "sandbox" setting.
- Kind: env (the nightly lacks the sandbox mode these tests assume). Confidence: inferred; not run.
- Fix: run these tests in the mode they expect (the owner decides whether they belong to the sandbox job), or give them a subprocess so the process-wide mode is not shared. Do not change `configure_process_control` (its one-way fix is deliberate).
- Scope: `nightly.yml` (or the test subprocess), `tests/test_runtime_boundary.py:730`.
- Proof: the nightly (dispatch) on these files; the sandbox job still passes.
- Route N, 0.5 day.

### N-7 Visual fields provider (7 IDs; `tests/test_timeline_visual_fields.py` 6, `tests/test_timeline_commit_integration.py:308-318` 1)
- Test IDs: `test_visual_field_provider_acceptance_and_refusal_regressions` (`:98` 'None' == 'type-on'), `test_visual_field_provider_preserves_opaque_custom_data`, `test_visual_fields_on_audio_track_are_refused_before_publication` (`:114`, 3 cases), `test_supported_top_level_type_on_retains_original_roundtrip_expectations` (`:98`), and `test_agent_written_visual_fields_validate_and_read_back_from_published_revision` (commit_integration).
- Evidence: the Agent pin rejects `durationFrames` in entrance and exit (`astrid/core/timeline/clip_fields.py:298` "has unknown key ...; allowed: type, duration"). The Runtime tests send `durationFrames` for entrance (`tests/test_timeline_commit_integration.py:308-318`, `:416`). The Agent accepts `durationFrames` for transitions (`clip_fields.py:389-392`). Both sides are in the tree, so this is a contract disagreement, not a simple stale test.
- Kind: unknown (Agent-contract drift). Route X: an Agent-side ruling on which keys entrance and exit accept.
- Dep: N-8 (the same contract). Open question for owner: is `durationFrames` valid for entrance or exit?

### N-8 Visual refusals before publication (7 IDs; `tests/test_timeline_commit_integration.py`)
- `test_unsupported_visual_fields_refuse_before_publication` (`:443`, 4 cases: entrance value0-2, transition value3), `test_agent_provider_refuses_top_level_type_on_without_publication` (`:415`), `test_agent_provider_refuses_animation_in_unsupported_phase_without_publication` (`:426`), `test_visual_candidate_is_refused_before_publication_when_builtin_phase_is_unsupported` (`:467`). All "DID NOT RAISE RuntimeErrorBase".
- Kind: unknown (Agent-contract drift). The Agent now accepts top-level `type-on` and some phases, so the refusal no longer happens.
- Fix: decide per phase with the Agent ruling (N-7), then update or keep each refusal. Possible overlap with N-7 (visual refusals): decide redundancy after.
- Route X, 1.5 days.

### N-9 Native clip replacement (6 IDs; `tests/test_timeline_clip_replacement.py`)
- `:305` (2: atomic CAS and exact replay, and public HTTP route; both `{'clips'...} == {'clips'...}`), `:394` ("merged" == "rebased" for a disjoint intervening edit), `:470`, `:499`, `:550` ("Regex pattern did not match", 3).
- Evidence: the R-b hard-coded path that CI had at `:96-106` is gone; the file now uses `astrid_checkout()` (`_native_agent_source`).
- Kind: stale-test for the three regex rows (error wording changed; inferred); unknown for `:305` and `:394` (`merged` vs `rebased` is a behaviour question).
- Fix: update the regexes to the current messages (after reading the product text); decide "merged" vs "rebased" with the owner (rebase is the documented rule for disjoint edits, if the docs say so).
- Route N for the regexes, X for `:305`/`:394`; 1 day total.

### N-10 Historical render admission (7 IDs; `tests/test_render_historical_admission.py`)
- `:257` (1, reason 'r...' vs 'publication_id'), `:357` (4, retained integrity checked before any publication: custody, missing, same-size, size), `:404` (1, "DID NOT RAISE ConflictError" for archived timeline), and `runtime_protocol/store.py:3218` KeyError `required_bytes` (1, `[storage]` case).
- Kind: unknown. Route X, 1.5 days. Proof: `pytest -q tests/test_render_historical_admission.py` (hosted).

### N-11 Capture candidate binding (6 IDs; `tests/test_capture_candidate_binding.py`)
- `:360` (4, `test_real_candidate_reaches_verified_host_without_mutating_inputs`: parent/child, inline/ref; the assertion compares an authority dict with a ref dict), and `test_real_structural_drafts_keep_certification` (2, "shot item source is unavailable", `astrid/sdk/timeline/_command_state.py:324`, Agent).
- Kind: unknown. Route X, 1.5 days. Dep: none, but the Agent pin is involved.

### N-12 Legacy word anchor (9 IDs; C4 7 + C36 1 + nightly C7 1)
- C4 (7): `test_timeline_commit_restore_integration.py` (3: `tampered-child`, retained inputs `[config]` and `[transcript]`), `test_timeline_commit_input_integration.py` (2, `retained_input_real_move_inverse_replay_after_restart`), `test_timeline_projection_occupancy.py` (1), `test_shot_candidate_promotion.py` (1). Message: "TimingCompileError: legacy word anchor is missing" (`runtime_protocol/service.py:3282`).
- Evidence: the Agent refuses legacy word anchors with no authorized source binding (`astrid/sdk/timeline/native_word_anchor.py:172`; `astrid/sdk/timeline/_commit_timing_validation.py:305-306`: "Child legacy word anchors have never had an authorized source binding"). The tests build such anchors.
- C36: `test_shot_candidate_promotion.py::test_catalog_promotion_preserves_accepted_film_and_retries_before_live_guards` (ConflictError "provider registration is required", `service.py:885`): the same registration family as N-13.
- C7 (declared-media, `test_timeline_commit_restore_integration.py`): the v33 fence (`v33_lifecycle.py:300`), owner of CI/nightly C7.
- Kind: stale-test or retired (C4), since the Agent's rule is explicit. Route X (the tests might be the legacy form; deciding "retired" vs "fix the fixture" needs an X reader). Size 2 days.
- Open question: are legacy word anchors a retired format under D5? If yes, the 7 C4 IDs are retire-candidates.

### N-13 Corrupt cache and provider registration (4 IDs)
- `tests/test_timeline_commit_input_integration.py:315` (2, `test_move_from_corrupt_local_timing_cache_conflicts_without_writes`, status 'c...' vs expected conflict; unknown), and `tests/test_timeline_commit_restore_integration.py` (2, `history-http`, `stale-head-http`: "migrated realm requires fresh Timeline provider registration before readiness", `daemon.py:320`).
- Kind: unknown (cache); env (registration). The `daemon.py:320` root is the same as CI C2 (other helper). Route N then X, 1 day.

### N-14 Contract and CLI drift (4 IDs)
- `tests/test_timeline_ordinary_http.py:64` (1, `test_ordinary_http_empty_bootstrap_must_be_reachable`): the Runtime `runtime_protocol/contract_metadata.py:5` digest is `sha256:9c9e74...`; the pin's Agent `astrid_runtime_client/contract_metadata.py:6` is `9628bb...` (pin `0e1543e0`) and `2c6a76...` at Agent release/15/main head. The test's first assertion (`:61`) compares client and runtime digests, and the failure at `:64` shows the Agent generated file does not name the Runtime digest. Kind: env (pin skew). Fix: a pin decision for the owner (the nightly comment says never modify the fixture pin); do not edit the digest in tests.
- `tests/test_timeline_public_s2_mixed_cli_journey.py` (2): `literal-media` (HTTP 410 Gone from `workspace_client.py:295`) and `historical-audio` (the strict xfail at `:230-236` expects `HistoricalAudioCaptureGap`, but gets a `ConflictError`). `literal-media`: unknown or retired (410 is a retired-route answer; inferred).
- `tests/test_spec_reference.py::test_visualize_task_hydrates_exact_saved_revision_and_refuses_missing_source` (1): "canonical capture projection provider is unavailable" (`capture_validation.py:124`). Unknown.
- Route N for the digest and the xfail, X for the rest. 1 day.

### N-15 Timeline repair, redo, mixed undo, source identity (10 IDs)
- `tests/test_foreground_authoring_integration.py` (1) and `tests/test_runtime_nine_track_wal_reopen.py` (3, `[backfill|control|truncate]`): "untracked source directory is unsupported" (`runtime_protocol/source_identity.py:141`). Unknown (fixture creates an untracked directory, or the product now refuses it).
- `tests/test_timeline_absent_head_repair_integration.py` (2, `[absent|null]`, schema dict mismatch), `tests/test_timeline_commit_integration.py` (2, `test_real_mixed_helper_commit_undo_is_exact_or_refuses_overlap` `[immediate|later-overlap]`, `'NoneType' has no attribute 'client'` at `astrid-agent/astrid/sdk/timeline/commit_session.py:496`), `tests/test_timeline_commit_acceptance.py` (1, "realm failed integrity checks", `backup.py:481`), `tests/test_timeline_redo_restoration_boundary.py:153` (1, "DID NOT RAISE CommitRejected", redo requires exact source restoration).
- Kind: unknown. Route X, 2 days. Each sub-cause is different; split at dispatch if the reproduce step confirms two causes (rule 6).

### N-16 Update jobs, sibling Agent path (3 IDs)
- `tests/test_update_jobs.py::test_authenticated_update_route_runs_selected_agent_platform_adapter[darwin|linux|win32]`, `:1078` `assert Path(agent_update_job.__file__).is_relative_to(agent_root)`. The test sets `agent_root = helper_path.parents[2]` where `helper_path = Path(__file__).parents[2] / "astrid-agent" / ...` (`:1058-1078`): a sibling of the runtime checkout, which CI does not provide (CI uses `$GITHUB_WORKSPACE/astrid-agent`). The Agent file exists at the pin (`astrid/installer/update_job_platform.py`), so the failure is the import location check.
- Kind: env (path assumption). Route N, 0.5 day. Fix: take the Agent root from `astrid_checkout()` (the same helper other tests use), not a sibling path.

### N-17 Launch and pack fixtures (4 IDs)
- `tests/test_verified_host_launch.py:431` (1, KeyError 'source_checkout_closure'): the test extracts `source_checkout_closure` from the Agent's `astrid/core/execution/generic_host.py`. The pin's file has no such function (only `_canonical_digest` at `:1846`). The function now lives in `runtime_protocol/verified_host_launch.py:171`. Kind: stale-test (moved; source is the file itself, commit not dated). Fix: read it from the Runtime module.
- `tests/test_astrid_activation_join.py:837`/`:846` (1): `assign(custody, "DARWIN_CUSTODY_SOCKET_PARENT", ...)` on `astrid_runtime.custody_broker`; the attribute no longer exists in the product (grep finds only the test). Kind: stale-test. Fix: remove the assignment or the test case, citing the removal.
- `tests/test_runtime_pack_startup.py:62` (1, IndexError) and `:128` (1, `assert N == N` restart with persisted admissions). Unknown.
- Route N, 1 day.

### Pointers (not carded here)
- Portability (7 nightly IDs): `tests/test_portable_lifecycle.py` (5: `:455`, `:409`, `:638`, `:684`, and a foreground test) and `tests/test_profile_services.py` (2: `:887`). Hand to the portability helper.
- R-b (1 nightly ID): `tests/test_wc10_installed_launcher.py:26` `AGENT_SOURCE = /home/user/work/wt/agt-pin-6efc8150`. Hand to the R-b helper.

## 5. Prune candidates (retired or redundant under the support line)

| ID(s) | Card | Verdict | Citation | Owner question |
| --- | --- | --- | --- | --- |
| 20 IDs, `test_snapshot_legacy_certification.py` | N-3 | retire | D5 (`plans/91 inputs.md:85`), D12 (Agent, 24 Nov 2026), `321cef4b` unfetchable (GitHub 422), M1 commit 2026-10-20 | Ratify for Runtime; is M1 before the last published release? |
| 3 IDs, R0 rollback in `test_v33_protected_acceptance.py` | CI-4 | retire | D5 names "the R0 and R1 install boundaries" | Was R0 published? (default: no) |
| 4 IDs (v28 inline spec, legacy write route, v31 migration x2) | CI-3 | retire (C28: assert refusal, not delete) | D5; Plan 39 R-h (`p39-inputs.md:57`, RT4) | Which schema was the last published release? |
| 7 IDs, legacy word anchor (C4) | N-12 | retire candidate | Agent `_commit_timing_validation.py:305` (no authorized binding ever) | Is the word-anchor form a retired format? |
| 1 ID, `literal-media` HTTP 410 | N-14 | retire candidate (inferred) | `workspace_client.py:295` | Does a user reach this route? |
| 1 ID, `test_astrid_activation_join` DARWIN knob | N-17 | stale-test (removed attribute) | grep: no product definition | none |
| 1 ID, `test_verified_host_launch` | N-17 | stale-test (moved function) | `verified_host_launch.py:171` | none |

Redundant candidates (not proven, need a read): N-7 and N-8 both test visual-field refusals before publication; the covering test must be named before either is deleted (rule: "naming the passing test ID").

## 6. Dispatch and proof recipe

1. Dispatch Nightly on `release/15/main` at `24e2c929` (`gh workflow run nightly.yml --repo banodoco/astrid-runtime --ref release/15/main`). This is a manager action; I did not run it.
2. Proof for each card: the hosted run on the card branch, with the `repeat` input where the cause is flaky. The local worker env runs Python 3.13 and cannot reproduce some Linux-only tests (`requires_posix_process_groups`).
3. Before deleting any ID from section 5, list it with its citation and have an X reviewer read the list (rule 3).

## 7. Could not verify

- I did not run any test, reproduce any failure, or read full test bodies for CI-2, CI-6, CI-7, CI-8, CI-10, N-4 to N-15. Their kinds are first readings from messages, file lines and the product code cited.
- Kinds marked "inferred" rest on message text and file layout, not on a diff against a passing commit.
- Commit dates for `2d49061`, `ee28cd6` and `4456b61` are from `git log` on `FETCH_HEAD`; I did not check when each test file last changed (rule 2 needs that).
- Whether the sandbox job (`tests/seccomp/run-suite.sh`) passes `--process-control=sandbox` was not read; I cited only the `ci.yml` line that invokes it.
- Whether M1 and R0 were published releases: I did not find a Runtime release list (the releases API returned nothing) and did not check tags. Both retirement calls depend on that.
- The `check_it.py` ID: I did not read the junit XML, so the "nested output" explanation is inferred from `tests/test_skip_guard.py:72-93`.
- The Agent pin contract digest mismatch (N-14) is read from two generated files, not from a rebuild.
