#!/usr/bin/env python3
"""Record actual agent model usage during a run; optionally summarize for PR review.

Append-only local JSONL under .otto/ (gitignored). This records provided facts;
it cannot discover hidden model identity or independently authenticate usage.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path

BASIS = ("runtime-observed", "self-reported")
ROLES = ("planning", "research", "implementation", "testing", "review", "other")
FILE = "model-usage.jsonl"


def make_record(model_id: str, provider: str, role: str, task: str,
                basis: str, effort: str = "unknown", receipt: str = "",
                tokens: int | None = None) -> dict:
    for field, value in (("model", model_id), ("provider", provider), ("task", task)):
        if not value or not value.strip():
            raise ValueError(f"{field} must be named or explicitly 'unknown'")
    if role not in ROLES or basis not in BASIS:
        raise ValueError("unrecognized model-use role or evidence basis")
    if basis == "runtime-observed" and not receipt:
        raise ValueError("runtime-observed use requires a source receipt/reference")
    if tokens is not None and tokens < 0:
        raise ValueError("token count cannot be negative")
    return {
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "provider": provider.strip(),
        "model_id": model_id.strip(),
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
            if not all(k in record for k in ("model_id", "role", "task", "basis")):
                raise ValueError("missing required fields")
            records.append(record)
        except (ValueError, json.JSONDecodeError) as exc:
            raise ValueError(f"{path}:{number}: malformed provenance record: {exc}") from exc
    return records


def summarize(records: list[dict]) -> str:
    """Return one copyable PR line, compatible with completion validation."""
    if not records:
        return ("Models used: Not recorded — No local invocation records exist; "
                "state why model identity is unavailable before submission.")
    entries: dict[tuple, int] = {}
    for record in records:
        key = (record["provider"], record["model_id"], record["role"],
               record.get("reasoning_effort") or "unknown", record["basis"])
        entries[key] = entries.get(key, 0) + 1

    summary = "; ".join(
        f"{provider}/{model} ({role}, effort: {effort}, {basis}, {count} invocation(s))"
        for (provider, model, role, effort, basis), count in sorted(entries.items())
    )
    return (
        "Models used: " + summary + "\n"
        "Basis: 'runtime-observed' means a source receipt was recorded; "
        "'self-reported' is not independently authenticated. "
        "The detailed local JSONL is not a public evidence pack."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path,
                        help="Existing .otto/runs/<id> folder; log remains local")
    sub = parser.add_subparsers(dest="command", required=True)
    record = sub.add_parser("record", help="Append one actual model invocation")
    record.add_argument("--model-id", required=True)
    record.add_argument("--provider", required=True)
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
                args.model_id, args.provider, args.role, args.task,
                args.basis, args.effort, args.receipt, args.tokens))
            print(f"Model invocation recorded locally: {path}")
        else:
            print(summarize(read_records(args.run_dir)))
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Model record error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
