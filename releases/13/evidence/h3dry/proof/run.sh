#!/bin/bash
set -euo pipefail
name=$1
mode=${2:-video-edit}
E=/home/user/wt/h3live.env
P=/home/user/cells/evidence/h3live/package
mount --bind /home/user/wt/h3live /home/user/wt/h3live
mount -o remount,bind,ro /home/user/wt/h3live
cd /home/user/wt/h3live
set +e
env -i PATH="$E/venv/bin:$(cat "$E/uv-dir"):/usr/local/bin:/usr/bin:/bin" HOME="$E/home" TMPDIR="$E/tmp" XDG_CACHE_HOME="$E/cache" LANG=C.UTF-8 UV_OFFLINE=1 PIP_NO_INDEX=1 PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONSAFEPATH=1 PYTHONPATH="/home/user/wt/h3live:$E/vibecomfy" VIBECOMFY_SOURCE="$E/vibecomfy" ASTRID_RUNTIME_CHECKOUT="$E/runtime" ASTRID_VIBECOMFY_CHECKOUT="$E/vibecomfy" GIT_NO_LAZY_FETCH=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=protocol.allow GIT_CONFIG_VALUE_0=never "$E/venv/bin/astrid" generate video --entry h3 --mode "$mode" --input "request=$P/requests/$name.yaml" --input "asset_map=$P/$name.asset_map.json" --placement runpod --dry-run --out "$P/out/$name" > "$P/dryrun/$name.output.json" 2> "$P/dryrun/$name.stderr"
printf '%s\n' "$?" > "$P/dryrun/$name.exit"
