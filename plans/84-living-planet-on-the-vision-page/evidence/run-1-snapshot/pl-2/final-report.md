# PL-2 proof checkpoint

Candidate: `22a308ef2cfc99434a624e94c415c0a7a8ef8ef8` (`plan-84/pl-2`, pushed). The mobile spacer repair is in `d52713a8ca6d8bc28622e8a7b850ca784f984c56`; the latest CSS checkpoint adds the copy tint/panel contrast refinements. Product changes are limited to `PublicAstridVision.css` and `VisionMobileLayout.css` after the spacer checkpoint. No tests were changed.

## Build and static checks

- `NODE_OPTIONS=--max-old-space-size=4096 npm run build:hosted` passed at the final source; build output is `build-d527-css-final.log`. Existing chunk-size, PostCSS, Browserslist and Tailwind class warnings remain; the build reports no remote font or script hosts.
- `git diff --check` passed before the final CSS commit.

## Phone spacer proof

Fixed date `2026-06-21T12:00:00Z`, pinned feed SHA `c233da0fcf0136204d0198c58186757dd5a7f4b29d2137cfd1df1a5f36e63625`, DPR 2, `isMobile:false`, `hasTouch:true`, no preview/query override. The visible-viewport draw gate passed.

- At 390×844, baseline Pillars card top was y=894.5 and unrevealed (`data-shown=false`, no `data-play`). Candidate `d52713a` card top is y=601.0, revealed and playing (`data-shown=true`, `data-play=true`). Live canvas backing is 390×776, has draw calls, and remains visible behind the hero/Foundation surface. Both pages have `scrollWidth=clientWidth=390`.
- At 844×390, canvas draws in both builds; the first Pillars card is below the viewport in both. Candidate portrait/landscape screenshots and per-build metrics are in `spacer-phone/`.
- Root visually accepted the portrait flow repair. Landscape composition is assigned to PL-3 camera/framing work.

## Contrast stress proof

`contrast-glyph.cjs` captured at 1440×900 / DPR 2 with a live WebGL draw gate. It inserted a test-only full-story black or white plane after the planet layer and before the copy/panel, left product tint/card CSS unchanged, and hid measured text paint only in the sampling screenshots. Each non-whitespace character was measured with its own Range rectangle. Chromium converted inherited CSS text colors to RGBA; the analyzer includes text alpha and ancestor opacity when computing contrast. Every declared selector resolved; each screenshot contains 198 hero, 352 Pillars and 307 Principles glyphs, with zero samples outside the viewport. Large text uses a 3:1 threshold only at ≥24px regular or ≥18.66px bold; other text uses 4.5:1.

All four palette/underlay cases pass. Minimum body contrast is 4.721:1 (light palette, black underlay, Principles card 2). Minimum large-heading contrast is 6.153:1 (light palette, black underlay, Principles heading). Detailed target minima, worst glyph coordinates, foreground/background pixels and screenshots are in `contrast-glyph-0e290681721e0272a73dbc59496c3676c2a49beb/results.json`, `contrast-glyph-0e290681721e0272a73dbc59496c3676c2a49beb/summary.json`, and `contrast-glyph-0e290681721e0272a73dbc59496c3676c2a49beb/*.png`. Earlier failing iterations are retained in `contrast-glyph-before-css/` and `contrast-glyph-60-86/`.

## Live image review

Five contract-pinned hero views and the two requested panel views are in `live-review/`:

- `phone-portrait-hero.png`, `phone-landscape-hero.png`, `tablet-portrait-hero.png`, `laptop-hero.png`, `wide-hero.png`
- `phone-portrait-panel.png`, `laptop-panel.png`

The capture metadata, including candidate SHA, date, feed SHA, browser, viewport settings, draw counts, panel anchor and document widths, is in `live-review/summary.json`. This final image set corresponds to candidate `22a308e`.

## Existing test status

The independent unchanged-spec run at immutable `88ac863` reported the Vision entry overflow restoration assertion and missing title assertion. Root is handling the separate `Vision.tsx` entry repair; this worktree did not modify assertions or rerun those specs against the new CSS candidate.

## PL-2 hero backing refinement (visual review pending)

Checkpoint `0e290681721e0272a73dbc59496c3676c2a49beb` replaces the broad oval with a blurred rectangular backing inset 42px vertically and 56px horizontally, with 28px blur. It preserves the shared Foundations 86% tint and phone spacer fix. Build passed in `build-soft-rect.log`; `git diff --check` passed. The run is committed/pushed, with root visual ruling pending before recapturing the full five-size set.

Laptop and 844×390 landscape live screenshots are `soft-rect-review/laptop-hero.png` and `soft-rect-review/landscape-hero.png`. Their settings and computed CSS are in `soft-rect-review/summary.json`. The full glyph stress method was rerun at the same 1440×900 contract. All targets pass; minimum body ratios by case are light-black 4.557, light-white 5.363, dark-black 6.765, dark-white 6.650. The image and per-target results are in `contrast-glyph-0e290681721e0272a73dbc59496c3676c2a49beb/`; the prior oval audit is retained in `contrast-glyph-oval-commit-22a308e/`.


Root accepted the soft rectangular feather at `0e290681721e0272a73dbc59496c3676c2a49beb`. The final five-size hero set is cataloged in `hero-final-0e29068/manifest.json`: phone portrait, phone landscape, tablet portrait, laptop, and wide. The two judged captures were preserved without recapture; the remaining three use the pinned contract. Laptop/phone panel screenshots are unchanged by this hero-only revision and are referenced in the manifest. PL-3 owns the remaining landscape camera composition.
