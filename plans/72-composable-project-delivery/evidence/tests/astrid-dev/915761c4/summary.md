# Plan 72 — gap-heading and duplicate release identity adverses

**Evidence date:** 21 November 2026. **Reader PR:** [#1076](https://github.com/banodoco/astrid-dev/pull/1076). **Scope:** authored gap/release identity, not architecture approval, closure or Release 15 integration.

## Reproduced failures before the fix

Previously passing reader `8d9515b7bd5025ef38a1e101ebcc13985f00f7aa` had both original GitHub required checks green in [run 44853224735](https://github.com/banodoco/astrid-dev/actions/runs/44853224735). New **test-only** commit `8e745182f69456ccd0fc3f3bb6189c995474795b` added four tests in `scripts/test_project_delivery.py`, `scripts/test_records.py`, `scripts/test_check_docs.py` and left production unchanged.

- `test_gap_heading_identity_must_match_filename`: a file at `vision/gaps/CA-001-finish-work.md` whose heading declares `# CA-002 —` still yielded a goal-to-CA-001-to-project-to-release graph. Canonical `checks._gap_structure` already rejected such heading/file mismatches; the delivery adapter had omitted that check.
- `test_duplicate_release_field_cannot_authorize_frozen_issue_link`: `releases/15.md` carrying **both** `**Release:** 15` and `**Release:** 16` still returned issue 123 → Release 15. The reader checked only the first parsed value and title.
- `test_release_field_duplicated_is_refused_even_with_valid_first_value`: `records.release_brief` accepted two identical 15 values **or** a 15/16 conflict when `strict=True` and did not record the duplicate error for `strict=False`.
- `test_duplicate_release_metadata_is_rejected_by_canonical_validator`: `check_docs.release_errors` also accepted both duplicate variants, because the shared parser omitted duplication and the document validator delegated to its `errors` list.

The exact [test-only documentation job 136722309865](https://github.com/banodoco/astrid-dev/actions/runs/44863623760/job/136722309865), [workflow 44863623760](https://github.com/banodoco/astrid-dev/actions/runs/44863623760), ran `python3 -m unittest discover -s scripts -p "test_*.py"`: **FAIL: 476 tests, six failing assertions** (two subcases each for the direct parser and document validator, one each for the two reader cases). The vision-consumer job was skipped after the failed dependency. No retries-to-green, test modifications or assertion weakening were used.

## Minimal correction and paired green evidence

- **Fix head:** `915761c49341aea3eefd383386951b1aad804a5b`, on existing `p72/pd3-pd5-adapters` / [#1076](https://github.com/banodoco/astrid-dev/pull/1076).
- `scripts/project_delivery.py` now checks the gap heading's required `# <gap ID> —` prefix **before** constructing the link, matching the existing `checks._gap_structure` contract. Diagnostics identify the path, declared heading and `gap:CA-001` identity.
- `scripts/records.py:release_brief` now rejects duplicate `Release` declarations in strict parsing and surfaces `Release duplicated` in non-strict parsing; therefore both direct reader and existing canonical `check_docs.release_errors` receive the same rejection.
- **Diff `8d9515b7..915761c4`:** only two source files (`project_delivery.py` +8 lines; `records.py` +3 lines) and the three additive test files (four new tests). **No original test or assertion deletion, relaxation or reclassification.**
- [Corrected native workflow 44863786568](https://github.com/banodoco/astrid-dev/actions/runs/44863786568): [documentation job 136722830312](https://github.com/banodoco/astrid-dev/actions/runs/44863786568/job/136722830312) **PASS: 476/476** (`Ran 476 tests in 38.350s; OK`). [vision-consumer-contract job 136723016372](https://github.com/banodoco/astrid-dev/actions/runs/44863786568/job/136723016372) **success** against the App consumer on the exact candidate.
- The dependent [PD-8 parity probe #1106](https://github.com/banodoco/astrid-dev/pull/1106) has been additively merged forward to `6907d14f7a0a5a3e166c414c0ea675baae34f618`, and [PD-10 guide #1079](https://github.com/banodoco/astrid-dev/pull/1079) to `775507485cf0b9404a31be8b7fb89490791e21ac`. GitHub comparisons show each differs from corrected reader only in its own test or documentation file. They require their own current-head CI qualification.

## Contract classification and remaining gates

Gap heading/file mismatch was already a canonical check refusal; the adapter now mirrors it. The duplicate Release field had no canonical refusal and was **added** to the existing shared release parser rather than hidden by a one-off reader filter. This is a structural-validation change affecting all callers and remains reviewable by a separate independent reviewer before integration.

**RS1 architecture review is not complete; Release 15 manager/branch custody remains unaccepted; the code PRs are not integrated.** This evidence concerns the exact candidate only. The prior fixed-revision feed-byte comparison ([PD-8 evidence](../57703432/feed-parity.md)) checked different source commits; final Plan 72 integration still needs fresh fixed-revision byte parity, generated-view checks and independent regression review.
