# Inputs — Saving holds on a heavy timeline

[Plan](plan.md) · [Tasks](tasks.md) · [Handover](handover.md) · [Rounds](rounds.md)

## Planning evidence

**Scope decision:** Pending — the design challenge below has not been obtained, so the end state is not yet signed off as such. Next: the first loop round's strategist advice, then the owner's sign-off. On 21 November 2026 the owner restated the end state in their own words ("run the timeline live in the app, and then just check what the speed is, and then optimize it, and then keep on doing that on loop until it was working fast enough") and asked for this pack to be merged to `main`. Background: the owner asked on 18 November 2026, in the Release 14 Lead's session, for this loop: a heavy generated timeline, live tests of every edit, a strategist consulted each round, optimization, and updates to the saving plans from what the loop finds. Codex does the work; the coordinator makes the judgment calls. The owner did not choose the plan's number, title or card list; those are the planner's draft. Source: the owner's message in that session, quoted in the task brief that created this pack (not otherwise recorded).

**Prior art:** The 14-kind sweep and its profiler, 18 November: [results.jsonl](evidence/results.jsonl) (3 saved, 11 refused), [log](evidence/sweep-loaded.log), [commit profile](evidence/sonnet-commit-profile-r14.md) (about 59% of a 3.74 s warm commit is `validate_final_candidate`, a doubled pass inside; 0.22 s on one clip). Design reviews that costed Plans 63, 75 and 76 and 18 from reading, not from a live loop: [final recommendations](evidence/fable-final-recommendations.md), [commit proof fit](evidence/fable-commit-proof-fit.md), [end-state review](evidence/fable-end-state-review.md). The state of everything on the crash day: [handover facts](evidence/handover-facts-20261118.md) and [QUEUE](evidence/QUEUE.md). The seeded harness is on astrid-app `release/15/plan-77` under `scripts/save-loop/`; the profiler helpers `prof_run.py` and `wall_run.py` could not be found on disk, so the profiling in SL-0 and SL-3c is redone from the report.

**Approach:** Measure first and fix by cause, rather than build the longer designs on estimates. A loop plan (a known end state, tasks from each live round) is the smallest form: three template files, a few setup cards and one standing card, run by the [live-loop workstream](../../skills/roles/astrid-dev-manage/workstreams/live-loop.md). Alternatives rejected: another one-shot sweep (it missed repeated gestures); starting Plans 63 and 75 first (the same costing gap); a fixed card list (the fixes are not known). The stop-gap speed target is about 2 s; 300 ms stays Plan 75's.

**Challenge:** Not yet obtained. The first loop round's strategist advice is the first independent check; the plan's own design is covered by the final review. Known risk: the release script copies the live realm and so may not run on a new machine (see SL-1). A sense check on 21 November 2026 (a critic session with three read-only helpers on the code) changed the order, the stack route, the timing method and the first matrix; it is not the design challenge.

**Proof and limits:** Completion in [plan.md](plan.md#completion). Limits: a synthetic fixture stands in for the owner's timeline, so a final run on the real timeline stays the owner's; the heavy shape below is from one timeline copied on 18 November.

**Review rounds:** The owner's standing preference: reviews at the very end, up to five advisor rounds (review, fix, review), no per-step gates. The strategist's per-round advice inside the loop is evidence, not a review round.

**Run start:** 21 November 2026 — Codex manager (hosted in Claude session session_011EzfW1FXS3o7GFnNSB7cZS), route S. The owner asked for a Codex manager on 21 November 2026. The host checks in hourly. The lane brief authorizes focused-proof PRs into `release/15/plan-77`, the sandbox setup and loop, and the stated merges that keep the plan current. The owner granted standing release landing approval on 21 November 2026, given to the hosting session, subject to D5. Other owner decisions go through the host. On 22 November 2026 the owner said, “You may merge your plan into release/15/main yourself, pins included, once the Release 15 Lead confirms its landing gate is met. Record this on your Run start line with today's date. Publishing a release still needs my own go.” At 22:39 UTC on 22 November 2026, the owner answered “I ACCEPT” to the final qualified first-cut opening integrity statement, including the measured 38.321 s save limitation. The written Release 15 landing confirmation and separate publishing approval still apply.
- **Accountable:** the coordinator session that claims the plan on the new machine; it records its session id in the `Owner` line of [plan.md](plan.md) when it starts.
- **May, without asking:** open and merge PRs into `release/15/plan-77` in all three repositories after focused proof; add a stack script under `scripts/save-loop/` on App `release/15/plan-77` (the release script itself is not edited); dispatch workers; take saving changes from the Plan 69 branches or `release/15/main` into the plan branches and retain the coherent Plan 77 Agent source set during the loop.
- **Needs the owner:** anything into `release/15/main`, `release/14/main` or product `main`; publishing anything; touching any live install or the owner's timelines; paid spend. Plan 77 follows the [Release skill](../../skills/capabilities/astrid-dev-release/SKILL.md). Its own landing may proceed once the Release 15 Lead confirms the landing gate, per the owner's 22 November 2026 statement above. Publishing still needs the owner's separate go.

### Heavy timeline shape

Measured read-only on 18 November 2026 from a copied Release 14 realm (see the discrepancy below); no names, text or paths of the owner's media kept. The document is the latest parent composition revision of the timeline.

| Dimension | Value |
| --- | --- |
| Tracks | 9 (6 visual, 3 audio) |
| Clips / placed occurrences | 8 (7 media, 1 hold) / 7, all on one visual track; 7 to 10 fields per clip, 12 per occurrence |
| Effects, transitions, keyframes | none; clip params only fade in and out |
| Occurrence length | 5 s min, 19.5 s median, 73 s max; timeline about 197 s |
| Canvas | 1920 by 1080 at 30 fps |
| Registry assets in the document | 441 entries (418 distinct media ids): about 106 png, 27 mp4 or mov, about 305 wav, 3 mp3 |
| Asset sizes (median) | png 0.96 MB; mp4 3.3 MB; mov 11.6 MB; wav 0.5 MB (largest files up to 470 MB; the fixture stays small) |
| Document size | 140 KB, of which the registry is 114 KB (81%) |
| Revisions / commit publications | 13 document revisions; 18 publications; 1 head; timeline version 18 |
| Side tables | 46 project shots; 237 media transcript documents (not in the timeline document) |

**Renumbering (21 November 2026):** this plan was drafted as Plan 66 and its product branches as `release/14/plan-66`; main had since used 66 for H3 composable core, so it became Plan 69, and then Plan 77 the same day, because `release/14/plan-69` already held unrecorded project-element work in astrid-app, astrid-agent and astrid-runtime (18 November). Its branches are `release/15/plan-77`. PR #880's 64 (fast saving) and 65 (editing together) became 75 and 76. The files under [evidence/](evidence/) are dated copies and keep the old numbers: there, Plan 64 means Plan 75 and Plan 65 means Plan 76.

**Discrepancy (not the spec):** the 18 November profile reports 616 clips and a document of about 2.6 MB for "Almost Ready (trial v2)"; the copied realm's "Almost Ready" has 8 clips and 140 KB. The copy probably read a different timeline. The fixture's primary target is the profiled shape, measured live through the stack's API; the table above sets only the asset mix ratios and the track layout.

## Owner decisions

- **D0 Order.** Decided, 21 November 2026: Plan 69 first, then this plan, run back to back by one manager ([decision](https://github.com/banodoco/astrid-dev/issues/1224#issuecomment-7067275617)).
- **D1 Release.** Decided, 18 November 2026: the owner asked in the Release 14 Lead's session for this work on a proper Release 14 branch, as a plan another machine runs. Moved, 21 November 2026: the owner moved the plan to Release 15 ("I think this should move to release. This should basically be release 15"), because Release 14 makes no speed claim and the saving plans it feeds (63, 75, 76, 18) are Release 15's. Release 15; listed in [releases/15.md](../../releases/15.md).
- **D9, D10, D14, D15** are open and carried from the [QUEUE](evidence/QUEUE.md); none is decided here:
  - **D9** which release carries Plans 63, 75 and 76 and 18: Release 15 recommended ([final recommendations, 5.4](evidence/fable-final-recommendations.md)).
  - **D10** corpus data: synthetic recommended; the shadow-applier experiment reads a local copy of real history and commits none of it (same file).
  - **D14** persist `file_identity` ([QUEUE](evidence/QUEUE.md), item 13). Its full wording is not recorded, and the QUEUE elsewhere calls it "cold start": confirm what it means before asking.
  - **D15** what a refused change looks like, the one most affecting this plan: "park it with everything behind it, with Try again and Discard" in the [final recommendations](evidence/fable-final-recommendations.md); "remove and list, or leave visible and marked" in the [QUEUE](evidence/QUEUE.md). The recommendations differ; the loop's refusals are shown as Try again / Discard until the owner decides.
- **D2 Review rounds.** Decided as the owner's standing preference (see Review rounds above): up to five advisor rounds at the very end.
- **D3 Round order and cap.** Decided on 22 November 2026, given to the hosting session. Run at most five live rounds. Rounds 1–3 focus on saving. Round 1 records the partial baseline and its first history-cost fix. Rounds 2 and 3 each use a fresh, full 616-clip fixture and both must pass the save criteria. Round 4 focuses on opening. Round 5 focuses on the largest measured CPU cost with no worsening of open or save time. Every round measures all three. Stop early when the work requires redesign, three rounds produce no fixes, or free disk falls below 15 GB.
- **D11 Batch fixes in a round.** Decided on 22 November 2026, given to the hosting session. Ask the strategist to rank the candidate fixes with expected opening, saving and CPU gains and risks. The manager can run several independent bounded fixes in parallel and merge them before one combined next-round measurement. Keep a separate PR, focused proof and before/after profile contribution for each fix. Larger changes to the document or history model or to shared contracts beyond an additive mirror go to Plan 75 or a new plan.
- **D14 One checkpoint follow-up.** Decided on 22 November 2026 through the host. The five scheduled slots remain the record of the original loop. The owner approved one Round 6 to implement and measure a persisted verification checkpoint out of that loop. Recompute exact stored history and dependency inputs before using clean, owner-bound prior verification. Unknown, stale or mismatched proof takes the existing full replay. An independent reviewer checks correctness before measurement. The owner reviews the measured result before any product landing. The commit-record format change stays outside this card.
- **D15 Quick indicator.** Decided on 22 November 2026 through the host. Deliver an independently reviewed, exact-CI-qualified tooling-only App candidate from Release 15 main. Measure unmodified product across empty, 10, 100 and restored v30. Use one-clip commits for ordinary seed history and measure the first edit after opening and the edit after a subsecond read with guarded cleanup. Report opening, save, unavailable intervals and request timing with simple thresholds. Reuse it for the checkpoint comparison.
- **D4 On-demand harness.** Decided on 21 November 2026, given to the hosting session. Land SL-0, SL-1 and SL-2 as a reusable optional test in `scripts/save-loop/`. One command builds an isolated stack, creates the synthetic fixture, runs the matrix, and prints the round table. A short README covers Node 20, ffmpeg, Playwright, 25 GB free, the Linux and macOS routes, outputs, and cleanup.

- **D5 Standing landing approval.** Decided on 21 November 2026, given to the hosting session. When the loop ends at the five-round cap or an early stop, land through the Runtime, Agent and App PRs only after exact independent review and a full comparison with the current Release 15 base find no new failing IDs. Each release PR names Plan 77, states each focus result against its target and links the round evidence and any remaining gap handed to Plan 75. This grants authority to ship reviewed improvements when the speed target remains open.
  - **Condition (d), recorded 21 November 2026 and given to the hosting session.** The Agent release candidate must carry only Plan 77 saving changes and derive its VibeComfy, lifecycle, Whisper and other non-saving pack pins and source bindings directly from the current `release/15/main`. Prove it with an empty diff over those files against that exact base. If a saving fix depends on the Plan 77 pack set, stop and bring the dependency to the host. Each measurement round uses the coherent Plan 77 pack and source set.
- **D6 Partial baseline at the projection stop.** Decided on 21 November 2026, given to the hosting session. If the current seed projects beyond about three hours for clips and shots, preserve the accepted prefix and measure the complete Round 1 editor matrix at the reached size on the checkpoint-repaired tuple. Record the exact clip count and all seed batch timings. Rounds 2 and 3 still use fresh stacks and the full qualified 616-clip fixture.

- **D7 Open and CPU.** Decided on 22 November 2026, given to the hosting session. Each round records first usable (the first 15 s visible and editable), full open (the whole timeline loaded and Saved), and gesture-to-Saved timing. The provisional full-fixture launch targets are about 5 s to first usable and 15 s to full open. Measure Runtime and browser process CPU seconds alongside wall time for opening and each scenario. Flag gains that spend more CPU. Loading the first 15 s first is a named candidate when a round finds a card-sized cause. Route a larger document-model change to Plan 75 or a new plan.
- **D8 Large-shots variant.** Decided on 22 November 2026, given to the hosting session. The optional harness supports `run.sh --variant large-shots` with a few substantial generated shots, many child clips, long durations and large generated assets. Document it in the README and report it alongside the standard fixture when time permits. The full standard fixture remains the completion reference.

- **D12 Save badge.** Decided on 22 November 2026, given to the hosting session. The owner delegates wording judgment to the reviewer. Show an opening state during project load. Untouched work must never show Not saved. Show device-saved and syncing only after the edit is durable locally, and Saved only after Runtime acceptance. A refusal keeps Try again and Discard. Use a bounded fix with proof of the opening, edit and refusal transitions. Schedule it in Round 2 if cheap or in Round 4 with opening.

- **D13 History contract staging.** The host decided on 22 November 2026 to take the existing-contract App lazy-read path in Round 2. Keep the optional compact Runtime read projection for Round 4 if Round 2 opening and undo measurements still justify it. If selected, use the official additive contract generation and exact Runtime, Agent and App pins.

## The owner's wider goals

- Humans and agents edit the same timelines.
- Fast saving, aiming at about 300 ms in the later plans.
- Extensibility for agents without touching the core.
- As elegant and minimal as possible.

## Source identities

Cut on 21 November 2026 from `release/14/int-59-64-65`, the Release 14 Lead's integration of Plans 59, 64 and 65, which contains all of `release/14/main` (with the release script) and all of Plan 59's App and Agent work:

| Repository | Branch | SHA at cut |
| --- | --- | --- |
| astrid-app | `release/15/plan-77` | `1f8da7f42`: the integration head `10a33dd64` plus the harness seed, cherry-picked from `36d2b8258` |
| astrid-agent | `release/15/plan-77` | `03e2db9a1`, the integration head; its `runtime.lock.json` pins Runtime `8a18168a3` |
| astrid-runtime | `release/15/plan-77` | `8a18168a3`, the integration head |

**Then built on Plan 69 (21 November 2026):** the owner asked for Plan 77 to sit on the project-element work ([Plan 69](../69-project-elements/plan.md)), which also carries speed fixes this plan needs (validation that judges only changed clips; Runtime object checks once per process). `release/15/plan-69` was merged into each `release/15/plan-77`, with pins regenerated (Agent pins Runtime, App pins both). Heads after that merge:

| Repository | `release/15/plan-77` head | Pins |
| --- | --- | --- |
| astrid-app | `2a34ab0f9` | Agent `c00721de3`, Runtime `e43bfccc8` |
| astrid-agent | `c00721de3` | Runtime `e43bfccc8` |
| astrid-runtime | `e43bfccc8` | — |

Every focused test that fails on these heads also fails on the cut or on `release/15/plan-69` (checked 21 November); the Runtime keeps Plan 59's verify-once CAS design over Plan 69's duplicate ([astrid-dev#1222](https://github.com/banodoco/astrid-dev/issues/1222)).

**Why not `release/15/main`:** on 21 November it was last forwarded on 18 November, carried none of Plan 59 and was 35 commits behind `release/14/main` in the App. It now carries `release/14/main` (forwarded 21 November, [astrid-dev#1224](https://github.com/banodoco/astrid-dev/issues/1224)) and reaches the plan branches through Plan 69; when Release 14's integration lands in `release/14/main` and is forwarded again, merge `release/15/main` into the plan branches.

**Runtime difference (checked 21 November):** the Runtime integration carries #62 ("keep verified history across unrelated writes") but not Plan 59's revert of it, #67, so the stack does not run what `release/14/plan-59` ran. That is the integration's choice at that SHA, still under review; record in round 1 which Runtime ran.

**Old branches:** the 18 November branches (`release/14/plan-66` in all three repositories, and `release/14/plan-77` in the Runtime, from an intermediate rename) are superseded. Delete them once nothing reads them. The uncommitted crash work stays on `release/14/plan-66-wip/*` (and, in the Runtime, the same commits under `release/15/plan-77-wip/*`); each branch and its base is in the [handover](handover.md#where-everything-is). Destination for every fix: the same repository's `release/15/plan-77`.

## References

- Longer-term plans for Release 15 are in astrid-dev PR #880 (branch `plan/63-dependable-saving`): 63 dependable saving, 75 fast saving, 76 editing together, 18 timeline editing. Main used 64 to 68 for other plans, so #880's 64 and 65 were renumbered to 75 and 76 on 21 November; see the [handover](handover.md#first-actions-on-a-new-machine). The plan deltas from [rounds.md](rounds.md) go into those plans.
- All evidence copies are in [evidence/](evidence/); absolute home paths were rewritten to `~`.
