# Live proof evidence, final candidate (23 November 2026)

[Live proof](../../live-proof.md#final-proof-on-the-landing-candidate-23-november-2026) · [Tasks](../../tasks.md) · [Plan](../../plan.md)

Copies of the small-project run on Agent `64cecdae` (Runtime `737843e9`). Copied from `/root/codex/le4/run9/`; the originals are machine-local and were not moved.

| File | Meaning |
| --- | --- |
| `report-small.md` | The run report. Step 4 is marked FAIL in the report: the live reads refused with `head_busy`, so the live outcome checks and the negatives did not run. The offline outcome checks passed. One line was removed from the copy: the window bullet (line 8 of the original) named the model family in a quoted permission message and in a path. The denial itself is stated in the live proof record. No other model name appears. |
| `commit-small1-receipt.json` | The accepted mixed commit receipt, `txn-8e764a2d932340299d0b568793cbdf8d`. |
| `outcome-small1.json` | Offline outcome checks, 14 of 14 pass, computed from the accepted response and the one passing post-commit history read. |
| `refs-small1.json` | The admitted refs for `le4-gold` and `le4-cyan`, pack `project_4944f3baaa40481ba360`. |
| `rows-after-commit.json` | History rows after the commit; the one new row equals the receipt id. |
| `throttle-host.log` | Repository throttle test on this head: 136 titles 20.675 ms, 0 discoveries, one stat per root. |
| `before-*.png` | Preview-only crops of the stills before the commit (1.5, 3.5, 5.5, 7.5 s). |
| `after-*.png` | Preview-only crops of the stills after the commit (1.5, 3.5, 5.5, 7.5, 10.5 s). Not a visual confirmation of page continuity. |

## Brightness comparison (7.5 s)

The control text card is black at 7.5 s both before and after the commit: `before-7.5.png` mean 33.6 and `after-7.5.png` mean 33.6 (greyscale, 0 to 255).

## Visual notes

- Both black stills (control at 7.5 s and NEW TITLE 1 at 10.5 s) are 0.5 s into their clips. The text card's own entrance is 18 frames (0.6 s at 30 fps) in the installed timeline-composition package (`chunk-BEYNBITW.js` line 14; the type-on reveal in `chunk-VHNHAQUG.js` lines 175-182). The control was black before the commit too, so the commit did not cause it. The earlier proof showed NEW TITLE 1 fully visible at 11.0 s.
- The extra stills at 8.0, 8.5, 11.0 and 11.4 s were not taken. The page controller has a fixed capture list, and a new page would break the one-page rule. They are part of the release-freeze item.
- The cyan slot card does not draw its label in this install. The installed motion pack file `astrid_motion/rendering/elements/effects/am-footage/component.tsx` draws the fixed `SLOT ... TO FILM` text at line 217 inside the `if (!url) {` branch (line 203) and does not read `label` there; `label` is drawn only in the media branches. The file's mtime is 14:04:23, before the fork (14:58) and the commit (15:00:08), and its sha256 is identical in the three isolated installs. The earlier proof's fork came from a different source (`if (placeholder)` with `p.label ? label : ...`), which is why its card showed REHEARSAL 2. The label parameter is stored correctly in the commit.
