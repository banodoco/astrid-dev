# 21: Astrid website, homepage journey

Status and owner are in the [root queue](../../README.md). Status: `queued`. Owner: `Unassigned`.

## Summary

Below the Astrid homepage hero, a scroll journey re-says the hero's six callout notes (three about the App, three about the Agent) in new ways, using the objects the hero already shows: the four editor panels, the conversation and the mink. Three sections and a finale make one story. Section 2 shows an agent extending the creative suite, section 3 shows an agent setting up open models, and section 4 shows a creative partner editing beside you with tools you can build. The finale is a vision. Every section keeps living while you rest on it, and each transition is the same live objects moving into a new arrangement. The sky runs from the visitor's own time of day toward its opposite peak as you scroll.

Everything shown is a placeholder for now, and the plan says so on screen.

## Journey outline

| Section | Re-explains hero notes | Headline | The "agent did this" device |
|---|---|---|---|
| §2 | 4, 5 | A creative suite your agent can extend. | `built by your agent` stamps on a 3D view and a beat-sync tool; `installed by your agent` on a new model. The layer each example extends lights up. |
| §3 | 2, 3 | Open models, without the setup pain. | `set up by your agent` under each readout title. |
| §4 | 1, 5 | A creative partner with deep tools. | Tool-call chips under Astrid's replies: `arrange · 3 clips`, `beat-sync · 3 downbeats`, `retime · crossfade`. |
| §5, finale | 6 | The Vision. | None. The sky reaches its opposite peak, the mink looks up, and there is one link, to Vision. |

## Mockups

These are composition guides, not pixel specs. Where they differ from the plan, the plan wins.

<table>
<tr>
<th>Night sky</th>
<th>Day sky</th>
</tr>
<tr>
<td><a href="mockups/full-page-night.jpg"><img src="mockups/full-page-night.jpg" alt="Full-page mockup of the homepage journey, night sky" width="360"></a></td>
<td><a href="mockups/full-page-day.jpg"><img src="mockups/full-page-day.jpg" alt="Full-page mockup of the homepage journey, day sky" width="360"></a></td>
</tr>
</table>

Per-section frames are in [`mockups/night/`](mockups/night/) and [`mockups/day/`](mockups/day/).

## Key decisions

- **Live panels, not stills.** The exploded stack is the live editor panels in a third pose. Moving from §2 to §3 and from §3 to §4 is a pose change of the same objects.
- **Scroll is never hijacked.** Scroll decides where the visitor is. Time plays each moment. Arriving in a section plays its demo once, then its ambient cycle keeps it alive. Only the sky follows the scroll.
- **The sky follows the visitor.** It runs 12 hours from the visitor's local time to the opposite peak: night visitors end at solar noon, day visitors at solar midnight. The moon shows its real phase.
- **Placeholders claim nothing real.** All music, stills, clips and mink strips are placeholders, labelled as examples. No GPU specs, timings, usage counts or visitor hardware detection. Real assets are a separate decision.
- **No flags, no hidden modes.** Work lives on one branch, `feat/home-journey`. Nothing reaches `main`, which deploys production, until the owner says go.
- **The preview is a Claude Artifact** of the branch's public entry, republished only by the coordinator. Scripted publishes never save, draft or write history.
- **Phones are designed in v1,** with a stage sized to about 45% of the viewport height and explicit reduced-motion paths.
- **Craft is fixed before engineering.** Copy, beat timings and motion tokens are set once (task T0) and engineering reads them from one tokens file.

## Scope

- **Included:** the journey below the hero (§2 to §5 and the finale), its phone and reduced-motion behaviour, placeholder assets, the capture harness, the preview, and the end-to-end and performance checks.
- **Deferred:** real media (PLAN part 6.2); the Art link (left out on purpose); the rest of the Astrid website, which this plan does not cover.

## Starting code

| Field | Record |
|---|---|
| Product repository | [banodoco/astrid-app](https://github.com/banodoco/astrid-app), route `/home` (`src/pages/Home/`) |
| Starting branch and commit | The plan is pinned to `main` at `17e46de99` (20 Oct 2026). `main` has moved since. Step 0 re-checks every pointer against the new branch point. |
| Existing work to preserve | None recorded. The journey adds to the public homepage; the hero stays as it is. |
| Predecessor output | `none` |
| Working candidate branch | `feat/home-journey`, created from `origin/main` at Step 0. Each task works on `hj/<id>`. |
| Intended merge destination | `main`, only at R4 after the owner's go. Merging deploys production. |

## Tasks

The plan has 34 tasks: 8 XHARD (route `X`), 13 NORMAL (route `N`), 7 TASTE-HIGH (Opus taste passes), 2 TASTE-LOW (Sonnet taste passes) and 4 ASSET placeholders. Routes `N` and `X` take their models from the [routing table](../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings). They run in phases, from Step 0 through the review rounds R1 to R4. The full table is in [PLAN.md](PLAN.md) part 7, and task progress is kept there, not here.

## Completion

The goal is met when every task in PLAN part 7 is merged into `feat/home-journey`, the journey end-to-end spec and the bundle budget are green, R1 (performance) and R2 (taste) have run and R3 has fixed or dropped their findings, and the owner has seen the preview on desktop and phone. The owner then decides two things: whether the placeholder media may ship, and whether `feat/home-journey` may merge to `main`. Nothing merges before that. Open: the real assets in PLAN part 6.2.

## Files

- [`PLAN.md`](PLAN.md): the build plan (v3). The executor brief and Step 0 come first, then the architecture, 34 tasks, the review rounds and the craft direction.
- [`START-HERE.md`](START-HERE.md): the hand-off for whoever builds it: repo, tools, model tiers and the rules that matter most.
- [`mockups/`](mockups/): the full-page JPGs, and `night/` and `day/` frames for each section.
- [`evidence/`](evidence/): the code read (`DEEP-PASS-RESULT.md`) and the two Opus reviews (`OPUS-REVIEW-RESULT.md`, `OPUS-CRAFT-RESULT.md`) that the plan was built from.

## How to start

1. Read [START-HERE.md](START-HERE.md).
2. Read the executor brief and Step 0 in [PLAN.md](PLAN.md). Nothing is built until the owner says go.

`docs/plans/home-journey/` in PLAN.md is where this folder is committed inside astrid-app (Step 0.3). It is not a path in this repository.
