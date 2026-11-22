# Installed attribution and provisional combined-range evidence — 22 November 2026

This is an evidence summary for the host's independent reviewer. It is not a review brief, a final combined-range verdict, or a completion claim. The measurements below are from installed CPU-container runs with a stand-in ComfyUI and `--no-wait`; they stop at task admission and do not include a real ComfyUI node-info answer or GPU work.

## Installed A/B

The retained run has 36 commands: three groups (same-prompt generation, changed-prompt generation, timeline), two arms, and one warm-up plus five measured attempts per arm. All commands succeeded. The summary reports a maximum load gate of 1.0. The before arm did not use `--timings`; the after arm did. Therefore this establishes installed wall-time A/B evidence, while the after-arm stage instrumentation has no instrumented before counterpart and may add some observer overhead.

| Group | Before median | After median | Change |
|---|---:|---:|---:|
| Same-prompt `generate` | 15.007 s | 5.410 s | 64.0% lower (0.36×) |
| Changed-prompt `generate` | 15.217 s | 5.624 s | 63.0% lower (0.37×) |
| Timeline | 1.254 s | 1.172 s | 6.5% lower |

The generation comparison meets the plan's installed threshold of at most 60% of baseline in these two groups. It does not establish a 90% attribution threshold, a one-second generation result, or a timeline-under-one-second result.

Before manifest: Agent `c0ad6b54aadd21630d98bb5039613e37efe92a8f`, Runtime `5120462d67479dc4719406d0d34440edb616ace1`, VibeComfy `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c`, lifecycle `9f88ef7640bc664f697112d966ecefa123d44340`.

After manifest: Agent `bc75d6c592e16582fffc5f1ca1a6aa35508c9ddf`, Runtime `72b129e5a2296dc58360a9896cc65fab9db4ad0c`, VibeComfy `36ea976ffa24ac3ab5b5e48b7b279af7565d5c41`, lifecycle `9f88ef7640bc664f697112d966ecefa123d44340`. These are installed candidate scratch inputs, not the final plan branch. At the time recorded, VibeComfy PR #182 remained open against base `48b5fa9e`; this summary does not change or approve that PR.

## After-arm attribution

The after-arm `--timings` records directly measure the following inclusive operation scopes. Values below are same-prompt medians; nested children are explanatory detail within their parent and must not be added again.

| Measured scope | Median | Notes |
|---|---:|---|
| Model registry | 1.0916 s | Includes pack discovery, median 0.4827 s, as a nested child. |
| Candidate preparation | 1.0602 s | Includes workflow build, median 0.7262 s, as a nested child. |
| Runtime connection | 0.8037 s | Directly timed parent scope. |
| Candidate qualification | 0.5095 s | Directly timed parent scope. |
| Workflow emission | 0.4145 s | Directly timed parent scope. |

These named headline rows sum to 3.8795 s; compared mechanically with the 5.410 s same-prompt wall median, that subset leaves 1.5305 s. For changed-prompt medians the corresponding headline rows are 1.1064, 1.1269, 0.8969, 0.5287 and 0.4231 s (sum 4.0819 s); against 5.624 s wall this subset leaves 1.5421 s. These differences are not the run's full unexplained remainder: other independently measured rows are present in the occurrence records.

Using every recorded exclusive `seconds` occurrence once (not inclusive `total_seconds` parents and children together), the per-process accounting is:

| Group | Per-process W−S range | Median W−S | Median R | Paired median W−C |
|---|---:|---:|---:|---:|
| Same-prompt | 0.700–0.819 s | 0.7212 s (13.1–14.8% per sample) | 0.3957 s | 0.3235 s |
| Changed-prompt | 0.810–0.895 s | 0.8586 s (14.2–15.7% per sample) | 0.4664 s | 0.3921 s |

Here W is process wall time, S is the sum of named measured exclusive rows, R is the unexplained remainder within the collector span, and C is the collector span. Every sample's W−S is above 10%, so the per-sample 10% bound is not met. The paired W−C values are separate: they include time before command-entry timing and after the collector snapshot, and are not attributed to a specific operation. Thus the 90% attribution target is not established by either route.

Direct evidence is the timer output in `summary-ab.json` and captured stdout/stderr. The labels and causal interpretation of measured operation spans are interpretation of those timers; this A/B cannot isolate which repository change caused how much of the wall reduction. In particular, the candidate changed Agent, Runtime and VibeComfy together.

## Provisional combined repository range and evidence state

This is a revision-and-proof inventory, not a conclusion that all work in the range is complete.

| Area | Range / known changes | Evidence and current limits |
|---|---|---|
| Agent | Published baseline `c0ad6b54`; candidate scratch Agent `bc75d6c5`. Candidate lineage includes Plan 69 and the R14 forward, plus Plan 81 attribution/fix work. F-1 and F-3 are included. Current live plan branch noted by the host was `9c95c680e645335a4a2ea8091f02b88934a2492b`. | Source test inventory and focused proofs are recorded in the plan/run logs, including the Plan 69 forward comparison. Do not treat a stale plan task table as final integrated status. A-5 remains an unqualified local observer draft; focused tests had 6 failures and 22 passes due eager witness aliases. Cross-process/full gate evidence is missing. |
| Runtime | Published baseline `5120462d`; candidate `72b129e5a2296dc58360a9896cc65fab9db4ad0c`. This candidate includes Plan 69 and R14 forward work; `182311f9d363712c0339254bd27e091d0e18318d` is an ancestor, not the full candidate range. | Runtime forward source-startup identity inventory was 29 passes on each side. The known portability-lifecycle failures were recorded as inherited. No final CI claim follows from these local comparisons. |
| VibeComfy | Published/base `48b5fa9e`; candidate PR head `36ea976f` for the witness change. PR #182 was still open at the host's 16:05 status. | The installed A/B includes this candidate head. The source harness's three attempts failed its fail-closed attestation: no `consume.py` execution was attested in host/descendants. This is a limitation, not a source timing result. Existing CLI-process witness captures (2,348 calls) and the 53-template count are count evidence only; A-5's exact cross-process budget remains open. |
| App | No clone/candidate was available to this run at the host's 16:05 status. | No App-range or App-proof claim. |

Plan 69's recorded Agent/Runtime forward comparison includes corrected setup-error reruns; its raw details are in `2026-11-22-plan69-forward.md`. A stale early inventory should not be represented as current complete-plan CI. US-2 is still undergoing owner/plan reconciliation, and US-7 remains unverified/ongoing. The evidence available here does not establish final US-2 status, US-7 completion, a full plan CI gate, or completion of A-5/A-6 source attribution.

## Evidence integrity and limitations

Primary retained input: `/root/codex/installed-baseline/evidence/ab-run-1/summary-ab.json`, SHA-256 `a51aead203c163e53ebec18a24b4e93d598ea78737a8f6e812b592ba016efe8b`. The raw directory retains 72 stdout/stderr files, `console.log`, and `records-recovered.jsonl`. The driver's mentioned `records.jsonl` is absent. In recovered records, argv was reconstructed from the console log and raw output; `started_at` is marked approximate from raw-file mtime, and `gate_wait_seconds` is null. Thus argv and starts are not preserved as original driver records, and per-command gate-wait duration is unavailable. The summary script initially raised a `KeyError` and was corrected before the retained summary was produced; the retained JSON parses and its top-level command count is 36. This note relies on the retained summary and file hash, not on missing driver files.

The host's requested source-completeness review and [evidence PR #1422](https://github.com/banodoco/astrid-dev/pull/1422) provide the broader plan context. This document adds only the installed attribution and provisional range inventory. It does not commission a reviewer or state a review outcome.
