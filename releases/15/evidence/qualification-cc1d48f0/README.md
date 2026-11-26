# Release 15 qualification evidence — candidate `cc1d48f0`

Recorded by the Release 15 Qualifier. This folder records measurements; it does not decide acceptance. Acceptance, the ledger and the owner's go belong to the Lead and the owner.

## Candidate under test

| Part | SHA |
|---|---|
| App (CI by-id head) | `cc1d48f0` (Tests 45668919908, Lanes 45668919952, E2E 45668919978) |
| App (installed stack measured for renders and saves) | `7676df48f4104fb8ebe2b19de64dea25b9ec3dc7` |
| Agent | `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5` (CI 45658943056, Lanes 45658943220) |
| Runtime | `686ca695469bda48cd40a70824c4ccef2a137284` |
| VibeComfy | `55c3948212d23cf037fae8a4c6faad77d33e7279` (manifest pin; installation not verified) |
| Motion pack | `2379ab54aca522019ff4f869cfdf9375bdb56dfc`, digest `75234c10…1029` — installed pin and computed digest matched |

The two App SHAs are as recorded in the respective reports; this folder does not claim they are the same tree.

## Tier 1 row 1 — whole-run by-id comparison against Release 14

See `by-id/`. Counting: distinct ids with FAILED or ERROR, SUBFAILED rows excluded, `darwin:` prefix kept but ignored when matching, E2E from numbered failure lines (not `::error` annotations).

- App Vitest: 1 failing id (`amSprite.phase … chapter cut`, known #1931); no new ids. Lanes: same two ids as R14/previous head. E2E: 85 failed results / 80 distinct ids, identical to R14.
- Agent CI: 6 ids absent from R14, all mapped to known issues (#1920, #1941, #1928, #1938) and none first appeared at `dc45d97c`.
- Agent Lanes: 37 ids absent from R14, all first appeared on earlier heads; 35 are not in R14's Lanes run at all and are tracked in #2002. 15 are `compiled element descriptor is invalid` and their cause is not established.

## Installed journeys on the candidate

- Update ×2 and heavy saves ×2: pass. Saved appeared 30.3 s and 32.0 s after mouse-up; no unconfirmed-save banner; 616 clips and Runtime digest identical after reload (`saves/`).
- Renders (`renders/`):
  - One second: pass, 1920×1080, 30 fps, 30 frames.
  - Standard 616 clips: pass — decode, 1920×1080, 30 fps, audio, known colours; 233.0 s, 6,990 frames. Peak RSS 7.9 GB is a lower bound (sampling gap).
  - Film-shaped: passes against the project's declared 1280×720 at 30 fps (195.967 s, 5,879 frames, audio). The 1920×1080 check in `film-shaped-verify-1920x1080-expectation.json` fails because of the Qualifier's wrong expectation, not the product. Peak RSS 5.26 GB.

## Observations not proven harmful (open)

1. In the film-shaped render, the 3-second frame is visibly dimmer/different in colour than the editor preview at the same source frame (0 s and 1 s align). Cause undetermined; see `renders/film-editor-comparison-report.txt` and the compare PNGs. Part of the render overlapped the editor comparisons, so added load is unquantified.
2. Heavy renders reach ≥7.9 GB RSS.
3. The 15 `compiled element descriptor is invalid` Agent integration ids (#2002).

## Files

- `by-id/` — reports, id lists, counts, per-id issue labels.
- `renders/` — verification JSON per render, editor comparison report and images.
- `saves/` — page-mark and CPU/RSS evidence for the two heavy-save attempts (`attempt1` and `clean-pair`).
- `terra-final-report-draft.md` — raw run report from the measuring Codex session.

Not covered here: owner's go, Tier 2 (App Direct Journey result is reported separately by the Qualifier).
