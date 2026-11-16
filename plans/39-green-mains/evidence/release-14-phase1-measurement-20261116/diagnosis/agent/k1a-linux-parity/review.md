# Independent final bounded review — six Linux module gates

**Verdict: ACCEPT the exact candidate for the manager's isolated Plan 39 publication decision. Blocking findings: none.** This accepts the six equivalent OS-gate migrations under the explicit new `K1a-linux-parity.md` card. It does not declare the underlying behavior green, complete K1a, spend formal RS1, or approve merging into `release/14/main` or public `main`. **Formal RS1 remains 0/1.**

Base: `372e39cd309e519857c1dbb2c86d71f7ef724232`. Candidate: `7e78fd7846b3271d30ed5f32900d68d9ecbee921`. Tree: `6f7300217cb10eef031ef885bf99b7dbb40f9d4b`. I independently read the exact Git diff and verified HEAD/tree and a clean product worktree. Actual local branch is `p39/k1a-posix-prerequisites`, as the evidence README records; the card's original branch label differs, but the exact base/candidate identities match. No remote action occurred in this review.

I ran no tests or collection, made no source changes, and did not duplicate the manager's separate full `test_skip_policy.py` proof. My only written artifact is this review. Evidence verification used Git/AST inspection and read-only parsing of existing XML/logs.

## Exact source and selection boundary

The candidate changes precisely six module-level `pytestmark` assignments, one line in each authorized file, from existing Linux-only `skipif` to existing `pytest.mark.linux_native`. No body, fixture, parameter, assertion, other mark, import, registry or workflow changes occur. An independent AST comparison against Git base, removing only the one module gate in each tree, found all six ASTs identical. All six saved `baseline/` source files independently matched Git base byte for byte.

The module gate scopes are preserved. `tests/lanes.py`, `pyproject.toml`, workflow selection and the excluded `test_host_cleanup_ack_barrier.py` have no diff. The R0 artifact test's direct `pytest.skip` is unchanged. Imports of fixtures or helpers from other migrated modules do not introduce an additional default-off lane. No integration mark or deselection was added.

The existing `linux_native` predicate is `sys.platform.startswith("linux")` and is not default-off. This is exactly the previous engine-readiness predicate; for the other five former `sys.platform != "linux"` gates it preserves eligibility on supported Linux, Darwin and Windows platform values. The ordinary Ubuntu unit lane remains their execution home. Darwin and Windows do not gain runnable coverage. No native-platform test run is claimed by this evidence. As previously reviewed, installer state/manager/lock simulations and the ownership-cleared readiness contract are within the narrow OS-gate scope; none of these six edits changes Plan 38 native identity/provider/host-spawn assertions or Plan 55 warm-job behavior.

## Independent proof verification

I parsed all 12 completed JUnit files and all 12 corresponding logs/exit files. For row 3, the completed before file is explicitly `03-boundary-registration-before-restart1.xml`. The comparisons establish:

- Exact before/after case-ID multisets match in every row, with no duplicate JUnit case IDs.
- Each XML's full case inventory matches the full `PASSED`, `FAILED`, and `ERROR` node lines in its own raw pytest log. This check preserves spaces inside parameter IDs, including registration's `[ leading]` and `[v1 ]` cases.
- Every completed proof exits 1. No JUnit skipped cases or reported deselections occur.
- Every before/after case has the same status and complete normalized failure/error message and traceback. I independently compared complete result-tuple multisets, not only counts or the worker comparator's dictionaries.

| Module | Cases | Before | After | Exit before/after |
| --- | ---: | --- | --- | --- |
| Engine readiness | 69 | 9 passed, 60 setup errors | identical | 1 / 1 |
| Boundary handoff | 80 | 79 passed, 1 failed | identical | 1 / 1 |
| Boundary registration | 72 | 71 passed, 1 failed | identical | 1 / 1 |
| Installer R0 entry | 50 | 49 passed, 1 failed | identical | 1 / 1 |
| Installer legacy-record update | 11 | 10 passed, 1 failed | identical | 1 / 1 |
| Update from field states | 48 | 44 passed, 4 failed | identical | 1 / 1 |
| Total across separate file proofs | 330 | 262 passed, 8 failed, 60 setup errors | identical | all 1 |

These are six focused file runs on each side, not a combined suite run. The engine's 60 bodies remain unproven because their fixture setup errors occur first.

## Signature normalization assessment

**Severity: informational — comparator implementation has general-purpose limitations, but they do not weaken this candidate's observed evidence.**

`compare_junit.py` retains complete failure/error/skipped messages and traceback text, while normalizing temporary run prefixes, hexadecimal addresses, explicit process IDs and monotonic deadline values. Its result dictionaries could hide differing outcomes for duplicate case IDs, and a generic hexadecimal regex could erase a semantic hex value in other evidence. I checked those risks concretely: all case IDs in these files are unique; all observed normalized addresses are Python object representations, not asserted constants; no process-ID pattern matches these failure signatures at all.

I also reran the *evidence comparison only* independently with narrower normalization: temporary run-ID path segments, hexadecimal values only inside `object at 0x...>` representations, and numeric deadlines only on standalone traceback-local `deadline = <float>` lines. It preserves other hex values, process-ID text and deadline expressions. All six pairs still match their entire normalized result tuples. R0-entry and field-state failure signatures require no normalization whatsoever. No semantic assertion text, exception class, owner/lock state, message choice, source hash, failure location or failing case was discarded.

This validates the current snapshots; it does not endorse the comparator unchanged for arbitrary future inputs. Pytest's own traceback abbreviation remains a normal limit of the captured evidence, and JUnit does not establish the unseen bodies of setup-failing tests. The exact AST/selection invariants are therefore essential to this OS-gate-only acceptance.

## Interruption and retained failures

The original row-3 before log contains only 32 progress dots and has no XML or exit file. It is retained as `03-boundary-registration-before.interrupted.log`, separate from the completed replacement. The manager's follow-up explicitly authorizes that one replacement after termination. The complete replacement reports 71 passed/1 failed, and its paired after proof independently matches it. The partial run is not counted as a pass, treated as a completed baseline, or used to hide a test failure. I did not independently observe its termination or the process cleanup; those facts are supplied by the manager's brief and evidence narrative.

The following causes remain visible, with identical case identities and signatures before/after:

- Engine readiness: 60 setup errors with `CustodyUnresolved`, stating the engine supervisor did not confirm command cleanup; owner state is alive and lock state held. This repaired-environment signature differs from the historical pre-repair dead-owner result, but the new before and after match each other, which is the authorized comparison.
- Boundary handoff: the policy-change refusal test expects the previous installer-refusal headline and receives `Astrid couldn't finish. Your work is kept.`
- Boundary registration: the pending-registration `--uninstall` case receives the earlier-version automatic-uninstall refusal instead of the expected registration-recovery wording.
- R0 entry: missing local R0 evidence triggers the existing direct skip, which the guard turns into a failure. The manual gate is not repaired or excused by the module migration.
- Legacy-record update: expected `failed`, actual `recovery-needed`; the cleanup/state assertions remain unchanged.
- Field states: one details-line mismatch and three reason-specific next-step mismatches (`error`, `installer-bug`, `windows-upgrade-unsupported`).

No claim is made that the policy guard now passes. The manager owns the separate exact-candidate policy proof and reporting of its remaining direct-call count. The excluded Plan 38 Darwin audit-token gate and R0 manual-evidence direct skip remain visible in source. Any additional residual direct gates identified by that proof must likewise remain reported. These incomplete acceptance items do not invalidate the six proved equivalent substitutions, and they continue to prevent a full K1a or RS1 completion claim.
