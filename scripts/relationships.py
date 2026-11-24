"""Immutable typed links between existing Astrid Dev records.

This module reads no files and owns no facts. Domain readers remain authoritative;
a relationship's source_path points back to the authored declaration.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


class RelationshipError(ValueError):
    """A structurally invalid record identity or authored link."""


RECORD_KINDS = frozenset({"goal", "gap", "project", "release", "issue"})
RELATION_KINDS = {
    "measures": ("gap", "goal", frozenset({"primary", "supporting"})),
    "addresses": ("project", "gap", frozenset({"primary", "supporting"})),
    "includes": ("release", "project", frozenset({"included"})),
    "listed-in": ("issue", "release", frozenset({"frozen"})),
}


@dataclass(frozen=True, order=True)
class RecordRef:
    kind: str
    id: str

    def __post_init__(self) -> None:
        if self.kind not in RECORD_KINDS:
            raise RelationshipError(f"unknown record kind: {self.kind!r}")
        if (not self.id or self.id != self.id.strip()
                or any(c.isspace() or ord(c) < 32 for c in self.id)):
            raise RelationshipError(f"invalid {self.kind} identity: {self.id!r}")

    def __str__(self) -> str:
        return f"{self.kind}:{self.id}"


@dataclass(frozen=True)
class Relationship:
    source: RecordRef
    kind: str
    target: RecordRef
    role: str
    source_path: str

    def __post_init__(self) -> None:
        rule = RELATION_KINDS.get(self.kind)
        if rule is None:
            raise RelationshipError(f"unknown relationship kind: {self.kind!r}")
        if (self.source.kind, self.target.kind) != rule[:2]:
            raise RelationshipError(
                f"{self.kind} requires {rule[0]} -> {rule[1]}, "
                f"got {self.source.kind} -> {self.target.kind}")
        if self.role not in rule[2]:
            raise RelationshipError(f"{self.kind}: invalid role {self.role!r}")
        if (not self.source_path or self.source_path.startswith("/")
                or "\\" in self.source_path
                or ".." in self.source_path.split("/")
                or any(ord(c) < 32 for c in self.source_path)):
            raise RelationshipError(f"{self.kind}: invalid provenance {self.source_path!r}")

    def identity(self) -> tuple[RecordRef, str, RecordRef]:
        """Role is intentionally excluded: primary+supporting is a conflict."""
        return self.source, self.kind, self.target


class RelationshipIndex:
    """Deterministic read-only snapshot; never a secondary canonical registry."""

    def __init__(
        self,
        records: Iterable[RecordRef],
        relationships: Iterable[Relationship],
        *,
        enablers: Iterable[RecordRef] = (),
    ) -> None:
        incoming_records = tuple(records)
        self.records = frozenset(incoming_records)
        if len(self.records) != len(incoming_records):
            raise RelationshipError("duplicate record identity")
        accepted_enablers = frozenset(enablers)
        if any(ref.kind != "project" or ref not in self.records for ref in accepted_enablers):
            raise RelationshipError("foundational enabler must be an existing project")
        self.enablers = accepted_enablers

        links = tuple(relationships)
        identities: set[tuple[RecordRef, str, RecordRef]] = set()
        for link in links:
            # Gapless enablers must not also declare a project-to-gap edge.
            if link.source in accepted_enablers and link.kind == "addresses":
                raise RelationshipError(
                    f"{link.source_path}: enabler {link.source} cannot declare addresses")
            if link.source not in self.records or link.target not in self.records:
                missing = link.source if link.source not in self.records else link.target
                raise RelationshipError(
                    f"{link.source_path}: {link.kind} names unknown {missing}")
            if link.identity() in identities:
                raise RelationshipError(
                    f"{link.source_path}: duplicate or contradictory {link.kind} "
                    f"{link.source} -> {link.target}")
            identities.add(link.identity())
        self.relationships = tuple(sorted(
            links,
            key=lambda e: (e.source.kind, e.source.id, e.kind,
                           e.target.kind, e.target.id, e.role, e.source_path)))

        # These are authored domain contracts, not a new workflow state machine.
        for kind, link_kind in (("gap", "measures"), ("project", "addresses")):
            for ref in sorted(self.records):
                if ref.kind != kind or ref in accepted_enablers:
                    continue
                primary = [e for e in self.relationships
                           if e.source == ref and e.kind == link_kind
                           and e.role == "primary"]
                if len(primary) != 1:
                    raise RelationshipError(
                        f"{ref}: expected one primary {link_kind} relationship, "
                        f"found {len(primary)}")

    def outgoing(self, source: RecordRef, kind: str | None = None) -> tuple[Relationship, ...]:
        return tuple(edge for edge in self.relationships
                     if edge.source == source and (kind is None or edge.kind == kind))

    def incoming(self, target: RecordRef, kind: str | None = None) -> tuple[Relationship, ...]:
        return tuple(edge for edge in self.relationships
                     if edge.target == target and (kind is None or edge.kind == kind))
