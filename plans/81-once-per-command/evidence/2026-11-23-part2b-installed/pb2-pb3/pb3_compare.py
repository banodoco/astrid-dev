"""Read-only PB-3 bundle digest probe for one VibeComfy checkout."""
from __future__ import annotations

import argparse
import hashlib
import json
import warnings
from pathlib import Path
from unittest.mock import patch

from vibecomfy.cli_loader import load_workflow_any
from vibecomfy.porting.object_info import consume as object_info
from vibecomfy.registry.ready import repo_ready_template_ids
from vibecomfy.security.provenance import Provenance
from vibecomfy.workflow_bundle import emit_bundle


parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=("warm", "cold"), required=True)
parser.add_argument("--output-root", type=Path, required=True)
args = parser.parse_args()

repo = Path.cwd().resolve()
ids = repo_ready_template_ids(root=repo / "ready_templates")
index_ids = [
    item["id"]
    for item in json.loads((repo / "template_index.json").read_bytes())["templates"]
    if item.get("readiness_class") == "ready"
]
assert ids == index_ids, "ready-template registry and index order differ"
assert len(ids) == 53, f"expected 53 ready templates, found {len(ids)}"

for template_id in ids:
    row: dict[str, object] = {"id": template_id, "mode": args.mode}
    warnings_seen: list[list[str]] = []
    lookups: list[int] = []
    orig_resolve = object_info._resolve_class_type

    for iteration in range(2 if args.mode == "warm" else 1):
        sequence: list[str] = []

        def traced(class_type: str, **kwargs):
            sequence.append(class_type)
            return orig_resolve(class_type, **kwargs)

        if args.mode == "cold":
            object_info.reset_cache()
        destination = args.output_root / args.mode / str(iteration) / template_id / "workflow.py"
        phase = "load"
        with patch.object(object_info, "_resolve_class_type", traced), warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                workflow = load_workflow_any(template_id)
                phase = "emit"
                bundle = emit_bundle(workflow, destination, Provenance.AGENT_AUTHORED)
                if iteration == (1 if args.mode == "warm" else 0):
                    row["revision"] = bundle.revision_id
                    row["bundle_sha256"] = [
                        hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in (destination, destination.with_suffix(".vibe.json"))
                    ]
            except Exception as exc:  # Report all template failures in the evidence.
                row.setdefault("failures", []).append(
                    [phase, type(exc).__name__, str(exc), len(sequence), sequence[-1:]]
                )
            warnings_seen.extend([[warning.category.__name__, str(warning.message)] for warning in caught])
        lookups.append(len(sequence))
    row["warnings"] = warnings_seen
    row["lookup_counts"] = lookups
    print(json.dumps(row, sort_keys=True), flush=True)
