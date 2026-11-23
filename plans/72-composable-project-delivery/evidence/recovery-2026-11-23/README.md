# Plan 72 — release source-selection and recovery transfer packet (23 Nov 2026)

**Status:** Off-release prepared evidence. **NOT** permission to start, integrate, merge, dispatch RS1, or publish. [Release 15 run board on canonical main](https://github.com/banodoco/astrid-dev/blob/main/releases/15/run.md) still records Plan 72 **HOLD**. Older manager retirement remains unverified. This packet was prepared solely on isolated [draft #1624](https://github.com/banodoco/astrid-dev/pull/1624), and the original #1212 chain was not changed.

## Next action for the Release 15 Lead

The consolidated [HOLD-to-integration execution packet](14-release15-lift-hold-execution.md) is the **single entrypoint** for pending owner decisions, protection requirements, the generic parser/branch-table and Plan72 authored-record owners, source selection, CI proof and future RS1/landing sequence. It includes the latest observed CLI / missing-AA-001 / Plan72-membership controls and distinguishes real Release13 delivery paths from Plan72's proposed Release15 enabler membership. This packet **does not lift HOLD**.

## Fixed identities

| Purpose | Exact source |
| --- | --- |
| Source of the existing selected Plan 72 chain | [#1212](https://github.com/banodoco/astrid-dev/pull/1212) `f13a584a31cb1d29b335533563420e1de35e3481`, tree `879caa2cc4ce83b62231b9116a6770b1cfa8ef2f` |
| Preserved recovered production/test changes | `da72e8d14acdf4577ec076bab977e02e9bfc3703`, tree `a7c236b8358ccde20317b1c6a8311324411dd763` |
| Patch artifact carrying **only** these changes | [`08-source-boundaries.patch`](08-source-boundaries.patch), captured verbatim from #1624's four-file PR diff before this evidence directory was added |
| Patch storage commit | `7ae5badd03be81727e37eb878606a309c0c117b8` |
| Release 15 Astrid-dev source snapshot (recheck on authorized start) | `release/15/main=321523e52bddbbd13477634b05974a16b54b825b` |
| Release 15 Lead (canonical) | `session_011EzfW1gtAhRQwk8pgJMzhG` |

The patch has **4 file sections / 8 hunks / 13,240 UTF-8 characters**. Source-exact in-memory replay against #1212 found **one** matching old context for each existing-file hunk and reconstructed **all four latest blobs exactly**. This is evidence of source applicability **only**, not a native Git `apply --check` or combined Release 15 test.

| Patch target | Source at #1212 | After patch |
| --- | --- | --- |
| `scripts/project_delivery.py` | `8d87b913e25d4ca34230ee0eecc657825c8f51fa` | `7f5a9659540984c05137d2f39e8e4e4a2ad25b5a` |
| `scripts/test_project_delivery_root_identity.py` | absent | `d422377dcf2acf76668d286477eb2cc8b6614c84` |
| `scripts/test_project_delivery_source_containment.py` | absent | `ab74166974ce35a15431ba3d55a9c34620ae3040` |
| `scripts/test_project_delivery_source_directories.py` | absent | `e3ae8f85155c4d53c712a6dd0816fcbe8b89b3a7` |

The cumulative production delta is **33 added lines**, with no deletion or modification of existing tests. There are **three tests-first fixes**: noncanonical existing roots, escaped authored Markdown-file aliases, and escaped/dangling canonical source-directory aliases. They are bounded source correctness, not a change to Plan48/53's parser ownership or to public feed format.

## Gates and owner routing — no Lead GO claimed

The already recorded [Release 15 Lead handoff #1245](https://github.com/banodoco/astrid-dev/pull/1245) names the responsible Lead. The [specific new dependency request](https://github.com/banodoco/astrid-dev/pull/1245#issuecomment-7103252095) asks for **three** ownership decisions:

1. **Generic branch parser — Release/Plan48 owner:** release's `scripts/records.py` blob `b2b62e72396f200efd00bcebc7b1c95f0f3df92e` excludes `astrid-dev` branch rows, but canonical main and the current release brief use them. Name the owner who will reconcile generic `records.py` and original `test_check_docs.py`, preserving the existing negative checks. *Do not replace full shared files with the #1212/default-main blobs.*
2. **Canonical authored records — Lead + plan record owner:** frozen Release 15 source lacks the whole `plans/72-composable-project-delivery/` pack and its Included plans/branch-table records. The original `test_actual_repository_delivery_traversal` must remain active and cannot pass as authentic release evidence without those authored sources. Select the canonical pack and record membership **only after** an authorized scope/Lead decision; never fabricate a successful traversal.
3. **Protection — owner/admin:** at the latest read (23 Nov), `release/15/main` had `protected:false` in Astrid-dev, Agent, Runtime, App and VibeComfy; active repo rulesets only protect default `main` in Astrid-dev. Record actual release-main ruleset IDs and read-back of non-delete/non-force, required checks, up-to-date and landing reference policy before any integration.

Also pending: owner `Scope decision` and `Challenge` acceptance in `inputs.md`; exclusive release integration writer/cut SHA; Plan53 Goals [draft #1059](https://github.com/banodoco/astrid-dev/pull/1059) source ownership; the `docs/extending.md` PD10 hunk conflict; a genuine integrated pre-RS1 review-stop candidate. The already named Lead—not this independent source branch—controls release branch cutting and landing. Historical review counters remain UNKNOWN; **no RS1, final R or project-wide Astra check has been dispatched**.

## Order to execute only after the Lead gate

1. Verify release branch's then-live source SHA, branch protections, one writer, accepted scope, recorded authored plan/release records and parser owner. Keep the isolated #1624 candidate immutable. Use a new *authorized* release-plan worktree/branch; never reuse the historical #1212 branch as the release base.
2. Replay the original [13-path source-selection preflight](https://chatgpt.com/space/page_e538b159d6d08191b1175bcb877474f1), **not** its unbounded ancestry: 01 typed core (#1074), 02 adapters (#1076), 03 RED regression tests (#1199), 04 GREEN guards (#1201) and 05 source ownership (#1212). Check each patch's exact donor SHA, path list, `git apply --check` and original focused tests. Do not cherry-pick the #1161 composition merge or newer `main`. Preserve the Release15 `records.py`/test-check-docs generic differences.
3. **Only after 01–05 have reconstructed the expected #1212 source-owned code**, retrieve this stored `08-source-boundaries.patch` by its exact blob/commit, verify it contains the four paths above, and apply it in the authorized worktree:
   ```sh
   # From the authorized working tree; an operator chooses the temporary path.
   git show 7ae5badd03be81727e37eb878606a309c0c117b8:plans/72-composable-project-delivery/evidence/recovery-2026-11-23/08-source-boundaries.patch > /tmp/plan72-08.patch
   git apply --check /tmp/plan72-08.patch
   git apply /tmp/plan72-08.patch
   git diff --check
   ```
   **If the file, Git object, base blob, exact checks, or hunk contexts are absent or different, BLOCK.** This cannot be treated as an independent release authorization. Do not copy the evidence directory itself into production code.
4. Prove the original source identities and all previously failing controls:
   ```sh
   for test in test_relationships.py test_project_contract.py test_records.py \
      test_check_docs.py test_project_delivery.py \
      test_project_delivery_critique_regressions.py test_project_source_ownership.py \
      test_project_delivery_root_identity.py test_project_delivery_source_containment.py \
      test_project_delivery_source_directories.py; do
     python3 -m unittest discover -s scripts -p "$test" || exit 1
   done
   python3 -m unittest discover -s scripts -p 'test_*.py'
   python3 scripts/astrid_dev.py check
   python3 scripts/astrid_dev.py sync
   python3 scripts/astrid_dev.py check
   git diff --check
   ```
   Use the repository's native CI, not an ad hoc selective `-k` omission, to prove generated views, original goldens and App `vision-consumer-contract` on the **actual combined tree**. Capture failed IDs with baseline/source context.
5. Separately prove the **Goal → Gap → Project → recorded Release** query, **locally frozen Issue → Release** query, and **same-authored-input fixed-revision public-feed byte parity**. Original #1212 or #1624 source-only green CI cannot substitute for integrated Release 15 proof. `test_project_delivery_parity.py` may be carried as a *test*, but PD8 acceptance and the PD10 guide are after RS1. Never skip, weaken, xfail or delete original tests to manufacture a pass.
6. Obtain an independent formal RS1 verdict at the actual authorized review stop, then execute approved downstream PD6–PD11 and final R. No Lead GO, no integration and no promotion have occurred in this recovery packet.

## Parser and authored-record ownership packet (23 November 2026)

The old Release15 generic branch parser and the new canonical authored records need **one Lead-owned migration**, not a Plan72-only `records.py` replacement. The frozen release brief lists Plans **39/50/40** with **zero plan rows**; the current stricter branch parser would reject all three until the Lead reconciles every included-plan row. Plan72 itself is a **Foundational enabler**, not a goal-gap delivery project.

The [two-file five-hunk generic compatibility patch](09-release15-branch-parser-compat.patch) is pinned to frozen Release15 `records.py` and `test_check_docs.py`, and strict in-memory replay reconstructs the canonical main versions byte-for-byte. **Do not apply it independently of the release-owned authored records and branch-table migration.** The [exact authored-record inventory and integration gate](10-release15-authored-records.md) pins Plan72's canonical three source blobs and the necessary owner/test sequence, including preservation of Plan72's gapless enabler semantics. Six new fixture-based `test_project_delivery_release15_seam.py` tests rehearse the source branch semantics but do **not** claim a release branch cut or combined CI.

## Native source-only receipts (not release qualification)

| Stage | Tests-first RED | Repaired hosted GREEN |
| --- | --- | --- |
| Invalid existing `--root` | [45159473732](https://github.com/banodoco/astrid-dev/actions/runs/45159473732), 498 tests, 3 expected failures | [45160066026](https://github.com/banodoco/astrid-dev/actions/runs/45160066026), 498/498 + App 13/13 |
| External authored Markdown symlink | [45172655840](https://github.com/banodoco/astrid-dev/actions/runs/45172655840), 503 tests, 4 expected failures | [45172983134](https://github.com/banodoco/astrid-dev/actions/runs/45172983134), 503/503 + App 13/13 |
| External/dangling source directory | [45178015895](https://github.com/banodoco/astrid-dev/actions/runs/45178015895), 512 tests, 8 expected failures | [45178363963](https://github.com/banodoco/astrid-dev/actions/runs/45178363963), 512/512 + App 13/13 |

The later same-head [post-description run 45178874971](https://github.com/banodoco/astrid-dev/actions/runs/45178874971) also passed 512/512, checks/views and App 13/13 on `da72e8d1` before this evidence artifact was added.

**Limits:** This packet's in-memory replay is **not** a native scratch worktree or `git apply` run. No local Astrid-dev checkout was available to this Chat session. Hosted CI is the actual Python/App execution evidence; actual Release15 combined CI and later gate receipts are still required.
