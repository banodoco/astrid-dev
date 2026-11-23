#!/bin/bash
source /root/codex/le4/isolated4/env.sh
export PYTHONDONTWRITEBYTECODE=1
PY=/root/codex/le4/isolated4/program/versions/981fb90f1a54/py/bin/python
D=/root/codex/le4/isolated4
for i in 1 2 3; do
  s=$(date -u +%H:%M:%S.%N | cut -c1-15); echo "## a$i start $s"; timeout 150 $PY -X utf8 /root/codex/le4/run9/diag/open-read.py le4-f2-p136 p136 2>&1 | tail -4; echo "## a$i end $(date -u +%H:%M:%S.%N | cut -c1-15)"
  s=$(date -u +%H:%M:%S.%N | cut -c1-15); echo "## b$i start $s"; timeout 150 $PY -X utf8 $D/hist-read.py le4-f2-p136 p136 2>&1 | tail -4; echo "## b$i end $(date -u +%H:%M:%S.%N | cut -c1-15)"
done
echo "## RUN136 DONE $(date -u +%H:%M:%S)"
