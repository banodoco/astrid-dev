# Personal-pack snapshot fix: worker test results

[Handoff](../../handoff.md) · [Tasks](../../tasks.md)

Verified personal-pack snapshot repair — release 12

Source: agent HEAD 313bbd46f1e24bfe635655d78b27ab0b321145d5, uncommitted patch.
Patch SHA256: 0334c09dcd73a5e61c5fb2730aea0d93b3acde544b9691a34295e379388b6f05
All completed requested runs used this exact patch; the final baseline probe
restored the patched files byte-for-byte and verified the same diff hash.

Blocker 1
Root cause: packs/__init__.py rejected reserved personal directories before
considering verified relocations.
Fix: astrid/packs/__init__.py:71-77 admits only the validated snapshot whose
original_root is the canonical personal pack. Other reserved paths still fail.
Tests: test_namespace_accepts_exact_canonical_personal_relocation (line 133),
and test_portable_personal_task_keeps_one_discovery_owner (line 1482).

Blocker 2
Root cause: selected_pack_environment advertised personal snapshot parents as
additional collections, causing discovery to find two owners.
Fix: astrid/core/pack/imports.py:165-181 uses original collection parents;
selected import maps continue to bind executable source to snapshot roots.
Tests: test_personal_snapshot_keeps_original_collection_identity (line 147),
and the real host/worker matrix invoking public astrid.sdk.discover().

Admission
imports.py:130-142 checks the exact owner-only runtime capture area and canonical
personal origin. Relocated digest verification remains unconditional at line 150,
even with verify_digests=False. Tests reject forged original roots, mismatched
roots/digests, reused authorizations, unverified shadows, public capture parents,
and snapshots outside the capture area. The Linux lease implementation is unchanged.
Installer bootstrap remains third-party-free: 7 isolated tests passed.

Before/after evidence
before-host-public-discovery.log: all 8 host cases fail on original production:
4 personal reserved-directory errors, 4 chiptune duplicate-owner discovery errors.
before-final-regressions.log: the final exact two host selectors and two unit
selectors all fail on 313bbd46f production bytes (4 expected failures, 8.70s).
Both final unit selectors and all 8 host cases pass with the patch.
after-focused-final.log: 28 passed, 77 deselected (20 relocation + 8 host cases).
Host cases cover personal/chiptune x Python/command x darwin/win32 capture choice.
They mutate live code after capture, prove execution from snapshot source, assert
one original discovery owner, successful receipts/settlements, and snapshot cleanup.
The OS selection is simulated on Linux; native macOS/Windows execution is unverified.

Required checks (completed runs; overlapping subsets are not added together)
- tests/core/pack: 512 passed, 14 failed, 47 deselected.
  All 14 failures are exactly the supplied known list: test_r8_prod_refusals (13)
  and test_non_strict_pack_scan_quarantines_optional_failure_without_downgrading_discovery (1).
- tests/core/execution/test_m1_13_pack_provenance.py: 79 passed, 6 deselected.
- tests/core/pack/test_verified_relocations.py: 20 passed, also included above.
- All 72 tests/test_installer_*.py files: 1930 passed, 123 failed,
  18 skipped, 95 deselected. Includes bootstrap imports: 7 passed in isolation.
- git diff --check: passed.
The build-hook contract file and browser-fixture transaction cases were omitted
as requested. Other deselections/skips are the repository's default lane/platform
rules. Per-test skip reasons remain in the logs. Full installer qualification
is blocked; its failures are outside the supplied ignore list.

Installer batches (bootstrap is isolated)
- required-installer-bootstrap: exit 0; 7 passed in 2.86s
- required-installers-01: exit 1; 28 failed, 266 passed, 6 deselected in 404.00s (0:06:44)
- required-installers-02: exit 1; 60 failed, 239 passed, 1 deselected in 30.23s
- required-installers-03-rerun: exit 1; 7 failed, 238 passed, 1 deselected in 519.25s (0:08:39)
- required-installers-04: exit 1; 1 failed, 151 passed, 18 deselected in 19.98s
- required-installers-05: exit 1; 10 failed, 179 passed, 1 skipped, 14 deselected in 15.98s
- required-installers-06: exit 1; 3 failed, 129 passed, 1 deselected in 27.70s
- required-installers-07: exit 1; 10 failed, 300 passed in 34.27s
- required-installers-08: exit 1; 3 failed, 269 passed, 2 deselected in 44.88s
- required-installers-09: exit 1; 1 failed, 152 passed, 17 skipped, 52 deselected in 9.25s

Installer baseline investigation
Five representative failure families also fail on 313bbd46f production:
- ACL service.home is a Mock, causing TypeError in unchanged service/R0 code.
- doctor fixture lacks the diagnostic attribute.
- local verification reaches browser-door failure before expected transaction check.
- busy-fence fixture is refused by the R0 copy-only boundary.
- staged-schema fixture omits installed runtime.lock.json.
See baseline-installer-probes.log (first four valid probes) and
baseline-installer-schema.log (corrected exact fifth probe). The initial fifth
probe lacked baseline-copy root resources; its result was invalid until corrected.
No claim is made that every one of the 123 installer failures was baseline-probed.
All failed node IDs are listed in installer-failures.txt. No failure trace points
to either modified production file. No installer implementation files changed.
A short-temp ACL diagnostic still failed, so path length does not explain all
installer failures; some Windows-root tests also hit the 90-character root guard.

Infrastructure/evidence
The first installer batch-3 attempt was interrupted by the disk monitor's du
race with test cleanup. Its record has no pytest exit/result. The monitor was
corrected and the exact batch reran to completion as required-installers-03-rerun.
Every test run checked disk space first; final workdir is about 468 MB, / has
7.5 GB free, and tmp/ is empty. No pods were used. Changes remain uncommitted.
Exact commands, environment, source SHA, patch hash and inner pytest exits:
requested-runs.jsonl; baseline probe commands: *.command.json.
Machine-readable completed check totals: test-results.json.
