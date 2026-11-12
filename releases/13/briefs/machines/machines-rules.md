## Rules (all apply)
- do not push or commit (the manager commits);
- never weaken, skip or delete a test, except one that encodes behaviour the owner ordered removed (generate-time allocation, per-job consent, the paid consent flag, `--until-release`); convert such a test to the new behaviour and list it with a one-line reason. If any other existing test conflicts with this brief, do not edit it: stop and report which test and why;
- no RunPod or paid calls: never call api.runpod.io, rest.runpod.io or any other RunPod endpoint, and never run any `astrid generate` or `astrid machines` command (the network proxy would act on the real paid account); drive the CLI only through `main([...])` in tests with fakes. Package registries, GitHub and Hugging Face reads are allowed;
- never read `.env`, credential files or ~/.codex;
- start no long-lived services (loopback test servers inside tests are fine);
- ruff must not rise (`python -m scripts.reshape.compare_ruff_baseline`; baseline 2117);
- no AI model or product names in code, comments, tests or text meant for commits;
- stop after three failed attempts at any one problem and report it;
- Python is `/home/user/astrid-agent.env/venv/bin/python` with `PYTHONPATH="$PWD:/home/user/wt/vibecomfy-fe92ac7"`;
- other workers run on this machine: run pytest with `TMPDIR=$PWD/.tmp-tests` and `--basetemp=$PWD/.tmp-tests/pt`, and delete `.tmp-tests` at the end;
- run only the proof this brief names: no full suite, no `pytest tests/` and no extra suites. A separate test lane compares the full suite on hosted CI, and on this shared 4-CPU machine extra runs cause failures from load alone;
- candidate gates (binding): read `/home/user/wt/briefs/wave3/machines-gates.md`. In the files you edit, bring mypy to net zero over Release 12 and never raise the core/pack boundary ratchet, and report both measurements;
- Use your Luna sub-agents for reading, inventories, call-site and test searches, mechanical edits and running checks; keep your own effort for the design and judgment; run independent sub-agents in parallel. Every sub-agent follows these same rules;
- run only the test commands this brief names; no full-repository suite;
- return the diff (`git diff --stat` and where the full diff is saved), the before and after results with counts, and every converted test with its reason.

## Owner principles (binding)
As simple as possible, one path for each thing; declared once, with sensible defaults; no shims or interim steps; minimal safety ceremony (keep real money and custody safety, drop bureaucracy); every failure or wait understandable from the product. If something looks muddled, say so in your report rather than building around it.
