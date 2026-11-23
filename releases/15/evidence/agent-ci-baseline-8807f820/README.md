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

**One more member of the readiness group, with a different-looking symptom (added 23 November 2026).** `tests/core/generation/test_readiness_missing_models.py::test_defaults_is_ready_once_the_files_are_listed` failed on two heads of Plan 81's candidate and passed on this baseline's run. It is the same defect, not the candidate's: the test's own fake server takes about as long to build its reply (1.7 to 1.9 seconds on a quiet machine, measured by Plan 81's reviewer) as the client's unchanged 2-second deadline allows, so on a busy runner the client gives up, the server's late write raises `BrokenPipeError`, and the test reports `ready` false with no reason printed. Run alone on the Lead's machine, the unchanged `8807f820` passed 16 of 16 times when the machine was quiet and failed 12 of 12 times beside five CPU-bound processes; Plan 81's `b5c30e61` failed 12 of 12 in the same alternating runs, each with the two `BrokenPipeError` traces ([counts](readiness-under-load.tsv)). Plan 81's independent reviewer reproduced the same on both heads and found the same requests in the same order. So: this id failing with `ready` false and `BrokenPipeError` from the fake server is a group member under the rule above. The repair belongs to the test's fixture or the deadline, which is the owner's call, and is not part of any lane's landing.

**Limits.** Each side is one run, so a difference of a few tests cannot be told from flakiness. The lists were extracted from the job logs by script in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG); the logs themselves are not kept here.
