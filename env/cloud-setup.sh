#!/usr/bin/env bash
# Cloud environment setup script for Astrid worker sessions (see env/README.md).
# Runs as root when a session's container is built, before Claude starts. It must finish fast (a slow
# setup script is stopped), so it only fetches astrid-dev and installs the test commands. Each command
# builds <checkout>.env/ on its first run, from the checkout root, then runs the tests:
#   astrid-agent-pytest, astrid-agent-pytest-pod, vibecomfy-pytest
# plus astrid-baseline-diff (env/baseline-diff.py), which needs no build.
# Never fails the session.
set -u
test -d /opt/astrid-dev || git clone -q --depth 1 https://github.com/banodoco/astrid-dev /opt/astrid-dev || exit 0
cmd() { # name setup-script test-script
  printf '#!/bin/sh\nset -e\nCO=$(pwd -P)\ntest -f "$CO.env/setup.txt" || bash /opt/astrid-dev/env/%s >&2\nexec bash /opt/astrid-dev/env/%s "$@"\n' "$2" "$3" > "/usr/local/bin/$1"
  chmod 755 "/usr/local/bin/$1"
}
cmd astrid-agent-pytest agent-setup.sh agent-pytest.sh
cmd astrid-agent-pytest-pod agent-setup.sh agent-pytest-pod.sh
cmd vibecomfy-pytest vc-setup.sh vc-pytest.sh
printf '#!/bin/sh\nexec python3 -I /opt/astrid-dev/env/baseline-diff.py "$@"\n' > /usr/local/bin/astrid-baseline-diff
chmod 755 /usr/local/bin/astrid-baseline-diff
exit 0
