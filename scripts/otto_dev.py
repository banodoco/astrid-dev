"""Dev's canonical authored records and line-addressed relationship adapter.

The domain readers still own interpretation. Location helpers locate accepted
declarations; they neither validate new fields nor introduce new edges.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Otto loads this exact file by path, without adding its directory to sys.path.
_SCRIPT_DIR = str(Path(__file__).resolve().parent)
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from otto.config import Workspace
from otto.ids import RecordRef as _RecordRef, SourceLocation
from otto.markdown import markdown_heading_anchors, section_after_match
from otto.records import Record, RecordBatch, RelationshipRow
from otto.relationships import Relationship as _Relationship

import gap_relationships as goal_links
from gap_relationships import gap_metadata
from project_contract import (
    GAP_LINK, PLAN_FOLDER, VISION_GAPS, VISION_ROLE, plan_gap_links, project_number,
)
from records import ISSUE_ROW, RELEASE_PLAN_LINE, release_brief
from relationships import RecordRef, Relationship, RelationshipError
from vision_subject import CHARACTERISTIC, SECTION, parse_subject


GAP_FILE = re.compile(r"^([A-Z]{1,3}-\d{3})-[a-z0-9-]+\.md$")


def _line(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _section_lines(text: str, name: str, pattern: re.Pattern) -> list[int]:
    """Locate rows in the same trimmed H2 section used by release_brief."""
    heading = re.search(r"^## " + re.escape(name) + r"\s*$", text, re.M)
    if heading is None:
        return []
    raw = section_after_match(text, heading, boundary=r"^## ", flags=re.M)
    first = _line(text, heading.end() + len(raw) - len(raw.lstrip()))
    return [number for number, line in enumerate(raw.strip().splitlines(), first)
            if pattern.fullmatch(line)]


def _goal_locations(text: str, provenance: str, items: list[dict]) -> list[SourceLocation]:
    # parse_subject has already validated this section and the ordered items.
    # Use its own heading patterns, including its whitespace trimming, solely
    # to recover their original source offsets.
    headings = list(SECTION.finditer(text))
    index = next(i for i, match in enumerate(headings)
                 if match.group(1).strip() == "Aspirations")
    start = headings[index].end()
    end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
    raw = text[start:end]
    start += len(raw) - len(raw.lstrip())
    marks = CHARACTERISTIC.finditer(raw.strip())
    anchors = markdown_heading_anchors(text)
    locations = []
    for item, mark in zip(items, marks, strict=True):
        matches = [anchor for level, title, anchor in anchors
                   if level == 3 and title == item["title"]]
        locations.append(SourceLocation(provenance, _line(text, start + mark.start()),
                                        matches[0] if len(matches) == 1 else None))
    return locations


def _collect_delivery(root: Path) -> tuple[
    tuple[Record, ...], tuple[_Relationship, ...], tuple[_RecordRef, ...]
]:
    """Collect only canonical, authored records and validated links.

    Read-only: draft release issue pulls are *not* proof of release membership.
    No unlabeled GitHub API result is silently given a relationship.
    """
    root = Path(root)
    if not root.is_dir():
        raise RelationshipError(f"delivery root is not an existing directory: {root}")
    # A real (possibly partial) authored tree needs at least one canonical
    # source area; an unrelated existing directory is not a valid empty graph.
    if not any((root / name).is_dir() for name in ("vision", "plans", "releases")):
        raise RelationshipError(
            f"delivery root contains no canonical vision/, plans/, or releases/ "
            f"directories: {root}")
    canonical_root = root.resolve()

    # An empty symlinked source area may contain no files for the per-file
    # containment check to examine; refuse escaped and dangling directories.
    for source_name in ("vision", "vision/pillars", "vision/principles",
                        "vision/gaps", "plans", "releases"):
        source_area = root / source_name
        if source_area.is_symlink():
            if not source_area.is_dir():
                raise RelationshipError(
                    f"{source_name}: source directory symlink has no directory target")
            if not source_area.resolve().is_relative_to(canonical_root):
                raise RelationshipError(
                    f"{source_name}: source directory resolves outside delivery root")

    def require_authored_source(path: Path) -> None:
        # Authored facts may be aliased within this tree but not loaded from
        # an external symlink destination masquerading as a canonical path.
        if not path.resolve().is_relative_to(canonical_root):
            raise RelationshipError(
                f"{path.relative_to(root).as_posix()}: "
                "authored source resolves outside delivery root")

    records: list[Record] = []
    links: list[_Relationship] = []
    enablers: list[_RecordRef] = []
    seen_issues: set[_RecordRef] = set()
    gap_sources: dict[str, Path] = {}

    # The existing subject reader owns goal parsing, including stable slug IDs.
    for directory, kind in (("pillars", "pillar"), ("principles", "principle")):
        for path in sorted((root / "vision" / directory).glob("*.md")):
            require_authored_source(path)
            text = path.read_text(encoding="utf-8")
            subject = parse_subject(text, path.as_posix())
            items = subject.get("goals", subject.get("characteristics", ()))
            provenance = path.relative_to(root).as_posix()
            for item, location in zip(items, _goal_locations(text, provenance, items), strict=True):
                ref = RecordRef("goal", f"{kind}:{path.stem}/{item['id']}")
                records.append(Record(ref, location, title=item["title"]))

    # The existing gap parser validates the *actual* subject and heading,
    # and determines the unique primary aspiration.
    for path in sorted((root / "vision/gaps").glob("*.md")):
        require_authored_source(path)
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
        records.append(Record(gap, SourceLocation(provenance, 1)))
        parse_goals = getattr(goal_links, "parse_gap_goals", None)
        if parse_goals is None:
            parse_goals = goal_links.parse_gap_aspirations  # Pending PR #1059
        try:
            metadata = gap_metadata(text)
            aspirations, primary = parse_goals(metadata, root / "vision")
        except ValueError as exc:
            raise RelationshipError(f"{provenance} ({gap}): {exc}") from exc
        metadata_line = next(i for i, line in enumerate(text.splitlines(), 1)
                             if line == metadata)
        for goal_id in aspirations:
            links.append(Relationship(
                gap, "measures", RecordRef("goal", goal_id),
                "primary" if goal_id == primary else "supporting",
                provenance, metadata_line))

    # Plan number is stable even when the folder's title changes.
    # Its own plan.md owns the gap relationship and enabler exception.
    project_folders: dict[str, str] = {}
    for path in sorted((root / "plans").glob("*/plan.md")):
        if not PLAN_FOLDER.fullmatch(path.parent.name):
            continue  # Existing catalog-path check owns malformed folder names.
        require_authored_source(path)
        project = RecordRef("project", project_number(path))
        provenance = path.relative_to(root).as_posix()
        first_folder = project_folders.get(project.id)
        if first_folder is not None:
            raise RelationshipError(
                f"{provenance} ({project}): duplicate project number {project.id}: "
                f"plans/{first_folder}/plan.md and {provenance}")
        project_folders[project.id] = path.parent.name
        plan_text = path.read_text(encoding="utf-8")
        try:
            declared_links = plan_gap_links(plan_text)
        except ValueError as exc:
            raise RelationshipError(f"{provenance} ({project}): {exc}") from exc
        # The validated Vision declaration exists even in a partial fixture
        # that has no title. Prefer the actual H1 when one is present.
        declaration = (VISION_GAPS if declared_links else VISION_ROLE).search(plan_text)
        heading = re.search(r"^# .+$", plan_text, re.M)
        records.append(Record(project, SourceLocation(
            provenance, _line(plan_text, (heading or declaration).start()))))
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
            # Locate the already parsed links using the canonical reader's
            # match spans, including any leading whitespace in its value.
            positions = GAP_LINK.finditer(declaration.group(1))
            for (gap_id, role, _), match in zip(declared_links, positions, strict=True):
                line = _line(plan_text, declaration.start(1) + match.start())
                links.append(Relationship(
                    project, "addresses", RecordRef("gap", gap_id),
                    role, provenance, line))

    # A release explicitly includes projects; a project marked done doesn't
    # imply a release. Draft issue snapshots are deliberately *not* proof.
    for path in sorted((root / "releases").glob("*.md")):
        if not path.stem.isdigit():
            continue
        require_authored_source(path)
        provenance = path.relative_to(root).as_posix()
        release = RecordRef("release", path.stem)
        try:
            text = path.read_text(encoding="utf-8")
            brief = release_brief(text)
        except ValueError as exc:
            raise RelationshipError(f"{provenance} ({release}): {exc}") from exc
        if brief["number"] != path.stem or brief["title_number"] != path.stem:
            raise RelationshipError(
                f"{provenance} ({release}): heading "
                f"'# Release {brief['title_number'] or '<missing>'}' and "
                f"**Release:** {brief['number'] or '<missing>'} must match "
                f"Release {path.stem} from the filename")
        # The strict reader accepted one matching release title and field.
        heading = re.search(r"^# Release ([1-9]\d*) — (\S.+)$", text, re.M)
        records.append(Record(
            release, SourceLocation(provenance, _line(text, heading.start())),
            title=brief["title"], status=brief["state"]))
        membership_lines = _section_lines(text, "Included plans", RELEASE_PLAN_LINE)
        for membership, line in zip(brief["plans"], membership_lines, strict=True):
            number, folder = membership["number"], membership["folder"]
            if project_folders.get(number) != folder:
                raise RelationshipError(
                    f"{provenance}: Plan {number} names unknown folder {folder}")
            links.append(Relationship(
                release, "includes", RecordRef("project", number),
                "included", provenance, line))
        if brief["issues_frozen"]:
            issue_lines = _section_lines(text, "Issues", ISSUE_ROW)
            for row, line in zip(brief["issues"], issue_lines, strict=True):
                issue = RecordRef("issue", str(row["number"]))
                if issue not in seen_issues:
                    records.append(Record(issue, SourceLocation(provenance, line)))
                    seen_issues.add(issue)
                links.append(Relationship(
                    issue, "listed-in", release, "frozen", provenance, line))

    return tuple(records), tuple(links), tuple(enablers)


def load_dev_records(workspace: Workspace) -> RecordBatch:
    """Registered Otto loader: one batch, no second registry or implicit edges."""
    records, links, _ = _collect_delivery(workspace.root)
    return RecordBatch(records, tuple(
        RelationshipRow(edge.source, edge.kind, edge.target, edge.role,
                        edge.source_path, edge.source_line)
        for edge in links))
