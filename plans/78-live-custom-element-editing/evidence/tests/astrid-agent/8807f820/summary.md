# Agent baseline, 22 November 2026

Candidate `8807f820eb47d6018db723511e024a0a123fbe95`; Python 3.13.18, Runtime `3c28211f3cb7ac4867ad744d8cdeeb38dd4484c5`, Node 20.19.4, locked Remotion dependencies; CPU. Command from the Agent root: `PYTEST_ADDOPTS=-rA bash scripts/worker-env/agent-pytest.sh -q tests/core/test_timeline_element_placement.py tests/editing_conformance/test_recipe_clip_set_element.py tests/sdk/test_timeline_commit_provider.py tests/core/test_elements_registry.py tests/core/pack/test_cli_manage.py tests/integrations/test_generic_host_pack_refresh_runtime.py`. Inner exit 1: 187 passed, 4 failed, 2 deselected by existing configuration. The first run lacked the pinned renderer tools; its 31 admission failures were environmental and the complete inventory was rerun after installing them. The table compares the corrected baseline with itself to classify its failing IDs. Raw logs are retained in the run directory.

| Side | Tests run |
|---|---|
| initial | 191 |
| candidate | 191 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 0 |
| preexisting | 4 |
| fixed | 0 |
| missing | 0 |
