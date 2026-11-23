#!/usr/bin/env bash
# Run focused App Vitest files in a disposable copy beside the product checkout.
set -euo pipefail
CO="$(pwd -P)"
E="$CO.env/app"
command -v node >/dev/null && command -v npm >/dev/null && command -v rsync >/dev/null || { echo 'ENV: node, npm and rsync are required' >&2; exit 3; }
[[ -f "$CO/package-lock.json" && -f "$CO/config/testing/vitest.config.ts" && $# -gt 0 ]] || { echo 'ENV: run from App root with named Vitest files' >&2; exit 3; }
mkdir -p "$E"
rsync -a --delete --exclude .git --exclude node_modules --exclude dist --exclude .env "$CO/" "$E/"
if ! (cd "$E" && npm ci --no-audit --no-fund); then echo 'ENV: npm setup failed' >&2; exit 3; fi
(cd "$E" && npx --no-install vitest run --config config/testing/vitest.config.ts "$@")
