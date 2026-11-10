# Strategy

Astrid's execution strategy is a sequence of **releases**, each a coherent step toward our [vision](vision/README.md). Each release document holds the living rationale, intended outcome, approach and included plans; this page is their short, ordered map.

The [plan catalog](plans/index.md) alone owns project status, priority, estimate and owner. [Vision gaps](vision/README.md) and their routes still define what needs to improve and how success will be assessed. A plan may be worked on before it is assigned to a release; an unassigned plan is not a release commitment.

**Last reviewed:** 2026-11-10, following the decision to make strategy release-led. Future assignments are provisional until explicitly finalized.

## Focus now

Finish the Release 12 candidate and its update/reliability proof under [Plan 29](plans/29-update-and-release/plan.md); the [release 12 run note](docs/ledger/2026-11-09-release-12-slow-path.md) documents what slowed qualification. In parallel, maintain the generation path through [Plan 32](plans/32-generation-placement-targets/plan.md) and the onboarding work in [Plan 20](plans/20-zero-to-first-image/plan.md). None of this silently adds a plan to a future release.

## Sequence

| Release | Highlight | Plans | Why this order |
|---|---|---|---|
| [Release 13 (draft)](releases/13.md) | Creators can see and control when their rented GPU machine stops and how much it can cost. | [Plan 40](plans/40-machine-lifetime-controls/plan.md) | Plan 40 is already targeted at Release 13 in the catalog; keep the rest of its scope open until the release is deliberately composed. |

The table is a summary, **not** a second definition of a release. Add a future row when its draft file is created; update the row whenever its highlight or included plans change. A published release's document remains as the historical ledger. [Plan 31](plans/31-releases-from-astrid-dev/plan.md) makes this workflow and its checks authoritative.

## Not now

Release assignments for [Plan 31](plans/31-releases-from-astrid-dev/plan.md), [Plan 30](plans/30-update-everywhere/plan.md), [Plan 38](plans/38-one-process-identity/plan.md) and other catalog work are not yet settled. Keep their sequencing and dependencies in the catalog and individual plan packs until a real release brief is created. Do not invent release numbers or force plans into a release for the sake of a tidy table.

Past releases are documented in the [existing release log](plans/releases.md) and actual receipts. Plan 31 migrates that history into canonical release records only where it can be grounded in publication evidence; Release 11's publication race is recorded in the [ledger](docs/ledger/2026-11-09-two-projects-published-release-11.md).

## Decisions

- **2026-11-10:** Strategy is release-led: each release file starts as a living strategy brief, with a highlight, intent, approach and linked plans. The overview here is mainly a summary of those release files.
- **2026-11-10:** An unpinned draft can change on `main` without publishing; publication requires separate, explicit finalization and owner-approved, validated pins (Plan 31).
- **2026-11-08:** Installed-release publication remains separately authorized. Plan 31 follows Plan 29; generation work continues on its own track.

## Keeping this page current

When a draft release is added or changes its headline or included plans, update the matching sequence row in the same PR. When a release is published, keep its final document immutable and retain its summary in release history. CI checks the draft's basic structure and consistency with the overview; the Plan 31 release gate separately protects publication. Keep this page short: deeper reasoning belongs in the release document, gap route or plan.
