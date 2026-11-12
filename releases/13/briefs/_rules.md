
## Rules (verbatim, all apply)
- do not push or commit;
- never weaken, skip or delete a test;
- no RunPod or paid services; package registries, GitHub and Hugging Face reads are allowed;
- no `.env`, credential files or ~/.codex;
- start no long-lived services (loopback test servers inside tests are fine);
- if /tmp is not writable, use `TMPDIR=$PWD/.tmp-tests` and delete it afterwards;
- ruff must not rise (`python -m scripts.reshape.compare_ruff_baseline`; the baseline is 2120);
- no AI model or product names;
- stop after three failed attempts;
- Python `/home/user/astrid-agent.env/venv/bin/python` with `PYTHONPATH="$PWD:/home/user/wt/c-dl-vc2"`;
- other Codex workers run in parallel on this machine, so use your own `TMPDIR` under your clone for pytest (`--basetemp=$PWD/.tmp-tests/pt`) and delete it at the end;
- return the diff and the before/after test results.

If an existing test pins behaviour this brief replaces, do not edit that test: stop and report which test and why.
