# Plan 89 profile: Runtime `c8b861c7` with App `9f26112d`, cold save and three warm saves under py-spy, 24 November 2026

Approved by the Plan 89 orchestrator as the second attempt after the [first measurement](../2026-11-24-p89-measure-run/README.md): the same package `release-15/p89-measure-command` head `ee89f2ed8ba6b4cb7c631b7d3a9f593c5bc01a71` (digest `1a2ee7c323fa483f9e5298a3c9a531fb5f4d1edbd13702823082db1b1d4dc6d8`), same SHAs (Runtime `c8b861c770aa58fd0392fe2dcefbda9ce23c84d1`, App `9f26112d746cba7a1a3287f0b679fd6c9ca39907`, Agent `096a2fb3536192785fabd33e6673ba8ab4ef5ead` two-file overlay), **only difference: `SV3_PROFILE=1`**. The first launch stopped before it touched the fixture (`first-launch-floor-stop.log`: `free space below 18 GiB start floor`, 17.91 GiB after the build; no copy, no Runtime start, no out dir); after reclaiming 0.5 GiB of finished receipt extractions it was launched again unchanged (`run-stdout.log`). The script exit status is again 1 (`ValueError: Runtime commit-stage timing sink is missing`, this Runtime writes no sink) after the profile saves and bursts were done, so `profile-attach-summary.json`, `summary.tsv` and `measurements.jsonl` were not produced; the per-save profile records (`rep-1/profile-*-profile.json`) show py-spy attached to all four saves (18,332, 6,499, 6,353 and 6,069 stack samples, one sampling error in the cold save). Idle-safe stop verified, ports closed, no Chrome, boundaries unchanged; disk minimum 16.56 GiB; `agent-loaded.json` `failures: []`.

Timings of this repetition (driver, release to Saved; POST to 200): cold 16.9 s (12.1), W1 6.5 s (4.9), W2 7.1 s (4.8), W3 6.7 s (5.2); no refusal; S0 verified-head 200, editor writable after 11.7 s; B5 5 POSTs 24.6 s, 5 of 5 in the document; B10 10 POSTs 48.6 s, 10 of 10 in the document (final start off by exactly the 0.05 s tolerance, reported `false`).

## Method

As in the earlier profiles: the commit thread is the one non-main thread with the most samples under a `timeline_commit*` frame; samples are put into stages by the line of the `_execute` frame in `timeline_commit_execution.py` of this exact source (`analyze-stages.py`: provider commit lines 618 to 634, durable reconciliation from 652, initial lookup 601 to 608) or by `accept` in `timeline_commit_port.py` (`port_store_accept`); groups by the innermost matching frame. Raw outputs: `profile-stages.txt`, `profile-callsites.txt`, `profile-validation.txt` (from `analyze-validation.py`).

## 1. Validation and jsonschema (seconds on the commit thread)

| | cold | W1 | W2 | W3 |
| --- | --- | --- | --- | --- |
| Commit thread | 12.22 | 4.84 | 4.65 | 4.97 |
| Under `timeline_commit_validation.py` (any frame) | 4.88 | 1.57 | 1.94 | 1.67 |
| Under `validate_commit_value` | 0.93 | 0.72 | 0.78 | 0.78 |
| Under any jsonschema frame (`descend` / `iter_errors`) | 1.63 | 1.06 | 1.02 | 1.19 |

- **The SV-L10 memo machinery is active:** frames `_remember_success` (0.33 s cold, 0.00 to 0.01 s warm), `_subtree_bytes` (0.09 cold, 0.04 to 0.11 warm), `_has_subtree_recursion_headroom` (0.01 to 0.04) and the `$ref` wrapper `reference` (`timeline_commit_validation.py:192`, 0.11 s in W2) are present. `_memoized_reference`, `_reviewed_item_nodes` and `_schema_resources` do not appear as sampled frames (they run once). The daemon reads the schema bundle from the overlay source tree (`candidate-daemon-module.json`: `runtime_protocol` under the archive; bundle sha256 `ce5490ae...` and `SCHEMA_DIGEST` equal the reviewed values), so the memo's bundle guard held.
- **jsonschema in `port_store_accept` fell** from 1.32 / 0.77 / 0.86 s (W1 to W3, eb4e8644 profile) to 0.29 / 0.35 / 0.19 s here; the jsonschema left is in the Agent patch code (`validate_reads`, `_commit_patch.py:32`, 0.3 to 0.4 s in `provider_commit`) and in the handler (0.11 to 0.35 s). Total jsonschema per warm save: 2.0 / 1.6 / 1.6 s before, 1.06 / 1.02 / 1.19 s now. `validate_commit_value` itself (the PreparedCommit schema check) is 0.72 / 0.78 / 0.78 s against 0.70 / 0.98 / 0.95 s installed on 23 November: **not halved**.

## 2. Stage split (seconds, profile)

| Stage | cold | W1 | W2 | W3 |
| --- | --- | --- | --- | --- |
| `provider_commit` | 9.44 | 2.71 | 2.58 | 2.88 |
| `port_store_accept` | 1.82 | 1.37 | 1.45 | 1.27 |
| `durable_reconciliation` | 0.57 | 0.46 | 0.39 | 0.34 |
| initial replay lookup | 0.01 | 0.02 | 0 | 0 |
| handler and rest | 0.38 | 0.28 | 0.23 | 0.48 |
| **Commit thread** | **12.2** | **4.84** | **4.65** | **4.97** |

Against the SV-4 profile of the eb4e8644 candidate (thread 6.4 / 5.4 / 6.2 s for W1 to W3; `provider_commit` 3.00 / 2.89 / 3.07, `port_store_accept` 2.49 / 1.71 / 2.20): the thread is 1.6 / 0.8 / 1.2 s shorter, almost all in `port_store_accept` (1.1 / 0.3 / 0.9 s less); `provider_commit` is 0.3 s shorter. Warm `provider_commit` is now: Agent patch capture and payload 0.7 to 0.8 s, copy and compare 0.6 to 0.8 s, jsonschema `validate_reads` 0.3 to 0.4 s, JSON 0.3 s, other 0.3 to 0.7 s. **Caution:** the unprofiled warm POST to 200 on `c8b861c7` was 4.59 s against 4.61 s on `eb4e8644` ([first measurement](../2026-11-24-p89-measure-run/README.md)), and the profiled POST to 200 of this run (4.9 / 4.8 / 5.2 s) is 0.8 to 1.4 s lower than the profiled eb4e8644 run (6.3 / 5.8 / 6.0 s); the sampler's effect differs between the two runs and a single repetition cannot separate it from a real gain.

## 3. Frames not seen in the 23 November profile

`step_covers` and `covers` (0.11 and 0.09 s: the new covers index), `_check_history_objects` (0.09 s), `history_read_scope` (0.07 s), `_history_entry_view` (0.24 s), `_verify_accepted` (0.38 s inclusive, with `_verify_accepted_record` 0.18 s and `_verify_accepted_replay` 0.12 s, i.e. history verification is not zero on a warm save here), `idempotency.py command_result` (0.12 s), `_producer_captures` and `allocations` (0.03 to 0.04 s). No frame name contains `guard`; which of these are the SV-L5 history guards is not established from the names alone.

## Not established

- A real gain: one repetition, with and without the sampler the saves differ by about 0.3 s (unprofiled 4.59 s, profiled 4.9 s per save).
- The cause of the slower first save (4.3 s before the first POST, 12.1 s POST to 200).
