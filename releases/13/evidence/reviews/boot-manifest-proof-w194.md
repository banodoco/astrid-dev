**BLOCK — R12 rollback fails after C restamps the manifest.** R12 `0e1543e0` accepts the original fixture, but raises `BootManifestDrift` against C’s replacement. Same-schema updates omit the backup, and rollback therefore cannot restore the old stamp before restarting R12. Both pinned Runtime versions use schema 33. The real rollback dispatcher reached `rollback_selected`, then R12 composition failed; service callbacks were simulated. [Reproduction](/home/user/wt/r13-tests/runs/w194/rollback-transaction.log), [backup policy](https://github.com/banodoco/astrid-agent/blob/dd4263be1a8452fdd3085eb8d7e080ef828c3c0a/astrid/installer/core.py#L835), [rollback restore condition](https://github.com/banodoco/astrid-agent/blob/dd4263be1a8452fdd3085eb8d7e080ef828c3c0a/astrid/installer/core.py#L322).

**A second blocking finding affects a busy resident host.** Successful resident attachment returns before composition. However, rejected attachment falls through to restamping **before** checking whether the resident host is busy or replacement is permitted. C then refuses reconfiguration, leaving the running host’s manifest changed. R12’s own provenance reader subsequently raises `HostError: boot manifest changed after host startup`; A″ preserves the stamp and passes. This can break completion of active work. Restamping must follow safe retirement/admission of the replacement host. [Bootstrap ordering:2247](https://github.com/banodoco/astrid-agent/blob/dd4263be1a8452fdd3085eb8d7e080ef828c3c0a/astrid/sdk/host_bootstrap.py#L2247), [C reproduction](/home/user/wt/r13-tests/runs/w194/busy-c.log), [R12 provenance check](/home/user/wt/r13-tests/runs/w194/r12-resident-provenance.log).

Fetched and reviewed A″ `34fee0cf` → C `dd4263be1`: **7 files, +429/−2**.

- `astrid/core/_shared/boot_manifest.py`: +35/−2.
- `tests/test_boot_manifest_legacy_restamp.py`: +224.
- `tests/fixtures/boot_manifest/r9-stamp.json`: +20.
- Four `r9`–`r12` provenance files: +150.

No existing test was edited; no existing assertions were weakened. [Exact diff list](/home/user/wt/r13-tests/runs/w194/diff-list.txt).

The manifest protects **consistency with a previously recorded derived state**. Equality compares schema version, `profile_order`, `registry_digest`, `conformance_digest`, `profile_digests` and `fixture_digests`. Registry identity includes declarative registry entries and fixture identities; conformance/profile digests cover fixture rows. File digests are declared fixture values, not fresh hashing of arbitrary files on disk. Differences can expose changed registry/fixture declarations, half-applied upgrades or downgrades. It is not an authenticated release signature. [boot_manifest.py:143](https://github.com/banodoco/astrid-agent/blob/dd4263be1a8452fdd3085eb8d7e080ef828c3c0a/astrid/core/_shared/boot_manifest.py#L143), [manifest construction:184](https://github.com/banodoco/astrid-agent/blob/dd4263be1a8452fdd3085eb8d7e080ef828c3c0a/astrid/core/_shared/boot_manifest.py#L184).

**The legacy rule weakens that drift detection during migration.** A valid-shaped stamp containing only `['pip_embedded']` and arbitrary valid-format digests is accepted and replaced without authenticating those digests against historical values. The replacement records live state. I reproduced A″ rejecting this and C accepting it, including a custom, internally consistent modified live registry/fixture set. Normal R13 composition still requires its empty profile set; inconsistent inputs fail validation. This is acceptable as an explicit migration policy for a same-user, writable derived cache—equivalent to establishing a fresh-install baseline—but it does not preserve R12’s prior-state comparison guarantee. It is not completely silent: each replacement emits a stderr notice. [Legacy predicate:413](https://github.com/banodoco/astrid-agent/blob/dd4263be1a8452fdd3085eb8d7e080ef828c3c0a/astrid/core/_shared/boot_manifest.py#L413), [integrity probe](/home/user/wt/r13-tests/runs/w194/integrity-c.log).

`load_boot_manifest_hash` remains read-only. Successful resident attachment preserves the legacy stamp; the rejected-attachment case above prevents an unconditional “resident paths never restamp” conclusion.

Cooperating host startups serialize through `generic-host.lock`. The writer flushes/fsyncs a temporary file and atomically replaces the destination. Two deliberately concurrent direct writers produced complete JSON and the same final hash; both emitted notices. Failed replacement preserved the original and cleaned the temporary file. A leftover lock pathname was acquirable. There is no new parent-directory fsync guarantee for power loss. [Writer:423](https://github.com/banodoco/astrid-agent/blob/dd4263be1a8452fdd3085eb8d7e080ef828c3c0a/astrid/core/_shared/boot_manifest.py#L423), [race evidence](/home/user/wt/r13-tests/runs/w194/race.log).

Tests used fresh worker environments and the requested wrapper, with networking isolated. Default runs produced **A″ 785 passed / 35 failed / 6 skipped; C 802 / 18 / 6**. A supplemental integration pass produced **54 passed / 24 failed / 1 skipped on each side**.

Combined per-file counts below are **passed / failed / skipped**. Labels are abbreviated; [exact paths, commands and IDs](/home/user/wt/r13-tests/runs/w194/combined-summary.json) are retained.

| Test file | A″ | C |
|---|---:|---:|
| core/execution/generic_host_actions_v3 | 165/1/0 | 165/1/0 |
| core/execution/producer_evidence_transport_f06 | 13/0/0 | 13/0/0 |
| core/execution/worker_startup_identity | 8/0/0 | 8/0/0 |
| core/gateway/doctor_bundle | 57/0/0 | 57/0/0 |
| core/gateway/doctor_tools | 1/0/0 | 1/0/0 |
| core/gateway/update_recovery | 5/0/0 | 5/0/0 |
| core/generation/native_alignment_projection | 3/0/0 | 3/0/0 |
| integrations/generic_host_activation_acceptance | 9/11/1 | 9/11/1 |
| packs/runpod/worker_staging | 6/10/0 | 6/10/0 |
| sdk/host_attach_rejection | 15/0/0 | 15/0/0 |
| sdk/host_bootstrap_source_identity | 81/0/0 | 81/0/0 |
| sdk/host_recovery | 75/1/6 | 75/1/6 |
| stage1/capability parity gate | 0/2/0 | 0/2/0 |
| stage1/generic host process bootstrap | 0/1/0 | 0/1/0 |
| stage1/host bootstrap manifest | 11/0/0 | 11/0/0 |
| stage1/pack_host_interpreter_identity | 17/11/0 | 17/11/0 |
| stage1/runtime_client_cutover | 38/1/0 | 38/1/0 |
| test_b6_boot_manifest | 19/0/0 | 19/0/0 |
| test_boot_manifest_legacy_restamp | 11/17/0 | 28/0/0 |
| test_generic_host | 305/4/0 | 305/4/0 |
| **Total** | **839/59/7** | **856/42/7** |

One additional macOS-only case remained deselected. No collection error reproduced in these environments. **No C-only failing pytest IDs; 17 fixed; 42 shared failures**, including the default run’s 18. The two blocking behavioral findings were reproduced separately.

Fail-first used C’s new tests and fixture in the detached A″ worktree: **17 failed, 11 passed**. C’s new tests, B6 tests and bootstrap-manifest tests total **58 passed**.

Offline composition results:

| Input/action | Result |
|---|---|
| Legacy fixture → A″ | `BootManifestDrift`; unchanged |
| Legacy fixture → C | Equals live; exactly one stderr line |
| C composition again | No change; no stderr |
| Removed plus unknown profile | `BootManifestDrift`; unchanged |
| Symlink | Refused with `BootManifestError` |
| Corrupt JSON | `BootManifestCorrupt`; unchanged |
| R13-restamped file → R12 | `BootManifestDrift` |

[Reproduction commands/results](/home/user/wt/r13-tests/runs/w194/probes.json).

All temporary worktrees, environments, basetemps and scratch roots were removed. No tracked shared-checkout edits, pushes or provider calls were made.

**Constraint violation:** the supplemental parity-gate test spawned nested pytest processes while both outer runners were active, exceeding your strict two-process cap during that file. [Cleanup and exception record](/home/user/wt/r13-tests/runs/w194/cleanup.json).