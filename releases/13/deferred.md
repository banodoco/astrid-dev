# Release 13: deferred items and where each goes

Hannah, 14 Nov 03:20: "make sure anything deferred is appropriately captured in future plans".

This register lists every item Release 13 deferred, cut or found already failing on Release 12. Each item has the future plan it belongs in. After publication, one planning PR on astrid-dev main adds each item to that plan's `tasks.md`, or files an issue where the plan says so. Each row is then ticked here with its PR or issue link.

The sources were extracted from the R13 records (decisions.md, release-record.md, tests.md, generation.md and the briefs) on 14 Nov 03:30. The citations are file:line in `releases/13/`.

## Plan 34: real-GPU proof (first after publication)
| Item | Source |
|---|---|
| ~~h3_av after publication~~: **pulled into R13** by Hannah (03:35 Sat): i2v, v2v and video-edit run live before publish. Only what that run leaves unproven stays here. | decisions.md (03:20, 03:30 Sat); generation.md:95, 112 |
| Warm machine reloads a cold engine and its models (Plan 32 T5f, Plan 34 G2/G5) | briefs/smells-out/h1.md:31 |
| astrid-dev #260: port only if Plan 34 wants its history | evidence/open-prs.md |

## Plan 50: recorded boundaries, offline harness, dry pod (astrid-dev #640)
| Item | Source |
|---|---|
| DP-4 to DP-9: source metadata, declare-once lock, head-only fetch with a dry mode, CPU engine stop, validation without queueing, hosted CPU job | decisions.md:1202, 1218; briefs/dry-pod-plan.md:51, 84 |
| Structural follow-ups: a real pod agent, a no-op CPU engine, migrating the remaining readers, lifecycle typed errors, a container CI job (about 11 worker-days) | structural-runpod-design.md:20, 432 |
| T6: size the lease to the full lifetime; key restart recovery on executor liveness and epoch (RB-4) | decisions.md:1276; briefs/lease-liveness/plan.md:79 |
| The Runtime declares `lease_seconds` in its contract (option a, with a pin bump) | decisions.md:1317-1320 |
| The Runtime exempts control capabilities from storage admission (option 1, with a pin bump). T4's control slot: deadlock #642, and #641 | decisions.md:1343-1349 |
| Separate venvs for the comfy and runpod extras, or a common SDK floor | decisions.md:1324 |
| Fault-matrix rows (reply lost after commit, host stalled, release during a job, release after a failed job) and a slow-transport injector | briefs/lease-liveness/plan.md:80 |
| The 57-minute CPU journey: bound its time (RB-1) | smells-out/2026-11-12-cpu-journey-takes-57-minutes.md |
| CPU journey's remaining failures: host graph cleanup, the pod deadline, a cancelled machine not released, receipt unavailable vs not_collected | smells-out/2026-11-12-cpu-journey-remaining-failures.md |
| The Agent reads `waiting_details`, which the pinned Runtime omits: pin a Runtime that sends it, or remove the read (RB-3/RB-4) | smells-out/2026-11-12-agent-reads-field-pinned-runtime-omits.md |
| The integration lane's Runtime and lifecycle checkouts are unprovisioned (RB-1; Plan 39 AT1.4) | smells-out/2026-11-12-integration-lane-dependencies-unprovisioned.md |
| Revise Plan 50: the scrubber, the ratchet and RB-4 are over-built (critique accepted) | decisions.md:677; smells-out/2026-11-12-plan-50-over-built.md |
| Volume pins an empty datacenter (no home yet; adjacent to RB-4) | smells-out/h2.md:28 |

## Next machines plan (M-series after R13)
| Item | Source |
|---|---|
| M3, M4 and M5 to M9 | decisions.md:1210 |
| M11: a neutral machine interface. Core neutrality: either pull M11 into M4/M7 or take an owner exception; the scanner vocabulary fix and a one-time baseline for the 36 RunPod crossings | decisions.md:771-788; briefs/machines-plan.md:56 |
| M12: several machines per account | briefs/machines-plan.md:57 |
| M13: the balance view and a default project at provisioning (T11) | briefs/machines-plan.md:58; release-record.md:68 |
| LT wiring: the enumeration table only, as a check; the LT-b publication latch T1 to T4; R2-2; the cede write-ahead record; the binding-fence test (astrid-dev #611) | decisions.md:997-1001, 1209-1211 |
| The watchdog stops its own pod: today at parity with R12 | decisions.md:1215 |
| K1 follow-ups: remote_placement, provider, failure_receipt and pod_fields typing and gates | briefs/machines-handover.md:116; briefs/machines-gates.md:15 |
| Structured machine interface: create, delete and leases; the shared inspect_target_records check | briefs/struct-design.md:37, 40 |
| No shell on a rented machine, for diagnosis (owner request O8) | decisions.md:1057 |
| Reconcile pod 0d7f7e41 in the old state | decisions.md:493-495 |
| The lifecycle exposes typed status and Retry-After | decisions.md:463 |

## Generation, catalog and engine (next generation plan; T-series group B)
| Item | Source |
|---|---|
| T7: the wait reason reaches the CLI | release-record.md:67 |
| T8: the Runtime blocker list | release-record.md:68 |
| T10: models stay loaded between jobs | release-record.md:68 |
| T13: CPU journey: two stale tests and the first-claim deadline | release-record.md:68; decisions.md:675 |
| T14: a dry run of every catalog entry (with T1) | release-record.md:68; decisions.md:676 |
| Astrid models.lock.json uses the same model record | release-record.md:68; briefs/declarations-t3.md:21 |
| Astrid `flf` mode shows as unavailable | briefs/declarations-t3.md:49 |
| About 16 templates' ready_id to fix. Four declare no qualified id (z_image_turbo, z_image_img2img, basic_image_upscale, empty_image_red) | decisions.md:505 |
| Music: minimax_music_3 needs a real default prompt, or stays below ace_step (R13 made ace_step the default) | decisions.md (02:25 Sat) |
| Video entries beyond h3 (wan-2.2 "not qualified" in CI) | test lane, 13 Nov |
| Supervisor records the launch offset, and jobs declare from it | decisions.md:364 |
| Patch work: schema identity for schema-changing patches, sha256_before diagnostics, attached release attestation, concurrent-writer atomicity, the engine_runner base-bump hazard, workflow-ref transport | decisions.md:564, 576 |
| TTS: fork to banodoco, replacing the declared-patches mechanism | decisions.md:786, 788 |
| Model layout: V2 (extra paths in the launch args), A4 (reuse a person's models folder), A5 (no ComfyUI-specific model code in core), D1 (a docs page) | briefs/model-layout-design.md:45 |
| Installed smoke test (parked as c-smoke2) | decisions.md:310, 456 |
| Re-pin cells to `r13/cells-vc` | decisions.md:735 |
| Keep the labels and drop the allowlist (rework) | decisions.md:340 |

## VibeComfy
| Item | Source |
|---|---|
| Lifecycle re-vendor: the lock can't resolve comfy and runpod-launch together (`r13/lifecycle-v2` is parked) | decisions.md:1312-1323 |
| cm_cli tests (6), already failing before R13 | decisions.md:572 |

## Runtime (next Runtime plan)
| Item | Source |
|---|---|
| Media-type hardening: filter media_type to image, video or audio; Runtime tests for unaccounted media | decisions.md:48 |

## Plan 39: tests and quality (already failing on Release 12, or quarantine rules)
| Item | Source |
|---|---|
| Timeline: all 173 test_timeline_* ids (Runtime commit 9ef8087), astrid-dev #637 | tests.md:58, 80; decisions.md (03:25 Sat) |
| tests/scripts: 85 + 4 (pod_jobs, pod_bootstrap, gpu_sanity, pod_session, pod_held_budget) | tests.md:81 |
| Lanes D order-dependent shared_redo (4), astrid-dev #636 | tests.md:46 |
| test_registry pack-declared backend id (4), astrid-dev #639 | tests.md:76 |
| test_pinokio_platform_adapter real_local_start flake (6), astrid-dev #621 | tests.md:67 |
| test_installer_sources VibeComfy-URL failures (17) | decisions.md:152 |
| 59 of 60 failures predating G2 (fail on main a105de3a) | decisions.md:23 |
| claim_runpod_5090_backup: 7 ids failing on R12 too | decisions.md (03:25 Sat) |
| Setup 409 conflict from stale host state, astrid-dev #631 | decisions.md:1064 |
| Mypy-parked types, astrid-dev #633 | evidence/tests/handover.md:18 |
| Non-blocking lint classes beyond F821, BLE001 and the name, attr and call-arg checks | decisions.md:1007-1010 |
| Remove the mypy total gate, and the ruff total gate if redundant (Hannah's decision) | decisions.md:895 |
| 54 broad-except sites, classes (a) and (b), for review | decisions.md:35 |
| Shared fakes per seam | decisions.md:1021 |
| test_warm_session paid-expiry: quarantine only under the Plan 39 rule if still unfixed | smells-out/2026-11-12-warm-session-paid-expiry-tests-failing.md |
| R13 named exceptions (stale tests after a deliberate R13 change), listed in the release record at publish | Hannah's rule, 03:20 Sat |
| Agent #264 | evidence/open-prs.md |

## Outside pull requests (owner revisits; nothing closed)
| Item | Source |
|---|---|
| Agent #346 (owner's call), runpod-lifecycle #2, and five worker-permission PRs (Agent #312, Runtime #38, App #220, VibeComfy #164, lifecycle #4), after publish | evidence/open-prs.md; release-record.md:70 |
| App #158: re-raise after R13; App #130: design input later | evidence/open-prs.md |
| Tell the deferred outside contributors which release considers their PRs | release-record.md:70, 124 |

## Process (astrid-dev skills and ledger)
| Item | Source |
|---|---|
| Weekly limit: every session reports its seven-day warning state at check-ins; warn Hannah and cut model use at the first warning | decisions.md (02:05, 02:40 Sat) |
| When a lane ends, its rows get a named owner within the hour (the engine-fork gap) | advisor dive 4 |
| Managers farm hands-on work to Codex subagents; the advisor measures it each dive | decisions.md (02:50 Sat) |
