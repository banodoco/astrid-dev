"""Decide planning auto-merge eligibility from API JSON; no network access."""

import argparse
import json
from pathlib import Path


def eligibility_reason(draft, author_association, labels, body, changed_paths):
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
                                pr["body"], paths)
    print(reason or "eligible")


if __name__ == "__main__":
    main()
