# Agent LE-2b baseline, 22 November 2026

Candidate `8807f820eb47d6018db723511e024a0a123fbe95`; Python 3.13.18, Runtime `3c28211f3cb7ac4867ad744d8cdeeb38dd4484c5`, CPU. Command from the Agent root: `PYTEST_ADDOPTS=-rA bash scripts/worker-env/agent-pytest.sh -q tests/test_installer_asset_checksums.py tests/core/pack/test_defaults.py`. Inner exit 0: 35 passed. The table compares this baseline with itself to classify its failure IDs; raw log is retained in the run directory.

| Side | Tests run |
|---|---|
| initial | 35 |
| candidate | 35 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 0 |
| preexisting | 0 |
| fixed | 0 |
| missing | 0 |
