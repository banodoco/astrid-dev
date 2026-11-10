# Release 12, Track B — Generation

[Release 12](../12.md) · [Track A: Fixes](fixes.md) · Handoffs: [Plan 32](../../plans/32-generation-placement-targets/handoff.md), [Plan 40](../../plans/40-machine-lifetime-controls/handoff.md), [Plan 20](../../plans/20-zero-to-first-image/handoff.md), [Plan 34](../../plans/34-real-gpu-proof/handoff.md) · [All-plans orchestrator handoff](../../docs/handoffs/2026-11-10-orchestrator.md)

**Purpose:** finish the generation work and deliver it to Track A as **one** reviewed, CI-compared and GPU-proven generation candidate that merges cleanly into the Release 12 candidate. Exact SHAs, evidence and restart points are in each plan's handoff; this page is the plan at the level a lead manager needs. State as of 10 Nov 2026.

## What this track delivers

| Plan | Delivers | State |
|---|---|---|
| [32](../../plans/32-generation-placement-targets/plan.md) | One generation path, `astrid generate --placement local\|runpod`, with paid consent, leases and warm reuse | Tasks done; three review rounds consumed. Pushed head `plan32/staging-int32` `d28cac190`, which includes the Plan 34 TTS-prompt and warm-receipt fixes. Open: CI comparison, completion (T8) |
| [40](../../plans/40-machine-lifetime-controls/plan.md) | `astrid machines`: when a machine stops and what it costs; keep, setup, claim, release; `--gpu` and `--datacenter`; waiting for capacity | T1–T8 integrated on `plan40/staging-int40` `b15e286b6`, built on int/32. Open: review blockers R1.1–R1.4, then **T9**, which keeps a machine after a failed job |
| [20](../../plans/20-zero-to-first-image/plan.md) | From the install line to a first image: setup skill, App handoff, default skills | Agent `plan20/staging-agent` `d2a84370f`; App `plan20/staging-app` `e61607a1a`. Phase 1.5 waits for the release revision. VibeComfy [#165](https://github.com/banodoco/VibeComfy/pull/165) and [#166](https://github.com/banodoco/VibeComfy/pull/166) are open |
| [34](../../plans/34-real-gpu-proof/plan.md) | Live GPU proof of every default slot through the product | Passed: image t2i, image edit, music, capacity wait and claim. TTS fails (`input_rejected`, cause unknown until T9). SFX needs both VibeComfy pins at `af5cb429`. Video is ready, not run. $3.13 of the $20 stop spent; 0 pods |

## The hierarchy

```text
Plan 32  int/32 (one generation path)          ← the base
  └─ Plan 40  int/40 (machine controls, T9)    ← built on int/32
  └─ Plan 20  int/20 (onboarding)              ← built on int/32; App side too
        ↓ composed into one generation candidate (Agent), plus Plan 20's App branch
Plan 34  GPU proof on that candidate           ← tests, doesn't change the code
        ↓ checkpoint B
Merge into Track A's cand/29-r12
```

Product bugs Plan 34 finds go to the plan that owns the code (32, 40 or 20). Plan 34 reproduces them and reports; it doesn't patch other plans' code.

## Tasks, in order

| # | Task | Lane | Depends on | Done when |
|---|---|---|---|---|
| B1 | Plan 40 R1.1–R1.4, the review's blocking findings | Plan 40 | — | Focused proof per card |
| B2 | Plan 40 **T9**: keep a failed job's machine within consented limits, with a bounded safe failure summary; then its own focused review | Plan 40 | B1 | Reviewed T9 SHA posted |
| B3 | Plan 32: refresh its R12 rehearsal against Track A's latest Agent candidate. Port the `d70bed508` repair explicitly; it can't be replayed automatically | Plan 32 | — (repeat each time A's candidate moves) | Rehearsal merges cleanly with focused proof |
| B4 | **Compose the generation candidate:** int/32 staging → merge int/40 (after B2) → merge Plan 20 Agent staging, all `--no-ff`, focused proof of each plan on the composed head | Generation lead | B1, B2 | One pushed generation candidate branch |
| B5 | Plan 20 App: merge App `cand/29-r12` into `plan20/staging-app`; re-prove P2.3, P2.4 and the R2 repairs | Plan 20 | — | App branch merges cleanly with Track A's App candidate |
| B6 | **GPU proof (Plan 34)**, one waiting product command per cell, census around each rental: **video** (i2v, v2v, edit) now; **SFX** on a candidate with **both** VibeComfy pins at `af5cb429`, verifying the pod's HEAD; **TTS** after B2, so a failure leaves the pod up to diagnose | Plan 34 | Video: none. SFX: one-source pin or both pins set. TTS: B2 | Each default slot passed, with receipts in [#260](https://github.com/banodoco/astrid-dev/pull/260) |
| B7 | **One Agent CI comparison** on the generation candidate (or on its rehearsal merge with Track A's candidate), against current baselines by the run contract's regression rule | Generation lead | B4 | No regressions; it stands in for Plan 32's and Plan 40's CI gates |
| B8 | Completion records: Plan 32 T8 draft [#276](https://github.com/banodoco/astrid-dev/pull/276) refreshed; Plan 40 phase review; Plan 20 P1.5 proof on the exact candidate | Record | B4–B7 | Completion PRs ready, linked from the release |
| **Checkpoint B** | Candidate reviewed, CI comparison clean, GPU cells passed, rehearsal merge with Track A clean | — | B1–B8 | Hand to Track A for the merge |

**Parallelism:**
- B1, B3, B5 and GPU video run at once.
- B2 waits for B1, and TTS waits for B2.
- B4 composes once B2 lands. Earlier interim compositions are fine for GPU work that doesn't touch T9.
- Each new candidate SHA is posted to Plan 34, which reruns a passed cell only if its code path moved.

## Rules for this track

- **GPU (Hannah's rules):**
  - one waiting product command per test, with no time window;
  - no geographic filters;
  - the cheapest adequate GPU;
  - one test at a time unless isolated;
  - a census before and after every rental, and every pod released;
  - stop at $20.
- **Pins:** the VibeComfy pin moves through the release pin, never as a merge to VibeComfy `main`. The candidate must pin it in **both** the install manifest and the engine recipe.
- **Reviews:** budgets already consumed stay consumed (Plan 32 used 3 of 3; Plan 40 used 1 of 1; Plan 20 R2 used 1 of 1). New merge changes get scoped, independent reviews.
- **General:** never weaken a check; merge commits only; no force-push; no pushes to product `main`.
