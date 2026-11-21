# Release 14 publication checklist — R14-PUB-1 (PREPARATION, NOT A GO)

**Owner:** Release 14 Lead (\`r14-lead\`); packet author: \`r14-PUB-1-1\`.
**Status:** BLOCKED for final qualification until the combined tuple is frozen, FIX-15/16/17/18 and Plans 59/64/65 are integrated and reviewed. This checklist is not permission to run paid work, dispatch workflows, promote or publish.
**Authority:** [R14 run board](../run.md#authority), [publication rule](../../14.md#publication), [R14-PUB-1 packet](../packets/R14-PUB-1.md).
**Superseding owner decisions:** [combined Plans 59/64/65 into R14](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7063263106), [owner runs real Windows update/local generation](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7063270699). The two-re-pin arrangement in [older Lead message](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7062896674) is superseded.

## A. Immutable reference: published Release 13

These are **two distinct Agent identities**, not interchangeable:

| Role | Published R13 source |
|---|---|
| Agent \`main\` used for source/CI baseline | \`959da7326c982a9197b5d6e2a4489f45e1deef0e\` |
| App deployed code / published baseline | \`de7dd1e668aa6dcf3cbce013c701fa7c76615f99\` |
| Agent installed by published App manifest | \`9814193a73f606719e81883a8be197d27dd361d4\` |
| Runtime installed by published App manifest | \`6855dfa8df65cf8ae4c002b57134d6505493c17c\` |
| VibeComfy installed by published App manifest | \`dba38f8644c46f652376f2cd5112ea161e40f09b\` |
| Runtime schema | \`sha256:9628bb5fd6e1dbbec392dd39f2e01031622dcf52d7ccff7cd1f0ad10743dcb1c\` |
| Required installer release | \`13\` (do not raise on R14; R14 is opt-in) |

[Immutable R13 manifest](https://github.com/banodoco/astrid-app/blob/de7dd1e668aa6dcf3cbce013c701fa7c76615f99/public/install-manifest.json). A served-manifest canary on the R13 App SHA [succeeded](https://github.com/banodoco/astrid-app/actions/runs/44891402290) on 21 Nov; preserve actual served bytes, the Railway deployment ID and its restoration capability in the [rollback runbook](../rollback.md) **before** the R14 production deployment.

## B. Input runs and provisional, unqualified observation

The current comparison is **not the frozen candidate**. It is a diagnostic snapshot on Agent \`release/14/main\` \`0020c2e8d7f5d6051db2964a235b97f4ba002a72\` and App \`release/14/main\` \`e6ca6e8032fcb2e6ab42cb713bb5047ae023f2e4\`. Both predate the combined integration and final App re-pin. Do not reuse their verdict at publication.

| Repository / workflow | Published R13 run | Provisional R14 run | Coverage / observation |
|---|---|---|---|
| Agent CI, eight unit shards | [43760673752](https://github.com/banodoco/astrid-agent/actions/runs/43760673752) | [44651391760](https://github.com/banodoco/astrid-agent/actions/runs/44651391760) | All eight shard jobs ran; both aggregate runs red. R13 \`fast checks\` **success**, provisional R14 \`fast checks\` **failure**, a job-level regression needing full diagnosis. |
| Agent Lanes, four integration shards | [43760673730](https://github.com/banodoco/astrid-agent/actions/runs/43760673730) | [44651391728](https://github.com/banodoco/astrid-agent/actions/runs/44651391728) | All four integration jobs red on both; compare exact IDs, not just exits. |
| App Tests / Vitest | [43860030897](https://github.com/banodoco/astrid-app/actions/runs/43860030897) | [44639404891](https://github.com/banodoco/astrid-app/actions/runs/44639404891) | Vitest jobs success on both. **Not per-ID proof:** logs primarily give file counts (\`1433\` versus \`1441\` passing files); require complete per-assertion JSON/JUnit reports on the exact SHAs. |
| App Lanes / journeys | [43860030963](https://github.com/banodoco/astrid-app/actions/runs/43860030963) | [44639404982](https://github.com/banodoco/astrid-app/actions/runs/44639404982) | \`quick-journey\` and \`checkout-lanes\` fail on both; inspect each Playwright ID and first boundary. |
| App Direct Journey | [44078954757](https://github.com/banodoco/astrid-app/actions/runs/44078954757) | **No run on \`e6ca6e80\`** | Published baseline passes \`direct-journey\` and \`three-products\`; candidate coverage unknown until Lead dispatch. |
| App E2E | [43860030918](https://github.com/banodoco/astrid-app/actions/runs/43860030918) | [44639404948](https://github.com/banodoco/astrid-app/actions/runs/44639404948) | Job and test-ID reconciliation required; aggregate red does not establish same IDs. |

**Known source-verified differences, for explanation rather than acceptance:**

| Exact ID / job | R13 | Provisional R14 | Disposition needed |
|---|---|---|---|
| \`tests/packs/rendering/test_hyperframes_backend.py::test_hyperframes_real_media_render_through_public_service\` | PASS | FAIL | FIX-18, reproduce both pinned states and inspect media-render child diagnostics |
| \`tests/packs/rendering/test_hyperframes_backend.py::test_hyperframes_real_render_through_public_service\` | PASS | FAIL | FIX-18, inspect text-render child diagnostics |
| \`tests/sdk/test_timeline_film_length.py::test_a_layer_longer_than_its_middle_shot_blocks_check\` | PASS | FAIL | FIX-18, six-second layer in four-second shot |
| \`tests/test_pinokio_platform_adapter.py::test_real_external_process_can_be_adopted_without_substitute_launch\` | PASS | FAIL | FIX-18, adopted PID/listener ownership |
| Agent \`fast checks\` CI job | success | failure | Full job-level outcome has changed; determine original failing step, compare latest frozen run |
| App \`release-guard\` Tests job | success | skipped | Not a passing candidate proof; verify whether intentional gating or lost coverage |
| App Vitest individual IDs | uncollected from default log | uncollected from default log | Must regenerate native reporter output; totals are insufficient |
| App Direct Journey | PASS on published baseline run | **not run at provisional head** | Lead dispatches on frozen tuple |

FIX-18's [exact four-ID task](../packets/R14-FIX-18.md) owns their cause/disposition; no packet here changes those tests. The initial eight-shard pytest log review also observed other pass-to-fail and missing IDs on the provisional Agent comparison (including H3, readiness, duplicate and installer cases). **They are not silently waived.** The complete frozen comparison must enumerate and disposition *every* such ID, including R13-only, skipped, renamed, newly failing and unknown outcomes.

## C. Reproducible final diff procedure (Lead dispatches workflows)

1. Freeze and record **all full 40-character SHAs**: Agent, Runtime, VibeComfy, App, pinned lifecycle, Runtime schema digest, served manifest bytes/digest. Confirm Agent's \`runtime.lock.json\` and \`astrid/packs/runpod/pins.json\` agree with App manifest, and Plans 59/64/65/FIX-15/16/17/18 qualify in the intended merge order.
2. Obtain complete CI, Agent Lanes, App Tests (Vitest per-ID), App Lanes, App Direct Journey and App E2E on exact R13 and frozen candidate source SHAs. The R13 App Vitest log lacks assertion IDs, so the Lead must obtain a native \`vitest --reporter=json --outputFile=...\` (or equivalent unaltered native assertion-level artifact) on \`de7dd1e6\`, plus the same form on the frozen App SHA. Do not alter or skip a test to make collection green.
3. Populate the \`candidate\` SHA and workflow run IDs in [publication-diff-inputs.json](publication-diff-inputs.json) **only after actual runs**. If a workflow is retried, name the exact attempt; do not splice attempt-one results into attempt-two job identities. Explicitly map only verified job/test renames, with provenance.
4. From a checkout of astrid-dev, with read-only GitHub API credentials and **no dispatch**:

   \`\`\`bash
   GH_TOKEN="$READ_ONLY_GITHUB_TOKEN" python3 releases/14/evidence/publication_diff.py \
     --manifest releases/14/evidence/publication-diff-inputs.json \
     --out /tmp/r14-publication-diff \
     --vitest-json-r13 /path/to/r13-vitest-json \
     --vitest-json-r14 /path/to/r14-vitest-json
   \`\`\`

5. Preserve \`report.md\`, \`jobs.csv\`, \`all-test-ids.csv\`, \`resolved-runs.json\` and the canonical \`env/baseline-diff.py\` outputs under the **astrid-dev evidence lane** (the Leader must decide what becomes committed versus linked GitHub artifact; no evidence in products). Every R13 PASS→candidate FAIL/ERROR/SKIP/MISSING, missing job, newly failing ID, rename, and incomplete ID stream needs an explicit cause and source. A green total with fewer IDs is not a pass. If the script returns nonzero, the publication diff is unqualified.
6. Lead compares the same frozen candidate to current product \`main\` using the [release skill](../../../skills/shared/workstreams/astrid-dev-release/SKILL.md#promote-or-publish), respects the sealed Plan 39 ceiling for inherited red IDs, and records each non-test job that changed from success to failure. No test deletion, deselection or loosened expectation.

**Final diff:** [ ] exact tuple frozen; [ ] eight Agent unit jobs; [ ] four Agent lanes; [ ] complete App Vitest assertion IDs; [ ] full App journey IDs; [ ] job-name comparison; [ ] omissions/renames explained; [ ] no unexplained pass→fail; [ ] Lead review and verdict.

## D. One rented generation — Lead-owned, not executed in this packet

**State:** Not run. No RunPod credential, balance, existing-pod census, paid job ID, result or teardown is asserted here. The Lead alone spends under the owner's delegated budget and reports it. The integration host's separate proposed **$30** live-case budget [awaits express owner confirmation](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7063263106); it is not fungible with the Lead's **$10** delegated GPU cap.

**Before any paid command:** verify exact frozen Agent/Runtime/VibeComfy/lifecycle pins, source worktree and installed tuple; use \`astrid generate defaults --json\` to choose the smallest **supported image entry** (do not assume an entry ID); verify the currently supported command flags using \`astrid generate image --help\`; check RunPod account balance and remaining approved budget **privately**; inspect pod census via \`astrid machines\`/pinned lifecycle; preserve all pre-existing pods and IDs. Set a conservative absolute \`--max-usd\` so *worst-case* preparation, execution and teardown fit remaining allowance. Require explicit paid consent and named limit; no raw RunPod API/SDK.

For the Lead to instantiate after those checks (parameters intentionally unresolved; one \`--gpu\` flag):

\`\`\`bash
astrid generate image --entry "$SUPPORTED_IMAGE_ENTRY" --placement runpod \
  --gpu "RTX 4090" --max-hourly-usd "$APPROVED_HOURLY_CAP" \
  --max-usd "$SAFE_JOB_CAP" --preparation-seconds "$PREP_LIMIT" \
  --execution-seconds "$EXEC_LIMIT" --idle-seconds "$IDLE_LIMIT" --consent paid
\`\`\`

**Receipt to fill from real evidence only:**

| Required field | Value |
|---|---|
| Frozen App/Agent/Runtime/VibeComfy/lifecycle SHAs; schema digest; manifest digest | **PENDING** |
| Run owner, authorization link, spend ceiling, balance before | **PENDING** |
| Census before (all pod IDs/states, including foreign pods) | **PENDING** |
| Chosen supported image entry, GPU and verified command | **PENDING** |
| Job ID, generated output URI + digest, output viewed/usable | **PENDING** |
| First failure reason, if any; receipt path and cleanup | **PENDING** |
| Stop/terminate acknowledgements and own-pod census after | **PENDING** |
| Balance after, measured spend and ledger, remaining cap | **PENDING** |

A usable image **and** zero pods owned by this run after teardown are necessary. If custody is uncertain, release owned resources and mark **BLOCKED**; do not call a wrapper success sufficient.

## E. Other publication gates and owner handoff

- [ ] FIX-15 Agent #457 lands; combined Plans 59/64/65 integrate with full CI and independent review, then Agent/Runtime/VibeComfy and App merge with final re-pin; schema backward compatibility is explicitly qualified.
- [ ] FIX-17 R13→R14 installed update and both **mixed-version** rows pass **twice the same day** on frozen SHAs. Include killed Windows update, all three OS fresh/update/save/reopen, R14 App+R13 install, R13 App+R14-written realm.
- [ ] Owner's **real Release 13 Windows install**: update, edit, save, reopen, one local generate, cancel and retry, with original data retained. [Owner accepted this work](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7063270699). Lead provides frozen tester build and script, not this packet.
- [ ] Lead's one rented image generation and complete budget/census receipt (above).
- [ ] Exact last-good R13 Railway deployment ID, immutable manifest bytes, rollback/redeploy permission and rehearsable procedure from [rollback.md](../rollback.md).
- [ ] [Draft release notes](../notes.md) reviewed for actual landed fixes and truthful known red ceiling.
- [ ] Branches/gates/checks complete, owner explicitly approves the **exact frozen tuple** in the publisher's session. Product main promotion Agent → Runtime → App (App last), production deploy, then the [served-manifest canary](https://astrid.haus/install-manifest.json) proves exact frozen SHAs. **Packet writer never merges or publishes.**

**Release cannot publish while any required box remains unchecked.** Keep diagnostic failures in their original reports; no count-only “green”, backdated evidence or paid spend inferred.
