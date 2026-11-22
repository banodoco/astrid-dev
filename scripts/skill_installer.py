"""Install only owned generated Astrid Dev skill packages into agent skill roots."""
from __future__ import annotations

import os
from pathlib import Path

from skill_builder import OUTPUT, check_packages


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
            if (item.name in desired or not item.name.startswith("astrid-dev-")
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
    actions = []
    for operation, link, source, identity in planned:
        target_identity = next(identity for target, identity in target_identities.values()
                               if target == link.parent)
        if _identity(link.parent) != target_identity:
            raise ValueError(f"destination changed during installation: {link.parent}")
        if _identity(link) != identity:
            raise ValueError(f"installation entry changed during preflight: {link}")
        if operation == "already":
            actions.append(f"already-linked {link}")
            continue
        actions.append(f"{'would-' + operation if dry_run else {'retire': 'retired', 'retarget': 'retargeted', 'link': 'linked'}[operation]} {link}")
        if dry_run:
            continue
        if operation in ("retire", "retarget"):
            link.unlink()
        if operation in ("link", "retarget"):
            try:
                link.symlink_to(source, target_is_directory=True)
            except OSError as exc:
                raise ValueError(
                    f"could not create skill directory symlink {link}: {exc}; "
                    "confirm link privileges on this platform"
                ) from exc
    return actions
