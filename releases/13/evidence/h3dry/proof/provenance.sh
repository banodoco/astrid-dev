#!/bin/bash
set -euo pipefail
cd /home/user/wt/h3live
export GIT_NO_LAZY_FETCH=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=protocol.allow GIT_CONFIG_VALUE_0=never
printf 'HEAD='; git rev-parse HEAD
printf 'tree='; git rev-parse HEAD^{tree}
git --no-optional-locks status --porcelain
git merge-base --is-ancestor 941fca2a4 HEAD
printf 'compose 941fca2a4 ancestor: yes\n'
printf 'VibeComfy='; git -C /home/user/wt/h3live.env/vibecomfy rev-parse HEAD
sha256sum /root/.cache/uv/sdists-v9/path/cb0db8c78d99a941/10cfy-NcZre4lD2C/astrid_runtime-0.1.0-py3-none-any.whl
env -i HOME=/home/user/wt/h3live.env/home PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/wt/h3live:/home/user/wt/h3live.env/vibecomfy /home/user/wt/h3live.env/venv/bin/python -B -c 'import sys,astrid,runtime_protocol,vibecomfy; print(sys.version); print(astrid.__file__); print(runtime_protocol.__file__); print(vibecomfy.__file__)'
