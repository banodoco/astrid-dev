# SV-4 profile: what `provider_commit` and `port_store_accept` spend on a warm 300-clip save, 24 November 2026

Same package, candidate and overlay as the [combined run](../2026-11-24-sv4-combined-run/README.md), approved by the Plan 89/77 orchestrator for one repetition in profile mode: package astrid-dev `release-15/p77-sv4-combined-package` head `9667048eb3f6b0e5decb4735a92d7c60ce5fd289` (digest `9a012700e773c31a9827d4245e7dea31dfea6064d0567c8ee95f97231dea1a3c`), Runtime `eb4e8644e3549c88d5d836cd5738ca75e76d311a` (instrumented), Agent `096a2fb3536192785fabd33e6673ba8ab4ef5ead` two-file overlay. **The only difference from the approved shell is the environment of the last command: `SV3_PROFILE=1` added and `SV3_REPETITIONS=1` instead of 3** (the profile mode forces one repetition anyway). One attempt, 02:41Z to 02:46Z, exit status 0 (`run-stdout.log`); idle-safe stop verified, ports closed, no Chrome, boundaries unchanged, disk minimum 16.62 GiB (stop 16 GiB). py-spy 0.4.1 attached to all four saves at 100 Hz with threads (17,825, 8,938, 6,974 and 7,866 stack samples; one sampling error in the cold save, none in the others; `profile-attach-summary.json`).

Timings of this repetition (release to Saved; POST to 200 in brackets): cold 15.7 s (12.8), W1 8.6 s (6.3), W2 7.5 s (5.8), W3 8.2 s (6.0), no refusal; B5 last edit to Saved 28.4 s, B10 60.8 s (no sampler during bursts). The profiled warm saves are about 1 s slower than the unprofiled ones of the combined run (5.1 s), which is the sampler's effect plus run-to-run spread.

## Method (thread selection and stage classification)

- **Thread:** the commit request thread is the one non-`MainThread` thread with the most samples whose stack holds a `timeline_commit*` frame (it is a `process_request_thread`, or the lifetime-reaper thread in two earlier profiles). Its samples summed to 12.7 s (cold), 6.4, 5.4 and 6.2 s (W1 to W3), against Runtime wall time in the timing lines of 12.8, 6.3, 5.8 and 6.0 s (`rep-1/timing-sink/commit-stage-timings.jsonl`).
- **Stage of a sample** (`analyze-stages.py`): `port_store_accept` if the stack passes `accept` in `timeline_commit_port.py`; else `provider_commit` if it passes `_execute` in `timeline_commit_execution.py` at lines 655 to 680 (the `provider.commit(...)` call); else `durable_reconciliation` if that frame is at line 690 or later; else initial lookup or handler/other. A sample inside `port.accept` is counted only in `port_store_accept`, like the exclusive timings. Its group is the innermost matching frame (`analyze-stages.py`); call sites are the nearest Runtime or Agent source frame above the library frame (`analyze-callsites.py`). Raw outputs: `profile-stages.txt`, `profile-callsites.txt`.

## Seconds by stage and group (profile) with the Runtime's own timing for the same save

| | cold | W1 | W2 | W3 |
| --- | --- | --- | --- | --- |
| **`provider_commit`** (profile / timing line) | 9.65 / 9.65 | 3.00 / 3.15 | 2.89 / 3.04 | 3.07 / 2.93 |
| patch capture and payload (Agent `_commit_patch`, `_doc_patch`) | 0.89 | 0.83 | 0.76 | 1.02 |
| copy and compare (`value_equal`, `deepcopy`) | 0.74 | 0.93 | 0.73 | 0.70 |
| jsonschema | 0.56 | 0.53 | 0.62 | 0.58 |
| JSON encode and decode | 2.33 | 0.38 | 0.27 | 0.28 |
| auth and value validation | 1.28 | 0.03 | 0.14 | 0.21 |
| old-history verification | 1.19 | 0 | 0 | 0.01 |
| SQLite | 0.66 | 0 | 0 | 0 |
| other | 2.00 | 0.30 | 0.37 | 0.27 |
| **`port_store_accept`** (profile / timing line) | 1.99 / 2.11 | 2.49 / 2.24 | 1.71 / 1.91 | 2.20 / 2.14 |
| jsonschema | 0.97 | 1.32 | 0.77 | 0.86 |
| auth and value validation | 0.38 | 0.51 | 0.36 | 0.51 |
| copy and compare (of which `covers`) | 0.49 (0.04) | 0.49 (0.05) | 0.39 (0.02) | 0.56 (0.08) |
| JSON, other | 0.15 | 0.17 | 0.19 | 0.27 |
| **`durable_reconciliation`** | 0.36 | 0.52 | 0.45 | 0.64 |
| **handler and rest** | 0.67 | 0.38 | 0.35 | 0.31 |

## Where the time sits (call sites)

- **`port_store_accept` (1.7 to 2.5 s), the largest single call site: jsonschema validation called from `validate_commit_value` at `timeline_commit_validation.py:250`: 1.46 s of 2.49 s in W1 (0.90 s of 2.20 s in W3).** The remainder is copy and compare from `detached` (`timeline_commit_validation.py:92`, 0.36 to 0.47 s) and auth/value validation (0.4 to 0.5 s). The `covers` index costs 0.02 to 0.08 s.
- **`provider_commit` warm (2.9 to 3.1 s) is spread over four causes:** jsonschema `validate_reads` at `_commit_patch.py:32` (0.5 to 0.6 s), Agent patch capture and payload (0.8 to 1.0 s), copy and compare (0.7 to 0.9 s; of it `detached` `timeline_commit_validation.py:92` 0.16 to 0.36 s, `before` `_commit_patch.py:413` 0.10 s, `_copy` `authoring_bundle.py:166` 0.10 s, `commit` `commit.py:1281` 0.08 s) and JSON (`_canonical_json` `authoring_bundle.py:171` 0.15 s, `_json` `commit.py:34` 0.09 to 0.15 s).
- **Cold save (`provider_commit` 9.65 s)** adds history verification (1.2 s), JSON encoding of the history chain (`canonical_json` `util.py:25`, 2.0 s), SQLite (0.7 s), auth and value validation (1.3 s) and 2.0 s of other work including `_read_manifest` at `canonical.py:435` (0.7 s).

## Not established

- Which of the jsonschema validations in `validate_commit_value` can be skipped or cached is not tested here; the table only shows where time is spent.
- The sampler's effect on the numbers (profile stage seconds match the timing lines within 0.2 to 0.4 s per stage).
- Instrumentation overhead of the counters and timer; the group `other` holds everything not matched by a named frame.
