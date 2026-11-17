# R14-P55-02 — candidate proof

[Pinned packet](https://github.com/banodoco/astrid-dev/blob/656be69360e8c91cb593589ae20b120028bf7554/releases/14/packets/R14-P55-02.md) · [Plan](../../plan.md) · [Pinned authority](https://github.com/banodoco/astrid-dev/blob/656be69360e8c91cb593589ae20b120028bf7554/releases/14/run.md#authority)

Packet session `r14-P55-02-1`, 17 November 2026. The Lead has integrated the two
pure syncs. The final LS-2 standing meter passes both recorded-reference
comparisons. The separate install-smoke failure and its successful replay
remain recorded below.
The Lead owns review, acceptance and task reconciliation; this evidence makes
no D1 speed or completed-plan claim. No `tasks.md` changes are part of it.

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

The Lead [accepted and merged both syncs](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-6956405239):
Agent merge `561950d084ee71a9b1e5e49be01c21bbbafcd785` and VibeComfy merge
`e5596dcd5ee1b9657acca4c90913c0da7631764a`. Their Git commit objects each have
exactly the tested candidate tree in the table above. This packet session
performed no merge.

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

The exact sync candidate also passed both hosted Windows fresh-install
variants in [run 44109272947](https://github.com/banodoco/astrid-agent/actions/runs/44109272947):
job `134130124785` with long paths off and job `134130125460` with long paths
on. Both include the installed-command/attached-ComfyUI smoke and private
DACL diagnostics. This is a separate install guard, not the LS-2 baseline.

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
edited to make the base green. The original
[BLOCKED](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-6952110654)
was resolved by the [Lead's decision, clause 6](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-6954911390):
accept the pure sync because the six failures reproduce on unchanged base
blobs, and carry their repair to a separate Plan 55 row. Both pure sync drafts
were [submitted for Lead review](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-6955180375).
This disposition does not claim that the six failing cases or hosted CI are green.

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
attempts, COMMIT statements and observed native flushes have a separately
labelled `50% + 10` allowance. Native counts remain distinct from Python
requests and cannot disappear in a comparison. The v2 policy requires the
same OS, workload, dependency commits, callers, tolerance, native coverage
and at least the reference's latency and counter sample counts. This is
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

### Repeated acquisition — Windows PASS, Linux counter failure retained

[Run 44111104582](https://github.com/banodoco/astrid-agent/actions/runs/44111104582)
tested the initial head through merge `3663fd5c667549ae764144866e1354bce46d5c04`.
The GitHub commit object confirms the same `ead505c1` tree as the candidate.
Command: `python -m tests.local_speed_meter_run --output plan55-meter-proof
--timeout 1800 --samples 5 --counter-samples 2`. It uses Python 3.11 and the
unchanged dependency commits above. Both jobs passed the 105 then-current
observer/collector checks, the separate Runtime support selection and native
calibration. The two normal-lane integration deselections are not lost cases:
Windows passed both in the integration step; Linux passed one with its declared
Windows-only case skipped.

[Windows job 134136613016](https://github.com/banodoco/astrid-agent/actions/runs/44111104582/job/134136613016)
passed all **10 latency and four counter cases**, with no failures, errors or
skips. Five-sample overheads are:

| Caller | Median, seconds | Slowest, seconds |
| --- | --- | --- |
| Resident SDK | 99.969 | 102.312 |
| Fresh Python CLI | 48.125 | 56.000 |

The exact, unrounded raw fields needed to reproduce the reference are retained
in [acquisition-44111104582.json](acquisition-44111104582.json), together with
source identities, JUnit outcomes and the original summary's SHA-256. The
complete output-identity and process records remain in the linked artifact.
Windows's measured native attached count is explicitly unobserved. Its separate
native calibration passed with six FileIoFlush completions, zero failed.

[Linux job 134136612257](https://github.com/banodoco/astrid-agent/actions/runs/44111104582/job/134136612257)
passed all **10 latency cases** and both CLI counter cases. Both instrumented
SDK cases exceeded the existing **600-second pytest limit**; counter results
were two failed / two passed. The outer capture completed with exit 1, not
timeout 124. The summary remains NO-RESULT and no complete Linux baseline
was fabricated from those partial counters. Native calibration separately
passed with nine completed flushes, zero failed.

Both artifacts were downloaded and their ZIP digests verified. Extracted
Windows evidence files also match the retained SHA256SUMS manifest.

| OS | Artifact | Verified ZIP SHA-256 |
| --- | --- | --- |
| Windows | [14347147925](https://github.com/banodoco/astrid-agent/actions/runs/44111104582/artifacts/14347147925) | `f9f85595c7e2e6a1d3622771c580a334a2f40bc0b0346e5f7c5da89f0fd9831b` |
| Linux | [14346966205](https://github.com/banodoco/astrid-agent/actions/runs/44111104582/artifacts/14346966205) | `9b463b09b51b336b692c4ebe7df5c881c43284a7a0f281c649fbce360c13aa00` |

### Targeted Linux retry and required Windows comparison

The retry is published at `46024d467df98b81621012afdb7e8fcd36ef9f2d`, tree
`5b0c1234452a2efa883572af85b5c73b105a4d9e`, exactly matching local checked
commit `6f55afc1964aa033e65933dccb1404b818f48edc`. It adds strace's
`--seccomp-bpf` kernel filter for the existing process/fsync/fdatasync selection.
Without this filter, choosing the printed syscall set still incurs unrelated
ptrace stops; see [upstream strace internals](https://github.com/strace/strace/blob/master/doc/INTERNALS.md).
The SDK timeout stack reaches recursive conversion under the Python observer;
the same observer finishes on Windows without Linux syscall tracing. Those
observations motivated the kernel-filter correction; its result is below.
The per-PID trace, reader checks, timeouts, sample counts and assertions remain.

The committed [Windows reference and provenance](https://github.com/banodoco/astrid-agent/tree/46024d467df98b81621012afdb7e8fcd36ef9f2d/tests/fixtures/local-speed-baselines)
exactly reproduce the downloaded raw Windows records with the v2 helper.
Conversion from the artifact's v1 baseline adds explicit unobserved native
coverage without changing measured numbers, source commits or tolerances.
That retry workflow required the Windows reference comparison and kept Linux
in explicit acquisition mode for its complete counter run.

The assembled retry passed **110 focused cases, two existing default-lane
deselections**, using the command above plus
`tests/core/generation/test_local_speed_native_reader.py`.
[Complete status inventory](meter-retry-focused.txt). YAML, all embedded
Python, reference-policy validation and diff checks passed. Local native
calibration remained NO-RESULT because the container denies PTRACE_TRACEME
with Operation not permitted; the [original refusal](local-native-refusal.txt)
is retained. No privileges were changed. Hosted calibration is required.

### Retry results — both jobs PASS

[Run 44127948473](https://github.com/banodoco/astrid-agent/actions/runs/44127948473)
passed both jobs. The actual tested merge was
`6bbc74dbe43e5244e3973e0ea303bd92e53211ac`; its GitHub commit object verifies
the same `5b0c1234` tree as head `46024d46` and the locally checked candidate.
[Exact raw fields and JUnit outcomes](retry-44127948473.json) are retained
without rounding, including native counts, calibration, source identities and
the raw summary SHA-256 values.

| OS | Job | Meter cases | Reference result |
| --- | --- | --- | --- |
| Linux | [134196776058](https://github.com/banodoco/astrid-agent/actions/runs/44127948473/job/134196776058) | 10 latency + four counter cases passed, zero failures/errors/skips | Complete reference acquired; comparison not requested |
| Windows | [134196776550](https://github.com/banodoco/astrid-agent/actions/runs/44127948473/job/134196776550) | 10 latency + four counter cases passed, zero failures/errors/skips | Stored reference PASS, zero regressions |

Both OSes passed **110 focused oracles**, with the same two default-lane
integration deselections. Separate Runtime support passed two cases on Windows;
Linux passed one and skipped the declared Windows-only case. Native calibration
passed on both systems: nine successful flushes on Linux, four FileIoFlush
completions on Windows, zero observed failed flushes or gaps.

Linux's two SDK counter cases took **90.679 and 84.044 seconds**, within the
unchanged 600-second limit; both had previously timed out. CLI cases took
63.985 and 63.616 seconds. The full counter capture took **307.813 seconds**,
exit 0. Native observations remain complete: each SDK sample has **161**
completed flushes and each CLI sample **160**, with no failures or gaps.
The corresponding Python force-request count is **150**; the quantities are
reported separately. The tracing correction affects the instrumented run;
changes in uninstrumented latency between runners are not attributed to it.

Windows's actual reference comparison passed with median/slowest overhead
**59.641 / 64.828 seconds for SDK** and **31.609 / 33.000 seconds for CLI**.
It retained the original reference instead of resetting to the faster repeat.
Both caller counter samples still observe 25 output hash streams, 84 Python
force requests and 13 Comfy requests. Attached native Windows flushes remain
unobserved; the separate native calibration does not qualify them.

Both ZIP digests and every extracted manifest entry were verified:

| OS | Artifact | Verified ZIP SHA-256 |
| --- | --- | --- |
| Linux | [14353432178](https://github.com/banodoco/astrid-agent/actions/runs/44127948473/artifacts/14353432178) | `444dedb9e04bcd2bc64a230eedc7eca984e14037099fd34f1cf664ab20752ece` |
| Windows | [14354311252](https://github.com/banodoco/astrid-agent/actions/runs/44127948473/artifacts/14354311252) | `6abab98ff7e7cc8d79da015b4086cc6be527824fbdaf2ad5173ff4f82a5b2aa3` |

### Required standing comparison on both systems

Final standing candidate: `820fe62af8295b15aa5d58b66d8b1f5b19892395`, tree
`1eabe717ec5c9f1ee7d6aa835d4c23a5f3fec986`, identical to local checked commit
`86cfab59fae0484ddba0af7f01efe0d7922293dc`. Its only changes after the passing
retry are the Linux reference, reference provenance README and workflow.
The [committed references](https://github.com/banodoco/astrid-agent/tree/820fe62af8295b15aa5d58b66d8b1f5b19892395/tests/fixtures/local-speed-baselines)
are exactly reproduced from verified raw records with the v2 helper:

| OS | Caller | Samples | Median overhead, seconds | Slowest overhead, seconds |
| --- | --- | --- | --- | --- |
| Windows | Resident SDK | 5 | 99.969 | 102.312 |
| Windows | Fresh Python CLI | 5 | 48.125 | 56.000 |
| Linux | Resident SDK | 5 | 22.438 | 22.617 |
| Linux | Fresh Python CLI | 5 | 16.920 | 16.991 |

Both OS jobs now require their recorded reference and fail if the file is
missing. Relevant product changes trigger the workflow. The acquisition-only
product freeze is removed so later optimizations can be tested; exact
dependency source-byte checks and identity comparison remain. Samples,
tolerances, counters, output assertions and dependency commits are unchanged.
Final workflow YAML, embedded Python, raw-reference equality/policy checks and
diff checks passed locally. The underlying helper/oracle code is the same as
the passing hosted retry.

[Final run 44140495768](https://github.com/banodoco/astrid-agent/actions/runs/44140495768)
is **SUCCESS on both OSes** at candidate `820fe62a`. The actual tested merge
`db037ee418b36edae7391100fa2d5f7ec43507cd` has exactly tree `1eabe717`, matching
the published and locally checked candidate. Both summaries report
`baseline_status: PASS`, the required OS reference path and
`baseline_regressions: []`. Both have **10 latency and four counter cases,
zero failures, errors or skips**. Each OS also passed 110 focused oracles and
its separate Runtime support/native calibration checks, with the previously
declared Runtime-support platform skip on Linux.

After the Lead's Agent sync merge, GitHub's current PR merge result
`2a883acbe689ee4e592c846caec3811a00ca96c3` has parents `561950d0` and
`820fe62a`, and still has exactly the tested tree `1eabe717`. The base
integration therefore does not change the measured candidate's file tree.

The final [raw proof fields](final-44140495768.json) retain full-precision
timings, counts, source IDs, native observations, counter-case results,
reference-file digests and original-summary digests. Recomputing both
comparisons from those raw records reproduces the PASS results.

| OS | Caller | Reference median / slowest, seconds | Final median / slowest, seconds |
| --- | --- | --- | --- |
| Linux | Resident SDK | 22.438 / 22.617 | 22.058 / 22.698 |
| Linux | Fresh Python CLI | 16.920 / 16.991 | 16.859 / 16.952 |
| Windows | Resident SDK | 99.969 / 102.312 | 83.797 / 84.609 |
| Windows | Fresh Python CLI | 48.125 / 56.000 | 42.125 / 42.328 |

Each timing distribution has five samples. Counter maxima across two separate
samples per caller are:

| Metric | Linux SDK | Linux CLI | Windows SDK | Windows CLI |
| --- | --- | --- | --- | --- |
| Pack-worker starts | 1 | 1 | 1 | 1 |
| Fresh CLI starts | 0 | 1 | 0 | 1 |
| Other external starts | 7 | 7 | 5 | 5 |
| Workflow compiles | 8 | 8 | 8 | 8 |
| Bundle compiles / emissions | 2 / 3 | 2 / 3 | 2 / 3 | 2 / 3 |
| Comfy HTTP requests | 13 | 13 | 13 | 13 |
| Output hash streams | 25 | 25 | 25 | 25 |
| Python force requests | 150 | 150 | 84 | 84 |
| Native completed fsync/fdatasync operations | 161 | 161 | Unobserved | Unobserved |
| Sleep attempts | 158 | 156 | 252 | 258 |
| Runtime COMMIT statements | 1381 | 1301 | 1518 | 861 |

Linux native coverage has zero failed flushes or gaps. The calibration again
observes nine completed flushes. Windows's separate calibration sees four
successful FileIoFlush completions; that does not qualify native attribution
inside its meter. All deterministic counters pass their recorded caps; sleep,
COMMIT and observed native counts pass the disclosed background allowance.
`budget_certified` remains false on both OSes.

| OS | Job | Verified artifact | ZIP SHA-256 |
| --- | --- | --- | --- |
| Linux | [134241636341](https://github.com/banodoco/astrid-agent/actions/runs/44140495768/job/134241636341) | [14356430304](https://github.com/banodoco/astrid-agent/actions/runs/44140495768/artifacts/14356430304) | `27531bfac4f6998d7b7d5a08fd8cb954ae625610fa58be2831a677dc7f4dda42` |
| Windows | [134241636180](https://github.com/banodoco/astrid-agent/actions/runs/44140495768/job/134241636180) | [14357113308](https://github.com/banodoco/astrid-agent/actions/runs/44140495768/artifacts/14357113308) | `d21e30a55db19d445dabcfe95ad16857f6936f07928d48482dc6116d2a9918c6` |

Both ZIPs and all selected extracted SHA256SUMS entries verified.

### Separate Windows installed-smoke failure and bounded replay

The automatically triggered [fresh-install guard run 44140495640](https://github.com/banodoco/astrid-agent/actions/runs/44140495640)
has an additional result outside the standing-meter comparison. Attempt 1's
[long-paths-on job 134241634426](https://github.com/banodoco/astrid-agent/actions/runs/44140495640/job/134241634426)
passed real installation, TLS and DACL checks, then failed
`generate defaults --json` with exit 2 and
`host native process metadata unavailable; field=registered_host`.
The CLI reports blocked/unavailable with `runtime_lifecycle_error`.
Long-paths-off job `134241634915` passed.

The immediately preceding candidate `46024d46` passed both install variants
in [run 44127948431](https://github.com/banodoco/astrid-agent/actions/runs/44127948431),
including long-paths-on job `134196776048`. The effective Runtime
`6855dfa8df65cf8ae4c002b57134d6505493c17c` and App
`de7dd1e668aa6dcf3cbce013c701fa7c76615f99` commits match between those jobs.
Agent's only intervening changes are the native-meter workflow, reference
README and Linux reference. Product, install workflow, smoke/journey helpers,
Runtime lock and packaging bytes are unchanged; the same long-path mode and
long user-like directory were used.

The failure's [verified diagnostic record](install-guard-44140495640.json)
retains its captured CLI output and source/file identities. Artifact
`14357140100` ZIP SHA-256 is
`bac59a6c72ee18a32497cabb56e080d2bae9269bb52934fe888c7ac7c729d8c7`.
The native guard catches errors from executable, argv or identity lookup;
the exposed message does not identify the particular failing query or OS
error. Matching inputs and prior passes do not establish its cause.

The original failure is retained. One bounded replay of only the failed leg
was requested at the same Agent head. Attempt 2 completed **SUCCESS**:
[replay job 134274341401](https://github.com/banodoco/astrid-agent/actions/runs/44140495640/job/134274341401)
passed real installation and the full installed-command/attached-ComfyUI
smoke. The log confirms a healthy Runtime belonging to this installation and
a running pack-host with its current ready file. Its effective Agent merge
`db037ee4`, Runtime `6855dfa8` and App `de7dd1e6` exactly match attempt 1.
The latest-attempt listing also reports long-paths-off job `134274343588`
successful; no claim is made that this already-passing variant was rerun.

The diagnostic JSON now retains the replay's full step inventory, source
identities, success receipt lines and fetched-log SHA-256. The successful
replay emits no artifact because the failure-only upload is skipped; the
original failure artifact remains available. No source, pin, selector or
assertion was changed. A successful replay does not identify the original
failing metadata query or OS error. Any native lifecycle product repair
remains separate Lead work, as requested in
[BLOCKED 6957369016](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-6957369016).

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
