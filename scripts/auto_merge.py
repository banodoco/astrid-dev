"""Decide planning auto-merge eligibility from API JSON; no network access."""

import argparse
import json
from pathlib import Path
import re

from records import key_value_lines


RELEASE_BRIEF = re.compile(r"^releases/[1-9]\d*\.md$")
# records.key_value_lines splits with str.splitlines(), which also breaks on these
# characters. A patch line containing one could be read as several lines, so refuse it.
UNUSUAL_LINE_BREAKS = frozenset("\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029")


def eligibility_reason(draft, author_association, labels, body, changed_paths, file_entries=None):
    """Return None if eligible, otherwise a reason. Paths include rename sources."""
    if draft:
        return "draft pull request"
    if author_association not in {"OWNER", "MEMBER", "COLLABORATOR"}:
        return "author is not an owner, member or collaborator"
    if "hold" in labels:
        return "hold label"
    if "Owner decision needed" in (body or ""):
        return "Owner decision needed in body"
    if not changed_paths:
        return "empty file list"
    for path in changed_paths:
        # Reject ambiguous spelling before matching, rather than normalizing a
        # traversal into an allowed directory. Git paths and this allowlist are
        # case-sensitive; only canonical repository-relative paths qualify.
        if (not isinstance(path, str) or "\\" in path
                or any(part in {"", ".", ".."} for part in path.split("/"))):
            return "non-canonical changed path"
        if path in {"strategy.md", "README.md"}:
            continue
        if "/" not in path or path.split("/", 1)[0] not in {"plans", "releases", "vision", "docs"}:
            return "changed path outside planning content"

    release_paths = {path for path in changed_paths if RELEASE_BRIEF.fullmatch(path)}
    covered_release_paths = set()
    for file in file_entries or []:
        paths = [file.get("filename"), file.get("previous_filename")]
        matching = {path for path in paths if isinstance(path, str) and RELEASE_BRIEF.fullmatch(path)}
        if not matching:
            continue
        covered_release_paths.update(matching)
        patch = file.get("patch")
        if not isinstance(patch, str) or not patch:
            return "release brief patch unavailable"
        # Split on "\n" only, as git writes patches. Hunks have no file headers,
        # so every "+" or "-" line is content, including ones starting "+++" or "---".
        for line in patch.split("\n"):
            if UNUSUAL_LINE_BREAKS.intersection(line):
                return "release brief patch has an unusual line break"
            if not line.startswith(("+", "-")):
                continue
            fields = key_value_lines(line[1:].lstrip(" \t"), style="bold")
            if fields:
                key, separator, _ = fields[0]
                if separator and key in {"Kind", "State"}:
                    return f"release brief changes **{key}:**"
        # A rename shows only the lines that differ, so a brief moved into or out of
        # releases/<N>.md can carry a Kind or State line the patch never mentions.
        if file.get("previous_filename") or file.get("status") == "renamed":
            return "release brief renamed"
    if release_paths - covered_release_paths:
        return "release brief patch unavailable"
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr", required=True, type=Path)
    parser.add_argument("--files", required=True, type=Path)
    args = parser.parse_args()
    pr = json.loads(args.pr.read_text(encoding="utf-8"))
    pages = json.loads(args.files.read_text(encoding="utf-8"))
    files = [file for page in pages for file in page]
    # The files API caps responses at 3,000 files. Fail closed on truncation or
    # a changing snapshot, even when all returned paths look eligible.
    if len(files) != pr["changed_files"] or len({file["filename"] for file in files}) != len(files):
        print("incomplete file list")
        return
    paths = []
    for file in files:
        paths.append(file["filename"])
        if file.get("status") == "renamed" and not file.get("previous_filename"):
            print("missing rename source")
            return
        if "previous_filename" in file:
            paths.append(file["previous_filename"])
    reason = eligibility_reason(pr["draft"], pr["author_association"],
                                [label["name"] for label in pr["labels"]],
                                pr["body"], paths, file_entries=files)
    print(reason or "eligible")


if __name__ == "__main__":
    main()
