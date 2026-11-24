# Plan 82 stage 1: installed `generate` time, base against candidate (24 November 2026)

For the Release 15 Lead's gate condition (r15-lead-p82-0002): the installed `generate` time on the landing head, with RA-6's check added and RA-1b's imports removed, against today's 5.36 s; stage 1 must not be slower. Measured by a background agent for the Plan 82 orchestrator; raw records in [run1/](run1/) and [run2/](run2/), driver in [scripts/floor_s1.py](scripts/floor_s1.py).

**Result: not slower.** Pooled medians over 10 samples per arm: base 5.645 s, candidate 5.481 s (delta -0.163 s). Over the 7 gated samples per arm (load below 1.0 before each): base 5.557 s, candidate 5.485 s (delta -0.071 s). The spread inside each arm is about 0.7 s, so **the end-to-end difference is within noise**. The one stage change that shows in both runs is the **approval compile, down about 0.16 s** (0.318 to 0.160 in run 2); emission is down about 0.05 to 0.09 s; workflow build, pack-host attachment and other command work are each 0.03 to 0.05 s higher. Pack discovery (2.3 s) is the same.

## What was measured

- **Installs:** the published bootstrap (`install.sh`, sha256 `c268a5fa…`, from the Part 2b copy) with `--root`, `--data-root`, `--yes --autostart off --command on --skills off --skill-copies off`, isolated HOME, two roots on different door ports; manifests in [manifest-base.json](manifest-base.json) and [manifest-cand.json](manifest-cand.json) (the floor experiment's manifest with the shas and local repos swapped; omp from npm). Python 3.11.13 for both; `run-astrid --version` astrid/0.1.0 for both ([versions.txt](versions.txt)).
- **Base:** Agent `514499de` (release/15/main before Plan 82), Runtime `24e2c929`, VibeComfy `c0e910ca`. **Candidate:** Agent `e254d780` (a local commit: Plan 82 stage 1 = `4f639cc0` plus the generator-only pin commit; `release/15/plan-82` at `c63a7f84` adds only a clean merge of release/15/main `a3f3b01c`, which touches no Plan 82 file), Runtime `24e2c929`, VibeComfy `901fc611`. Deviation: because the source repos are shallow and the candidate commit is unreferenced, uv fetched from throwaway repos that borrow the originals' object stores (alternates); the originals were not changed.
- **Command:** `run-astrid generate image "a red square on a plain background" --mode t2i --placement http://127.0.0.1:<stand-in port> --project floor --no-wait --json --timings`, to "task queued", against the stand-in ComfyUI (13 classes), five alternating samples per arm per run, one warm-up, each task followed untimed to a terminal state (all 24 tasks `succeeded`). A shared 4-vCPU box. Run 1 ran while two long pytest suites were active (the load gate was not met for its first three samples); run 2 ran on a quiet box with every sample gated (load 0.89 to 1.00).

| | Run 1 (s) | Run 2 (s) |
|---|---|---|
| Base | 5.696, 5.787, 5.943, 5.254, 5.256 (median 5.696) | 5.955, 5.331, 5.919, 5.557, 5.593 (median 5.593) |
| Candidate | 5.283, 5.695, 5.254, 5.478, 5.485 (median 5.478) | 5.526, 6.018, 5.341, 5.464, 5.577 (median 5.526) |

## Limits

The 5.36 s in the floor experiment was a different box state; the base here is 5.56 to 5.65 s. These are component timings on a shared container with a stand-in ComfyUI, not a person's machine. **No cache is in this stage, so the 3 s target is not claimed; the stage-1 claim is "not slower, approval compile faster".**
