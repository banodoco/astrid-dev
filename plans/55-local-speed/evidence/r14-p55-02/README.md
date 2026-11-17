# R14-P55-02 — candidate proof

[Pinned packet](https://github.com/banodoco/astrid-dev/blob/656be69360e8c91cb593589ae20b120028bf7554/releases/14/packets/R14-P55-02.md) · [Plan](../../plan.md) · [Pinned authority](https://github.com/banodoco/astrid-dev/blob/656be69360e8c91cb593589ae20b120028bf7554/releases/14/run.md#authority)

Packet session `r14-P55-02-1`, 17 November 2026. These are scoped candidate
checks, not integration, independent review, a completed plan, or a D1 speed
claim. The Lead owns acceptance and task reconciliation. No `tasks.md` changes
are part of this evidence.

## Pure branch synchronization

| Repository | Plan parent | Release parent | Published candidate | Exact tree | Draft |
| --- | --- | --- | --- | --- | --- |
| Agent | `cb1a590e0008dde7e3fc2d3fbf341ef98401b32a` | `fc391dea696ec5799db222799a34f9de6a69659b` | `d10ebd15dbdbc831e4579dab937b7cb46c616cc9` | `58b795e354854eeef0bb12bfaa0dc12ad7a9c947` | [#379](https://github.com/banodoco/astrid-agent/pull/379) |
| VibeComfy | `7fde33e2523281f840121b93a8a865a7f5d847de` | `aee8bd825c619cfb516feb63d38f500aa4ddb4d7` | `f6a6f189bade2ee8f20b2504174c551454175073` | `1e674eae343b1db855de70325de22fb419079cb3` | [#173](https://github.com/banodoco/VibeComfy/pull/173) |

Both branches are `p55/sync-r14-main` and target `release/14/plan-55`. Git's
ordinary merge succeeded without conflicts. Each remote commit has both named
parents and exactly the locally merged tree, with no extra edits. The local
commits checked were Agent `5e24938d98859a27a4277a7539be2284084bacb0` and VibeComfy
`5e9f96a028c6f9aeceafd99c9db3210f550d53a5`; the connector-created commits differ
in commit metadata only. VibeComfy changes only its PR template and two workflow
files; its product and test bytes equal the plan parent.

### Agent CPU checks — PASS

Command, from the Agent sync checkout:

```sh
PYTEST_ADDOPTS=-rA bash scripts/worker-env/agent-pytest.sh -q \
  tests/core/generation/backends/test_comfy_target.py \
  tests/core/generation/test_output_delivery.py \
  tests/core/test_generic_host_thumbnails.py tests/sdk/test_media_open.py
```

Result: **97 passed, one warning, exit 0**. [Every final status](agent-sync-cpu.txt)
is retained. The warning is the existing legacy template-ref fallback. This
covers the plan's input custody, output delivery, thumbnail and SDK-copy
contracts; it is not an entire Agent-suite result. The ordinary worker setup
used Python 3.13.5, Runtime `6855dfa8df65cf8ae4c002b57134d6505493c17c`,
VibeComfy `dba38f8644c46f652376f2cd5112ea161e40f09b`, and lifecycle
`7f0b025e9391baac9f5c2fb7393617ea6fef0704`, fetched at and verified against the
unchanged checkout pins. Test execution time is not generation-speed evidence.

### VibeComfy CPU checks — existing failures, no demonstrated regression

Command, from the VibeComfy sync checkout, using the existing astrid-dev
`env/vc-setup.sh` / `env/vc-pytest.sh` environment and frozen lock:

```sh
PYTEST_ADDOPTS=-rA bash <astrid-dev>/env/vc-pytest.sh -q \
  tests/test_runtime_transport.py tests/test_runtime_session_server.py \
  tests/test_runtime_session_validation.py tests/test_workflow_bundle.py
```

Python 3.13.5; **221 passed, six failed, exit 1**.
[Candidate final statuses](vibe-sync-cpu.txt). The exact six failed node IDs
were rerun on a detached checkout of the plan parent, using the same installed
dependencies, that checkout on `PYTHONPATH`, a separate pytest temporary
directory and `-p no:cacheprovider -q -rA`: **six failed, zero passed, exit 1**.
[Base final statuses](vibe-baseline-failures.txt).

The canonical `env/baseline-diff.py` [comparison](vibe-comparison/summary.md)
reports zero regressions, six pre-existing failures, zero missing tests.
Only the failing six were rerun on the base; this does not claim 221 base
passes. The affected implementation and test files are byte-identical across
the sync. The failures are:

| Existing cases in `tests/test_workflow_bundle.py` | Observed cause on both candidates |
| --- | --- |
| `test_derived_template_live_identity_requires_package_lock_and_checkout[False-True-True-True]`, `[True-False-True-True]`, `[True-True-True-True]` | The fixture changes `workflow_bundle.__file__`, but lock authority is resolved through `node_packs._lockfile.resolve_lockfile_path()`. Its expectations do not match the effective authoritative lock. |
| `test_v2_companion_keeps_generated_python_small_and_round_trippable` | Expects `wf = wf.finalize({}, outputs=[])`; the unchanged emitter writes `return wf.finalize({}, outputs=[])`. |
| `test_v2_source_contract_rejects_whole_file_integrity_mutations` | The same old source-shape assertion fails before its mutation check. |
| `test_v2_rebuild_refreshes_edited_model_requirement` | Expects a model-name string; the unchanged emitter returns the model metadata mapping. The node input changes correctly. |

The packet requires a pure merge, so these tests and product files were not
edited to make the base green. The passing-inventory requirement remains
unproven and is reported to the Lead in
[BLOCKED](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-6952110654).

Hosted baseline comparison also preserves existing failures:

| Gate | Sync run / job | Plan-base run / job | Same first error |
| --- | --- | --- | --- |
| CI install | [44108561807 / 134127547772](https://github.com/banodoco/VibeComfy/actions/runs/44108561807/job/134127547772) | [43892170816 / 133386017046](https://github.com/banodoco/VibeComfy/actions/runs/43892170816/job/133386017046) | No matching `runpod-lifecycle>=0.3.1.dev0,<0.4` distribution; `install-ci` exits before the tests. |
| Canonical parity | [44108561873 / 134127546357](https://github.com/banodoco/VibeComfy/actions/runs/44108561873/job/134127546357) | [43892170815 / 133386015992](https://github.com/banodoco/VibeComfy/actions/runs/43892170815/job/133386015992) | `Tracked repository root does not match the Makefile allowlist.`; parity does not run. |

## LS-2 cause and bounded repair

The inherited draft [Agent #359](https://github.com/banodoco/astrid-agent/pull/359)
matched the board's `d083878970ef1ac04ff11426b8c716397d675a6d` before mutation.
The [original Windows job 133594213473](https://github.com/banodoco/astrid-agent/actions/runs/43951310565/job/133594213473)
passed the two uninstrumented latency tests and native calibration (five
completed FileIoFlush operations). The attached capture then reported
`decode_exit: 124` and `RuntimeError: instrumented attached meter/capture
failed; retained native/proof.log`. WPR start/stop succeeded. Its native
attached count is **NO-RESULT**, not zero. Artifact `14269207422` retains the
roughly 503 MB original proof; this packet did not download that large archive.
Linux job `133594213925` passed its single-sample meter and native calibration.

The pinned packet explicitly assigns native Windows trace work to LS-13.
The standing meter therefore runs its bounded Python process/counter capture
on Windows without invoking the system-wide WPR decode. Linux retains native
strace counts. The original strict Windows path remains available with
`--native all`: loss checks, flush/OpEnd pairing, failed-flush checks and
unknown-as-unknown behavior remain. No native reader assertion was weakened.

Python `fsync`/`fdatasync` attempts, successes and errors, Runtime COMMIT
statements, and completed native OS flushes are different reported quantities.
The first is not used to invent the third. COMMIT statements include background
activity and are not claimed to be successful transactions or SQLite flushes.
HTTP coverage remains the observed Comfy stand-in paths. The output fixture is
a valid 16-by-16 PNG, not the one-megapixel D1 workload or GPU inference.

The collector now accepts repeated caller samples, requires all sample IDs and
JUnit cases, and reports median and slowest overhead. It subtracts only the
stand-in execution span; queue time remains reported and is never silently
subtracted. Timing uses uninstrumented runs; counters use separate runs with
the original output and distinct-succeeded-task assertions.

The reference policy was fixed before measurement: median overhead at most
`1.5 * reference + 3 seconds`; slowest at most `2 * reference + 5 seconds`.
Deterministic operation counts may not increase. Existing background sleep
and COMMIT counts have a separately labelled `50% + 10` allowance. This is
the standing regression baseline for today's path; `budget_certified` stays
false until the design budget and later speed work are qualified.

Initial repeated-meter candidate: `26c664d435b04ac0f44443cbc3fc6686ca2f4df0`,
tree `ead505c1ab097eec7ff9d383becad60fbd868eee`, equal to local
`95867fed31a86292b97aa1375bcaea3b4f05594e`. Its additive merge
`3a418a45f02bda070b10727863e44241906818d6` includes Agent sync #379;
the Lead should integrate that sync first. The focused observer/collector
and initial-baseline policy selection was **91 passed, two deselected, exit 0**
([status rows](meter-calibration.txt)). Those two default-lane deselections
are the separately invoked existing Runtime-support integration tests in CI.
The focused command, from the meter worktree and the unchanged worker
environment above, was:

```sh
PYTHONPATH="$PWD:<agent-env>/runtime:<agent-env>/runtime/packages/python:<agent-env>/vibecomfy" \
ASTRID_RUNTIME_CHECKOUT=<agent-env>/runtime \
<agent-env>/venv/bin/python -m pytest -q -rA \
  tests/core/generation/test_local_speed_meter_collector.py \
  tests/core/generation/test_local_speed_baseline.py \
  tests/core/generation/test_local_speed_process_observer.py \
  tests/core/generation/test_local_speed_hash_observer.py \
  tests/core/generation/test_local_speed_report_capture.py \
  tests/core/generation/test_local_speed_runtime_support.py \
  tests/core/generation/test_local_speed_schema_encoding.py
```

The exact Linux/Windows measurement run is
[44111104582](https://github.com/banodoco/astrid-agent/actions/runs/44111104582);
both jobs remain queued as of 15:29 UTC on 17 November. Its command is
`python -m tests.local_speed_meter_run --output plan55-meter-proof --timeout
1800 --samples 5 --counter-samples 2`. The workflow uses Python 3.11 and the
same exact Runtime, VibeComfy and lifecycle pins listed above. The first run
records a reference; it does not yet claim a reference comparison. A subsequent
candidate must retain the measured per-OS references, require the comparison
in CI, and pass it before the packet's standing-baseline proof is complete.

A local one-sample iteration completed two latency and two counter cases with
no failures, errors or skips. It verified each delivered PNG and both distinct
succeeded task records. It ran `--native none` in this Linux container and is
only a harness check, not a hosted baseline, native-write proof, or a final
candidate qualification. Local timings are not used to set hosted thresholds.

The historical oracle run and offline replay identity required by the packet
are retained in [E6 of the existing evidence](../continuation-20261116/approved-implementation-followup.md#e6--identities-retained-from-superseded-draft-783).

Routes used: N for research; N for scoped baseline testing; X for direct
implementation, override Astra. The detailed local JSONL is self-reported
and is not published. No review round was commissioned or consumed.
