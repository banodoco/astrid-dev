**Verdict: findings; not merge-ready.** C redacts the ordinary synthetic secrets at the requested display paths, but JSON-encoded PEM material survives, receipt JSON loses useful paths and message text, and the bounded URL pattern leaves sufficiently long userinfo visible.

The fetch completed. The full diff from `f709407cb` to `f5d8c2b9` changes nine files: five production files—`domain_tasks.py`, `doctor_bundle.py`, generation `cli.py`, `failure_receipt.py`, and `remote_placement.py`—and four corresponding test files. The stat is **313 insertions, 18 deletions**.

| Boundary | Coverage in C |
|---|---|
| `generate failure`, default | `failure_receipt.py:433,457` applies `redact_log()` to the rendered receipt. Coverage has the PEM and truncation limitations below. |
| `generate failure --json` | `generation/cli.py:792` redacts the serialized receipt. JSON parses in the tested case, but paths and some entire message values are replaced. JSON-encoded PEM can remain visible. |
| `generate failure --logs` and `--name`, including combinations with `--json` | `generation/cli.py:794–809` redacts headers and decoded log contents. A JSON-formatted log containing a PEM string can expose it. `--json --logs` concatenates receipt JSON and logs; `--json --name` prints the named log, so neither promises one JSON document. |
| `tasks logs --name`, with or without `--json` | `domain_tasks.py:283–298` decodes and redacts the selected object before writing it. The `--json` flag does not turn a named log into a JSON envelope. |
| `tasks logs` listing, human and JSON | `domain_tasks.py:301–308` redacts metadata. JSON-encoded PEM in a metadata string remains visible. |
| MCP `generate_failure` and `tasks_logs` | `mcp_server.py:247–254,315–331,449–465,605–613` invokes the CLI **in a subprocess**, then wraps stdout/stderr; it has no independent redaction pass. It inherits the CLI’s coverage and misses. |
| Engine-install stdout/stderr | `remote_placement.py:754–757` redacts returned install stdout and failed-job stderr. The stderr change also applies to other jobs. |
| Failed generation’s first issue | `failure_receipt.py:192–203,293–295` retains the original issue; `:480–483` redacts the value returned by `kept_failure_details`, which reaches the terminal through `generation/cli.py:831–837`. The redaction is conditional on receipt enrichment; the final print itself does not redact. The enriched machine-list projection also changes. |
| `tasks show` | **Missed:** `domain_tasks.py:228–233` prints the task result without this redactor, including any log metadata carried in that result. |
| Failure-time stdout/stderr tails | **Missed by this change:** `generic_host.py:10915–10924,11211–11221` puts captured tails into failure messages after scrubbing known secret values; the generic CLI error path uses separate credential redaction, not `redact_log()`. I did not find a separate direct CLI print of the `job.stdout`/`job.stderr` files outside the named-log paths. |
| Doctor stdout | **Missed by this change:** `gateway/dispatch.py:345–350,430–447` prints the local report or errors without `redact_log()`. The host-log section reports metadata, not log contents; support-bundle log contents already pass through the redactor at `doctor_bundle.py:289–297`. |

The main findings are:

- **PEM in JSON leaks.** A synthetic PEM block in a JSON string remained visible through `tasks logs --json`, `generate failure --json`, and a JSON log printed by `--logs` or `--name`. `doctor_bundle.py:67–100` scans for PEM delimiters before JSON decoding, so escaped newlines prevent the line-based PEM matcher from seeing the block.
- **Receipt output loses useful data.** `generate failure --json` parsed successfully and retained the tested top-level keys and IDs, but changed `/tmp/run/job.log` to `<redacted>` and replaced an entire issue message containing `api_key=` with `<redacted>`. The structured redactor can also replace values under sensitive-looking keys, changing value types or nested structure. In human output, a PEM delimiter immediately following `Cause: issue_message=` caused the preceding failure heading and cause to be discarded.
- **Long URL userinfo leaks.** At `doctor_bundle.py:26`, a synthetic 512-character userinfo was redacted; a 513-character userinfo was printed unchanged. A scheme longer than 32 characters likewise bypassed the pattern.
- **The JSON quote/backslash probes did not raise.** The actual `tasks logs --json` function returned parseable JSON for synthetic API-key and bearer strings adjacent to quotes, a Windows-style path, backslashes, a URL, and an escaped PEM. This demonstrates those cases, not that every possible input is safe.

For ordinary text lines, the probes retained suffixes and used redaction markers. For example, `api_key=synKeyXYZ keep-end` became `api_key=<redacted> keep-end`.

The synthetic retained-file check used a bearer header, API key, token-only URL, PEM block, and `HF_TOKEN`. The source log and retained copy had SHA-256 `b7f0e6c2231c9f468f6216a6de4aa224b023cadeea1507f9d4ef2a7799f0e062` both before and after; the receipt also had identical before/after hashes. The tested plain-text output removed all five synthetic values. The in-process task test likewise left its fake stored log unchanged. These checks and the diff support unchanged storage for the exercised paths; they do not independently prove every Runtime object or backup/export copy.

A synthetic invalid UTF-8 byte printed as **U+FFFD** through both failure-log and named task-log output, while its stored bytes remained unchanged. The MCP wrapper captures subprocess output as text, not bytes. The inspected named-log tests assert text output; I did not find a byte-parsing consumer of these CLI outputs.

| Test file | A′ | C |
|---|---:|---:|
| `tests/core/cli/test_tasks_logs.py` | 11 pass | 16 pass |
| `tests/core/gateway/test_doctor_bundle.py` | 14 pass | 57 pass |
| `tests/core/gateway/test_doctor_tools.py` | 1 pass | 1 pass |
| `tests/core/gateway/test_update_recovery.py` | 5 pass | 5 pass |
| `tests/packs/runpod/test_remote_placement.py` | 16 pass | 26 pass |
| `tests/packs/runpod/test_failure_receipt_logs.py` | 4 pass | 13 pass |
| `tests/packs/runpod/test_failure_receipt.py` | 44 pass | 44 pass |
| `tests/packs/runpod/test_failure_logs.py` | 6 pass | 6 pass |
| `tests/test_failure_receipts.py` | 25 fail | 25 fail |
| `tests/test_mcp_server.py` | 30 pass | 30 pass |
| `tests/test_mcp_generation_parity.py` | 10 pass | 10 pass |
| `tests/test_mcp_machines_consent.py` | 3 pass | 3 pass |

Each side used one pytest process after setup. Totals were **144 passed, 25 failed** on A′ and **211 passed, 25 failed** on C. The failing ID sets were identical: all 25 failures in the additional receipt-aggregation file hit `KeyError: 'macos-15'` in `tests/failure_mode_fixtures.py:63`. **C-only failing IDs: none.** No existing printed-content assertion was changed or weakened; the diff only adds assertions.

On this shared machine, the four W177 1 MiB shapes took **0.299 s** (`a://` repeated), **0.265 s** (`x@` repeated), **0.724 s** (letters), and **0.691 s** (`https://` followed by letters without `@`). A 20 MiB synthetic multiline log with a few secrets took **11.051 s, or 0.553 s/MiB**; a simple linear extrapolation is about 142 seconds for 256 MiB, not a measurement at that size. `--logs` uses `Path.read_text()` and then redacts the resulting string, so it loads the whole file into memory rather than streaming.

The temporary worktrees, environments, basetemps, and probes were removed. No tracked files were edited and no push was made.