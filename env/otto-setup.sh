#!/usr/bin/env bash
# Run from the candidate astrid-dev checkout root, with its Python environment active.
set -euo pipefail
commit="$(python3 - <<'PY'
import re
import tomllib

with open("otto.toml", "rb") as config:
    commit = tomllib.load(config)["otto"]["commit"]
if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
    raise SystemExit("otto.commit must be 40 lowercase hex characters")
print(commit)
PY
)"
python3 -m pip install "banodoco-otto @ git+https://github.com/banodoco/otto@${commit}"
