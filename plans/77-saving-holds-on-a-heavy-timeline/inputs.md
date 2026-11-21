# Inputs — Saving holds on a heavy timeline

[Plan](plan.md) · [Tasks](tasks.md) · [Handover](handover.md) · [Rounds](rounds.md)

## Planning evidence

**Scope decision:** Pending — the design challenge below has not been obtained, so the end state is not yet signed off as such. Next: the first loop round's strategist advice, then the owner's sign-off. On 21 November 2026 the owner restated the end state in their own words ("run the timeline live in the app, and then just check what the speed is, and then optimize it, and then keep on doing that on loop until it was working fast enough") and asked for this pack to be merged to `main`. Background: the owner asked on 18 November 2026, in the Release 14 Lead's session, for this loop: a heavy generated timeline, live tests of every edit, a strategist consulted each round, optimization, and updates to the saving plans from what the loop finds. Codex does the work; the coordinator makes the judgment calls. The owner did not choose the plan's number, title or card list; those are the planner's draft. Source: the owner's message in that session, quoted in the task brief that created this pack (not otherwise recorded).

**Prior art:** The 14-kind sweep and its profiler, 18 November: [results.jsonl](evidence/results.jsonl) (3 saved, 11 refused), [log](evidence/sweep-loaded.log), [commit profile](evidence/sonnet-commit-profile-r14.md) (about 59% of a 3.74 s warm commit is `validate_final_candidate`, a doubled pass inside; 0.22 s on one clip). Design reviews that costed Plans 63, 75 and 76 and 18 from reading, not from a live loop: [final recommendations](evidence/fable-final-recommendations.md), [commit proof fit](evidence/fable-commit-proof-fit.md), [end-state review](evidence/fable-end-state-review.md). The state of everything on the crash day: [handover facts](evidence/handover-facts-20261118.md) and [QUEUE](evidence/QUEUE.md). The seeded harness is on astrid-app `release/14/plan-77` under `scripts/save-loop/`; the profiler helpers `prof_run.py` and `wall_run.py` could not be found on disk, so the profiling in SL-0 and SL-3c is redone from the report.

**Approach:** Measure first and fix by cause, rather than build the longer designs on estimates. A loop plan (a known end state, tasks from each live round) is the smallest form: three template files, a few setup cards and one standing card, run by the [live-loop workstream](../../skills/roles/astrid-dev-manage/workstreams/live-loop.md). Alternatives rejected: another one-shot sweep (it missed repeated gestures); starting Plans 63 and 75 first (the same costing gap); a fixed card list (the fixes are not known). The stop-gap speed target is about 2 s; 300 ms stays Plan 75's.

**Challenge:** Not yet obtained. The first loop round's strategist advice is the first independent check; the plan's own design is covered by the final review. Known risk: the release script copies the live realm and so may not run on a new machine (see SL-1).

**Proof and limits:** Completion in [plan.md](plan.md#completion). Limits: a synthetic fixture stands in for the owner's timeline, so a final run on the real timeline stays the owner's; the heavy shape below is from one timeline copied on 18 November.

**Review rounds:** The owner's standing preference: reviews at the very end, up to five advisor rounds (review, fix, review), no per-step gates. The strategist's per-round advice inside the loop is evidence, not a review round.

**Run start:** The owner's go is their own message in the main session on 18 November 2026: "write like basically a handover thing for this … make sure that everything is pushed to like a proper release-14 branch … it ultimately should just be like a plan within Astrid-dev that I'm able to give to another machine and they're able to do it … we're going to use Codex for most of the heavy lifting while it just acts as the coordinator, you know, fixing the stuff and making judgment calls on it."
- **Accountable:** the coordinator session that claims the plan on the new machine; it records its session id in the `Owner` line of [plan.md](plan.md) when it starts.
- **May, without asking:** open and merge PRs into `release/14/plan-77` in all three repositories after focused proof; add an empty-realm option to the release script on App `release/14/plan-77` (and say so in the PR, for Plan 61); dispatch workers; fix the docs of astrid-dev PR #880 (renumber, Approach lines).
- **Needs the owner:** anything into `release/14/main` or product `main`; publishing anything; touching any live install or the owner's timelines; paid spend. Plan 77 reaches `release/14/main` only through the [Release skill](../../skills/capabilities/astrid-dev-release/SKILL.md), on the owner's go.

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

**Renumbering (21 November 2026):** this plan was drafted as Plan 66 and its product branches as `release/14/plan-66`; main had since used 66 for H3 composable core, so it became Plan 69, and then Plan 77 the same day, because `release/14/plan-69` already held unrecorded project-element work in astrid-app, astrid-agent and astrid-runtime (18 November). Its branches are `release/14/plan-77`. PR #880's 64 (fast saving) and 65 (editing together) became 75 and 76. The files under [evidence/](evidence/) are dated copies and keep the old numbers: there, Plan 64 means Plan 75 and Plan 65 means Plan 76.

**Discrepancy (not the spec):** the 18 November profile reports 616 clips and a document of about 2.6 MB for "Almost Ready (trial v2)"; the copied realm's "Almost Ready" has 8 clips and 140 KB. The copy probably read a different timeline. The fixture's primary target is the profiled shape, measured live through the stack's API; the table above sets only the asset mix ratios and the track layout.

## Owner decisions

- **D1 Release.** Decided, 18 November 2026: the owner asked in the Release 14 Lead's session for this work on a proper Release 14 branch, as a plan another machine runs. Release 14; listed in [releases/14.md](../../releases/14.md).
- **D9, D10, D14, D15** are open and carried from the [QUEUE](evidence/QUEUE.md); none is decided here:
  - **D9** which release carries Plans 63, 75 and 76 and 18: Release 15 recommended ([final recommendations, 5.4](evidence/fable-final-recommendations.md)).
  - **D10** corpus data: synthetic recommended; the shadow-applier experiment reads a local copy of real history and commits none of it (same file).
  - **D14** persist `file_identity` ([QUEUE](evidence/QUEUE.md), item 13). Its full wording is not recorded, and the QUEUE elsewhere calls it "cold start": confirm what it means before asking.
  - **D15** what a refused change looks like, the one most affecting this plan: "park it with everything behind it, with Try again and Discard" in the [final recommendations](evidence/fable-final-recommendations.md); "remove and list, or leave visible and marked" in the [QUEUE](evidence/QUEUE.md). The recommendations differ; the loop's refusals are shown as Try again / Discard until the owner decides.
- **D2 Review rounds.** Decided as the owner's standing preference (see Review rounds above): up to five advisor rounds at the very end.

## The owner's wider goals

- Humans and agents edit the same timelines.
- Fast saving, aiming at about 300 ms in the later plans.
- Extensibility for agents without touching the core.
- As elegant and minimal as possible.

## Source identities

On 18 November 2026, all on origin, cut from `release/14/plan-59`:

| Repository | Branch | SHA at cut |
| --- | --- | --- |
| astrid-app | `release/14/plan-77` | `2ffc0a300` at the cut; head `36d2b8258` after the harness seed |
| astrid-agent | `release/14/plan-77` | `ec758a9b8` |
| astrid-runtime | `release/14/plan-77` | `ee235d39d` |

Merged into `release/14/plan-59` before the cut: Runtime #66 (member-list removal), Runtime #67 (revert of the #62 retention), App #308 (gesture registry read). Destination for every fix: the same repository's `release/14/plan-77`. The uncommitted crash work is on `release/14/plan-77-wip/*`; each branch and its base is listed in the [handover](handover.md#where-everything-is).

## References

- Longer-term plans for Release 15 are in astrid-dev PR #880 (branch `plan/63-dependable-saving`): 63 dependable saving, 75 fast saving, 76 editing together, 18 timeline editing. Main used 64 to 68 for other plans, so #880's 64 and 65 were renumbered to 75 and 76 on 21 November; see the [handover](handover.md#first-actions-on-a-new-machine). The plan deltas from [rounds.md](rounds.md) go into those plans.
- All evidence copies are in [evidence/](evidence/); absolute home paths were rewritten to `~`.
