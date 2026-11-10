# Direct Journey round 5 evidence (App 3ab9f5067)

[Handoff](../../handoff.md) · [Tasks](../../tasks.md)

# Direct Journey release 12 — round 5

2026-11-10. CI run 42840758126; clean starting App head `3ab9f5067` on `cand/29-r12`, including round 4 `26819d552`. Candidate is the uncommitted diff in `app/`. Supplied CI files were parsed only as data. No installs, git writes, publication, live workspace access or pods.

## 1. Stale-build persistence failure (:779) — test drift

Evidence base: `ev/direct-journey-traces/direct-journey-restarts-Ap-b4c76--timeline-persistence-fails/`.

- `trace/0-trace.trace:220`, `call@1250` / `pw:api@50`: clicks Reload.
- `trace/0-trace.network:105`: POST `/commit` fails with status -1. **The route injection does fire.**
- `trace/0-trace.network:107`: GET of the editor document succeeds after that failure, at monotonic time 130398.21. This is navigation, not a missing alert locator on the old page.
- `trace/0-trace.trace:349`: recovered page snapshot contains “You have unsaved changes”; `error-context.md` also shows the draft label and recovery actions.
- `trace/test.trace:65`, `expect@51`: no “Could not safely reload” alert exists, so the old `Timeline:` assertion fails.

Reload intentionally accepts either a Runtime acknowledgement or verified local recovery. `useTimelineSave.ts:484` catches a failed flush and calls `preserveTimelineDraftForReload`; `draftSafeReload.ts:133` uses the recovery-capable guard for Reload. Aborting `/commit` alone therefore does not inject failure of the reload's persistence boundary. Round 4 correctly fixed the obsolete URL, but that exposed this mismatch. This is not a product failure to surface a rejected reload: the reload was admitted.

Fix: `app/tests/e2e/local/direct-journey.spec.ts:789` additionally injects a `QuotaExceededError` for readwrite transactions **only** in `astrid.timeline-drafts`. Native outbox storage and readonly inspection remain usable; the commit abort is retained. The assertion at line 807 pins the actual authoritative guard's text: `Timeline owner: Injected timeline persistence failure`.

Strength: no-reload sentinel, original draft label, unchanged Runtime head, and visible failure are all still required. The error assertion is more specific. Neither timeout nor product reload policy changes.

## 2. Concurrent edit (:449, failure :601) — product bug

Evidence base: `ev/three-products-traces/three-products-concurrent--81b8f-onflict-and-keeps-its-draft/`.

- `trace/0-trace.network:248`: the queued native C request receives 409; its response is resource `90cc67aa3e65820352ca6a67faf9362dbd044c33.json`.
- `trace/test.trace:626`, `expect@393`: **round 4's full A+C draft equality after Keep passes**. Keep closes the first conflict; canonical B is shown. Round 4's durability repair is retained unchanged.
- `trace/0-trace.trace:1323`, `call@998` / `pw:api@477`: after reload, the same durable A+C slot remains, with its original base and cleared transition.
- `trace/0-trace.trace:1351`, `call@1005` / `pw:api@481`: clicks Save them. `:1371`, `call@1008` / `expect@482`: waits for the named conflict, which never appears. No POST `/commit` follows that click in `trace/0-trace.network`; the final snapshot still has the recovery alert and canonical crossfade.

The two recovery representations were not connected at this action: the native owner retains its rejected original chain and knows it is conflicted, while the one-slot action only follows the generic build-and-capture path. It has no branch to reopen that existing native refusal in persistence's conflict state. Reconstructing a new native edit from the slot is invalid: `trustedRecoveryHead` restores only the revision pin (the record has no publication pin), and `timelineLocalSaveHandoff.checkHead` requires the complete original pair. Such a capture can fail locally as `TimelineSaveError` rather than reaching the named remote-conflict flow; recopying the slot also risks replacing the original durable record. The trace establishes the missing UI/no new send; the source establishes this invalid recapture path. Round 4 made this later step reachable by preserving the correct draft.

Fix: `app/src/tools/video-editor/hooks/useTimelineSave.ts:701` recognizes a recovered native session already in `conflict` and reopens resolution directly. `useTimelinePersistence.ts:415` reuses the existing conflict handler, including the synchronous poll/write gate. The branch runs after the recovery slot's scoped provenance check and before rebuilding/capturing/writing it. It does not change the original request, guards, key, intents, base or record, and it does not retry or rebase the rejected chain.

Regression: `app/src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx:458` extends the real native rejection/rollback test through Keep, unmount/remount against the remote head, Save them, and Use latest. It requires complete slot and outbox equality across Save them, visible conflict state, canonical display, no additional send, then explicit draft deletion and conflict closure. Existing assertions are retained. `three-products.spec.ts:600` also strengthens the journey to compare the complete retained draft record and require no additional POST when reopening the existing refusal. All original history, retry bytes, publication counts, reload, conflict and discard checks remain.

## 3. M2 native None bulk (:2988, failure :3013 → :2865) — test drift

Evidence bases:

- `ev/three-products-traces/three-products-M2-native-N-4956c-ict-retains-the-whole-draft/`
- `ev/three-products-traces/three-products-M2-native-N-4956c-ict-retains-the-whole-draft-retry1/`

The round 4 command-envelope equality at :3006 passes on both attempts. First attempt `trace/0-trace.trace:560`, `call@1519`, and retry `:552`, `call@1515`, return the durable outbox with one document intent. The complete pending request body equals the wire body byte for byte; its single doc.patch envelope equals the persisted changes, including unknown transition revision and literal `__proto__` values.

The actual failure is later: both `trace/test.trace:355`, `expect@201`, fail the history read list. Both `trace/test.trace:346`, `expect@197`, contain the full persisted publication used by that assertion. The record has five reads in order: first clip id/transition, second clip id/transition, then the **shared** parent pinnedShotGroups absence once. The test expected it twice, interleaved per clip.

The same captured history also proves the next old expectation was wrong: two derived config.clips mirror writes are persisted, both with cause 0. Mirror 1 removes only clip 1's transition; mirror 2 starts with that exact intermediate array and removes clip 2's transition. The previous test expected a single base-to-final mirror. This is per-removal history inside one atomic command/publication, not extra commits.

Fix: `app/tests/e2e/local/three-products.spec.ts:2867` asserts the exact five reads in their persisted order. Line 2878 constructs the independently expected mirror sequence from the base revision and the requested removal order; line 2887 compares the entire derived-write array exactly, and the final array must equal the accepted revision's clips. The helper applies equally to a single clear and the bulk clear.

Strength: no subset/normalization/set conversion of actual results. The full command record, original values, every write, every intermediate mirror, final document and unknown data remain pinned. The atomic intent/envelope, lost-ACK exact retry, immutable closure, history count, restart, undo and later real-conflict checks remain. No product code changes for this failure.

## Validation and limits

- PASS: `python3 round5-audit.py` reads both attempts, verifies persisted bytes and full command envelopes, exact five-read lists and complete intermediate mirror sequences. It also verifies stale-build navigation after the abort and absence of a new commit after concurrent Save them. An initial audit-script run used the wrong path index for clip ids and failed; correcting the audit to the actual `['clips', 'id:…', 'transition']` paths produced the passes. No CI data was executed.
- PASS: `git -C app diff --check` on the final patch.
- NO-RESULT: TypeScript, Vitest and Playwright. `app/node_modules` is absent; dependency installation and running these checks here are prohibited. New unit regression and all three journey selectors require CI execution. Evidence audit is not execution proof for the patched App.
- Workspace: about 301 MB, below 2 GB. All changes remain uncommitted.

Recommended CI replay: the three named journeys; the two stale-build journeys together; the focused mounted native conflict regression above. No claim that skipped cases pass.

## Remaining skipped tests with shared exposure

The native conflict/one-slot handoff can affect the skipped M1 real dependency-conflict case (original :2422), and any restart/reopen journey that reaches a retained rejected owner: Runtime restart (:633), M1 real gesture (:1506), real gate 5 (:1619), ordinary extension batch (:1836), native occurrence duplicate (:2485), and mixed editing (:2667). Their successful delivery paths must still exercise exact retries; the new branch only handles a known rejected conflict. The unreached real-conflict/restart tail of this M2 None test shares that recovery risk too.

The recorded-clear helper is shared with single-None clearing, and any future multi-leaf native history assertion must account for shared reads and per-removal mirrors while retaining full equality. The stopping/restart cases can encounter recovery-capable reload semantics, but the remaining security, rendering and extension-loading skips have no demonstrated connection to these three causes. Round 4's separate warning about mounted documentIntent versus explicit commands remains applicable to unreached mounted-gesture tests.

This pack is the local incident/issue draft for the orchestrator; no external issue or PR was published. Routes used: Unknown — no independent model-usage manifest was supplied for this scoped repair.
