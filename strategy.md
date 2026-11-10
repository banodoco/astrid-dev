# Strategy

What we're doing now, next and later, which [gaps](vision/README.md#gaps--17-assessed-outcomes) that closes, and why that order.

This page is the *why* and the sequence. Other facts each live in one place:
- the [plan catalog](plans/index.md): each project's order, status and owner;
- each gap's **Route to closure**: how that gap closes;
- each project's pack: its tasks and proof.

When a project finishes, its completion PR updates this page (enforced by `scripts/check_completion.py`).

**Last reviewed:** 2026-11-10, for Plan 32 completion preparation; the owner's priority order is unchanged. The liveness repair, i2v CPU journey and final exact-head CI comparison remain pending.

## Focus now

1. **[F-001 Platform reliability](vision/gaps/F-001-platform-reliability.md).** Release 10 (0.0.10) is published, but on a machine that already completed the Release 1 storage handoff, `install --update` exits 0 and installs nothing. Plan 29 is reopened to fix this (UR-15 and its follow-ups) and to publish Release 11 with a field receipt. Less common setups remain in [Plan 30](plans/30-update-everywhere/plan.md).
2. **[F-008 Portable generation](vision/gaps/F-008-portable-generation.md),** in parallel. Generation is what creators come for. It runs on its own track and follows [its route to closure](vision/gaps/F-008-portable-generation.md#route-to-closure).

## Sequence

| Order | When | Gap | Plans | What creators get | Waiting on |
|---|---|---|---|---|---|
| 1 | Now | [F-001](vision/gaps/F-001-platform-reliability.md) | [Plan 29](plans/29-update-and-release/plan.md) (reopened) | Update works after the storage handoff; Release 11 published with a field receipt | Fix UR-15 and UR-15b; the owner's go on Release 11 |
| 1 | Now | [F-008](vision/gaps/F-008-portable-generation.md) | [Plan 33](plans/33-unblock-live-generation/plan.md) | Plans 01, 02 and 06 landed on `main`, proven on CPU (9 Nov). Plan 32 replaces the interim pod route and includes h3_av; Plan 34 supplies the live proof | — |
| 1 | Now | [F-003](vision/gaps/F-003-creative-execution.md) | [Plan 20](plans/20-zero-to-first-image/plan.md) | One onboarding skill takes a person or their agent from the install line to Connected with choices they saw and could change, on the way to a first generated image | Runs alongside release 12 by the owner's go on 9 Nov; its Agent `main` merge waits for release 12 published and the owner's go |
| 2 | Next | [F-001](vision/gaps/F-001-platform-reliability.md) | [Plan 31](plans/31-releases-from-astrid-dev/plan.md) | Releases are defined, checked and published from astrid-dev, and users see versions such as 0.0.11 | the owner's go; Plan 29; astrid-dev `main` protection |
| 3 | Next | [F-001](vision/gaps/F-001-platform-reliability.md) | [Plan 39](plans/39-green-mains/plan.md) | Every product `main` passes its own checks and stays green, so a red check means a new regression, and releases need everything green | release 12 published |
| 4 | Next | [F-001](vision/gaps/F-001-platform-reliability.md) | [Plan 30](plans/30-update-everywhere/plan.md) | Updating also works on older Linux, and through Pinokio and fully local | the owner's go; Plan 29 |
| 5 | Now | [F-008](vision/gaps/F-008-portable-generation.md) | [Plan 32](plans/32-generation-placement-targets/plan.md) → [Plan 34](plans/34-real-gpu-proof/plan.md) | One generation path on managed local, attached and RunPod CPU stand-ins, followed by real-GPU proof. See the gap's reassessment for the candidate and limits | Liveness repair, exact i2v CPU journey and final-head CI comparison; Plan 34 owns the separate hardware proof |
| 6 | Later | [F-008](vision/gaps/F-008-portable-generation.md) | [Plan 12](plans/12-multiple-inference-routes/plan.md) ∥ [Plan 17](plans/17-vibecomfy-extensibility/plan.md) | A second engine, and packs that extend generation without changing core | Plan 32 |
| 7 | Later | [F-001](vision/gaps/F-001-platform-reliability.md) | [Plan 10](plans/10-pinokio-qualification/plan.md), [Plan 09](plans/09-install-and-update-confidence/plan.md) | Pinokio qualified natively; rollback, migrating updates and removal qualified | the owner's go; Plan 30 |

## Not now

These are deliberately deferred, so they aren't re-argued:
- Reshaping the catalog: cutting Plan 09 down to lifecycle qualification, retitling Plan 05, and fixing the gap links. All of these wait until Release 10 ships.
- Writing routes to closure for the other gaps, starting with F-001. Waits until Release 10 ships.
- Gaps with no planned work this quarter: AA, CA, CI, LS and F-002 to F-007. Their plans keep their catalog order.

## Decisions

- **2026-11-08:**
  - Release 10 first. Every follow-on project on this page waits for the owner's explicit go, even after Plan 29 ships; none starts automatically.
  - Plan 31 follows Plan 29.
  - Green mains is not a project (owner's go). Once Release 10 ships:
    - the [Release skill](skills/astrid-dev-release/SKILL.md) gains the rule that a publish never turns a passing check red, and each publish PR into a product `main` passes that repo's own checks;
    - today's red checks on the App, Agent and Runtime mains are fixed in one short batch of fix tasks;
    - once that batch has made the mains green, Manage drops its "ignore checks that were already failing" rule. Dropping it earlier would block every task merge.
  - Generation continues on its own track.

## Keeping this page current

- **Starting a project:** the planner reads this page first, and the plan names its row here.
- **Finishing a project:** its completion PR updates this page (the row, and focus or sequence if they changed) and its gap's route to closure.
- **Check-ins:** the advisor flags it when the catalog order and this page disagree.
- **Size:** keep it to one page. Detail belongs in gap routes and project packs.
