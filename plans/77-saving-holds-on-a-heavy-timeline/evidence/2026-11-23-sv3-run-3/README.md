# SV-3 measurement, third run: stopped by the 16 GiB disk guard in repetition 1, 23 November 2026

Approved for exactly: package head `53bbbda5b297ab82e640ed7cc885c77a77b42339`, `package.sha256` digest `6eaaa32f1b894f9808ca1b481802f6f083c8e10c20a6390941b101591c516138`, candidate Runtime `f2da02e1dcf02439ee149f1412310c72aa4bf0bb`. Ran once from 15:29Z. **No measurement happened.** Not retried.

## What passed

- Setup: pristine copy and audit, the work copy, the rewritten service declaration (`rep-1/services.json`, installed-layout paths swapped to the copy), the candidate Runtime start (`rep-1/up.json`, 2.5 min), the preview health check and the browser start.
- **The supervised pack host ran on the copy:** `rep-1/pack-host.json` says `pack host running`: the stack's pack-host log grew by 2842 bytes with no `exiting after failure` line (run 1 showed three crash loops). The claim poll itself is not logged (`claim_lines` 0).
- Cleanup: idle-safe `down` verified on the first attempt (`rep-1/down.1.json`), preview ports closed (`rep-1/preview-after.json`), no leftover Chrome, boundaries unchanged (`boundary.json`: signed backup, owner, locks and the original data listing unchanged).

## What stopped it

The disk guard. Free space was 18.57 GiB at the start, 17.03 GiB after the two copies, 16.84 GiB when the browser phase began and 16.78 GiB at 15:33:31, below the 16 GiB (16777216 KiB) stop (`disk-stop.txt`, `free-kib.tsv`). The guard sent TERM to the script, which stopped the browser before any drag finished, so there is no `browser-sv3-measure.json`. The disposable browser profile directory was left non-empty (`rmdir` failed) and was removed by hand. After the stop, reproducible scratch was reclaimed so the next run starts with about 20 GiB free (`sv3-reclamation.tsv`).
