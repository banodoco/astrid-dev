"""Read-only delivery composition of existing Astrid Dev Markdown contracts.

All interpretation comes from the established domain readers. No persistent
graph, new authoring format, live GitHub calls or workflow execution.
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

import gap_relationships as goal_links
from gap_relationships import gap_metadata
from project_contract import PLAN_FOLDER, plan_gap_links, project_number
from records import release_brief
from relationships import RecordRef, Relationship, RelationshipError, RelationshipIndex
from vision_subject import parse_subject


ROOT = Path(__file__).resolve().parents[1]
GAP_FILE = re.compile(r"^([A-Z]{1,3}-\d{3})-[a-z0-9-]+\.md$")


@dataclass(frozen=True)
class DeliveryPath:
    goal: RecordRef
    gap: RecordRef
    project: RecordRef
    release: RecordRef
    gap_role: str
    project_role: str


def load_delivery(root: Path = ROOT) -> RelationshipIndex:
    """Collect only canonical, authored records and validated links.

    Read-only: draft release issue pulls are *not* proof of release membership.
    No unlabeled GitHub API result is silently given a relationship.
    """
    root = Path(root)
    if not root.is_dir():
        raise RelationshipError(f"delivery root is not an existing directory: {root}")
    records: list[RecordRef] = []
    links: list[Relationship] = []
    enablers: list[RecordRef] = []
    gap_sources: dict[str, Path] = {}

    # The existing subject reader owns goal parsing, including stable slug IDs.
    for directory, kind in (("pillars", "pillar"), ("principles", "principle")):
        for path in sorted((root / "vision" / directory).glob("*.md")):
            subject = parse_subject(path.read_text(encoding="utf-8"), path.as_posix())
            for item in subject.get("goals", subject.get("characteristics", ())):
                records.append(RecordRef("goal", f"{kind}:{path.stem}/{item['id']}"))

    # The existing gap parser validates the *actual* subject and heading,
    # and determines the unique primary aspiration.
    for path in sorted((root / "vision/gaps").glob("*.md")):
        matched = GAP_FILE.fullmatch(path.name)
        if not matched:
            raise RelationshipError(f"{path}: gap filename lacks stable ID")
        text = path.read_text(encoding="utf-8")
        gap = RecordRef("gap", matched.group(1))
        provenance = path.relative_to(root).as_posix()
        # Mirror the canonical gap-structure title contract before emitting
        # any edge; a CA-001 filename cannot author a CA-002 relationship.
        required_heading = f"# {gap.id} —"
        if not text.startswith(required_heading):
            heading = text.splitlines()[0] if text else "<empty>"
            raise RelationshipError(
                f"{provenance} ({gap}): heading {heading!r} must start "
                f"{required_heading!r} to match the canonical gap filename")
        previous = gap_sources.get(gap.id)
        if previous is not None:
            raise RelationshipError(
                f"{gap}: duplicate authored sources "
                f"{previous.relative_to(root).as_posix()} and {provenance}")
        gap_sources[gap.id] = path
        records.append(gap)
        parse_goals = getattr(goal_links, "parse_gap_goals", None)
        if parse_goals is None:
            parse_goals = goal_links.parse_gap_aspirations  # Pending PR #1059
        try:
            aspirations, primary = parse_goals(gap_metadata(text), root / "vision")
        except ValueError as exc:
            raise RelationshipError(f"{provenance} ({gap}): {exc}") from exc
        for goal_id in aspirations:
            links.append(Relationship(
                gap, "measures", RecordRef("goal", goal_id),
                "primary" if goal_id == primary else "supporting",
                path.relative_to(root).as_posix()))

    # Plan number is stable even when the folder's title changes.
    # Its own plan.md owns the gap relationship and enabler exception.
    project_folders: dict[str, str] = {}
    for path in sorted((root / "plans").glob("*/plan.md")):
        if not PLAN_FOLDER.fullmatch(path.parent.name):
            continue  # Existing catalog-path check owns malformed folder names.
        project = RecordRef("project", project_number(path))
        provenance = path.relative_to(root).as_posix()
        first_folder = project_folders.get(project.id)
        if first_folder is not None:
            raise RelationshipError(
                f"{provenance} ({project}): duplicate project number {project.id}: "
                f"plans/{first_folder}/plan.md and {provenance}")
        records.append(project)
        project_folders[project.id] = path.parent.name
        plan_text = path.read_text(encoding="utf-8")
        try:
            declared_links = plan_gap_links(plan_text)
        except ValueError as exc:
            raise RelationshipError(f"{provenance} ({project}): {exc}") from exc
        if not declared_links:
            enablers.append(project)
        else:
            # The canonical project parser owns relation role and raw link.
            # Validate the authored target, not just its numeric gap ID.
            for gap_id, role, href in declared_links:
                target = (path.parent / href).resolve()
                canonical = gap_sources.get(gap_id)
                if canonical is None:
                    raise RelationshipError(
                        f"{provenance} ({project}): unknown gap:{gap_id} "
                        f"linked as {href!r}")
                canonical_path = canonical.relative_to(root).as_posix()
                if not target.is_file():
                    raise RelationshipError(
                        f"{provenance} ({project}): gap:{gap_id} link {href!r} "
                        f"does not exist; canonical source is {canonical_path}")
                if target != canonical.resolve():
                    raise RelationshipError(
                        f"{provenance} ({project}): gap:{gap_id} link {href!r} "
                        f"does not name canonical source {canonical_path}")
            for gap_id, role, _ in declared_links:
                links.append(Relationship(
                    project, "addresses", RecordRef("gap", gap_id),
                    role, provenance))

    # A release explicitly includes projects; a project marked done doesn't
    # imply a release. Draft issue snapshots are deliberately *not* proof.
    for path in sorted((root / "releases").glob("*.md")):
        if not path.stem.isdigit():
            continue
        provenance = path.relative_to(root).as_posix()
        release = RecordRef("release", path.stem)
        try:
            brief = release_brief(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            raise RelationshipError(f"{provenance} ({release}): {exc}") from exc
        if brief["number"] != path.stem or brief["title_number"] != path.stem:
            raise RelationshipError(
                f"{provenance} ({release}): heading "
                f"'# Release {brief['title_number'] or '<missing>'}' and "
                f"**Release:** {brief['number'] or '<missing>'} must match "
                f"Release {path.stem} from the filename")
        records.append(release)
        for membership in brief["plans"]:
            number, folder = membership["number"], membership["folder"]
            if project_folders.get(number) != folder:
                raise RelationshipError(
                    f"{provenance}: Plan {number} names unknown folder {folder}")
            links.append(Relationship(
                release, "includes", RecordRef("project", number),
                "included", provenance))
        if brief["issues_frozen"]:
            for row in brief["issues"]:
                issue = RecordRef("issue", str(row["number"]))
                if issue not in records:
                    records.append(issue)
                links.append(Relationship(
                    issue, "listed-in", release, "frozen", provenance))

    return RelationshipIndex(records, links, enablers=enablers)


def deliveries_for_goal(
    graph: RelationshipIndex, goal: RecordRef
) -> tuple[DeliveryPath, ...]:
    """Prove authored goal → gap → project → release links, not gap closure."""
    if goal.kind != "goal":
        raise RelationshipError(f"expected goal, got {goal}")
    paths = []
    for measured in graph.incoming(goal, "measures"):
        for addressed in graph.incoming(measured.source, "addresses"):
            for included in graph.incoming(addressed.source, "includes"):
                paths.append(DeliveryPath(
                    goal, measured.source, addressed.source, included.source,
                    measured.role, addressed.role))
    return tuple(paths)


def frozen_releases_for_issue(
    graph: RelationshipIndex, issue_number: str | int
) -> tuple[RecordRef, ...]:
    """Return only release membership proved by its *frozen* issue ledger."""
    issue = RecordRef("issue", str(issue_number))
    return tuple(link.target for link in graph.outgoing(issue, "listed-in"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", choices=("check", "goal", "issue"))
    parser.add_argument("id", nargs="?")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    if args.query != "check" and not args.id:
        parser.error("goal and issue queries require an ID")
    try:
        graph = load_delivery(args.root)
        if args.query == "check":
            print(f"Validated {len(graph.records)} records and "
                  f"{len(graph.relationships)} typed relationships")
        elif args.query == "goal":
            for path in deliveries_for_goal(graph, RecordRef("goal", args.id)):
                print(f"{path.goal} -> {path.gap} ({path.gap_role}) -> "
                      f"{path.project} ({path.project_role}) -> {path.release}")
        else:
            for release in frozen_releases_for_issue(graph, args.id):
                print(f"issue:{args.id} -> {release}")
    except (ValueError, OSError) as exc:
        print(f"ERROR project delivery: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
