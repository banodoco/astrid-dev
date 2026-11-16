# A2 runtime preflight validation

Draft handoff source `38c2919052840d9de8e724023ff2710bd0d5229a`; no CI run or comparison performed. Four local environments from `/workspace/r12-a2-resume` were checked offline.

Under sanitized `env -i`, `PYTHONSAFEPATH=1`, `PYTHONNOUSERSITE=1`, `PYTHONDONTWRITEBYTECODE=1`, and each pinned Python virtualenv, the old preflight's `find_spec('tests')` returned absent for r10, r11, base and candidate; each VibeComfy revision constant matched its respective pin. Diagnostic CI run 43014791915 did not preserve its raw traceback, so this reproduces a definite failure mechanism, not proof excluding other CI-specific causes.

The new `runtime_preflight.py` returned exit 0 for all four sides under the same safe-path environment, verifying the explicitly loaded Agent tests package origin, Runtime protocol source origin, both exact fixture module paths, and VibeComfy revision. Each process had a 20-second ceiling. All four Agent, Runtime, VibeComfy and lifecycle checkout HEADs matched the runner's full SHA allowlist; their tracked files were clean. The local checkouts did not have matching configured origin URLs, so the local origin URL check could not independently establish fetch provenance. CI runner source fetches from the fixed GitHub URLs and verifies each full SHA.

Offline unit validation: runtime preflight 6 tests, stages 6, sanitizer 9, frozen inventory 4; all passed. Synthetic fixture tests cover Agent fixture shadowing, wrong Runtime protocol path, missing fixtures, missing Agent package, and preimported tests modules. No heavy suite or CI was started. This does not count as A2 comparison evidence and does not authorize a rerun.
