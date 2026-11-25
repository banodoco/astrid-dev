# Release 15 — parser compatibility and Plan 72 authored-record seam

**PREPARED ONLY · Release 15 HOLD · no integration or review authorization.** The owner delegated **isolated pre-RS1 preparation** on [draft #1624](https://github.com/banodoco/astrid-dev/pull/1624). The previous manager's retirement remains unverified. The canonical Lead is `session_011EzfW1gtAhRQwk8pgJMzhG`, but its [#1245 handoff thread](https://github.com/banodoco/astrid-dev/pull/1245#issuecomment-7103252095) has no newer parser/records/protection ownership response at this checkpoint. This packet records the minimum compatible source and the missing release records, not a GO.

## Source-of-truth inventory (pinned 23 November 2026)

| Source | Frozen `release/15/main` at `321523e52bddbbd13477634b05974a16b54b825b` | Canonical `main` |
| --- | --- | --- |
| `scripts/records.py` | blob `b2b62e72396f200efd00bcebc7b1c95f0f3df92e` | blob `e865b2165d0248081d8f3f46c15fa4840048976e` |
| `scripts/test_check_docs.py` | blob `032a887af4ea6f16ed3fa896931b898486d211ce` | blob `29c9798038e83757a6a125cdb5f13222d463aaaf` |
| `releases/15.md` | blob `75ab70c56014b18b94ec887cd29ec64a126c39d4` | blob `e53f0fd53aea5d48b0387a9d7fb6c7cce0351bb1` |
| `plans/72-composable-project-delivery/plan.md` | **ABSENT** | blob `9066011c5547ce6ec62944f85a5847f2858409ac` |
| `plans/72-composable-project-delivery/inputs.md` | **ABSENT** | blob `5caae0ebc3dec1748251677b18c2ec1b38663d59` |
| `plans/72-composable-project-delivery/tasks.md` | **ABSENT** | blob `0ecdcca32053cd124f2bf07293e264e1a73ed6b1` |

The three canonical Plan 72 record files are an **authored pack**, not a substitute for an accepted owner scope decision. `inputs.md` still says `Scope decision: Pending` and `Challenge: Pending`; preserve those fields until the actual owner decision. The latest `plan.md` says `Status: queued`, `Owner: Unassigned`. Its source declaration is **`Vision role: Foundational enabler`**, NOT `Vision gaps`: importing Plan72 must not create a fictional project→gap `addresses` edge.

**What the preserved real-tree test actually requires:** `test_project_delivery.py::test_actual_repository_delivery_traversal` asserts `gap:AA-001`, `project:72` and `goal:pillar:artistic-ambition/finished-artistic-work` exist, and also that *some* authored goal→gap→project→recorded release path exists; it does **not** require that the path's project is 72. Plan72 may legitimately be a gapless enabler while a different authored project supplies the real traversal.

## Generic Release/Plan48 parser patch, prepared but NOT applied

[09-release15-branch-parser-compat.patch](09-release15-branch-parser-compat.patch) is a **two-file, five-hunk, 4,896-character** proposed patch from the frozen Release15 `records.py`/original `test_check_docs.py` blobs listed above. It selects only the already canonical `main` generic branch contract: `BRANCH_REPOSITORIES` including `astrid-dev`, tracking every included plan's branch row, and the two existing positive/negative parser tests. No Plan72-specific release-brief guards or unrelated code are in this patch.

**Static exact replay:** Each of the 5 hunks matched its frozen source context uniquely. The resulting `scripts/records.py` and `scripts/test_check_docs.py` texts were **byte-for-byte equal to the above current-main blobs** on the pinned inputs. This is stronger than an unverified textual guess but **not a native `git apply --check`, Python run or release acceptance**. The Release Lead/Plan48 generic-record owner must approve this shared-parser migration and independently qualify the preserved original tests.

**Critical dependency:** The frozen Release15 brief lists included Plans **39, 50, 40** but contains **three release rows and zero plan rows**. The newer generic parser would fail all three included-plan branch-row checks on that unchanged frozen brief. In contrast, current canonical `main` lists **16 included plans** and contains at least one plan branch row for **all 16**, plus explicit `astrid-dev release/15/main` and `astrid-dev release/15/plan-72` records. Therefore **09 cannot be landed or declared validated in isolation**: the Lead must reconcile the entire release-owned `## Included plans` / `## Branches` contract (including all previously included plans) in the same coordinated release-source integration. Do not replace the frozen Release15 brief with the latest main *wholesale*; it includes other plans and lane decisions that the Lead owns.

## Authored-record and validation cases prepared off-release

[Six source-scoped integration seam tests](https://github.com/banodoco/astrid-dev/blob/p72/recovery-root-guard-20261123-1/scripts/test_project_delivery_release15_seam.py) cover: valid `astrid-dev` release and uncut Plan72 rows, an included plan missing its plan row, a plan row without its repository's release row, included membership with its actual plan file absent, separation of frozen issue membership from authored plan delivery, and the valid **foundational-enabler** case with no project→gap edge. These tests operate on **temporary authored fixtures**, not the frozen Release15 repository. They are integration *preparation*, not proof of a cut branch or actual release traversal. No original test was altered.

The original real-repository test and all native docs/golden tests must remain enabled on the eventual authorized combined tree. Do not add `Vision gaps` to Plan72 merely to satisfy a delivery path; preserve foundational enabler and prove the traversal through actual other authored projects.

## Conditional Lead-owned selection sequence — do not run before GO

1. Lead records a specific Plan72 `GO` or `HOLD` and confirms the owner scope decision, one exclusive integration writer, exact new cut SHA, release-main branch-protection receipts and owner for generic `records.py`/brief. **The present status is HOLD.**
2. In a **new authorized release-plan checkout**, re-pin frozen source and every dependency. Have the generic Release/Plan48 owner apply/qualify 09 and reconcile **every** included plan's branch row and current repository set, preserving all earlier branch tests.
3. Select the canonical Plan72 pack by its **three exact blob IDs** (or a Lead-approved later revision). Include Plan72's actual `Foundational enabler` semantics and the Lead-approved `releases/15.md` membership/branch records. Note that a `not yet cut` branch table cell is *authored intent*, **not** proof the branch exists.
4. Follow the preexisting [13-path source preflight](https://chatgpt.com/space/page_e538b159d6d08191b1175bcb877474f1) to select typed core → readers → original RED regressions → GREEN repairs → source ownership, **without** mass-merging #1161 history. Then apply the existing [08-source-boundaries.patch](08-source-boundaries.patch) from this recovery. Defer PD7 check-registry work and the PD10 `docs/extending.md` context conflict until RS1's documented stage.
5. Run the unchanged native suite (including `test_check_docs.py`, `test_records.py`, `test_project_delivery.py`, `test_project_delivery_release15_seam.py`, the three recovery regression suites, original `test_golden.py`, `test_views.py`), `python3 scripts/astrid_dev.py check`, generated-view and public-feed byte parity with the **same authored inputs and fixed revision**, plus App `vision-consumer-contract` on the **actual combined tree**. A failed original test is a BLOCKED migration, not a reason to weaken tests.
6. Obtain a separately bound formal RS1 reviewer at the legitimate integrated stage or a distinct owner-approved exception, **never inferred from this packet**. Final R, release merge and publication remain independently gated.

**No ownership claim:** The existing #1245 Lead handoff has been notified. The parser and authored-record migration are not yet assigned to this isolated source manager, and all five visible Release15/main branch objects are currently unprotected. This artifact does not cut, merge, modify protections or dispatch reviewers.
