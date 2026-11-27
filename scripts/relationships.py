"""Bind Otto's shared relationship graph to Dev's legacy API and messages."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from otto.config import read_declaration
from otto.records import Record
from otto.relationships import (
    EnablerRule,
    RecordRef as _RecordRef,
    Relationship as _Relationship,
    RelationshipError as _RelationshipError,
    RelationshipIndex as _RelationshipIndex,
    RelationshipSchema,
)


class RelationshipError(ValueError):
    """A structurally invalid Dev record identity or authored link."""


# Read declaration data only, not the workspace inventory. In-memory callers
# and delivery queries over partial source trees do not require otto.toml in
# their selected root. This is a local, immutable schema, not an Otto global.
_declaration, _source_map = read_declaration(
    Path(__file__).resolve().parents[1] / "otto.toml", display_path="otto.toml")
_SCHEMA = RelationshipSchema.from_declarations(
    (kind["name"] for kind in _declaration["record_kinds"]),
    _declaration["relation_kinds"], _source_map,
    enablers=EnablerRule("project", "addresses", "primary",
                         "foundational enabler must be an existing project"))


def RecordRef(kind: str, id: str) -> _RecordRef:
    # Membership and identity must fail at construction, as before; Otto's
    # schema.ref owns both checks and returns the shared typed identity.
    try:
        return _SCHEMA.ref(kind, id)
    except _RelationshipError as exc:
        raise RelationshipError(exc.message) from exc


def Relationship(source: _RecordRef, kind: str, target: _RecordRef,
                 role: str, source_path: str,
                 source_line: int | None = None) -> _Relationship:
    try:
        return _Relationship(source, kind, target, role, source_path,
                             source_line, schema=_SCHEMA)
    except _RelationshipError as exc:
        # The legacy body can already contain a path. Do not prepend another
        # path/line, or attempt to strip a prefix from the body itself.
        raise RelationshipError(exc.message) from exc


def RelationshipIndex(records: Iterable[Record | _RecordRef],
                      relationships: Iterable[_Relationship], *,
                      enablers: Iterable[_RecordRef] = ()) -> _RelationshipIndex:
    try:
        return _RelationshipIndex(records, relationships, schema=_SCHEMA,
                                  enablers=enablers)
    except _RelationshipError as exc:
        raise RelationshipError(exc.message) from exc
