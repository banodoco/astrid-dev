#!/usr/bin/env bash
# Reproduce the review admission-order checks against two source trees.
# Usage: reproduce-admission-order.sh BASE_TREE CANDIDATE_TREE
set -euo pipefail
if [[ $# -ne 2 ]]; then
  echo "usage: $0 BASE_TREE CANDIDATE_TREE" >&2
  exit 2
fi
base=$(realpath "$1")
candidate=$(realpath "$2")
selector='action_entries_refuse_duplicate_before_dirty_managed_inventory or discovery_refuses_busy_collection_after_warm_metadata or action_entries_refuse_busy_collection_after_warm_projection'
for tree in "$base" "$candidate"; do
  if [[ ! -f "$tree/tests/core/pack/test_discovery_admission_order.py" ]]; then
    echo "missing admission-order test file under $tree" >&2
    exit 2
  fi
done
printf '\n=== BASE: %s ===\n' "$base"
set +e
(cd "$base" && python -m pytest -q tests/core/pack/test_discovery_admission_order.py -k "$selector")
base_status=$?
printf '\n=== CANDIDATE: %s ===\n' "$candidate"
(cd "$candidate" && python -m pytest -q tests/core/pack/test_discovery_admission_order.py -k "$selector")
candidate_status=$?
set -e
if [[ $base_status -eq 0 ]]; then
  echo "baseline passed; expected the saved pre-correction regression failures" >&2
  exit 1
fi
if [[ $candidate_status -ne 0 ]]; then
  echo "candidate failed the admission-order reproduction" >&2
  exit "$candidate_status"
fi
