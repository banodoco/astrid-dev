# PB-7 installed timing result: run 1

**Result:** the five-sample median saving was **1.3253 seconds**, below the 1.5-second acceptance gate by **0.1747 seconds**. All measured commands succeeded and all measured start loads were below 1.0. Full raw output and timing rows are retained. No second sample run has been started.

## Comparison tuple

- A / `before`: local Agent trial `6ab118b7f05d040e835c70aba04c5209e97108b4`, from frozen Plan 78 parent `64cecdae9f679537f4a6dc82e5102e53b6943ef7`, with the local generated VibeComfy pin `c0e910caab9734a551fb2c1a455fff72c3a1b1cb`.
- B / `after`: branch tip `f20175032283521d5cac3540d2ebbf4b70363770` on `p81/pb7b-discover-once`, followed by local generated pin trial `6106240805d64b2454f2a2b20a2ad4305bcedc1b`. This includes the branch range commits `0d71e509`, `f64da201`, and `f2017503` above the A parent.
- Both arms used Runtime `737843e9cb92c565c266452dde540832ee2c745b`, VibeComfy `c0e910caab9734a551fb2c1a455fff72c3a1b1cb`, lifecycle `9f88ef7640bc664f697112d966ecefa123d44340`, and the same `omp` npm pin.
- The generator pin diffs are byte-identical (SHA-256 `d20b1977bc5be895673c4dd163649bbb35183fd0a3e409cd50e0e659f209a393`). Requested and selected manifests are retained here.

## Samples

Measured wall seconds; start load in parentheses. Arms ran in alternating A then B order after one warm-up each.

| Arm | Warm-up | Sample 1 | Sample 2 | Sample 3 | Sample 4 | Sample 5 | Median |
|---|---:|---:|---:|---:|---:|---:|---:|
| A / before | 8.3331 | 6.1961 (0.5732) | 5.8109 (0.9292) | 6.2597 (0.9878) | 6.3958 (0.9961) | 6.9397 (0.9414) | 6.2597 |
| B / after | 7.3887 | 5.0603 (0.9229) | 4.7256 (0.9863) | 4.7964 (0.9956) | 5.0284 (0.9360) | 4.9344 (0.9268) | 4.9344 |

Setting: installed CPU builds, stand-in ComfyUI, `--no-wait` (timing through task admission), `--timings` on both arms, same `sitecustomize.py` SHA instrumentation, fixed load gate `<1.0`, and five measured alternating pairs after warm-ups. Admission loads ranged from 0.5732 to 0.9961.

Median `pack discovery` exclusive time was 1.1551 s (A) and 0.9362 s (B). Both arms had identical hash instrumentation medians: 246 SHA-256 calls, 287,596,236 bytes, and three object-info files per command. These stage spans are descriptive and can overlap.

## Evidence limits and reproduction

`ASTRID_AB_ATTEST=off` was used because the successful installs are rooted at `installs/A|B/data/astrid`, while the part2b listener attester expects a `program/current` root. Requested and selected manifest SHAs and pre/post listener process observations are recorded, but the run does **not** claim listener/source attestation or prove per-command socket contact. The run-local wrapper captured stand-in and sampler ownership to clean up its child processes.

Reproduction command: `./runner/run-pb7-timing.sh`. The run-local harness copy adapts A/B launchers and per-arm paths, enables `--timings` for both arms, disables listener attestation, and uses the 1.5-second PB-7 gate. The bounded code follow-up stopped before a commit because it changed refusal order; no source change, reinstall, or follow-up sample resulted. Source tests were not edited or run by this timing task. Five discovery test files were already part of the fetched B branch and were not run.

`records.jsonl`, `summary-ab.json`, `timing-result.json`, `hash-instrumentation.jsonl`, `raw/`, `load-samples.txt`, process observations, manifests, runner config, preflight logs and checksums preserve this run. Since `--no-wait` with a stand-in ends at task admission, no generated image artifact/output digest was produced; task IDs and raw evidence are retained and hashed.
