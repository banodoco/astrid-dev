The gate finds two new package-level cycles:

- `cli → gateway → cli`: `domain_tasks.py:267` imports `gateway.doctor_bundle.redact_log`; `gateway/hivemind.py:11` and `gateway/dispatch.py:633` import from `cli`.
- `generation → gateway → generation`: `generation/cli.py:782` imports the same redaction helper; `gateway/dispatch.py:87–88` imports from `generation`.

Commit **`f5d8c2b9d4cae8a8b0b474fd0c3e246216a9c675`** introduced both imports. The isolated A' merges of logfetch and winclaim passed; the redact merge failed with both cycles. Merging each requested later addition onto A'' left the same two failures.

| Revision | Local `make cycles` |
|---|---|
| A' `f709407cb` | Pass |
| A'' `34fee0cf` | Fail: two new cycles |
| A''' `8e0006f5` | Fail: same two cycles |

CI runs `make cycles`, which invokes `python -m scripts.reshape.import_cycles --baseline scripts/reshape/baselines/import_cycles.json`. A'' job `132810827812` and A''' job `132824463120` both failed only that gate.

The appropriate fix is to move the redaction helper and its dependencies into a leaf module and update its callers. The checker counts function-local imports, and neither new pair is in `known_before_release_13`. **I did not create `runs/w198/fix.diff`:** a complete behavior-preserving extraction cannot be expressed as the requested one-to-three-line patch, and changing only the imports would reference a nonexistent helper.

Scratch worktrees were removed. No test suite ran and no push was made.