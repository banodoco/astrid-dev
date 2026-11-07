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
from gap_relationships import parse_gap_relationships
from project_contract import plan_gap_ids

REPO_URL = "https://github.com/banodoco/astrid-dev"
PILLAR = re.compile(r"^### \[([^\]]+)\]\((pillars/[^)]+\.md)\)\s*$", re.M)
PRINCIPLE = re.compile(r"^### \[([^\]]+)\]\((principles/[^)]+\.md)\)\s*$", re.M)
GAP_ID = re.compile(r"([A-Z]{1,3}-\d{3})-[a-z0-9-]+\.md")
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
    vision_file = Path("vision/README.md")
    vision = read(root, vision_file)
    if not vision.startswith("# Astrid — "):
        raise ValueError("vision README must have '# Astrid — <headline>'")
    title = heading(vision).removeprefix("Astrid — ")
    intro = section(vision, "Ambition")
    pillar_index = section(vision, "Four pillars")
    pillars = []
    for m in PILLAR.finditer(pillar_index):
        name, relative_path = m.groups()
        descriptor = next((line.strip() for line in pillar_index[m.end():].splitlines() if line.strip()), '')
        path = Path("vision") / relative_path
        body = read(root, path)
        if heading(body) != f"Pillar {len(pillars)+1} — {name}":
            raise ValueError(f"{path}: heading must match README and order")
        details = body.split("\n", 1)[1].strip()
        details = re.split(r"^\*\*(?:Gap|Gaps|References):\*\*", details, maxsplit=1, flags=re.M)[0].strip()
        pillars.append({
            "id": path.stem, "title": name, "descriptor": descriptor,
            "bodyMarkdown": rewrite_links(details, path, revision, root),
        })
    if len(pillars) != 4 or len({p["id"] for p in pillars}) != 4:
        raise ValueError("the vision must reference four distinct pillars")

    principles = []
    for m in PRINCIPLE.finditer(section(vision, "Four driving principles")):
        name, relative_path = m.groups()
        path = Path("vision") / relative_path
        source = read(root, path)
        if heading(source) != name:
            raise ValueError(f"{path}: principle heading must match README")
        details = source.split("\n", 1)[1].strip()
        principles.append({
            "id": path.stem, "title": name,
            "bodyMarkdown": rewrite_links(details, path, revision, root),
        })
    if len(principles) != 4 or len({p["id"] for p in principles}) != 4:
        raise ValueError("the vision must reference four distinct principles")
    valid_anchors = {f"pillar:{p['id']}" for p in pillars} | {f"principle:{p['id']}" for p in principles}

    gaps = []
    seen = set()
    for gap_file in sorted((root / "vision/gaps").glob("*.md")):
        path = gap_file.relative_to(root)
        contents = read(root, path)
        match = re.match(r"^# ([A-Z]{1,3}-\d{3}) — (.+)$", contents, re.M)
        if not match or not GAP_ID.fullmatch(gap_file.name) or GAP_ID.fullmatch(gap_file.name).group(1) != match.group(1):
            raise ValueError(f"{path}: invalid gap heading/name")
        gap_id, name = match.groups()
        if gap_id in seen:
            raise ValueError(f"duplicate gap ID: {gap_id}")
        seen.add(gap_id)
        metadata = next((x for x in contents.splitlines() if x.startswith("**Applies to:**")), "")
        assessment = metadata.split("**Assessment:**", 1)
        if len(assessment) != 2 or not (status := STATUS.match(assessment[1].strip())):
            raise ValueError(f"{path}: Assessment must begin with an allowed status")
        relationships, primary_relationship = parse_gap_relationships(metadata)
        for relationship in relationships:
            if relationship not in valid_anchors:
                raise ValueError(f"{path}: unknown vision relationship {relationship}")
        gap = {"id": gap_id, "title": name,
               "githubUrl": f"{REPO_URL}/blob/{revision}/{path.as_posix()}",
               "assessment": status.group(1).lower(),
               "assessmentDetail": assessment[1].strip(),
               "appliesTo": relationships,
               "primaryAppliesTo": primary_relationship}
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
        linked = plan_gap_ids(plan_text)
        if any(gap not in seen for gap in linked):
            raise ValueError(f"{plan}: unknown gap reference")
        projects.append({
            "id": plan.parent.name, "title": name, "goalMarkdown": goal,
            "status": status, "owner": owner, "estimate": estimate,
            "waitingOn": waiting, "priorityOrder": i + 1,
            "gapIds": linked, "githubUrl": f"{REPO_URL}/blob/{revision}/{plan.as_posix()}",
        })

    return {
        "schemaVersion": 1,
        "source": {"repository": "banodoco/astrid-dev", "revision": revision},
        "vision": {"title": title, "introMarkdown": rewrite_links(intro, vision_file, revision, root),
                   "contributeMarkdown": rewrite_links(section(vision, "Build Astrid with us"), vision_file, revision, root)},
        "pillars": pillars, "principles": principles, "gaps": gaps, "projects": projects,
    }



def render_readme(root: Path, page: dict) -> str:
    """One generated, complete vision index; source documents remain editable.

    Give every pillar/principle and gap a visible entry. A gap's concise closure
    synopsis is derived from its own evidence criteria, not a separate summary
    maintained by an author.
    """
    vision_root = Path("vision")
    vision_text = read(root, vision_root / "README.md")
    intro = section(vision_text, "Ambition")
    contribution = section(vision_text, "Build Astrid with us")
    lines = [
        "# Astrid — " + page["vision"]["title"],
        "",
        "<!-- Ambition and participation live here; pillar, principle and gap summaries are derived from their own documents. -->",
        "",
        "## Ambition",
        "",
        intro,
        "",
        "## Four pillars",
        "",
    ]
    for pillar in page["pillars"]:
        path = vision_root / "pillars" / (pillar["id"] + ".md")
        body = read(root, path)
        tagline = next((line for line in body.splitlines()
                        if line.startswith("**") and line.endswith("**")), "")
        lines.extend([
            f"### [{pillar['title']}](pillars/{pillar['id']}.md)",
            "",
            pillar["descriptor"],
            "",
            tagline,
            "",
        ])

    lines.extend(["## Four driving principles", ""])
    for principle in page["principles"]:
        title = principle["title"]
        path = vision_root / "principles" / (principle["id"] + ".md")
        body = read(root, path).split("\n", 1)[1].strip()
        lines.extend([
            f"### [{title}](principles/{principle['id']}.md)",
            "",
            body,
            "",
        ])

    lines.extend([
        f"## Gaps — {len(page['gaps'])} assessed outcomes",
        "",
        "Each gap describes a result that remains independently verifiable even "
        "if its proposed implementation changes. Follow its link for the full "
        "current assessment, sources and closure evidence. Project completion "
        "never closes a gap automatically.",
        "",
    ])
    for gap in page["gaps"]:
        matches = sorted((root / vision_root / "gaps").glob(gap["id"] + "-*.md"))
        if len(matches) != 1:
            raise ValueError(f"{gap['id']}: expected one canonical gap document")
        path = matches[0].relative_to(root)
        closure = section(read(root, path), "Closure evidence").split("\n\n", 1)[0]
        closure = " ".join(closure.split())
        synopsis = re.split(r"(?<=[.!?])\s+", closure, maxsplit=1)[0]
        synopsis = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", synopsis)
        lines.append(
            f"- **[{gap['id']} — {gap['title']}](gaps/{path.name})** — "
            f"{gap['assessment'].capitalize()}. {synopsis}"
        )

    lines.extend([
        "",
        "## Projects and participation",
        "",
        "The [project catalog](../plans/index.md) owns current priority, "
        "status and accountability; project packs contain their own scope, "
        "sources, tasks and proof. [How to contribute](../docs/contribution-workflow.md) "
        "covers issues, claims, scope review, PRs, writing and completion. "
        "Individual gap records hold their own evidence and closure criteria.",
        "",
    ])
    lines.extend(["## Build Astrid with us", "", contribution, ""])
    return "\n".join(lines)


ROOT_SUMMARY_START = "<!-- vision-summary:start -->"
ROOT_SUMMARY_END = "<!-- vision-summary:end -->"


def render_root_summary(page: dict) -> str:
    """Derive the counts and minimal navigation from canonical vision and catalog."""
    gaps, projects = len(page["gaps"]), len(page["projects"])
    return (
        "Our vision has four main pillars and four guiding principles. "
        f"We've identified {gaps} gaps between us and that end state, "
        f"informing {projects} projects.\n\n"
        "[Vision](vision/README.md) · "
        "[Pillars](vision/README.md#four-pillars) · "
        "[Principles](vision/README.md#four-driving-principles) · "
        f"[Gaps](vision/README.md#gaps--{gaps}-assessed-outcomes) · "
        "[Projects](plans/index.md)"
    )

def render_root_readme(source: str, page: dict) -> str:
    """Keep just the source-dependent summary generated; all other copy is editable."""
    if source.count(ROOT_SUMMARY_START) != 1 or source.count(ROOT_SUMMARY_END) != 1:
        raise ValueError("README.md needs exactly one vision summary marker pair")
    before, remainder = source.split(ROOT_SUMMARY_START, 1)
    _, after = remainder.split(ROOT_SUMMARY_END, 1)
    return before + ROOT_SUMMARY_START + "\n" + render_root_summary(page) + "\n" + ROOT_SUMMARY_END + after


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", help="40-character Astrid Dev revision (defaults to local HEAD)")
    parser.add_argument("--output", type=Path, help="optional JSON output; omit for validation only")
    parser.add_argument("--sync-readme", action="store_true", help="regenerate vision/README.md from canonical sources")
    args = parser.parse_args()
    revision = args.revision or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    try:
        result = build(ROOT, revision)
        expected_readme = render_readme(ROOT, result)
        readme = ROOT / "vision/README.md"
        root_readme = ROOT / "README.md"
        root_text = root_readme.read_text(encoding="utf-8")
        expected_root_text = render_root_readme(root_text, result)
        if args.sync_readme:
            readme.write_text(expected_readme, encoding="utf-8")
            if root_text != expected_root_text:
                root_readme.write_text(expected_root_text, encoding="utf-8")
        else:
            if readme.read_text(encoding="utf-8") != expected_readme:
                raise ValueError("vision/README.md is stale; run python3 scripts/export_public_vision.py --sync-readme")
            if root_text != expected_root_text:
                raise ValueError("README.md vision summary is stale; run python3 scripts/export_public_vision.py --sync-readme")
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
