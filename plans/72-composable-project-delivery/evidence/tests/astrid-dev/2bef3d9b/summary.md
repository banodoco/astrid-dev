# Plan 72 — duplicate project number source identity regression

**Scope:** read-only Plan 72 relationship adapter, PD-4 / PD-5 project identity and provenance. **Not** independent RS1 architecture approval or Release 15 integration authority.

## Existing canonical behavior

The existing `scripts/checks.py:_unique_project_numbers` recognizes duplicate numeric project IDs and reports duplicate plan folders. The Plan 72 `scripts/project_delivery.py:load_delivery` adapter instead used `project_folders[project.id] = path.parent.name` without first checking for an existing key, overwriting a previously discovered folder. Subsequent release membership validation could then report an unrelated missing release folder rather than the actual duplicate.

The fix does not change `checks.py`, `project_contract.project_number` or any upstream authoring/source record. It brings the derived reader into agreement with the established unique-project identity contract.

## Failing-before reproduction

- **Previously passing reader source:** `915761c49341aea3eefd383386951b1aad804a5b`, [reader PR #1076](https://github.com/banodoco/astrid-dev/pull/1076), [native CI 44863786568](https://github.com/banodoco/astrid-dev/actions/runs/44863786568) green.
- **Test-only head:** `29616fe4ff6713079b261423e388f9440897b0e3`, adding two focused tests to `scripts/test_project_delivery.py` without production changes or assertion deletions:
  1. `test_duplicate_project_number_reports_both_authored_sources` creates `plans/72-demo/plan.md` and `plans/72-z-duplicate/plan.md` (both project 72), while release 15 still includes `72-demo`.
  2. `test_duplicate_gapless_project_number_is_not_an_enabler_escape` uses the same duplicate number with the second plan explicitly designated a foundational enabler. This must not suppress duplicate-ID rejection.
- [**Native red CI 44868649615**, documentation job 136737966571](https://github.com/banodoco/astrid-dev/actions/runs/44868649615/job/136737966571) executed the unchanged selected full suite `python3 -m unittest discover -s scripts -p "test_*.py"`: **FAIL: 478 tests, 10 assertion failures** (four missing expected substrings and one unexpected `unknown folder` assertion in each new case). The first observed error in both cases was `releases/15.md: Plan 72 names unknown folder 72-demo`. It did not identify the duplicate project number or either authored `plan.md` path. The App consumer job was skipped due to failed documentation.

## Smallest corrective change and positive proof

- **Fix head:** `2bef3d9b295008733ae672204ebf728c1a069ed5` on existing `p72/pd3-pd5-adapters` / [PR #1076](https://github.com/banodoco/astrid-dev/pull/1076).
- **Change:** In `scripts/project_delivery.py`, before inserting into the existing `project_folders` dict, inspect `project_folders.get(project.id)`. If already present, raise `RelationshipError` with **`project:72`, `duplicate project number`, `plans/72-demo/plan.md` and `plans/72-z-duplicate/plan.md`**. This prevents overwriting evidence or reaching a misleading release-membership error. It uses the same stable ID as the canonical `project_number` parser; no parallel registry or state machine.
- **Original-to-corrected diff:** `915761c4..2bef3d9b` includes exactly `scripts/project_delivery.py` (+5, −0) and `scripts/test_project_delivery.py` (+29, −0). Existing and new tests preserved unchanged after the test-only head.
- [**Native green CI 44868739125**, documentation job 136738257438](https://github.com/banodoco/astrid-dev/actions/runs/44868739125/job/136738257438) ran the same original selection: **PASS: 478/478 tests**, `Ran 478 tests in 74.339s; OK`. [App vision-consumer contract job 136738631480](https://github.com/banodoco/astrid-dev/actions/runs/44868739125/job/136738631480) also returned **success** at the corrected exact head.

## Limits and open gates

This is supplementary negative-control validation, not the configured high-judgment RS1 architecture verdict. It does not qualify a final integrated Release 15 branch, prove final public-feed byte parity or imply release publication. The [RS1 review requests #1074](https://github.com/banodoco/astrid-dev/pull/1074) / [#1076](https://github.com/banodoco/astrid-dev/pull/1076) remain pending. The [Release 15 Lead handoff #1098](https://github.com/banodoco/astrid-dev/pull/1098) is pending acceptance, and no Astrid-dev Release 15 integration branch is present.

**Reproduce:** inspect both linked GitHub Actions jobs and compare the two commits, retaining the source names and test selection exactly. This evidence reports the inner selected command and result, not only the workflow wrapper.
