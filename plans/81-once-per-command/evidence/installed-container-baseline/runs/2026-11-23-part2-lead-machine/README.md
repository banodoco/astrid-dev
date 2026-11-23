# Part 2 three-arm installed run, Lead machine, 23 November 2026

Attempt 2 of the run block in this folder. The manager ran its local copy of the block (sha256 `68d8f052143aa758a24c4009d86c10681f3a39f188f634c0ec746159db0bf80a`) with the attempt-2 set-up below; `RUN-BLOCK.md` here is the later amended version (#1613, #1615) that writes the same fixes into the block. Attempt 1 stopped at the first install because a source clone had no local ref for its pinned commit; attempt 2 created a local branch for each commit, allowed fetch by id and proved each fetch before installing (`receipts/source-fetch-proof.txt`).

Run 08:18:08Z to 08:35:16Z on a shared 4-vCPU CPU container with a stand-in ComfyUI, `--no-wait` (timed to "task queued"), load gate 1.0, five samples per arm and group after one warm-up.

| Arm | Agent | Runtime | VibeComfy |
| --- | --- | --- | --- |
| before | 8807f820 | 3c28211f | 48b5fa9e |
| vc48 (Part 1 landed) | bd94a6e1 | 53a035ba | 48b5fa9e |
| after (Part 1 + Part 2) | bd94a6e1 + local trial pin (`receipts/trial-identity.txt`) | 53a035ba | 675f5dc2 |

## Result

Every command exited 0. The driver exited 5 only because its own qualification (after/before median at most 0.5) failed.

| Group | before | vc48 | after | Part 2 saving (vc48 - after) |
| --- | ---: | ---: | ---: | ---: |
| same | 16.632 s | 12.250 s | 12.343 s | -0.093 s |
| changed | 16.406 s | 12.215 s | 12.331 s | -0.116 s |
| timeline | 1.500 s | 1.426 s | 1.348 s | within noise |

Part 1 is the whole saving (about 26%). Part 2's VibeComfy memo saves nothing on an installed command: workflow emission stays about 6.1 to 6.2 s exclusive per command in both vc48 and after. Part 2 was in any case stopped by the blind review's class (i) entry (`../../../part2-memo-review/`); this number goes to Plan 82 (#1618) as its baseline, and the first question there is why emission costs 6 s installed when the memo does not reach it.

## Receipts

`receipts/` holds everything the run produced except `trial.bundle` (46 MB, the trial Agent pin commit as a git bundle), which stays on the Lead machine at `/root/codex/p81box/part2-attempt2/receipts/trial.bundle` and is listed in `receipts/SHA256SUMS`. sha256 of `receipts/SHA256SUMS`: `265ccf7ae9073a065304d59089a141b300c2fddf1d21cba39ccbc477abbb432e`. Per-command walls and loads: `receipts/run/summary-ab.json`; console: `receipts/step6-console.txt`; raw stdout and stderr per command: `receipts/run/raw/`.
