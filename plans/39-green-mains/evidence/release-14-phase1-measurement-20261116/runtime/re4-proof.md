# RE4 full-file proof

- Candidate tree: `3fff009d7cb8c46a1a1df21f3f541596b98480bd`
- Local commit: `ac9e6d2e7f6a0a6961d7a2d924040f61832925d1`
- Exact merged hosted commit: `4fe2c0b847cf83771b2f3ce4e4fba0934f64f6ce`
- The local commit differs from the hosted merge commit, but both point to the same tree.
- Python: 3.12.14
- Command: `bash scripts/worker-env/runtime-pytest.sh -q tests/test_timeline_bundle2_contract.py tests/test_timeline_commit_contract.py`
- Result: **PASS — 110 passed in 41.70s; exit 0.**
- Full captured output: [re4-full-files.log](re4-full-files.log)
- SHA-256: `ffa4d0c3f8a21d08ebff69a0f5e27d42c1cc3a0b950317938aa5216ac27ad358`

This completes the requested local full-file acceptance proof for both RE4 files at the requested tree. It does not establish that the exact merge commit's hosted CI run passed; exact-head G2 run 43938386357 was still queued at the latest saved snapshot. No code was changed; no additional selector or full unit suite was run.

