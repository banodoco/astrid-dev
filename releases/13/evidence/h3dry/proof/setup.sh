#!/bin/bash
set -uo pipefail
export UV_OFFLINE=1 PIP_NO_INDEX=1 PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=protocol.allow GIT_CONFIG_VALUE_0=never
mount --bind /home/user/wt/h3live /home/user/wt/h3live
mount -o remount,bind,ro /home/user/wt/h3live
cd /home/user/wt/h3live
bash /home/user/astrid-dev/env/agent-setup.sh > /home/user/cells/evidence/h3live/setup.log 2>&1
printf '%s\n' "$?" > /home/user/cells/evidence/h3live/setup.exit
