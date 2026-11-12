# Strategy

Astrid's execution strategy is a sequence of **releases**, each a coherent step toward our [vision](vision/README.md). Each release document holds the living rationale, intended outcome, approach and included plans; this page is their short, ordered map.

Each plan's own `plan.md` holds its status, owner and estimate, `plans/priority.md` holds the order, and the [plan catalog](plans/index.md) is generated from them. [Vision gaps](vision/README.md) and their routes still define what needs to improve and how success will be assessed. A plan may be worked on before it is assigned to a release; an unassigned plan is not a release commitment.

**Last reviewed:** 2026-11-12, for the completions of Plan 48 and Plan 51 (no release assignment changed; neither plan is in a release) after the 2026-11-11 split of Release 12 into Releases 12 and 13. Future assignments are provisional until explicitly finalized.

## Focus now

Ship [Release 12](releases/12.md), the update fixes under [Plan 29](plans/29-update-and-release/plan.md) plus the onboarding tour, as a fixes-only release ([task list](releases/12/fixes.md)). In parallel, make the generation path runnable and explainable without paid work, then rebuild it on published Release 12 as [Release 13](releases/13.md). The [release 12 run note](docs/ledger/2026-11-09-release-12-slow-path.md) documents what slowed qualification so far.

## Sequence

| Release | Highlight | Plans | Why this order |
|---|---|---|---|
| [Release 12 (draft)](releases/12.md) | Updating Astrid works reliably on every platform, and the new onboarding tour ships with it. | [Plan 29](plans/29-update-and-release/plan.md) | The fixes are close and field users need them; shipping them alone removes the generation merge, GPU proof and budget risk from their path ([task list](releases/12/fixes.md)). |
| [Release 13 (draft)](releases/13.md) | Creators generate media through one path, locally or on a rented GPU they control, and a failed generation comes back with a receipt that says why. | [Plan 32](plans/32-generation-placement-targets/plan.md), [Plan 40](plans/40-machine-lifetime-controls/plan.md), [Plan 20](plans/20-zero-to-first-image/plan.md), [Plan 34](plans/34-real-gpu-proof/plan.md) | Generation has an undiagnosed live TTS failure and needs a failure receipt and one clear launch path before paid proof; it rebuilds on published Release 12 ([task detail](releases/13/generation.md)). |

The table is a summary, **not** a second definition of a release. Add a future row when its draft file is created; update the row whenever its highlight or included plans change. A published release's document remains as the historical ledger. [Plan 31](plans/31-releases-from-astrid-dev/plan.md) makes this workflow and its checks authoritative.

## Not now

Release assignments for [Plan 31](plans/31-releases-from-astrid-dev/plan.md), [Plan 30](plans/30-update-everywhere/plan.md), [Plan 38](plans/38-one-process-identity/plan.md) and other catalog work are not yet settled. Keep their sequencing and dependencies in the catalog and individual plan packs until a real release brief is created. Do not invent release numbers or force plans into a release for the sake of a tidy table.

Past releases are documented in the [existing release log](plans/releases.md) and actual receipts. Plan 31 migrates that history into canonical release records only where it can be grounded in publication evidence; Release 11's publication race is recorded in the [ledger](docs/ledger/2026-11-09-two-projects-published-release-11.md).

## Decisions

- **2026-11-12:** [Plan 51](plans/51-astrid-dev-clean-up/plan.md) (the astrid-dev clean-up) is done. It was never assigned to a release, so [Release 12](releases/12.md) and [Release 13](releases/13.md) and their rows above are unchanged. It left the release skill and the GPU-validation skill alone. Its assessment and route in [CA-005](vision/gaps/CA-005-parallel-contribution.md) are updated; that gap stays open.
- **2026-11-11:** Hannah split the combined release. Release 12 is fixes-only and includes the onboarding-tour commits on App `main`; generation (Plans 32, 40, 20 and 34) is [Release 13](releases/13.md), built on published Release 12. This reverses the 10 Nov fold-in below.
- **2026-11-10:** Hannah folded the generation work (Plans 32, 40, 20 P1.5 and staged work, and Plan 34's proof) into Release 12 instead of a Release 13. The draft `releases/13.md` is folded into [Release 12](releases/12.md); the next release brief starts fresh after publish.
- **2026-11-10:** Strategy is release-led: each release file starts as a living strategy brief, with a highlight, intent, approach and linked plans. The overview here is mainly a summary of those release files.
- **2026-11-10:** An unpinned draft can change on `main` without publishing; publication requires separate, explicit finalization and owner-approved, validated pins (Plan 31).
- **2026-11-08:** Installed-release publication remains separately authorized. Plan 31 follows Plan 29; generation work continues on its own track.

## Keeping this page current

When a draft release is added or changes its headline or included plans, update the matching sequence row in the same PR. When a release is published, keep its final document immutable and retain its summary in release history. CI checks the draft's basic structure and consistency with the overview; the Plan 31 release gate separately protects publication. Keep this page short: deeper reasoning belongs in the release document, gap route or plan.
