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
    actions = []
    for target in targets:
        target = Path(target).expanduser()
        if target.is_symlink() or not target.is_dir():
            raise ValueError(f"destination must already be a real directory: {target}")
        for item in sorted(target.iterdir()):
            if (item.name in desired or not item.name.startswith("astrid-dev-")
                    and item.name not in ("astrid-dev", "shared")):
                continue
            if _owned_link(item, root):
                actions.append(f"{'would-retire' if dry_run else 'retired'} {item}")
                if not dry_run:
                    item.unlink()
        for name, source in sorted(desired.items()):
            link = target / name
            if link.is_symlink():
                if _target_of(link) == source.resolve():
                    actions.append(f"already-linked {link}")
                    continue
                if not _owned_link(link, root):
                    raise ValueError(f"foreign symlink, leaving untouched: {link}")
                actions.append(f"{'would-retarget' if dry_run else 'retargeted'} {link}")
                if not dry_run:
                    link.unlink()
                    link.symlink_to(source, target_is_directory=True)
            elif link.exists():
                raise ValueError(f"foreign installation entry, leaving untouched: {link}")
            else:
                actions.append(f"{'would-link' if dry_run else 'linked'} {link}")
                if not dry_run:
                    try:
                        link.symlink_to(source, target_is_directory=True)
                    except OSError as exc:
                        raise ValueError(
                            f"could not create skill directory symlink {link}: {exc}; "
                            "confirm link privileges on this platform"
                        ) from exc
    return actions
