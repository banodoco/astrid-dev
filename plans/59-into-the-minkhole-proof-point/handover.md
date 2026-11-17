# Handover — Into the Minkhole proof point

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Release 14](../../releases/14.md)

Written by the Release 14 release manager on 16 November 2026, about 21:00 UTC, from the branches and records as they stood then. It is a dated snapshot for whoever manages this plan next. The plan's live record is on the astrid-dev branch `release/14/plan-59`, last changed at 18:48 UTC; the copy on `main` is older. The work was still moving when this was written.

## Where it stands

The first creative task is done: the rough cut imports, a clean frame comes out of one command, and a one-second render plays. The second, filling the frame, has a reviewed candidate across three repositories with five findings still being fixed. Transcription and the voice pilot have code on task branches that the record does not describe. Two of the ten outcomes in the [plan](plan.md#outcome-and-scope) have proof behind them, and all of that proof is local: no Plan 59 branch has had a hosted CI run.

Merged product work is on astrid-agent `release/14/plan-59`, 39 commits ahead of `release/14/main` (56 files, 25 of them tests), with no pull request open. More sits on task branches, below.

## The ten outcomes

| Outcome | State | Basis |
| --- | --- | --- |
| 1 Matrix shots fill the frame | Not proven | A candidate exists in the composition package; no Matrix frame has been shown to the owner. |
| 2 Same frame in editor, export and CLI | Not proven | The same candidate. |
| 3 Fit, fill and crop per clip | Not proven | Candidate on `p59/c2-app`, `p59/c2-agent` and `p59/c2-runtime`, unmerged. |
| 4 One command gives a clean frame | Proven, locally | A 1280 by 720 frame at 6.5 s; seven tests in `test_visualize_export.py`. |
| 5 The archive imports with one command | Partly | Both archives import on a Runtime run from source. Not shown on a built release. |
| 6 Morpheus says the new lines | Not proven | Pilot code on `p59/h3-pilot-integrated`. No GPU run; $0 of the $25 spent. |
| 7 Words with timestamps | Not proven | Code on `p59/c3-transcripts`. No proof recorded. |
| 8 A mouth mask without painting | Not started | No task names it. |
| 9 Takes arrive beside their shot | Not started | No task names it. |
| 10 A cheaper agent repeats the edit | Not started | |

## Blockers fixed, and how each is proven

| Blocker | Fix | Proof |
| --- | --- | --- |
| The archive was refused | Agent `a17104dc9` to `4baabb4b3` | 26 tests, and both real archives imported. Probably also fixes [#635](https://github.com/banodoco/astrid-dev/issues/635); no commit says so. |
| Composed capture rejected its own context | Agent `d88a22ae9` | Five tests, and a real frame. |
| Inputs-mode visualize reported success and wrote nothing | Agent `a340ec7ed` | Tests, and a real run. |
| No clean single frame | Agent `eb0fc0c0c` | Seven tests, and a real frame. |
| Render refused a stored `height` | Agent `7e407e84e`, `d01155ecb` | 36 tests, and a one-second render checked with `ffprobe`. |
| `astrid hivemind search` failed from source | Ten commits, merged at `15e14282c` | Tests. The record still says "review pending". |
| Preview and export disagree | Candidate in `banodoco/timeline-composition`, `2c0740a`, as 0.0.18 | The package's own 91 tests. Five review findings open. Not consumed by the App or the Agent. |
| Asset records are admitted open and refused at render | None | Waits on a decision (below). |

Nineteen commits landed after the record was last changed. Thirteen are a ranged render review, tied to [#771](https://github.com/banodoco/astrid-dev/issues/771), which no plan file mentions. Six are Hivemind follow-ups.

## Work on task branches, not merged and not recorded

None has a pull request, and none is in the plan branch.

| Branch | Size | For |
| --- | --- | --- |
| astrid-agent `p59/c2-agent` | 28 commits, 66 files | C2, appearance |
| astrid-app `p59/c2-app` | 12 commits, 96 files | C2; pins the composition package at 0.0.19 |
| astrid-runtime `p59/c2-runtime` | 1 commit, 21 files | C2, appearance edit fields |
| astrid-agent `p59/c3-transcripts` | 19 commits, 27 files | C3, transcription |
| astrid-agent `p59/h3-pilot-integrated` | 20 commits, 63 files | C4, the voice pilot |
| astrid-agent `p59/h3-claim-owner` | 4 commits, 32 files | Renting a machine for the pilot |

## Loose ends

- The App's release branch pins the composition package at 0.0.17, the record says the candidate is 0.0.18, and `p59/c2-app` pins 0.0.19. The record is behind the code.
- The record names task branches `p59/h3-conform`, `p59/see-the-timeline` and `p59/archive-import` that are no longer on the remote.
- Issues this plan was given on 16 November and has not touched: [#748](https://github.com/banodoco/astrid-dev/issues/748), [#745](https://github.com/banodoco/astrid-dev/issues/745), [#668](https://github.com/banodoco/astrid-dev/issues/668), [#746](https://github.com/banodoco/astrid-dev/issues/746). Issues it filed: [#757](https://github.com/banodoco/astrid-dev/issues/757) to [#761](https://github.com/banodoco/astrid-dev/issues/761), and #771.

## Waiting on the owner

1. **The composition package.** Whether its `release/14/plan-59` branch becomes that repository's `main`, its missing licence field, and which stray branches and copies to delete. Only the owner deletes those.
2. **One asset contract.** Whether asset records are checked once at admission. Today they are admitted open and refused late at render.
3. **The Matrix frames.** The owner looks at before and after once the five findings are fixed.
4. **Plan 60.** This plan's voice work, C4 and C5, now points at [Plan 60](https://github.com/banodoco/astrid-dev/tree/release/14/plan-60/plans/60-refining-h3-av) for its H3 integration. Plan 60 is queued, estimated at 13 days, has no run authorized and is not in the Release 14 brief. Until that is settled, C4 to C8 have no route to done.

The GPU rental is also held, for an independent review of the machine's lifetime bound. The record does not name the reviewer.

## For the next manager, in order

1. Read the [Manage skill](../../skills/roles/astrid-dev-manage/SKILL.md). The plan's loop is unchanged: take the next creative task, attempt it with Astrid's own tools, fix each blocker at its cause or file it, and record what a weaker agent needs.
2. Bring the record up to date, then bring it to `main`: the blocker log lacks the ranged render work, still calls the Hivemind fix unreviewed, and says nothing of the six task branches above.
3. Open a pull request from the Agent plan branch so hosted CI runs on it. Every proof so far is local, and 39 commits have never been through CI. Seven tests already fail on the base ([#757](https://github.com/banodoco/astrid-dev/issues/757)); know which before reading the result.
4. Finish C2: fix the five findings, land the three C2 branches together, since the App, Agent and Runtime halves depend on each other, and show the owner the Matrix frames. Cut `release/14/plan-59` in the App and the Runtime for them to land on.
5. Prove and land C3 from `p59/c3-transcripts`. It needs no GPU and no owner decision.
6. Bring the four decisions above to the owner together. C4 cannot start without the fourth.

## What this run taught

- **Success was reported for nothing done.** Visualize said it succeeded and wrote no file. Check a command by what it leaves behind.
- **Data was accepted early and refused late.** A record the importer stored was rejected by the renderer. One contract, checked on the way in.
- **The cause was hidden behind a generic error.** A TLS failure in a browser download surfaced as "renderer lease channel closed" ([#760](https://github.com/banodoco/astrid-dev/issues/760)).
- **Starting from source was undiscoverable.** The Node pin, the source manifest, the status command and the port were all learned by failing ([#758](https://github.com/banodoco/astrid-dev/issues/758)).
- **The work outran its record.** Two hours of merged commits have no row, and six task branches, more code than the plan branch holds, are not mentioned. A work loop needs its log written as it goes, or the skill at the end is written from memory.
