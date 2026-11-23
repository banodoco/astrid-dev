# LE-4 live proof — 22 November 2026

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

The ready [motion-pin patch](evidence/app-motion-pin.patch) is handed to the Release Lead for the single freeze pin; it does not merge into `release/15/main` from Plan 78 because it changes the App install tuple. This proof applies it to a disposable App copy only. Agent `astrid/installer/tools.py:validate_manifest` for `packs` and its tests land as source in Plan 78’s slot and tolerate a manifest without `packs`.

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
