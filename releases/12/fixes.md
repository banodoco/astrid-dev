# Release 12, Track A — Fixes

[Release 12](../12.md) · [Track B: Generation](generation.md) · [Plan 29 handoff](../../plans/29-update-and-release/handoff.md) · [Plan 29 orchestrator brief](../../plans/29-update-and-release/orchestrator-brief.md)

**Purpose:** finish the Release 12 candidate that has been in qualification since 9 Nov, then receive Track B's merge and run the release's one final qualification. This track owns the candidate branches and the publish. Exact SHAs, evidence and restart points are in the [Plan 29 handoff](../../plans/29-update-and-release/handoff.md). This page is the plan at the level a lead manager needs. State as of 10 Nov 2026.

## What this track delivers

The Release 11 field-failure follow-ups, the review-round fixes, and every product regression against Release 10 (Plan 39 decision D8). After the merge, this track also owns qualifying and publishing the combined release.

## Where it stands

| Area | State |
|---|---|
| **Agent** | `cand/29-r12` = `313bbd46f`. The next candidate, `r12/cand-next` = `733ac5a43`, adds five fixes: personal-pack snapshots, the ready-marker fence, the schema cache, Windows read-only cleanup, and HOME in the update job and handoff launcher. It is **not proven yet**: its before/after comparison must be rerun. Base failures are recorded in [agent-comparison.md](../../plans/29-update-and-release/evidence/r12/agent-comparison.md) |
| **App** | `cand/29-r12` = `8cfe10ce7` (Direct Journey rounds 3–6). The last early Direct Journey had 2 failures open: `:1264` (a seed helper uses the retired save route) and `:649` (Runtime restart, the draft survives). Two real product bugs in the conflict and recovery flow were found and fixed on the way |
| **Harness** | `harness/29-r12` = `b550ecadf` |
| **Matrix** | The last full run was 4 of 11 green. Every failing row has a root cause and a fix or a rerun ([verdicts](../../plans/29-update-and-release/evidence/r12/matrix-42835188782.md)) |
| **Reviews** | Rounds 1–3 done; round 3's blockers are fixed in `733ac5a43`. Round 4 is due on those fixes |
| **Not yet adopted** | Plan 32 found a Windows pack-exchange recovery bug introduced by `35c170e39`: crash recovery can delete the previous generation. Its reviewed fix is on donor branch `plan32/r12-windows-recovery-donor` (`26380e3a`). Check it against `989cd0f6c`, adopt it, and prove it |

## Tasks, in order

| # | Task | Owner lane | Depends on | Done when |
|---|---|---|---|---|
| A1 | Rerun the Agent before/after comparison: `733ac5a43`, R11 and R10, against the recorded base | Agent | — | No new failures; regressions against R11 or R10 fixed |
| A2 | Adopt the Windows recovery donor `26380e3a` (merge `--no-ff`, focused proof, both parents compared) | Agent | A1 running | Its focused Windows tests pass on the candidate |
| A3 | Push the Agent candidate to `cand/29-r12`; then review round 4 on `313bbd46f..cand` | Agent + Review | A1, A2 | No open blocker |
| A4 | Direct Journey round 7 onward (`:1264`, `:649`), then early Direct Journey runs until 0 failures. Diagnose from traces | App | — | Direct Journey 0 on the fixes-only tuple |
| A5 | VibeComfy pin consistency: the install manifest and the engine recipe pin VibeComfy separately and can disagree. Add an install-time match check, or derive one pin from the other | Agent | — | One source, or a failing check on mismatch |
| **Checkpoint A** | A fixes-only tuple: one re-pin commit, then App Tests, Direct Journey and the matrix, as a confidence run | Matrix | A3, A4 | Green, or failures diagnosed and owned. It separates fixes failures from generation failures before the merge |
| A6 | **Receive the merge** from Track B (see below) | Agent + App | Checkpoints A and B | Merged heads pushed |
| A7 | The final round on one tuple ([gate](../12.md#gate-both-tracks-merged-tuple)) | All lanes | A6 | Gate holds |
| A8 | Publish with the Release skill; post-publish notices; Hannah's Mac confirmation | Orchestrator | A7 | Published and confirmed |

A1–A5 run in parallel where their dependencies allow. Checkpoint A costs one round of runners. Skip it only if Track B is already at its checkpoint, and then go straight to the merge.

## Receiving the merge

- **Agent:** Track B's generation candidate merges `--no-ff` into `cand/29-r12`. Track B prepares and rehearses it; this track's Agent lane performs it and runs the focused proof of both sides on the merged head.
- **App:** Plan 20's App work (`plan20/staging-app`, already merged with App `cand/29-r12` by Track B) merges into App `cand/29-r12`.
- **Pins:** one App re-pin commit pins the final Agent SHA, regenerates the vendor lock, and sets VibeComfy to the release's SHA in **both** places. It then runs `vendor-lock.mjs check`, the runtime lock check, `cliSurfaceVerbs.test.ts`, `pin.mjs --check` and `release-guard`.
- **Review:** one release review round on the merge delta, alongside the final round.

## Rules for this track

- Never weaken a check. Prove "test drift" from the trace.
- Every Agent batch gets a before/after comparison before it is pushed to `cand`.
- Installer changes run every `tests/test_installer_*.py`.
- Push by full GitHub URL; never force-push; one PR per branch.
- Only the Release skill merges to product `main`.

The full list is in the [orchestrator brief](../../plans/29-update-and-release/orchestrator-brief.md#9-standing-constraints).
