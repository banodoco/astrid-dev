# Inputs — Dependable saving

[Plan](plan.md) · [Tasks](tasks.md) · [Statements](statements.md)

## Planning evidence

**Scope decision:** Pending — the owner decided the release and the order (D9, below), and approved Plan 18's re-scope earlier ([Plan 18 D1](../18-timeline-editing/inputs.md#owner-decisions)); what she has not yet seen is this written plan and its [statements](statements.md). D15 is open. Next: the owner reads the statements and answers D15 (needed before CC-5) and D14; the scope PR records her answers here; only then does the plan become `Accepted`.

**Origin.** This plan is Plan 18's former Phase 0 (the commit contract), moved here whole on 18 November 2026 with the deltas of the save-category design applied, because the owner asked whether stability should come before extensibility and the answer was that the two are separable and stability goes first. Plan 18 phase 1 puts every gesture on the save path and would inherit every flaw in it; the stable base needs nothing from extensibility. The earlier decision to extend Plan 18 (the main session's, on the advice of the near-instant review, because Plan 18 was queued, unowned and #852 already pointed there) is superseded by D9: the work now has its own plan, owner, release and "done". Sources: the reviews and profiles of 17 and 18 November held by the Release 14 Lead (`fable-near-instant-review.md`, `fable-edit-refusals-deeper.md`, `plan-near-instant-commits.md` Rev 2, `near-instant-facts.md`, `sonnet-commit-profile.md`, `live-check-almost-ready.md`, `sonnet-unnamed-edits-on-shot-timelines.md`) and, new, the save-failures evidence pack, `fable-save-category-design.md`, `fable-stability-sequencing.md` and `sonnet-commit-profile-r14.md`. They are private and not committed, so what matters is restated here as shapes and counts. Nothing in this plan copies content from the owner's timeline.

**Prior art:** The category is already named, traced and partly fixed once; this plan reuses and does not re-derive.

- *The incidents.* Sixteen failures of saving on one long-lived timeline in one week (I-1 to I-16, table below). Earlier issues: [#839](https://github.com/banodoco/astrid-dev/issues/839) (the equality bridge), [#842](https://github.com/banodoco/astrid-dev/issues/842) (whole-head re-judging), [#826](https://github.com/banodoco/astrid-dev/issues/826) and [#846](https://github.com/banodoco/astrid-dev/issues/846) (cost), [#732](https://github.com/banodoco/astrid-dev/issues/732) (the stuck state), [#847](https://github.com/banodoco/astrid-dev/issues/847) (the same 400 at first start), Plan 54's principle "verify at a trust boundary once; inside a job, carry the digest" (written for generation jobs, per job and not per history), and `releases/12/decisions.md` (a sticky refusal fixed once at one site). Plan 59's handover records the writer-side lesson: "Data was accepted early and refused late." None made it a mechanism, and no test held a document with a history or with size.
- *The measured shape.* One timeline with shots, about 8 records and a closure of 7 shots, about 1 MB per revision and about 1,100 distinct stored objects. An uncontended add-media commit took 187 seconds (176 live); profiled, 280 seconds, of which about 190 were CAS re-verification (59 history read passes, 32,686 confirmations, 23,268 physical reads, the Agent loading the base 11 times) and about 80 were legacy timing probes. History was only 3 entries, so the reservation scan (2 + 3N closure loads per attempt) grows by three loads per edit. A clip move was refused after 85 seconds for a legacy declaration it never touched. The editor polls about 110 requests a minute per tab; a history GET took 8 to 9 seconds while holding the store mutex.
- *The state of the editor.* A change can be in an outbox owner, a session copy, a draft slot and six React flags at once; a reply can be classed nine ways by status code; eight statuses and at least thirteen throws stand between an edit and the queue; there are six save surfaces. Live findings of 18 November (owner's browser on :2400, read from IndexedDB `astrid.command-outbox`; shapes and sizes only): outbox records are 2.6 to 10.6 MB each, because whole before and after documents are stored per intent; two editor sessions on one origin each held a pending intent on the same head, so the second gets `stale_head`, and `useTimelineSave.ts:395-399` reportedly throws when more than one owner has pending work at recovery (unverified: CC-5 reproduces it first).

**The incidents, and the invariant that prevents each** (invariants numbered as in [plan.md](plan.md#outcome-and-scope)):

| Incident | Prevented by | How |
| --- | --- | --- |
| I-1 slow saves, 60 s cut, wait for a replay | 5, 2 | Work is bounded by count. A cut is `unavailable`: same bytes, same key, replay |
| I-2 "inputs changed" became permanent | 2 | The server says `unavailable`; the client cannot call it anything else |
| I-3 drop refused because the head moved | 4 | The drop's guard reads its track and shot only; later the drop is an intent the server judges (Plan 18 TL-10) |
| I-4 "original verified authoring head is unavailable" | 1, 3 | No second document to disagree with. A moved head is `moved` |
| I-5 "Wait for retained dependent saves" | 3 | Adding to the queue has no precondition. The throw is deleted |
| I-6 banner after reload; Discard does nothing | 1, 3 | One row, one bar, the same before and after a reload. Discard empties the row |
| I-7 409 retried for ever | 4, 2 | The guard no longer fires on lifecycle. An unreadable reply is `refused` |
| I-8 upload fails during a save | 5, 2, 1 | No bulk re-download. A cut upload is `unavailable` and is sent again from the queue (CC-10) |
| I-9 two tabs block each other | 1 | One row per timeline; both tabs read it; one sends |
| I-10 a commit per keystroke | 1 | One gesture, one record |
| I-11 move refused for an untouched `gap_after_s` | 4 | Signed by its own value, through the delta gate |
| I-12 half association written, then refused | 4 | One admission function for every writer |
| I-13 accepted commit loses its reply (`ENOBUFS`) | 5, 2 | The writer survives `ENOBUFS`. If a reply is still lost, it is `unavailable` and replays |
| I-14 `/objects/` 503s and stalls | 5 | Bytes once, through one reader |
| I-15 badge stuck on "Saving" | 1 | The badge is the function of the row |
| I-16 stale owner never sent, never dropped | 1, 3 | No owners. A row with nothing to send does not exist |

**Approach.** Make the principle a mechanism, with a typed boundary, one model test and counts that may only fall: a counted scaling test (CC-1) so no cost can scale with history again; a rule registry and one delta gate (CC-3) so no rule can re-judge an accepted head; four outcomes and one decoder (CC-4) and one queue, one bar and a way out (CC-5) so a disagreement has an outcome other than a permanent refusal; one write-time admission (CC-6) so a writer cannot store what a reader refuses; one corpus (CC-7) that runs all of it; bounded transport (CC-9) and uploads as queue records (CC-10). Enforcement:

1. **The boundary.** `send(request): Promise<Outcome>` is the only function in the editor that sees an HTTP status. `Outcome` is a four-member union generated from the Agent's list. A lint fails on `ApiError`, `.status` or a match on error text anywhere under `tools/video-editor/`.
2. **The model test, one file.** A scripted `send` plays every outcome at every queue position, a lost reply, a cut request, a reload between any two steps and a second tab. After every step it asserts: adding an edit never throws; what the screen shows equals the function of the row; every record is accepted, in the "not saved" list, or queued behind an `unavailable`; Dismiss and Discard always leave a saved state, and the next edit saves. A new state or surface cannot be added without this test failing, because the screen is compared with the function.
3. **Counts in the one ratchet file, held at zero or falling:** IndexedDB or `localStorage` opened for save state outside the queue module; `throw` reachable from adding to the queue; `fetch` of an object URL outside the reader; object GETs per gesture on the corpus (adding one object: that object only); the computation counters.
4. **Server side.** The generated grid: every operation on every corpus head introduces no finding. The corpus gains a selection whose lifecycle advanced between select and commit, and a head with many audio sources. A route-table test sends every mutating route twice with one key and expects one effect. A writer test delivers a reply through a socket that raises `ENOBUFS`.

Alternatives rejected: a cache keyed by base revision (every ordinary edit creates a new base, so it only helps retries); a second resolver for the legacy probes called "equivalent" (the pattern the 17 November review named; the collect pass reuses the evaluator and the old probe stays as a test oracle); a clock gate (the owner forbids it); keeping this inside Plan 18 as a phase (superseded by D9: one cause, one home, one release); **pulling TL-5 (the document as head plus queue) in** (it is the heart of Plan 18's command layer and, with TL-6 to TL-11, about 60 days of conversions: it would make "stability" a 90-day project and delay the result now; with the upload half of TL-10 moved in as CC-10, this plan completes all five invariants in the form a person can observe, and what remains for phase 1 is the deletion of one stored copy); doing extensibility first (each conversion would be built against code that is then deleted, every pack rule could refuse an old document, the gesture matrix would be generated twice, and the owner could not edit dependably for the length of phase 1).

**Challenge:** Reviewed — Plan 18's Phase 0 had an independent review by Opus (merge with edits; 18 November 2026; the report is `opus-phase0-review.md`, held by the Release 14 Lead), and its seven required edits are in this pack. The save-category design and the sequencing note are Fable's, read against the code and the 16 incidents; they are the source of the deltas applied here. Next: the main thread reviews this pack; a further fresh reviewer may read it against the code, briefed to build as little as possible, before the owner's answers.

**Proof and limits:** Completion is the list in [plan.md](plan.md#completion), each item guarded by a named test. Limits: nothing here was built or run; the stuck states were read from code, the pack and the map. The 37-day estimate is task arithmetic on Plan 18's own figures, not a bottom-up estimate. "About 3 s after the `_reference_basis` fix" is 33% of the measured 9 s and has not been measured. Whether `discardScope` can delete a row another tab holds under its Web Lock is unproven (the claim's generation check should fence the stale tab, reported at `commitOutbox.ts:272-273`; the model test's two-tab case must show it). Whether a `File` stored in the queue row survives a reload in every supported browser is unconfirmed: CC-10 starts by confirming it.

**Review rounds:** Recommended: one (R0, at the end, before any publishing task), because the plan changes the save path of all three repositories. A review stop after CC-4 and CC-5 was considered and not recommended: the model test is the proof of those two, and R0 reads it. Pending the owner's agreement.

**Run start:** Pending — no run is authorized. The plan's branches are cut from `release/14/main` once today's save fixes have landed there. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking, what needs her go, and the advisor session. **Priority:** recommended to sit ahead of Plan 18 in [priority.md](../priority.md) (the owner or the orchestrator adds it; a new plan stays out of that file until then).

### What Release 14 already ships

The save fixes already merged on Release 14 (N1 to N12, the `_reference_basis` fix, Runtime #61 to #63, App #299 to #300) carry the behaviour (no endless retry, one bar, Discard always works, no lost reply, a drop survives a save); this plan carries the structure. The test for each part: does it change what is stored in the browser, what goes over the wire, or what the owner sees happen to their work? If so, it needs the corpus and the model test under it first, and those are this plan's first tasks.

| Item | What | Where it is in Release 14 | What this plan does with it |
| --- | --- | --- | --- |
| N1 | The selected-media guard signs identity and bytes only (object id, size, media type, variant id); `lifecycle`, `durability` and `provenance` leave the digest | Runtime #61 (merged), `runtime_protocol/timeline_commit_port.py:1047-1065` | End design (invariant 4); CC-3 and CC-6 name the selected-media digest as a signed guard |
| N2 | No 409 is sent again with the same bytes unless the server says so (`head_busy`, `runtime_unavailable`); every other 409 becomes a dischargeable `conflict` | App #299 (merged), `src/integrations/runtime/client.ts` | CC-4 builds the full decoder, with its total default and the three `>= 500` copies folded in |
| N3 | Discard is total: `discardScope(scope)` deletes every owner row for the timeline in one transaction, for any state | App, `commands/commitOutbox.ts`, `commands/localSaveSession.ts`, `hooks/useTimelineSave.ts` | End design; `discardScope` becomes "clear the queue row" |
| N4 | One bar replaces the save notice, the recovery banner, the conflict bar, the conflict dialog, the watchdog banner and the shot-preview copy | App, `components/TimelineEditorShellCore.tsx`, `components/ShotTimelinePreview.tsx` | End design; its input changes from six flags to one row (CC-5) |
| N5 | One reply writer for both paths: 64 KiB pieces; on `ENOBUFS` wait for the socket and continue | Runtime, `runtime_protocol/server.py` | End design (invariant 5); CC-9 adds the writer test |
| N6 | Warm each object URL once per session | App, `compositions/AudioAnalysisProvider.tsx` | **Stopgap.** The set moves into CC-9's one object reader |
| N7 | Position fields commit at the end of the edit | App, `components/PropertiesPanel/ClipPanelBody.tsx` | End design (one gesture, one record) |
| N8 | While retained saves replay, the edit is declined by the bar, not by exception text | App, `commands/localSaveSession.ts:350`, `:353` | **Stopgap.** CC-5 deletes both throws: a new edit queues behind |
| N9 | An unavailable save retries by itself with backoff; "Try again" retries at once; no owner with nothing to send is kept | App, `commands/localSaveSession.ts` | End design |
| N10 | Health is served without `store._mutex` | Runtime, `runtime_protocol/server.py` | End design; CC-9 adds object reads |
| N11 | `timeline_commit_timing` logged for every commit; `runtime.log` timestamped; the proxy's stderr written to `logs/editor.log` | Runtime, App | End design (evidence) |
| N12 | A failed upload removes its "uploading" placeholder clip | App, `hooks/useExternalDrop.ts` | **Stopgap.** CC-10 makes uploads queue records |
| `_reference_basis` fix | The measured 67% of the commit | Agent; the old probe stays as the test oracle | CC-2 starts from the profile and takes what is left |
| Model-test seed | The scripted `send` with the cases true today (Discard, reload, two retained owners, the next edit saves) | App, `commands/localSaveSession.discard.test.ts` | CC-5a grows it first; nothing is thrown away |

The Release 14 profile (Agent `458d9d51`, Runtime `d725811`, 18 November, on the owner's timeline cloned): the Runtime commit is about 9 s idle (was 187 s, about 21 times faster), 67% of it in `_legacy_exemptions` through `_reference_basis` (400 calls, each deep-copying the shot clips and source documents; 25.6M `deepcopy` calls). CAS re-hashing is gone (about 0.4 s). History reads are 0.07 to 0.2 s warm. **An import does wait on a commit:** 5.0 to 6.7 s behind `store._mutex` (idle 0.1 s), and a commit that overlaps an import takes 22 to 26 s against 9 s sequential (mechanism unproven). So a save in progress does delay an upload, but the failure itself was the cut connection, not the wait. The fix of the 67% is in Release 14; CC-2 starts from the profile and the import wait belongs to CC-9.

What Release 14 does not give: a guarantee that the category cannot come back (see [plan.md](plan.md#outcome-and-scope)). What the owner sees on Release 14 (inferred, not measured): saves in a few seconds, not minutes; a drop during a save works; nothing retries for ever; one bar with Try again and Discard, the same after a reload; Discard always clears.

### What gets deleted

| Deleted | Where | By invariant |
| --- | --- | --- |
| The draft database and everything that reads it | `data/timelineDraftIndexedDb.ts`; `recoveryDraft`, `recoveredAsDirty`, `offerRecovery`, `retryRecoveredDraft`, `discardRecoveredDraft` in `useTimelineSave.ts` | 1 |
| Owners: several rows per timeline, `recoverableOwners`, `recover(ownerId)`, the recovery loop | `commitOutbox.ts:153-157`, `localSaveSession.ts:343-346`, `:431-445`, `useTimelineSave.ts:380-405` | 1 |
| The session's own document copies and the equality bridge | `LocalSave.before` and `after`, `same(...)` at `localSaveSession.ts:357`, `:390`; `replaying` | 1 |
| Six save flags in React | `saveError`, `isConflictExhausted`, `schemaIncompatible`, `watchdogTripped`, `watchdogReason`, `saveStatus` | 1 |
| Five of six surfaces | save notice, recovery banner, conflict bar, conflict dialog, watchdog banner, the shot-preview copy | 1 |
| The upload's private recovery | `persistMediaImportOperation`, `recoverMediaImportAfterLostAck` (`dataProvider.ts:1718`, `:1735-1765`); the "Failed to save asset" toast | 1, 2 |
| `RuntimeCommitFailureKind` (nine kinds) and its three call-site preludes | `client.ts:307-345` | 2 |
| `isRuntimeConflict`, `isRuntimeCanonicalPayloadConflict`, `permanentRejectionMessage` | `client.ts:291`, `:352`; `localSaveSession.ts:67-77` | 2 |
| `retryable` as a per-reason flag | the earlier CC-4 and Plan 18 TL-4 | 2 (the outcome carries it) |
| Statuses `retry`, `conflict`, `blocked`, `recovery`, `error` as modes | `localSaveSession.ts:30` | 3 |
| `rollback`'s retained-chain branch, `discharge('keep' \| 'latest')`, the single-track-label exception | `localSaveSession.ts:181-206`, `:408-430`, `:88-103` | 3 |
| Every throw that refuses an edit or a send for an earlier state (seven) | `localSaveSession.ts:132`, `:350`, `:353`, `:400`, `:436`; `commitOutbox.ts:496`, `:501` | 3 |
| The whole-record selection digest; the head-equality test on a drop (Plan 18 TL-10 deletes the latter) | `timeline_commit_port.py:1061`; `useAssetManagement.ts:330` | 4 |
| Three private fetchers of object bytes and four URL builders | `AudioAnalysisProvider.tsx:149-181`, `useWaveformData.ts:29-50`, `audioAnalysisClient.ts:188`; `client.ts:1216`, `bridgeMediaUrl.ts:41`, `mediaRoutes.ts:27`, `dataProvider.ts:1651` | 5 |

Line numbers are from the 18 November reading and will have moved: re-check against the code at dispatch. Plan 18's TL-12 deletes whatever of this remains when it runs.

### Issue ledger

States were read from the GitHub API on 18 November 2026. "Closes" means the plan's end-state check for it passes and the Lead closes the issue then; the plan does not close issues itself.

| Issue | State now | This plan | How |
| --- | --- | --- | --- |
| [#826](https://github.com/banodoco/astrid-dev/issues/826) history reads pay for the whole history; every write clears the verification cache | open | closes | CC-1, CC-2, check P0-1 (the verification-cost part is already on the Runtime's `p59/revision-listing-perf`) |
| [#846](https://github.com/banodoco/astrid-dev/issues/846) every refusal clears the replay memo | open | closes | CC-2, check P0-1 (zero re-hashes after a refusal) |
| [#852](https://github.com/banodoco/astrid-dev/issues/852) the editor sends intent and adopts the head | open | **states and ratchets; closes at Plan 18 TL-12** | this plan cannot close it alone: the editor half is Plan 18's TL-3b, TL-5, TL-6 to TL-12; CC-8 stops the bridge growing meanwhile |
| [#732](https://github.com/banodoco/astrid-dev/issues/732) a rejected save leaves the editor stuck | open (labelled `planned`, `release:14`; owner-blocked) | closes | CC-5, check P0-4; `release/14/save-rejections` and `rejected-discharge` land the part for `too_large` and both buttons |
| [#842](https://github.com/banodoco/astrid-dev/issues/842) validation re-judges whole heads | closed 17 November | **reopen as the mechanism** | CC-3, check P0-2: the principle ("refused only for problems it introduces or touches") closed after four rules; the registry makes it hold for the next rule. The Lead reopens it with a comment linking this plan when the scope PR merges |
| [#847](https://github.com/banodoco/astrid-dev/issues/847) first start fails with "inputs changed" | open | links | CC-4 logs which component moved and returns a retryable reason; the trace is Plan 61 RB-9 |
| [#839](https://github.com/banodoco/astrid-dev/issues/839) the equality bridge | closed 17 November | links | the interim fix is Release 14's `release/14/edit-refusals`; CC-8 ratchets; Plan 18's TL-12 retires the bridge |
| [#720](https://github.com/banodoco/astrid-dev/issues/720) a world on the timeline makes a 413 save that retries forever | open | links | the retry class is CC-4's (`too_large` is `refused`, so never retried); the scene-by-reference removal is Release 14's |
| [#745](https://github.com/banodoco/astrid-dev/issues/745) multi-shot fork rejects valid per-command parents | open, `plan:59` | links | the same habit (re-prove against the original base); Plan 59 owns the fix; CC-3's grid is where a fix adds its row |
| [#769](https://github.com/banodoco/astrid-dev/issues/769) commit accepts properties that render refuses | open | links | Plan 59's asset-admission contract owns "renderable subset"; CC-6 calls it when it lands, and its identity fields are the one definition N1 shares |

### Deferred

| Item | Decision | Reason |
| --- | --- | --- |
| The editor's poll rate (about 110 requests a minute per tab) | Deferred; the cost is bounded by CC-2 | After CC-2 a GET does no hashing and clears no trust, proven by count. Lowering the rate needs the editor to subscribe to the head it adopts, which is Plan 18's send-and-adopt (TL-5). Re-measure after CC-2 and file an issue if the Runtime is still busy |
| Persisting verified trust across restarts (cold start) | **Not deferred: owner decision D14**; CC-2 bounds it by count meanwhile | A cold start hashes each object of the requested closure once and only those; persisting trust is a trust-model choice for the owner |
| The roughly 1 MB snapshot stored per revision | Deferred; file an issue | The contract bounds work, not disk; the work is bounded by the head, which is one pass. Delta storage is a storage-format change with a migration, which this plan does not need |
| The residue under one second | Deferred to a re-profile after CC-2 | No number in the profile shows under one second; "low seconds" is the honest expectation. Wall time on the owner's timeline is recorded as evidence, not gated. The editor's 500 ms save debounce is a separate floor |
| Waveform peaks stored beside the object | Deferred | CC-9 makes one reader fetch each object once; storing derived peaks is a separate storage question |
| The two proxy hops of the local install | Deferred | Each is a second mechanism around a cause CC-9 and N5 remove; proxy limits, connection pooling and a longer proxy timeout are not built |
| Metadata reads other than object and health sharing the commit's mutex | Deferred | CC-9 takes object and health reads off the lock; the rest is re-measured after CC-9 |

## Owner decisions

Decision ids keep the numbers they had in [Plan 18](../18-timeline-editing/inputs.md#owner-decisions) so references stay valid. D15 is new.

**D9 — Decided, 18 November 2026: the release for this plan is Release 14.** Source: the owner, in chat, 18 November 2026, after asking whether stability should come before the extensibility work: "SO DO WE HAVE A STABILITY PROJECT? HAVE WE PUSHED OUR CURRENT WORK TO E.G. RELEASE/15/MAIN SO IT CAN BUILD ON TOP", and then, correcting the release: "SORRY, FOR RELEASE 14 I MEANT". Earlier the same day, about the week's timeline-editing failures, she had said: "get it fixed now and PROPERLY fixed in the follow up plan". The "now" is Release 14's fix branches; this plan is the follow-up, and it goes before Plan 18's phase 1. Reason: Release 14's theme is already "Stability and elegance", and this fits it. Cost, stated plainly: it adds about 15 elapsed days (about 37 engineering days, about 33 once the merged N-items are counted) to Release 14, per the stability sequencing note, and the plan changes the save path of all three repositories. The earlier proposals of Release 15 and Release 17 are withdrawn.

**D10 — Open (owner): the corpus data.** Recommended: CC-7 builds synthetic documents to the recorded shapes and counts, with no owner content. Both new shapes (a selection whose lifecycle advanced; a head with many audio sources) are synthetic. Optionally the owner supplies one anonymised export of a long-lived timeline (titles, text, asset names and paths removed, shapes and counts kept) for Plan 18's TL-15b. Never a raw copy, and never committed to this public repository without the owner's say.

**D11 — Main-session ruling, to confirm: what `stale_head` does.** For an intent command that names its own reads (the named-op path), the App re-reads the head and re-sends with a new expected head and the same key (`moved`); for a raw document patch that cannot be applied to the new head, the change is `refused` and appears in the same bar, and the conflict card goes. Reason: an intent is re-evaluated by the Agent against the new head; a patch is a whole-document claim that the other writer may have invalidated.

**D12 — Main-session ruling, to confirm: the contract is checked by counts, with no clock.** Per the owner's rule that tests carry no time limits. Live wall time is recorded as evidence only.

**D13 — Session ruling, 18 November 2026** (updated after the Opus review, "merge with edits", and the coordinator's ruling, both weighed): one rule home (CC-3's registry; `validate_final_candidate` runs the registered rules under the delta gate, no second list), and one closed outcome and refusal list owned by the Agent with one wording home (CC-4 creates it, Plan 18's TL-4 extends it). On registration, the phase 1 session wanted one shared door for ops and rules and Opus wanted none here; the middle path is that CC-3 builds `register_rule` for built-in rules only and drops the shared `op` kind. When packs gain registration (Plan 18's TL-1 designs it, TL-3r builds it), pack rules go through that same extension surface, under the same delta gate, calling CC-3's `register_rule`: there is never a second door. CC-8's temporary ratchet stays; Plan 18's TL-12 check replaces it.

**D14 — Open (owner): persist verified trust across restarts (cold start).** Recommended: persist each verified object's `file_identity` (dev, inode, size, `mtime_ns`, `ctime_ns`) in the store database, so a restart does not re-hash every media object (about 8 s on one timeline, 2.2 GB on this realm, growing with media bytes; [#847](https://github.com/banodoco/astrid-dev/issues/847) first start lives here). It is the largest uncovered cost: every restart re-hashes. What is given up is corruption that changes no file metadata, across restarts; a running process already gives that up. Until decided, CC-2 hashes each object of the requested closure once and only those.

**D15 — Open (owner), new: what a refused change looks like.** Options: (1) **remove it from the timeline and list it with Restore and Dismiss** (recommended); (2) leave it visible on the timeline and marked. Effect of (1): on `refused`, the record and its dependents move out of the queue into a "not saved" list in the same row; the document returns to the head plus what is left; one bar says what and why. It is what `too_large` does today (`discardOversized`, `localSaveSession.ts:160-170`), and it is the only choice under which the editor is never blocked. Restore needs the row change. Without Restore, (1) discards work, so the two ship together. **This is the only decision on the critical path: it is needed before CC-5 starts.** Ask it now.

Decisions table (bold is the recommendation the plan proceeds on):

| ID | Decision | Status |
| --- | --- | --- |
| D9 | Release for this plan | **Decided: Release 14** (the owner, 18 November 2026) |
| D10 | Corpus data | **Open (owner).** Recommended synthetic, plus optionally one anonymised export |
| D11 | What `stale_head` does | **Main-session ruling** (above), to confirm |
| D12 | Counts, no clock | **Main-session ruling**; the owner's standing rule |
| D13 | One rule home; one refusal list; one door | **Session ruling** (above) |
| D14 | Persist verified trust across restarts | **Open (owner).** Recommended: persist `file_identity` |
| D15 | What a refused change looks like | **Open (owner).** Recommended: remove from the timeline and list with Restore. Needed before CC-5 |

Plan 18 keeps D1 to D8 (D4, the release for phase 1, now reads "the release after this plan's").

## Source identities

Before code work, record the actual repository, ref and SHA for each. This plan changes three product repositories and astrid-dev. Branches follow the rule for a plan in Release 14 or later: `release/14/plan-63` in each repository the plan changes (astrid-app, astrid-runtime, astrid-agent), cut from that repository's `release/14/main` once today's save fixes have landed there.

| Repository | Starting branch + SHA | Retained work / donor SHAs / unpublished changes | Verified predecessor output | Candidate branch | Intended destination |
|---|---|---|---|---|---|
| astrid-app | TBD: `release/14/main` after the save fixes land | Merged on Release 14: N2 to N4, N6 to N9, N12 (App #299 to #300), `release/14/save-recovery`, `rejected-discharge` (`88045a78c`, astrid-app #295), `save-rejections` (#720, `ba20e7da`, merged), `drop-placement`; the model-test seed | N1 to N12 and the seed on `release/14/main` | `release/14/plan-63` | `release/14/main` |
| astrid-agent | TBD: `release/14/main` | `release/14/legacy-probes`, `commit-loads`, `edit-refusals` (#842, `d5f90a4b`), #393 (merged `b126d7482`), the `_reference_basis` fix | the uniform baseline rule (#842) | `release/14/plan-63` | `release/14/main` |
| astrid-runtime | TBD: `release/14/main` | `release/14/commit-cost` (cut from `519b404`), N1 (#61), N5, N10, N11 (`release/14/transport`) | N1, N5, N10, N11 | `release/14/plan-63` | `release/14/main` |
| astrid-dev | `origin/main` | this pack | None | `plan/63-dependable-saving` | `main` by the scope PR |

Release 14 fix branches, as recorded on 18 November (identities to be recorded at CC-1; none is a retained donor until merged; the rejected-discharge PR is #295 in the plan's earlier table and #294 in its earlier source list, same SHA `88045a78c`, and CC-1 settles which):

| Repository | Branch or PR | What it carries (intent, per Rev 2) |
| --- | --- | --- |
| astrid-runtime | `release/14/commit-cost` (cut from `519b404`) | CAS verify-once by file identity; trust survives memo clears; "inputs changed" as `head_busy`, the one refusal a client retries, with the moved component logged |
| astrid-agent | `release/14/legacy-probes` (cut from `b126d7482`) | one collect pass on base and candidate judged by `split_findings` (only if a differential against the old probe holds on every corpus head, else the probe stays and the difference goes to the owner); unsupported declarations signed by value; the `gap_after_s` probe test |
| astrid-agent | `release/14/commit-loads` (cut from `b126d7482`) | verified document memoised per commit; reserved identities per accepted revision |
| astrid-agent | #393, merged `b126d7482` | an incomplete catalog association judged only when a change introduces or touches it (the reader side) |
| astrid-app | `release/14/rejected-discharge` (cut from `a4f765fbb`) | `stale_head` takes the conflict and rebase path; both conflict buttons discharge a rejected change through the local save session, including after a reload, when the rejected entry's base is gone and when several owners have retained work |
| astrid-app | `release/14/drop-placement` (into plan-59) | the drop guard's OR-chain split into named reasons; it refuses only when the target is really gone |
| astrid-app | `release/14/save-rejections` (#720, `ba20e7da`, merged) | a permanently rejected save (413) is not retried forever; a banner and a discard for `too_large` |
| astrid-agent | `release/14/edit-refusals` (#842, `d5f90a4b`) | the uniform baseline rule, one helper called by every rule |

## References

- Plan 18: [plan](../18-timeline-editing/plan.md), [tasks](../18-timeline-editing/tasks.md), [inputs](../18-timeline-editing/inputs.md); Phase 0 lived there until 18 November 2026.
- Issues: [#826](https://github.com/banodoco/astrid-dev/issues/826), [#846](https://github.com/banodoco/astrid-dev/issues/846), [#732](https://github.com/banodoco/astrid-dev/issues/732), [#847](https://github.com/banodoco/astrid-dev/issues/847), [#720](https://github.com/banodoco/astrid-dev/issues/720), [#745](https://github.com/banodoco/astrid-dev/issues/745), [#769](https://github.com/banodoco/astrid-dev/issues/769), [#838](https://github.com/banodoco/astrid-dev/issues/838), [#839](https://github.com/banodoco/astrid-dev/issues/839), [#842](https://github.com/banodoco/astrid-dev/issues/842), [#852](https://github.com/banodoco/astrid-dev/issues/852).
- Principle: [Plan 54](../54-warm-latency/plan.md) "Verify at a trust boundary once"; writer-side lesson: [Plan 59 handover](../59-into-the-minkhole-proof-point/handover.md).
- Release 14: [`releases/14.md`](../../releases/14.md); gap: [F-001](../../vision/gaps/F-001-platform-reliability.md).
- Reviews and profiles of 17 and 18 November (the save-failures evidence pack, the save-category design, the stability sequencing, the Release 14 commit profile, the Opus Phase 0 review): held by the Release 14 Lead; their findings are summarised above.
