# Release 12, Track B — Generation

[Release 12](../12.md) · [Track A: Fixes](fixes.md) · Handoffs: [Plan 32](../../plans/32-generation-placement-targets/handoff.md), [Plan 40](../../plans/40-machine-lifetime-controls/handoff.md), [Plan 20](../../plans/20-zero-to-first-image/handoff.md), [Plan 34](../../plans/34-real-gpu-proof/handoff.md) · [All-plans orchestrator brief](../../docs/handoffs/2026-11-10-orchestrator.md)

**Purpose:** finish the generation work and hand Track A **one** generation candidate that is composed, rehearsal-merged with Track A's candidate, CI-compared, reviewed and GPU-proven. One manager runs each plan, all reporting to the orchestrator. Plan 32's manager composes the candidate. Exact SHAs, evidence and restart points are in each plan's handoff. This is a working brief, frozen when [Release 12](../12.md) becomes Final. State as of 10 Nov 2026.

## What this track delivers

| Plan | Delivers | State |
|---|---|---|
| [32](../../plans/32-generation-placement-targets/plan.md) | One generation path, `astrid generate --placement local\|runpod`, with paid consent, leases and warm reuse | Tasks done; 3 of 3 review rounds used. `plan32/staging-int32` `d28cac190` includes Plan 34's TTS-prompt and warm-receipt fixes. Its last CI and its baseline stopped at three collection errors, so no test-level comparison exists yet. Open: CI comparison, completion (T8, draft [#276](https://github.com/banodoco/astrid-dev/pull/276)) |
| [40](../../plans/40-machine-lifetime-controls/plan.md) | `astrid machines`: when a machine stops and what it costs; keep, setup, claim, release; `--gpu` and `--datacenter`; waiting for capacity | T1–T8 on `plan40/staging-int40` `b15e286b6`, built on int/32 `99724131d`, not on staging `d28cac190`. 1 of 1 review round used. Open: blockers R1.1–R1.4, then **T9**, which keeps a machine after a failed job |
| [20](../../plans/20-zero-to-first-image/plan.md) | From the install line to a first image: setup skill, App handoff, default skills | Agent `plan20/staging-agent` `d2a84370f`, on an older int/32 (`26eeaff4`), with Plan 29's donor `bc5aa747` cherry-picked. App `plan20/staging-app` `e61607a1a`. Review rounds used: R1 1/1, R2 1/1, R3 1 of 2 |
| [34](../../plans/34-real-gpu-proof/plan.md) | Live GPU proof of the in-scope slots through the product | Passed: image t2i and edit on `26eeaff4`, music on `e9cb9e6b9`, capacity wait and claim. These ran **before** T4, T5-R1, R1.x, T9 and the warm-receipt fix, so they need a second pass (G4). TTS fails (`input_rejected`, cause unknown until T9). SFX needs one VibeComfy release SHA. Video is ready on `plan34/candidate-17acda421`. $3.13 of the $25 stop spent (H2); 0 pods |

## The hierarchy

```text
Plan 32  int/32 (one generation path)          ← the base
  ├─ Plan 40  int/40 (machine controls, T9)    ← on int/32; must take staging + fix N
  └─ Plan 20  int/20 (onboarding)              ← on an older int/32; App side too
        ↓ Plan 32's manager composes ONE generation candidate (Agent)
        ↓ + one VibeComfy release SHA, reconciled ComfyUI and Runtime pins
        ↓ rehearsal-merged into Track A's cand/29-r12  → CI comparison + merge-delta review
Plan 34  GPU proof on that rehearsal head      ← tests, doesn't change the code
        ↓ checkpoint B → Track A performs the merge
```

Product bugs Plan 34 finds go to the plan that owns the code (32, 40 or 20). Plan 34 reproduces them and reports; it doesn't patch other plans' code.

## Tasks, in order

| # | Task | Owner | Depends on | Done when |
|---|---|---|---|---|
| B1 | Plan 40 R1.1–R1.4, the review's blocking findings | 40 | — | Focused proof per card |
| B2 | Merge staging `d28cac190` and Plan 34 fix N `e0d95d7b8` (`plan34/fix-failure-diagnostics`) into int/40. Both are prerequisites of T9 | 40 | B1 | Focused proof on the merged head |
| B3 | Plan 40 **T9**: keep a failed job's machine within consented limits, with a bounded safe failure summary; then its own focused review | 40 | B2 | Reviewed T9 SHA posted |
| B4 | **Pins:** one VibeComfy release SHA combining [#165](https://github.com/banodoco/VibeComfy/pull/165) (`38969618`) and [#166](https://github.com/banodoco/VibeComfy/pull/166) (`af5cb429`) on a release branch, not merged to VibeComfy `main`; set in the Agent's engine recipe (via Track A's A1b) and the App manifest. Reconcile ComfyUI (`423cbd20` in Plan 32 vs `ee71d5c4` in R12) and the Runtime (`4f5477cb` under the earlier proof vs `42ae24aff` in the candidate). One value each, recorded | 32 + orchestrator | — | Pins agreed; VibeComfy SHA pushed |
| B5 | **Compose the generation candidate**, all `--no-ff`: int/32 staging, then int/40 (after B3), then Plan 20 Agent staging. Plan 20's manager resolves its old int/32 base and the duplicate Plan 29 donor. Run focused proof of each plan on the composed head | 32 (20 and 40 assist) | B3, B4 | One pushed generation candidate |
| B6 | Plan 20 App: merge App `cand/29-r12` into `plan20/staging-app`; re-prove P2.3, P2.4 and the R2 repairs. P2.3's generation link must not go live before S2 is on Agent `main` | 20 | — | Merges cleanly with Track A's App candidate |
| B7 | **Rehearsal merge** of the candidate into Track A's latest `cand/29-r12`; repeat whenever either side moves. Port the `d70bed508` repair explicitly | 32 | B5; Track A's A3 | Clean merge, focused proof |
| B8 | Fix the three CI collection errors, then run **one** Agent CI comparison on the B7 rehearsal head, with Track A's candidate as the baseline | 32 | B7 | Test-level comparison, no regressions. It stands in for Plans 32 and 40's CI gates |
| B9 | **Merge-delta release review**, one round, on the B7 head | Review | B7 | No open blocker |
| B10 | **GPU proof (Plan 34)** on the B7 rehearsal head: the in-scope slots, including same-pod warm reuse (H3), plus G4's second pass. Video can start now on `plan34/candidate-17acda421`, as a first look. SFX runs after B4, verifying the pod's VibeComfy HEAD. TTS runs after B3, so a failure leaves the pod up to diagnose. One waiting product command per cell, with a census around every rental | 34 | B4, B3, B7; $25 stop (H2) | Each in-scope slot passed, receipts in [#260](https://github.com/banodoco/astrid-dev/pull/260); then Plan 34's final review |
| B11 | Completion records: Plan 32 T8, Plan 40's phase, Plan 20 P1.5 proof on the exact head | Each plan | B8–B10 | Completion PRs ready, linked from the release |
| **Checkpoint B** | B7 merge clean; B8, B9 and B10 passed | — | — | Hand to Track A; the merge is a repeat of B7 |

**Parallelism:**
- B1, B4, B6 and the first-look video run start at once. B2 → B3 is the critical path, because TTS waits for T9.
- B7 can start on an interim composition, before T9, to surface merge conflicts early. The final B7 → B10 run on the full candidate.
- Every new candidate SHA is posted to Plan 34, which reruns a passed cell if its code path or pins moved.

## Rules for this track

- **GPU (Hannah's rules):**
  - one waiting product command per test, with no time window;
  - no geographic filters;
  - the cheapest adequate GPU;
  - one test at a time unless isolated;
  - a census before and after every rental, and every pod released;
  - stop at $25 (H2).
- **Pins:** VibeComfy changes reach users only through the release pin, never as a merge to VibeComfy `main`.
- **Reviews:** budgets already used stay used. New merge changes get the scoped merge-delta review (B9) and focused independent reviews.
- **General:** never weaken a check; merge commits only; no force-push; no pushes to product `main`.
