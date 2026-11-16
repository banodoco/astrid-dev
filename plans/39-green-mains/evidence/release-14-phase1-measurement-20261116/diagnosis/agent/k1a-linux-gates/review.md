# Independent prepublication review — K1a Linux gate batch

Verdict: **ACCEPT the exact three-file candidate for the manager's isolated Plan 39 publication decision. No blocking findings.** This is a bounded prepublication review, not formal RS1, K1a completion, a green-suite claim, or approval to merge into `release/14/main` or public `main`. Formal RS1 remains **0/1**.

Reviewed base `16ef29bf8cd9d9df82c6f2a892feff3dffc44d70`, candidate `372e39cd309e519857c1dbb2c86d71f7ef724232`, candidate tree `aabdeab6b08f14bff2205186b9ae1aa2f1f16380`. HEAD and tree matched the brief; the product worktree was clean. I ran no tests, collected no new tests, changed no product files, and performed no remote action. This report is my sole written artifact.

## Findings and evidence

**Blocking findings: none.**

The exact diff replaces three existing Linux skip gates: the module gate in `tests/test_installer_update_end_to_end.py`, and one decorator each on the XDG foreground-lock app-update test and XDG custody test. It changes three lines in three files. An independent AST comparison of Git base/candidate trees, removing only each exact gate node, was identical. The saved baseline files also matched Git base byte for byte. All bodies, fixtures, assertions, parameters, other marks and test names are preserved. The six held files and excluded native audit-token test are absent from the diff.

I read the raw pre/post logs and exit files, rather than accepting README counts alone:

| Migrated scope | Before | After |
| --- | --- | --- |
| End-to-end update module | 4 passed, exit 0 | 4 passed, exit 0 |
| App-update XDG selector | 1 passed, exit 0 | 1 passed, exit 0 |
| Pinokio-custody XDG selector | 1 passed, exit 0 | 1 passed, exit 0 |

The end-to-end module has four unparameterized test functions and no added default-off lane. The two selectors each name one unchanged test. Static case identity plus those complete selected counts supports parity for this small change. These `-q` logs do not independently stamp command lines, commit identities or every passed node ID; command provenance is the worker card/README, and commit/body identity was independently checked through Git. I do not treat the evidence as proof of native Windows/Darwin execution or a full CI run.

`tests/lanes.py:132` defines `linux_native` as a platform lane with `sys.platform.startswith("linux")`, Ubuntu ownership and `default_off=False`. `pytest_collection_modifyitems` applies a declared skip when that availability predicate is false. For supported Python/Linux, Windows (`win32`) and Darwin (`darwin`) values, this preserves the old `sys.platform != "linux"` gate's eligibility. The spelling is not mathematically identical for hypothetical other platform strings beginning with `linux`; this does not expand any supported platform in this repository. The registry's descriptive reason mentions `/proc` and pidfds, but the existing predicate is the appropriate Linux-only selection for these systemd/XDG contracts.

`pyproject.toml:314` does not exclude `linux_native`. Ubuntu CI's default unit shards run normal pytest selection, with all eight groups on the applicable non-PR runs; pull requests currently run group 1 only. Thus the tests retain their existing default Ubuntu coverage; this review does not claim they necessarily run in PR shard 1. Darwin's explicit lane expression does not select these cases. Native Windows selection does not gain them, and a direct default invocation there retains a declared platform skip. The broader default Linux execution set is unchanged.

The end-to-end update assertions cover installer acceptance, selected helper invocation, fake systemd submission/recovery, and update status. They do not assert warm generation-job transport or settlement. The XDG tests cover foreground refusal before writes and installer lock-path retention/release. They neither establish nor replace Plan 38 native identity-provider/token contracts. I checked the cited ownership resolution, Plan 38 and Plan 55 boundaries, and the actual test bodies; no ownership violation was found.

## Held proofs and environment evidence

**Severity: informational — known red behavior remains visible and is not addressed by this candidate.** Raw logs confirm engine readiness 9 passed/60 errors; boundary handoff 36 passed/44 failed; boundary registration 8 passed/64 failed; R0 entry 49 passed/1 failed; legacy-record update 10 passed/1 failed; field-state update 18 passed/30 failed. All six pre-proof exit files contain 1. There are no post-proof files for these held rows in this batch.

A shared environment contributor is evidenced for at least three holds. The raw handoff, registration and field-state traces reject the exact ancestor `/workspace/scratch/cd53b069f320/p39-repair/astrid-agent.env/venv` with `Managed paths cannot contain links`. During this review I initially observed that directory as `venv -> venv-complete`. The fixtures record `Path(sys.executable)` into managed versions, and `Version.load` rejects linked parent directories. Handoff and field-state logs additionally show `runtime_checkout must be an explicit absolute pinned checkout path`; `tests/test_boundary_handoff.py:100` obtains `runtime_root` from `workspace_copy.__file__`, and the trace records that root under the environment's installed `site-packages`, not the declared Runtime checkout.

The manager subsequently repaired the environment layout independently. I read `../environment-layout-correction/result.json` and `interpreter.txt` and observed `venv` now as a real directory. That report records Python 3.13.5 and equal dependency inventory hash `63d2241b36576bc935fde2c7d6c003c9d09103585a6ae06f3b4779fbf6b32734`. The old raw failures remain valid historical evidence of the original layout; they cannot establish outcomes under the repaired environment. I performed no repair or rerun.

The exact next small diagnostic for the remaining source-profile question is a read-only module-origin/interpreter check, with no pytest execution:

```bash
PYTHONDONTWRITEBYTECODE=1 /workspace/scratch/cd53b069f320/p39-repair/astrid-agent.env/venv/bin/python -B -I -c 'import sys; from pathlib import Path; from astrid_runtime import workspace_copy; p=Path(workspace_copy.__file__).parent.parent; print("executable",sys.executable); print("runtime_root_from_fixture",p); print("runtime_root_is_absolute",p.is_absolute()); print("runtime_root_has_git",(p/".git").exists()); print("executable_linked_parents",[str(x) for x in Path(sys.executable).parents if x.is_symlink()])'
```

The fixture imports `workspace_copy` from `astrid_runtime` at line 22, matching this diagnostic. A source-tree origin versus installed-package origin distinguishes the next harness diagnosis without weakening a pinned-checkout or managed-path check.

There is no evidence that one environment cause explains all six holds. Engine readiness repeatedly reports dead supervisor owners and ultimately `CustodyUnresolved`; subprocess stderr is discarded by its launch code, so the raw log does not establish why that supervisor exits. R0 entry has the separate undeclared local-artifact skip. Legacy-record update has the independent expected `failed` versus actual `recovery-needed` assertion. Each remains separately held.

## Manager follow-up: equivalent migrations while behavior stays red

**Judgment: conditionally acceptable as separately authorized OS-gate-only follow-up cards, not as retroactive satisfaction of the original passing-pre-proof card.** The original K1a card explicitly says to hold failed proofs and not retry them; this candidate obeys that instruction. If the manager issues revised bounded cards, unrelated failing assertions need not be repaired merely to replace an equivalent selection declaration. The invariant is that the migration preserves their visibility and eligibility, not that a previously red behavior is relabeled green.

Concrete boundaries:

| Held gate | Permitted follow-up boundary |
| --- | --- |
| Engine readiness module | Ownership resolution already clears only its Linux module gate. Keep real custody/profile/source-verifier assertions and every fixture intact. A repeated setup failure does not validate the unexecuted bodies or permit engine-custody changes. |
| Boundary handoff module | Linux manager simulation, copy-only adoption/rollback, crash recovery and installer refusal contracts. Replace only the module OS gate; retain process kill cuts, assertions and source/managed-path checks. These are not native birth-provider or host-spawn parity tests. |
| Boundary registration module | Persistent systemctl simulation and installer publication/recovery, including alias checks. Same module-gate-only boundary; no publication/recovery or native-provider fixes implied. |
| R0 entry module | Replace only the Linux manager-simulation module gate if separately authorized. Preserve `test_captures_match_real_r0_evidence` and its currently forbidden direct skip unchanged. That residual skip still blocks full K1a acceptance; migrating the module gate does not resolve or excuse it. |
| Legacy-record update module | Fake systemd liveness and legacy installer update-record reconciliation. Preserve the failing `failed`/`cleanup_status` assertions exactly; these concern installer updates, not Plan 55 generation-job settlement. |
| Field-state update module | Installer field-state normalization, rollback, refusal and health probing. The health-probe case consumes `platform.process_identity` to populate a discovery fixture, but asserts release/instance/update behavior, not provider format or rotation. Only its existing module gate is cleared; provider/source-closure behavior remains outside scope. |

For each new card, establish a new before/after pair under the same repaired environment and exact product base; do not pair the old symlink-environment baseline with a repaired-environment post result. Require identical collected node-ID multisets and unchanged selection/lane scope, independent AST equality outside the one gate, unchanged per-node phase outcomes and normalized exception/assertion signatures, plus recorded exit codes. Compare cases rather than aggregate counts; ignore only inherently volatile addresses, temporary prefixes and elapsed time. A changed failure category, newly skipped/deselected node, new default-off mark or unaccounted collection difference requires a hold. Capture full passed/failed/error node records or JUnit, because the old two-line passing logs are insufficient for a larger red-baseline comparison.

Passing tests must remain passing, known failures must remain visible with their causes tracked, and any full policy-guard failure must remain reported. No scanner whitelist, changed expectations, new integration mark, manual-gate rewrite or Plan 38/55 behavior fix follows from this judgment. Such a follow-up can close an individual equivalent-gate migration while K1a overall and formal RS1 remain held.
