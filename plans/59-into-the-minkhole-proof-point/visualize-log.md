# timelines visualize: field log

`timelines visualize` is the main way agents look at this film without rendering it, and it is still unproven. Every time we use it on this project, record what we wanted to see, the command that worked, and what was missing or confusing. Each gap becomes a small fix (astrid-dev#798) or a new selector or preset. Newest entries go at the top.

## What we need to see for this film (target views)

| Need | Today | Wanted |
|---|---|---|
| Whole cut, one tile per cut | `--preset overview` works | Plain header (name, version, length, cuts); readable legend; one numbering scheme; plan labels on the tiles (`--shot-plans` prints text only) |
| One frame at full size | `--at T --size 1920x1080` works | Page path as the last line printed; next-step commands copyable through the launcher |
| Detail of a region (sunglasses, mouth) at source resolution | Missing (only `timelines check --zoom/--region`) | `--region X,Y,W,H` / `--zoom <layer>` on visualize, and named regions from a shot plan's masks |
| A mask over the source frames | Missing | A mask outline layer over frames of the shot, from the plan's `inputs.masks` |
| A generated take, before placing it | Unknown (`--asset`?) | View a take's frames next to the source at the same moments (before/after) |
| Words under the picture | Tiles read clip words only; "—" or "no words stored" | Stored transcripts projected into the snapshot (branch `p59/transcribe-standard`, B2) |
| Silence and voice where expected | Red "dead air" boxes everywhere, including intended silence | Flag only where a line is expected (from the plan or the script) |
| Plan status across the film | `--shot-plans` text rows | The same on the tiles: methods, status, takes |

## Entries

### 17 November, late: judging the old man re-takes (install-4)
- `--compare-media <O1> --against cut --cut 7`: the page rendered, but the difference map is dominated by framing. The source cut is the letterboxed still and the take is the bar-free reference, so every pixel "differs" (12.4/255) and the question that mattered, whether the mouth stays closed, can't be answered from it. Wanted: compare after fitting the take to the source's picture area (ignore the bars), or a take-only mouth/motion view (`--layer lipsync` on a media id, not only on a cut).
- `--compare-media <O2> --against cut --cut 9`: "could not read a frame at 2.50 s of generated_00001-audio.mp4". The take is 2.50 s and the cut 2.54 s, so the sampler asked for a frame at the take's exact end. Wanted: clamp samples to the take's last frame and say the take is 0.04 s shorter than the cut.

### 17 November, evening: after batch 1 (dev loop, branch p59/visualize-readable)
- Overview: much better. Plain header (name, length, cuts in shots, short revision); readable legend; no false dead-air boxes; one numbering ("cut 5 5.00-8.00 s"); shot names wrap; words line says "voice here; no words stored (timelines transcripts run)" or "no voice under this cut"; plan labels on the tiles.
- `--at 14 --region 300,0,1200,450`: source-resolution crop of the sunglasses with a locator. Rough edge: the region was clipped to the 1280 canvas without saying so.
- Not intuitive yet for judging a mask: `--region` works only with `--at` (no region over time); `--cut 8 --layer heat,diff` draws a per-frame pixel-change bar chart and one text line ("pixels change inside x 18%-80%, y 0-100%"), not where the movement is on the picture; the `heat` layer drew nothing. Wanted (batch 2, in progress): region strips over a cut or range, a mask overlay with inside/outside motion, a heat overlay on the frame, and a take shown against its source.
- Useful existing layers found: `lipsync` (mouth state against words), `onion`, `strip`, `diff`.

### 17 November: first real use on the approved cut (install-2)
- `--preset overview` drew 19 cuts in 9 shots and confirmed the shot map: Morpheus in cuts 5 and 8, the old man stills in cuts 7 and 9, the lens stills in 13-15.
- Confusing: an internal ID and "UNCERTIFIED preview (claimed revision …)" as the header; a tiny legend; red dead-air boxes on intended silence; "ch02" next to "01 Two options"; "—" under every tile with no explanation.
- `--at 14 --size 1920x1080` confirmed Neo is in both lenses with the blue pill in the right one. Missing: a crop of the lenses at source resolution.
- The suggested next commands print an internal path (`…/omp_agent.py timelines visualize`) and a 70-character revision ID, so they can't be copied.
- Finding the page meant searching hash-named folders, because the page path was not the last line printed.
- `timelines visualize --at 10.5` / `--at 17.5` on the shared Runtime queued behind another task and returned no frames. The command should say it is waiting, or say why it returned nothing.
- Measuring the baked-in letterbox on the old man stills (121/122 px) needed the media's own pixels; visualize had no way to show or measure bars.
