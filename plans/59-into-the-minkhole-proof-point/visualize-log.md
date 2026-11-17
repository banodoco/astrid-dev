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

### 17 November: first real use on the approved cut (install-2)
- `--preset overview` drew 19 cuts in 9 shots and confirmed the shot map: Morpheus in cuts 5 and 8, the old man stills in cuts 7 and 9, the lens stills in 13-15.
- Confusing: an internal ID and "UNCERTIFIED preview (claimed revision …)" as the header; a tiny legend; red dead-air boxes on intended silence; "ch02" next to "01 Two options"; "—" under every tile with no explanation.
- `--at 14 --size 1920x1080` confirmed Neo is in both lenses with the blue pill in the right one. Missing: a crop of the lenses at source resolution.
- The suggested next commands print an internal path (`…/omp_agent.py timelines visualize`) and a 70-character revision ID, so they can't be copied.
- Finding the page meant searching hash-named folders, because the page path was not the last line printed.
- `timelines visualize --at 10.5` / `--at 17.5` on the shared Runtime queued behind another task and returned no frames. The command should say it is waiting, or say why it returned nothing.
- Measuring the baked-in letterbox on the old man stills (121/122 px) needed the media's own pixels; visualize had no way to show or measure bars.
