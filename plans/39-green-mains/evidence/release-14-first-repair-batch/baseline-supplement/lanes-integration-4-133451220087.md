# Agent Lanes integration shard 4 supplement

Captured from the completed job log for run 43888589840. This supplements the frozen 17:26 snapshot; it does not replace or update that snapshot.

## Provenance

- Repository: `banodoco/astrid-agent`
- Ref and SHA: `release/14/main` at `ab95803ce28fa51eec937b4074f5ec0f0439b98a`
- Run/job: `43888589840` / `133451220087` (integration shard 4 / 4)
- Job completed: `2026-11-16T17:52:43Z`; pytest summary emitted at `2026-11-16T17:52:36.8789095Z`
- [Job evidence](https://github.com/banodoco/astrid-agent/actions/runs/43888589840/job/133451220087)

## Exact outer pytest summary

`= 99 failed, 391 passed, 32163 deselected, 8 warnings, 26 errors in 4064.38s (1:07:44) =`

Counts reconcile to 99 failed test IDs and 26 error test IDs (125 total); 391 passed, 32,163 deselected, and 8 warnings. The full log contains nested pytest output inside escaped `output_tail` strings. Only anchored records in the final outer short-summary block were counted.

## Distinct signatures

The audit retains **55 outcome-scoped full-message groups** (50 failed groups and 5 error groups), covering all 125 IDs. At the first line after pytest’s summary delimiter, these reconcile to **43 distinct literal signatures**; one first-line signature appears for both a FAILED and an ERROR outcome. Full multiline variants remain preserved in the primary groups. The JSON records each complete message, count, node IDs, first-line reconciliation, triage, and disposition. All signatures map to **new — A-b / AT1 unclassified observed signature** under the existing G1 triage logic; these are candidate findings, not proven independent root causes.

| Measurement | Count |
|---|---:|
| Failed test IDs | 99 |
| Error test IDs | 26 |
| Full-message groups (outcome-scoped) | 55 |
| First-line signatures (outcome-agnostic) | 43 |

### Largest full-message groups by outcome ID count

| Count | Outcome | Literal signature (first line; complete message in JSON) |
|---:|---|---|
| 14 | failed | `Failed: Timeout (>120.0s) from pytest-timeout.` |
| 12 | failed | `runtime_protocol.errors.RuntimeErrorBase: selected PARAM authority is unavailable` |
| 9 | error | `IndexError: list index out of range` |
| 9 | error | `subprocess.CalledProcessError: Command '['git', '-C', '/home/runner/work/astrid-agent/astrid-agent/astrid-runtime', 'archive', '6d53a19070faf63fc15ae1f81417722edc2c8a5f']' retur…` |
| 6 | failed | `astrid.installer.core.RuntimeOperationError: Runtime Pinokio interruption refused: no owner or completed-stop evidence.` |
| 6 | failed | `astrid.installer.core.RuntimeOperationError: Runtime interruption refused: owner endpoint or process identity failed validation.` |
| 5 | failed | `astrid.core.rendering.errors.RendererProtocolError: audio preparation requires the managed asset server` |
| 4 | error | `AssertionError: missing qualified authentic G5 archive: /home/user/timeline-hub/hub/design/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz` |
| 4 | failed | `Failed: set ASTRID_RUNTIME_REPO to the local source checkout to run this offline check` |
| 3 | error | `subprocess.CalledProcessError: Command '['git', 'archive', '0e1543e0da2215db9cb3320cfd1083174c3c62a9']' returned non-zero exit status 128.` |
| 3 | failed | `AssertionError: assert [{'blendMode'...'audio', ...}] == []` |
| 3 | failed | `astrid.sdk.timeline._command_state.CommandError: replacement changes provider-managed edges` |
| 2 | failed | `AssertionError: Regex pattern did not match.` |
| 2 | failed | `AssertionError: assert 'label' not in {'blendMode': 'normal', 'fit': 'contain', 'id': 'V1', 'kind': 'visual', ...}` |
| 2 | failed | `AttributeError: 'Runtime' object has no attribute '_last_handshake'` |

## Plan 38 / Plan 55 ownership

No exact failed or error node IDs matched the Plan 38 or Plan 55 inventories used in the existing G1 audit. Their owned work remains **WAITING**; this shard does not justify assigning ownership from test names or neighboring code.

## Evidence and limits

- The complete 4,767,224-byte raw log is retained in the local evidence capture; SHA-256 `43920f54f01ce57e8fc0aaa40091189af8dd5aa0a2080459abecd20a31653a05`. [GitHub job evidence](https://github.com/banodoco/astrid-agent/actions/runs/43888589840/job/133451220087). The full outer message ledger and all node IDs are persisted below.
- Machine-readable audit and complete message ledger: [`lanes-integration-4-133451220087.json`](lanes-integration-4-133451220087.json).
- Shard 4 is one completed job. At capture, integration shard 3 was still running, so the overall Lanes run was not yet a complete result.
- No reruns, repository edits, or remote writes were performed.
- The frozen 17:26 snapshot was not modified; see the [baseline section](../README.md#baseline-retained-including-its-gaps).

Root reconciliation independently matched all 125 outcome/node-ID pairs to the raw outer summary. No nested pytest record was counted as another outer failure.
