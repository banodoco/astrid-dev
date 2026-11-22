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

## Run 2 (22 November 2026, 16:32 UTC)

Run 2 is a separate three-arm comparison. It preserves run 1 above and its results. The arms were run in fixed before → after → vc48 order. Each of the three groups had one warm-up and five measured commands per arm (9 warmups, 45 measured commands; 54 total), all successful. The run used a shared 4-vCPU CPU container, stand-in ComfyUI and `--no-wait`, so generation timing ends at task admission. No real ComfyUI node-info response or GPU work was measured. The candidate executions used `--timings`; the published before arm did not, so instrumentation overhead is included in those candidate timings.

| Group | Published before | Candidate after | Candidate vc48 |
|---|---:|---:|---:|
| Same-prompt generate | 15.183 s | 5.906 s | 11.294 s |
| Changed-prompt generate | 15.127 s | 5.453 s | 10.951 s |
| Timeline edit | 1.113 s | 1.147 s | 1.122 s |

The candidate comparison is descriptive. The after and vc48 tuples also differ in Agent pin, so the after-vs-vc48 delta cannot be assigned to VibeComfy alone. No causal share is claimed.

The after-arm workflow-emission medians were 0.4261 s (same-prompt) and 0.4146 s (changed-prompt), versus vc48 5.8054 s and 5.6831 s. These are measured stage spans; nested scopes overlap and must not be added to estimate total command time.

Raw-derived per-process accounting, in seconds:

| Arm / group | Median W−S | Median R | Median W−C | Per-sample W−S as share of W |
|---|---:|---:|---:|---:|
| After, same | 0.8969 | 0.4412 | 0.4313 | 12.51–16.36% |
| After, changed | 0.7688 | 0.4121 | 0.3407 | 13.54–14.48% |
| vc48, same | 0.8129 | 0.4419 | 0.3873 | 6.90–7.95% |
| vc48, changed | 0.7168 | 0.3956 | 0.3103 | 6.43–7.05% |

W is process wall time, S is the sum of named measured exclusive rows, R is residual inside the collector span, and C is the collector span. The evidence does not establish an occurrence-count oracle or a whole-process 90% attribution result. In the original run-2 records, C is absent despite being present in raw output; `collector-spans.json` is an explicitly derived reconstruction from those raw files, with paths and hashes. The original records were not amended. Raw outputs are retained under `ab-run-2/raw/`.

## Tooling and interpretation notes

The driver/summary tooling copied here includes fixes made after run 2. The original results above were recorded before those fixes; this evidence update did not rerun the measurements. The earlier broad `pkill` cleanup had a risk of matching unrelated processes. The current script uses process-ownership checks and only signals tracked children after verifying ancestry and install-root identity; focused decoy-path and child-cleanup tests are included but were not run for this evidence update. Source-only checkout paths recorded by the measurement tooling are historical; live trees and installed trees were separate. Summary ratios are descriptive measurements from these observed runs and do not identify causal contribution by repository.
