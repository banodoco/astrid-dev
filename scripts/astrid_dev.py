#!/usr/bin/env python3
"""List or run Astrid repository checks, generate views and build agent skills."""
import argparse
from pathlib import Path

import checks

ROOT = Path(__file__).resolve().parent.parent


def main(argv=None, *, root=ROOT, registry=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List each check's id, trigger and description")
    commands.add_parser("sync", help="Legacy spelling: regenerate declared Markdown views")
    views_command = commands.add_parser("views", help="Generated Markdown views")
    views_subcommands = views_command.add_subparsers(dest="views_action", required=True)
    views_subcommands.add_parser("generate", help="Regenerate declared Markdown views")

    skills_command = commands.add_parser("skills", help="Build/check/install generated agent skills")
    skills_subcommands = skills_command.add_subparsers(dest="skills_action", required=True)
    skills_subcommands.add_parser("build", help="Generate standard skills from opted-in Markdown")
    skills_subcommands.add_parser("check", help="Validate generated skill package identity and bytes")
    install = skills_subcommands.add_parser("install", help="Build and link owned skill packages")
    install.add_argument("--dry-run", action="store_true",
                         help="Display intended link changes; require existing build")
    install.add_argument("--destination", type=Path, action="append",
                         help="Already existing skills directory; repeat to install into several")

    release_command = commands.add_parser("release", help="Release coordination tools")
    release_subcommands = release_command.add_subparsers(dest="release_action", required=True)
    status = release_subcommands.add_parser("status", help="Reconcile included plan records")
    status.add_argument("number", type=int)
    mode = status.add_mutually_exclusive_group()
    mode.add_argument("--refresh", action="store_true", help="Refresh the draft release's recorded plan status")
    mode.add_argument("--check", action="store_true", help="Check the draft snapshot is current")
    check = commands.add_parser("check", help="Run applicable checks")
    check.add_argument("--base")
    body = check.add_mutually_exclusive_group()
    body.add_argument("--event", type=Path)
    body.add_argument("--body-file", type=Path)
    args = parser.parse_args(argv)
    entries = checks.REGISTRY if registry is None else registry
    if args.command == "release":
        from release_status import run
        try:
            return run(Path(root), args.number, refresh=args.refresh, check=args.check)
        except (ValueError, OSError) as exc:
            print(f"ERROR release status: {exc}")
            return 1
    if args.command in ("sync", "views"):
        import views
        try:
            changed = views.sync(Path(root))
        except (ValueError, OSError) as exc:
            print(f"ERROR {'sync' if args.command == 'sync' else 'views generate'}: {exc}")
            return 1
        for target in changed:
            print(f"Updated {target}")
        if not changed:
            print("Views are current")
        return 0
    if args.command == "skills":
        from skill_builder import build_packages, check_packages
        try:
            if args.skills_action == "build":
                changed = build_packages(Path(root))
                for item in changed:
                    print(item)
                if not changed:
                    print("Skill packages are current")
                return 0
            if args.skills_action == "check":
                problems = check_packages(Path(root))
                for item in problems:
                    print(f"ERROR skills check: {item}")
                if not problems:
                    print("Skill packages match their Markdown sources")
                return int(bool(problems))
            from skill_installer import install_packages
            if args.dry_run:
                problems = check_packages(Path(root))
                if problems:
                    raise ValueError("build skills first for a dry run: " + "; ".join(problems))
            else:
                built = build_packages(Path(root))
                for item in built:
                    print(item)
            linked = install_packages(Path(root), args.destination, dry_run=args.dry_run)
            for item in linked:
                print(item)
            if not linked:
                print("No skill links changed")
            return 0
        except (ValueError, OSError, UnicodeError) as exc:
            print(f"ERROR skills {args.skills_action}: {exc}")
            return 1
    if args.command == "list":
        for entry in entries:
            print(f"{entry.id} {entry.trigger} {entry.description}")
        return 0
    if bool(args.base) != bool(args.event or args.body_file):
        parser.error("--base and one of --event or --body-file must be supplied together")
    context = checks.Context(Path(root), args.base, args.event, args.body_file)
    failed = False
    for entry in entries:
        if entry.trigger == "always" or args.base:
            for message in entry.run(context):
                print(f"ERROR {entry.id}: {message}")
                failed = True
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
