# Plan 72 — supplementary reader identity and provenance regression

**Area:** PD-4 / PD-5 read-only delivery adapter. **Candidate:** `banodoco/astrid-dev` `p72/pd3-pd5-adapters`. This is an original-source/negative-control receipt, **not** an RS1 independent architecture verdict, completed integration or release authorization.

## Original failure and preserved tests

- **Original supplied candidate:** `844d9150d66636768d3034c5bebc23e8132ac405`, [reader PR #1076](https://github.com/banodoco/astrid-dev/pull/1076). Original native [CI 44824479455](https://github.com/banodoco/astrid-dev/actions/runs/44824479455) ran **464/464** passing tests, but did not exercise the adverse cases.
- **Tests-first divergence:** `7bed1f2293e626fd6ffd494c2014165489251532` adds five bounded tests to `scripts/test_project_delivery.py` **without changing production or existing tests**. [GitHub Actions 44846475104, documentation job 136667316305](https://github.com/banodoco/astrid-dev/actions/runs/44846475104/job/136667316305) ran `python3 -m unittest discover -s scripts -p "test_*.py"` and returned **FAIL** with **469 tests, 5 assertion failures and 2 errors** (expected red baseline):
  - `test_wrong_gap_filename_with_right_id_is_rejected` — `CA-001-does-not-exist.md` accepted as long as `CA-001` existed (no exception).
  - `test_changed_release_heading_cannot_publish_a_false_issue_link` — `# Release 16` inside `releases/15.md` still returned an issue-123 link to Release 15 (no exception).
  - `test_duplicate_gap_sources_name_identity_and_both_files` — two `CA-001` files produced only `duplicate record identity`, with neither ID nor either source path; three subtest assertion failures.
  - `test_gap_without_primary_names_source_and_identity` — raised bare `ValueError: exactly one primary gap aspiration required, found 0`, omitting `gap:CA-001` and its document.
  - `test_plan_without_primary_names_source_and_identity` — raised bare `ValueError: project must declare exactly one primary vision gap`, omitting `project:72` and its plan file.

## Narrow fix and positive proof

- **Fix commit:** `577034321cdfc8c2e8d554cacc5d3b563ab8ddb3`, [PR #1076](https://github.com/banodoco/astrid-dev/pull/1076). Only `scripts/project_delivery.py` changed after the tests-first commit; no existing or new assertions changed. It reuses the canonical `project_contract.GAP_LINK`, `VISION_GAPS` and `plan_gap_ids` rules rather than altering them or inventing a new source registry.
- **Product behavior:** rejects a link to an absent/wrong Markdown file even when the gap ID exists; requires both title and declared release numbers to match the release filename before emitting any edges; rejects duplicate gap sources with the stable ID and both source paths; and adds path/record ID context to malformed primary declarations.
- **Native unchanged selection:** [GitHub Actions 44846649303, documentation job 136667896032](https://github.com/banodoco/astrid-dev/actions/runs/44846649303/job/136667896032) executed `python3 -m unittest discover -s scripts -p "test_*.py"` at `57703432` and returned **PASS**, **469/469 tests** (`Ran 469 tests in 40.281s; OK`). No skipped/deleted/broadened assertions were used to get green.
- **App vision consumer:** its status is tied separately to the exact same [workflow 44846649303](https://github.com/banodoco/astrid-dev/actions/runs/44846649303); check the actual job conclusion before asserting pass.

## First divergence and authority limits

The first semantic divergence is accepting the numeric gap ID without verifying the authored link's full canonical file identity. The release variant trusts `**Release:**` and omits the heading field exposed by `records.release_brief`; canonical release-document validation already treats them as one identity. The diagnostic variants come from losing domain source paths before constructing the graph or from leaving original parser exceptions unscoped. The focused correction stays in the adapter; the canonical parsers, public feed schema and release publishing rules remain unchanged.

**Limitations:** This proves the original failure cases and fixed candidate *at the stated test commits*. It does not prove integrated head/public JSON byte equality or approve RS1's independent architecture design. The active [Goals contract PR #1059](https://github.com/banodoco/astrid-dev/pull/1059) remains a separate writer; the [Release 15 Lead handoff #1098](https://github.com/banodoco/astrid-dev/pull/1098) and Release 15 Astrid-dev integration-branch custody remain separate. **Do not merge implementation into `main` on the strength of these receipts alone.**
