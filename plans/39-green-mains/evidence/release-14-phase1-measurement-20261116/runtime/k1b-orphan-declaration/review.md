# Independent pre-publication review — orphan xfail declaration

**Verdict: NO BLOCKER for this bounded removal.** This retires stale registry data, not a live test. Full K1b remains incomplete; formal RS1 remains **0/1**.

Reviewed exact Runtime range `a05d360c50b35c6803d710909c87b51daf5e84b2..2777051c06c3d15e14d3e8d13de26b19f875c4bc`, independently resolved tree `2749ee50447b2082b198cf561c895796a6d09444`. Read the manager card, inventory group 3, primary commit `925a7dd1c648a7632ba5b44a53566329ad947564`, entire candidate diff, current live test and semantic guard, REPORT and both focused logs. No source edits, test reruns, workflow actions or remote changes; this report is the sole write. Diff whitespace check passes.

The diff removes exactly the `runtime-exact-idempotency` object from `tests/lanes.py` and its matching `_PINNED_XFAILS` entry from `tests/test_skip_guard.py`. No other declaration, assertion, marker, guard function, cap, expiry rule or test body changes.

Primary commit `925a7dd` explicitly removed the retired-only combined timeline-shot/reference journey in favor of existing refusal controls. Its diff actually deletes `test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting`. Searching the candidate's tracked tests finds no such node/body. Removing its lingering declaration therefore does not reduce executable coverage or hide a present failure. This review does not retrospectively certify all decisions in that historical deletion; it verifies that the present registry entry is orphaned.

The distinct live `test_project_reference_creation_is_keyed_durable_and_non_overwriting` is untouched. It still verifies missing-key 400, creation, restart same-key replay, changed-payload 409, different-key overwrite 409 and persisted name `Exact`. Its file has no changes in this range. No Plan 38 or Plan 55-owned live test changes.

The immutable semantic comparison remains exact over all surviving declaration node IDs, raises types and reason strings; strictness/nonempty constraints remain. Its negative test still checks repointed node, added node and widened exception against the pin. Only the mirror of the already-absent test is removed, rather than weakening the comparison to allow arbitrary declaration drift.

Independently counted the AST declarations at both commits: **10 groups / 20 exact node IDs → 9 groups / 19 exact node IDs**. The cap remains **10 node IDs**, and the **14-day** expiry bound and issue/owner/expiry checks are unchanged. Nine surviving groups still lack required metadata. The Plan 38 installed-pair declaration remains present and unresolved.

Both raw focused logs show **6 passed** (the three semantic guard selectors include three mutation parameters, plus the live reference case). REPORT records both exits as zero; unlike the Agent evidence, this directory does not retain separate raw exit-status files, so that exit value is the worker's recorded report rather than independently readable exit-file evidence. The six passing summaries and exact diff are consistent with the bounded claim; this minor provenance limit is not a code blocker and does not justify an unnecessary rerun.

Do not interpret these focused passes as a passing full registry or K1b completion. The count is still over cap and real metadata is still missing. The card's instruction to await the in-flight integrated CI/Nightly before publication remains a manager sequencing condition; this read-only code review did not query or satisfy it. No concrete implementation defect requiring a further local test was identified.
