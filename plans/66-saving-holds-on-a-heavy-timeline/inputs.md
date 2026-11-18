# Inputs — Saving holds on a heavy timeline

[Plan](plan.md) · [Tasks](tasks.md) · [Handover](handover.md) · [Rounds](rounds.md)

## Planning evidence

**Scope decision:** The owner asked on 18 November 2026, in the Release 14 Lead's session, for this loop: a heavy generated timeline, live tests of every edit, a strategist consulted each round, optimization, and updates to the saving plans from what the loop finds. Codex does the work; the coordinating Claude session makes the judgment calls. The owner did not choose the plan's number, title or card list; those are the planner's draft and need the owner's confirmation. Source: the owner's message in that session, quoted in the task brief that created this pack (not otherwise recorded).

**Prior art:** The 14-kind sweep and its profiler, 18 November: [results.jsonl](evidence/results.jsonl) (3 saved, 11 refused), [log](evidence/sweep-loaded.log), [commit profile](evidence/sonnet-commit-profile-r14.md) (about 57% of a 3.74 s save is `validate_final_candidate`, a doubled pass inside; 0.22 s on one clip). Design reviews that costed Plans 63 to 65 and 18 from reading, not from a live loop: [final recommendations](evidence/fable-final-recommendations.md), [commit proof fit](evidence/fable-commit-proof-fit.md), [end-state review](evidence/fable-end-state-review.md). The state of everything on the crash day: [handover facts](evidence/handover-facts-20261118.md) and [QUEUE](evidence/QUEUE.md). The seeded harness is on astrid-app `release/14/plan-66` under `scripts/save-loop/`; the profiler helpers `prof_run.py` and `wall_run.py` could not be found on disk, so the profiling in SL-0 and SL-3c is redone from the report.

**Approach:** Measure first and fix by cause, rather than build the longer designs on estimates. A loop plan (a known end state, tasks from each live round) is the smallest form: three template files, a few setup cards and one standing card, run by the [live-loop workstream](../../skills/roles/astrid-dev-manage/workstreams/live-loop.md). Alternatives rejected: another one-shot sweep (it missed repeated gestures); starting Plans 63 and 64 first (the same costing gap); a fixed card list (the fixes are not known). The stop-gap speed target is about 2 s; 300 ms stays Plan 64's.

**Challenge:** Not yet obtained. The first loop round's Astra strategy is the first independent check; the plan's own design is covered by the one final Astra review. Known risk: the release script copies the live realm and so may not run on a new machine (see SL-1).

**Proof and limits:** Completion in [plan.md](plan.md#completion). Limits: a synthetic fixture stands in for the owner's timeline, so a final run on the real timeline stays the owner's; the heavy shape below is from one timeline copied on 18 November.

**Review rounds:** One Astra round at the end, after the loop stops (recommended by the planner; the owner has not yet confirmed). Astra's per-round strategy advice inside the loop is evidence, not a review round.

**Run start:** Pending — No run is authorized. Next: the owner starts the run and records the date, the cards it covers (SL-0 to SL-3 first), the accountable coordinator session, and what it may do without asking.

### Heavy timeline shape

Measured read-only on 18 November 2026 from the copied Release 14 realm; no names, text or paths of the owner's media kept. The document is the latest parent composition revision of the timeline.

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

**Mismatch to settle in SL-0:** the 18 November profile reports "616 clips, 2.6 MB" for Almost Ready, but this copy has 8 clips and 140 KB. The copy may be an earlier state or the profile a differently expanded view. The fixture is calibrated to the measured save time (about 3.7 s), not to either figure alone.

## Owner decisions

- **D1 Release and number.** Plan 66 is cut as `release/14/plan-66`. Recommended: keep it in Release 14, since its fixes land on the Release 14 branches. Pending.
- **D2 Review rounds.** One Astra round at the end. Pending the owner's confirmation.

## Source identities

On 18 November 2026, all on origin, cut from `release/14/plan-59`:

| Repository | Branch | SHA at cut |
| --- | --- | --- |
| astrid-app | `release/14/plan-66` | `2ffc0a300` at the cut; head `36d2b8258` after the harness seed |
| astrid-agent | `release/14/plan-66` | `ec758a9b8` |
| astrid-runtime | `release/14/plan-66` | `ee235d39d` |

Merged into `release/14/plan-59` before the cut: Runtime #66 (member-list removal), Runtime #67 (revert of the #62 retention), App #308 (gesture registry read). Destination for every fix: the same repository's `release/14/plan-66`. The uncommitted crash work is on `release/14/plan-66-wip/*`; each branch and its base is listed in the [handover](handover.md#where-everything-is).

## References

- Longer-term plans for Release 15 are in astrid-dev PR #880 (branch `plan/63-dependable-saving`): 63 dependable saving, 64 fast saving, 65 editing together, 18 timeline editing. Main has since used 64 and 65 for other plans, so #880's must be renumbered (67, 68); see the [handover](handover.md#first-actions-on-a-new-machine). The plan deltas from [rounds.md](rounds.md) go into those plans.
- All evidence copies are in [evidence/](evidence/); absolute home paths were rewritten to `~`.
