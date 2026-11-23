#!/bin/sh
set -eu
exec flock /tmp/astrid-timing.lock /root/codex/plan-81m/attribution-evidence.env/bin/python "$(dirname "$0")/sampler_runner.py" "$@"
