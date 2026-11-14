#!/bin/bash
set -euo pipefail
export UV_OFFLINE=1 PIP_NO_INDEX=1 PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=protocol.allow GIT_CONFIG_VALUE_0=never
E=/home/user/wt/h3real.env
mkdir -p "$E/source"
cp /home/user/wt/h3real/pyproject.toml /home/user/wt/h3real/LICENSE /home/user/wt/h3real/NOTICE "$E/source/"
cp -a /home/user/wt/h3real/astrid "$E/source/"
uv pip install --python "$E/venv/bin/python" -e "$E/source[dev]"
uv pip install --python "$E/venv/bin/python" --no-deps /root/.cache/uv/sdists-v9/path/cb0db8c78d99a941/10cfy-NcZre4lD2C/astrid_runtime-0.1.0-py3-none-any.whl
cp -a "$(readlink -f /root/.cache/uv/sdists-v9/path/cb0db8c78d99a941/10cfy-NcZre4lD2C/astrid_runtime-0.1.0-py3-none-any)" "$E/runtime"
git -C /home/user/vibecomfy worktree add --detach "$E/vibecomfy" dba38f8644c46f652376f2cd5112ea161e40f09b
dirname "$(command -v uv)" > "$E/uv-dir"
