# Release 12, Track A — Fixes

[Release 12](../12.md) · [Track B: Generation](generation.md) · [Plan 29 handoff](../../plans/29-update-and-release/handoff.md) · [Plan 29 orchestrator brief](../../plans/29-update-and-release/orchestrator-brief.md)

**Purpose:** finish the Release 12 candidate that has been in qualification since 9 Nov. Then receive Track B's merge and run the release's one final qualification and publish. Plan 29's manager runs this track. Exact SHAs, evidence and restart points are in the [Plan 29 handoff](../../plans/29-update-and-release/handoff.md). This is a working brief, frozen when [Release 12](../12.md) becomes Final. State as of 10 Nov 2026.

## What this track delivers

The Release 11 field-failure follow-ups, the review-round fixes, and every product regression against Release 10 (Plan 39 decision D8). It also owns the candidate branches, the merge, the final qualification and the publish.

## Where it stands

| Area | State |
|---|---|
| **Agent** | `cand/29-r12` = `313bbd46f`. The next batch, `r12/cand-next` = `733ac5a43`, adds five fixes: personal-pack snapshots, the ready-marker fence, the schema cache, Windows read-only cleanup, and HOME in the update job and handoff launcher. It is **not proven yet**. Base failures are recorded in [agent-comparison.md](../../plans/29-update-and-release/evidence/r12/agent-comparison.md) |
| **App** | `cand/29-r12` = `8cfe10ce7` (Direct Journey rounds 3–6). The last early Direct Journey had 2 failures open: `:1264` (a seed helper uses the retired save route) and `:649` (Runtime restart, the draft survives). Two real product bugs in the conflict and recovery flow were found and fixed on the way |
| **Harness** | `harness/29-r12` = `b550ecadf` |
| **Matrix** | The last full run was 4 of 11 green. Every failing row has a root cause and a fix or a rerun ([verdicts](../../plans/29-update-and-release/evidence/r12/matrix-42835188782.md)) |
| **Reviews** | Rounds 1–3 done; round 3's blockers are fixed in `733ac5a43`. Round 4 is due |
| **Not yet adopted** | A Windows pack-exchange recovery bug, introduced by `35c170e39` and found by Plan 32: crash recovery can delete the previous generation. Its reviewed fix is on donor `plan32/r12-windows-recovery-donor` (`26380e3a`). Plan 32 calls it a Release 12 blocker needing native-Windows proof |

## Tasks, in order

| # | Task | Depends on | Done when |
|---|---|---|---|
| A1 | Into `r12/cand-next`, merge `--no-ff`: the Windows donor `26380e3a` (checked against `989cd0f6c`, both parents compared), and **A1b**, one source for the VibeComfy pin. The engine recipe (`astrid/packs/vibecomfy/pins.json`, and audit `astrid/packs/runpod/pins.json`) must derive from, or be checked against, the install manifest's pin at install | — | Both merged, focused proof passes |
| A2 | **One** before/after comparison on that head, against the recorded base, R11 and R10 | A1 | No new failures; any regression against R11 or R10 fixed |
| A3 | Push to `cand/29-r12`; review round 4 on `313bbd46f..cand` | A2 | No open blocker. Post the SHA to Track B, which rehearses against it |
| A4 | Direct Journey round 7 onward (`:1264`, `:649`), then early Direct Journey runs until 0 failures. Diagnose from traces | — (parallel with A1–A3) | Direct Journey 0 |
| **Checkpoint A** | Re-pin commit #1 (fixes-only tuple), then App Tests, Direct Journey and the full matrix | A3, A4 | Green, **including the Windows rows**, which are the donor's native proof. This separates fixes failures from generation failures before the merge |
| A5 | **Receive the merge** (see below) | Checkpoints A and B | Merged heads pushed |
| A6 | Re-pin commit #2 (final tuple), then the final round ([gate](../12.md#gate-merged-tuple)) | A5 | Gate holds |
| A7 | Publish with the Release skill, after Hannah's go (H1); post-publish work; Hannah's Mac confirmation | A6 | Published and confirmed |

## Receiving the merge

- **Agent:** Track B's generation candidate merges `--no-ff` into `cand/29-r12`. It repeats the rehearsal merge that was reviewed and CI-compared at checkpoint B. **Check the resulting tree equals the rehearsal's tree**; if it differs, the delta goes back for review before qualifying.
- **App:** Plan 20's App work (`plan20/staging-app`, already merged with App `cand/29-r12` by Track B) merges into App `cand/29-r12`.
- **Re-pin commit #2** pins:
  - the final Agent SHA (which already carries the VibeComfy and ComfyUI pins);
  - the VibeComfy release SHA in the App's install manifest;
  - the Runtime, as reconciled by Track B;
  - a regenerated vendor lock.

  It then runs `vendor-lock.mjs check`, the runtime lock check, `cliSurfaceVerbs.test.ts`, `pin.mjs --check` and `release-guard`.

## Rules for this track

- Never weaken a check. Prove "test drift" from the trace.
- Every Agent batch gets a before/after comparison before it is pushed to `cand`.
- Installer changes run every `tests/test_installer_*.py`.
- Push by full GitHub URL; never force-push; one PR per branch.
- Only the Release skill merges to product `main`.

The full list is in the [orchestrator brief](../../plans/29-update-and-release/orchestrator-brief.md#9-standing-constraints).
