"""Read-only release status, with an explicit draft brief snapshot refresh."""
from pathlib import Path
import re

from otto.lifecycle import names
from records import project_fields, release_brief
from otto.markdown import section_by_heading as section, split_table_row

START = "<!-- release-status:start -->"
END = "<!-- release-status:end -->"
HEADING = "## Plan status snapshot"
# Releases before 15 are historical backfill, not live status snapshots.
SNAPSHOT_FIRST_RELEASE = 15


def progress(text):
    """Count only rows in task tables with a final Progress column.

    A tick is a recorded tick, not proof. Preserve unfamiliar dispositions.
    Task IDs need not be unique across sections, so counts are rows, not tasks.
    """
    counts = {"ticked": 0, "open": 0, "other": 0}
    pending = []
    found = False
    in_table = False
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            in_table = False
            continue
        cells = split_table_row(line)
        if cells and cells[0] == "Task / outcome" and cells[-1] == "Progress":
            found = in_table = True
            continue
        if not in_table or not cells or all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        item = cells[0].strip("*").split()
        task = item[0].strip("*\x60") if item else "unnamed row"
        state = cells[-1]
        if re.match(r"^\[[xX]\](?:\s|$)", state):
            counts["ticked"] += 1
        elif re.match(r"^\[ \](?:\s|$)", state):
            counts["open"] += 1
            pending.append(task)
        else:
            counts["other"] += 1
            pending.append(task)
    return counts if found else None, pending


def landing(text, number):
    rows = []
    for line in section(text, "Branches").splitlines():
        if line.strip().startswith("|"):
            cells = split_table_row(line)
            if len(cells) == 5 and cells[2] == f"plan {number}":
                rows.append((cells[3], cells[4]))
    if not rows:
        return "not recorded"
    if any(state not in ("open", "merged") for _, state in rows):
        return "unknown"
    if all(state == "merged" and cut != "not yet cut" for cut, state in rows):
        return "merged"
    if all(cut == "not yet cut" and state == "open" for cut, state in rows):
        return "not cut"
    if any(state == "merged" for _, state in rows):
        return "partial"
    return "open"


def cell(value):
    # Keep repository text as table data, not Markdown/HTML control syntax.
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "&#124;").replace("\n", " ")


def report(root, number, text):
    brief = release_brief(text)
    if brief["number"] != str(number) or brief["state"] not in ("Draft", "Final"):
        raise ValueError("release number or state does not match brief")
    lines = [
        "Generated from the current included plan headers, task Progress tables and recorded branch rows.",
        "Counts are task-table rows (ticked / open / other), not percentage complete. Landing is recorded, not live-verified. No state implies qualification or publication.",
        "",
        "| Plan | Status | Accountable owner (recorded) | Task rows | Recorded landing |",
        "| --- | --- | --- | --- | --- |",
    ]
    findings = []
    seen = set()
    for plan in brief["plans"]:
        n, folder = plan["number"], plan["folder"]
        if n in seen or folder.split("-", 1)[0] != n:
            raise ValueError(f"ambiguous release membership for Plan {n}")
        seen.add(n)
        path = root / "plans" / folder
        fields = project_fields((path / "plan.md").read_text(encoding="utf-8"))
        status, owner = fields["Status"], fields["Owner"]
        if status not in names():
            raise ValueError(f"Plan {n}: invalid status {status!r}")
        tasks = path / "tasks.md"
        counts, pending = progress(tasks.read_text(encoding="utf-8")) if tasks.is_file() else (None, [])
        branch = landing(text, n)
        row = "not recorded" if counts is None else f"{counts['ticked']} / {counts['open']} / {counts['other']}"
        # Owner values may contain plan-relative links. The plan is linked; keep
        # owner as readable text without misdirected relative links.
        owner_text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", owner)
        lines.append(f"| [Plan {n}](../plans/{folder}/plan.md) | {status} | {cell(owner_text)} | {row} | {branch} |")
        flags = []
        if owner.lower().startswith("unassigned") and (status == "active" or branch in ("open", "partial", "merged")):
            flags.append("check accountable owner")
        if status == "queued" and branch in ("partial", "merged"):
            flags.append("reconcile queued status against recorded landing")
        if branch in ("unknown", "not recorded"):
            flags.append("reconcile branch records")
        if counts is None:
            flags.append("no readable task Progress table")
        elif pending:
            ids = ", ".join(cell(v) for v in pending[:8])
            tail = f" (+{len(pending)-8} rows)" if len(pending) > 8 else ""
            flags.append(f"review open/other rows: {ids}{tail}")
        if branch == "merged" and status not in ("done", "cancelled"):
            flags.append("review whole-plan versus release-slice closure and evidence")
        if status == "done" and branch in ("open", "partial", "not cut"):
            flags.append("reconcile done status against release landing")
        if flags:
            findings.append(f"- Plan {n}: " + "; ".join(flags) + ".")
    lines.extend(["", "### Reconciliation prompts", "", *(findings or ["- No mechanical discrepancies found; qualification and scope decisions remain human judgments."])])
    return "\n".join(lines) + "\n"


def snapshot(text):
    if START not in text and END not in text:
        return None
    if text.count(START) != 1 or text.count(END) != 1 or text.index(START) > text.index(END):
        raise ValueError("invalid plan status snapshot markers")
    if len(re.findall(r"^## Plan status snapshot\s*$", text, re.M)) != 1:
        raise ValueError("snapshot needs one Plan status snapshot section")
    region = section(text, "Plan status snapshot")
    if not region.startswith(START + "\n") or not region.endswith("\n" + END):
        raise ValueError("snapshot markers must enclose the Plan status snapshot section")
    body = region.split(START, 1)[1].split(END, 1)[0]
    return body.strip("\n") + "\n"


def refreshed(text, body):
    old = snapshot(text)
    block = START + "\n" + body + END
    if old is not None:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        return before + block + after
    if HEADING in text:
        raise ValueError("existing plan status heading has no snapshot markers")
    anchor = re.search(r"^## Branches\s*$|^## Publication\s*$", text, re.M)
    if anchor is None:
        raise ValueError("missing Branches/Publication section")
    return text[:anchor.start()] + HEADING + "\n\n" + block + "\n\n" + text[anchor.start():]


def validate_change(root: Path, number: int, before: str | None, after: str):
    """Check changed snapshots and the Draft-to-Final gate, not unrelated drift.

    Historical Final snapshots may never be rewritten from later plan records.
    Legacy releases before the feature are not retroactively given a snapshot.
    """
    try:
        previous = snapshot(before or "")
        current = snapshot(after)
        old_state = release_brief(before, strict=False)["state"] if before else None
        new_state = release_brief(after, strict=False)["state"]
        if old_state == "Final":
            if previous != current:
                return ["Final plan status snapshot is historical; restore it"]
            return []
        finalizing = new_state == "Final"
        if current is None:
            if previous is not None or (finalizing and number >= SNAPSHOT_FIRST_RELEASE):
                return ["plan status snapshot required; refresh and check it while Draft"]
            return []
        if current == previous and not finalizing:
            return []
        if current != report(root, number, after):
            return ["plan status snapshot is stale or edited; regenerate with release status --refresh while Draft"]
    except (ValueError, OSError) as exc:
        return [str(exc)]
    return []


def run(root: Path, number: int, *, refresh=False, check=False):
    if number < 1:
        raise ValueError("release number must be positive")
    path = root / "releases" / f"{number}.md"
    text = path.read_text(encoding="utf-8")
    brief = release_brief(text)
    if brief["number"] != str(number):
        raise ValueError("release number does not match brief")
    if brief["state"] == "Final":
        if refresh or check:
            raise ValueError("Final release is historical; do not refresh or compare with live plan state")
        print(snapshot(text) or "No recorded plan status snapshot for this historical release.")
        return 0
    body = report(root, number, text)
    if check:
        if snapshot(text) != body:
            print(f"Release {number}: snapshot missing or stale; run release status {number} --refresh")
            return 1
        print(f"Release {number}: recorded snapshot is current (not a qualification verdict)")
    elif refresh:
        if path.is_symlink() or path.parent.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("unsafe release snapshot target")
        updated = refreshed(text, body)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
        print(f"Release {number}: refreshed plan status snapshot")
    else:
        print(f"# Release {number} — {brief['title']}\n\n" + body, end="")
    return 0
