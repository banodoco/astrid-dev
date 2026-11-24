# Branch inventory vs `origin/release/15/main`

Fetched refs; Git 2.55.0. Counts are `release/15/main...branch` and `release/14/main...branch` (left=main-only, right=branch-only). `+/-` = `git cherry` patch-id results. Logs below are every non-Release-15 commit; none exceed 80.

## astrid-agent

| Branch (head/date) | Counts; merge-base (date); `+/-`; merge-tree | Unique commits / area; diffstat totals; requested render paths |
|---|---|---|
| `plan-69` 83d5f8fe 11-21 | 597/0; 504/21; 83d5f8fe (11-21); 0/0; clean | Log empty; no diff. |
| `r6-fixes` ad10ff6d 11-22 | 597/7; 504/28; 83d5f8fe (11-21); 7/0; conflicts: `astrid/core/execution/generic_host.py`, `astrid/core/rendering/remotion_runtime.py` | `7bf7d908` “Drop editor's own-object route”; `24740fdf` “preserve shot clips when swapping imported media”; `cb90a4b9` thumbnail metadata; `7332e03d` launch-context names; `d4bf28e4` timing provenance; `0f6aea92` worker-context validation; `ad10ff6d` legacy retime. Areas: rendering, timeline write path, tests. Stat: `astrid` +464/−55 (15 files), `tests` +809/−1 (7). Render-path commits: 7bf,247,cb90,733,0f6. |
| `r6-render-stopgaps` 221e5003 11-22 | 597/16; 504/37; 83d5f8fe (11-21); 16/0; same two conflicts | Adds nine STOPGAPs: `f4f5a321` readiness kind; `f84c80be` empty pack path; `90380578` worker pack roots; `fa3b6df1` bundler pack roots; `54e605c6`,`007c40d3` Remotion aliases; `b051e8cc` heartbeat; `7265aa5d` custody retry; `221e5003` archived fade patch. Also inherits prior seven. Stat: `astrid` +509/−58 (17), `tests` +883/−1 (8), `remotion` +9, `astrid_runtime_client` +2/−1, `docs` +18. Render-path additions: f4f,f84,903,fa3,54e,007,b051,726. |
| `fix-1238-stale-registry-asset` 1951cfe4 11-22 | 618/1; 504/1; 9f614dff (11-18); 1/0; clean | `1951cfe4` “Drop editor's own-object route…” Rendering/tests; stat `astrid` +83/−6 (5), `tests` +99/−1 (2). Render path: this commit. |
| `fix-occurrence-media-swap` 53833fd3 11-22 | 597/1; 504/22; 83d5f8fe (11-21); 1/0; clean | `53833fd3` “preserve shot clips when swapping imported media”; timeline SDK/tests; stat `astrid` +257/−28 (7), `tests` +439. Render path: this commit (`astrid/packs/rendering/…`). |

## astrid-app

| Branch (head/date) | Counts; merge-base (date); `+/-`; merge-tree | Unique commits / area; diffstat totals |
|---|---|---|
| `plan-61` 71258577 11-19 | 170/0; 112/0; same (11-19); 0/0; clean | Log empty; no diff. |
| `plan-66` 36d2b825 11-18 | 147/1; 89/1; 2ffc0a30 (11-18); 1/0; conflicts: `scripts/save-loop/lib.mjs`, `scripts/save-loop/sweep.mjs` | `36d2b825` “seed the save-loop harness”; installer/stack tooling scripts; `scripts` +154 (3 files). No requested render paths. |
| `plan-69` e0c6f7cd 11-21 | 194/0; 146/10; same (11-21); 0/0; clean | Log empty; no diff. On Release 15, `scripts/astrid-release/astrid-release` exists (mode 100755, blob d1088c71). Vendor tree: stack App `vendor/astrid-browser` 8d5f11efb0e0d592948f12713123e9dab8fad183; Release 15 App 0ac00fc8038e211a4921d36fa059347d6b2a7e75; parent commits e0c6f7cd (11-21) and e3dbad64 (11-22): different revisions. |

## astrid-runtime

| Branch (head/date) | Counts; merge-base (date); `+/-`; merge-tree | Unique commits / area; diffstat totals |
|---|---|---|
| `plan-66` ee235d39 11-18 | 77/0; 44/0; same (11-18); 0/0; clean | Log empty; no diff. |
| Stack pin / `plan-69` b2ea261f 11-21 | 92/0; 64/5; same (11-21); 0/0; clean | Log empty; no diff. Stack commit subject: “Verify CAS objects once per process; stop re-hashing timeline history.” |

## astrid-dev plans / project-pack location

`plans/66-saving-holds-on-a-heavy-timeline/plan.md` and `plans/69-saving-holds-on-a-heavy-timeline/plan.md`: both title “Saving holds on a heavy timeline,” status “queued.” Plan 66 describes measuring/fixing saves on a synthetic 616-clip timeline, target “about 2 s”; Plan 69 extends the loop to the Plan 69 stack branches (source: `0fb17c72`, 2026-11-21; Plan 66 evidence updated at `d91b73a2`, 2026-11-18). The film project's pack sources are under `~/astrid-release/release-14-r6-fixes/data/project-packs/221335d5-722e-48d0-a0ab-d9fde94b2277/801a01b3a87941a1ab25958c488afdbf/packs/project_cd4fa4f1666bc788f4a9/` (`pack.yaml`, `docs/`, `rendering/`).
