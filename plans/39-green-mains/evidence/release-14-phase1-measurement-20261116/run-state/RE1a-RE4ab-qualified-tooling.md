# Exact Agent package and remaining compiler wiring

Manager `/root`; follow-up messages are part of the brief. Never ask the user questions. Route X (`gpt-6.1-terra`, high): N's first pin proof did not verify the installed package and the first compiler proof hit that old dependency. Reading helpers may be delegated to N if a slot becomes available; no overlapping writers.

Sole editable repository `/workspace/scratch/cd53b069f320/p39-repair/astrid-runtime`, start `eeb84ef511272e772250cb1b5da2414fc16c00ac`, tree `2f5a647cf1d7496d8de65bc05da9c0946fe77a3a`. This unpublished one-line test pin now selects released R12 Agent `0e1543e0da2215db9cb3320cfd1083174c3c62a9` (plan RE1 allows this because previous b05 was Release 1). Branch `p39/re1a-re4ab-tooling`, additive commits only. No push, PR, merge or workflow dispatch.

First fix evidence/environment provenance. The prepared Agent checkout is at the correct R12 commit, but the environment's Agent is a non-editable installation at `venv/lib/python3.13/site-packages/astrid`. N's source-verification incorrectly called it editable; raw installed-module-provenance and pip-freeze contradict that. Install the verified checkout into the existing Runtime venv using the canonical `--no-deps` behavior, preserving Runtime and dependency versions (a forced reinstall is appropriate). Verify actual installed timeline modules/helper bytes against that exact Git tree and import provenance without prepending the source path. Append a correction; retain old logs and false claim as superseded evidence, not silently rewritten history.

Then repair two measured environment causes, without changing any test, assertion, marker, selection or product:

1. `.github/workflows/nightly.yml`: add Node 22, `npm ci` in `packages/typescript`, and locked `node_modules/.bin` on GITHUB_PATH matching CI unit. Preserve strict selected-Agent equality, full histories, historical321cef warning, all test selection and SF3a result summaries/artifacts.
2. `tests/seccomp/container-entrypoint.py`: npm ci already installs the locked compiler; prepend the copied workspace's `packages/typescript/node_modules/.bin` to the `env` passed to pytest. Keep sandbox user, mounts, environment, command/arguments, subprocess return code and all other provisioning unchanged. Four hosted failures are missing bare tsc; do not alter their tests.

Evidence: Nightly43938386391/job133548961758 has3tscerrors; CI43938386357/sandbox133548963680 has4tscfailures. Full logs/ledgers in `p39-g2-evidence/runtime/`. Original RE4's two files pass110 and hosted units have0tscerrors. No live Docker is available.

Exact focused proofs after package correction and wiring edits (no broad suites):

```sh
bash scripts/worker-env/runtime-pytest.sh -q -m "" tests/test_operation_handle_integration.py
bash scripts/worker-env/runtime-pytest.sh -q tests/test_timeline_clip_replacement.py
bash scripts/worker-env/runtime-pytest.sh -q tests/test_timeline_commit_type_generator.py tests/test_timeline_document_object_contract.py
```

Baselines already retained: operation file3missing-capture errors at old pin, then3passes with source checkout updated but installed copy not qualified; clip file old missingcapture, then10strictxfail/17deselected and exit1because no passes. Preserve these distinctions. If a new substantive product/test failure appears, record its full output and stop that cause card; no expectation fixes in this scope. For wiring, inspect YAML and Python syntax and demonstrate the exact new PATH resolves the repository compiler; local focused proofs are not live-Docker or hosted acceptance. Do not invent a simulated full Docker pass or write redundant implementation-mirroring tests.

Save complete raw logs/exit codes, current Python/Node/tsc, source and installed package provenance, full diff and commit/tree under `p39-g2-evidence/runtime/re1a-re4ab-tooling/`. Root will independently read diff and commission review before publishing the batch. Formal RS1 remains0/1.
