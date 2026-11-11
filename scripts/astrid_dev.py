#!/usr/bin/env python3
"""List or run Astrid repository checks."""
import argparse
from pathlib import Path

import checks

ROOT = Path(__file__).resolve().parent.parent


def main(argv=None, *, root=ROOT, registry=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List checks and their triggers")
    commands.add_parser("sync", help="Regenerate every declared view")
    check = commands.add_parser("check", help="Run applicable checks")
    check.add_argument("--base")
    body = check.add_mutually_exclusive_group()
    body.add_argument("--event", type=Path)
    body.add_argument("--body-file", type=Path)
    args = parser.parse_args(argv)
    entries = checks.REGISTRY if registry is None else registry
    if args.command == "sync":
        import views
        changed = views.sync(Path(root))
        for target in changed:
            print(f"Updated {target}")
        if not changed:
            print("Views are current")
        return 0
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
