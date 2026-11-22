# Installed A/B run, gated (22 November 2026)

Setting, stated every time: installed builds, a CPU container, a stand-in ComfyUI, a shared 4-vCPU box, `--no-wait` (times Astrid up to "task queued"). Not covered: a real ComfyUI's answer to the node-information request, and anything GPU-bound. Every command started below 1-minute load 1.0 (0.92 to 0.98); all 36 commands succeeded. The after arm ran with `--timings`, whose overhead is inside its numbers.

Before: the published Release 14 (agent c0ad6b54, runtime 5120462d, VibeComfy 48b5fa9e, lifecycle 9f88ef76). After: Plan 81's range (agent bc75d6c5 = a local pin-bump commit on `release/15/plan-81` at 9c95c680, runtime 72b129e5, VibeComfy 36ea976f from PR 182). `omp` came from npm in both arms (its GitHub source was blocked for the session; the timed commands never call it).

| Group | Before median | After median | After / before | Change |
| --- | ---: | ---: | ---: | ---: |
| `generate image`, same prompt | 15.007 s | 5.410 s | 0.36 | -64.0% |
| `generate image`, changed prompt | 15.217 s | 5.624 s | 0.37 | -63.0% |
| `timelines edit` | 1.254 s | 1.172 s | 0.935 | -6.5% |

After-arm stages (median seconds, same prompt / changed prompt): model registry 1.09 / 1.11 (pack discovery 0.48); candidate preparation 1.06 / 1.13 (workflow build 0.73 / 0.77); Runtime connection 0.80 / 0.90 (pack host attachment 0.54 / 0.61; launcher connection 0.20; source identity 0.14, inside attachment); candidate qualification 0.51 / 0.53; workflow emission 0.41 / 0.42.

Limits: the run's summary step crashed on a stage row with no `total_seconds`; `summary-ab.json` was rebuilt from the printed per-command lines and the raw output with `rebuild_ab_summary.py` (load figures to two decimals). The driver was patched to tolerate that field; the patch has not yet been exercised in a full run. The split of the 63% between the Agent range and the VibeComfy fix is not separated yet. Re-run: `run-ab-installed.sh --run` on a quiet box.
