# Scoped CPU comparisons — 15 November 2026

These are focused task checks against the published Release 13 sources. They are not full-suite qualification, a speed-budget pass, RS1, or the final review. Empty bucket files mean that `env/baseline-diff.py` found no test IDs in that bucket.

| Repository | Checked local candidate | Exact tree | Published baseline | Candidate proof |
| --- | --- | --- | --- | --- |
| astrid-agent | `c1a20a3731dcd454f1e76d34dc99816dfcf36130` | `134921281eaee936178693fb612d4f95c2495668` | `9814193a73f606719e81883a8be197d27dd361d4` | 50 Comfy target cases and 3 selected attached integration cases passed |
| VibeComfy | `35d815eae8b767e4b525f24f9bff800ec74872ee` | `e036602549eca52eb60cc8b3bef5c0598ecb4d5b` | `dba38f8644c46f652376f2cd5112ea161e40f09b` | 6 existing session cases and 10 transport cases passed |

The GitHub connector created commits with different metadata but exactly those checked trees: Agent `bbe65044635a7910e0b9418c1ec866523dd05ac4` ([task PR 349](https://github.com/banodoco/astrid-agent/pull/349)); VibeComfy `b26b018d3b45d66f952053ff92f6634d0c066492` ([task PR 167](https://github.com/banodoco/VibeComfy/pull/167)). Task PRs target `int/55-local-speed`.

Agent's environment used Python 3.13.5, Runtime `6855dfa8df65cf8ae4c002b57134d6505493c17c`, VibeComfy `dba38f8644c46f652376f2cd5112ea161e40f09b`, and lifecycle `7f0b025e9391baac9f5c2fb7393617ea6fef0704`. Its baseline comparison includes 46 test IDs; the candidate includes 53. VibeComfy's comparison includes 6 baseline IDs and 16 candidate IDs. Neither comparison found a regression or missing baseline test.

## Commands

Agent used its own `scripts/worker-env/agent-setup.sh` and `agent-pytest.sh`. The candidate commands were `PYTEST_ADDOPTS=-rA bash scripts/worker-env/agent-pytest.sh -q tests/core/generation/backends/test_comfy_target.py` and `PYTEST_ADDOPTS='-rA -m integration' bash scripts/worker-env/agent-pytest.sh -q 'tests/integrations/test_workflow_file_placements_cpu.py::test_workflow_file_runs_on_each_placement[attached]' tests/integrations/test_local_speed_meter.py`. The first baseline attempt without an explicit integration marker selected no test and is **NO-RESULT**; the corrected, explicitly selected baseline is the one compared here.

VibeComfy used the prepared `env/vc-pytest.sh` environment with `PYTEST_ADDOPTS=-rA`. Existing session selectors in `tests/test_runtime_session_server.py`: `test_server_session_waits_for_history_and_records_outputs`, `test_server_session_does_not_finalize_watchdog_completed_before_history`, `test_server_session_concurrent_runs_get_exclusive_roots`, `test_server_queue_http_200_without_or_blank_prompt_id_fails_without_history_retry`, and `test_server_acceptance_witness_write_failure_is_unknown_discarded` (six cases including parametrization). New coverage was `tests/test_runtime_transport.py` (ten cases). Both commands passed in an independent N rerun on the final clean candidate.

## Limits

LS-2 remains a measurement scaffold: it explicitly records `budget_certified: false`, labels synthetic execution, and leaves unobserved child-process, compile/emission, output-hash and native flush counts unknown. SDK and CLI timing boundaries are reported separately; these tests do not establish comparable performance medians.

LS-5's real upstream terminal-event ordering has not been independently verified; the source-read tool returned `DisabledError` and was not retried. The tests exercise the documented history-ready signal. Agent transport integration, progress consumers and a re-pin remain outstanding. No dependency pin changed in either candidate. Full relevant CI and review remain future gates.

## Partial LS-6 combined candidate

Agent `6e7e0ec9d40d43ab82178000443f05095f708f0e`, tree `618b517c1f0f272039300fe74b6619c2fe8ace95`, adds the host digest-carrying change to the already checked LS-2/LS-11 integration. The connector commit `12ca27d59c779e8c602fc6a7830415e800a06421` in [task PR #351](https://github.com/banodoco/astrid-agent/pull/351) has exactly that tree.

An independent N check passed 45 cases in `tests/core/generation/test_output_delivery.py`, `tests/sdk/test_media_open.py`, and `tests/core/test_generic_host_thumbnails.py`. With the explicit integration marker it also passed the attached-custody selector in `tests/packs/vibecomfy/test_local_server_run.py`, the attached placement selector, and both meter cases: four integration cases. The comparison under `astrid-agent/6e7e0ec/` contains 43 baseline IDs and 49 candidate IDs, with no regressions or missing baseline IDs. Warnings concern the existing legacy template-ref fallback.

The tests exercise a file changed after harvesting being rejected by real Runtime inline staging, attempt-bound upload identity checks, remaining hash passes, truncated caller delivery, and source-aware caller-copy isolation. The manager withheld an SDK materialization optimization rather than change existing reuse semantics; SDK production code is byte-identical to the published base. Global duplicate hashes, buffered transfers, and synchronous thumbnails remain. This candidate does not complete LS-6 or certify a speed target.
