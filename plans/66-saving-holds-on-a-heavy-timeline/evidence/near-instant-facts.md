# Facts for the near-instant fixes (Haiku readers, 18 Nov; spot-checked by the main thread)

Plan and decisions: `plan-near-instant-commits.md` (Rev 2). Review: `fable-near-instant-review.md`. Profile: `sonnet-commit-profile.md`.

## Runtime (the code lives on `release/14/plan-59`, not `release/14/main`)
- **`release/14/main` (`2537fed`) does not contain `519b404`.**
  - `_confirm_object` and `history_read_scope(final=...)` came in with plan-59's merge `519b404`, "Merge p59/revision-listing-perf: history reads confirm each object once per pass", via task commit `93f198d`/`dbe8d0c`, "Check history CAS bytes once per read, not once per nested boundary".
  - Its purpose was performance (cold history read on a film: 36 s → 3.3 s). The guarantee it kept: "the outermost evaluation still re-reads every consumed object before returning"; "every exit path still re-reads once before trust or commit".
  - Its tests: `test_cold_history_and_head_reads_check_media_a_bounded_number_of_times` and `test_bounded_history_read_still_refuses_changed_media_bytes`.
- **`_check_history_objects`** came in with `43407a1` (D94, verified-history state reuse; empty body). Its tests are in `tests/test_timeline_history_state.py`: `test_change_after_warm_hit_is_refused_before_return` (:124), `test_retained_warm_forgery_is_also_rejected_after_an_external_write`, `test_refusal_discards_state_and_a_new_store_always_verifies_cold`, `test_cached_legacy_closure_still_checks_physical_cas_bytes` (:431), and others.
- **`09a27ef`**, "close D94a history cache baseline race": it rechecks DB/WAL dev, inode, size, mtime and ctime inside read snapshots and after BEGIN IMMEDIATE, so "an external writer cannot be absorbed into the baseline". That's the DB side; keep it as it is. Its tests: `test_external_write_before_begin_immediate_cannot_be_absorbed`, `test_same_size_file_timestamp_change_invalidates_verified_state`, and others.
- **`6a9a98f`** added `history_read_scope`: "Recheck before authoritative results leave the existing locked port". Its tests: `test_provider_refuses_mutation_after_dependent_history_reads` and `test_provider_read_freshness_isolated_after_refusal_and_between_requests`.
- **Service verify-once map:** `service.py:641` (init), `:5399` (set on ingest), `:6031-6036` (checked by `file_identity`). The commit store doesn't use it, and no test covers it.
- **"Inputs changed" raise sites** on `release/14/main` (line numbers differ on plan-59): `timeline_commit_store.py:192, 211, 243, 421, 472, 479, 538`.
- **Fixtures:**
  - `tests/test_timeline_commit_port.py:24` has the `service` fixture and `commit()` at `:47`.
  - Build N entries with `for n in range(N): commit(service, body, key=f"k-{n}")`, as in `tests/test_timeline_commit_closure_growth.py:19-30`. `body` and `provider` come from `tests/test_timeline_commit_authentication.py`.
  - For a warm cache, use `warm()` (`test_timeline_history_state.py:32`).
- **Running tests:** `pip install -e '.[test]'`, then `python -m pytest -q <files>`. The default addopts skip integration, darwin_native and live tests.

## Agent: legacy probes (`astrid/sdk/timeline/_commit_timing_validation.py`, `_timing_evaluators.py`)
- **How legacy declarations flow.** `compile_timing` (`compiler.py:128`) validates `legacy_declarations` (`:100-110`) and then calls `evaluate` (`_timing_evaluators.py:284`).
  - The exemption is at `:541-546`: when the authored `on`/`until` text equals the legacy text, the value is set to None and skipped.
  - The unsupported-declaration check (`:525`, for `UNSUPPORTED_DECLARATIONS` at `:27-28`: sequence, sequence_fit, formulas, orphan, gap_after_s) runs **before** the exemption.
  - Declaration failures are raised at `:416` (parse), `:423-424` (word binding), `:455`/`:463` (cut anchor), `:458`, `:483-489`, `:507-508`, `:531-532`, `:571` and `:573` (an unused word binding, which may fire when a word declaration is exempted).
  - A collect mode could be a separate pre-pass running only the declaration checks (`:416-424`, `:455-463`, `:522-532`), returning `(key, field, message)`. That avoids touching graph construction.
- **History of the probe.**
  - `2ad707b7a` gates exemptions by baseline validity: "keeping valid anchors on the exact compiler path".
  - `d1d41c405` adds `_restored_legacy_exemptions`, which calls `_legacy_declaration_is_resolvable(source, …)`, for authenticated restorations.
  - `89c700ade` adds the shared-physical-image ambiguity branch, `_physical_shot_context`, `_legacy_beat_only` and `_known_unresolvable_timing_error`. Unclassified failures stay on the real path.
  - `6d190daec` doesn't touch the probe.
- **Tests pinning the probe** (none call it by name):
  - `tests/sdk/test_p1_doc_patch_provider.py`: `test_unchanged_unresolved_legacy_timing_is_retained_for_unrelated_edit`, `test_unchanged_valid_legacy_child_timing_uses_rational_compiler_result`, the beat/downbeat parametrised test, and `test_shared_physical_shots_keep_valid_beat_inputs_in_provider_timing`;
  - `tests/editing_conformance/test_authenticated_legacy_restore.py` (4 tests);
  - `tests/editing_conformance/test_commit_timing_validation.py`, `test_commit_legacy_text_reference.py`, `test_commit_boundaries_d12.py` and `test_commit_fps_d12.py`.
- **R5 signature.** `_unsupported_findings` (`_commit_timing_validation.py:486-528`) signs `json.dumps([declarations[name], row])`, where `row` is the clip minus `params`. That's why any move "touches" `gap_after_s`. `_drop_preexisting_unsupported` returns early when `baseline is None`.
  - Tests are in `tests/editing_conformance/test_preexisting_violations_scoped.py`: `test_edited_or_touched_unsupported_declaration_is_refused` is parametrised over declaration, timing and track. **Its "timing" and "track" cases pin today's whole-row behaviour and must change.** The file also has the invariant `test_invariant_every_long_lived_head_accepts_an_unrelated_commit_and_a_duplicate`, plus helpers `check`, `unrelated_change`, `_head_unsupported_declaration`, `_head_unknown_asset` and `_head_mismatched_fps`.
- **There's no `doc-a` fixture on `release/14/main`.** The corpus is `tests/timeline/test_timeline_roundtrip_corpus.py` (globs `*.timeline*.json`), `tests/sdk/test_p1_case_corpus.py` and closure fixtures `tests/fixtures/timeline_redo_media_closure_1338.json` and `tests/editing_conformance/fixtures/main_image_cap_raw_closure.json`. Never commit `almost-ready.json` content (public repo).

## Agent: loads (`astrid/sdk/timeline/commit.py`), one `clip.add-media` with base == head
- **Base:** `_load` at `:432` (one `revision_closure` each); `:1227` loads the base once.
- **`_check_reservations`** (`:730`), called at `:1398` once per CAS attempt (up to 3, `:1351-1398`):
  - `_history(port, current, None, …)` (`:661-687`) pages the full chain from genesis;
  - per entry it calls `boundary(previous)` (`:1012`) and `boundary(entry)` (`:1013`), then `boundary(entry)` **again** (`:1017`) inside `_reservation_refs(State(...))`;
  - the final `boundary(current)` is at `:1021`.
- **Total:** 2 + 3N `revision_closure` calls per attempt. Bootstrap or legacy entries with `records` None, before the first recorded entry, cost zero (`:1000-1003`).
- **Not on this path:** `scan`'s `boundary` at `:958` (only `timeline.restore`), and undo, restore or inverse paths (`:1260`, `:1281`, `:1303`, `:1314`, `:1368`).
- **The head moved:** `:1351-1352`.

## Agent: loads, safety of a memo
- `bundle_from_document` (`commit.py:154-166`) already deep-copies its input, and `open_authoring_bundle` deep-copies everything it keeps. `_load` never stores the port result. So memoising the **verified document per ref** and calling `bundle_from_document` per use is safe.
- What `scan()` mutates is the bundle's own state:
  - `State.set` (`_command_state.py:590-591`) does `bundle.clear(); bundle.update(deepcopy(closure))`;
  - `State.entity` returns live references;
  - `restore_native_fork` installs a `_CopiedShot`.
  
  So never share a bundle object between uses.
- **Reservation tests.**
  - Real-port: `tests/sdk/test_timeline_commit_graph_roots.py` (`reservation_check` at `:225`, `RuntimeRealm` at `:53`, `RuntimeHistoryPort` at `:145`; integration, needs `ASTRID_RUNTIME_CHECKOUT`).
  - Fake-port, no Runtime needed: `tests/sdk/test_timeline_commit_provider.py` (`DetachedRealm` at `:68`, `DetachedPort` at `:114`; `realm.call([...])` appends one entry; `page_size = 1` forces paging). Its tests at `:335`, `:817`, `:841`, `:870`, `:950` and `:1540` cover `identity_collision` and `history_unavailable`.
  - Semantic: `tests/sdk/test_timeline_semantic_reservations.py`, including `:169` fail-closed and `:208` "moves and deletions do not scan history".
  - `tests/sdk/test_timeline_commit_provider_runtime.py:190` monkeypatches `_check_reservations` to prove a receipt retry skips it.

## App: retry classification and the stuck state (`origin/release/14/main`)
- **`src/integrations/runtime/client.ts:319-341` `classifyRuntimeCommitFailure`.**
  - `details.reason` `head_busy` or `runtime_unavailable` gives `unknown`, which retries at any HTTP status.
  - Otherwise `details.status` `conflict` gives `conflict` and `refused` gives `refused`.
  - Otherwise a 400 or 422 gives `validation`, and a 5xx gives `unknown`.
  - In `localSaveSession.ts:265-266` and `commitSession.ts:248-249`, only `unknown` and `storage` retry. **Everything else is `rejected`**, including `conflict` and `refused`.
- **The 400 `protocol_error`** (`errors.py:83-85`) is classed `validation`, so it's rejected. `commitOutbox.ts:519-527` then marks every later dependent intent as conflict.
- **The Runtime never emits `head_busy`.** It's listed as a legacy refusal reason in `contract/commit-v2.md:1416-1419`, with 409 and `details.status: "refused"`.
- **The real head contention reason is `stale_head`** (`timeline_commit_store.py:1844`, `:2121`; `timeline_commit_port.py:674`, `:705`), sent as 409 `{code: "conflict", details: {status: "refused", reason: "stale_head", …}}`.
  - The App classes that as `refused`, so it's rejected and not retried.
  - `isRuntimeConflict` (`client.ts:295`) returns false for it, which contradicts its own comment at `:297-299`, which says the stale-head 409 should be a conflict.
  - The test at `timelineCommit.test.ts:538-541` only uses a synthetic `head_busy`.
  - **A likely real cause of stuck tabs:** any head movement, such as a second tab or an agent publish, becomes a permanent rejection.
- **Retry timing:** `useTimelinePersistence.ts:63-64`, 500 ms × 2^n capped at 8 s, unbounded. The outbox re-sends the same body and the same `Idempotency-Key`.
- **Inspector:** timing fields call `onChange` on every keystroke (`ClipPanelBody.tsx:153-157`); `onValueCommitted` only dedupes. Saves are debounced by 500 ms. **Decision: no inspector change now.** Re-check in the browser after the commit-cost fix.

## App: the traced stuck state (Haiku readers, on `wt-rejected-discharge` `a4f765fbb`; static reading, not run)
Paths are under `src/tools/video-editor/`.
- **The buttons.**
  - "Use latest version" calls `chrome.reloadFromServer()`, which leads to `useTimelinePersistence.ts:1601-1749`. That clears the conflict flags (`:1694-1697`), the pending refs, `captureFailure` and `editFailure`, and the IndexedDB draft, and sets status `saved`.
  - "Keep my changes" calls `chrome.retrySaveAfterConflict()` (`:1780-1807`). It needs the IndexedDB draft (`:1793-1802`, early return keeps the card), then calls `reloadFromServer({preserveDraft:true})`.
  - **Neither touches the commit outbox or the local save session.** `useTimelinePersistence.ts` never references `commitOutbox`, and neither button calls `resolveRejected`.
- **The persisted rejection.**
  - `commitOutbox.ts:517-527` writes `pending.outcome` and `intent.conflict` durably (IndexedDB `astrid.command-outbox`, store `owners`).
  - Only `resolveRejected` (`commitOutbox.ts:354-372`) clears it. Its only wired caller is `localSaveSession.ts:163`, for `too_large`.
  - `commitSession.ts:1213`, `:1345` (`useLatest`, `keepLabelChanges`) do call it, but `commitSession` is test-only.
- **After a reload it comes back.**
  - `localSaveSession.ts:334-337` sees the pending entry and sets `recovery`.
  - `useTimelineSave.ts:395` calls `recover` → `pump` → `rollback` → re-publishes `conflict` or `error`.
  - `useTimelineSave.ts:715-719` restores the card when the status is `conflict`.
- **The next edit is blocked.**
  - `localSaveSession.ts:341` throws "Resolve retained local saves before editing again" when the status is `conflict` or `error`.
  - `commitOutbox.ts:470-471` throws "Outbox has a rejected prefix" on dispatch.
  - `useTimelinePersistence.ts:1249` returns early while `isConflictExhausted`.
- **Which rejections show the card.**
  - A `conflict` rejection, or any rejection whose intent carries `timeline.inverse` (`localSaveSession.ts:176-187`), publishes `conflict`. The handoff (`timelineLocalSaveHandoff.ts:934`) then throws `TimelineVersionConflictError`, and `useTimelinePersistence.ts:931` → `handleConflictExhausted` (`:433-446`) shows the card.
  - A `validation` (400) rejection publishes `error`, which shows a toast and an error badge, no card. Edits are still blocked at `:341`.
- **Possible stale session document** (inferred): `localSaveSession.ts:109` keeps its own `document`, which neither button resets; only `resetToCanonical` (`:145-155`) does. `timelineLocalSaveHandoff.ts:430` refuses a capture when the session document differs.
- **Existing tests:** `commands/localSaveSession.permanentRejection.test.ts:16` (`too_large` only) and `components/TimelineEditorShellCore.test.tsx:2037-2103` (labels and the dialog).

## Constraints for every agent
- Disk is tight: 5.7 GiB free while :2400 rebuilds. Read and write code straight away, but **create no venv or `node_modules` until :2400 answers** (`curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:2400/` returns 200), then only if `df -h /` shows at least 3 GiB.
  - Use `pip install --no-cache-dir`.
  - Use one venv per repo at `/private/tmp/claude-501/-Users-hannahomalley/89e96a59-5dfa-43fb-8013-1fe9d0216757/scratchpad/venv-<repo>`. If it already exists, reuse it, since another agent may share it.
- Never touch `~/astrid-release/release-14-plan-59` (except cloning `node_modules` once it's back), the live service, `~/.astrid` or `~/.local/share/astrid`.
- Tests are focused and count-based, never timed.
- PRs are posted as AstridPseudon in team voice ("we"). Get the credential with `git credential fill` into a variable and never echo it. Use curl; `gh` isn't installed. Leave PRs unmerged.
