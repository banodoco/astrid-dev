# A2 incomplete-receipt diagnostics: bounded offline validation

Exact source `a6c1917c1d1699edde3fad4f7fdf6e978f87cc68` on non-triggering `handoff/r12-a2-incomplete-receipts`. No triggering ref, CI, or heavy pytest was started. A coordinated brief host window was released after the checks.

Python 3.11.17 with `PYTHONDONTWRITEBYTECODE=1`, 30-second per-command ceilings: `test_sanitize.py` 19 passed; `test_receipt_guard.py` 9 passed; `test_full_plan.py` 12 passed; `test_verify_prior.py` 6 passed; `test_stages.py` 6 passed; `test_runner.py` 4 passed; `test_runtime_preflight.py` 6 passed. Total 62. Four `A2_PRIOR FAILURE_FLAG_INVALID` lines were expected negative tests.

The checks cover fixed-enum bounded shape counts without accepting malformed output; minimal INCOMPLETE fallback receipt construction; no fabricated clear census; forged clear and raw-secret exclusion; unsafe output symlinks; literal artifact paths; sticky failure guards; exact prior receipt bytes and 80-pair scope. They do not exercise live Actions uploads, prove absolute retention on cancellation/runner loss, eliminate same-UID races, prove free quota, or resolve the live group 041 cause. Independent read-only source review found no blocker; separate trigger coordination remains required.

Exact commands, executed from `/workspace/r12-a2-ci-draft` after checking that `git rev-parse HEAD` equaled the source SHA above:

```bash
PYTHONDONTWRITEBYTECODE=1 timeout 30s /workspace/r12-a2-resume/r11.env/venv/bin/python tools/r12-a2-ci/test_sanitize.py
PYTHONDONTWRITEBYTECODE=1 timeout 30s /workspace/r12-a2-resume/r11.env/venv/bin/python tools/r12-a2-ci/test_receipt_guard.py
PYTHONDONTWRITEBYTECODE=1 timeout 30s /workspace/r12-a2-resume/r11.env/venv/bin/python tools/r12-a2-ci/test_full_plan.py
PYTHONDONTWRITEBYTECODE=1 timeout 30s /workspace/r12-a2-resume/r11.env/venv/bin/python tools/r12-a2-ci/test_verify_prior.py
PYTHONDONTWRITEBYTECODE=1 timeout 30s /workspace/r12-a2-resume/r11.env/venv/bin/python tools/r12-a2-ci/test_stages.py
PYTHONDONTWRITEBYTECODE=1 timeout 30s /workspace/r12-a2-resume/r11.env/venv/bin/python tools/r12-a2-ci/test_runner.py
PYTHONDONTWRITEBYTECODE=1 timeout 30s /workspace/r12-a2-resume/r11.env/venv/bin/python tools/r12-a2-ci/test_runtime_preflight.py
```

The commands were chained with `&&`; all seven reported `OK` and the command chain exited 0.
