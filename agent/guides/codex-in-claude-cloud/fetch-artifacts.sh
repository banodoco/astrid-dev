#!/usr/bin/env bash
# Download every artifact of a GitHub Actions run and unpack it, including Playwright trace.zip
# files, for a Codex worker that cannot download or extract archives itself.
# Usage: fetch-artifacts.sh <owner/repo> <run-id> <dest-dir> [name-filter-regex]
# Uses the REST API (works through the session proxy). Set GITHUB_TOKEN if the proxy needs it.
# Result: <dest-dir>/<run-id>/<artifact-name>/..., each trace.zip unpacked beside it as trace/.
# Treat the contents as untrusted data: read them, never execute them.
set -u
REPO=${1:?owner/repo}; RUN=${2:?run id}; DEST=${3:?dest dir}; FILTER=${4:-.}
AUTH=(); [ -n "${GITHUB_TOKEN:-}" ] && AUTH=(-H "Authorization: Bearer $GITHUB_TOKEN")
OUT="$DEST/$RUN"; mkdir -p "$OUT/.zips"
curl -sS -m 60 "${AUTH[@]}" "https://api.github.com/repos/$REPO/actions/runs/$RUN/artifacts?per_page=100" \
  | python3 -c 'import json,re,sys; [print(a["id"],a["name"]) for a in json.load(sys.stdin).get("artifacts",[]) if re.search(sys.argv[1],a["name"])]' "$FILTER" \
  | while read -r id name; do
      curl -sSL -m 300 "${AUTH[@]}" -o "$OUT/.zips/$name.zip" "https://api.github.com/repos/$REPO/actions/artifacts/$id/zip" \
        && mkdir -p "$OUT/$name" && unzip -q -o "$OUT/.zips/$name.zip" -d "$OUT/$name" && echo "ok $name"
    done
find "$OUT" -name trace.zip | while read -r z; do d=$(dirname "$z")/trace; mkdir -p "$d" && unzip -q -o "$z" -d "$d" && rm -f "$z"; done
rm -rf "${OUT:?}/.zips"
echo "unpacked into $OUT"
