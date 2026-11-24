#!/usr/bin/env bash
set -Eeuo pipefail

app="${1:?path to the disposable App worktree}"
reference="${2:?path to the reference App checkout providing node_modules}"
expected_app=092013f3b88e9d49e48102630951a40a450c4868
expected_config=b5a636d330a7e1f145d475b3385ff85980bf815af0a3085b1276a3549c8989a5
config="$app/config/vite/vite.config.ts"
backup="$app/.svl2-vite.config.ts.original"
cache="$app/.svl2-vite-cache"
log="$app/build-svl2.log"
guard_receipt="$app/build-node-modules-guard.json"
build_pgid=''
reference_tree_before=''

[[ "$app" == /* && "$reference" == /* && -d "$app" && -d "$reference" ]]
[[ "$(git -C "$app" rev-parse HEAD)" == "$expected_app" ]]
[[ -L "$app/node_modules" && "$(realpath "$app/node_modules")" == "$(realpath "$reference/node_modules")" ]]
cmp "$app/package.json" "$reference/package.json"
cmp "$app/package-lock.json" "$reference/package-lock.json"
[[ "$(sha256sum "$config" | cut -d' ' -f1)" == "$expected_config" ]]
[[ ! -e "$backup" && ! -e "$cache" && ! -e "$guard_receipt" ]]

node_modules_snapshot() {
  python3 - "$reference/node_modules" <<'PY'
import hashlib
import os
import stat
import sys

root = os.path.abspath(sys.argv[1])
digest = hashlib.sha256()
for directory, dirs, files in os.walk(root, topdown=True, followlinks=False):
    dirs.sort()
    files.sort()
    for name in [".", *dirs, *files]:
        path = directory if name == "." else os.path.join(directory, name)
        relative = os.path.relpath(path, root)
        info = os.lstat(path)
        fields = (relative, str(stat.S_IFMT(info.st_mode)), str(info.st_size),
                  str(info.st_mtime_ns), str(info.st_ctime_ns),
                  os.readlink(path) if stat.S_ISLNK(info.st_mode) else "")
        digest.update("\0".join(fields).encode("utf-8", "surrogateescape") + b"\0")
print(digest.hexdigest())
PY
}

restore_and_check() {
  result=$?
  trap - EXIT INT TERM
  if [[ -n "$build_pgid" ]]; then
    kill -- "-$build_pgid" 2>/dev/null || true
    wait "$build_pgid" 2>/dev/null || true
    build_pgid=''
  fi
  if [[ -e "$backup" ]]; then
    cp -- "$backup" "$config" || result=1
    python3 - "$backup" <<'PY'
from pathlib import Path
import sys
Path(sys.argv[1]).unlink(missing_ok=True)
PY
  fi
  [[ "$(sha256sum "$config" | cut -d' ' -f1)" == "$expected_config" ]] || result=1
  if [[ -n "$reference_tree_before" ]]; then
    reference_tree_after=$(node_modules_snapshot) || result=1
    [[ "$reference_tree_after" == "$reference_tree_before" ]] || {
      echo 'Reference node_modules tree or mtimes changed during the App build.' >&2
      result=1
    }
    python3 - "$guard_receipt" "$reference_tree_before" "$reference_tree_after" "$expected_config" <<'PY'
import json
from pathlib import Path
import sys
Path(sys.argv[1]).write_text(json.dumps({
    "reference_node_modules_before": sys.argv[2],
    "reference_node_modules_after": sys.argv[3],
    "reference_node_modules_unchanged": sys.argv[2] == sys.argv[3],
    "vite_config_restored_sha256": sys.argv[4],
}, indent=2) + "\n")
PY
    printf 'Reference node_modules metadata before: %s\n' "$reference_tree_before"
    printf 'Reference node_modules metadata after:  %s\n' "$reference_tree_after"
  fi
  python3 - "$cache" <<'PY'
from pathlib import Path
import shutil
import sys
path = Path(sys.argv[1])
if path.exists():
    shutil.rmtree(path)
PY
  exit "$result"
}
trap restore_and_check EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

(( $(df -Pk /home/user | awk 'NR==2 {print $4}') >= 18*1024*1024 ))
reference_tree_before=$(node_modules_snapshot)
cp -- "$config" "$backup"
python3 - "$config" "$expected_config" <<'PY'
from pathlib import Path
import hashlib
import sys

path = Path(sys.argv[1])
expected = sys.argv[2]
source = path.read_text()
if hashlib.sha256(source.encode()).hexdigest() != expected:
    raise SystemExit("Vite config changed from the pinned App revision")
needle = "  return {\n    customLogger: logger,"
replacement = "  return {\n    cacheDir: process.env.SVL2_VITE_CACHE_DIR,\n    customLogger: logger,"
if source.count(needle) != 1:
    raise SystemExit("Expected exactly one Vite config insertion point")
path.write_text(source.replace(needle, replacement, 1))
PY

setsid --wait bash -c 'cd -- "$1"; exec env SVL2_VITE_CACHE_DIR="$2" npm run build' \
  svl2-app-build "$app" "$cache" >"$log" 2>&1 &
build_pgid=$!
while kill -0 "$build_pgid" 2>/dev/null; do
  free_kib=$(df -Pk /home/user | awk 'NR==2 {print $4}')
  if (( free_kib < 16*1024*1024 )); then
    kill -- "-$build_pgid" 2>/dev/null || true
    wait "$build_pgid" || true
    echo "Stopped App build below 16 GiB free: ${free_kib} KiB" >&2
    exit 1
  fi
  sleep 2
done
wait "$build_pgid"
build_pgid=''
