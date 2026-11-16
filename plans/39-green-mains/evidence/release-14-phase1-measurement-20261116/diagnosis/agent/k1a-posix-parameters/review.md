# Independent review — five POSIX gates, six selected cases

**Verdict: ACCEPT the exact candidate for the manager's isolated Plan 39 publication decision. Blocking findings: none.** This is a bounded prepublication review, not full K1a acceptance or formal RS1. **Formal RS1 remains 0/1.** It does not authorize publication to `release/14/main` or public `main`.

Reviewed base `7e78fd7846b3271d30ed5f32900d68d9ecbee921`, candidate `cfabc7dabeceef6340809db22f895e7952fc8cfd`, tree `2cdff60eab7cbbddf8a59923e1c7de698176f90e`. HEAD/tree match the brief and the product worktree is clean. The exact diff contains only the three authorized files; saved `patch.diff` is byte-identical to that diff. I read the exact `run-state/K1a-posix-parameters.md` card, raw proof artifacts, registry/selection code, test bodies/fixtures and Plan 38/55 boundaries.

No tests or collection were run, no product files changed, and no remote actions occurred. This review is my only written artifact.

## Evidence and invariant verification

An independent AST comparison used Git base/candidate source, verifying that all saved `before/` files match Git base byte for byte. Unlike the worker script, which removes all target-function decorators for its comparison, my comparison retained every decorator and parameter except the exact five authorized gate substitutions. It verified the precise removed OS conditions and skip messages, the precise new lane marks, and equality of the entire remaining module AST. All assertions, helpers, fixtures, imports, parameter values/order and unrelated test bodies are unchanged.

I independently parsed both JUnit files, checked their case inventories against their raw `PASSED` log lines, and checked the exit files:

| Exact selected case | Before | After |
| --- | --- | --- |
| `tests/core/generation/test_model_verification_record.py::test_non_utf8_filename_hashes_then_reuses` | passed | passed |
| `tests/core/pack/test_verified_relocations.py::test_forged_personal_relocation_is_rejected[public]` | passed | passed |
| `tests/packs/runpod/test_failure_diagnostics.py::test_bounded_observer_rejects_malformed_or_late_child_frame[partial]` | passed | passed |
| Same function `[oversized]` | passed | passed |
| `tests/packs/runpod/test_failure_diagnostics.py::test_partial_ipc_from_unkillable_caller_returns_with_pending_fence[False]` | passed | passed |
| Same function `[True]` | passed | passed |

Each XML contains exactly these six cases, with no failure/error/skipped children; case-ID multisets match exactly. Both raw logs report six passed, and both actual exit files contain 0. The command scripts use the same canonical wrapper, flags and selectors, changing only evidence output destinations. Their final shell `exit 0` is not mistaken for pytest's status: each separately captures `$?` immediately after the proof command into the inspected exit file. There are no failure signatures to normalize.

## Conditions, parameter scopes and default eligibility

- **Model filename case:** the old `if os.name != 'posix': pytest.skip(...)` is equivalent to the existing `posix_native` lane's `os.name == 'posix'` eligibility predicate. The independent `try/except (OSError, UnicodeError): pytest.skip('filesystem does not support this filename')` remains exactly unchanged. Filename byte round-trip, actual hashing/reuse, and stored path assertions remain in place and executed successfully in the selected proof.
- **Personal relocation:** the old Windows exclusion occurs only inside the final branch for `forgery='public'`. The candidate marks only that parameter. The other exact values remain `original`, `selection`, `digest`, `reused`, `outside`, in the same order and with no added mark. Public permissions are still made `0o755`; both relocation validation and namespace-collision refusal assertions remain unchanged.
- **Malformed Runpod frame cases:** only `partial` and `oversized` replace their Windows-exclusion parameter marks with `posix_native`. The portable `late` and `eof` parameters remain unmarked and unchanged. Child-entry evidence, bounded elapsed time, sentinel exclusion and child-cleanup assertions are intact.
- **Unkillable caller:** the Windows-exclusion function mark becomes `posix_native`; `early_abort=[False, True]` is unchanged. Both cases retain the exact pending-fence exception, elapsed bound, kill attempt, retained process, token-redaction and cleanup assertions.

For the Windows-exclusion substitutions, `sys.platform != 'win32'` and `os.name == 'posix'` are equivalent on the repository's supported Windows/Linux/macOS runners. They are not asserted equivalent for arbitrary unsupported Python platforms. Moving the body-time public/filename OS gate to pytest's lane gate means unsupported-platform setup can now be skipped earlier; that is normal declared platform-gate behavior, not a loss of intended runnable coverage.

`tests/lanes.py:132` defines `posix_native` as a platform lane, maps it to the Ubuntu unit job, and leaves `default_off=False`. Default pytest marker selection does not exclude it. No integration/default-off mark, module-level lane, registry edit, workflow edit or scanner exception was added. Supported POSIX default invocations retain eligibility; Windows retains the same platform exclusion for these cases. The dedicated Darwin workflow's existing explicit marker selection is not expanded by this patch. Native Windows/macOS execution was not performed or claimed. Unselected neighboring parameters are preserved by source/AST evidence, not claimed as newly executed proof.

## Ownership judgment and limits

These selected contracts are within the narrow authorized OS-gate migration scope:

- The model test checks surrogateescape filename identity and persistence/reuse of a model verification record. Its helper name `warm` means reusing that file record; it does not exercise a warm ComfyUI job, resident session, transport or Plan 55 settlement/performance budget.
- The selected relocation parameter checks a publicly accessible personal-pack snapshot directory is refused. Its fixture consumes generic-host snapshot helpers, but the assertion is private capture-directory permission/relocation authorization, not Plan 38's Runtime/Agent host-source component-list parity, native token/birth provider, peer custody or host-only spawn contract. Plan 55's pack admission/resident-session work does not make every consumer of pack imports an owned warm-path test.
- The Runpod cases check bounded remote-observer IPC framing and retained child fences. They do not test native process-identity provider parity or local warm generation behavior. Plan 55 expressly excludes rented-machine work from its local warm-path scope.

I checked actual bodies and owning-plan contract descriptions rather than relying only on absent filenames. The excluded native audit-token test is untouched. This finding clears only the five gate substitutions; it does not authorize changes to the consuming product code or any Plan 38/55 behavior.

**Severity: informational — residual policy hold remains.** The filename-creation exception retains its direct skip as expressly required by the card. Passing this POSIX proof does not make that separate direct-skip policy issue disappear, establish all-filesystem support, or make the full skip-policy gate green. No full policy or broader suite result is claimed. Existing K1a holds and formal RS1 remain with the manager.
