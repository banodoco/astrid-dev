#!/usr/bin/env python3
"""Record the route (N, X, S or T) that ran each piece of work; summarize for PR review.

Append-only local JSONL under .otto/ (gitignored). Optional provider/model-id stay
local and are never summarized. This records provided facts; it cannot
independently authenticate usage.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path

BASIS = ("runtime-observed", "self-reported")
ROUTES = ("N", "X", "S", "T")
ROLES = ("planning", "research", "implementation", "testing", "review", "other")
FILE = "model-usage.jsonl"


def make_record(route: str, role: str, task: str, basis: str,
                override: str = "", model_id: str = "", provider: str = "",
                effort: str = "unknown", receipt: str = "",
                tokens: int | None = None) -> dict:
    if route not in ROUTES:
        raise ValueError("route must be one of N, X, S or T")
    if not task or not task.strip():
        raise ValueError("task must be named")
    if role not in ROLES or basis not in BASIS:
        raise ValueError("unrecognized model-use role or evidence basis")
    if basis == "runtime-observed" and not receipt:
        raise ValueError("runtime-observed use requires a source receipt/reference")
    if tokens is not None and tokens < 0:
        raise ValueError("token count cannot be negative")
    return {
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "route": route,
        "override": override.strip() or None,
        "provider": provider.strip() or None,
        "model_id": model_id.strip() or None,
        "role": role, "task": task.strip(), "reasoning_effort": effort.strip() or "unknown",
        "basis": basis, "receipt": receipt.strip() or None,
        **({"tokens": tokens} if tokens is not None else {}),
    }


def append_record(folder: Path, record: dict) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / FILE
    raw = (json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_APPEND, 0o600)
    try:
        if os.write(fd, raw) != len(raw):
            raise OSError("incomplete model usage record write")
    finally:
        os.close(fd)
    return path


def read_records(folder: Path) -> list[dict]:
    path = folder / FILE
    if not path.exists():
        return []
    records = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            record = json.loads(line)
            if not all(k in record for k in ("role", "task", "basis")):
                raise ValueError("missing required fields")
            records.append(record)
        except (ValueError, json.JSONDecodeError) as exc:
            raise ValueError(f"{path}:{number}: malformed provenance record: {exc}") from exc
    return records


def summarize(records: list[dict]) -> str:
    """Return one copyable PR line, compatible with completion validation."""
    if not records:
        return ("Routes used: Not recorded — No local invocation records exist; "
                "state why the route is unavailable before submission.")
    entries: dict[tuple, int] = {}
    for record in records:
        key = (record.get("route") or "", record["role"], record.get("override") or "")
        entries[key] = entries.get(key, 0) + 1

    parts = []
    for (route, role, override), count in sorted(entries.items()):
        label = f"{route} for {role}" if route else f"route not recorded for {role}"
        note = f", override: {override}" if override else ""
        parts.append(f"{label} ({count} invocation(s){note})")
    return (
        "Routes used: " + "; ".join(parts) + "\n"
        "Basis: the detailed local JSONL is not a public evidence pack; "
        "a manual record is not independently authenticated."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path,
                        help="Existing .otto/runs/<id> folder; log remains local")
    sub = parser.add_subparsers(dest="command", required=True)
    record = sub.add_parser("record", help="Append one invocation's route")
    record.add_argument("--route", choices=ROUTES, required=True)
    record.add_argument("--override", default="",
                        help="Model name, only if the run used one other than the route's")
    record.add_argument("--model-id", default="", help="Local JSONL only; never summarized")
    record.add_argument("--provider", default="", help="Local JSONL only; never summarized")
    record.add_argument("--role", choices=ROLES, required=True)
    record.add_argument("--task", required=True)
    record.add_argument("--basis", choices=BASIS, default="self-reported")
    record.add_argument("--effort", default="unknown")
    record.add_argument("--receipt", default="")
    record.add_argument("--tokens", type=int)
    sub.add_parser("summary", help="Print copyable review summary; no files published")
    args = parser.parse_args()
    try:
        if args.command == "record":
            path = append_record(args.run_dir, make_record(
                args.route, args.role, args.task, args.basis, args.override,
                args.model_id, args.provider, args.effort, args.receipt, args.tokens))
            print(f"Model invocation recorded locally: {path}")
        else:
            print(summarize(read_records(args.run_dir)))
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Model record error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
