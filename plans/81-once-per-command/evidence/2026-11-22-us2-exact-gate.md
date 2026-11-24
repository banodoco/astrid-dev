# US-2 exact candidate gate — 22 November 2026

The ordinary no-delay gate passed on test candidate `2217ac4c5943e13ef7ba10d6affddb51036d9d99` with the original ceilings unchanged. Five fresh processes per group all succeeded against a source Runtime and stand-in ComfyUI on the shared four-vCPU Linux container. `bash /root/codex/plan-81/run/us2-normalized/run.sh exact-normal-2217` invoked the focused integration gate; pytest exited 0, one passed, one warning in 5:02.

| Group | Median | Original ceiling |
| --- | ---: | ---: |
| Same prompt | 19.874382 s | 20.518136 s |
| Changed prompt | 19.495070 s | 20.013685 s |
| Timeline edit | 3.807003 s | 4.204191 s |

The [accompanying JSON](2026-11-22-us2-exact-gate.json) records full stage medians, load, identities, cleanup and visualization outcome. Visualization remained report-only and failed after about 60 seconds with a renderer-lease error. All trial processes were cleaned up. The earlier ordinary run on `0f2b07cb` failed the changed-prompt ceiling, as [previously recorded](2026-11-22-us2-source-calibration.md); this later pass does not erase that result. Original ceilings were not raised. This local result does not prove the later integrated head or hosted CI, and the owner decision on initial ceilings remains open.
