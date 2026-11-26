"""Read-only delivery composition of existing Astrid Dev Markdown contracts.

All interpretation comes from the established domain readers. No persistent
graph, new authoring format, live GitHub calls or workflow execution.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from otto.relationships import RecordRef as _RecordRef, RelationshipIndex as _RelationshipIndex
from otto_dev import GAP_FILE, _collect_delivery
from relationships import RecordRef, RelationshipError, RelationshipIndex


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class DeliveryPath:
    goal: _RecordRef
    gap: _RecordRef
    project: _RecordRef
    release: _RecordRef
    gap_role: str
    project_role: str


def load_delivery(root: Path = ROOT) -> _RelationshipIndex:
    """Collect canonical Dev records, then build Otto's configured graph."""
    records, links, enablers = _collect_delivery(root)
    return RelationshipIndex(records, links, enablers=enablers)



def deliveries_for_goal(
    graph: _RelationshipIndex, goal: _RecordRef
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
    graph: _RelationshipIndex, issue_number: str | int
) -> tuple[_RecordRef, ...]:
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
