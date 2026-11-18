# Release 14 near-instant set: independent review

18 Nov 2026. Read-only: nothing merged, pushed or commented. Five Haiku readers listed files, line counts, tests and markers (no TODO, FIXME, skip or xfail was added in any PR). I read every diff myself. I ran the Runtime and Agent tests on scratch exports of each PR head (scratchpad, isolated HOME), plus two reviewer probes; the App tests were not run. Merge paths were simulated with `git merge-tree` on `--shared` scratch clones. `release/14/commit-loads` is not pushed (uncommitted local work), so it is skipped.

## Verdicts

| PR | Verdict |
|---|---|
| Runtime #59 `commit-cost` → plan-59 | **Merge after named small fixes** (F59-1, F59-2, F59-3) |
| Agent #394 `legacy-probes` → main | **Merge after named small fixes** (F394-1 to F394-3, plus one recorded decision) |
| App #295 `rejected-discharge` → main | **Merge after named fixes** (F295-1, F295-2). Both are deletions or moves; without them it brings back the B4 incident pattern. |
| App #296 `drop-placement` → plan-59 | **Merge after a named small fix** (F296-1) |
| App #297 `am-camera-inset` → main | **Merge.** Land poms_packs `100f388` on poms_packs main (or pin it) before publication |
| App #294 `media-association` → main | **Merge after a named small fix** (F294-1) |

## Runtime #59: CAS confirm by file identity, `head_busy`

8 files, +362/-17; production +119/-15. One commit, `975ab0f`. New test file `tests/test_timeline_commit_cost.py` (4 tests, 4 tamper cases). On the export, the new tests plus `test_timeline_history_read_cost.py` and `test_timeline_history_state.py` gave **73 passed**.

**It does what it claims for the warm path.** A warm commit and a warm history read cost 0 hashes, 0 opens, and about 14 stats per consumed object (probe: 70 stats for 5 objects). Trust lives in `RealmStore.verified_cas`, shared with the service map, and is never cleared by memo resets or refusals.

**`head_busy` reaches the App correctly.**
- `HeadBusyError` is answered with `exc.status` (409, `server.py:568`) and `details.reason: head_busy`. The App's classifier on `release/14/main` already sends `reason === 'head_busy'` to the `unknown` (same-key retry) lane (`client.ts:324`), and #295 keeps that check first.
- A refusal is never recorded for replay (`timeline_commit_execution.py` only replays a durable acceptance), so the retry really re-verifies.
- The Agent can't swallow it: `RuntimeErrorBase` derives from `Exception`, not the `ValueError`/`CommandError` that `commit.py:1018` turns into `history_unavailable`, and `commit.py:1206` catches only `ConflictError`. Subclassing `ProtocolError` rather than `ConflictError` is what keeps it out of that catch; say so in the docstring.

**Integrity: can a changed CAS file be trusted?** Not through the commit store's own path.
- Trust is recorded only when the bytes hashed to the id and `fstat` before and after the read are equal. The identity is `(dev, ino, size, mtime_ns, ctime_ns)`.
- On APFS, every write updates mtime and ctime. `utime` restoring mtime sets ctime to now, and so do `chmod`, `link` and `unlink`. An unprivileged process cannot set ctime, and a replacement is a new inode (the store never replaces; publication is a no-replace link).
- The four tamper tests (same-size rewrite, replacement, each with restored mtime) prove it.
- A process's first confirm always hashes, because the map starts empty.

Residuals, none blocking:
1. **Root-level writes.** Clock rollback, raw block-device writes and silent media corruption go undetected until the next process start. That is the same trust the database already gets.
2. **The ingest seed** (`service.py:5401`) records the published file's identity *without hashing the published bytes*; it relies on the staging stream's hash. That was already trusted for media serving, and #59 extends it to commit confirms. The window is milliseconds, inside the Runtime's own staging. Simplest close: don't seed there, and let the first confirm hash once per process.
3. **Coarse-timestamp filesystems** (FAT/exFAT external drives, some network mounts): a same-size rewrite within one timestamp tick of the trusted read could keep its identity. APFS, NTFS and ext4 are not affected.

**What it misses for "near instant": the bytes are still read after any memo clear.**
- `_history_object_value` (`timeline_commit_store.py:513`) has exactly one caller, the media pins at `:1560`, which need only `(size, sha)`. After a memo clear it still goes to `_read_history_object` → `cas.read`, which opens and reads the whole file (no hash).
- A memo clear happens on every refusal and every database write: #826, and `_sync_replay_memo` clears on any change to the version tuple.
- My probe on the PR's `film` fixture, after a refused commit and after an external DB write: **hashes 0, opens 5 of 5 consumed objects**, every byte re-read. The PR's trust test counts only hashes, so it can't see this.
- On Almost Ready that is about 1,100 media objects per commit and per history GET, the 3.9 s of `read` in the profiled GET, and the GET holds `store._mutex` the whole time.

**A "one lstat" confirm is about ten syscalls.** `_file_unchanged` and `_read_object` build a new `ContentAddressedStore` per call, and its `__init__` runs `Path.resolve()` and `mkdir(parents=True, exist_ok=True)`. The counter patches `current_identity`, so it can't see this.

**Elegance.** Good: one map, no mode, refusal sites unchanged in number. `_digest_bytes` exists only as a test seam. Pass counts weren't reduced (`final=False` for inner scopes), which is fine once each confirm is cheap.

## Agent #394: legacy probes, unsupported declarations by value

6 files, +583/-90; production +276/-83. Three commits.

**Correctness.**
- **Collect mode.** `evaluate(collect=...)` runs only the declaration-time `moment_rule` checks. `moment_rule` depends on setup built before the clip loop (`bases`, `groups`, `local_bases`, `pins`), not on earlier iterations, so the early `continue` is faithful.
- **Probes.** The compile runs first. A per-declaration probe runs only on an attributable resolve-time failure, at most once per declaration. A clean commit runs one compile and no probe.
- **Restored exemptions.** The change in `_restored_legacy_exemptions` is equivalent: that loop only reaches parent *word* declarations, where the old probe returned exactly `not _word_declaration_unresolved`.

**Acceptance changes.**
1. **R5 (planned).** Moving or re-tracking a clip with an unchanged unsupported declaration (gap_after_s, sequence, formulas, …) is now accepted; a new or changed one still refuses.
2. **The probe now drops the base's own unsupported declarations** (`d6fe2abb0`). On any base carrying one (Almost Ready does), an unchanged legacy on/until that the base can't resolve is now exempt. The old probe never exempted it, because it failed first on the unmarked "unsupported timing declaration".
   - This widens acceptance, in the direction of the #842 rule ("refuse only what the change introduces").
   - The plan said a set difference is an owner decision. **Record it as decided** (the main thread can make this call) in the decision log and the PR body.
3. Nothing else. I compared verdicts against the true pre-PR module (`release/14/main`'s `_commit_timing_validation.py`, loaded beside the new one) over the PR's 12 cases × {plain, gap_after_s, formulas} × {unrelated edit, moved clip}. 56 of 72 are identical. The 16 that differ are all refuse → accept, all on bases with an unsupported declaration, and all explained by changes 1 and 2. No case went accept → refuse, and the plain variants are all identical.

**The proof is weaker than it looks.**
- `legacy_probe_oracle.py` imports the production `_legacy_declaration_is_resolvable`, which commit 3 modified. The "old" side of the differential is therefore not the old code, and a change to the probe can't fail it.
- Every differential case is a synthetic `candidate()` variant. Fable's E.5 and the plan both asked for every corpus head.
- `test_legacy_probe_gap_after_fault.py` is exploration scaffolding. Its docstring says the fault still happens, it names the deleted `_known_unresolvable_timing_error`, it prints, and it re-implements the probe.

**Elegance.**
- Adding `collect` to `evaluate` is the shape the review asked for.
- `_failing_candidates` attributes a failure by matching the owner's tuple repr inside the error text. That's acceptable for now; long term the kernel should raise the owner and field as structure.
- Production adds more than it deletes (+276/-83).

## App #295: dischargeable refusals

10 files, +369/-5. Tests are count-based with no timers.

**Correct:**
- `discharge('latest'|'keep')` leaves the state from both buttons, including after a reload (`resolveRejected` / `rebaseRejected` on the durable outbox).
- `head_busy` stays in the retry lane, and `isRuntimeConflict` is false for it.
- Multi-owner recovery resends each owner's chain on its *original* base, so the Agent's rebase still checks intervening writes. A live tab's owner still fails to claim (`ifAvailable`), as it did before.

**F295-1: the automatic `stale_head` rebase brings back the B4 incident.** `rollback()` (`localSaveSession.ts:193`) moves the rejected chain's basis to the latest head and resends it, up to 5 times, with no user choice.
- **The premise is wrong.** Ordinary head movement never yields `stale_head`. With base ≠ head, the Agent rebases the commands itself, checking intervening writes (`commit.py:1345-1390`, `value_conflict`/`dependency_changed`).
- **When `stale_head` actually happens.** The editor's outbox gets it only from the store's accept-time race (`timeline_commit_store.py:2181`, `rowcount != 1`). `timeline.restore` also produces it, but the editor never sends that.
- **What the rebase skips.** Moving the basis to the latest head skips the Agent's intervening-write check against exactly the concurrent write that caused the race, so a same-field change by the other tab or an agent publish is silently overwritten.
- **The prior incident.** `useTimelinePersistence.ts:490-492` records it: "reloaded the remote version and re-POSTed local state, silently overwriting the other writer (the CAS-defeating bug from the incident). B4 removes it entirely". The same file says two lines below the new branch (`localSaveSession.ts:210`): "never … resend it automatically".

**F295-2: every programmatic reload now discards a retained refusal.** `reloadFromServer()` calls `discharge('latest')` whenever `preserveDraft` is unset (`useTimelinePersistence.ts:1634`). It is called after shot duplicate (`AstridTimelineEditor.tsx:380`), promote primary (`:427`), draft Discard (`useTimelineSave.ts:788`), the schema "Reload" (`TimelineEditorShellCore.tsx:875`) and `ShotTimelinePreview.tsx:363/376`.
- Scenario: an inspector edit is refused; the user dismisses the card and duplicates a shot. The duplicate's reload drops the refused change, which "Keep my changes" could have resent, with no message. **This is the one way #295 loses a user edit without the user choosing it.**
- "Use latest version" itself is an explicit discard, and 'keep' loses nothing.

Nits:
- `retrySaveAfterConflict`'s docstring ("Save as copy … never silently re-POSTed") no longer describes 'keep'.
- A validation refusal still surfaces as "This timeline changed somewhere else" on the next edit (follow-up).

## App #296: drop placement

2 files, +172/-26. Tests are count-based with no timers.

**Correct:**
- Reasons are named, logged and sent to telemetry. The tokens map to plain text through `DECLINED_DETAIL`, so the toast is not raw.
- A drop is no longer refused because the head moved or the placeholder vanished on re-adoption. Placing it at the drop time doesn't resurrect a deletion: users can't delete `uploading-*` placeholders (`useClipEditing.ts:150`), and undo carries them over (`useTimelineHistory.ts:213`).
- A different object under the same key gets its own key.
- The dropped `forceNewTrack`/`insertAtTop` and project checks are fine, since the Agent is the authority.

**F296-1: same-object reuse doesn't match the Agent.**
- **The Agent's rule.** For an existing key, `clip.add-media` requires `equal(entry, {media_id, type, generationId, variantId})`, which is exact JSON with an exact key set (`native_occurrence_media_commands.py:60-65, 140-145`). Otherwise it refuses `dependency_changed` ("existing registry binding differs from exact selection").
- **What #296 does.** It reuses any entry with the same `media_id`/`content_sha256` (`useAssetManagement.ts:348-359`) and installs that entry locally. The server then refuses, and the user gets an outbox `conflict` card instead of the earlier client toast.
- **Its own reuse test pins the refused case.** It reuses an entry carrying `file`, `content_sha256` and `extra`, exactly the shape the Agent refuses. Legacy bootstrap entries (Almost Ready's registry style) and a re-import that yields a new generation or variant both hit it.

Nit (one rule, one place): the guard now allows a selection with neither id (`:343`), but the handoff still requires all five non-empty keys (`timelineLocalSaveHandoff.ts:700-704`). That case therefore reaches a different, later refusal. Let the handoff own the selection shape.

## App #297: am-camera-inset

6 files, +113/-13.
- **Source match.** All five vendored files are byte-identical to poms_packs `100f388`, and `provenance.json` hashes match.
- **Where `100f388` lives.** It is pushed (`task/plan59-am-camera-inset`) but is not on poms_packs main. The provenance header still names only `astrid_commit ec0a9f5`, so a later vendor refresh from the Agent could revert these files (the gap already filed in QUEUE).
- **Before publication.** Land or pin `100f388` so renders and the hosted editor agree.
- **Code.** Existing integer-zoom timelines are unchanged, and the keyframe edge cases are safe. Nit: an `am-discord` first step with `ease: linear` tweens from itself, so it gives no push-in from 1×.
- **Tests.** None, which matches the no-tests-under-elements convention. Validate by stills, as planned.

## App #294: both ids or neither

6 files, +139/-10. Correct at the one planner (`planGenerationAssetRegistration`); callers pass the variant they know, and a final video carries neither.

**F294-1: a pinned image group with a variant-less image never converges.**
- **The trigger.** `primary_variant_id` is `null` whenever a generation has no primary (`generationAccess.ts:132`, `useProjectGenerations.ts:140`). #294 then writes neither id.
- **Why it never matches.** `usePinnedGroupSync` decides "in sync" by comparing registry `generationId`s (`usePinnedShotGroups.ts:228-245`, `getClipGenerationId` at `:68`). The new clip never reports its generation, so current never equals desired. The group is rebuilt, and that clip is never found for reuse.
- **Why that becomes a loop.** The effect depends on `data` (`:455`, 300 ms debounce), so it commits again after its own edit.
- **What changed.** Before #294, the half association converged locally (and the Agent refused it since #393).

## Interactions and merge order

**Text merges.** All clean (`merge-tree` exit 0):
- App: main ← #295, #294 and #297 (pairwise too); plan-59 ← #296; (plan-59 + #296) ← that main.
- Agent: main ← #394; plan-59 ← (main + #394).
- Runtime: plan-59 ← #59; (plan-59 + #59) ← main.

**Branch state.** Runtime plan-59 already contains main. Agent plan-59 is 210 commits ahead of main.

**Semantics.**
- **#59 and the App.** #59 needs nothing from #295; `head_busy` is already retried on `release/14/main`.
- **#295 and #296** share no files. A server refusal caused by F296-1 would land in #295's card, which is another reason to fix F296-1 before the browser check.
- **#394 and commit-loads.** commit-loads touches only `commit.py` and `tests/conftest.py`, so there is no overlap.
- **"Both or neither" lives in three places:** #294's planner, #296's guard and the handoff. They disagree on "neither". Follow-up: one rule.

**Order:**
1. Runtime #59 (with F59-1 to F59-3) into `release/14/plan-59`. Independent.
2. Agent #394 (with F394-1 to F394-3 and the recorded decision) into `release/14/main`.
3. App #294 (F294-1), #297 and #295 (F295-1, F295-2) into `release/14/main`, in any order.
4. App #296 (F296-1) into `release/14/plan-59`.
5. Merge App and Agent `release/14/main` into their `plan-59`; Runtime main is already contained.
6. Rebuild :2400. Re-profile counting opens and stats (not only hashes), record wall times as evidence, then review commit-loads.
7. Before publication: poms_packs `100f388` on main or pinned.

## Required fixes

- **F59-1 (Runtime): media-pin reads use the identity map.**
  - In `_history_object_value`, when `verified_cas[object_id]` equals the current `lstat` identity, record `(trusted[2], bytes.fromhex(object_id))` the way `_read_history_object` records a value, and return it without opening the file.
  - Extend `test_trust_survives_a_refused_commit_and_an_unrelated_database_write` to assert **opens == 0** after the refusal and after the external write.
- **F59-2 (Runtime): one CAS instance per commit store.** `_file_unchanged` and `_read_object` currently build `ContentAddressedStore` per call, which costs `resolve()` plus `mkdir` each time. Alternatively, `lstat(cas_root / id[:2] / id[2:])` directly.
- **F59-3 (Runtime test):** in `test_commit_and_history_read_cost_does_not_grow_with_history`, also assert stats are equal at 3 and 30 entries. Today only hashes and opens are compared.
- **F394-1 (Agent test): freeze the oracle.** Copy `release/14/main`'s `_legacy_declaration_is_resolvable` and `_known_unresolvable_timing_error` verbatim into `legacy_probe_oracle.py`. Assert the gap_after_s divergence as the one expected difference.
- **F394-2 (Agent test):** run the verdict differential (new vs frozen oracle, accept/refuse) over the real-shape heads as well as `candidate()`:
  - `tests/fixtures/timeline_redo_media_closure_1338.json`;
  - `tests/editing_conformance/fixtures/main_image_cap_raw_closure.json`;
  - the roundtrip-corpus heads that carry legacy on/until.
  Each head gets an unrelated edit and a moved clip.
- **F394-3 (Agent test):** delete `test_legacy_probe_gap_after_fault.py`. `test_unresolved_declaration_on_a_base_carrying_gap_after_s_is_exempt` covers it.
- **Decision (Agent):** record that unchanged unresolvable legacy declarations on bases carrying unsupported declarations are now exempt.
- **F295-1 (App): delete the automatic `stale_head` rebase.**
  - Remove the `rollback()` branch, `MAX_STALE_HEAD_REBASES` and `staleHeadRebases`. Keep `rebaseRejected` for the explicit 'keep'.
  - `stale_head` then shows the card like any conflict.
  - Test: a `stale_head` refusal sends nothing until the user chooses.
  - Optional Runtime follow-up: answer the accept race at `:2181` as `head_busy` (same-key retry), since nothing was accepted.
- **F295-2 (App): discharge only on the explicit choice.**
  - Remove `discharge('latest')` from `reloadFromServer`.
  - Add a chrome action, "use latest version", that calls `discharge('latest')` and then `reloadFromServer()`. Wire it to the banner button (`TimelineEditorShellCore.tsx:846`) and the dialog's `onDiscardRemoteChanges` (`:343`).
  - Test: a programmatic reload (shot duplicate) keeps a retained refusal and its card.
- **F296-1 (App): reuse only an exact binding.**
  - Reuse an existing key only when its entry equals `{media_id, type: 'image', generationId, variantId}` built from this selection; otherwise take a new key.
  - Change the reuse test: an entry with extra fields gets a new key, and an exact binding is reused.
- **F294-1 (App): let pinned-group sync converge.**
  - Build `desiredGenerationIds`, and the placement loop, only from images that will be associated (skip `primary_variant_id == null`, as images without `generation_id` are skipped).
  - Test: a group with a variant-less image; the second sync pass makes zero edits.

## Missing tests that would let a regression through

- **Runtime:**
  - opens after a memo clear (F59-1);
  - a `head_busy` on a commit POST, not only on a history GET, followed by a same-key acceptance.
- **Agent:** frozen oracle and corpus (F394-1, F394-2).
- **App:**
  - 'keep' with the one-slot draft still present must not re-offer or duplicate the edit (the hook test clears the draft first);
  - pinned-group convergence (F294-1);
  - reuse checked against the Agent's binding rule (F296-1).
- **Recommended, App:** cap or count `head_busy` retries. An unbounded same-key retry hides a persistent cause such as #847's first-start error; the Runtime now logs the moved component, so check how often it fires on :2400.

## Runs

- Runtime `975ab0f` export: `test_timeline_commit_cost.py`, `test_timeline_history_read_cost.py` and `test_timeline_history_state.py` gave 73 passed. Probe (`scratchpad/rt59src/tests/test_probe_opens_after_memo_clear.py`):
  - warm commit: 0 hashes, 0 opens, 70 stats;
  - after a refusal: 0 hashes, 5 opens, 93 bytes;
  - after an external DB write: 0 hashes, 5 opens.
- Agent `d6fe2abb0` export, with the Runtime export on the path and an empty HOME (the real `~/Astrid/packs` collides with test fixtures): the three new or changed files, `test_authenticated_legacy_restore.py`, `test_commit_timing_validation.py`, `test_commit_legacy_text_reference.py`, `test_commit_boundaries_d12.py`, `test_commit_fps_d12.py` and `tests/sdk/test_p1_doc_patch_provider.py` gave 181 passed and 27 deselected.
- Comparison against the frozen oracle (`scratchpad/ag394src/tests/editing_conformance/test_zz_reviewer_frozen_oracle.py`, which loads `release/14/main`'s module beside the PR's): 72 combinations, **56 same and 16 different**. All 16 go old-refuse → new-accept, and every one has an unsupported declaration (gap_after_s or formulas) on the base:
  - 12 unrelated edits over an unchanged unresolvable declaration: acceptance change 2;
  - 4 moves of the clip carrying the declaration: R5.
  
  Every "plain" combination is identical, and nothing goes accept → refuse. This is synthetic data only; F394-2 extends it to real heads.
