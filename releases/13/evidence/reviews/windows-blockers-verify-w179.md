**Both reported defects are confirmed by source inspection and Linux simulations of the relevant Windows behavior.** Native Windows execution was not performed.

1. **Release-control failure — confirmed.** At candidate `f709407cb`, `astrid/packs/runpod/release_control.py:99` calls `os.fchmod` without a platform or availability guard. The surrounding handler catches `OSError` and `ValueError`, not the resulting `AttributeError`; the server constructor catches the exception to close its socket and then re-raises it. `RunPodLeaseOwner` constructs the server at `worker_owner.py:168`, before starting a fresh claim.

   The smallest complete fix is to use `runtime_protocol.platform.owner_only(fd)` for the descriptor at line 99 and use the corresponding native privacy check in `request_release` at line 179. A bare `hasattr` guard would avoid the exception but would not establish Windows owner-only access. Also ensure the failure cleanup closes the temporary descriptor. A fail-first test should remove `os.fchmod`, simulate the Windows permission helper, construct the server, and exercise the descriptor reader; a native Windows test should verify the actual access control.

2. **Provider-gate failure — confirmed.** `provider.py:196` opens the parent directory after `os.replace`, without catching the open failure. Fresh or changed gate state calls it at `provider.py:288`; account binding occurs at `target_selection.py:800`, before volume discovery and creation. Thus this is an independent failure after the first defect is corrected.

   Replace the `os.replace` and directory-flush block at `provider.py:195–200` with the existing `runtime_protocol.platform.durable_replace(temporary, self.path)`, as used by `worker_preparation.py:163`. A fail-first test should make directory `os.open` raise `EACCES`, exercise fresh gate initialization and a changed state, and verify successful persistence through the platform helper. Include native Windows coverage for the helper’s rename behavior.

**Windows reachability.** Windows is a beta installation target in `docs/getting-started.md:3`; the RunPod pack declares a claim action without a platform restriction. The machine CLI reaches the host adapter, which constructs the owner without a Windows exclusion (`machines_cli.py:383`, `adapter.py:533, 743, 442`). This establishes a supported, source-reachable route, not an end-to-end native Windows success claim. The Windows CI job uses Python 3.11 and runs installer, service/host recovery, Remotion, and selected native process and permission tests (`.github/workflows/ci.yml:19–53`). Those selected test files contain no direct `RunPodLeaseOwner` or `_replace_state` reference; they do not directly test these failures. The testing guide says native Windows end-to-end qualification remains outstanding.

**R12 comparison.** At `0e1543e0`, neither `release_control.py` nor `provider.py` existed; the R12 `RunPodLeaseOwner` constructor did not construct a release-control server. The two specific claim-path failures are new in R13. The reported introducing commits, `4b61f1272` and `0a212484cd`, contain the respective additions. R12 did contain a separate unconditional `os.fchmod` in `generic_host.py:260` on terminal-request persistence paths; this investigation does not establish that Windows was free of other pre-existing failures.

**Simulation output.** With temporary directories, no provider operations, and import-time external symbols stubbed because the local dependency was unavailable:

```text
ReleaseControlServer -> _write_descriptor, release_control.py:99
AttributeError: module 'os' has no attribute 'fchmod'

ProviderGate._replace_state, provider.py:196
PermissionError: [Errno 13] Permission denied: '/tmp/...'
State exists after exception: True
```

The second result matters because the state file had already been replaced when the exception escaped.

Fetched origin, made no tracked edits or pushes, and removed `/home/user/wt/w179-a`.