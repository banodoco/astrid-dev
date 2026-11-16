# Independent pre-publication review — Agent POSIX gates and failed-candidate contract

**Verdict: NO BLOCKER for publishing this bounded two-card repair to its review/plan branch.** No weakening of the reviewed security assertions, coverage loss on supported CI platforms, or Plan 38/55-owned behavior change was found. This is not full K1a acceptance or formal RS1. **RS1 remains 0/1.**

Exact reviewed range: `6c06460d3e7b46001f9d57e5b011cb114bfa23d0..cd778822a9a5fab273144ca367cfdd94a20889e3`; independently resolved final tree `001f36c60b039ab5a6fc8048f7472e82645a1a0c`. Intermediate six-gate commit: `56eecc08c4fa58cccd2556be4652d9476bef5ada`. The complete diff changes five test files: six decorators in four files, then one function in the installed-schema file. Product code, shared fixtures, registry, workflow, quarantine and all neighboring tests are unchanged. `git diff --check` passes.

Reviewed both manager cards under `plans/39-green-mains/.otto/runs/repair-20261116/`, their complete evidence folders, the retained failed baseline at `p39-g2-evidence/agent/k1a-posix-filesystem/before-complete-python.stdout`, current source/registry/selection, and product commit `896544e9558bf9b3a30d3eb9f6815b9082deb28f`. No tests were rerun and no source or remote state was changed; this review report is the only write.

## Six gate replacements

The exact diff replaces only `pytest.mark.skipif(os.name == "nt", ...)` with the existing `pytest.mark.posix_native` at these six functions:

- `tests/core/pack/test_cli_manage.py::test_implicit_descriptor_refuses_writable_and_aliases`
- `tests/core/pack/test_git_environment.py::test_planted_ssh_in_working_directory_never_runs`
- `tests/core/pack/test_git_environment.py::test_recorded_git_that_lost_its_execute_bit_falls_back_to_absolute_path_lookup`
- `tests/test_installer_pack_cleanup.py::test_posix_failed_removal_never_chmods_a_symlink_target_outside_the_tree`
- `tests/test_installer_sources.py::test_missing_runtime_lock_names_the_missing_path_not_aliasing`
- `tests/test_installer_sources.py::test_missing_candidate_or_product_root_directory_is_named`

Bodies, signatures, assertions, other decorators, and parameters are byte-preserved by the patch. The final function retains all four `candidate`, `py`, `lib`, and `site-packages` parameters; five single cases plus those four remain **nine cases**. The saved AST comparison agrees with this independent complete-diff inspection. The separate missing-Git direct skip is untouched and remains visible debt.

The lane's `available()` is `os.name == "posix"`; it is not default-off. The default pytest expression includes it and Ubuntu unit-shards own it. On Windows it receives the registry's declared platform skip, matching the previous platform exclusion. On macOS the lane is available, but the actual dedicated CI expression selects `darwin_native or remotion or chrome or codex_cli`, excluding these tests both before and after; no new macOS coverage is claimed. This establishes selection equivalence on the supported Linux/Windows/macOS platforms, not every hypothetical Python `os.name` value.

Before/after raw stdout records **9 passed**, exits **0/0**, with empty stderr. Those focused observations support the six migrations; they do not clear the whole skip-policy scanner.

## Installed-schema cleanup correction

The baseline fails **after** the expected foreign-owner refusal, at `candidate, = versions.iterdir()`, with zero remaining directories. That distinction matters: the failure is the stale leftover-candidate expectation, not missing admission enforcement.

Primary product evidence is commit `896544e9558bf9b3a30d3eb9f6815b9082deb28f`. Its message explicitly says to remove the candidate folder left by a failed prepare. Its backend diff introduces the `_stage` delegation inside `try`, removes only the new candidate through `remove_pack_tree(folder)` on failure, and re-raises the original exception. Current `Backend.stage` retains that behavior at lines 1335–1364. The cleanup correction follows intentional product behavior; it neither changes that behavior nor mistakes a newly exposed refusal for obsolete security coverage.

The unchanged fixture records `state.product_root` from the actual candidate venv's purelib path before installing the wheel and injecting foreign ownership. The new expression

```python
versions = state.root / "versions"
candidate = versions / state.product_root.relative_to(versions).parts[0]
```

recovers that candidate lexically from fixture provenance after removal. It does not require a surviving directory, glob for an arbitrary survivor, or replace the product's removal implementation.

All required checks remain:

| Contract | Review result |
| --- | --- |
| Foreign-owner refusal | Unchanged `pytest.raises(ValueError, match="foreign owner or type")`; the production guarded-directory walk still raises `installed timeline schema input has a foreign owner or type`. The existing regex is preserved, not broadened. |
| Services/profile absence | Both `candidate/services.json` and `candidate/profile.json` absence assertions remain. |
| Refusal before service declaration | The recorded-command assertion forbidding any `service_declaration` argument remains. Removing the candidate cannot conceal an invocation from this command log. |
| Failed-candidate removal | New `assert not candidate.exists()` explicitly requires the intended cleanup. |
| Outside hardlink safety | New assertions compare each fixture cache file's bytes and full `st_mode` with its pre-stage snapshots. The fixture makes these cache files outside the candidate and hardlinks them to the guarded installed inputs, so these checks constrain cleanup/admission side effects on shared inodes. |
| Admission/deletion realism | No new mocks, fixture edits or interception of admission/deletion is introduced. The fixture's existing foreign-owner injection stays unchanged. |

The file already has `pytestmark = pytest.mark.linux_native` at line 35. Removing this function's inner Windows `pytest.skip` therefore removes a redundant unreachable platform gate without a new lane, module widening, selector change or changed test ID. The neighboring FIFO case remains untouched.

The exact focused candidate result is **1 passed**, exit **0**, empty stderr. The retained baseline is **1 failed / 9 passed**, with this function failing solely at the obsolete directory unpack. These records justify the narrow correction, not a broad installed-schema or installer qualification claim.

## Ownership and residual limits

These seven test contracts concern managed descriptor permissions/aliases, Git executable resolution and planted SSH protection, installer symlink cleanup, staged-input error naming, and installed-schema foreign-owner refusal plus candidate cleanup. They do not assert Plan 38 native process identity/peer tokens/host-only pack spawn/shared source-closure parity, nor Plan 55 warm-generation session, transport, settlement or invocation behavior. Merely sharing the words “owner” or “source” does not place installer filesystem admission inside those excluded contracts. No excluded owned contract was changed.

No blocking finding or concrete new risk requiring another local test was identified. Full K1a scanner acceptance remains the manager's separate batched proof; remaining direct skips and external ownership holds are not waived. Publication of these test repairs must not be described as completed phase 1, hosted green, or formal RS1 clearance.
