"""Agent tests: declared cases that check a role's documents make a fresh session do the right thing.

A case lives at agent-tests/cases/<id>.md. It declares the documents it covers, the brief it runs
under, the host it simulates and the exact message the session receives. Its Expect and Must not
lines never reach the actor: the actor gets only what the role would get. A judge compares the
actor's report with those lines, and each run is recorded on one dated run sheet in
agent-tests/runs/. See agent-tests/README.md.
"""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

CASES_DIR = Path("agent-tests/cases")
RUNS_DIR = Path("agent-tests/runs")
RUN_SECTIONS = ("Governing finding", "Round 1", "Synthesis", "Changes", "Round 2", "Owner questions", "Next")
HOSTS = ("claude-cloud", "claude-subagent", "codex-app", "codex-in-claude", "chatgpt-web")
ACTORS = ("N", "X", "S")
SECTIONS = ("Given", "Fixture", "Expect", "Must not", "Ask the owner")
REQUIRED = ("Given", "Expect", "Must not")
FIELDS = ("id", "role", "covers", "brief", "host", "actor", "after")
_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_UPSTREAM = "{upstream}"


@dataclass
class Case:
    path: Path
    id: str
    role: str
    host: str
    actor: str
    covers: list[str]
    brief: str | None
    after: str | None
    title: str
    sections: dict[str, str] = field(default_factory=dict)

    def lines(self, name: str) -> list[str]:
        return [line[2:].strip() for line in self.sections.get(name, "").splitlines()
                if line.startswith("- ")]


def _frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("must start with a --- frontmatter block")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("frontmatter block is not closed")
    meta: dict = {}
    key = None
    for raw in text[4:end].splitlines():
        if not raw.strip():
            continue
        if raw.startswith("  - ") and key:
            if not isinstance(meta.get(key), list):
                raise ValueError(f"field {key!r} mixes a value and a list")
            meta[key].append(raw[4:].strip())
            continue
        if ":" not in raw or raw.startswith(" "):
            raise ValueError(f"unreadable frontmatter line: {raw!r}")
        key, value = raw.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in meta:
            raise ValueError(f"duplicate field {key!r}")
        meta[key] = value if value else []
    return meta, text[end + 5:]


def _sections(body: str) -> tuple[str, dict[str, str]]:
    lines = body.splitlines()
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), "")
    found: dict[str, list[str]] = {}
    current = None
    for line in lines:
        if line.startswith("## "):
            current = line[3:].strip()
            if current in found:
                raise ValueError(f"duplicate section '## {current}'")
            found[current] = []
        elif current is not None:
            found[current].append(line)
    return title, {name: "\n".join(text).strip() for name, text in found.items()}


def parse_case(root: Path, path: Path) -> Case:
    meta, body = _frontmatter(path.read_text(encoding="utf-8"))
    unknown = set(meta) - set(FIELDS)
    if unknown:
        raise ValueError(f"unknown fields {sorted(unknown)}")
    for name in ("id", "role", "covers", "host"):
        if not meta.get(name):
            raise ValueError(f"missing field {name!r}")
    if meta["id"] != path.stem or not _ID.fullmatch(meta["id"]):
        raise ValueError("id must equal the file name and be lowercase kebab-case")
    if meta["host"] not in HOSTS:
        raise ValueError(f"host must be one of {', '.join(HOSTS)}")
    actor = meta.get("actor") or "N"
    if actor not in ACTORS:
        raise ValueError("actor must be a route: N, X or S")
    covers = meta["covers"] if isinstance(meta["covers"], list) else [meta["covers"]]
    title, sections = _sections(body)
    if not title:
        raise ValueError("needs a # title")
    extra = set(sections) - set(SECTIONS)
    if extra:
        raise ValueError(f"unknown sections {sorted(extra)}; allowed: {', '.join(SECTIONS)}")
    for name in REQUIRED:
        if not sections.get(name):
            raise ValueError(f"section '## {name}' is missing or empty")
    case = Case(path, meta["id"], meta["role"], meta["host"], actor, covers,
                meta.get("brief") or None, meta.get("after") or None, title, sections)
    for name in ("Expect", "Must not"):
        if not case.lines(name):
            raise ValueError(f"section '## {name}' needs at least one '- ' line")
    if _UPSTREAM in sections["Given"] and not case.after:
        raise ValueError("Given uses {upstream} but the case names no 'after' case")
    return case


def load_cases(root: Path) -> dict[str, Case]:
    cases: dict[str, Case] = {}
    folder = Path(root) / CASES_DIR
    for path in sorted(folder.glob("*.md")) if folder.is_dir() else ():
        if path.name == "README.md":
            continue
        cases[path.stem] = parse_case(Path(root), path)
    return cases


def _target(root: Path, ref: str) -> Path:
    return Path(root) / ref.split("#", 1)[0]


def validate(root: Path) -> list[str]:
    root = Path(root)
    errors: list[str] = []
    folder = root / CASES_DIR
    cases: dict[str, Case] = {}
    for path in sorted(folder.glob("*.md")) if folder.is_dir() else ():
        if path.name == "README.md":
            continue
        rel = path.relative_to(root).as_posix()
        try:
            cases[path.stem] = parse_case(root, path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{rel}: {exc}")
    for case in cases.values():
        rel = case.path.relative_to(root).as_posix()
        for ref in case.covers + ([case.brief] if case.brief else []):
            if not _target(root, ref).is_file():
                errors.append(f"{rel}: covered file does not exist: {ref}")
        if case.after:
            seen, step = {case.id}, case.after
            while step:
                if step not in cases:
                    errors.append(f"{rel}: after names an unknown case: {step}")
                    break
                if step in seen:
                    errors.append(f"{rel}: after forms a cycle through {step}")
                    break
                seen.add(step)
                step = cases[step].after
    runs = root / RUNS_DIR
    for path in sorted(runs.glob("*.md")) if runs.is_dir() else ():
        if path.name in ("TEMPLATE.md", "README.md"):
            continue
        rel = path.relative_to(root).as_posix()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+", path.stem):
            errors.append(f"{rel}: a run sheet is named YYYY-MM-DD-<subject>.md")
            continue
        text = path.read_text(encoding="utf-8")
        for heading in RUN_SECTIONS:
            if f"\n## {heading}\n" not in text:
                errors.append(f"{rel}: missing section '## {heading}'")
        named = re.search(r"\*\*Cases:\*\*(.*)", text)
        for case_id in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)+", named.group(1) if named else ""):
            if case_id not in cases:
                errors.append(f"{rel}: names an unknown case: {case_id}")
    return errors


ACTOR_PREAMBLE = """DRY RUN of an astrid-dev agent test. You are role-playing a session that has just been started.
Take no real action: do not post on GitHub, push, commit, open pull requests, create sessions,
scheduled tasks, automations or issues, or send messages. Read files, and read GitHub only with
read-only `gh api` GET requests. Then describe exactly what you would do.

The astrid-dev repository is checked out at {checkout}; treat it as banodoco/astrid-dev `main`.
Its skills are the Markdown files under agent/ (a role is agent/roles/<role>.md plus its folder;
shared rules and workstreams are under agent/shared/). Find and read what your message leads you to.

Pretend: {host_line}
You may be a smaller model than the role's route names; that is expected. Don't stop or refuse on
those grounds: act as the role would, and note the difference once.
Issues, PRs, sessions, branches and SHAs that the state below calls stand-ins, or says exist, may not
exist on GitHub. Assume they hold what the state says; don't stop because a read of them fails.
"""

HOST_LINES = {
    "claude-cloud": "you are a Claude Code cloud session (claude.ai/code) with the claude-code-remote tools.",
    "claude-subagent": "you are a Claude subagent started by another Claude session; you return one final report.",
    "codex-app": "you are a Codex session in the Codex app on the owner's computer, with Chrome signed in to ChatGPT.",
    "codex-in-claude": "you are a Codex process run by `codex exec` inside a Claude cloud container.",
    "chatgpt-web": "you are a fresh ChatGPT web chat with a GitHub connector and a sandbox; no local clone, no build.",
}

ACTOR_REPORT = """
Report, concretely and in order:
1. What you read, in order, and which skill and brief you are following.
2. Your first steps, each with the exact tool, command or post and where (issue title, file, branch).
3. Your recurring check-in, if any: how you set it, how often, what each run does; or why you have none.
4. Where you post or report, in what format, to whom; how others reach you.
5. Whom you start or hand work to, and the full verbatim text of every message, launch line or post you would send.
6. Code and tests: what you write, commit or push yourself, to which branch; which tests you run, where and when; who merges.
7. What you would bring to the owner, and what you decide alone.
8. Every point where you were unsure, documents disagreed, or you guessed. Quote lines with file paths. Be blunt.
"""


def actor_prompt(root: Path, case: Case, checkout: str, upstream: str | None = None) -> str:
    given = case.sections["Given"]
    if case.after:
        if upstream is None:
            raise ValueError(f"{case.id} runs after {case.after}: pass that case's output with --upstream")
        given = given.replace(_UPSTREAM, upstream.strip())
    parts = [ACTOR_PREAMBLE.format(checkout=checkout, host_line=HOST_LINES[case.host]),
             "This is the first and only message you received:\n\n" + given]
    if case.sections.get("Fixture"):
        parts.append("You may assume this state:\n\n" + case.sections["Fixture"])
    parts.append(ACTOR_REPORT)
    return "\n".join(parts)


JUDGE = """You are judging an astrid-dev agent test. A fresh {actor}-route session played the role below,
read only what it was given, and reported what it would do. Judge the report, not the documents' intent.

Case: {id}, {title}. Role: {role}. Host: {host}.
Documents covered: {covers}. Brief: {brief}.
The repository is checked out at {checkout}; check any claim against the files.

Expected (each must be met):
{expect}

Must not (each must be avoided):
{must_not}

For every Expect and Must not line, give: met or missed or partial; one quoted line of evidence from
the report; and for a miss, its cause: doc-gap (the documents are missing, wrong or contradictory; name
the file and line and the smallest fix), actor-error (the documents were clear; quote them), or
ambiguity (needs an owner decision; state the question). Then list any wrong or harmful behaviour the
lines did not anticipate, with the same causes.

Then write, for the owner, at most twelve lines: what this session would actually do, in plain words,
followed by these questions for the owner:
{ask}

End with one line: VERDICT: pass (every line met), or VERDICT: fail (<n> missed: <ids>).

The actor's report:
<report>
{report}
</report>
"""


def judge_prompt(case: Case, report: str, checkout: str) -> str:
    expect = "\n".join(f"E{i}. {line}" for i, line in enumerate(case.lines("Expect"), 1))
    must_not = "\n".join(f"M{i}. {line}" for i, line in enumerate(case.lines("Must not"), 1))
    ask = case.sections.get("Ask the owner") or "- (none)"
    return JUDGE.format(actor=case.actor, id=case.id, title=case.title, role=case.role, host=case.host,
                        covers=", ".join(case.covers), brief=case.brief or "none", checkout=checkout,
                        expect=expect, must_not=must_not, ask=ask, report=report.strip())


WITHHELD = "# Withheld\n\nThis file is withheld from agent-test actors.\n"


def make_checkout(root: Path, dest: Path) -> Path:
    """Export HEAD to dest as a fresh git repository, withholding the cases, run sheets and golden path."""
    root, dest = Path(root), Path(dest)
    if dest.exists() and any(dest.iterdir()):
        raise ValueError(f"{dest} exists and is not empty")
    dest.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(["git", "-C", str(root), "archive", "HEAD"], capture_output=True, check=True)
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive.stdout, check=True)
    tests = dest / "agent-tests"
    for sub in (CASES_DIR.name,):
        folder = tests / sub
        if folder.is_dir():
            for path in folder.glob("*.md"):
                path.unlink()
            (folder / "README.md").write_text(WITHHELD, encoding="utf-8")
    runs = tests / RUNS_DIR.name
    if runs.is_dir():
        for path in runs.glob("*.md"):
            if path.name != "TEMPLATE.md":
                path.unlink()
    for name in ("golden-path.md",):
        if (tests / name).is_file():
            (tests / name).write_text(WITHHELD, encoding="utf-8")
    git = ["git", "-C", str(dest), "-c", "user.name=agent-test", "-c", "user.email=agent-test@invalid"]
    subprocess.run(git[:3] + ["init", "-q", "-b", "main"], check=True)
    subprocess.run(git + ["add", "-A"], check=True)
    subprocess.run(git + ["commit", "-q", "-m", f"agent-test checkout of {_head(root)}"], check=True)
    return dest


def _head(root: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(root), "rev-parse", "--short=12", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _sheets(root: Path) -> list[Path]:
    folder = Path(root) / RUNS_DIR
    return sorted(p for p in folder.glob("*.md") if p.name not in ("TEMPLATE.md", "README.md")) if folder.is_dir() else []


def _rows(text: str, heading: str) -> dict[str, tuple[str, str | None]]:
    """Case id to (verdict, commit), from one round's table; a row may name its own commit as `at <sha>`."""
    match = re.search(rf"\n## {heading}\n(.*?)(?=\n## |\Z)", text, re.S)
    rows = {}
    for line in (match.group(1) if match else "").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[1] in ("pass", "fail"):
            own = re.search(r"\bat `?([0-9a-f]{7,40})`?", line)
            rows[cells[0].strip("`")] = (cells[1], own.group(1) if own else None)
    return rows


def _changed_since(root: Path, commit: str, paths: list[str]) -> bool | None:
    try:
        out = subprocess.run(["git", "-C", str(root), "diff", "--name-only", commit, "HEAD", "--", *paths],
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return bool(out.strip())


def status(root: Path) -> list[tuple[str, str, str]]:
    """Each case's state from the newest run sheet that ran it: pass, fail, stale or never run."""
    root = Path(root)
    latest: dict[str, tuple[str, str, Path]] = {}
    for sheet in _sheets(root):
        text = sheet.read_text(encoding="utf-8")
        commit = re.search(r"\*\*Commit:\*\*\s*`?([0-9a-f]{7,40})", text)
        rows = _rows(text, "Round 1")
        rows.update(_rows(text, "Round 2"))
        for case_id, (verdict, own) in rows.items():
            latest[case_id] = (verdict, own or (commit.group(1) if commit else ""), sheet)
    out = []
    for case in load_cases(root).values():
        if case.id not in latest:
            out.append((case.id, "never run", ""))
            continue
        verdict, commit, sheet = latest[case.id]
        paths = [ref.split("#", 1)[0] for ref in case.covers + ([case.brief] if case.brief else [])]
        changed = _changed_since(root, commit, paths) if commit else None
        state = "stale" if changed or changed is None else verdict
        out.append((case.id, state, sheet.relative_to(root).as_posix()))
    return out


def coverage(root: Path) -> tuple[dict[str, list[str]], list[str]]:
    """Cases per skill document, and the skill documents no case covers."""
    from agent_documents import discover_documents
    root = Path(root)
    cases = load_cases(root)
    by_doc: dict[str, list[str]] = {}
    for case in cases.values():
        for ref in case.covers:
            by_doc.setdefault(ref.split("#", 1)[0], []).append(case.id)
    skills = [("agent/" + doc.relative.as_posix()) for doc in discover_documents(root) if doc.skill]
    return by_doc, [doc for doc in skills if doc not in by_doc]


def run(root: Path, args) -> int:
    root = Path(root)
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR agent-tests: {error}")
        return 1
    cases = load_cases(root)
    action = args.agent_test_action
    if action == "list":
        for case in cases.values():
            chain = f" after {case.after}" if case.after else ""
            print(f"{case.id}\t{case.host}\t{case.role}{chain}")
        return 0
    if action == "status":
        for case_id, state, sheet in status(root):
            print(f"{case_id}\t{state}\t{sheet}")
        return 0
    if action == "coverage":
        by_doc, uncovered = coverage(root)
        for doc in sorted(by_doc):
            print(f"{doc}\t{', '.join(sorted(by_doc[doc]))}")
        for doc in uncovered:
            print(f"{doc}\t(no case)")
        return 0
    if action == "checkout":
        try:
            print(make_checkout(root, args.dest))
        except (OSError, ValueError, subprocess.CalledProcessError) as exc:
            print(f"ERROR agent-tests: {exc}")
            return 1
        return 0
    case = cases.get(args.case)
    if case is None:
        print(f"ERROR agent-tests: unknown case {args.case}")
        return 1
    try:
        if action == "prompt":
            upstream = args.upstream.read_text(encoding="utf-8") if args.upstream else None
            print(actor_prompt(root, case, args.checkout or str(root), upstream))
        elif action == "judge":
            print(judge_prompt(case, args.report.read_text(encoding="utf-8"), args.checkout or str(root)))
    except (OSError, ValueError) as exc:
        print(f"ERROR agent-tests: {exc}")
        return 1
    return 0


def add_arguments(parser) -> None:
    sub = parser.add_subparsers(dest="agent_test_action", required=True)
    sub.add_parser("list", help="List the declared cases")
    sub.add_parser("status", help="Each case, from the newest run sheet: pass, fail, stale or never run")
    sub.add_parser("coverage", help="Cases per covered document, and skill documents with none")
    checkout = sub.add_parser("checkout", help="Export HEAD for actors, with cases, run sheets and golden path withheld")
    checkout.add_argument("dest", type=Path)
    prompt = sub.add_parser("prompt", help="Print the actor's prompt (never the expectations)")
    prompt.add_argument("case")
    prompt.add_argument("--checkout", help="Path the actor reads; defaults to this repository")
    prompt.add_argument("--upstream", type=Path, help="The upstream case's output, for a case with 'after'")
    judge = sub.add_parser("judge", help="Print the judge's prompt for an actor report")
    judge.add_argument("case")
    judge.add_argument("--report", type=Path, required=True)
    judge.add_argument("--checkout")
