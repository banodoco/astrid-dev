# Release 14 publication checklist — R14-PUB-1 (PREPARATION, NOT A GO)

**Owner:** Release 14 Lead (`r14-lead`); packet author: `r14-PUB-1-1`.
**Status:** BLOCKED for final qualification until the combined tuple is frozen, FIX-15/16/17/18 and Plans 59/64/65 are integrated and reviewed. This checklist is not permission to run paid work, dispatch workflows, promote or publish.
**Authority:** [R14 run board](../run.md#authority), [publication rule](../../14.md#publication), [R14-PUB-1 packet](../packets/R14-PUB-1.md).
**Superseding owner decisions:** [combined Plans 59/64/65 into R14](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7063263106), [owner runs real Windows update/local generation](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7063270699). The two-re-pin arrangement in [older Lead message](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7062896674) is superseded.

## A. Immutable reference: published Release 13

These are **two distinct Agent identities**, not interchangeable:

| Role | Published R13 source |
|---|---|
| Agent `main` used for source/CI baseline | `959da7326c982a9197b5d6e2a4489f45e1deef0e` |
| App deployed code / published baseline | `de7dd1e668aa6dcf3cbce013c701fa7c76615f99` |
| Agent installed by published App manifest | `9814193a73f606719e81883a8be197d27dd361d4` |
| Runtime installed by published App manifest | `6855dfa8df65cf8ae4c002b57134d6505493c17c` |
| VibeComfy installed by published App manifest | `dba38f8644c46f652376f2cd5112ea161e40f09b` |
| Runtime schema | `sha256:9628bb5fd6e1dbbec392dd39f2e01031622dcf52d7ccff7cd1f0ad10743dcb1c` |
| Required installer release | `14` (required update; [owner decision](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7065093369)) |

[Immutable R13 manifest](https://github.com/banodoco/astrid-app/blob/de7dd1e668aa6dcf3cbce013c701fa7c76615f99/public/install-manifest.json). A served-manifest canary on the R13 App SHA [succeeded](https://github.com/banodoco/astrid-app/actions/runs/44891402290) on 21 Nov; preserve actual served bytes, the Railway deployment ID and its restoration capability in the [rollback runbook](../rollback.md) **before** the R14 production deployment.

## B. Input runs and provisional, unqualified observation

The current comparison is **not the frozen candidate**. It is a diagnostic snapshot on Agent `release/14/main` `0020c2e8d7f5d6051db2964a235b97f4ba002a72` and App `release/14/main` `e6ca6e8032fcb2e6ab42cb713bb5047ae023f2e4`. Both predate the combined integration and final App re-pin. Do not reuse their verdict at publication.

| Repository / workflow | Published R13 run | Provisional R14 run | Coverage / observation |
|---|---|---|---|
| Agent CI, eight unit shards | [43760673752](https://github.com/banodoco/astrid-agent/actions/runs/43760673752) | [44651391760](https://github.com/banodoco/astrid-agent/actions/runs/44651391760) | All eight shard jobs ran; both aggregate runs red. R13 `fast checks` **success**, provisional R14 `fast checks` **failure**, a job-level regression needing full diagnosis. |
| Agent Lanes, four integration shards | [43760673730](https://github.com/banodoco/astrid-agent/actions/runs/43760673730) | [44651391728](https://github.com/banodoco/astrid-agent/actions/runs/44651391728) | All four integration jobs red on both; compare exact IDs, not just exits. |
| App Tests / Vitest | [43860030897](https://github.com/banodoco/astrid-app/actions/runs/43860030897) | [44639404891](https://github.com/banodoco/astrid-app/actions/runs/44639404891) | Vitest jobs success on both. **Not per-ID proof:** logs primarily give file counts (`1433` versus `1441` passing files); require complete per-assertion JSON/JUnit reports on the exact SHAs. |
| App Lanes / journeys | [43860030963](https://github.com/banodoco/astrid-app/actions/runs/43860030963) | [44639404982](https://github.com/banodoco/astrid-app/actions/runs/44639404982) | `quick-journey` and `checkout-lanes` fail on both; inspect each Playwright ID and first boundary. |
| App Direct Journey | [44078954757](https://github.com/banodoco/astrid-app/actions/runs/44078954757) | **No run on `e6ca6e80`** | Published baseline passes `direct-journey` and `three-products`; candidate coverage unknown until Lead dispatch. |
| App E2E | [43860030918](https://github.com/banodoco/astrid-app/actions/runs/43860030918) | [44639404948](https://github.com/banodoco/astrid-app/actions/runs/44639404948) | Job and test-ID reconciliation required; aggregate red does not establish same IDs. |

**Known source-verified differences, for explanation rather than acceptance:**

| Exact ID / job | R13 | Provisional R14 | Disposition needed |
|---|---|---|---|
| `tests/packs/rendering/test_hyperframes_backend.py::test_hyperframes_real_media_render_through_public_service` | PASS | FAIL | FIX-18, reproduce both pinned states and inspect media-render child diagnostics |
| `tests/packs/rendering/test_hyperframes_backend.py::test_hyperframes_real_render_through_public_service` | PASS | FAIL | FIX-18, inspect text-render child diagnostics |
| `tests/sdk/test_timeline_film_length.py::test_a_layer_longer_than_its_middle_shot_blocks_check` | PASS | FAIL | FIX-18, six-second layer in four-second shot |
| `tests/test_pinokio_platform_adapter.py::test_real_external_process_can_be_adopted_without_substitute_launch` | PASS | FAIL | FIX-18, adopted PID/listener ownership |
| Agent `fast checks` CI job | success | failure | Full job-level outcome has changed; determine original failing step, compare latest frozen run |
| App `release-guard` Tests job | success | skipped | Not a passing candidate proof; verify whether intentional gating or lost coverage |
| App Vitest individual IDs | uncollected from default log | uncollected from default log | Must regenerate native reporter output; totals are insufficient |
| App Direct Journey | PASS on published baseline run | **not run at provisional head** | Lead dispatches on frozen tuple |

FIX-18's [exact four-ID task](../packets/R14-FIX-18.md) owns their cause/disposition; no packet here changes those tests. The initial eight-shard pytest log review also observed other pass-to-fail and missing IDs on the provisional Agent comparison (including H3, readiness, duplicate and installer cases). **They are not silently waived.** [Provisional Agent native-ID ledger](publication-preflight-agent-20261121.md) records 21 PASS→FAIL and 432 PASS→missing/skip in eight CI shards, plus four PASS→FAIL and two PASS→missing/skip in four Lanes shards on the **non-final** R14 head. Those per-job counts are not distinct cross-job union IDs, and no root causes/renames are presumed. [Provisional App journey ledger](publication-preflight-app-20261121.md) establishes that the existing dot-reporter logs have **zero extractable complete test-ID streams**; this is **unknown coverage**, not zero regression. The complete frozen comparison must enumerate and disposition *every* ID, including R13-only, skipped, renamed, newly failing and unknown outcomes.

## C. Reproducible final diff procedure (Lead dispatches workflows)

1. Freeze and record **all full 40-character SHAs**: Agent, Runtime, VibeComfy, App, pinned lifecycle, Runtime schema digest, served manifest bytes/digest. Confirm Agent's `runtime.lock.json` and `astrid/packs/runpod/pins.json` agree with App manifest, and Plans 59/64/65/FIX-15/16/17/18 qualify in the intended merge order.
2. Obtain Agent CI and Lanes, App Tests, Lanes, Direct Journey and E2E, Runtime CI and VibeComfy `ci` on the recorded R13 and frozen R14 SHAs. Use full native Vitest JUnit or JSON with the same format on both App SHAs. Obtain native Vitest JSON for the checkout lane and native Playwright JSON for each journey and E2E job. Keep the original selectors and assertions. Record the run, job, attempt, source SHA and artifact or command for each supplied report. The **latest attempt** of each workflow must be complete and pinned explicitly in `attempts`. The template records R13 attempt 1 from the rehearsal.
3. Copy [publication-diff-inputs.json](publication-diff-inputs.json) to `$R14_FREEZE_DIR/inputs.json` and fill in the candidate SHAs, workflow run IDs and attempts. Provide `native_reports` provenance bindings keyed by `SIDE/app/WORKFLOW/JOB`. Bind either Vitest JSON or JUnit to `SIDE/app/Tests/vitest`; bind native Vitest JSON from the App `Lanes/checkout-lanes` job to `SIDE/app/Lanes/checkout-lanes`. That checkout job is validated as Vitest format. Other known journey and E2E native jobs remain validated as Playwright format. Each entry has `type` (`artifact` or `local`), `run_id`, `attempt`, `sha` and `sha256` (hex SHA-256 of the report bytes). Artifact entries also require `artifact_id` and the exact ZIP `member`. The comparator verifies the run, the pinned job's time window, the GitHub archive digest and the report digest. A local entry needs an owner-approved `local_evidence_exceptions` entry under the same key with matching `run_id`, `attempt`, `sha` and `sha256` and a nonempty `approve_reason`. The verdict lists local evidence under **LOCAL-EVIDENCE**.

   For a failed job without IDs, record its `setup_failure_ok` exception. Other jobs without IDs in a test workflow require `no_ids_expected`. Both maps use exact `SIDE/PRODUCT/WORKFLOW/JOB` keys and nonempty reason strings. A failed candidate job needs a matching R13 job failure and a separate `[job]` entry in the approved inventory. A candidate failed step absent from the R13 counterpart requires a `failed_step_exceptions` entry with exact `candidate/PRODUCT/WORKFLOW/JOB/STEP` key and a nonempty reason. Provide a reason and source for each documented rename in `job_renames` and `test_id_renames` using `{"to":"new stable ID","reason":"verified cause","source":"PR, run, or source permalink"}`. Save Playwright inputs in `$R14_FREEZE_DIR/playwright.json` as a JSON object mapping each `SIDE/WORKFLOW/JOB` to its report path. Use `baseline` and `candidate` sides and exact job names.
4. From an astrid-dev checkout, export read-only `GH_TOKEN` or `GITHUB_TOKEN` and set `R14_FREEZE_DIR` to the directory containing the final inputs. Non-rehearsal publication comparisons require `--inherited-base` naming an ancestor commit with the committed `releases/14/evidence/inherited-red.json` current list. A manifest-only externally sealed digest does not qualify this CLI run.

   ```bash
   timeout 1200s python3 releases/14/evidence/publication_diff.py \
     --manifest "${R14_FREEZE_DIR:?}/inputs.json" \
     --inherited-red "$R14_FREEZE_DIR/inherited-red.json" \
     --inherited-base "$INHERITED_BASE_COMMIT" \
     --out "$R14_FREEZE_DIR/verdict" \
     --junit-xml-r13 "$R14_FREEZE_DIR/r13-vitest.xml" \
     --junit-xml-r14 "$R14_FREEZE_DIR/r14-vitest.xml" \
     --playwright-inputs "$R14_FREEZE_DIR/playwright.json"
   ```

   `--inherited-base` is required for this non-rehearsal command; omitting it is refused before records are collected. Rehearsals using `--rehearsal-records` may omit it. The `--playwright-inputs` mapping accepts job-specific native JSON paths: use Playwright for the known journey/E2E jobs and Vitest JSON for `baseline/Lanes/checkout-lanes` and `candidate/Lanes/checkout-lanes`; each must also have the matching `native_reports` provenance binding above.
5. For review, add `--generate-candidate-list "$R14_FREEZE_DIR/proposed-inherited-red.json"` to record the observed candidate reds with R13 statuses and job identities. The Lead and owner approve the inventory separately. Each reviewed entry has `repo`, `workflow`, `job`, `id` and optional `count` (default 1). Use `[job]` for a job-level failure. Keep only entries whose exact identities are still red on both sides. The Lead uses `--allow-growth` once for the owner-approved initial inventory. The verdict records the override and checks exact R13 evidence for every approval.
6. Preserve verdict outputs in the astrid-dev evidence lane. `report.md` and `counts.json` give by-repo totals, `r14-only.md` lists each added red by job, and `all-test-ids.csv`, `jobs.csv` and `resolved-runs.json` retain run and attempt binding. Verify `native-report-input-digests.json` and `playwright-expected-actual.json` against the original command or artifact; the latter retains Playwright expected/actual/retry detail and records native Vitest occurrence outcomes for checkout. The canonical `env/baseline-diff.py` outputs provide an additional Agent diagnostic. A nonzero exit leaves the publication diff unqualified. Treat XPASS as changed, and PASS→XFAIL as red. No proposal approves a red or changed result.
7. Lead compares the same frozen candidate to current product `main` using the [release skill](../../../agent/shared/workstreams/release.md#promote-or-publish), respects the sealed Plan 39 ceiling for inherited red IDs, and records each non-test job that changed from success to failure. Preserve the original tests, selectors and expectations.

**Final diff:** [ ] exact tuple frozen; [ ] every workflow pinned to latest completed attempt; [ ] eight Agent unit jobs; [ ] four Agent lanes; [ ] complete App Vitest assertion IDs; [ ] full App journey IDs; [ ] job-name comparison; [ ] omissions/renames explained; [ ] no unexplained pass→fail, XPASS change, or PASS→XFAIL; [ ] Lead review and verdict.

The provisional 434-ID investigation is in [the breakdown](publication-preflight-agent-breakdown.md); changed tests remain open for Lead review.

## D. One rented generation — Lead-owned, not executed in this packet

**State:** Not run. No RunPod credential, balance, existing-pod census, paid job ID, result or teardown is asserted here. The Lead alone spends under the owner's delegated budget and reports it. The integration host's separate proposed **$30** live-case budget [awaits express owner confirmation](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7063263106); it is not fungible with the Lead's **$10** delegated GPU cap.

**Before any paid command:** verify exact frozen Agent/Runtime/VibeComfy/lifecycle pins, source worktree and installed tuple; use `astrid generate defaults --json` to choose the smallest **supported image entry** (do not assume an entry ID); verify the currently supported command flags using `astrid generate image --help`; verify credentials and account access with a non-paid check, recording the result without secrets; check RunPod account balance and remaining approved budget **privately**; obtain a full account pod census via `astrid machines`/pinned lifecycle. If any foreign pods exist, leave them alone and stop. Set a conservative absolute `--max-usd` so *worst-case* preparation, execution and teardown fit remaining allowance. Require explicit paid consent and named limit; no raw RunPod API/SDK.

For the Lead to instantiate after those checks (parameters intentionally unresolved; one `--gpu` flag):

```bash
astrid generate image --entry "$SUPPORTED_IMAGE_ENTRY" --placement runpod \
  --gpu "RTX 4090" --max-hourly-usd "$APPROVED_HOURLY_CAP" \
  --max-usd "$SAFE_JOB_CAP" --preparation-seconds "$PREP_LIMIT" \
  --execution-seconds "$EXEC_LIMIT" --idle-seconds "$IDLE_LIMIT" --consent paid
```

**Receipt to fill from real evidence only:**

| Required field | Value |
|---|---|
| Frozen App/Agent/Runtime/VibeComfy/lifecycle SHAs; schema digest; manifest digest | **PENDING** |
| Run owner, authorization link, spend ceiling, balance before | **PENDING** |
| Credential and account access check (no secrets) | **PENDING** |
| Full census before (all pod IDs/states, including foreign pods) | **PENDING** |
| Chosen supported image entry, GPU and verified command | **PENDING** |
| Job ID, generated output URI + digest, output viewed/usable | **PENDING** |
| First failure reason, if any; receipt path and cleanup | **PENDING** |
| Stop/terminate acknowledgements and full account pod census after | **PENDING** |
| Balance after, measured spend and ledger, remaining cap | **PENDING** |

A usable image **and a full empty account pod census after teardown** are necessary. If foreign pods exist, leave them alone and stop; do not pass the receipt. If custody is uncertain, release owned resources and mark **BLOCKED**; do not call a wrapper success sufficient.

## E. Other publication gates and owner handoff

- [ ] FIX-15 Agent #457 lands; combined Plans 59/64/65 integrate with full CI and independent review, then Agent/Runtime/VibeComfy and App merge with final re-pin; R14 reopening of R13-written realms is explicitly qualified.
- [ ] FIX-17 update rows pass on Windows, macOS and Linux; the R13 App shows the required-update prompt and drafts survive update; an R14 install reopens R13-written realms with timelines, history and save queue. Retain the killed Windows update row and two same-day passes on frozen SHAs.
- [ ] Owner's **real Release 13 Windows install**: update, edit, save, reopen, one local generate, cancel and retry, with original data retained. [Owner accepted this work](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7063270699). Lead provides frozen tester build and script, not this packet.
- [ ] Lead's one rented image generation and complete budget/census receipt (above).
- [ ] Exact last-good R13 Railway deployment ID, immutable manifest bytes, rollback/redeploy permission and rehearsable procedure from [rollback.md](../rollback.md).
- [ ] [Draft release notes](../notes.md) reviewed for actual landed fixes and truthful known red ceiling.
- [ ] Branches/gates/checks complete, owner explicitly approves the **exact frozen tuple** in the publisher's session. Product main promotion Agent → Runtime → App (App last), production deploy, then the [served-manifest canary](https://astrid.haus/install-manifest.json) proves exact frozen SHAs. **Packet writer never merges or publishes.**

**Release cannot publish while any required box remains unchecked.** Keep diagnostic failures in their original reports; no count-only “green”, backdated evidence or paid spend inferred.
