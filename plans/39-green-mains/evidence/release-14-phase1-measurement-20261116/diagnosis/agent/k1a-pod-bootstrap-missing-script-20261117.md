# K1 prerequisite: 26 red pod-bootstrap tests share a missing source shell script

**17 November 2026 UTC · Route N, source and actual-XML diagnosis only.** No product/test/fixture mutation, no independent review, and no acceptance or release promotion. This is a K1a policy-gate dependency and a potential separately triaged legacy product-route failure, **not** proof that every one of these assertions is stale or that PR369 regressed behavior.

## Verified hosted evidence

Agent CI [43967861168](https://github.com/banodoco/astrid-agent/actions/runs/43967861168), attempt 1, at exactly `6bbda788c1a62abcdda242f85c7a1cae86c57d3d` (reviewed tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`), has completed failure. [Unit shard 6 job 133651924641](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924641) uploaded actual [JUnit artifact 14283023095](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14283023095). The preexisting verified ZIP SHA-256 is `74811e80afd29518a356b8f2dd4b4794b4a34f5ea375412dc5ad11cab0ea7d47`, and inner `unit-shard.xml` SHA-256 is `b397f917a9ef5f01734ff06fcaeb7b7e39d8a35d3064f4d610977fc97168f89a`. This follow-up checked the complete local hashed literal-message/testcase inventory rather than inferring details from a run badge.

**All 26 actual testcase IDs prefixed `tests.scripts.test_pod_bootstrap::` have outcome `failure`**. They cluster into six full literal XML message strings, with counts **13, 9, 1, 1, 1, 1** (26 total). No individual case is counted from an absent or uncollected ID:

| Exact current XML count | Literal error/failure signature | Interpretation |
|---:|---|---|
| 13 | `FileNotFoundError: [Errno 2] No such file or directory: '/home/runner/work/astrid-agent/astrid-agent/scripts/pod_bootstrap.sh'` | Tests reading the shell or extracting its functions cannot access it |
| 9 | `AssertionError: /bin/bash: /home/runner/work/astrid-agent/astrid-agent/scripts/pod_bootstrap.sh: No such file or directory` (inner shell exits 127 instead of expected 0) | Tests invoking the absent shell fail before checking its behavior |
| 1 | `subprocess.CalledProcessError: Command '['bash', '-n', '/home/runner/work/astrid-agent/astrid-agent/scripts/pod_bootstrap.sh']' returned non-zero exit status 127.` | Syntax check cannot run |
| 1 | `AssertionError: assert 'fixture source identity refused' in '/bin/bash: ... No such file or directory\\n'` | Refusal behavior not reached |
| 1 | `AssertionError: assert ('cannot create or write' in '/bin/bash: ... No such file or directory\\n')` | Unwritable-root guard not reached |
| 1 | `AssertionError: assert 'uv not found' in '/bin/bash: ... No such file or directory\\n'` | Missing-dependency guard not reached |

These are **26 failure occurrences, not 26 independent root causes**. The job has many other failures outside this family. The previous plan head `b8f26929` also lacks `scripts/pod_bootstrap.sh` and has the same pack-owned Python payload blob; its exact XML outcomes are **not** re-compared in this note, so no old-versus-new outcome claim or PR369 attribution is made.

## Checked source identities and conflicting contracts

1. [`tests/scripts/test_pod_bootstrap.py`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/scripts/test_pod_bootstrap.py#L1-L18) resolves `SCRIPT` to `scripts/pod_bootstrap.sh`. Every one of the 26 tests uses that source, directly or via `_setup_runtime_function`/`_boot`/`_gpu_sanity_function`. The script is **absent** from the exact merged tree (GitHub contents returns 404), the previous plan head, and the separately recorded Agent release-main `fc391dea`.
2. [`astrid/packs/runpod/pod_bootstrap.py`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/astrid/packs/runpod/pod_bootstrap.py#L1-L43) contains `SCRIPT` as a pack-owned shell payload. The module explicitly says it was relocated to ship without checkout-level scripts. [`remote_placement.py`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/astrid/packs/runpod/remote_placement.py#L780-L795) writes this payload to a staged `pod_bootstrap.sh` and transports it.
3. **Not proven equivalent:** the old test asserts a noneditable package-install sequence, whereas the current pack-owned shell's `staged_uv_install` intentionally supplies `-e` for Agent and Runtime at lines 37–41. Simply substituting a Python `SCRIPT` string for the missing shell path would reach materially changed assertions and may conflate two bootstrap contracts. No assertions were loosened.
4. The separate [`scripts/pod_session.py` bootstrap command](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/scripts/pod_session.py#L447-L455) still invokes `bash src/astrid-agent/scripts/pod_bootstrap.sh`. The source-tree path is absent, making this a **potential live legacy-route defect** if `pod_session.py` is still an admitted entrypoint. The current installed pack route writes its own payload separately. Reachability, support status and consequences of changing the legacy caller are **not established** by XML alone.

## Repair boundary and next proof

Before a change, determine whether the legacy `scripts/pod_session.py` entrypoint is supported and whether its old bootstrap contract must be preserved. That is **product/scope ambiguity**, not a safe mechanical test update. Preserve all 26 currently red IDs, identity checks, idempotency, no-secrets, and source-integrity tests; do not add a skip, xfail or misleading shim to turn these green. If the legacy route is supported, route its production-path repair with security/data review (S-class) and its exact entrypoint test; if retired by a documented product change, use that authoritative change to design a tested N-class port of the 26 expectations to the pack-owned payload, explicitly reconciling editable-source semantics and source provenance. Either needs focused proof and a separate independent review before any Plan 39 integration.

The previously noted K1a row 13 `test_setup_runtime_with_real_runtime_creates_workspace_once` is **not merely an unprovisioned Runtime executable** on this head: its actual XML outcome is already `failure` from the missing bootstrap script. This corrects the earlier unverified dependency hypothesis without changing the remaining-gates historical record.

**Held:** Agent draft [PR373](https://github.com/banodoco/astrid-agent/pull/373) is still unmerged without an independent submitted reviewer or authentic Windows XML for its two selectors. The short-lease historical Runtime checkout remains held for Plan55 ownership, and the separate Runtime clip 25P/2F exact-retry/CAS-history decision is unchanged. Plan38/55 WAITING; Release15 excluded. Formal G1/G2 incomplete, RS1 0/1. No auth retry, other-session workflow rerun/cancellation, inputs/task-checkbox edit, or main-branch push/merge.
