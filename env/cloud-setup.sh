#!/usr/bin/env bash
# Cloud environment setup script for Astrid worker sessions (see env/README.md).
# Runs as root when a session's container is built, before Claude starts. It must finish fast (a slow
# setup script is stopped), so it only fetches astrid-dev and installs the test commands. Each command
# builds <checkout>.env/ on its first run, from the checkout root, then runs the tests:
#   astrid-agent-pytest, astrid-agent-pytest-pod, vibecomfy-pytest
# Never fails the session.
set -u
test -d /opt/astrid-dev || git clone -q --depth 1 https://github.com/banodoco/astrid-dev /opt/astrid-dev || exit 0
cmd() { # name setup-script test-script
  printf '#!/bin/sh\nset -e\nCO=$(pwd -P)\ntest -x "$CO.env/venv/bin/python" || bash /opt/astrid-dev/env/%s >&2\nexec bash /opt/astrid-dev/env/%s "$@"\n' "$2" "$3" > "/usr/local/bin/$1"
  chmod 755 "/usr/local/bin/$1"
}
cmd astrid-agent-pytest agent-setup.sh agent-pytest.sh
cmd astrid-agent-pytest-pod agent-setup.sh agent-pytest-pod.sh
cmd vibecomfy-pytest vc-setup.sh vc-pytest.sh
exit 0
