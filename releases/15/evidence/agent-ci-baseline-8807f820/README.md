# The Agent's hosted CI baseline for Release 15 (22 November 2026)

What fails in astrid-agent's own CI on `release/15/main`, test by test, compared with the published Release 14. Every lane landing in Release 15 compares its "no new failures" result against these lists, not against a local run: a test that fails locally and passes here is an environment difference.

| | Release 14 | Release 15 |
| --- | --- | --- |
| Commit | `c0ad6b54aadd21630d98bb5039613e37efe92a8f` | `8807f820eb47d6018db723511e024a0a123fbe95` |
| CI run | [45010433010](https://github.com/banodoco/astrid-agent/actions/runs/45010433010) | [45031908687](https://github.com/banodoco/astrid-agent/actions/runs/45031908687) |
| Unit shards: tests failing | 750 | 747 |
| Unit shards: tests erroring | 328 | 328 |
| macOS job: tests failing | 15 | 13 |

Both runs have the same jobs with the same conclusions, and every failed job's full log was read, so the comparison is complete. Counts are distinct test ids; pytest's own totals are slightly higher because three tests fail in several subtests.

- **Inherited:** 1,070 unit test ids fail or error on both releases.
- **New on Release 15:** 5, in [new-on-release-15.txt](new-on-release-15.txt). Two in `test_readiness_missing_models.py`, two in `test_pinokio_platform_adapter.py`, and the pack boundary ratchet.
- **Fixed on Release 15:** 10, in [fixed-on-release-15.txt](fixed-on-release-15.txt): seven in `test_pinned_project_elements.py`, one in `test_readiness_missing_models.py` (the same assertion as the two new ones there, so it may have moved, not been fixed) and two macOS render tests that failed on a 1.1-second deadline.
- **All failing and erroring ids:** [Release 15](release-15-8807f820-failing-ids.tsv) and [Release 14](release-14-c0ad6b54-failing-ids.tsv), one per line, with `FAILED` or `ERROR` first; macOS ids are prefixed `darwin:`.

**The errors have five stated causes, the same on both releases, covering 318 of the 328:** the Runtime's `runtime_protocol` imported from the installed package instead of the Runtime checkout (182); pinned Node and esbuild inputs missing (50); `tests.test_verified_host_launch` not importable (45); `ASTRID_REMOTION_PROJECT_DIR` unset (33); the RunPod Lifecycle checkout not being a Git checkout (8). **The failures have no single cause;** the largest group is 72 installer tests stopping with `R0StopError`.

**Two groups move between runs, so gate on the group, not the id.** Tests in `tests/test_pinokio_platform_adapter.py` that fail with `AdapterError: active process is not the configured listener owner` fail in different members on different runs of unchanged code (two on Release 14, three on Release 15, and two more on Plan 81's candidate); the cause is not yet found. Tests in `tests/core/generation/test_readiness_missing_models.py` that report `no attached ... unavailable` in place of the expected reason do the same (one on Release 14, two on Release 15). A candidate that fails another member of either group with the same message has met the same defect, not added one; a different message is a new failure.

**Limits.** Each side is one run, so a difference of a few tests cannot be told from flakiness. The lists were extracted from the job logs by script in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG); the logs themselves are not kept here.
