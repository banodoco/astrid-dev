"""Validation of successful generation receipts from the A/B driver."""
import math


def _duration(value):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and value >= 0)


def generation_error(parsed, args):
    if args[:2] == ["timelines", "edit"]:
        data = parsed.get("data")
        revision = data.get("accepted_revision_id") if isinstance(data, dict) else None
        if not isinstance(data, dict) or data.get("status") != "accepted":
            return "timeline output missing accepted status"
        if not isinstance(revision, str) or not revision.strip():
            return "timeline output missing accepted_revision_id"
        return None
    if args[:2] != ["generate", "image"]:
        return None
    task = parsed.get("kernel_task_id")
    if not isinstance(task, str) or not task.strip():
        return "generation output missing kernel_task_id"
    if "--timings" not in args:
        return None
    return timings_error(parsed)


def timings_error(parsed, allow_missing_span=False):
    """Validate timing evidence, with an explicit option for historical records."""
    timings = parsed.get("timings")
    if not isinstance(timings, list) or not timings:
        return "generation output missing requested timings"
    if not (allow_missing_span and "collector_span_seconds" not in parsed) and not _duration(parsed.get("collector_span_seconds")):
        return "generation output missing or invalid collector_span_seconds"
    for row in timings:
        if (not isinstance(row, dict) or not isinstance(row.get("stage"), str)
                or not row["stage"] or not _duration(row.get("seconds"))
                or ("total_seconds" in row and not _duration(row["total_seconds"]))):
            return "generation output contains malformed timing row"
    return None
