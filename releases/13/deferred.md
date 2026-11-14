# Release 13: deferred items and where each goes

Hannah, 14 Nov 03:20: "make sure anything deferred is appropriately captured in future plans".

This register lists every item Release 13 deferred, cut or found already failing on Release 12. Each item has the future plan it belongs in. After publication, one planning PR on astrid-dev main adds each item to that plan's `tasks.md`, or files an issue where the plan says so. Each row is then ticked here with its PR or issue link.

The sources were extracted from the R13 records (decisions.md, release-record.md, tests.md, generation.md and the briefs) on 14 Nov 03:30. The citations are file:line in `releases/13/`.

## Plan 34: real-GPU proof (first after publication)
| Item | Source |
|---|---|
| ~~h3_av after publication~~: **pulled into R13** by Hannah (03:35 Sat): i2v, v2v and video-edit run live before publish. Only what that run leaves unproven stays here. | decisions.md (03:20, 03:30 Sat); generation.md:95, 112 |
| ~~Warm machine reloads a cold engine and its models (Plan 32 T5f, Plan 34 G2/G5)~~: **pulled into R13** with T10 (Hannah, 14:05 Sat) | briefs/smells-out/h1.md:31 |
| astrid-dev #260: port only if Plan 34 wants its history | evidence/open-prs.md |

## Plan 50: recorded boundaries, offline harness, dry pod (astrid-dev #640)
| Item | Source |
|---|---|
| DP-4 to DP-9: source metadata, declare-once lock, head-only fetch with a dry mode, CPU engine stop, validation without queueing, hosted CPU job | decisions.md:1202, 1218; briefs/dry-pod-plan.md:51, 84 |
| Structural follow-ups: a real pod agent, a no-op CPU engine, migrating the remaining readers, lifecycle typed errors, a container CI job (about 11 worker-days) | structural-runpod-design.md:20, 432 |
| T6: size the lease to the full lifetime; key restart recovery on executor liveness and epoch (RB-4) | decisions.md:1276; briefs/lease-liveness/plan.md:79 |
| The Runtime declares `lease_seconds` in its contract (option a, with a pin bump) | decisions.md:1317-1320 |
| The Runtime exempts control capabilities from storage admission (option 1, with a pin bump). T4's control slot: deadlock #642, and #641 | decisions.md:1343-1349 |
| Separate venvs for the comfy and runpod extras, or a common SDK floor. **This covers the VibeComfy re-vendor:** lifecycle on Linux keeps `runpod>=1.12`, so VibeComfy's `[comfy]+[runpod-launch]` lock can't resolve against comfyui's `requests<2.34` | decisions.md:1324 |
| Fault-matrix rows (reply lost after commit, host stalled, release during a job, release after a failed job) and a slow-transport injector | briefs/lease-liveness/plan.md:80 |
| The 57-minute CPU journey: bound its time (RB-1) | smells-out/2026-11-12-cpu-journey-takes-57-minutes.md |
| CPU journey's remaining failures: host graph cleanup, the pod deadline, a cancelled machine not released, receipt unavailable vs not_collected | smells-out/2026-11-12-cpu-journey-remaining-failures.md |
| The Agent reads `waiting_details`, which the pinned Runtime omits: pin a Runtime that sends it, or remove the read (RB-3/RB-4) | smells-out/2026-11-12-agent-reads-field-pinned-runtime-omits.md |
| The integration lane's Runtime and lifecycle checkouts are unprovisioned (RB-1; Plan 39 AT1.4) | smells-out/2026-11-12-integration-lane-dependencies-unprovisioned.md |
| Revise Plan 50: the scrubber, the ratchet and RB-4 are over-built (critique accepted) | decisions.md:677; smells-out/2026-11-12-plan-50-over-built.md |
| The timeout failure RPC carries no `failure_diagnostic`; only `lease_lost` sends it (generic_host.py ~:11552). The receipt has it. A new contract, not R13 (machines, 04:25 Sat) | machines' message, 04:25 Sat |
| T4 control slot: branch `r13/machines-t4` b9dcbce0f (#642 deadlock, #641 unacknowledged cancel). It conflicts with engine T1 on `test_fail_closed_g28.py::…[settlement]`. Journey row `test_runtime_silent_for_one_lease_then_release` is saved as `wt/runs/t4/journey-test-v2.patch`, and is blocked on the CPU fake pod serving the install-receipt and logs-manifest reads | machines' message, 04:25 Sat |
| Volume pins an empty datacenter (no home yet; adjacent to RB-4) | smells-out/h2.md:28 |

## Next machines plan (M-series after R13)
| Item | Source |
|---|---|
| Pod RPC startup timeout without orphaning: the hosted 600 s test (`test_machine_cli_claim_then_generate_reuses_pod_and_paid_expiry`) is the transport retrying 404s until the wall because its command timer starts after startup. A bound that kills the local child skips the transport's remote cancel (orphans an accepted command) and lets claim startup retry past an unreaped child. Root fix: keep the remote command identity and reserve time for verified cancellation, and fence an unreaped observer into the owner's custody before any retry or admit. R13 reverted the unsafe bound | M2 rows review (wt/briefs/wave3/m2-rows-review.log), machines 04:50 Sat |
| Reclaim does not age the private default attempt spool: generic-host default attempt spools now live under the private runtime data root / `XDG_RUNTIME_DIR` / `~/.cache/astrid/attempts/<sha256(executor_id)[:16]>` (hostwedge, `r13/host-wedge` 1505a379c), but `storage_ownership`'s `attempt-roots` policy only ages `astrid-attempt-*` under the system temp directory (2 days). The host removes each attempt root on completion (`_cleanup_ephemeral_attempt`), so only crash-abandoned attempts accumulate, and a hostwedge recovery marker is left on purpose after a skipped 404 (`recovery_blocked` entries name the paths). Narrow fix: add a second `attempt-roots` scan of `<private root>/attempts/<digest>/astrid-attempt-*` by child mtime (keep the digest directory). Deeper cause: reclaim has one fixed temp root per policy rather than asking the host where it spools; one shared resolver would serve both. | cells hostwedge3 report; machines review (297270e38) |
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
| RunPod model-cache GC: a references-based, dry-run-first cleanup of the network volume with deletion receipts (h3 hit "Disk quota exceeded" on the 200 GB volume 2z2dlu1v8g; suspected old `h3-golden` release copies). About 2–3 days plus live qualification | machines, 04:25 Sat; decisions.md 04:35 |
| No shell on a rented machine (O8): storage could not be inspected on the full volume. Candidate: product diagnostics as declared run-log steps | decisions.md 04:35 Sat |
| Host attempt reclaim does not age crash leftovers in the private per-executor root (hostwedge 1505a379c): a slow disk leak, no custody effect | decisions.md 16:50 Sat (machines review) |
| hostwedge hardening beyond R13: descriptor (fstat) validation of the spool base, ancestor checks, and the reclaim uid/mode rule in storage_ownership.py:163/:224 (Astra W84 items 2–3; not user-hittable on a single-user machine) | decisions.md 17:52 Sat |
| httpj: cold SDK release for an older journal without `claim_preferences` (no users, so no old journals at R13) | decisions.md 17:52 Sat |
| The lifecycle exposes typed status and Retry-After | decisions.md:463 |
| Network volume size freshness: the storage preflight takes the volume size from the claim journal, which copies the saved setup preference (machines_cli.py:616). A volume resized larger after `machines setup` can be refused against its old size until setup is re-run. Root: refresh the size from the provider record the claim already reads, or record its read time in the refusal | volsize card; Agent 9e5a1963a; machines 11:00 Sat |
| storage.inventory walker hardening: traverse descriptor-relative with O_NOFOLLOW and check each opened directory's identity and device, so a directory swapped for a symlink mid-walk cannot list names outside the volume (P2); count each hardlinked inode once per reported ancestor (P3). The inventory is read-only diagnostics on our own pod | volume card review 3 (wt/runs/vol/review3-findings.md); machines 09:55 Sat |
| Storage preflight across directories: two target directories sharing one budget (a common quota or device, or bind aliases) can each pass while together they do not fit; R13 accepts this missed refusal to rule out false refusals. Root: establish each measurement's real quota scope (XFS project ids, MooseFS quota roots) before aggregating | volume card review 2; ruling machines 08:47 Sat; docs/runpod-storage.md |
| Storage preflight credits a sha256-verified model that native fetch will still redownload, because its source receipt (URL or revision) changed: a missed refusal, no worse than without the preflight. Root: VibeComfy exposes one read-only reuse decision (today it is inline in fetch.download, fetch.py:542), and preflight and fetch share it | volume card review P1 #3 (wt/runs/vol/review-findings-r1.md); Agent b216b4cfa; machines 08:30 Sat |
| Core→vibecomfy imports to reroute through the engine contribution: generic_host.py:12831/12835 (live approval and managed-asset staging) via a new engine `host_preflight`, keeping trusted-host ordering (EDGE-1/2); managed_preparation.py:653/666/682 native pip, preparation and doctor program factories via contribution factories, keeping the generated bytes, verified interpreter and custody (EDGE-4). R13 baselines them under named rulings; precedent: the machine failure_recorder hook in 4a9b9dcfb | wt/runs/edges/core-pack-import-analysis-08d74e27e.md; machines 05:52 Sat |
| Model download resume in managed preparation: the native VibeComfy fetch path (`managed_preparation._command` → vibecomfy fetch, fetch.py:589-618) never reads a `.part`, so an interrupted multi-GB download restarts from zero, and a stale `.part` keeps occupying the volume. `asset_alignment._fetch_model` resumes, but peaks at 2S−P. Root: one resuming fetch with a peak of S−P, declared once. The R13 storage preflight charges the full size (correct for today's path) | volume card round 4 (wt/c-vol/.tmp-tests/proof/round4/source-findings.md), machines 05:45 Sat |
| Reuse one pod source archive per pinned tuple: bootstrap rebuilds and recompresses the whole source tree for every claim and re-bootstrap (a killed-pod third generation built it three times). R13 drops gzip to level 1 (18.8 s to 6.5 s, 134 MB to 144 MB) as the narrow fix; the root is a content-addressed archive cached locally and on the volume | rows2 report (wt/runs/rows2/keep/report.txt), machines 05:32 Sat; Agent bcd674ed4 |
| ~~Four remote_machine_cpu assertions that predate deliberate changes~~ DONE in R13: Agent a50bfda18 (rows3 515c25e1f; 4 passed with Runtime, test lane 06:41 Sat). Was: ruled for update, not applied before the 06:00 read: custody-change expects `--models-root` (7e3314ad2); cancel-mid-poll keeps the verified idle pod until explicit release, then delete and 404 (80bbf6904, d072cf5da); the preclaimed job has no capacity-wait phase (d29f58570); an unreported log manifest is `unavailable/not_reported` (30795fec8) | rows2 report, machines 05:32 Sat |

## Generation, catalog and engine (next generation plan; T-series group B)
| Item | Source |
|---|---|
| T7: the wait reason reaches the CLI | release-record.md:67 |
| T8: the Runtime blocker list | release-record.md:68 |
| ~~T10: models stay loaded between jobs~~: **pulled into R13** by Hannah (14:05 Sat), with release on memory need or warm-down. Fable sense-check, then cards | release-record.md:68 |
| One home for warmth: `backends/vibecomfy.py` fingerprint warm session (frees on any fingerprint change) and `_WARM_SESSION_ADAPTERS` (Wan only) sit off the R13 warm path. Plus: release before the next job after an OOM-classified failure, only if a self-managing node pack (TTS, Foley, h3) is seen to OOM | Fable warm-models check, decisions.md 14:12 Sat |
| With the explicit `models.trust_unchanged` opt-out enabled (default: full re-verification): Model verification records optimize re-verification for trusted writers on reliable storage metadata. They are not tamper-proof evidence against code running as the engine's user (ComfyUI and its custom nodes, which this design already trusts: engine_custody 'trusted engine'), nor against changes that preserve (st_dev, size, mtime_ns, inode, ctime_ns). Before W3, a model-only change was caught at the next preparation; now a same-user process that also writes a record is not. A separate isolation boundary (another UID or a sandbox) would be needed to restore that. The device number is not stable across a network volume remounted on another pod, so key matching there is best-effort and may re-hash. | machines/engine W3 round 3 ruling, 16:55 Sat; Agent `r13/machines-w3` at `ae4d0a58e` |
| Attached model download writes to whatever absolute folder the ComfyUI server reports (asset_gaps.py:328). It is shown in the confirmation, so acceptable for R13; constrain it to known model roots later (P4.6b.1) | advisor dive 7 phase 4 review |
| T13: CPU journey: two stale tests and the first-claim deadline | release-record.md:68; decisions.md:675 |
| T14: a dry run of every catalog entry (with T1) | release-record.md:68; decisions.md:676 |
| Astrid models.lock.json uses the same model record | release-record.md:68; briefs/declarations-t3.md:21 |
| Astrid `flf` mode shows as unavailable | briefs/declarations-t3.md:49 |
| About 16 templates' ready_id to fix. Four declare no qualified id (z_image_turbo, z_image_img2img, basic_image_upscale, empty_image_red) | decisions.md:505 |
| Music: minimax_music_3 needs a real default prompt, or stays below ace_step (R13 made ace_step the default) | decisions.md (02:25 Sat) |
| h3 i2v is reference-guided, not a true first frame (Hannah asked for "feeding first frame"). A guide at index 0 conditions but doesn't preserve pixels; the follow-up is a protected latent anchor (cells' h3first, 04:55 Sat) | cells' message, 04:55 Sat |
| Video entries beyond h3 (wan-2.2 "not qualified" in CI) | test lane, 13 Nov |
| Supervisor records the launch offset, and jobs declare from it | decisions.md:364 |
| Patch work: schema identity for schema-changing patches, sha256_before diagnostics, attached release attestation, concurrent-writer atomicity, the engine_runner base-bump hazard, workflow-ref transport | decisions.md:564, 576 |
| TTS: fork to banodoco, replacing the declared-patches mechanism | decisions.md:786, 788 |
| Model layout: V2 (extra paths in the launch args), A4 (reuse a person's models folder), A5 (no ComfyUI-specific model code in core), D1 (a docs page) | briefs/model-layout-design.md:45 |
| Installed smoke test (parked as c-smoke2) | decisions.md:310, 456 |
| Re-pin cells to `r13/cells-vc` | decisions.md:735 |
| Keep the labels and drop the allowlist (rework) | decisions.md:340 |
| Engine bootstrap size: R13 raised the per-string source budget 96→120 KiB and the total to 136 KiB (f5f9e2ebc) because the source grew to ~103 KiB. Safe for R13's local-exec use (8 KiB under Linux's 128 KiB MAX_ARG_STRLEN), but the 136 KiB aggregate exceeds Linux's 128 KiB guaranteed minimum, excludes the inherited environment, and no remote caller's serialized transport is checked. Root fix before any remote use: shrink the source (base85 saves ~6.5 KB) or transfer the payload separately, and check the final transport limit | machines/engine ruling 04:10 Sat; s1-regress Astra review (wt/briefs/wave3/s1-regress-review.log) |
| h3 cold runs: size the preparation deadline from the bytes still to fetch, capped at the claim's paid expiry (53.5 GB vs the fixed one-hour deadline, local_job.py:139). Needs paid expiry carried to the pod job and model requirements resolved before the deadline is set. R13 only adds "rerun to resume the download" to the timeout message (f7afb3e42) | h3-live plan row 5; machines/engine 04:25 Sat |
| RunPod model-cache GC: references from current locks, retained versions and active jobs; version retirement; dry-run-first cleanup with explicit apply, custody revalidation and deletion receipts (about 2–3 days plus live qualification). R13 ships a read-only lock-aware audit (scripts/model_storage_audit.py) and a measured storage preflight | machines volume card, 04:25 Sat |
| h3_av: rational `5/24` duration fails canonicalization for source-backed modes (spec.py:218, request_v2.py:62-84; normalization emits a float that is rechecked exactly). R13 inputs use six frames; one duration representation is the root fix (card `h3dur` may land it) | cells-log.md 02:51 Sat |
| h3 i2v image is reference conditioning (Picture 1), not a guaranteed first frame: a guide at frame 0 conditions but does not preserve pixels; the preferred follow-up is a protected latent anchor (locked `MiniMaxH3CustomKeyframesMasked`: new executed node, sampler-mask route, request contract), 35-60 lines for narrow admission; GPU qualification and an encoding/composition contract needed for literal pixel identity (card h3first, evidence h3first-resume/report.txt) | cells card h3first |
| Hook admission order is implicit: the merged h3 hook declared run logs before validating the request, so typed refusals (ignored frame overrides) turned into log-setup errors until `05b83dc58` reordered them. Root: one explicit admission step in the hook contract (validate, then declare outputs, then run) | cells commit 05b83dc58 (narrow) |
| h3 plain inputs: plain documents are v1 (tested v2-canonical equivalence only); local/attached defaults now require the H3 dependencies and do not fall back to LTX; the source-backed five-frame clock issue is fixed separately (c5e4f7cc2). GPU execution of the plain path unproven | cells card h3plain, h3merge |
| Default selection resolves h3 for a target that lacks its nodes (an attached video/i2v default now selects h3 and refuses with a typed `missing_node_pack` readiness error: 'target is missing node BasicGuider; install it on the requested ComfyUI target, or choose a target that provides it'), instead of choosing a runnable default or naming the h3 requirement up front. R13 keeps the recorded no-LTX-fallback limit (named exception: h3 declares the kind's plain inputs, 5fe9ed7a0); cells commits e42e0dd40 (actionable message) and fea67d9cb (`missing_node_pack` listed in the selection test's REFUSALS). Follow-up: select by the target's installed nodes, or fall back to a runnable default with a notice | cells card i2vsel |

## Runtime contract
| Item | Source |
|---|---|
| bug14 `test_conflict_fails_exact_owner_without_conflicting_evidence`: its oracle is from a042638fc, and the pinned Runtime 6855dfa8 now accepts the metadata alias. Decide the contract, then update the test or the Runtime (machines, 04:20 Sat) | machines' message, 04:20 Sat |

## VibeComfy
| Item | Source |
|---|---|
| Lifecycle re-vendor: the lock can't resolve comfy and runpod-launch together (`r13/lifecycle-v2` is parked) | decisions.md:1312-1323 |
| cm_cli tests (6), already failing before R13 | decisions.md:572 |
| Save-as-entry is slow: `generate workflow --as-entry --no-run` takes about 61 s per flux workflow because `cache_file_witness` re-hashes about 14 MB per node with no memo (consume.py:220/264/270/314 at d3850831). Fix: memoise per (path, stat). **Fix ready:** VibeComfy `post13/object-info-witness-memo` e8f19340 (memo keyed on path plus size/mtime_ns/inode/ctime; 3,058 hashes → 2, 5.37 s → 1.21 s offline; 0 regressions over 1,779 tests). It is based on d3850831, so it is merged onto vc-11 when pinned after publish. Plan 20 P4.9 times it. | Plan 20 inputs.md (b7b8960); decisions.md 12:38 |
| ~~`audio/hunyuan_video_foley` picker contract~~: **fixed in R13** (VibeComfy `r13/cells-vc-7` 8083c8ef: optional `diffusion_model` and `vae` public pickers; Agent pin `r13/compose-pin-vc7`). Remote placement had skipped the binder (live passed); explicit attached/local runs failed `catalog role 'foley' does not match its pinned template input` | cells card foleybind, vc7 |
| LTX i2v checkpoint identity: **pinned in R13** (VibeComfy ae7dd067: sha256 28606c5b5a06ce56f896d4dfcb20f212739e07a68fbe48e53638188449d26450, size 29145431166, revision 91eda216f820e5ecb3d17dc9fe3b7cdaf56b587d, from one unauthenticated HF HEAD, no weight bytes). The same template's LoRA and text-encoder records still lack digests | cells card vc7; evidence/cells/vc7-ltx-metadata.txt |
| **Class: template models without declared digests.** Offline survey of all 52 ready templates at VibeComfy ae7dd067: 132 incomplete declared records (missing sha256 and/or size_bytes) across 31 templates; the Agent's managed-preparation guard (731c27b0d, managed_preparation.py:277-280) refuses every one of them when managed. Includes the flux2-klein edit templates, the LTX LoRA/text-encoder records and many more (full list: evidence/cells/vc7-digest-gaps.md). Fix: every downloadable model carries a pinned revision, digest and size declared once, filled from authoritative metadata (one head-only read per file), then one pin refresh | cells card vc7 |
| **Security (fixed in R13 as VibeComfy cells-vc-11 + one Agent pin; the deeper question stays open):** should a user workflow's arbitrary model URL be fetched at all without an explicit confirmation? R13 closes the credential leak (`HF_TOKEN` was attached to every URL `vibecomfy.fetch.download` fetched, fetch.py:583-586; now only https Hugging Face hosts) but a user or third-party workflow's `properties.models[].url` still makes the pod download from any https host with the digest the workflow declares. The follow-up is an explicit confirmation of non-Hugging-Face model sources (Plan 20 P4.6b is the start), plus a host allow-list or per-run consent in the Agent's direct-URL lock form (`model_downloader._validate_model` accepts any https host) | cells analysis 12:50 Sat; orchestrator note 12:51 |

## Runtime (next Runtime plan)
| Item | Source |
|---|---|
| `astrid-runtime up --wait` fails when another Runtime holds door port 17340, and `--hosted-origin off` is refused with `--wait`. This affects only two Runtimes on one machine or a source checkout; installed users start via the service. | Plan 20 walk P4.9.2, decisions.md 15:46 Sat |
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
| Production-engine tests duplicate or mock around the owned-preparation path; build one shared prepared-engine fixture (cells narrow fix: Agent `r13/rows-ir-bridge` 3573a5b85) | cells-log.md 02:51 Sat; r13/rows-ir-bridge |
| The shipped census hard-codes counts (executors 54 to 49 at `r13/rows-packs-census`): derive the expected set from the pack manifests, keep a short allow-list for deliberate changes | cells-log.md 02:51 Sat; test_b2_integrated_closure.py |
| Red-cell characterization tests pin another layer's message wording instead of an error code (cells narrow fix: `r13/sfx-red-ruling` 11f222e36, `_RED[("audio","sfx"),"attached"]`); characterize red cells by error code plus the missing-weight name | cells-log.md 05:15 Sat; machines ruling 05:10 |
| Integration cells run under the 120 s timeout on a loaded box and share the worktree's `astrid/.packs.transaction.lock` between concurrent runs (load artefacts, no code): give each concurrent run its own pack-lock root | cells-log.md 05:15 Sat; gold-after.log |
| Import cycles `generation ↔ pack` (pack/permissions.py:7 ↔ generation/availability.py:23) and `rendering ↔ timeline` (timeline/banodoco_schema.py:518 ↔ rendering/profile.py:13) are absent from import_cycles.json yet reproduce at R12 main 0e1543e0 (worker-env run, `make cycles`); move each shared contract to a dependency-neutral module. The third pair, `generation ↔ machines_cli`, is new at R13 and was fixed by machines (cli_shared.py), not deferred. Both pairs are recorded in `scripts/reshape/baselines/import_cycles.json` (`known_before_release_13`, branch `r13/tests/cycles-baseline` 62c2317e6): removing a cycle in Plan 39 removes its baseline entry and this row together | test-manager run W71 (a4d893c8), /home/user/wt/r13-tests/runs/w71/report.md; orchestrator ruling 08:43 Sat |
| `tests/core/generation/test_listing.py::test_qualified_fake_model_remains_available` fails on R12 main 0e1543e0 (local R12 run, 14 Nov: rows `availability: unavailable, backend: cloud, fix: use a qualified generation route`) and on every R13 head; qualified-model listing | test-manager R12 run (/home/user/wt/agent-r12); Plan 20 workers via orchestrator, 14 Nov |
| `tests/core/generation/test_readiness_inputs_f04.py::test_missing_target_nodes_and_models_are_all_reported` and `::test_dry_run_is_the_readiness_envelope_without_source_or_config_writes` fail on R12 main 0e1543e0 (local R12 run, 14 Nov: 2 failed, 25 passed) and on R13 a045b00ee (2 failed, 28 passed). At R13 the first reports `AttributeError: 'types.SimpleNamespace' object has no attribute 'kind'` at entries.py:1053 from a test stub; the R12 assertion text differs, so the stub should be rebuilt on the current entry contract | test-manager R12 run (/home/user/wt/agent-r12); Plan 20 workers via orchestrator, 14 Nov |
| `tests/stage1/test_docs_runtime_authority.py::test_live_docs_name_runtime_bootstrap_and_authority` fails on R12 main 0e1543e0 (local R12 run, 14 Nov: 1 failed, 2 passed) with the same assertion as on R13 a045b00ee: the README no longer contains the text `Set up Astrid →` linking to docs/getting-started.md; README banner commits of 9-10 Nov changed the text, the test was not updated. Stale test or README: decide which is right | test-manager R12 run (/home/user/wt/agent-r12); Plan 20 workers via orchestrator, 14 Nov |
| `tests/core/generation/test_engine_custody.py::test_two_full_h3_runtime_runs_reuse_owned_native_service[outer]` drives the retired action `astrid action h3_av.transform` (removed by 3079370d5, census 54 to 49) and imported helpers from a test module deleted by 218a46d53. It does not run on hosted CI, so it is latent, not red. Its assertions (same supervisor/child pids and start ticks, one service start, unchanged owner token and registry files, verified publication, two inference submissions) have no equivalent: `test_two_finite_h3_cpu_preflights_reuse_owned_native_service` covers finite preflights and `test_engine_runner.py::test_run_two_reuses_the_instance_run_one_left_running` a fake context. Rewrite it to `generate video --entry h3` (the separate finalizer task and transform receipt no longer exist), run on a machine with the CPU h3 install and ffmpeg. Cells' branch `r13/custody-test-helpers` d89e9fc5b only restores the helpers | test-manager run of the file on d89e9fc5b (triage/cust); cells ruling, 14 Nov |
| sfx has no installed-package proof: `test_installed_runpod_dry_run_per_default[sound-effects]` and `test_installed_sound_effects_auto_dry_run_resolves_foley` error in fixture setup on every base here (uv cannot download Python 3.11.13: `invalid peer certificate: UnknownIssuer`; the file estimates a 12 GB peak). Needs a runner with uv certificates and free disk; not a product failure | cells cards sfxinst, gold (03:07 Sat) |
| job-seam fixture: `test_controller_shipped_default_job_runs_on_the_real_local_path` is still red after three relaunches; the git-backed ComfyUI stand-in (Agent `r13/job-seam-fixture` 9d1a0cd66, cause engine_runner.py:557) reaches submission, then times out staging its input on a loaded 4-CPU box. Also needed by test_runpod_slot_path_cpu.py and test_workflow_file_placements_cpu.py (local-managed). Rerun alone on a quiet or hosted runner; share one fixture across the three files | cells card jobseam |
| Declared-input lists are pinned exactly in tests (`test_h3_declared_inputs_describe_and_resolve_without_execution`, the selected-h3 refusal cases), so every input-contract change (named exception: h3 declares the kind's plain inputs, 5fe9ed7a0; cells commits b65363d9e, 681a56edb) rewrites test lists by hand. Derive the expected list from the entry's own declaration (h3.yaml) and keep only the contract-level assertions (accepted/refused cases) pinned | cells card h3rows; test lane named exception |
| Fake-media fixtures built from unbounded lavfi sources and `-shortest` (the h3 composition fixture fixed at 16c338f55: observed 164 frames vs planned 108 on newer FFmpeg): grep the other fake-media helpers for infinite `color=`/`sine=` inputs and bound each with an explicit duration | cells card h3cov; evidence h3cov-diff |
| Tests mock model-reference records by hand (structural validation fixture needed the full `node_id`/`class_type`/`field` shape after e109c593b): build mocked references through the loader's own reference constructor so shape changes do not break fixtures (fixed narrowly at 1444896d0) | cells card nodeid |

## Outside pull requests (owner revisits; nothing closed)
| Item | Source |
|---|---|
| Agent #346 (owner's call), runpod-lifecycle #2, and five worker-permission PRs (Agent #312, Runtime #38, App #220, VibeComfy #164, lifecycle #4), after publish | evidence/open-prs.md; release-record.md:70 |
| App #158: re-raise after R13; App #130: design input later | evidence/open-prs.md |
| Tell the deferred outside contributors which release considers their PRs | release-record.md:70, 124 |

## Test infrastructure (Plan 39)
| Item | Source |
|---|---|
| Local disk fills in every lane: pytest scratch dirs and old worker worktrees and envs are never cleaned. It killed test-lane workers twice on Sat. Add a cleanup step to the worker env and a disk floor check before heavy proofs | advisor dive 6 |
| Tests that pass alone and time out on a loaded shard: d18 `test_concurrent_submission_during_child_wait` (harness wait raised 1 s → 10 s, f45f121ba), the music and tts receipt ids, the sfx slot-path cells. Root: wall-clock bounds in tests that assume an idle box | advisor dive 6; decisions.md 10:15 Sat |
| The hosted fast-checks job needed the VibeComfy, Runtime and lifecycle checkouts to collect tests (36 collection errors before fbeb3871a). One place should provision a test environment for every job, rather than per-job copies | decisions.md 08:45 Sat |

## Process (astrid-dev skills and ledger)
| Item | Source |
|---|---|
| Local disk fills in every lane, third occurrence (test lane at 91–97%; my disk guard killed live W1, costing $0.37). Root: prune old install homes, worktrees and envs at the START of every live round and every proof, as a script step, not by hand | advisor dive 7; decisions.md 17:52 Sat |
| The proxy blocks the installer's GitHub archive download of the Runtime (Plan 20 walk 1, b900c5bb). Worked around with local `repo` sources. Root: document the local-source route in the setup skill, or have the installer fall back to a git clone | advisor dive 7; decisions.md 17:52 Sat |
| Weekly limit: every session reports its seven-day warning state at check-ins; warn Hannah and cut model use at the first warning | decisions.md (02:05, 02:40 Sat) |
| When a lane ends, its rows get a named owner within the hour (the engine-fork gap) | advisor dive 4 |
| Managers farm hands-on work to Codex subagents; the advisor measures it each dive | decisions.md (02:50 Sat) |
