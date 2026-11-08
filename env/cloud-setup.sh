#!/usr/bin/env bash
# Cloud environment setup script for Astrid worker sessions (see env/README.md).
# Runs as root when a session's container is built, after its repositories are cloned and before Claude starts,
# from the directory that holds the checkouts. For each Astrid checkout present it builds <checkout>.env/ and
# installs its test commands on PATH, so workers run no setup script and need no copy of these scripts.
# Never fails the session: a failed step is logged in /var/log/astrid-cloud-setup.log.
set -u
exec >>/var/log/astrid-cloud-setup.log 2>&1
ENV=/opt/astrid-dev/env
test -d /opt/astrid-dev || git clone -q --depth 1 https://github.com/banodoco/astrid-dev /opt/astrid-dev || exit 0
if [ -d astrid-agent ]; then
  (cd astrid-agent && bash "$ENV/agent-setup.sh") && echo "astrid-agent: ready" || echo "astrid-agent: setup FAILED"
  install -m 755 "$ENV/agent-pytest.sh" /usr/local/bin/astrid-agent-pytest
  install -m 755 "$ENV/agent-pytest-pod.sh" /usr/local/bin/astrid-agent-pytest-pod
fi
VC=$(ls -d vibecomfy VibeComfy 2>/dev/null | head -1)
if [ -n "$VC" ]; then
  (cd "$VC" && bash "$ENV/vc-setup.sh") && echo "$VC: ready" || echo "$VC: setup FAILED"
  install -m 755 "$ENV/vc-pytest.sh" /usr/local/bin/vibecomfy-pytest
fi
exit 0
