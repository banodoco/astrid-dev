# SR-3 focused proof — 2026-11-18

Agent candidate `849b6cbc5c638439d7750bc183d79199bc679d19`, identical to merge tree `2d0b466adab47b96ec787a68ebe5a66138f8ff54`. The CPU worker ran the six SR-3 files, host-added three builder-caller files and `test_spec.py` with `PYTEST_ADDOPTS=-rA` through `env/agent-pytest.sh`. Result: 290 passed, three pre-existing failed, 29 integration/installed lane deselected. Baselines are the full plan-scoped start `b50371baf` and the added caller/spec base `d88b7b804` (12 and 53 passes). The 47 missing IDs below belong to other plan test files outside this focused run, not removed tests; full CI is the later end gate. Raw logs remain in the run directory.

| Side | Tests run |
|---|---|
| start | 201 |
| sr3base | 65 |
| candidate | 293 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 0 |
| preexisting | 3 |
| fixed | 0 |
| missing | 47 |
