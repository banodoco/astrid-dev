# Direct Journey round 4 evidence (App 99738aefc)

[Handoff](../../handoff.md) · [Tasks](../../tasks.md)

# Direct Journey release 12: three newly reached failures

Issue draft — 2026-11-10. CI run 42836162499; App `cand/29-r12` at `99738aefcb7f055b0ebee4c68041c6c74fb876f3`. Source began clean; the candidate is the uncommitted diff in `app/`. Runtime `42ae24aff8d2cb854f874ce134161077a3ba3641`, Agent `313bbd46f1e24bfe635655d78b27ab0b321145d5` from the downloaded reports. No live workspace was accessed or altered. CI evidence was parsed as data, never executed.

## 1. Stale-build durable save — test drift

The test at original `direct-journey.spec.ts:753` completes Reload click (`trace/test.trace`, `pw:api@50`, lines 52–53), then waits at original line 773, `await saveStarted`. Its private route only signals that promise for POST `/composition-revisions`, a retired save path. It does not call `holdTimelineSaves` or `holdCommandRequests`, directly or indirectly.

Evidence directory: `ev/direct-journey-traces/direct-journey-restarts-Ap-ebc76-eline-save-before-reloading/`. `trace/0-trace.network:106` shows POST `/commit` returned 200; `:108` reads the accepted successor revision. No POST to `/composition-revisions` exists. The later test timeout is in `trace/test.trace:60`. The App saved successfully while the test awaited an event that could never occur.

Fix: `app/tests/e2e/local/direct-journey.spec.ts:761` now holds the actual native save with `holdTimelineSaves`, observes the held request, and releases it after checking the Saving state and the old-page sentinel. Head advancement, saved track value after reload and absence of recovery remain required. The 180-second timeout is unchanged; the formerly unbounded promise is replaced with the same 20-second request observation used by neighboring tests. The same retired route in the next, skipped persistence-failure test is corrected at line 785.

Round 3 (`git show 723025f60`) is unrelated: `held.add(route)` precedes the gate wait; release leaves held routes in the set, so `held.delete(route)` succeeds and continue runs. `abortHeld` removes and explicitly aborts only its current snapshot, intentionally preventing those routes from continuing again; future recovery requests are added separately. No helper change is needed.

## 2. Concurrent edit loses C on Keep — product bug

`timelineDraft` (`app/tests/e2e/local/support/app.ts:470`) opens `astrid.timeline-drafts` and gets the timeline record from the `timeline-drafts` object store in a readonly IndexedDB transaction. It never reads the mounted editor. Canonical display rollback in `localSaveSession.ts:125` is intentional; losing the recovery record is not.

Evidence directory: `ev/three-products-traces/three-products-concurrent--81b8f-onflict-and-keeps-its-draft/`. In `trace/0-trace.trace:863`, `call@678` / `pw:api@331` reads the durable A+C draft after the conflict: the transition is absent and the base is the original head (`…e61c`). Its full equality to draftC passes (`trace/test.trace`, `expect@332`). Keep is clicked at `pw:api@371` (`test.trace:582`). In `0-trace.trace:951`, `call@700` / `pw:api@378` reads a replacement record with a new owner, B's head (`…ca22`), and transition `{durationFrames:36,id:"cross-fade"}`. `expect@384` fails at `test.trace:609`.

Cause: `useTimelinePersistence.retrySaveAfterConflict` called `createRecoverySave` on `getDataRef().current`, which had already been rolled back to B. That overwrote the correct durable A+C slot and its CAS provenance.

Fix: `app/src/tools/video-editor/hooks/useTimelinePersistence.ts:1676` drains recovery writes, verifies successful storage and the existing native draft, and then reloads canonical with `preserveDraft:true` without recopying the display. Missing or failed native storage leaves the conflict open. Legacy save-as-copy still stashes the visible local draft. No command/outbox operands, retries or CAS rules change.

Regression: `useTimelineCommandsService.persistence.test.tsx:456` extends the real native conflict/rollback test through Keep; the entire durable record (including original base), retained intents and pending request must remain identical, canonical display remains remote, and no extra send is allowed. `useTimelinePersistence.test.tsx:2188` covers missing drafts and failed writes even when an older slot is readable. The journey gains a full draft equality assertion at `three-products.spec.ts:581`; all conflict, replay, revision count, reload, Retry and Use latest checks remain.

## 3. Native None bulk owner payload — test drift

`commandsOf` reads payload.commands. Native document saves persist `documentIntent` and synthesize the doc.patch envelope only when dispatching (`localSaveSession.ts:190`). The existing handoff-test helper `mountedDocumentIntentOf` validates this representation.

Evidence: `ev/three-products-traces/three-products-M2-native-N-4956c-ict-retains-the-whole-draft/trace/0-trace.trace:536`, `call@1400` / `pw:api@159`; retry1 directory's `trace/0-trace.trace:525`, `call@1413` / `pw:api@159`. Both returned outbox payloads have `before,after,label,kind,displayBasis,documentIntent`, with no commands field. Both contain two documentIntent.changes exactly equal to the sent doc.patch args.changes, including every opaque before-value and literal __proto__ property. The final failed assertion is `expect@161` (`trace/test.trace:275`) on each attempt.

Fix: `app/tests/e2e/local/three-products.spec.ts:3006` reads the validated mounted document intent and compares the entire request command array exactly to the doc.patch envelope containing those changes. Exact equality includes command count, schema/version, selection, created IDs, operands, guards and all unknown nested data. One atomic intent, lost-ACK exact retry, immutable closure, history, undo, real conflict and restart assertions remain untouched.

## Skipped cases

The immediately following stale-build persistence-failure test had the same retired route; it is fixed as above. Other skipped mounted-gesture cases still assert concrete commands/commandsOf (notably M1 real gesture, ordinary extension batch, native duplicate's queued label, and mixed editing). The mounted move/label/element routes can persist documentIntent, so those assertions warrant the same representation audit when reached; explicit command routes such as prepared media, duplicate operations and inverse history must keep their command checks. They have not been replayed here and are not claimed repaired. The durable-draft fix also protects other native conflicts that roll the display back before Keep.

## Validation and recovery

- PASS: `git -C app diff --check` on the final uncommitted candidate.
- PASS: read-only Python JSON audit of supplied traces confirms the actual /commit success, durable C before Keep versus B afterward, and exact equality of persisted changes to both native None request bodies. This is evidence verification, not product execution.
- NO-RESULT: TypeScript, Vitest and Playwright. `node_modules` is absent, and installing dependencies or running those tests is prohibited in this environment. New and changed unit regressions require CI execution. No green runtime claim is made.
- Workspace size remains about 292 MB, below the 2 GB limit. No git writes, installs, pods or external publication.

Recovery for the release candidate is to apply this uncommitted patch and replay the three named failures plus the adjacent stale-build error test and the focused unit regressions in CI. The patch is reversible file edits; rollback is reverting only these hunks. Existing drafts already overwritten by Keep cannot be restored by this code change; rejected outbox owners are retained and should not be deleted.

This local issue draft is ready for the release orchestrator; no issue or PR was published because the requested handoff is uncommitted source changes. Routes used: Unknown — no run manifest or independent model-usage provenance was supplied for this scoped repair.
