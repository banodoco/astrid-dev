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


# A deleted pack copied to a new folder can be indistinguishable from a rename.
def new_packs(base: str, root: Path) -> list[str]:
    """Return new pack folders in the working tree, excluding Git-detected renames."""
    import os
    import shutil
    import subprocess
    import tempfile

    root = Path(root)
    valid = git_result(root, "cat-file", "-e", f"{base}^{{commit}}")
    if valid.returncode:
        raise ValueError(f"base revision {base!r} is unavailable")

    def git_path(name: str) -> Path:
        result = git_result(root, "rev-parse", "--git-path", name)
        if result.returncode:
            raise ValueError(f"can't locate Git {name}: {result.stderr.strip()}")
        path = Path(result.stdout.strip())
        return path if path.is_absolute() else root / path

    with tempfile.TemporaryDirectory() as temporary:
        temporary = Path(temporary)
        index = temporary / "index"
        real_index = git_path("index")
        if real_index.exists():
            shutil.copyfile(real_index, index)
        objects = temporary / "objects"
        objects.mkdir()
        env = os.environ.copy()
        env["GIT_INDEX_FILE"] = str(index)
        env["GIT_OBJECT_DIRECTORY"] = str(objects)
        alternates = [str(git_path("objects").resolve())]
        if env.get("GIT_ALTERNATE_OBJECT_DIRECTORIES"):
            alternates.append(env["GIT_ALTERNATE_OBJECT_DIRECTORIES"])
        env["GIT_ALTERNATE_OBJECT_DIRECTORIES"] = os.pathsep.join(alternates)

        def run(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(["git", *args], cwd=root, env=env, text=True,
                                  capture_output=True, check=False)

        added = run("add", "-A", "--", "plans/")
        if added.returncode:
            raise ValueError(f"can't snapshot project changes: {added.stderr.strip()}")
        changed = run("diff", "--cached", "-M20%", "--name-status", "-z", base, "--", "plans/")
        if changed.returncode:
            raise ValueError(f"can't compare project changes: {changed.stderr.strip()}")

    renamed = set()
    candidates = set()
    fields = iter(changed.stdout.split("\0"))
    pack_files = {"plan.md", "inputs.md", "tasks.md"}
    for status in fields:
        if not status:
            break
        source = Path(next(fields))
        destination = Path(next(fields)) if status.startswith(("R", "C")) else source
        if destination.parts[:1] != ("plans",) or len(destination.parts) != 3:
            continue
        if destination.name == "plan.md" and status != "D":
            candidates.add(destination.parent.name)
        if (status.startswith("R") and len(source.parts) == 3
                and source.parts[0] == "plans" and source.name in pack_files
                and destination.name in pack_files and source.parent != destination.parent
                and not (root / source.parent).exists()):
            prior = git_result(root, "cat-file", "-e", f"{base}:{source.parent}/plan.md")
            if not prior.returncode:
                renamed.add(destination.parent.name)

    new = set()
    for folder in candidates - renamed:
        if not PLAN_FOLDER.fullmatch(folder) or not (root / "plans" / folder / "plan.md").is_file():
            continue
        prior = git_result(root, "cat-file", "-e", f"{base}:plans/{folder}/plan.md")
        if prior.returncode:
            new.add(folder)
    return sorted(new)
