#!/usr/bin/env python3
"""Build a read-only public vision snapshot from Astrid Dev's existing Markdown."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

from check_docs import CATALOG, PLAN_LINK, ROOT, catalog_rows, read

REPO_URL = "https://github.com/banodoco/astrid-dev"
PILLAR = re.compile(r"^\d+\. \*\*\[([^\]]+)\]\((pillars/[^)]+\.md)\)\*\* — (.+)$", re.M)
GAP_ID = re.compile(r"([A-Z]{1,3}-\d{3})-[a-z0-9-]+\.md")
GAP_LINK = re.compile(r"\]\(\.\./\.\./visions/gaps/([A-Z]{1,3}-\d{3})-[^)]+\.md\)")
MD_LINK = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\n]+)\)")
STATUS = re.compile(r"^(Open|Partially evidenced|Closed|Needs recheck)\b", re.I)
REVISION = re.compile(r"^[a-f0-9]{40}$", re.I)


def heading(text: str, prefix: str = "# ") -> str:
    match = re.search(rf"^{re.escape(prefix)}(.+)$", text, re.M)
    if not match:
        raise ValueError(f"missing heading: {prefix}")
    return match.group(1).strip()


def section(text: str, title: str) -> str:
    match = re.search(rf"^## {re.escape(title)}\s*$", text, re.M)
    if not match:
        raise ValueError(f"missing section: {title}")
    tail = text[match.end():]
    next_section = re.search(r"^## ", tail, re.M)
    return tail[:next_section.start()].strip() if next_section else tail.strip()


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower().replace("'", "")).strip("-")


def rewrite_links(text: str, source: Path, revision: str, root: Path) -> str:
    """Internal Markdown links go to the exact GitHub source revision."""
    def replace(match: re.Match[str]) -> str:
        label, target = match.groups()
        if re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", target, re.I):
            return match.group(0)
        file_part, _, fragment = target.partition("#")
        destination = (root / source.parent / (file_part or source.name)).resolve()
        try:
            relative = destination.relative_to(root.resolve())
        except ValueError as exc:
            raise ValueError(f"{source}: link escapes repository: {target}") from exc
        if not destination.exists():
            raise ValueError(f"{source}: nonexistent link: {target}")
        kind = "tree" if destination.is_dir() else "blob"
        url = f"{REPO_URL}/{kind}/{revision}/{quote(relative.as_posix(), safe='/')}"
        if fragment:
            url += f"#{fragment}"
        return f"[{label}]({url})"
    return MD_LINK.sub(replace, text)


def build(root: Path, revision: str) -> dict:
    if not REVISION.fullmatch(revision):
        raise ValueError("revision must be an immutable 40-character commit SHA")
    vision_file = Path("visions/vision.md")
    vision = read(root, vision_file)
    if not vision.startswith("# Astrid — "):
        raise ValueError("vision.md must have '# Astrid — <headline>'")
    title = heading(vision).removeprefix("Astrid — ")
    intro = vision.split("\n\n", 2)[1]
    pillars = []
    for m in PILLAR.finditer(vision):
        name, relative_path, descriptor = m.groups()
        path = Path("visions") / relative_path
        body = read(root, path)
        if heading(body) != f"Pillar {len(pillars)+1} — {name}":
            raise ValueError(f"{path}: heading must match vision.md and order")
        details = body.split("\n", 1)[1].strip()
        details = re.split(r"^\*\*(?:Gap|Gaps|References):\*\*", details, maxsplit=1, flags=re.M)[0].strip()
        pillars.append({
            "id": path.stem, "title": name, "descriptor": descriptor,
            "bodyMarkdown": rewrite_links(details, path, revision, root),
        })
    if len(pillars) != 4 or len({p["id"] for p in pillars}) != 4:
        raise ValueError("the vision must reference four distinct pillars")

    principles_file = Path("visions/principles.md")
    principles_text = read(root, principles_file)
    principles = []
    for m in re.finditer(r"^## (.+)$", principles_text, re.M):
        name = m.group(1).strip()
        if name == "Evidence and delivery":
            break
        content = section(principles_text, name)
        principles.append({
            "id": slug(name), "title": name,
            "bodyMarkdown": rewrite_links(content, principles_file, revision, root),
        })
    if not principles or len({p["id"] for p in principles}) != len(principles):
        raise ValueError("missing or duplicate operating principles")
    valid_anchors = {f"pillar:{p['id']}" for p in pillars} | {f"principle:{p['id']}" for p in principles}

    gaps = []
    seen = set()
    for gap_file in sorted((root / "visions/gaps").glob("*.md")):
        path = gap_file.relative_to(root)
        contents = read(root, path)
        match = re.match(r"^# ([A-Z]{1,3}-\d{3}) — (.+)$", contents)
        if not match or not GAP_ID.fullmatch(gap_file.name) or gap_file.name.split("-")[0] != match.group(1).split("-")[0]:
            raise ValueError(f"{path}: invalid gap heading/name")
        gap_id, name = match.groups()
        if gap_id in seen:
            raise ValueError(f"duplicate gap ID: {gap_id}")
        seen.add(gap_id)
        metadata = next((x for x in contents.splitlines() if x.startswith("**Applies to:**")), "")
        assessment = metadata.split("**Assessment:**", 1)
        if len(assessment) != 2 or not (status := STATUS.match(assessment[1].strip())):
            raise ValueError(f"{path}: Assessment must begin with an allowed status")
        relationships = []
        for dest in re.findall(r"\]\((\.\./(?:pillars/[^)]+|principles\.md(?:#[^)]+)?))\)", assessment[0]):
            if dest.startswith("../pillars/"):
                relationship = "pillar:" + Path(dest).stem
            else:
                _, sep, anchor = dest.partition("#")
                if not sep:
                    raise ValueError(f"{path}: principle relationship must identify a section")
                relationship = "principle:" + anchor
            if relationship not in valid_anchors:
                raise ValueError(f"{path}: unknown vision relationship {relationship}")
            if relationship not in relationships:
                relationships.append(relationship)
        if not relationships:
            raise ValueError(f"{path}: no valid relationships")
        gap = {"id": gap_id, "title": name, "assessment": status.group(1).lower(),
               "assessmentDetail": assessment[1].strip(), "appliesTo": relationships}
        for source_title, out_key in [
            ("Desired state", "desiredMarkdown"),
            ("Current state", "currentMarkdown"),
            ("Gap", "missingMarkdown"),
            ("Closure evidence", "closureEvidenceMarkdown"),
        ]:
            value = section(contents, source_title)
            if not value:
                raise ValueError(f"{path}: empty {source_title}")
            gap[out_key] = rewrite_links(value, path, revision, root)
        gaps.append(gap)

    projects = []
    for i, row in enumerate(catalog_rows(read(root, CATALOG))):
        name, goal, status, owner, estimate, waiting, link = row
        plan = Path("plans") / PLAN_LINK.fullmatch(link).group(1)
        plan_text = read(root, plan)
        declaration = re.findall(r"^\*\*Vision gaps:\*\*\s*(.+)$", plan_text, re.M)
        linked = GAP_LINK.findall(declaration[0]) if declaration else []
        if len(linked) != len(set(linked)) or any(gap not in seen for gap in linked):
            raise ValueError(f"{plan}: duplicate or unknown gap references")
        if not declaration and not re.search(r"^\*\*Vision role:\*\*", plan_text, re.M):
            raise ValueError(f"{plan}: missing gap/enabler declaration")
        projects.append({
            "id": plan.parent.name, "title": name, "goalMarkdown": goal,
            "status": status, "owner": owner, "estimate": estimate,
            "waitingOn": waiting, "priorityOrder": i + 1,
            "gapIds": linked, "githubUrl": f"{REPO_URL}/blob/{revision}/{plan.as_posix()}",
        })

    return {
        "source": {"repository": "banodoco/astrid-dev", "revision": revision},
        "vision": {"title": title, "introMarkdown": rewrite_links(intro, vision_file, revision, root)},
        "pillars": pillars, "principles": principles, "gaps": gaps, "projects": projects,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", help="40-character Astrid Dev revision (defaults to local HEAD)")
    parser.add_argument("--output", type=Path, help="optional JSON output; omit for validation only")
    args = parser.parse_args()
    revision = args.revision or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    try:
        result = build(ROOT, revision)
    except (ValueError, OSError) as exc:
        print(f"ERROR public vision content: {exc}")
        return 1
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Public vision content OK: {len(result['pillars'])} pillars, "
          f"{len(result['principles'])} principles, {len(result['gaps'])} gaps, "
          f"{len(result['projects'])} projects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
