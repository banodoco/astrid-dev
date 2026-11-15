# Path to 1.0

**Aim:** Make Astrid a dependable place to create finished work with agents and open tools that people can shape and share.

## Where we are

Astrid has the beginnings of a workspace where people and agents can make creative work together. The immediate work is to make that everyday experience dependable: fast generation, clear failures, reliable installation and updates, and work that survives changes to the software.

## At 1.0

A creator should be able to take a project through repeated revisions to finished work, with their materials and decisions intact. They can work on their own machine or use one they rent, stay in control of what agents do, and adapt the workspace through packs. A useful tool or technique should be something another creator can build on. These are practical steps toward the [vision](vision/README.md).

## How we get there

First, make what Astrid already does fast and dependable. Version 0.1 brings together local speed, stability, installation and updates, then hardening and documentation. After that, choose the next steps from real creative work and the problems people encounter. Version 0.2 is open; its candidates are not commitments. Each release brief says what it delivers and why, and the groups below show how those releases build toward each version.

**Last reviewed:** 2026-11-15. The recorded release and version decisions below stand; this opening and the 0.1 wording are a draft for the owner's rewrite under [Plan 58](plans/58-strategy-from-releases/plan.md).

## Focus now

[Release 12](releases/12.md) (updates and the onboarding tour) and [Release 13](releases/13.md) (one generation path, locally or on a rented GPU) are out. Their briefs remain Draft until [Plan 31](plans/31-releases-from-astrid-dev/plan.md) verifies their final records. Next: [version 0.1](#version-01), starting with local speed in [Release 14](releases/14.md).

Each release has one theme, plus a standing lane for fixes and small plans that come from actual usage and user reports.

## Versions

Each version's aim and context are written here. Its releases and their contributions come from the release briefs. An undecided version says `Open`. The [contribution guide](docs/contribution-workflow.md#review-the-strategy) explains how the levels fit together.

### Version 1.0

**Aim:** [The aim at the top of this page](#path-to-10), with the outcome described in [At 1.0](#at-10).

#### Version 0.1

**Aim:** What Astrid already does, made fast and dependable: hardening, updates, stability and speed.

This is the first version we intend to call stable. A new person should be able to install, update and generate unaided on Windows, macOS and Linux, with every test green and documentation that takes them from purpose to a first result. The work hardens the capabilities already present; the decisions still open in [Release 17](releases/17.md#approach) remain open.

**Plans:** [Plan 55](plans/55-local-speed/plan.md), [Plan 52](plans/52-issue-intake/plan.md), [Plan 39](plans/39-green-mains/plan.md), [Plan 50](plans/50-recorded-boundaries/plan.md), [Plan 40](plans/40-machine-lifetime-controls/plan.md), [Plan 29](plans/29-update-and-release/plan.md), [Plan 30](plans/30-update-everywhere/plan.md), [Plan 09](plans/09-install-and-update-confidence/plan.md), [Plan 38](plans/38-one-process-identity/plan.md), [Plan 31](plans/31-releases-from-astrid-dev/plan.md), [Plan 19](plans/19-first-principles-documentation/plan.md)

**Releases:** [Release 14](releases/14.md), [Release 15](releases/15.md), [Release 16](releases/16.md), [Release 17](releases/17.md)

#### Version 0.2

**Aim:** Open

**Plans:** None yet

#### Version 0.3

**Aim:** Open

**Plans:** None yet

#### Version 0.4

**Aim:** Open

**Plans:** None yet

#### Version 0.5

**Aim:** Open

**Plans:** None yet

#### Version 0.6

**Aim:** Open

**Plans:** None yet

#### Version 0.7

**Aim:** Open

**Plans:** None yet

#### Version 0.8

**Aim:** Open

**Plans:** None yet

#### Version 0.9

**Aim:** Open

**Plans:** None yet

### Candidates, not yet in a version

Version 0.2 is open. These are the candidates so far, from Release 13's deferred list, the owner's requests and the plan catalog; none is assigned:

- **Set up any workflow in one step:** its models and node packs, with a recorded answer for what cannot be found ([Plan 56](plans/56-workflow-setup/plan.md), decisions made 15 November 2026; [issue 665](https://github.com/banodoco/astrid-dev/issues/665) for identifying unknown models). Its small corrections can ship earlier in the standing lane.
- **Generation complete:** every bundled workflow ready, video models beyond the default, the rest of onboarding ([Plan 20](plans/20-zero-to-first-image/plan.md), [Plan 32](plans/32-generation-placement-targets/plan.md)); frames at positions on the default video workflow (first frame, last frame or any position, one feature).
- **Finish a video:** generate onto the timeline, agent edits that never overwrite the creator's, export ([Plan 37](plans/37-generate-time-destination/plan.md), [Plan 04](plans/04-concurrent-edits/plan.md), [Plan 18](plans/18-timeline-editing/plan.md), [Plan 27](plans/27-video-render-options/plan.md)). Three of these are goals without tasks; walk one real video end to end before scoping.
- **Rented machines:** speed and the slow first job ([Plan 54](plans/54-warm-latency/plan.md)).
- **Packs extend the database:** a pack adds its own tables and rows, with Astrid's own fields protected, updates accommodated and destructive actions refused; features such as references then become default-installed packs ([Plan 57](plans/57-pack-database-extensions/plan.md), a draft; the owner asked for it on 15 November 2026 as one for after version 0.1).

## Sequence

| Release | Highlight | Plans | Why this order |
|---|---|---|---|
| [Release 12 (draft)](releases/12.md) | Updating Astrid works reliably on every platform, and the new onboarding tour ships with it. | [Plan 29](plans/29-update-and-release/plan.md) | The fixes are close and field users need them; shipping them alone removes the generation merge, GPU proof and budget risk from their path ([task list](releases/12/fixes.md)). |
| [Release 13 (draft)](releases/13.md) | Creators generate media through one path, locally or on a rented GPU they control, and a failed generation comes back with a receipt that says why. | [Plan 32](plans/32-generation-placement-targets/plan.md), [Plan 40](plans/40-machine-lifetime-controls/plan.md), [Plan 20](plans/20-zero-to-first-image/plan.md), [Plan 34](plans/34-real-gpu-proof/plan.md) | Generation has an undiagnosed live TTS failure and needs a failure receipt and one clear launch path before paid proof; it rebuilds on published Release 12 ([task detail](releases/13/generation.md)). |
| [Release 14 (draft)](releases/14.md) | On your own computer with the model already loaded, a generation comes back in about the time the model takes. | [Plan 55](plans/55-local-speed/plan.md), [Plan 52](plans/52-issue-intake/plan.md) | The slowness is the roughest edge Release 13 ships with, and it rewrites the path every job takes, so it comes before stabilising that path. |
| [Release 15 (draft)](releases/15.md) | Every test passes on every platform and stays passing, and the generation failures users can hit are fixed. | [Plan 39](plans/39-green-mains/plan.md), [Plan 50](plans/50-recorded-boundaries/plan.md), [Plan 40](plans/40-machine-lifetime-controls/plan.md) | Not being green cost Release 13 hours of telling new failures from old; doing it after the speed release avoids stabilising code that is about to be replaced. |
| [Release 16 (draft)](releases/16.md) | Installing, updating, rolling back and removing Astrid works on Windows, macOS and Linux, and you can see which version you have. | [Plan 29](plans/29-update-and-release/plan.md), [Plan 30](plans/30-update-everywhere/plan.md), [Plan 09](plans/09-install-and-update-confidence/plan.md), [Plan 38](plans/38-one-process-identity/plan.md), [Plan 31](plans/31-releases-from-astrid-dev/plan.md) | A stable version must survive its own updates on every system. |
| [Release 17 (draft)](releases/17.md) | Version 0.1: Astrid installs, updates and generates quickly and dependably on Windows, macOS and Linux, with every test green. | [Plan 19](plans/19-first-principles-documentation/plan.md) | Hardening only, once speed, stability and updates are in; this release carries version 0.1. |

The table is a summary, **not** a second definition of a release. Add a future row when its draft file is created; update the row whenever its highlight or included plans change. A published release's document remains as the historical ledger. [Plan 31](plans/31-releases-from-astrid-dev/plan.md) makes this workflow and its checks authoritative.

## Not now

Work beyond a single creator's path is not yet placed in a version: hosted workspaces, the sandbox, Hivemind, agent learning, contribution discovery, the portable workspace and editors beyond video. Open owner decisions for version 0.1: whether rented machines are fully supported or labelled experimental, and whether Pinokio is a supported install route. Releases after Release 14 are provisional: their scope is set from actual usage when each brief is taken up.

Past releases are documented in the [existing release log](plans/releases.md) and actual receipts. Plan 31 migrates that history into canonical release records only where it can be grounded in publication evidence; Release 11's publication race is recorded in the [ledger](docs/ledger/2026-11-09-two-projects-published-release-11.md).

## Decisions

- **2026-11-15:** This page is to be populated from the release briefs and plans (Hannah): each release brief lists its plans and its issues, and the page pulls each release's and each plan's sentence under a hand-written sentence and paragraph for each version. There is one strategy document for each major version, opening with the aim in one line and a few paragraphs. [Plan 58](plans/58-strategy-from-releases/plan.md) does this before [Plan 31](plans/31-releases-from-astrid-dev/plan.md) and corrects the documents that describe this page.
- **2026-11-15:** This page is a structured map (Hannah): a major version with one sentence, holding the minor versions that lead to it, each with one sentence and its plans, with gaps kept open all the way to 1.0, and CI enforcing the structure. The sentence for version 1.0 was proposed by the advisor and is hers to change.
- **2026-11-15:** Hannah set the destination: version 0.1 "should be focused on hardening, updates, stability and speed", and version 0.2 "should be open" for now; fixes and plans are added "on the fly based on actual usage and user reports". Version 0.1 is Releases 14 (local speed; "RunPod is unimportant" for it), 15 (stability), 16 (install and update everywhere) and 17 (hardening only, carrying the version). Generation complete, workflow set-up, finishing a video and rented-machine speed are candidates for 0.2, not sequenced. An earlier proposal the same day placed them before 0.1 as Releases 16 and 18; this replaces it.
- **2026-11-12:** [Plan 51](plans/51-astrid-dev-clean-up/plan.md) (the astrid-dev clean-up) is done. It was never assigned to a release, so [Release 12](releases/12.md) and [Release 13](releases/13.md) and their summaries on this page are unchanged. It left the release skill and the GPU-validation skill alone. Its assessment and route in [CA-005](vision/gaps/CA-005-parallel-contribution.md) are updated; that gap stays open.
- **2026-11-11:** Hannah split the combined release. Release 12 is fixes-only and includes the onboarding-tour commits on App `main`; generation (Plans 32, 40, 20 and 34) is [Release 13](releases/13.md), built on published Release 12. This reverses the 10 Nov fold-in below.
- **2026-11-10:** Hannah folded the generation work (Plans 32, 40, 20 P1.5 and staged work, and Plan 34's proof) into Release 12 instead of a Release 13. The draft `releases/13.md` is folded into [Release 12](releases/12.md); the next release brief starts fresh after publish.
- **2026-11-10:** Strategy is release-led: each release file starts as a living strategy brief, with a highlight, intent, approach and linked plans. The overview here is mainly a summary of those release files.
- **2026-11-10:** An unpinned draft can change on `main` without publishing; publication requires separate, explicit finalization and owner-approved, validated pins (Plan 31).
- **2026-11-08:** Installed-release publication remains separately authorized. Plan 31 follows Plan 29; generation work continues on its own track.

## Keeping this page current

**Words and decisions.** Keep the major aim, each version's sentence and paragraph, the candidates and the decisions here. Change them when the owner's direction changes. The [catalog](plans/index.md) carries plan status and ownership; [vision gaps](vision/README.md) retain their own assessments and routes.

**Generated parts.** Edit a release's kind, state, highlight and included plans in its release brief, then run `python3 scripts/astrid_dev.py sync` to see the result here. Do not edit between the strategy markers. On `main`, the refresh job updates these parts after a source change, so they may be stale for one CI run. The [Release skill](skills/astrid-dev-release/SKILL.md) covers pulling and freezing issue lists; the page shows counts only for frozen lists.

**The next major version.** When 1.0 ships, preserve this page as `strategy-1.0.md` beside it and begin a new `strategy.md`. Publication remains a separately authorized release step.
