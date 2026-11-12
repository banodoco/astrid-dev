"""Check that newly added project packs follow the project templates."""
from __future__ import annotations

import re
from pathlib import Path

from check_project_planning import LABELS as PLANNING_LABELS
from project_contract import PLAN_FOLDER
from records import PROJECT_FIELDS, git_result, read_text


def _headings(text: str) -> list[str]:
    return re.findall(r"^## (.+)$", text, re.M)


def _planning_labels(text: str) -> list[str]:
    match = re.search(r"^## Planning evidence\s*$", text, re.M)
    if match is None:
        return []
    tail = text[match.end():]
    end = re.search(r"^## \S", tail, re.M)
    block = tail[:end.start()] if end else tail
    return re.findall(r"^\*\*(.+?):\*\*", block, re.M)


def _first_table_header(text: str) -> list[str] | None:
    for line in text.splitlines():
        if line.startswith("|"):
            return [cell.strip() for cell in line.strip().strip("|").split("|")]
    return None


def template_shape(root: Path) -> dict[str, object]:
    """Read the ordered declarations from the three project templates."""
    plan = read_text(Path(root), Path("templates/project/plan.md"))
    inputs = read_text(Path(root), Path("templates/project/inputs.md"))
    tasks = read_text(Path(root), Path("templates/project/tasks.md"))
    return {
        "task_header": _first_table_header(tasks),
        "plan_headings": _headings(plan),
        "inputs_headings": _headings(inputs),
        "input_labels": _planning_labels(inputs),
    }


def _ordered_error(actual: list[str], expected: list[str]) -> str | None:
    cursor = 0
    for item in expected:
        try:
            cursor = actual.index(item, cursor) + 1
        except ValueError:
            if item in actual:
                return f"heading '## {item}' is out of order; move it to where the template puts it"
            return f"missing heading '## {item}'; add it where the template puts it"
    return None


def shape_errors(folder: str, shape: dict[str, object], root: Path) -> list[str]:
    """Report template shape faults not already owned by another check."""
    root = Path(root)
    pack = root / "plans" / folder
    errors: list[str] = []

    for name, key in (("plan.md", "plan_headings"), ("inputs.md", "inputs_headings")):
        path = pack / name
        if not path.is_file():
            continue  # plan-files owns missing pack files
        text = read_text(root, Path("plans") / folder / name)
        if name == "plan.md":
            header = text.split("## ", 1)[0]
            if any(not re.search(r"^\*\*" + re.escape(field) + r":\*\*\s*.+$", header, re.M)
                   for field in PROJECT_FIELDS):
                continue  # plan-catalog owns the six plan fields
        required = shape[key]
        if name == "inputs.md":
            required = [heading for heading in required if heading != "Planning evidence"]
        actual = _headings(text)
        message = _ordered_error(actual, required)
        if message:
            errors.append(f"plans/{folder}/{name}: {message}. templates/project/{name} declares the shape of a new pack.")

    inputs_path = pack / "inputs.md"
    if inputs_path.is_file():
        inputs = read_text(root, Path("plans") / folder / "inputs.md")
        if re.search(r"^## Planning evidence\s*$", inputs, re.M):
            expected_labels = shape["input_labels"]
            uncovered = [label for label in expected_labels if label not in PLANNING_LABELS]
            actual_labels = _planning_labels(inputs)
            cursor = 0
            for label in uncovered:
                try:
                    cursor = actual_labels.index(label, cursor) + 1
                except ValueError:
                    if label in actual_labels:
                        message = f"label '**{label}:**' under '## Planning evidence' is out of order; move it to where the template puts it"
                    else:
                        message = f"missing label '**{label}:**' under '## Planning evidence'; add it where the template puts it"
                    errors.append(f"plans/{folder}/inputs.md: {message}. templates/project/inputs.md declares the shape of a new pack.")
                    break

    tasks_path = pack / "tasks.md"
    if tasks_path.is_file():
        header = _first_table_header(read_text(root, Path("plans") / folder / "tasks.md"))
        expected_header = shape["task_header"]
        if header is None:
            errors.append(f"plans/{folder}/tasks.md: no task table; start the file's first table with the template's header row. templates/project/tasks.md declares the shape of a new pack.")
        elif header != expected_header:
            errors.append(f"plans/{folder}/tasks.md: the first table's header row differs from the template's; copy it exactly. templates/project/tasks.md declares the shape of a new pack.")

    return errors


def new_packs(base: str, root: Path) -> list[str]:
    """Return new pack folders in the working tree, excluding Git-detected renames."""
    root = Path(root)
    valid = git_result(root, "cat-file", "-e", f"{base}^{{commit}}")
    if valid.returncode:
        raise ValueError(f"base revision {base!r} is unavailable")

    changed = git_result(root, "diff", "-M", "--name-status", base, "--", "plans/*/plan.md")
    if changed.returncode:
        raise ValueError(f"can't compare project changes: {changed.stderr.strip()}")
    renamed = set()
    candidates = set()
    for line in changed.stdout.splitlines():
        fields = line.split("\t")
        status = fields[0]
        if status.startswith("R") and len(fields) == 3:
            renamed.add(Path(fields[2]).parent.name)
        elif status != "D" and len(fields) >= 2:
            candidates.add(Path(fields[-1]).parent.name)

    untracked = git_result(root, "ls-files", "--others", "--exclude-standard", "--", "plans/")
    if untracked.returncode:
        raise ValueError(f"can't list untracked project files: {untracked.stderr.strip()}")
    candidates.update(Path(name).parent.name for name in untracked.stdout.splitlines()
                      if Path(name).name == "plan.md")

    new = set()
    for folder in candidates - renamed:
        if not PLAN_FOLDER.fullmatch(folder) or not (root / "plans" / folder / "plan.md").is_file():
            continue
        prior = git_result(root, "cat-file", "-e", f"{base}:plans/{folder}/plan.md")
        if prior.returncode:
            new.add(folder)
    return sorted(new)
