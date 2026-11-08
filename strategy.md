# Strategy

What we're doing now, next and later, which [gaps](vision/README.md#gaps--17-assessed-outcomes) that closes, and why that order.

This page is the *why* and the sequence. Other facts each live in one place:
- the [plan catalog](plans/index.md): each project's order, status and owner;
- each gap's **Route to closure**: how that gap closes;
- each project's pack: its tasks and proof.

When a project finishes, its completion PR updates this page (enforced by `scripts/check_completion.py`).

**Last reviewed:** 2026-11-08, by the owner with the advisor.

## Focus now

1. **[F-001 Platform reliability](vision/gaps/F-001-platform-reliability.md).** Update now has never worked on a published install, so every other improvement reaches users only by reinstalling. Plan 29 makes updating work on Linux, macOS and Windows and publishes Release 10. Until that ships, it comes first.
2. **[F-008 Portable generation](vision/gaps/F-008-portable-generation.md),** in parallel. Generation is what creators come for. It runs on its own track and follows [its route to closure](vision/gaps/F-008-portable-generation.md#route-to-closure).

## Sequence

| Order | When | Gap | Plans | What creators get | Waiting on |
|---|---|---|---|---|---|
| 1 | Now | [F-001](vision/gaps/F-001-platform-reliability.md) | [Plan 29](plans/29-update-and-release/plan.md) | Update now works on Linux, macOS and Windows; Release 10 | the owner's go on the release candidate |
| 1 | Now | [F-008](vision/gaps/F-008-portable-generation.md) | [Plan 33](plans/33-unblock-live-generation/plan.md) → [Plan 34](plans/34-real-gpu-proof/plan.md) | Every default slot and h3_av produce results on RunPod, proven on real GPUs | see the catalog |
| 2 | Next | [F-001](vision/gaps/F-001-platform-reliability.md) | [Plan 31](plans/31-releases-from-astrid-dev/plan.md) | Releases are defined, checked and published from astrid-dev, and users see versions such as 0.0.11 | the owner's go; Plan 29; astrid-dev `main` protection |
| 3 | Next | [F-001](vision/gaps/F-001-platform-reliability.md) | Green mains (proposed): a Release rule plus a one-off fix batch, not a plan | Every product `main` passes its own checks, so a red check means a new regression | Release 10 ships |
| 4 | Next | [F-001](vision/gaps/F-001-platform-reliability.md) | [Plan 30](plans/30-update-everywhere/plan.md) | Updating also works on older Linux, and through Pinokio and fully local | the owner's go; Plan 29 |
| 5 | Now | [F-008](vision/gaps/F-008-portable-generation.md) | [Plan 32](plans/32-generation-placement-targets/plan.md) | The same generation request runs the same way on any machine | runs alongside Plan 33, on functions Plan 33 doesn't touch (owner, 8 Nov) |
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
    - Manage drops its "ignore checks that were already failing" rule;
    - today's red checks on the App, Agent and Runtime mains are fixed in one short batch of fix tasks.
  - Generation continues on its own track.

## Keeping this page current

- **Starting a project:** the planner reads this page first, and the plan names its row here.
- **Finishing a project:** its completion PR updates this page (the row, and focus or sequence if they changed) and its gap's route to closure.
- **Check-ins:** the advisor flags it when the catalog order and this page disagree.
- **Size:** keep it to one page. Detail belongs in gap routes and project packs.
