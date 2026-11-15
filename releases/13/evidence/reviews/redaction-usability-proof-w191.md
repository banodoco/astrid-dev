**Verdict: findings.** The delta fixes the tested receipt usability and PEM cases, and the comparative tests found no candidate-only failures. Standard `PGP PRIVATE KEY BLOCK` armor remains visible, however, so the requested private-key variant coverage is incomplete. The same gap exists on B.

The fetch succeeded, and I read the full diff from B `f5d8c2b9d` to C `887f81594`. It changes six files, with **196 insertions and 25 deletions**:

- `astrid/core/gateway/doctor_bundle.py`
- `astrid/core/generation/cli.py`
- `astrid/packs/runpod/failure_receipt.py`
- `tests/core/cli/test_tasks_logs.py`
- `tests/core/gateway/test_doctor_bundle.py`
- `tests/packs/runpod/test_failure_receipt_logs.py`

**(a) Receipt JSON.** A receipt-shaped synthetic probe passed through C’s `generate failure --json` function. Only these values changed:

| Field | Before → after |
|---|---|
| `message` | `failed: api_key=abc123 then continued` → `failed: api_key=<redacted> then continued` |
| `cause.issue_message` | `Bearer abc.def keep` → `Bearer <redacted> keep` |
| `logs[0].tail` | `api_key=tailsecret keep` → `api_key=<redacted> keep` |

Keys and value types were identical. Numeric `token_count`, Boolean `api_key_present`, sizes, timings and enums remained intact.

**The metadata exemption leaves secrets in metadata visible.** The synthetic log path `https://pathsecret@host/source` and task ID `https://idsecret@host/task` both appeared unchanged in JSON. Paths, IDs, digests, sizes, timing, stage, enums and other fields outside the allowlist are exempt. The allowlist is exactly `message`, `issue_message`, `cause`, `tail`, `excerpt`, `log_tail`, `log_excerpt`, `stdout_tail`, and `stderr_tail`; only string values under those keys are processed.

**(b) PEM.** The probe confirmed `<redacted PEM>`, preservation of same-line prefixes and suffixes, matching END delimiters, two blocks in one text, and preservation of earlier lines when BEGIN has no END. An unterminated PEM in a JSON field stopped at that field; the adjacent field and number survived. `Cause: issue_message=` remained visible. Escaped PEM strings were redacted through both `tasks logs --json` and `generate failure --json --logs`.

`PRIVATE KEY`, `OPENSSH PRIVATE KEY`, `RSA PRIVATE KEY`, `EC PRIVATE KEY`, and the literal `PGP PRIVATE KEY` delimiter were redacted. The standard **`-----BEGIN PGP PRIVATE KEY BLOCK-----`** form was not: its synthetic key material remained visible on both B and C.

The changed existing assertion is:

```diff
-    assert "credentials" in redacted and "<redacted private key>" in redacted
+    assert "credentials" in redacted and "<redacted PEM>" in redacted
```

The preceding loop asserting that each synthetic secret is absent was unchanged; no secret-absence assertion was removed or weakened.

**(c) URLs and timing.** Userinfo lengths 513, 1024, 2048 and 4096 were redacted. Length 4097 remained visible. A 33-character scheme also remained visible. All 15 W177 examples retained their prior behavior, including unchanged ordinary URLs, email and Windows paths; redacted URL userinfo; and unchanged raw `/` or `?` inside the userinfo candidate.

| Synthetic input | Seconds | Seconds/MiB |
|---|---:|---:|
| 1 MiB letters | 0.699 | 0.699 |
| 1 MiB `https://` plus letters | 0.622 | 0.622 |
| 1 MiB repeated `a://` | 0.263 | 0.263 |
| 1 MiB repeated `x@` | 0.241 | 0.241 |
| 1 MiB repeated `a-b.c+d` | 0.293 | 0.293 |
| 20 MiB multiline log | 7.449 | 0.372 |

The 20 MiB output removed its three synthetic secrets. Timings were measured while the comparative suites were running.

| Test file | B | C |
|---|---:|---:|
| `tests/core/cli/test_tasks_logs.py` | 16 passed | 18 passed |
| `tests/core/gateway/test_doctor_bundle.py` | 57 passed | 68 passed |
| `tests/core/gateway/test_doctor_tools.py` | 1 passed | 1 passed |
| `tests/core/gateway/test_update_recovery.py` | 5 passed | 5 passed |
| `tests/packs/runpod/test_remote_placement.py` | 26 passed | 26 passed |
| `tests/packs/runpod/test_failure_receipt_logs.py` | 13 passed | 18 passed |
| `tests/packs/runpod/test_failure_receipt.py` | 44 passed | 44 passed |
| `tests/packs/runpod/test_failure_logs.py` | 6 passed | 6 passed |
| `tests/test_mcp_server.py` | 30 passed | 30 passed |
| `tests/test_mcp_generation_parity.py` | 10 passed | 10 passed |
| `tests/test_mcp_machines_consent.py` | 3 passed | 3 passed |
| `tests/test_failure_receipts.py` | 25 failed | 25 failed |
| **Total** | **211 passed, 25 failed** | **229 passed, 25 failed** |

Both sides completed the prescribed setup. The 25 failure IDs were identical and each had the known `KeyError: 'macos-15'`; **C-only failing IDs: none**. In a scratch copy of C’s changed tests against B’s product code, the nine new regression test functions expanded to **13 cases, all failing**.

Temporary worktrees, environments, basetemps and probes were removed. No provider call or push was made, and no tracked shared-checkout files were edited.