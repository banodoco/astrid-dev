"""Read-only inventory of tracked references to the pre-migration Astrid skill layout.

The output is a review queue, *not* a rewrite script or cutover authorization.
Run from a checkout: python3 scripts/agent_reference_inventory.py --format markdown
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess

SELF_PATHS = frozenset({"scripts/agent_reference_inventory.py", "scripts/test_agent_reference_inventory.py",
                        "scripts/ms9_cutover_preflight.py", "scripts/test_ms9_cutover_preflight.py"})
TEXT_SUFFIXES = frozenset({".md", ".py", ".sh", ".yml", ".yaml", ".json", ".toml", ".txt", ".ini"})
OLD_REFERENCE = re.compile(
    r"(?P<path>skills/(?:astrid-dev(?:/[A-Za-z0-9_./-]+)?(?![A-Za-z0-9_-])|"
    r"roles/astrid-dev-[A-Za-z0-9_./-]+|shared/[A-Za-z0-9_./-]+|"
    r"capabilities/[A-Za-z0-9_./-]+))"
    r"|(?P<command>\bsync\.sh\b|\bscripts/astrid_dev\.py\s+sync\b)"
    r"|(?P<skill>\bastrid-dev-(?:lead|manage|orchestrate)\b)"
)
ROLE_NAMES = {"lead": "leader", "manage": "manager", "orchestrate": "orchestrator"}
ROLE_PATHS = {"lead": "leader", "manage": "manager", "orchestrate": "orchestrator", "worker": "worker"}
SHARED_NAMES = frozenset({"bugfix", "gap", "gpu-validate", "green", "improve", "iterate", "merge", "plan", "release"})


def tracked_paths(root: Path) -> list[str]:
    """Only tracked paths; never follow filesystem aliases or inspect untracked run state."""
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=root)
    return sorted(path.decode("utf-8") for path in raw.split(b"\0") if path)


def scope_for(path: str) -> str:
    if path.startswith(("docs/handoffs/", "docs/ledger/", "docs/proposals/", "releases/")) and (
        path.startswith(("docs/handoffs/", "docs/ledger/", "docs/proposals/"))
        or "/evidence/" in path
    ):
        return "historical-evidence"
    if path.startswith("plans/") and ("/evidence/" in path or "/handoffs/" in path or path.endswith("/handoff.md")):
        return "historical-evidence"
    if path.startswith("skills/"):
        return "current-authority"
    if path.startswith("agent/"):
        return "staged-agent"
    if path.startswith("plans/"):
        return "plan-owner-review"
    if path.startswith("releases/"):
        return "release-lead-review"
    # Disposable migration proof is test/evidence code, never a live consumer.
    if path in {"scripts/ms9_compat_rollback.py", "scripts/ms10_extension_exercise.py",
                "scripts/ms11_negative_matrix.py"}:
        return "pinned-test-or-fixture"
    if path.startswith(("scripts/test_", "scripts/fixtures/", "env/tests/")):
        return "pinned-test-or-fixture"
    if path.startswith(("scripts/", ".github/", "env/", "templates/", "docs/", "vision/")) or path in (
        "README.md", "CONTRIBUTING.md", "strategy.md", "sync.sh"
    ):
        return "active-consumer"
    return "other-review"


def mapped_target(match: str, kind: str) -> str | None:
    """Return only a *known* candidate target; unresolved references stay explicit."""
    if kind == "skill":
        return "astrid-dev-" + ROLE_NAMES[match.removeprefix("astrid-dev-")]
    if kind != "path":
        return None  # sync.sh and the sync subcommand have different purposes
    path = match.rstrip(".,;:")
    fixed = {
        "skills/astrid-dev/SKILL.md": "agent/start.md",
        "skills/astrid-dev/references/domains.md": "agent/shared/domains.md",
        "skills/shared/run-contract.md": "agent/shared/run-contract.md",
        "skills/shared/glossary.md": "agent/shared/glossary.md",
        "skills/shared/templates/run.yaml": "agent/shared/templates/run.yaml",
        "skills/shared/templates/decisions-ledger.md": "agent/shared/templates/decisions-ledger.md",
        "skills/shared/workstreams/astrid-dev-release/references/sources.md": "agent/shared/release-sources.md",
        "skills/roles/astrid-dev-plan": "agent/shared/workstreams/plan.md",
    }
    if path in fixed:
        return fixed[path]
    role = re.fullmatch(r"skills/roles/astrid-dev-(lead|manage|orchestrate|worker)/SKILL\.md", path)
    if role:
        return f"agent/roles/{ROLE_PATHS[role[1]]}.md"
    role_workstream = re.fullmatch(
        r"skills/roles/astrid-dev-(lead|manage|orchestrate)/workstreams/([a-z0-9-]+\.md)", path
    )
    if role_workstream:
        return f"agent/roles/{ROLE_PATHS[role_workstream[1]]}/{role_workstream[2]}"
    cloud = re.fullmatch(
        r"skills/roles/astrid-dev-orchestrate/workstreams/(codex-cloud|codex-in-claude-cloud)/([A-Za-z0-9_.-]+)",
        path,
    )
    if cloud:
        return f"agent/guides/{cloud[1]}/{cloud[2]}"
    stream = re.fullmatch(r"skills/(?:shared/workstreams|capabilities)/astrid-dev-([a-z0-9-]+)(?:/SKILL\.md)?", path)
    if stream and stream[1] in SHARED_NAMES:
        return f"agent/shared/workstreams/{stream[1]}.md"
    return None


def inventory(root: Path, paths: list[str] | None = None) -> list[dict[str, object]]:
    root = root.resolve()
    rows: list[dict[str, object]] = []
    for path in (tracked_paths(root) if paths is None else sorted(paths)):
        if path in SELF_PATHS:
            continue  # mapping-table and fixture strings are not runtime consumers
        candidate = root / path
        if candidate.is_symlink() or not candidate.is_file() or candidate.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            source = candidate.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            # A tracked file that cannot be inspected is not a clean inventory.
            raise ValueError(f"cannot read tracked text file {path}") from None
        scope = scope_for(path)
        for line_no, line in enumerate(source.splitlines(), 1):
            for hit in OLD_REFERENCE.finditer(line):
                kind = hit.lastgroup
                assert kind is not None
                token = hit.group().rstrip(".,;:")
                target = mapped_target(token, kind)
                if scope == "historical-evidence":
                    action = "preserve-history"
                elif scope == "current-authority":
                    action = "retain-until-MS9"
                elif scope in {"release-lead-review", "plan-owner-review", "pinned-test-or-fixture"}:
                    action = "owner-adjudicate"
                elif target:
                    action = "candidate-after-D5"
                else:
                    action = "manual-path-or-command-review"
                rows.append({
                    "file": path,
                    "line": line_no,
                    "kind": kind,
                    "scope": scope,
                    "reference": token,
                    "proposed_target": target,
                    "disposition": action,
                    "text": line.strip(),
                })
    return rows


def render_markdown(rows: list[dict[str, object]], source_sha: str) -> str:
    counts = Counter(str(row["scope"]) for row in rows)
    lines = [
        "# Plan 73 MS-7 — legacy-reference inventory (pre-cutover)",
        "",
        f"**Inspected checkout:** `{source_sha}`",
        "",
        "Generated from tracked text files. Each row is a literal match, not an approved migration,",
        "a live-runtime ownership decision, or authorization to rewrite historical evidence.",
        "The old `skills/` tree remains authoritative until D5 and MS-7–MS-9 cutover approval.",
        "",
        f"**Matches:** {len(rows)}. **No automatic rewrites.**",
        "",
        "| Scope | Matches |",
        "| --- | ---: |",
    ]
    lines += [f"| {key} | {value} |" for key, value in sorted(counts.items())]
    lines += [
        "",
        "**Interpretation:** `current-authority` is not a candidate for early removal;",
        "`historical-evidence` must remain truthful or be revision-pinned;",
        "`plan-owner-review` and `release-lead-review` need owner-specific D5 decisions;",
        "`pinned-test-or-fixture` requires explicit oracle protection. A proposed target is not a command to edit.",
        "",
        "| Source:line | Scope | Existing reference | Proposed target | Disposition |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        source = str(row["file"]).replace("|", "\\|")
        link = f"[`{source}:{row['line']}`](https://github.com/banodoco/astrid-dev/blob/{source_sha}/{source}#L{row['line']})"
        token = str(row["reference"]).replace("|", "\\|").replace("`", "\\`")
        target = str(row["proposed_target"] or "—").replace("|", "\\|")
        lines.append(f"| {link} | {row['scope']} | `{token}` | `{target}` | {row['disposition']} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path, help="Write report here; otherwise print to stdout")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    rows = inventory(root)
    if args.format == "json":
        report = json.dumps({"source_sha": sha, "matches": len(rows), "records": rows}, indent=2, ensure_ascii=False) + "\n"
    else:
        report = render_markdown(rows, sha)
    if args.output is not None:
        args.output.write_text(report, encoding="utf-8")
        print(f"Inventory {sha}: {len(rows)} matches -> {args.output}")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
