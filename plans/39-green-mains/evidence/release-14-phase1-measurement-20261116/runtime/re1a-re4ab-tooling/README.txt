Correction to prior evidence: prior source-verification incorrectly called Agent editable. Earlier proofs used an unqualified installed copy despite the updated checkout. Retained old logs and claims are historical and superseded as provenance evidence. Reinstalled verified R12 checkout using uv pip install --python ../astrid-runtime.env/venv/bin/python --no-deps --reinstall ../astrid-runtime.env/agent; freeze before and after are identical. provenance.txt records clean source commit and tree, imports from site-packages without adding checkout to sys.path, and byte equality against all 78 tracked astrid/sdk/timeline files at the exact Git tree.

Focused commands and results:
bash scripts/worker-env/runtime-pytest.sh -q -m "" tests/test_operation_handle_integration.py: exit 0, 3 passed.
bash scripts/worker-env/runtime-pytest.sh -q tests/test_timeline_clip_replacement.py: exit 1, 10 declared strict xfails and 17 deselected, because no test passed. This matches the prior observed outcome and does not establish a passing file.
bash scripts/worker-env/runtime-pytest.sh -q tests/test_timeline_commit_type_generator.py tests/test_timeline_document_object_contract.py: exit 0, 29 passed.

Wiring checks parse YAML and Python syntax and resolve the prepended repository compiler under the local workspace with Node 22. These checks and focused proofs do not constitute live Docker or hosted acceptance; no Docker run was available. Full command logs, exit codes, package snapshots, provenance, diffs and commit/tree are retained here. Formal RS1 remains 0/1.
