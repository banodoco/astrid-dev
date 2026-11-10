# Release 12, Track B — Generation

[Release 12](../12.md) · [Track A: Fixes](fixes.md) · Reference only: handoffs for [P32](../../plans/32-generation-placement-targets/handoff.md), [P40](../../plans/40-machine-lifetime-controls/handoff.md), [P20](../../plans/20-zero-to-first-image/handoff.md), [P34](../../plans/34-real-gpu-proof/handoff.md)

This page gives the **P32, P40, P20 and P34 managers** their orders. It is binding, together with [releases/12.md](../12.md). The plan handoffs are reference only, for SHAs, evidence and history. **Don't follow their "next action", "resume", "pick up", gate, freeze or budget text.** In particular, nobody pushes `int/**` or dispatches CI except B8. This is a working brief, frozen when Release 12 becomes Final. State as of 10 Nov 2026.

## Rules for every Track B manager

- **Never:**
  - push `int/**` or any `main`;
  - merge to VibeComfy `main`;
  - land `plan32/release*-ci-prep`;
  - rent a pod (only P34 rents);
  - weaken, skip or delete a test;
  - call anything done on CPU proof that needs GPU proof;
  - rerun CI, a review or a GPU cell without the orchestrator's OK.
- **Push:** only the branches named for you below. Merge commits only; never force.
- **Messages:** only to the orchestrator, using the labels in [hand-offs](../12.md#hand-offs-all-via-mailboxes).
- **While waiting:** `RUN-STATUS: WAITING <label> from <sender>` as the last line of your reply. Re-read `run/to-codex.md` first. If others may still need you, end `WAITING`, never `DONE`.
- **First action, every manager:** push a test commit to `scratch/<plan>-push-test`, and run `smoke.sh` once. Use the [How-to](../12.md#how-to-tools-every-manager-uses) for tests, dispatch, artifacts (`NEED-ARTIFACTS`) and disk.
- **Precedence:** these pages override your skills' and `manager-brief.md`'s `int/<NN>`, CI and GPU-flow rules.
- **Review budgets already used stay used:** P32 3/3, P40 1/1, P20 R1 1/1 and R2 1/1. P20 R3 has 1 round left. New merge changes are covered by the single merge-delta review (B9).

## START HERE — P40 manager

- **Do now:** B1, P40-R1.1–R1.4, on `plan40/staging-int40` (`b15e286b6`).
- **Then:** B2, merging `plan32/staging-int32` `d28cac190` and Plan 34 fix N `e0d95d7b8` (branch `plan34/fix-failure-diagnostics`). Then B3, **P40-T9** per its card in Plan 40's `tasks.md`, with its focused review.
- **Push:** `plan40/staging-int40` only.
- **Done when:** you have posted `P40-T9 sha=<sha>` (reviewed). Then end `WAITING CHECKPOINT-B from orchestrator`, not `DONE`, so you can answer P32's questions during composition.

## START HERE — P20 manager

- **Do now, in parallel:**
  1. Merge `plan32/staging-int32` `d28cac190` into `plan20/staging-agent` (`d2a84370f`), re-prove it, and post `P20-AGENT sha=<sha>`. Plan 29's donor `bc5aa747` is also in Track A's candidate; when the two copies meet at B5, keep one, and prove it with P20-P3.3b's selection and opt-out tests.
  2. B6: merge App `cand/29-r12` into `plan20/staging-app` (`e61607a1a`), re-prove P20-P2.3, P20-P2.4 and the R2 repairs, and post `P20-APP sha=<sha>`. If App `cand` moves later, repeat once when the orchestrator asks.
  3. B4a: create VibeComfy `release12/vibecomfy` from VibeComfy `main` (`e65f4941`), merging #165 (`38969618`) and #166 (`af5cb429`) `--no-ff`. Run their focused tests, push once, and post `VIBECOMFY-RELEASE sha=<sha>`. This is the one pin change Plan 20 makes; it overrides your handoff's hard limit for this release only.
- **The S2 rule** ("P2.3's link not live before S2 is on Agent `main`") is satisfied by shipping P2.3 and S2 in the same Release 12 tuple. Don't strip the link.
- **Push:** `plan20/staging-agent`, `plan20/staging-app` and VibeComfy `release12/vibecomfy`.
- **Done when:** `P20-AGENT`, `P20-APP` and `VIBECOMFY-RELEASE` are posted. Then end `WAITING CHECKPOINT-B from orchestrator`, to answer conflicts at B5.

## START HERE — P32 manager

- **Do now:** keep `plan32/staging-int32` current. The three CI collection errors are P29's task A0; fix any **further** collection errors caused by generation code on your staging branch.
- **When `P40-T9` and `P20-AGENT` arrive:** B5. Create `release12/gen-candidate` from `plan32/staging-int32`, then merge `--no-ff` exactly those two SHAs, int/40 first. Run each plan's focused proof on the head and post `B-CANDIDATE sha=<sha>`.
- **When `A-FROZEN` and `B-CANDIDATE` both exist:** B7. Create `release12/gen-rehearsal` from `A-FROZEN`'s Agent SHA, merge `release12/gen-candidate` `--no-ff`, port the `d70bed508` repair explicitly, run focused proof of all four plans, and post `FINAL-B7 sha=<sha>`. **Build it once.** If anything moves after that, ask the orchestrator.
- **Then, once each, on `FINAL-B7`:**
  - B8: dispatch Agent CI. Either `POST https://api.github.com/repos/banodoco/astrid-agent/actions/workflows/ci.yml/dispatches` with body `{"ref":"release12/gen-rehearsal"}`, or ask the orchestrator to dispatch it. Compare against `A-FROZEN`'s `ci-run`.
  - B9: the orchestrator runs the merge-delta review on `git log --merges --remerge-diff A-FROZEN..FINAL-B7`, plus the `d70bed508` port and the pin files. Each plan's own code was already reviewed by its own rounds.
- **Push:** `plan32/staging-int32`, `release12/gen-candidate` and `release12/gen-rehearsal`.
- **Done when:** B8 shows no regressions and B9 has no open blocker. Then refresh the P32-T8 completion draft [#276](https://github.com/banodoco/astrid-dev/pull/276) against `FINAL-B7`.
- **An early rehearsal on `A-CAND`,** to surface conflicts, is allowed once, on a scratch branch. It never replaces B7.

## START HERE — P34 manager

- **You learn SHAs only from your `run/to-codex.md`.** Don't watch `int/32`, which won't move.
- **Do now:** nothing paid. Prepare the cell inputs from the committed fixtures, and get `RUNPOD_API_KEY` from your environment (never print it). End `WAITING P40-T9 from P40`.
- **Installing a candidate:** follow [astrid-dev-gpu-validate](../../skills/astrid-dev-gpu-validate/SKILL.md) for the install and census mechanics only. The cell table below replaces its flow, its budget and its release-on-failure rule. For the TTS diagnosis, build a manifest override for the named candidate the way the [SFX audit](https://github.com/banodoco/astrid-dev/blob/plan34/gpu-validation-2026-11-10/validation/gpu/2026-11-10-sfx-candidate.md) did, and install with `run-astrid install --manifest <file>`. For the final cells, use `release12/candidate-manifest`, which P29 pushes at Checkpoint A, with the Agent SHA set to `FINAL-B7`.
- **When `P40-T9` arrives:** one **TTS diagnosis** run on a candidate the orchestrator names (the first-look pool). If it fails, the pod stays up, and you inspect it within T9's limits. Report the cause.
- **When `FINAL-B7` arrives:** install from `release12/candidate-manifest` with `FINAL-B7`'s Agent, verify the pod's VibeComfy HEAD equals `VIBECOMFY-RELEASE`, then run the in-scope cells below, **each once**. Up to **two at a time**, each in its own isolated install and data root, as Hannah's rules allow. Post each result.
- **Rules:**
  - one waiting product command per cell, with no time window;
  - no geographic filters;
  - the cheapest adequate GPU;
  - a census before and after every rental, and every pod released;
  - **at $25 total, stop, release everything, and report `BLOCKED: budget`.**
- **A failed final cell:** report it. Rerun it once only after the owning plan's fix lands on a re-frozen `FINAL-B7`, and only with the orchestrator's OK.
- **Push:** the evidence branch `plan34/gpu-validation-2026-11-10` only, which updates record PR [#260](https://github.com/banodoco/astrid-dev/pull/260).
- **Done when:** every in-scope cell has passed on `FINAL-B7`, and the record PR is updated. Then run Plan 34's final review (H3: it runs, but doesn't gate).

## GPU cells

$3.13 is already spent. The caps below are ceilings, not targets.

| Cell | In scope? | Runs on | Max runs | Cap |
|---|---|---|---|---|
| TTS diagnosis | in | candidate with T9 | 1 | $3 (first-look pool) |
| image t2i | in | `FINAL-B7` | 1 | $1 |
| image edit | in | `FINAL-B7` | 1 | $1 |
| music | in | `FINAL-B7` | 1 | $1 |
| TTS | in | `FINAL-B7` | 1 | $3 |
| SFX | in | `FINAL-B7` | 1 | $3 |
| video i2v, v2v, edit | in | `FINAL-B7` | 1 each | $2 each ($6) |
| same-pod warm reuse (second job, same pod) | in (H3) | `FINAL-B7` | 1 | $1 |
| reruns after a fix | — | re-frozen `FINAL-B7` | orchestrator's OK | from what's left of the $25 |
| local-managed, attached, h3_av | **out** until Hannah decides (H3) | — | 0 | — |

The planned total is $3.13 + $3 + $16 = $22.13, leaving about $2.87 for reruns, which is less than one TTS rerun. If a rerun needs more than what's left, post `BLOCKED: budget`; the orchestrator asks Hannah.

## Task index (for the orchestrator)

| # | Task | Owner | Depends on |
|---|---|---|---|
| B1 | P40-R1.1–R1.4 | P40 | — |
| B2 | staging + fix N into int/40 | P40 | B1 |
| B3 | P40-T9 + focused review | P40 | B2 |
| B4 | Pins: VibeComfy release (P20, B4a); ComfyUI and Runtime per the [pin rule](../12.md#pins-default-rule-b4) | P20 + orchestrator | — |
| B5 | Compose `release12/gen-candidate` | P32 | B3, P20's merge |
| B6 | P20 App branch merges App `cand/29-r12` | P20 | — |
| B7 | `release12/gen-rehearsal` → `FINAL-B7` | P32 | `A-FROZEN`, B5 |
| B8 | One Agent CI on `FINAL-B7` vs `A-FROZEN` | P32 | B7 |
| B9 | One merge-delta review | Orchestrator | B7 |
| B10 | GPU cells | P34 | B7, B4 |
| B11 | Completion records (P32-T8, P40 phase, P20-P1.5 proof) | Each plan | B8–B10 |

`CHECKPOINT-B` is posted by the orchestrator when B8, B9 and B10 are clean.
