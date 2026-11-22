# A-1 scoped test comparison

Starting Agent `315b8b7a9336ec3147b399f6bf6f168011d09b27`; candidate `4227f48bc8ed7d11baeeeea439e3cd7b099fb3ea`. Complete `-rA` baseline outcomes and candidate proof were sorted with `env/baseline-diff.py`. The baseline has 190 unique outcomes, 173 passed and 17 failed. Runtime-backed files were rerun with the pinned Runtime import paths after initial setup errors; interrupted and wrong-Runtime runs are excluded. Raw command logs remain in the run workspace.

The full-inventory comparison has 166 missing IDs because the candidate run was limited to A-1 focused tests; it does not establish a full-inventory result for the candidate. The matched A-1 comparison has no regression or other nonempty bucket; candidate-only passing tests are not failures. Both sides used scoped tests, not a full suite. CI was not dispatched.
