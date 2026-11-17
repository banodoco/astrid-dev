# Handover — Run a release branch locally

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Release 14](../../releases/14.md) · [Plan 62, the follow-up](../62-one-manifest-one-stack/plan.md)

Written on 17 November 2026, late evening, by the session that moved Plans 61 and 62 onto `main` and the tool onto its own plan branch. It is a dated snapshot for whoever manages this plan next. The branches and records below are as they stood then; re-read them with `git ls-remote` before acting. The plan's live record is `plan.md`, `tasks.md` and `inputs.md` on the astrid-dev branch `release/14/plan-61` (and on `main`, until the two diverge).

## Where it stands

The tool exists and has run once, for real. `scripts/astrid-release/astrid-release release/14/plan-59` built an isolated stack on a copy of the owner's realm, and a browser check passed. What is left is one proper proof run, one review, and landing the plan branches in the release branch.

- **The tool** is on astrid-app `release/14/plan-61`, head `cf383fc0e2668fe25c4a24f77c1a0b438a3a9fca`. It is cut from `release/14/main` (`0b6ef161`) and holds two cherry-picks of the tool commits. It is **not** in `release/14/main`: RB-7 merges it there after the proofs and the review.
- **Plan 59's branch** no longer carries the tool: one commit, `4eb6fb350`, returned the tool's paths to their `release/14/main` state. The preview banner fix (`158186d8`) is Plan 59's and stays there.
- **The docs** are on astrid-dev `release/14/plan-61`: a section "Try a release or plan branch live" in the release skill (at the old skill path on that branch) and a ledger entry, from [#834](https://github.com/banodoco/astrid-dev/pull/834).
- **Plan 62**, the long-term path (one stack, `use` and `back`), is queued after this plan, in no release brief. Nothing in it has started.
- Closed on 17 November: astrid-app #283 (the tool against `main`) and astrid-dev #832. Both are replaced by the branches above.

Of the ten tasks (RB-1 to RB-9 and R), RB-1 and RB-5 are done. The other eight are open: RB-2, RB-3, RB-4, RB-8 (edits and their proofs), RB-9 (the first-start trace), RB-6 (the real run), R (the review) and RB-7 (landing). The code for RB-2, RB-3 and RB-8 is committed; their proofs have not been run on the real stack.

## What is proven, and how

| Claim | Proof | Where it is recorded |
| --- | --- | --- |
| The `release/14/plan-59` stack runs isolated on a copy of the owner's realm | A real run: Agent `cce5d69a`, Runtime `519b4047`, ports 2400, 17500 and 17501. The editor at `http://127.0.0.1:2400/tools/video-editor?entry=editor` showed the "Almost Ready" timeline, 5 timelines, clips and a preview frame | The [run record](tasks.md#run-record), first paragraph. It used the earlier hand edit of the catalog, not `workspace attach` |
| The live install was untouched by that run | The live install (Agent `9814193a`, Runtime `6855dfa8`, door 17340) was still running afterwards. This was **not** the hash-and-database comparison that Completion asks for | `plan.md`, Status. Treat it as seen, not proven |
| The preview banners no longer take half the preview | Fixed in `158186d8` and seen in the browser check | Plan 59's branch |
| The tool's own scripts parse and its realm fixture passes | On 17 November, from a scratch clone of `release/14/plan-61`, Node 20.19.4: `bash -n` on both scripts passes; `test-realm-snapshot.sh` reports `passed=35 failed=0`; `manifest.test.mjs` runs 6 tests and all 6 pass | The [run record](tasks.md#run-record), second paragraph |
| The diff of the plan branch is only the tool | `git diff --stat origin/release/14/main..origin/release/14/plan-61` lists seven files: `.gitignore`, four under `scripts/astrid-release/`, `manifest.test.mjs`, `pin.mjs` | The same paragraph |
| The tool uses its own `pin.mjs`, so Plan 59's branch no longer needing it is safe | Read in the code: `node "$SCRIPT_DIR/../installer/pin.mjs" ... --in ... --out ...`, and the target branch is read only with `git show` | `plan.md`, Status |

## What is not proven

- `workspace attach` on the real stack (RB-3). The stack that is running used the hand edit.
- The `data/` clone that the tool makes before a destructive step, and the refusal text of `update` after the Agent or Runtime moved (RB-8).
- An edit surviving a restart (the `timeline_commit_history` count read before and after).
- `update` with nothing moved printing `unchanged` and running no installer (RB-2).
- The first-start failure, "accepted commit inputs changed during verification". It happens once on the first start of a fresh copy, and a guarded retry (at most 2) starts it. The cause is unknown after a tracer run and a review (RB-9).
- The live install untouched, by hashes and database facts, over a whole run.
- A fresh-clone run from `release/14/plan-61`, after cloning the old `data/` aside and deleting the root.
- A hosted CI run on either plan branch. Every proof above is local.
- `astrid-runtime restart`, `up` and `down` and the installer's `--update` on a stack beside a live install: read from the code to fail ([#825](https://github.com/banodoco/astrid-dev/issues/825)), never run to confirm. The tool avoids them.

## The running stack

A stack is running now, and it is the owner's working copy to look at.

- Root: `~/astrid-release/release-14-plan-59`. Ports: editor 2400, proxy 17500, door 17501.
- Editor: `http://127.0.0.1:2400/tools/video-editor?entry=editor`. The `?entry=editor` skips the welcome dialog; the editor talks only to the stack's own proxy, never to the live door 17340.
- Built by the earlier tool commit `1412e9ffc` from the `release/14/plan-59` branch, with the realm hand-edited into the catalog.
- **Do not stop, restart, install over or delete it** without the owner's go and a notice first, and keep each stop under 2 minutes. On 17 November two restarts happened without notice while a tool change was tested on the stack in use. The rule that came out of it: test tool changes on fixtures and scratch roots, and use the real stack last.
- Do not touch the live install either: door 17340, ports 2222, 17336 and 17391, `~/.astrid` and the `haus.astrid.runtime` login service.
- `astrid-release stop release/14/plan-59` ends only processes under the stack's root. It is the way back to normal, and it is also a stop that needs the owner's go.
- The checkout the tool was run from is a separate clone; do not modify it. Use a fresh clone of `release/14/plan-61` for the proof run (below).

**Disk.** On 17 November the machine had about 3 GiB free at the time of the run, and a later measurement showed about 8 GiB with scratch clones in place. The stack itself takes about 10 GB (program 3.6 GB, isolated home 3.6 GB, editor clone 0.7 GB, plus twice the realm database). The fresh-clone proof needs about 5 GiB free on top. Check free space first, run one heavy job at a time, and clean scratch clones before the fresh-clone proof.

## Waiting on the owner

1. **The stop window.** One approved window, announced first, for RB-6 and RB-9. The first start of a fresh copy and the restart proof both need the stack stopped, each stop under 2 minutes. Until she gives it, do nothing that stops the running stack, and do the work that needs no stop: RB-2, RB-4, RB-8 and the fixture checks on scratch roots.
2. **D3, review rounds.** Pending, recommended (a), one round R before RB-7. Ask once RB-6 has run and before R starts.
3. **D4, a real RunPod proof.** Pending, recommended (a), none in this plan. Ask after RB-6 has passed. No money is spent unless she says (b).
4. **The three drafted issues** in [tasks](tasks.md#issues-to-file) are not filed. They are hers to file or decline: the Runtime startup failure that stops everything with no stack trace, the installer's retained-profile guard, and the App's hardcoded port 5180. Issues made from RB-9's trace may add to the first.
5. **Run start.** She has said the plan is to be taken over and driven to completion, but `inputs.md` still has no record of what the manager may do without asking. Ask for it when you start, and record it.

D1 (Release 14) and D2 (the release route) are decided, with her words in [inputs.md](inputs.md#owner-decisions). Do not ask them again.

## For the next manager, in order

1. Read the [Manage skill](../../skills/roles/astrid-dev-manage/SKILL.md) and the [Release skill](../../skills/capabilities/astrid-dev-release/SKILL.md), then this plan's `plan.md`, `tasks.md` and `inputs.md`. Record yourself as the plan manager on `plan.md` (`Owner:` stays the owner's; say who manages in the Status) and tell the Release 14 Lead on the mailbox, [astrid-dev #796](https://github.com/banodoco/astrid-dev/issues/796), as the run board says.
2. Make a fresh clone of astrid-app at `release/14/plan-61` and run the fixture and the unit test with Node 20 (`bash -n` on both scripts; `scripts/astrid-release/test-realm-snapshot.sh`; `node --test scripts/installer/manifest.test.mjs`). They passed on 17 November. This gives you a baseline that costs no stop.
3. Do the work that needs no stop, on task branches `p61/<task id>` cut from `release/14/plan-61`, merged into it by pull request: RB-2's proof, RB-4's README check (each claim names the script line that does it), RB-8's refusal fixture. RB-3's fixture is already in.
4. Ask the owner for the stop window. Announce it, then do RB-6 in order on the fresh clone, following [Completion](plan.md#completion), with the live-install hashes before and after. Paste each command and output into the run record. Run RB-9's trace in the same window, on the first start of a fresh copy.
5. Fix what RB-6 finds on `release/14/plan-61`. Ask D3. Run the review R, with a reviewer who did not write the tool, against the commit RB-6 ran.
6. RB-7: merge the current `release/14/main` into `release/14/plan-61` in astrid-app and astrid-dev (never rebase), rerun the unit test, the fixture and one `update` with nothing moved, and get hosted CI green on the exact head. The astrid-app pull request must name Plan 61 for the `landing reference` check. Then merge each plan branch into its `release/14/main`, set both rows in [`releases/14.md`](../../releases/14.md#branches) to `merged`, and run `python3 scripts/release_branches.py check 14`.
7. File the drafted issues if the owner says so. Ask D4 if it still matters.
8. Close the project through the Manage skill's completion PR: Status to `done`, the run record filled, a short note on what Plan 62 may now start from. Leave Plan 62's release to the owner. Delete nothing that is not merged into `release/14/main`.

## What this run taught

- **Check the home before building.** The tool was first committed on another plan's branch, then proposed against a product `main`, with its docs on a side branch and its plan on a scope branch. Each was in the wrong place under the release rules, and moving them took more work than the first placement would have. A plan in Release 14 and later has a plan branch in each repository it changes, from day one.
- **A tool that is tested on the stack in use breaks it.** Two restarts happened without notice. Fixtures first, scratch roots next, the real stack last, with notice.
- **Something other than the agent that built a check should verify it.** Several "running" claims turned out wrong when read by someone else. This handover's "proven" column names the command and the place its output is recorded, so you can run it yourself.
- **One path.** Adopt could not copy a realm into a fresh install, so the realm is a snapshot plus the Runtime's `workspace attach`, and nothing else. Resist adding a second route.
- **Unknown cause, guarded net.** The first-start failure was never reproduced in ten tries in scratch. The retry is capped, names its exact message and keeps each failed log. Delete it when RB-9 names the cause.
- **Disk is a constraint, not a detail.** With about 3 GiB free and swap near full, one heavy job at a time; the fresh-clone proof needs about 5 GiB.
- **Run long steps in the foreground and report only what finished.** Several "running" claims in this work were wrong until someone else looked.
