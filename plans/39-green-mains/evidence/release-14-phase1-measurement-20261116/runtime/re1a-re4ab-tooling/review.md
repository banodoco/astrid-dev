# Independent pre-publication review — RE1a / RE4ab

**Verdict: NO BLOCKER for publishing this bounded repair to its review/plan branch. This is not hosted acceptance, completed G2, formal RS1 or release approval. Formal RS1 remains 0/1.**

Reviewed Runtime range `ac9e6d2e7f6a0a6961d7a2d924040f61832925d1..a05d360c50b35c6803d710909c87b51daf5e84b2`; independently resolved final tree `0291fadcde521650fdc71257a9ec2fd61b7226a4`. Exactly three files change: the one-line Agent test pin, seven Nightly tool-provisioning lines, and the sandbox pytest environment PATH prepend. No test body, assertion, registry, selector, product code, lockfile, artifact step or privilege/mount configuration changes. Diff whitespace check is clean. Review is read-only except this report; no new tests or remote operations were performed.

## Authority and source identity

Read both manager cards at `plans/39-green-mains/.otto/runs/repair-20261116/RE1a-released-agent-pin.md` and `RE1a-RE4ab-qualified-tooling.md`, the saved `agent-pin-contract-trace.md`, Plan 39 RE1/RE4 scope and the Release 12 gate record. RE1 explicitly permits a pin update when G1 proves the pin behind Release 12. The old `b05ac03a5bcab278bccf99d85b49f4037b5dec10` release-1 pin lacks the needed timeline modules; the new `0e1543e0da2215db9cb3320cfd1083174c3c62a9` is the recorded published R12 Agent, not an inferred current R14 target. The separate qualified-tooling card authorizes the Nightly and sandbox compiler changes; they are not smuggled into the one-file RE1a scope.

The prepared Agent checkout independently reports clean status, HEAD `0e1543e0da2215db9cb3320cfd1083174c3c62a9` and tree `f5744c903c3d681518510204d8e2e3e96825144d`. That checkout is shallow; it cannot independently establish the older b05 ancestry. The sibling Agent repository does establish b05→R12 ancestry. The source trace and published tuple are consistent with this narrow pin choice.

The corrected evidence explicitly supersedes N's erroneous editable-install claim. `install.txt` records rebuilding and reinstalling Astrid from the verified local Agent source; `README.txt` records the `--no-deps --reinstall` command. `freeze-before.txt` and `freeze-after.txt` are identical. `provenance.txt` shows installed imports from the existing venv's site-packages, no Agent checkout inserted in that standalone provenance process, the exact Agent Git identity, and all **78 tracked timeline files** matching Git bytes. This addresses the observed stale-installed-package failure. It is scoped timeline provenance, not a claim that every installed Agent file or every transitive dependency was independently hashed.

## Wiring and preservation

- Nightly adds Node 22, `npm ci` in `packages/typescript`, and the repository `node_modules/.bin` to `GITHUB_PATH` before pytest. The committed lock resolves TypeScript 5.9.3; no global compiler fallback, install-lock change or command substitution for tests is introduced. Existing immutable Agent override validation, checked-out SHA equality, full histories, historical-source warning, `-m integration`, JUnit flags, always-run summary and upload remain identical.
- Sandbox already runs `npm ci` in its owned copied workspace as the unprivileged `ci` user. The new line prepends that workspace's compiler bin directory to the environment of the final pytest subprocess, after provisioning. The command still uses its absolute venv Python, unchanged `-n 2`, sandbox mode and exclusion expression, unchanged forwarded arguments, `drop_privileges`, and `return result.returncode`. The read-only source/Agent mounts, copied history, result mount ownership, seccomp profile and shell propagation remain untouched. No newly privileged execution or writable source mount is introduced.
- The new compiler directory contains the package's locked `tsc`/`tsserver`; the Python path is not changed by this diff. Node selection in the sandbox remains its existing apt provisioning. Local Node 22 is not proof of the container's actual Node version, but this patch neither changes that version nor adds a newer compiler than its existing `npm ci` already installed.
- There is no new Agent fallback or import workaround. Existing fixture behavior still matters: `tests/test_timeline_clip_replacement.py::_native_agent_source` inserts the explicit `ASTRID_CHECKOUT` into `sys.path`, and integration helpers may select source modules. The standalone provenance check is installed-only; do **not** generalize that phrase to every test's execution. Source and installed timeline package now both match R12, so this existing source selection does not establish contamination or a blocker in this range.

## Evidence and limits

Read `README.txt`, all three focused logs and exit files, install/provenance/wiring logs and exits, both package snapshots, complete diff and commit/tree receipt.

| Recorded proof | Result | What it establishes |
| --- | --- | --- |
| Operation-handle integration, explicit `-m ""` | 3 passed; exit 0 | These three real SDK/transport cases run after the qualified R12 replacement and local locked compiler setup. |
| Timeline type generator plus document-object contract | 29 passed; exit 0 | These local compiler/document cases pass with the repository TypeScript compiler. |
| Exact clip-replacement file invocation | 10 strict declared xfails, 17 deselected; exit 1 | Missing-import setup no longer prevents these selected legacy cases reaching their existing strict sentinel. The file is **not passing**, and the deselected integration cases are unproved. |
| Syntax and executable resolution | Python AST and YAML parse OK; Node 22.23.5; `tsc` resolves to repository TypeScript 5.9.3 | Static wiring and local executable provenance, not an Actions or container execution. |

The local environment is Python **3.13.5**; Nightly/container use **3.11**. The local worker wrapper already provisioned and exposed the locked compiler, so these local passes demonstrate the selected pair/cases, not that the new Actions or Docker wiring has executed successfully. No live Docker proof was available. The README states these limits accurately.

## Remaining acceptance obligations (non-blocking for this publication)

1. Obtain hosted Nightly and sandbox runs on the integrated candidate, retain effective Runtime/Agent SHAs and complete per-test results, verify the measured bare-`tsc` failures disappear, and classify any newly exposed failures. RE1's unit/other applicable job evidence remains separate.
2. Do not claim all 539 timeline, nine helper or three custody-class errors are cleared from these 32 passing local cases. A published Agent version is a justified pin target, not proof of compatibility with every current Runtime test. Pin advancement affects all jobs that consume this file and can expose additional behavior differences.
3. Retain the clip exit-1 result and K1 inventory/metadata blockers. Preserve Plan 38/55 ownership exclusions; this review grants no fixes or green credit to their behavior. Do not consume formal RS1 or mark phase 1 complete from this review.

No concrete implementation regression requiring an additional local test was identified in the three-file range. The missing hosted/container execution is an explicit acceptance follow-up, not evidence of a source defect or permission to weaken the guards.
