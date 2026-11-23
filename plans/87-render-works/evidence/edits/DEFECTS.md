# Timeline editing defects — release-14-plan-69

Project: Almost Ready (`801a01b3a87941a1ab25958c488afdbf`), timeline trial v2 (`77f906f3242c48179ab86ca7c3e62eb4`). Investigated 2026-11-22. No installed source, SQLite, or GitHub writes. No Runtime restart.

Source prefixes below are exact installed paths:

- `A` = `~/astrid-release/release-14-plan-69/program/versions/5bf20639e293/py/lib/python3.11/site-packages/astrid`
- `R` = `~/astrid-release/release-14-plan-69/program/versions/5bf20639e293/r`
- `G` = `~/astrid-release/release-14-plan-69/program/versions/5bf20639e293/py/lib/python3.11/site-packages/astrid_runtime_client`
- `E` = `~/astrid-release/release-14-plan-69/editor/src/tools/video-editor`

“Verified” means observed in a reproduction, saved request/receipt, fresh Runtime read, or inspected source. “Inferred” explicitly marks a causal link the logs cannot establish. Repro scripts use `bash edits/stackpy.sh -u SCRIPT` from r6, with this stack's environment. Never run CLI `--help`.

## 1. Oversized commit upload becomes an unknown outcome

**Verified:** the original flight `timeline-edit-8e8c71ea6b8d4944abe7059883ead17f` contains 1,781,813 UTF-8 bytes, one `doc.patch` command / 449 changes, and `dry_run:true`. The time-lapse still had all 341 clips on our first independent current-head read; the whole timeline had 621 clips. That flight could not publish even if processed because it was a dry run. The Runtime was accepting other writes: sandbox project `r6-write-sandbox` (`23d9b5a570b2498d878edced4f3d4942`) has a verified trivial committed name edit, revision `db8c636c…` → `834b865a…` (full revisions in `sandbox-test.log`). The Runtime was not globally wedged.

**Minimal sandbox repro:** `edits/recovery-repros/oversize_dryrun.py`, detailed in `recovery-repros.md`. Set one opaque config field to 1,100,000 characters and preview through a unique SDK outbox. Command plus step metadata makes the request 2,200,894 bytes. The error is:

```text
CommitOutcomeUnknown No reply could be verified; this edit may or may not have been committed. Call tl.commit() again with no arguments to confirm the saved request; the edit is not re-run blindly.
```

Our original flight retry with `tl.session.flush(dry_run=True)` additionally exposed the underlying error verbatim:

```text
WorkspaceClientError [Errno 32] Broken pipe
```

**Root cause, verified source:** `R/runtime_protocol/server.py:205–206` sets timeline bodies to 1,048,576 bytes, independently of its 64 MiB general cap. `:247–256` rejects `Content-Length` before reading the body; `:1561–1566` prefetches with that limit before routing. The SDK talks directly to daemon port 50301, not through browser door 17501. The daemon error inherits HTTP 400 (`R/runtime_protocol/errors.py:85–91`; server.py:576–584); the separate browser door maps size errors to 413. A daemon 413 must not be assumed. `G/generated.py:652–689` uploads through urllib and can lose the early refusal while sending. `A/sdk/workspace_client.py:297–307` normalizes transport exceptions. `A/sdk/timeline/sync.py:1078–1082,1166–1170` treats everything outside typed conflict/refused/invalid as unknown. Access logging is disabled at server.py:209, and no matching key/error appears in Runtime logs, so the precise network sequence producing Broken pipe remains **inferred**, not log-proven. The cap and oversized request are verified.

**Deliberate?** Byte cap and conservative uncertainty are deliberate; permitting a locally knowable oversized preview to poison a durable session is defective. **Severity:** critical for an agent performing bulk edits.

**Smallest correct fix:** check serialized request size before persisting a flight; return a typed known refusal for a pre-dispatch size rejection; drain/close the upload correctly so clients receive the structured error. Report the actual byte cap. Reduce emitter amplification rather than claiming a fixed clip-count limit: `A/sdk/timeline/emitter.py:78–84` includes the whole remaining identity order for every removal, and `commit_session.py:87–92` duplicates the patch into step metadata. E ultimately fit in one legitimate guarded collection-set request (about 350 KB); no split was necessary.

## 2. Unknown dry-run recovery instruction does not preserve request mode

**Minimal sandbox repro:** after #1, do exactly what the error says: `tl.commit()`.

```text
TimelineEditError: in-flight request is immutable; retry its original payload and key
```

**Root cause, verified:** `A/sdk/timeline/commit_session.py:603` defaults `dry_run=False`; `sync.py:1295–1315` requires the original dry-run flag, as well as body/key, to match. `sync.py:107–128` and `_commit_wording.py:45–48` recommend a no-argument retry without preserving the mode. `tl.commit(dry_run=True)` / session `flush(dry_run=True)` sends the original preview, but cannot cure its size refusal.

**Deliberate?** Immutable retry is deliberate; the proposed recovery is wrong. **Severity:** high. **Smallest correct fix:** an argument-free reconciliation should infer mode and key from the saved flight; new intent must remain explicit. At minimum emit the correct dry-run replay call in the error.

## 3. There is no supported way to retire a provably non-publishing unknown preview

**Minimal repro:** retain the oversized sandbox dry-run flight from #1 and retry it in its original mode. The same request must remain over the cap. `pending_drop` accepts saved pending changes, not unknown flights. `timelines discard` explicitly retains unknown requests.

**Root cause, verified:** `A/sdk/timeline/sync.py:422–435,1001–1075,1166–1170` retains and resends the immutable flight; `commit_session.py:1061–1077` drops only pending records; `A/core/cli/domain_timelines.py:1299–1303` preserves unknown flights. No supported abandon/reset API was found. This is a source-audit conclusion, bounded to the installed API.

**Deliberate?** Protecting unknown real writes is deliberate; lack of a safe preview-only escape is an omission. **Severity:** critical for the default session. **Smallest correct fix:** a supported reconciliation/abandon-preview operation that verifies `dry_run:true`, preserves an audit record, and clears only that flight; also classify known pre-admission rejections correctly.

**Workaround actually used, verified:** `Timeline.open(..., outbox_path=<unique path>)` (`commit_session.py:1099–1113`, `sync.py:407–421`) creates an independent supported SDK session. The original default outbox was preserved unchanged. This restored our ability to edit; it did **not** repair the default poisoned outbox. No storage hand edits or restart were used.

## 4. clip.delete refuses unrelated clips when semantic declarations exist anywhere

**Minimal sandbox repro:** `edits/sandbox_guard_probes.py` (log and `sandbox-guard-followup.md`) adds `config.app.astrid.slots={'probe':{}}` to a detached sandbox candidate and deletes a plain unreferenced parent hold through `capture_clip_delete`. It reproduces the exact config-path guard. `edits/guard_repros.py` separately verifies the target-slot case. On the actual film, clip-1 itself has no semantic relation fields and no declared references; only its own ID occurs in the clip rows / baseline mirrors. Original refusal:

```text
CommandError: clip.delete cannot prove declared semantic dependencies safe
```

Film detail: `kind=unsupported_dependency`, path `['config','app','astrid','slots']`. The sandbox target-slot variant gives path `['app','astrid','slot']`.

**Root cause, verified:** `A/sdk/timeline/_delete_commands.py:16–23,40–51` scans all parent and occurrence config/clip declarations and rejects any nonempty sequences/formulas/slots or relation fields; it never checks whether a declaration actually references the selected clip. `:54–69` deliberately restricts deletion to a bounded parent slice.

**Deliberate?** Explicitly deliberate conservative guard; excessive for this unrelated image. **Severity:** high. **Smallest correct fix:** validate known dependency shapes and reject only references to the selected identity; keep refusal for unknown reference-bearing schemas. A was applied via supported full-collection `doc.patch set` after checking references and preserving every other clip.

## 5. set_param cannot resolve a project-admitted element

**Minimal sandbox/local repro:** `edits/guard_repros.py` calls the same `element_schema('ar-discord')` helper used by `Clip.set_param`, while connected to the sandbox. It produces:

```text
ElementPackNotInstalled [element_pack_not_installed] ar-discord: no installed pack declares this element, and it is not one this release knows moved to a pack; no param was written. Install the pack that provides it, or check the clip type (`astrid packs list` shows what is installed).
```

**Root cause, verified:** `A/sdk/timeline/model.py:682–691` uses local `timeline_address.element_schema`; `A/sdk/timeline_address.py:436–468,480–520` consults the default installed pack registry/moved-element table. The film instead carries a pinned `elementRef` in `project_cd4fa4f1666bc788f4a9`. Editor `E/runtime/admittedElementLoader.ts:90` reads `/packs/project-elements?project=...`; commit validation `A/sdk/timeline/validation.py:494–524` resolves retained project snapshots. These are different resolvers. Successful B/C raw-parameter commits further verify that the project pack is admitted and writable without reinstalling it.

**Deliberate?** Schema validation is deliberate; ignoring the clip's project elementRef in the editing helper is a defect. **Severity:** high. **Smallest correct fix:** resolve a clip's exact project elementRef/schema through the connected project registry before falling back to local installed packs. `packs list --project` is unsupported and not an authoritative test of project admission. B/C used guarded document edits, retaining the exact elementRef.

## 6. nudge of one clip retimes unrelated content

**Minimal local repro:** `edits/nudge_reflow_repro.py` loads a detached film-shaped bundle and calls `nudge(-1)` plus `hold_for(1.533334)` on only the arrow. That current detached normalization changed 9 rows, not 354. The original retained, dropped record `pc_2bcbaa00d8f3` independently verifies **362 operations touching 354 clip IDs**: 353 at writes, 8 hold writes, and 1 on write. Example saved operation: `c17-tl-001.at: 0.433 → 0.433333`; parent music hold `188.1667 → 188.167`. The pending-record count is verified; the current local probe is a smaller reproduction, not evidence of an identical 354 count today.

**Root cause, verified:** `A/sdk/timeline/model.py:396` nudge delegates to `on`; `:299–334` invokes timeline-wide `retime()`. `reflow.py:370–425` snapshots sequence duration ratios and relays picture sequences to cut spans; `_relay_steps` at `:1272–1298` rewrites all their positions/lengths. Timing normalization affects untouched rows. `sequence_shape_from` is provenance, not a frozen shape used by retime.

**Deliberate?** Global reflow is intended for semantic edits; nudge's scope is unsafe for an agent requesting one exact clip move. **Severity:** high. **Smallest correct fix:** expose a scoped exact timing edit, or have nudge default to a local move with an explicit opt-in reflow; make broad changed-row counts visible before publication. D used direct guarded fields and a cut-relative on expression, with only its clip changed.

## 7. Failed/pending state and _OutboxChanged were conflated

**Minimal sandbox repro:** `edits/recovery-repros/outbox_changed.py` queues another SDK command in an isolated outbox during function evaluation, then observes:

```text
_OutboxChanged: outbox changed during evaluation; nothing was submitted
```

**Root cause, verified:** `A/sdk/timeline/sync.py:955–960` compares the complete expected local state before submitting. `commit_session.py:810–839` handles the local race, and dry runs deliberately raise immediately. Known refusal/invalid results save an inspectable pending record and clear the active flight at `sync.py:1083–1150`. `edits/pending_after_refusal.py` additionally verified that a new valid preview succeeds in the **same** outbox while the prior refused pending record remains (see `pending-after-refusal.log`). Pending records alone do not block that next call; an unknown flight is a separate blocker. The “every failed commit blocks every later call” claim is too broad.

**Deliberate?** Pending retention and the race fence are deliberate safety behavior, not themselves defects. **Severity:** medium for shared actor sessions, critical only when combined with #3. **Smallest correct fix:** improve diagnostics to distinguish saved pending edits, active flight, and another writer's outbox race; use per-agent supported outboxes or explicit pending retry/drop. Do not silently discard failed intent.

## 8. Unstamped direct SDK caller gets a misleading older-runtime message

**Minimal source/local repro:** `edits/identity_repro.py` compares `capture_startup_identity(environ={})` with the stack-stamped environment. Empty env gives release 0; `ASTRID_INSTALL_RELEASE=13` gives release 13. `identity-repro.log` records only safe identity metadata. Original connection error:

```text
ServiceUnavailableError: An older Astrid is still running. Restart it after its running tasks finish.
```

**Root cause, verified:** `runtime_protocol/startup_identity.py:30` defaults the caller release to 0. `R/astrid_runtime/identity.py:12–14` uses one generic older-runtime refusal for an identity mismatch. This test directory is named release-14 but its installed version/manifest identity is consistently release 13. The previous custom `env -i` Python wrapper dropped the stamp; the managed CLI wrapper overlays version environment correctly. This is **not** evidence that the managed install is internally release-mismatched.

**Deliberate?** Identity fence deliberate; misleading diagnosis/restart advice defective. **Severity:** high for custom SDK execution. **Smallest correct fix:** provide a supported installed SDK runner/environment adapter and identify “unstamped caller identity” distinctly; do not recommend restarting a healthy owner. Our stackpy wrapper mirrors the actual version stamp.

## 9. Document list.remove capture disagrees with Runtime authorization

**Minimal sandbox repro, verified:** `edits/list-observation-repro.py` creates `r6-list-repro`, seeds one ordinary parent hold by collection set, then previews two equivalent removals. `list-observation-repro.log` records:

```text
item_scoped_list_remove: refused code=validation_error reason=invalid_records message=provider list effect lacks a full collection observation
full_collection_set: ok=True status=preview error=None
```

Film A encountered the same refusal before the successful whole-collection set. Both use registered product commands.

**Root cause, verified:** `A/sdk/timeline/_doc_patch.py:506–520` intentionally records selected collection identity plus removed-row read/clear, then compiles mirrors, omitting a full collection write. `R/runtime_protocol/timeline_commit_auth.py:937–944` requires a recorder write at the exact full collection path to project a list effect, and refuses if absent. This is a client/provider/Runtime contract mismatch.

**Deliberate?** The row-scoped optimization is deliberate; incompatible admission is a defect. **Severity:** critical for document deletions / bulk shortening. **Smallest correct fix:** teach Runtime to project authenticated row/collection-identity removals without guarding every survivor, or have the provider emit the collection result in a form Runtime accepts. Full collection set is the accepted guarded workaround, at the cost of whole-list contention.

## 10. Edited internal word declaration has no supported exact-binding capture

**Minimal sandbox repro:** `edits/sandbox_guard_probes.py` adds one synthetic shot-owned internal clip in a detached sandbox candidate. `compile_timing` reproduces the missing-binding error; the equivalent cut-offset compiles successfully (see `sandbox-guard-followup.md`). **Film evidence:** the first D attempt changes only at/hold and `on` from `"up" in N12 +0.07s` to `"up" in N12 -0.93s`. `D-word-refusal.log` contains:

```text
candidate.timing: missing exact word binding for ('occ-77f906f3242c48179ab86ca7c3e62eb4-55940497dcea0a1f1f66-occ', '77f906f3242c48179ab86ca7c3e62eb4-55940497dcea0a1f1f66', 'c23-desloppify-arrow').on
```

**Root cause, verified:** `A/sdk/timeline/_timing_evaluators.py:413–425` requires a binding matching the exact new word declaration. `native_word_anchor.py:233–257,293` supports parent clips and rejects shot-owned word anchors; `_commit_timing_validation.py:126–133` explicitly notes the shot binding gap. `_capture_free_edits` (`commit_session.py:485`) emits document changes without generating new word bindings. An old preexisting missing binding is tolerated until its declaration/timing changes.

**Deliberate?** Exact pinning is deliberate; internal clip support is incomplete. **Severity:** high. **Smallest correct fix:** extend authenticated word-anchor capture/validation to occurrence-owned internal clips, resolving exact transcript/version/word IDs. D's supported alternative is `on:'+3.133333s'`: `core/timeline/moments.py:83–91,249–256` resolves it relative to c23's 52.8 s cut start, producing the requested 55.933333 s start. This intentionally follows the cut rather than a future moved word. No other clip needs to be retimed.

## Scope and retained evidence

- `A`–`E` receipts and before/after bundles: `edits/{letter}-receipt.json`, `{letter}-before.json`, `{letter}-after.json`.
- Independent changed-ID checks: `edits/audit_edits.py`, `edits/audit.json`.
- E frame/asset proof: `edits/E-rederived-plan.json`, `edits/E.log` (99 clips, 410 frames, minimum 4; original asset subsequence/order retained; overlays unchanged).
- Real editor stills and observed timecodes: `edits/verify/`; read-only playback, no timelines render.
- Original poisoned default outbox remains at the path in FRICTION.md. Separate session files here are SDK-managed proposals/receipts, not alternate timeline authorities.

## 11. Centisecond playback labels truncate and can lose a hundredth to binary rounding

**Verified editor observation:** the frame slider's duration text is `3:16.56` for 5897 frames / 30 fps = 196.566666… seconds. The requested rounded end is `3:16.57`. A seek to 7.6 seconds also displayed `0:07.59` while the DOM time was 7.6. These labels do not imply a different authored end.

**Minimal repro:** the pure `formatTime(196.566667, CENTISECOND_TIME_OPTIONS)` and `formatTime(7.6, CENTISECOND_TIME_OPTIONS)` calls require no project mutation. The same rendering is visible when reviewing the sandbox or film; this is an editor formatter, not Runtime timing.

**Root cause, verified:** `editor/src/shared/lib/timeFormatting.ts:36–45` separately floors whole seconds and `(seconds % 1)*100`, exposing binary remainder error and truncating duration rather than rounding it. `E/components/PreviewPanel/PreviewTransport.tsx:344–360` uses it for current time and duration.

**Deliberate?** Truncation is explicit; using it as a rounded duration and losing a hundredth at an exact nominal centisecond are UX defects. **Severity:** low editorial ambiguity. **Smallest correct fix:** use one integer centisecond conversion with an explicitly chosen display policy (rounded for duration), then derive minutes/seconds/fraction from that integer; for current frame display, quantize from the frame index with a defined rounding policy. Do not change authored clip timing to correct a label.
