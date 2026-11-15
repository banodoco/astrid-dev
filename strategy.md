# Strategy

Astrid's execution strategy is a sequence of **releases**, each a coherent step toward our [vision](vision/README.md). Each release document holds the living rationale, intended outcome, approach and included plans; this page is their short, ordered map.

Each plan's own `plan.md` holds its status, owner and estimate, `plans/priority.md` holds the order, and the [plan catalog](plans/index.md) is generated from them. [Vision gaps](vision/README.md) and their routes still define what needs to improve and how success will be assessed. A plan may be worked on before it is assigned to a release; an unassigned plan is not a release commitment.

**Last reviewed:** 2026-11-15, when Hannah set version 0.1's focus (hardening, updates, stability and speed) and left version 0.2 open. Future assignments are provisional until explicitly finalized.

## Focus now

[Release 12](releases/12.md) (updates and the onboarding tour) is published. [Release 13](releases/13.md) (one generation path, on your own ComfyUI or a rented GPU) is being published on 15 November 2026; its brief stays marked draft until its record is finalised. Next: make local generation fast in [Release 14](releases/14.md) ([Plan 55](plans/55-local-speed/plan.md)).

The destination is a stable **version 0.1**, focused on hardening, updates, stability and speed: what Astrid already does, made fast and dependable on Windows, macOS and Linux. It is reached in four releases: local speed (14), stability (15), install and update everywhere (16), and a hardening-only release that carries the version number ([Release 17](releases/17.md)). **Version 0.2 is open**: its candidates are listed [below](#version-02-open) and are not sequenced.

Each release has one theme, plus a standing lane for fixes and small plans that come from actual usage and user reports.

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

### Version 0.2: open

Not sequenced and not numbered; a release brief is written when one is taken up. Candidates so far, from Release 13's deferred list, the owner's requests and the plan catalog:

- **Set up any workflow in one step:** its models and node packs, with a recorded answer for what cannot be found ([Plan 56](plans/56-workflow-setup/plan.md), decisions made 15 November 2026; [issue 665](https://github.com/banodoco/astrid-dev/issues/665) for identifying unknown models). Its small corrections can ship earlier in the standing lane.
- **Generation complete:** every bundled workflow ready, video models beyond the default, the rest of onboarding ([Plan 20](plans/20-zero-to-first-image/plan.md), [Plan 32](plans/32-generation-placement-targets/plan.md)); frames at positions on the default video workflow (first frame, last frame or any position, one feature).
- **Finish a video:** generate onto the timeline, agent edits that never overwrite the creator's, export ([Plan 37](plans/37-generate-time-destination/plan.md), [Plan 04](plans/04-concurrent-edits/plan.md), [Plan 18](plans/18-timeline-editing/plan.md), [Plan 27](plans/27-video-render-options/plan.md)). Three of these are goals without tasks; walk one real video end to end before scoping.
- **Rented machines:** speed and the slow first job ([Plan 54](plans/54-warm-latency/plan.md)).

## Not now

Work beyond a single creator's path is after version 0.2 is settled: hosted workspaces, the sandbox, Hivemind, agent learning, contribution discovery, the portable workspace and editors beyond video. Open owner decisions for version 0.1: whether rented machines are fully supported or labelled experimental, and whether Pinokio is a supported install route. Rows after Release 14 are provisional: their scope is set from actual usage when each brief is taken up.

Past releases are documented in the [existing release log](plans/releases.md) and actual receipts. Plan 31 migrates that history into canonical release records only where it can be grounded in publication evidence; Release 11's publication race is recorded in the [ledger](docs/ledger/2026-11-09-two-projects-published-release-11.md).

## Decisions

- **2026-11-15:** Hannah set the destination: version 0.1 "should be focused on hardening, updates, stability and speed", and version 0.2 "should be open" for now; fixes and plans are added "on the fly based on actual usage and user reports". Version 0.1 is Releases 14 (local speed; "RunPod is unimportant" for it), 15 (stability), 16 (install and update everywhere) and 17 (hardening only, carrying the version). Generation complete, workflow set-up, finishing a video and rented-machine speed are candidates for 0.2, not sequenced. An earlier proposal the same day placed them before 0.1 as Releases 16 and 18; this replaces it.
- **2026-11-12:** [Plan 51](plans/51-astrid-dev-clean-up/plan.md) (the astrid-dev clean-up) is done. It was never assigned to a release, so [Release 12](releases/12.md) and [Release 13](releases/13.md) and their rows above are unchanged. It left the release skill and the GPU-validation skill alone. Its assessment and route in [CA-005](vision/gaps/CA-005-parallel-contribution.md) are updated; that gap stays open.
- **2026-11-11:** Hannah split the combined release. Release 12 is fixes-only and includes the onboarding-tour commits on App `main`; generation (Plans 32, 40, 20 and 34) is [Release 13](releases/13.md), built on published Release 12. This reverses the 10 Nov fold-in below.
- **2026-11-10:** Hannah folded the generation work (Plans 32, 40, 20 P1.5 and staged work, and Plan 34's proof) into Release 12 instead of a Release 13. The draft `releases/13.md` is folded into [Release 12](releases/12.md); the next release brief starts fresh after publish.
- **2026-11-10:** Strategy is release-led: each release file starts as a living strategy brief, with a highlight, intent, approach and linked plans. The overview here is mainly a summary of those release files.
- **2026-11-10:** An unpinned draft can change on `main` without publishing; publication requires separate, explicit finalization and owner-approved, validated pins (Plan 31).
- **2026-11-08:** Installed-release publication remains separately authorized. Plan 31 follows Plan 29; generation work continues on its own track.

## Keeping this page current

When a draft release is added or changes its headline or included plans, update the matching sequence row in the same PR. When a release is published, keep its final document immutable and retain its summary in release history. CI checks the draft's basic structure and consistency with the overview; the Plan 31 release gate separately protects publication. Keep this page short: deeper reasoning belongs in the release document, gap route or plan.
