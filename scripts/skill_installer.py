"""Install only owned generated Astrid Dev skill packages into agent skill roots."""
from __future__ import annotations

import os
from pathlib import Path
import tempfile

from agent_documents import SKILL_PREFIX
from skill_builder import OUTPUT, check_packages


class CommittedRetargetCleanupError(ValueError):
    """Retarget succeeded; the cleanup failure occurred after publication."""


class PartialInstallationError(ValueError):
    """A later failure left earlier owned link changes installed.

    The completed list contains only operations that actually returned
    successfully. This records a retryable partial state, not a transaction.
    """

    def __init__(self, completed_changes: list[str], failed_link: Path, cause: Exception):
        self.completed_changes = tuple(completed_changes)
        self.failed_link = failed_link
        changed = "; ".join(completed_changes)
        super().__init__(
            f"partial skill installation: {len(completed_changes)} changes completed "
            f"before failure at {failed_link}: {cause}; "
            f"completed links: {changed}; "
            "inspect the destinations and retry skills install"
        )


def default_destinations() -> list[Path]:
    home = Path.home()
    return [path for path in (home / ".claude/skills", home / ".codex/skills",
                              home / ".agents/skills") if path.is_dir() and not path.is_symlink()]


def _target_of(link: Path) -> Path:
    raw = Path(os.readlink(link))
    return (raw if raw.is_absolute() else link.parent / raw).resolve()


def _owned_link(link: Path, root: Path) -> bool:
    if not link.is_symlink():
        return False
    target = _target_of(link)
    return (target.is_relative_to(root / OUTPUT)
            or target.is_relative_to(root / "skills"))


def _identity(path: Path) -> tuple | None:
    try:
        stat = path.lstat()
    except FileNotFoundError:
        return None
    return (stat.st_dev, stat.st_ino, stat.st_mode,
            os.readlink(path) if path.is_symlink() else None)


def _retarget_owned_link(link: Path, source: Path, expected_identity: tuple) -> None:
    """Prepare the new symlink first and replace one owned link in one operation.

    Failure to create the staged symlink or replace the destination preserves
    the old symlink. This is per-entry only: the entire install set is not a
    transaction, and an uncooperative writer can still race after preflight.
    """
    replaced = False
    try:
        # The private same-filesystem directory ensures staging cannot replace
        # an unrelated entry and is normally removed on success or failure.
        with tempfile.TemporaryDirectory(prefix=f".{SKILL_PREFIX}stage-", dir=link.parent) as tmp:
            staged = Path(tmp) / "package"
            staged.symlink_to(source, target_is_directory=True)
            # Preflight and the per-item check ran before staging. Recheck
            # after staging too, so an intervening foreign replacement is not
            # silently overwritten by our atomic publication. This does not
            # eliminate a hostile race between this check and os.replace.
            if _identity(link) != expected_identity:
                raise ValueError(f"installation entry changed during staged retarget: {link}")
            os.replace(staged, link)
            replaced = True
    except OSError as exc:
        if replaced:
            # TemporaryDirectory cleanup may fail AFTER os.replace committed.
            # Do not claim the old link survived; report the actual new target.
            raise CommittedRetargetCleanupError(
                f"retargeted skill directory symlink {link}, but staging cleanup failed: "
                f"{exc}; the new link is installed"
            ) from exc
        raise ValueError(
            f"could not retarget skill directory symlink {link}: {exc}; "
            "the previous owned link was preserved"
        ) from exc


def install_packages(root: Path, destinations: list[Path] | None = None,
                     *, dry_run: bool = False) -> list[str]:
    """Link named packages; never replace other repositories' files or links.

    A former Astrid Dev link into the old skills/ layout is owned and may be
    retargeted or retired. This is not a general cleanup tool.
    """
    root = Path(root).resolve()
    failures = check_packages(root)
    if failures:
        raise ValueError("build/check skills before installing: " + "; ".join(failures))
    package_root = root / OUTPUT
    desired = {
        path.name: path for path in package_root.iterdir()
        if path.is_dir() and not path.is_symlink()
    }
    explicit = destinations is not None
    targets = list(destinations) if explicit else default_destinations()
    if not targets:
        raise ValueError("no installed skill destinations found; pass --destination")
    planned = []
    target_identities = {}
    for target in targets:
        target = Path(target).expanduser()
        if target.is_symlink() or not target.is_dir():
            raise ValueError(f"destination must already be a real directory: {target}")
        canonical = target.resolve()
        if canonical in target_identities:
            raise ValueError(f"duplicate skill destination: {target}")
        target_identities[canonical] = (target, _identity(target))
        for item in sorted(target.iterdir()):
            if (item.name in desired or not item.name.startswith(SKILL_PREFIX)
                    and item.name not in ("astrid-dev", "shared")):
                continue
            if _owned_link(item, root):
                planned.append(("retire", item, None, _identity(item)))
        for name, source in sorted(desired.items()):
            link = target / name
            if link.is_symlink():
                if _target_of(link) == source.resolve():
                    planned.append(("already", link, source, _identity(link)))
                    continue
                if not _owned_link(link, root):
                    raise ValueError(f"foreign symlink, leaving untouched: {link}")
                planned.append(("retarget", link, source, _identity(link)))
            elif link.exists():
                raise ValueError(f"foreign installation entry, leaving untouched: {link}")
            else:
                planned.append(("link", link, source, None))
    # Inspect every destination before mutating any; recheck each entry just
    # before use. Unexpected concurrent changes still cannot be made atomic.
    for target, identity in target_identities.values():
        if _identity(target) != identity:
            raise ValueError(f"destination changed during preflight: {target}")
    for _, link, _, identity in planned:
        if _identity(link) != identity:
            raise ValueError(f"installation entry changed during preflight: {link}")
    # Publish/retarget requested packages before retiring obsolete names. If
    # adding a new skill fails, legacy entry points remain available.
    planned.sort(key=lambda entry: entry[0] == "retire")
    actions = []
    completed_changes = []
    for operation, link, source, identity in planned:
        try:
            target_identity = next(identity for target, identity in target_identities.values()
                                   if target == link.parent)
            if _identity(link.parent) != target_identity:
                raise ValueError(f"destination changed during installation: {link.parent}")
            if _identity(link) != identity:
                raise ValueError(f"installation entry changed during preflight: {link}")
            if operation == "already":
                actions.append(f"already-linked {link}")
                continue
            status = {"retire": "retired", "retarget": "retargeted", "link": "linked"}
            label = f"{'would-' + operation if dry_run else status[operation]} {link}"
            if dry_run:
                actions.append(label)
                continue
            if operation == "retire":
                link.unlink()
            elif operation == "retarget":
                _retarget_owned_link(link, source, identity)
            elif operation == "link":
                try:
                    link.symlink_to(source, target_is_directory=True)
                except OSError as exc:
                    raise ValueError(
                        f"could not create skill directory symlink {link}: {exc}; "
                        "confirm link privileges on this platform"
                    ) from exc
            # Count an operation only after it actually returned successfully.
            actions.append(label)
            completed_changes.append(label)
        except (OSError, ValueError) as exc:
            if not dry_run and isinstance(exc, CommittedRetargetCleanupError):
                # The replace already committed. Include this entry in the
                # actual mutation list instead of under-reporting progress.
                completed_changes.append(label)
            if not dry_run and completed_changes:
                raise PartialInstallationError(completed_changes, link, exc) from exc
            raise
    return actions
