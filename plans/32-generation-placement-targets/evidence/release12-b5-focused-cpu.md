# Release 12 B5 focused CPU receipt

This receipt records focused checks, not B5 acceptance or a release gate pass.

The Agent merge was `1439ccc63bf8d9ed5422ac1f95ffdd6158560e1e`, with parents `6a2351d95bb7eabc8b0ff6f988163fe420fcb3d7` and `e1731b9e4e86638e6425cf5601160e32be683a72`. The checked Runtime was `8b312c4b29bbb4fef5ac0849188678fe356b9e84`, VibeComfy `8d065a8fef3dd602d5462e27d8eca088cf4e8262`, and lifecycle `f2948817eeb94af8dee76be21f6d673724f1606e`.

On 11 November 2026, the focused run from 16:39:01 to 16:40:05 UTC exited 1: 17 cases passed and the self-attach integration case failed. The test environment had imported an older Runtime schema before the fixture added the requested checkout. The second run from 16:42:04 to 16:42:18 UTC put the exact Runtime checkout first on Python's startup path, verified its import origin and schema digest `sha256:2b23a675a0b6f9747a7fae1b8fe3b8e9f91741002a6d3022e02a50dace42188d`, and passed the self-attach case (1 passed, exit 0). The prior 17 cases were not rerun.

The initial selection used `python -m pytest -p no:cacheprovider -q -m ''` with:

- `tests/packs/runpod/test_failure_diagnostics.py::test_job_failure_crosses_cli_frame_and_journal_without_private_text`
- `tests/test_producer_evidence_f06.py::test_failed_producer_receipt_survives_executor_to_safe_remote_frame`
- `tests/core/generation/test_pod_owned_preparation.py::test_execution_failure_closes_preparation_and_removes_scratch`
- `tests/core/generation/test_readiness_inputs_f04.py::test_generation_error_uses_explicit_sdk_category`
- `tests/core/generation/test_readiness_inputs_f04.py::test_legacy_sdk_validation_also_exposes_the_shared_envelope`
- `tests/test_mcp_generation_parity.py::test_generation_mcp_rejects_non_object_inputs_before_invocation`
- `tests/packs/runpod/test_setup_lifecycle_probe.py`
- `tests/sdk/test_host_attach_rejection.py`

The rerun selected `tests/sdk/test_host_attach_rejection.py::test_serialized_runtime_registration_attaches_and_tampering_refuses` only. Both used a 120-second timeout. The local command and log files are not checked in; their SHA-256 values identify the original receipts if retained:

| Local file | SHA-256 |
|---|---|
| `run.sh` | `88ef1a1912a4f7a944bf2c918331c7cd19a543f7f8366638b70faa039feff8d2` |
| `proof.log` | `24203bd821d9122f778b891ffc1722c4507530322a8eea77a7266ea341cc51d4` |
| `self-attach.sh` | `687bb2e0d690c9f9e4cdeb151351e5742e2589c3242c8fa8d8041955ad3dce1e` |
| `self-attach.log` | `8dbc7c52f7c219628d532b56f8a18ed0a79a8cde00a4c770b97c087a6b7c0493` |

Other B5 and release gates remain open; the Runtime pin is provisional.
