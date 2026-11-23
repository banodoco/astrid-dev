## Final proof on the landing candidate (23 November 2026)

[Plan](plan.md) · [Tasks](tasks.md) · [Evidence](evidence/live-proof-final/README.md)

Status: the offline and SDK-path proof on the candidate is recorded. The hosted CI comparison is pending. The live online outcome checks, the negatives, the heavy 136-clip fixture, the 11.0 s still and the Codex chat-agent step are not run; they move to a release-freeze item. The statement that the final proof was pending in [tasks](tasks.md) (R1.8) and [handover](handover.md) is superseded by this section. The 22 November record below is kept as history.

### Receipts

| Item | Value | Source |
| --- | --- | --- |
| Candidate | Agent `release/15/plan-78` head `64cecdae9f679537f4a6dc82e5102e53b6943ef7`: Plan 78 `c52a4ccf` after merging Plan 40's landing `8fdf6615` as `ef826edf`, merged with the timeline first cut `b324d7c1`. Runtime lock `737843e9cb92c565c266452dde540832ee2c745b`. | [tasks](tasks.md) |
| Hosted runs | Dispatched 23 November 14:55 UTC on that exact head: [CI](https://github.com/banodoco/astrid-agent/actions/runs/45199409761) and [Lanes](https://github.com/banodoco/astrid-agent/actions/runs/45199416493). By-test-id comparison with the baseline: **pending**. No result is claimed. | GitHub run links |
| Overlap reads | `astrid/core/pack/discovery.py` after the Plan 40 and Plan 81 landings: PASS on four points. Timeline first-cut merge (store.py verified-reader GET, remote client additions, both runtime locks `53a035ba` to `737843e9` with their literal-pin tests, Plan 78 files byte-identical): PASS. Fresh read-only reviewers. | [tasks](tasks.md), [handover](handover.md) |
| Live stack | Isolated install `/root/codex/le4/isolated3` (Agent `64cecdae`, Runtime `737843e9`). Runtime PID 543, instance `2a4eb62990164f8ab879979ac6770fc3`, unchanged throughout. Registry warmed first (motion elements absent). Motion pack installed after Runtime start, transaction `bf52b99b218548498066939e0ebb2ed7`, PID unchanged. Pack refresh completed: `.group.json` `refresh: null`, revision 3, written 9 s after the install. | [run report](evidence/live-proof-final/report-small.md) |
| Throttle on this head | 136 titles 20.675 ms, 0 rediscoveries, one stat per root (the manager's earlier run: 20.992 ms). | [throttle log](evidence/live-proof-final/throttle-host.log) |
| Project | `le4-small1`, timeline `small1`, 4-clip seed `txn-1957160531d742acafeaf7b76ea1ccc1`; history reads after seed 5 of 5 pass. | [report](evidence/live-proof-final/report-small.md) |
| Mixed commit | Through the public SDK path, ONE commit. Receipt `txn-8e764a2d932340299d0b568793cbdf8d`; 6 commands (3 `clip.set-element` with refs gold/cyan/gold, 3 `doc.patch`). Exactly ONE new history row, equal to the receipt id. Accepted head `authoring-parent-revision-6c55dabb0eca3ceac3fa12354d883311817bbda7de9a44362f8b346a1ce425ad`. | [receipt](evidence/live-proof-final/commit-small1-receipt.json), [rows](evidence/live-proof-final/rows-after-commit.json) |
| Forks admitted live | `le4-gold` `sha256:d8eaaf4855528d7c36e434a3c7ef07a73229f6aee70599e03d8fc1b41cf74fb8`; `le4-cyan` `sha256:dcb5e113e7016f7c0a0792a66364be41a158b2a2a536c26b3d7b49aaaebed6ea`; packId `project_4944f3baaa40481ba360`. The three retargeted clips use these forks. | [refs](evidence/live-proof-final/refs-small1.json) |
| Other checks | Untouched control clip identical to its seed definition; one title added; page marker `le4-small1-1795445924341` survived. | [outcome](evidence/live-proof-final/outcome-small1.json) |
| Offline outcome checks | 14 of 14 pass, computed from the accepted response and the one passing post-commit history read. | [outcome](evidence/live-proof-final/outcome-small1.json) |
| Timings | Commit 5.868 s (SDK-measured). First-visible upper bound 33.165 s after commit end, from page text; not a visual confirmation. | [report](evidence/live-proof-final/report-small.md) |

**Visuals (stills are preview-only crops):** the control text card is black at 7.5 s both before and after the commit: `before-7.5.png` mean 33.6 and `after-7.5.png` mean 33.6. NEW TITLE 1 is black at 10.5 s. Both stills are 0.5 s into their clips. The text card's own entrance is 18 frames (0.6 s at 30 fps) in the installed timeline-composition package (`chunk-BEYNBITW.js` line 14; the type-on reveal in `chunk-VHNHAQUG.js` lines 175-182), so nothing shows before frame 18. The Lead ruled these not defects: "fixture/fade timing". The earlier proof showed NEW TITLE 1 at 11.0 s. The extra stills at 8.0, 8.5, 11.0 and 11.4 s were not taken: the page controller has a fixed capture list, and a new page would break the one-page rule. The cyan slot card does not draw its label in this install: the installed `am-footage` file draws the fixed `SLOT ... TO FILM` text in its `if (!url) {` branch (line 203, text at line 217) and does not read `label` there. The earlier proof's fork came from a different source, so its card showed REHEARSAL 2. The label parameter is stored correctly in the commit. These are element-source differences, not the commit. Visual notes: [evidence README](evidence/live-proof-final/README.md).

**D2 (a fresh install gets the motion pack) is not delivered by Plan 78.** The fix row sits under [#1525](https://github.com/banodoco/astrid-dev/issues/1525). The App `packs` patch lands in Plan 78's slot after the Agent lands, as a PR into astrid-app `release/15/main` with `release` left at 15 and the guard run against published main quoted.

### Not done, moved to a release-freeze item

The Release Lead's ruling, 23 November about 15:07 UTC: "Plan 78 lands on the offline proof ... plus the hosted CI comparison, recorded as such. The live outcome checks, the negatives and the 11.0 s still move to a release-freeze item: run on the same stack with the save run's fixed Runtime overlaid, before Release 15 is qualified."

The freeze item covers: the live online outcome checks; all negatives of the LE-4 card; the heavy 136-clip fixture run; the 11.0 s still; and the Codex chat-agent step. The owner's Codex limit (until 28 November) made the editor's chat-agent step impossible. Per the owner's rule, relayed by the Release Lead on 23 November about 13:35 UTC, the live proof runs on the exact head before hosted CI. The chat-agent step is recorded as `re-run when Codex returns` and is not substituted.

Reason: a Runtime defect, not Plan 78. After a clip-bearing commit, the next verified history read or `Timeline.open` is refused with `head_busy` ("accepted commit inputs changed during verification"). The pack host's idle claim poll writes a temporary-table row on the live connection, which moves SQLite `total_changes` during a long replay (`runtime_protocol/timeline_commit_store.py:1355-1357`; `service.py:2753-2759`; `generic_host.py:13841-13844`). It reproduces on plain titles with no pack element. Pausing the pack host for 9 s, both reads passed inside the pause and were refused again after it ([astrid-dev PR 1676](https://github.com/banodoco/astrid-dev/pull/1676), [PR 1677](https://github.com/banodoco/astrid-dev/pull/1677); folder `plans/77-saving-holds-on-a-heavy-timeline/evidence/2026-11-23-head-busy/`). It is owned by the Plan 77 save run (SV-2). In this run, `Timeline.open` after the commit was refused with `head_busy` on 10 of 10 attempts, and the pack-host pause windows were refused by the permission system, so no live read ran inside a window. The run report marks step 4 FAIL for this reason.

### Limits

- One synthetic small project on one local stack. It shows nothing about hosted isolation, shared use, or every project size.
- The offline checks are computed from the accepted response and one passing history read. The live online checks did not run.
- The hosted CI comparison is pending; no by-test-id result is claimed.
- D2 is not delivered by Plan 78 ([#1525](https://github.com/banodoco/astrid-dev/issues/1525)).
- The stills are preview-only crops; they are not visual confirmation of page continuity.
- The run used the owner's Codex login folder through `CODEX_HOME` on her earlier instruction. The run report records that the folder was not read by the worker.

## LE-4 live proof, 22 November 2026 (earlier run, superseded for the final proof)

[Plan](plan.md) · [Tasks](tasks.md)

The editor's chat agent edited a disposable synthetic project on one local machine. The Runtime recorded one new history row and one accepted receipt for seven retargeted clips, their parameter changes and six new titles. The operator's live Playwright page and navigation record report that four after-stills were captured without a reload. The original accepted response was redirected to scratch and was not independently captured; the receipt evidence is the Runtime history row.

Paths under `/root/codex/le4/` are machine-local to the proof run.

## Sources and fixture

- Agent `07e7cc0373f03d139d44de26eaa2c5fe6c8d03df`; locked Runtime `3c28211f3cb7ac4867ad744d8cdeeb38dd4484c5`.
- App `e3dbad64d402724ac5a35fb6447f18e432c64b78`, with the motion-pack manifest patch applied to a disposable copy only; the App change was not landed for this proof.
- Motion pack source `https://github.com/banodoco/poms_packs`, commit `2379ab54aca522019ff4f869cfdf9375bdb56dfc`, `pack-tree-v1` digest `75234c10217e67ec0f111a4cb6be4a6252e172a9cd382506498d07ce1d241029`.
- The proof used a synthetic moderate timeline: 40 initial clips, three shots, approximately 149.8 seconds, no owner media. A separate heavy fixture had 136 clips, eight shots and approximately 479.8 seconds; it was used for timing exploration, not the final chat proof, because the moderate fixture provided a clear title window and a practical editor rehearsal. Fixture generator: `/root/codex/le4/fixture/` and `/root/codex/le4/run4/fixture/`.
- On earlier Agent `07e7cc03`, the fresh isolated install listed `am-type` and `am-footage` before a manual pack add, and completed in 104 s. Installer publication is now removed from the candidate; this observation does not prove that a fresh install of the current candidate includes the motion pack.

## Prompt sent to the editor's agent

> In the moderate project, make editable copies of the installed AM Type and AM Footage motion elements. Call the copies LE4 Gold and LE4 Cyan, respectively. Give LE4 Gold a gold look (#FFD34E), and give LE4 Cyan a cyan background (#42D9FF).
>
> Use the two copies for the seven existing motion clips in timeline order, alternating Gold, Cyan, Gold, Cyan, Gold, Cyan, Gold. For the Gold clips, set the words to REHEARSAL 1, 3, 5, and 7 respectively, the text size to 120, and the text color to gold (#FFD34E). For the Cyan clips, show the placeholder card with labels REHEARSAL 2, 4, and 6 respectively, and a cyan background (#42D9FF).
>
> In the first shot, add six text titles reading NEW TITLE 1 through NEW TITLE 6. Start them at 10, 12, 14, 16, 18, and 20 seconds within that shot, each lasting 1.5 seconds. Please make all these changes together as one edit, so they appear as one new history entry.

## Result and times

Prompt sent at 22:59:05 UTC; first tool activity was visible by 22:59:19. Admission was reported at 23:03, within 3 min 55 s; exact admission completion time was not captured. The history receipt `txn-1a909b6859274123bb4e3b592e9fb69b` was recorded at 23:03:26.365, 4 min 21.365 s after the prompt, with head `authoring-parent-revision-539ca914f3ece4008c2c76179f5266a1405deaf53d5fa9961882433da8022bfc`. The separately returned commit response and exact save-response time were not captured. The earliest observed post-edit DOM result was 23:04:48, 5 min 43 s after the prompt; the first verified after-still at 23:08:18, 9 min 13 s after the prompt, is an upper bound, not first-render latency.

The receipt contains 14 commands: seven `clip.set-element` and seven `doc.patch` operations, with six title insertions in the final patch. The seven existing clips alternate the two admitted project elements: Gold on 1, 3, 5 and 7, with size 120 and gold `#FFD34E`; Cyan on 2, 4 and 6, with placeholder enabled and cyan `#42D9FF`. The admitted refs belong to `project_9afbc3050353e594c65c`:

- `le4-gold`: `sha256:2c55b0e50dab18bccf204ddec60d0b8b25b4f6d3c1b3f75574293737c46ff35f`.
- `le4-cyan`: `sha256:50fd1778f74a29730cbe838921f1c463fa71e654d86e3022ef61a57522ed9465`.

The first-shot titles `NEW TITLE 1`–`NEW TITLE 6` start at 10, 12, 14, 16, 18 and 20 seconds, each 1.5 seconds. These are numeric timings, as allowed by the plan.

## Preview stills

The before images were cropped to the preview box (device pixels x=26, y=116, 1484×956); after images were captured directly from the preview surface at the same size. The live Playwright page and navigation record support the no-reload observation; the images show the visual comparisons, not page continuity. The first before-still was at 1.49 s, 0.01 s before its after-still. The other displayed playheads matched. The source report's descriptions and the captured after-stills give the following comparison:

| Playhead | Before | After and intent |
| --- | --- | --- |
| 1.50 s | [Before](evidence/live-proof/before-1.5.png): dim PANEL 1 on black. | [After](evidence/live-proof/after-1.5.png): gold REHEARSAL 1. |
| 3.50 s | [Before](evidence/live-proof/before-3.5.png): dim PANEL 2 on black. | [After](evidence/live-proof/after-3.5.png): REHEARSAL 2 on the cyan placeholder. |
| 11.00 s | [Before](evidence/live-proof/before-11.png): black frame. | [After](evidence/live-proof/after-11.png): white NEW TITLE 1. |
| 31.50 s | [Before](evidence/live-proof/before-31.5.png): dim PANEL 4 on black. | [After](evidence/live-proof/after-31.5.png): REHEARSAL 4 on the cyan placeholder. |

The after captures showed no preview error; the chat reported a preview error, but no corresponding preview timeout or page error was recorded. The one recorded console error was a transient 503 before the chat. The visual record does not independently establish the separately returned commit response.

## Negative cases and running-pack probe

An earlier synthetic rehearsal recorded stale head, wrong or unadmitted revision, failed compile, and failed commit after good admission. Each reported its failing step and retained the same head and all six history rows; the failed commit left a recoverable pending record. These cases were not repeated in the final chat session. Detailed source: `/root/codex/le4/run2/report.md` and its negative-case record.

On the fresh isolated install, a Runtime process first resolved an existing effect, then `astrid packs add` installed `le4_probe` and the next shot patch using `probe-cyan` committed without restarting that process. Pack add took 2 s; commit took 2.000 s and returned receipt `txn-8e216465a7a14875a48b8428ef0f6765`. This warm-up was an effect resolution in a successful commit, not a separately issued lookup. A later container restart created a new Runtime process; this no-restart result belongs to the earlier process. Detailed source: `/root/codex/le4/run4/report.md`.

## Limits

The ready [motion-pin patch](evidence/app-motion-pin.patch) lands in Plan 78’s slot as a PR into astrid-app `release/15/main`; keep `release` at 15 and `required` untouched, and quote in the PR the guard run against published main showing it accepts 15. This proof applies the patch to a disposable App copy only. Agent `astrid/installer/tools.py:validate_manifest` for `packs` and its tests land as source in Plan 78’s slot and tolerate a manifest without `packs`. The pin data lands, but fresh installation of the motion pack awaits the fix row under [#1525](https://github.com/banodoco/astrid-dev/issues/1525); D2 is not delivered by Plan 78.

- The Lead's 23 November gate defines a blocking finding as one that breaks the headline claim (a pack installed after startup used in a mixed commit), breaks or changes an existing base test, prints a falsehood, loses user data, or crosses a decided boundary. Other findings receive an issue each and a line under the plan's limits.
- A stateful lookup callback can return different results on the two evaluations of a warm miss: [#1599](https://github.com/banodoco/astrid-dev/issues/1599).
- A published registry can share the base process-global mutable kind registry with other callers: [#1588](https://github.com/banodoco/astrid-dev/issues/1588).
- A pack can land after its root stamp is sampled and before a miss returns; a later lookup can see it: [#1584](https://github.com/banodoco/astrid-dev/issues/1584).
- Animation and transition discovery after startup is outside this proof and plan scope: [#1564](https://github.com/banodoco/astrid-dev/issues/1564).
- The pack-add message can say refresh is pending after the host has acknowledged it; the Lead accepted this over-cautious direction: [#1566](https://github.com/banodoco/astrid-dev/issues/1566).
- The base group transaction can delete a concurrently written file inside a newly installed or updated pack during swap-back: [#1578](https://github.com/banodoco/astrid-dev/issues/1578).
- A transaction sync failure after swap-back can omit the retained generation's path from its error; on a truly fresh install that generation contains no user's prior workspace: [#1567](https://github.com/banodoco/astrid-dev/issues/1567).
- The prompt asked for the changes “together as one edit, so they appear as one new history entry”. The proof shows the editor’s agent can deliver them as one commit when asked; it does not show that the skills alone lead an agent to choose one commit unprompted.

- This is one synthetic fixture on one machine, not evidence about hosted or shared use. The final chat ran on the 40-clip fixture, not the 136-clip fixture.
- The editor's admitted-element list and imports share a 30 s deadline. Under load, the list waited on the Runtime store mutex while history was being read and validated; the observed wait does not establish a scaling law. Follow-up: [#1433](https://github.com/banodoco/astrid-dev/issues/1433).
- A container restart interrupted the wider run. The live page and navigation record report that the final chat and after-stills used one open page without reload; the earlier no-restart probe used the previous Runtime process.
- The owner's existing Codex login folder was used via `CODEX_HOME` on her explicit 22 November instruction. That login was exposed to the chat agent for this run; no login contents are included in this record.
- One initial chat session was stopped before any edit; the second made the edit. The agent's dry run failed after admission, and it subsequently submitted the guarded commit. Admission, commit-response and first-visible-result durations were not individually captured.
