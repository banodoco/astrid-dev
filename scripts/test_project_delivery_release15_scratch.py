"""Native disposable Release 15 source/record rehearsal (off-release only).

Build a detached temporary worktree at the pinned *frozen* release commit,
select only the preserved Plan 72 donor patches, apply the two stored recovery
patches, and add canonical authored Plan 72 records plus explicitly selected
branch rows. No remote mutations, release branch cuts, network, merges, test
suppression or modifications to the caller's checked-out source.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
RELEASE_BASE = "321523e52bddbbd13477634b05974a16b54b825b"
P72_SOURCE = "f13a584a31cb1d29b335533563420e1de35e3481"
ARTIFACT_DIR = Path("plans/72-composable-project-delivery/evidence/recovery-2026-11-23")

# Every selected historical diff is path-limited. The composed #1161 merge
# and unrelated default-main history are never cherry-picked or replayed.
DONORS = (
    ("01-core", "4b3e3841af3921d9846389a4cd744f027c1db0b3",
     "06c0ce64bb86e7524bb80208388c0d7147d8f511",
     ("scripts/relationships.py", "scripts/test_relationships.py")),
    ("02-reader", "06c0ce64bb86e7524bb80208388c0d7147d8f511",
     "2bef3d9b295008733ae672204ebf728c1a069ed5",
     ("scripts/project_contract.py", "scripts/project_delivery.py",
      "scripts/records.py", "scripts/test_check_docs.py",
      "scripts/test_project_contract.py", "scripts/test_project_delivery.py",
      "scripts/test_records.py")),
    ("03-negative", "16eaf64899f2dde82c7cb79ad92b88928afbd374",
     "65fe0478f84eaf777d328594f7c79c6e067f2238",
     ("scripts/test_project_delivery_critique_regressions.py",)),
    ("04-guards", "65fe0478f84eaf777d328594f7c79c6e067f2238",
     "997a72a5bd2ac85aea68dc8127055bf40a540edf",
     ("scripts/project_contract.py", "scripts/project_delivery.py",
      "scripts/records.py", "scripts/relationships.py")),
    ("05-role", "997a72a5bd2ac85aea68dc8127055bf40a540edf",
     P72_SOURCE,
     ("scripts/project_contract.py", "scripts/project_delivery.py",
      "scripts/test_project_source_ownership.py")),
)
RECORD_BLOBS = {
    "plans/72-composable-project-delivery/plan.md":
        "9066011c5547ce6ec62944f85a5847f2858409ac",
    "plans/72-composable-project-delivery/inputs.md":
        "5caae0ebc3dec1748251677b18c2ec1b38663d59",
    "plans/72-composable-project-delivery/tasks.md":
        "0ecdcca32053cd124f2bf07293e264e1a73ed6b1",
}
MAIN_RELEASE_BRIEF_BLOB = "e53f0fd53aea5d48b0387a9d7fb6c7cce0351bb1"
EXPECTED_SOURCE_BLOBS = {
    "scripts/project_delivery.py": "7f5a9659540984c05137d2f39e8e4e4a2ad25b5a",
    "scripts/test_project_delivery_root_identity.py": "d422377dcf2acf76668d286477eb2cc8b6614c84",
    "scripts/test_project_delivery_source_containment.py": "ab74166974ce35a15431ba3d55a9c34620ae3040",
    "scripts/test_project_delivery_source_directories.py": "e3ae8f85155c4d53c712a6dd0816fcbe8b89b3a7",
    "scripts/relationships.py": "6af4fa29092bab9bb9f2d0770f59123d61816950",
}
# Source rows are copied verbatim from the pinned main brief, NEVER invented.
CANONICAL_ROWS = (
    ("astrid-dev", "release/15/main", "release"),
    ("astrid-dev", "release/15/plan-39", "plan 39"),
    ("astrid-dev", "release/15/plan-50", "plan 50"),
    ("astrid-dev", "release/15/plan-72", "plan 72"),
    ("astrid-agent", "release/15/plan-40", "plan 40"),
)


def git(*args: str, cwd: Path = REPO, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(
        ("git", *args), cwd=cwd, input=input_bytes,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise AssertionError(
            f"git {' '.join(args)} failed ({result.returncode}) in {cwd}:\n"
            f"{result.stderr.decode('utf-8', errors='replace')[-2500:]}"
        )
    return result.stdout


def blob(sha: str) -> bytes:
    return git("cat-file", "blob", sha)


def current_hash(data: bytes) -> str:
    return git("hash-object", "--stdin", input_bytes=data).decode().strip()


def check_and_apply(worktree: Path, patch: bytes, label: str) -> None:
    if not patch.startswith(b"diff --git "):
        raise AssertionError(f"{label}: missing Git patch header")
    git("apply", "--check", "-", cwd=worktree, input_bytes=patch)
    git("apply", "-", cwd=worktree, input_bytes=patch)


def validate_main_source(blob_sha: str, label: str) -> str:
    data = blob(blob_sha)
    if current_hash(data) != blob_sha:
        raise AssertionError(f"incorrect pinned blob for {label}")
    return data.decode("utf-8")


class FrozenRelease15RehearsalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # GitHub's existing docs.yml checks out with fetch-depth: 0. Missing
        # local Git objects fail CLOSED; never fetch or fall back to main.
        git("cat-file", "-e", RELEASE_BASE + "^{commit}")
        for name, base, head, _ in DONORS:
            git("cat-file", "-e", base + "^{commit}")
            git("cat-file", "-e", head + "^{commit}")
        cls.temporary = tempfile.TemporaryDirectory(prefix="p72-r15-disposable-")
        cls.scratch = Path(cls.temporary.name) / "release15"
        cls.created_worktree = False
        try:
            git("worktree", "add", "--detach", str(cls.scratch), RELEASE_BASE)
            cls.created_worktree = True
            if git("rev-parse", "HEAD", cwd=cls.scratch).decode().strip() != RELEASE_BASE:
                raise AssertionError("wrong pinned frozen Release15 checkout")
            cls.frozen_release_brief = (
                cls.scratch / "releases/15.md"
            ).read_text(encoding="utf-8")

            for name, base, head, paths in DONORS:
                patch = git("diff", "--binary", base, head, "--", *paths)
                check_and_apply(cls.scratch, patch, name)
            for number, filename in (
                ("08", "08-source-boundaries.patch"),
                ("09", "09-release15-branch-parser-compat.patch"),
            ):
                patch = (REPO / ARTIFACT_DIR / filename).read_bytes()
                check_and_apply(cls.scratch, patch, number)

            for path, sha in RECORD_BLOBS.items():
                data = blob(sha)
                if current_hash(data) != sha:
                    raise AssertionError(f"{path}: unexpected canonical content")
                dest = cls.scratch / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)

            # Keep the original Release15 brief as the base and add only the
            # canonical Plan72 included-plan line and five canonical branch
            # rows. This is a disposable test composition, NOT release input.
            main_brief = validate_main_source(
                MAIN_RELEASE_BRIEF_BLOB, "canonical main releases/15.md"
            )
            plan72 = [
                line for line in main_brief.splitlines()
                if line.startswith("- [Plan 72](")
            ]
            if len(plan72) != 1:
                raise AssertionError("missing/ambiguous canonical Plan72 line")
            canonical = main_brief.splitlines()
            selected = []
            for repo, ref, role in CANONICAL_ROWS:
                matches = [
                    row for row in canonical
                    if row.startswith(f"| {repo} | `{ref}` | {role} |")
                ]
                # Backticks are literal Markdown in the source; do not escape
                # them in this Python f-string. A missing exact row is BLOCKED.
                if len(matches) != 1:
                    raise AssertionError(
                        f"expected exactly one canonical row: {repo} {ref} {role}"
                    )
                selected.append(matches[0])
            brief = cls.frozen_release_brief
            if brief.count("\n## Branches\n") != 1:
                raise AssertionError("frozen brief has no unique Branches section")
            brief = brief.replace(
                "\n## Branches\n",
                "\n" + plan72[0] + "\n\n## Branches\n",
                1,
            )
            if brief.count("\n## Issues\n") != 1:
                raise AssertionError("frozen brief has no unique Issues section")
            branch_section, after_issues = brief.split("\n## Issues\n", 1)
            branch_section = branch_section.rstrip("\n")
            # Keep all branch-table rows in one uninterrupted Markdown table.
            # A blank line would create a second table and must fail the test.
            if not branch_section.splitlines()[-1].startswith("|"):
                raise AssertionError("frozen release branch table has an unexpected tail")
            brief = (
                branch_section + "\n" + "\n".join(selected)
                + "\n\n## Issues\n" + after_issues
            )
            (cls.scratch / "releases/15.md").write_text(brief, encoding="utf-8")
            cls.composed_release_brief = brief
            print(
                "P72 SCRATCH: exact frozen Release15 source, 01-05 + 08 + 09 "
                "native git apply, three canonical authored records and "
                "five verbatim canonical branch rows"
            )
        except BaseException:
            cls.tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls) -> None:
        if getattr(cls, "created_worktree", False):
            git("worktree", "remove", "--force", str(cls.scratch))
            cls.created_worktree = False
        if hasattr(cls, "temporary"):
            cls.temporary.cleanup()

    def test_selected_source_files_are_expected_exact_blobs(self):
        for path, sha in EXPECTED_SOURCE_BLOBS.items():
            with self.subTest(path=path):
                self.assertEqual(current_hash((self.scratch / path).read_bytes()), sha)

    def test_canonical_plan72_authored_pack_is_verbatim(self):
        for path, sha in RECORD_BLOBS.items():
            with self.subTest(path=path):
                self.assertEqual(current_hash((self.scratch / path).read_bytes()), sha)

    @classmethod
    def _reader(cls, brief: str, *, check_role: bool = False) -> dict:
        # Run imports from the patched FROZEN checkout in a fresh interpreter,
        # never accidentally from the current off-release PR branch.
        script = """
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
from records import release_brief, release_branch_errors
from project_contract import plan_gap_links
body = sys.stdin.read()
info = release_brief(body)
errors = release_branch_errors(body, "15", tuple(p["number"] for p in info["plans"]))
role = plan_gap_links((root / "plans/72-composable-project-delivery/plan.md").read_text()) if sys.argv[2] == "1" else None
print(json.dumps({"errors": errors, "plans": [p["number"] for p in info["plans"]], "roles": role}))
"""
        result = subprocess.run(
            (sys.executable, "-c", script, str(cls.scratch), "1" if check_role else "0"),
            cwd=cls.scratch, input=brief, text=True, capture_output=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, check=False,
        )
        if result.returncode:
            raise AssertionError(
                f"rehearsed frozen parser failed ({result.returncode}): "
                f"{result.stderr[-2500:]}"
            )
        import json
        return json.loads(result.stdout)

    def test_frozen_brief_refuses_all_three_missing_original_plan_rows(self):
        parsed = self._reader(self.frozen_release_brief)
        self.assertEqual(parsed["plans"], ["39", "50", "40"])
        for num in ("39", "50", "40"):
            with self.subTest(plan=num):
                self.assertTrue(
                    any(f"Included plan {num} has no" in e for e in parsed["errors"]),
                    parsed["errors"],
                )

    def test_composed_brief_and_enabler_use_real_canonical_records(self):
        parsed = self._reader(self.composed_release_brief, check_role=True)
        self.assertEqual(parsed["plans"], ["39", "50", "40", "72"])
        self.assertEqual(parsed["errors"], [])
        # Plan72 is an enabler. A fictional project->gap edge is forbidden.
        self.assertEqual(parsed["roles"], [])

    def test_missing_authored_plan_row_and_repo_release_row_are_refused(self):
        # Mutate only the disposable authored fixture, not a canonical file.
        no_plan = "\n".join(
            line for line in self.composed_release_brief.splitlines()
            if "| astrid-dev | `release/15/plan-72` |" not in line
        ) + "\n"
        result = self._reader(no_plan)
        self.assertTrue(
            any("Included plan 72 has no" in e for e in result["errors"]),
            result["errors"],
        )
        no_release = "\n".join(
            line for line in self.composed_release_brief.splitlines()
            if "| astrid-dev | `release/15/main` |" not in line
        ) + "\n"
        result = self._reader(no_release)
        self.assertTrue(
            any("astrid-dev" in e and "no release row" in e for e in result["errors"]),
            result["errors"],
        )


    def test_paired_frozen_and_selected_code_export_same_authored_feed(self):
        # This is genuine CODE-version parity with identical authored inputs,
        # not a comparison of two differently-authored historical snapshots.
        # The baseline is another detached checkout of the pinned frozen
        # release; both sides receive precisely the same three records and
        # release brief. Never change source fixtures or copy the new parser
        # into the frozen baseline to manufacture a passing comparison.
        import hashlib
        import json

        def authored_inventory(root: Path) -> dict[str, str]:
            return {
                path.relative_to(root).as_posix(): hashlib.sha256(
                    path.read_bytes()
                ).hexdigest()
                for path in root.rglob("*.md")
                if ".git" not in path.relative_to(root).parts
            }

        script = """
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
from export_public_vision import build
payload = build(root, "0" * 40)
sys.stdout.buffer.write(
    (json.dumps(payload, ensure_ascii=False, indent=2) + "\\n").encode("utf-8")
)
"""
        def feed(root: Path) -> bytes:
            result = subprocess.run(
                (sys.executable, "-c", script, str(root)),
                cwd=root, capture_output=True,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                check=False,
            )
            self.assertEqual(
                result.returncode, 0,
                f"public vision build on {root} failed:\n"
                + result.stderr.decode(errors="replace"),
            )
            return result.stdout

        with tempfile.TemporaryDirectory(prefix="p72-r15-paired-parity-") as temp:
            baseline = Path(temp) / "frozen"
            created = False
            try:
                git("worktree", "add", "--detach", str(baseline), RELEASE_BASE)
                created = True
                self.assertEqual(
                    git("rev-parse", "HEAD", cwd=baseline).decode().strip(),
                    RELEASE_BASE,
                )
                for relative, sha in RECORD_BLOBS.items():
                    authored = (self.scratch / relative).read_bytes()
                    self.assertEqual(current_hash(authored), sha)
                    dest = baseline / relative
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(authored)
                (baseline / "releases/15.md").write_bytes(
                    (self.scratch / "releases/15.md").read_bytes()
                )

                frozen_inputs = authored_inventory(baseline)
                selected_inputs = authored_inventory(self.scratch)
                self.assertEqual(
                    frozen_inputs, selected_inputs,
                    "Both code revisions must see identical authored Markdown",
                )
                frozen_bytes = feed(baseline)
                selected_bytes = feed(self.scratch)
                self.assertEqual(
                    frozen_bytes, selected_bytes,
                    "Selected Plan72 code changed the fixed-revision public "
                    "feed with identical authored records; frozen="
                    + hashlib.sha256(frozen_bytes).hexdigest()
                    + " selected="
                    + hashlib.sha256(selected_bytes).hexdigest(),
                )
                self.assertEqual(json.loads(frozen_bytes)["schemaVersion"], 1)
                self.assertEqual(
                    frozen_inputs, authored_inventory(baseline),
                    "Baseline exporter mutated authored Markdown",
                )
                self.assertEqual(
                    selected_inputs, authored_inventory(self.scratch),
                    "Selected exporter mutated authored Markdown",
                )
                print(
                    "P72 PAIRED FEED PARITY: bytes=" + str(len(frozen_bytes))
                    + " sha256=" + hashlib.sha256(frozen_bytes).hexdigest()
                    + " authored_files=" + str(len(frozen_inputs))
                )
            finally:
                if created:
                    git("worktree", "remove", "--force", str(baseline))

    def test_public_vision_feed_is_unchanged_by_real_traversal(self):
        # Same authored input, same fixed revision and same frozen exporter.
        # This establishes non-mutation; NOT cross-revision byte parity.
        exporter = self.scratch / "scripts/export_public_vision.py"
        self.assertEqual(
            current_hash(exporter.read_bytes()),
            "672eb3a0eb6889df7dec3486eb55734d18eef282",
        )
        script = """
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
from export_public_vision import build
from project_delivery import load_delivery, deliveries_for_goal
from relationships import RecordRef
revision = "0" * 40
before_page = build(root, revision)
before = (json.dumps(before_page, ensure_ascii=False, indent=2) + "\\n").encode()
graph = load_delivery(root)
paths = deliveries_for_goal(
    graph, RecordRef("goal", "pillar:artistic-ambition/finished-artistic-work")
)
if not paths:
    raise AssertionError("no authored real goal-to-release traversal")
after_page = build(root, revision)
after = (json.dumps(after_page, ensure_ascii=False, indent=2) + "\\n").encode()
if after != before:
    raise AssertionError("real delivery traversal changed public vision feed bytes")
if after_page["schemaVersion"] != 1:
    raise AssertionError("public vision schema-v1 identity changed")
print("P72 FEED SAME-INPUT: bytes=" + str(len(before))
      + " sha256=" + hashlib.sha256(before).hexdigest()
      + " authored_paths=" + str(len(paths)))
"""
        result = subprocess.run(
            (sys.executable, "-c", script, str(self.scratch)),
            cwd=self.scratch, capture_output=True, text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            check=False,
        )
        self.assertEqual(
            result.returncode, 0,
            "Pinned-source read-only feed stability:\n" + result.stdout
            + result.stderr,
        )
        self.assertIn("P72 FEED SAME-INPUT: bytes=", result.stdout)

    def test_historical_rows_and_direct_source_selection_classify_full_check(self):
        # CONDITIONAL, scratch-only proof. Never update Release15/main or
        # suggest the Lead has approved these historical branch records.
        # Select only exact current-main Git blobs required by original errors,
        # preserving the frozen briefs' original Included-plan sets.
        import re

        missing_sources = {
            "skills/shared/workstreams/astrid-dev-plan/SKILL.md":
                "8dbe54a4342aadf9531409d7a320e887b6bded68",
            "skills/shared/workstreams/astrid-dev-release/SKILL.md":
                "13e67ad00410464ca6a323adc0de9e4a1a192bd6",
            "skills/shared/run-contract.md":
                "71a32afa24dd913568f0855b5bd0c39cb9f73589",
            "plans/72-composable-project-delivery/evidence/tests/astrid-dev/4b3e384/summary.md":
                "d8f1a1a8bdc02b63e46ebdcf5ec75f36164f433e",
            "plans/72-composable-project-delivery/evidence/tests/astrid-dev/2bef3d9b/summary.md":
                "a6368f05e613b37c6eef5c1cb167e17e40dfdcb8",
            "plans/72-composable-project-delivery/evidence/tests/astrid-dev/16eaf648/feed-parity.md":
                "4090b378f32cf3293bb6477576015e78335481d0",
            "plans/72-composable-project-delivery/evidence/tests/astrid-dev/57703432/summary.md":
                "0f7e4bb0f3fe56e0f06920bddd290056f33df80e",
            "plans/72-composable-project-delivery/evidence/tests/astrid-dev/915761c4/summary.md":
                "02942215aff7c899869e5dc02fd1882409859fea",
            "plans/72-composable-project-delivery/evidence/tests/astrid-dev/915761c4/feed-parity.md":
                "62a92a9c1875b4a20c3087d3033c165979c1a9bf",
        }
        releases = {
            "14": {
                "frozen": "3abb990ef613c5ba8a13fa5f60130a8d6b510f8a",
                "canonical": "957772f4048623a628438c0d10f9f276fc900465",
                "missing_plans": ("52",),
            },
            "16": {
                "frozen": "cd4fe6d0cd8f2e3a8551a9174654b99f90b9bf08",
                "canonical": "0c15894349237d83c72720141389722478fca026",
                "missing_plans": ("29", "30", "09", "38", "31"),
            },
            "17": {
                "frozen": "6c873adba56286bb7c6f5024de7ad69372aee364",
                "canonical": "0adcbce2fe94a36541ed873e456855316fac3fc2",
                "missing_plans": ("19",),
            },
        }
        originals = {}
        new_files = []
        added_historical_rows = 0
        def rows(text):
            match = re.search(r"^## Branches\n(.+?)(?=^## |\Z)", text,
                              re.M | re.S)
            if not match:
                raise AssertionError("Missing historical Branches section")
            return [
                line for line in match.group(1).splitlines()
                if line.startswith("| ") and not line.startswith(
                    ("| Repository", "| ---")
                )
            ]

        try:
            for number, info in releases.items():
                path = self.scratch / "releases" / f"{number}.md"
                original = path.read_bytes()
                self.assertEqual(current_hash(original), info["frozen"])
                originals[path] = original
                old_text = original.decode("utf-8")
                canonical = blob(info["canonical"]).decode("utf-8")
                old_rows = rows(old_text)
                selected = []
                included = old_text.split("## Included plans\n", 1)[1].split(
                    "\n## ", 1
                )[0]
                for plan in info["missing_plans"]:
                    self.assertIn(f"- [Plan {plan}]", included)
                    matches = [line for line in rows(canonical)
                               if f"| plan {plan} |" in line]
                    self.assertTrue(matches, f"release {number}: no canonical {plan}")
                    selected.extend(matches)
                for repository in sorted(set(
                    line.split("|")[1].strip() for line in selected
                )):
                    if not any(
                        row.startswith(f"| {repository} | ")
                        and " | release |" in row for row in old_rows
                    ):
                        release_rows = [
                            line for line in rows(canonical)
                            if line.startswith(f"| {repository} | ")
                            and " | release |" in line
                        ]
                        self.assertEqual(len(release_rows), 1)
                        selected.insert(0, release_rows[0])
                self.assertEqual(len(selected), len(set(selected)))
                self.assertFalse(any(line in old_rows for line in selected))
                added_historical_rows += len(selected)
                before, after = old_text.split("\n## Issues\n", 1)
                before = before.rstrip("\n")
                self.assertTrue(before.splitlines()[-1].startswith("|"))
                path.write_text(
                    before + "\n" + "\n".join(selected)
                    + "\n\n## Issues\n" + after, encoding="utf-8"
                )

            # The branch-table-only migration should eliminate every
            # historical release-documents error, but the 15 Plan72 authored
            # local links must still be missing until their source is present.
            self.assertEqual(added_historical_rows, 22)

            def original_check(stage):
                result = subprocess.run(
                    (sys.executable, "scripts/astrid_dev.py", "check"),
                    cwd=self.scratch, text=True, capture_output=True,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                    check=False,
                )
                errors = [line for line in result.stdout.splitlines()
                          if line.startswith("ERROR ")]
                self.assertEqual(
                    result.returncode, int(bool(errors)),
                    f"{stage}: original checker exit/diagnostic disagreement:\n"
                    + result.stdout + result.stderr,
                )
                print(
                    f"P72 CLOSURE {stage}: checker_exit={result.returncode} "
                    f"diagnostics={len(errors)} historical_rows="
                    f"{added_historical_rows}"
                )
                for line in errors:
                    print(f"P72 CLOSURE {stage} ERROR: " + line)
                return errors

            after_rows = original_check("ROWS")
            self.assertEqual(len(after_rows), 15, after_rows)
            self.assertTrue(
                all(line.startswith("ERROR markdown-links: "
                                     "plans/72-composable-project-delivery/")
                    for line in after_rows),
                after_rows,
            )

            for relative, sha in missing_sources.items():
                dest = self.scratch / relative
                self.assertFalse(
                    dest.exists(), f"dependency unexpectedly already exists: {relative}"
                )
                contents = blob(sha)
                self.assertEqual(current_hash(contents), sha)
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(contents)
                new_files.append(dest)

            residual = original_check("NINE_DIRECT_LINK_SOURCES")
            # The original Plan72 authored records and all older release
            # branch tables have had their *direct* dependencies provided.
            # Transitive links in the copied newer skills remain an honest
            # HOLD reason, not a reason to skip or weaken markdown-links.
            self.assertFalse(
                any(line.startswith("ERROR release-documents: ") for line in residual),
                residual,
            )
            self.assertFalse(
                any(line.startswith("ERROR markdown-links: "
                                    "plans/72-composable-project-delivery/"
                                    + name + ":")
                    for name in ("plan.md", "inputs.md", "tasks.md")
                    for line in residual),
                residual,
            )
            self.assertTrue(
                residual, "The pending owner-controlled dependency closure "
                          "unexpectedly passed without a full source selection",
            )
            self.assertTrue(
                all(line.startswith("ERROR markdown-links: ") for line in residual),
                "New non-link checker failures require separate adjudication: "
                + repr(residual),
            )
            self.assertTrue(
                any("glossary.md" in line for line in residual),
                "The known transitive shared-skill link must be reported",
            )
        finally:
            for path, data in originals.items():
                path.write_bytes(data)
                self.assertEqual(path.read_bytes(), data)
            for path in new_files:
                path.unlink()
            for path in new_files:
                self.assertFalse(path.exists())

    def test_full_repository_checker_on_disposable_selected_release(self):
        # A release candidate must eventually pass its real repository check,
        # not only the relationship reader's check command. This intentionally
        # does NOT label an incomplete scratch composition green: it records
        # exact errors so the Lead can distinguish absent authored views from
        # real implementation failures without changing protected checks.
        result = subprocess.run(
            (sys.executable, "scripts/astrid_dev.py", "check"),
            cwd=self.scratch, text=True, capture_output=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            check=False,
        )
        self.assertIn(
            result.returncode, (0, 1),
            "The original checker crashed or returned an invalid exit:\n"
            + result.stdout + result.stderr,
        )
        errors = [
            line for line in result.stdout.splitlines()
            if line.startswith("ERROR ")
        ]
        self.assertEqual(
            result.returncode, int(bool(errors)),
            "Check command exit and diagnostic presence contradict each other:\n"
            + result.stdout + result.stderr,
        )
        # Explicitly report, rather than suppress, each checker error ID.
        # A failing scratch source does not authorize changing any original
        # test, default-main source, protection or release record.
        for error in errors:
            print("P72 SCRATCH CHECK DIAGNOSTIC: " + error)
        print(
            f"P72 SCRATCH CHECK RESULT: exit={result.returncode} "
            f"diagnostics={len(errors)}"
        )

    def test_native_release15_enabler_inclusion_needs_authored_plan_line(self):
        # The branch table states intended branch custody; only the actual
        # Included plans bullet creates the release -> project edge. This
        # checks the REAL composed checkout, not synthetic sample Markdown.
        release = self.scratch / "releases/15.md"
        original = release.read_bytes()

        def native_relationships():
            script = """
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
from project_delivery import load_delivery, deliveries_for_goal
from relationships import RecordRef
graph = load_delivery(root)
enabler = RecordRef("project", "72")
goal = RecordRef("goal", "pillar:artistic-ambition/finished-artistic-work")
print(json.dumps({
    "enabler": enabler in graph.enablers,
    "addresses": len(graph.outgoing(enabler, "addresses")),
    "includes": [[link.source.id, link.role, link.source_path]
                 for link in graph.incoming(enabler, "includes")],
    "real_releases": sorted({p.release.id
                             for p in deliveries_for_goal(graph, goal)})
}))
"""
            result = subprocess.run(
                (sys.executable, "-c", script, str(self.scratch)),
                cwd=self.scratch, text=True, capture_output=True,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                check=False,
            )
            self.assertEqual(result.returncode, 0,
                             result.stdout + result.stderr)
            import json
            return json.loads(result.stdout)

        actual = native_relationships()
        self.assertTrue(actual["enabler"])
        self.assertEqual(actual["addresses"], 0)
        self.assertEqual(
            actual["includes"], [["15", "included", "releases/15.md"]]
        )
        self.assertEqual(actual["real_releases"], ["13"])

        source = original.decode("utf-8")
        plan72 = [
            line for line in source.splitlines(keepends=True)
            if line.startswith("- [Plan 72](")
        ]
        self.assertEqual(len(plan72), 1, "Expected one authored Plan72 bullet")
        release.write_text(source.replace(plan72[0], "", 1), encoding="utf-8")
        try:
            unlisted = native_relationships()
            self.assertTrue(unlisted["enabler"])
            self.assertEqual(unlisted["addresses"], 0)
            self.assertEqual(
                unlisted["includes"], [],
                "An orphan plan-72 branch-table row cannot grant release membership",
            )
            self.assertEqual(
                unlisted["real_releases"], actual["real_releases"],
                "Removing a Plan72 membership must not invent or erase "
                "unrelated genuine Release13 delivery paths",
            )
        finally:
            release.write_bytes(original)
        self.assertEqual(release.read_bytes(), original)

    def test_native_project_delivery_cli_on_composed_release(self):
        # Exercise the actual user-facing read-only CLI from the temporary
        # Release15 checkout rather than importing it from the source PR.
        def invoke(*args):
            return subprocess.run(
                (sys.executable, "scripts/project_delivery.py", *args,
                 "--root", str(self.scratch)),
                cwd=self.scratch, text=True, capture_output=True,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                check=False,
            )

        validated = invoke("check")
        self.assertEqual(
            validated.returncode, 0, validated.stdout + validated.stderr
        )
        self.assertIn("Validated ", validated.stdout)
        self.assertIn("typed relationships", validated.stdout)

        goal = invoke(
            "goal", "pillar:artistic-ambition/finished-artistic-work"
        )
        self.assertEqual(goal.returncode, 0, goal.stdout + goal.stderr)
        # Pin the ACTUAL frozen authored path and role ordering. AA-001 is
        # present in the graph, but this goal's release paths travel through
        # F-003 and Release13, not AA-001 or enabler Plan72.
        base = "goal:pillar:artistic-ambition/finished-artistic-work"
        self.assertEqual(goal.stdout.splitlines(), [
            base + " -> gap:F-003 (supporting) -> project:20 (primary) -> release:13",
            base + " -> gap:F-003 (supporting) -> project:32 (supporting) -> release:13",
            base + " -> gap:F-003 (supporting) -> project:34 (primary) -> release:13",
        ])
        # Plan72 is a gapless enabler; it must not acquire a fictitious
        # addresses edge to manufacture a path to Release15.
        self.assertNotIn("project:72", goal.stdout)

        unknown_issue = invoke("issue", "999999999999")
        self.assertEqual(
            unknown_issue.returncode, 0,
            unknown_issue.stdout + unknown_issue.stderr,
        )
        self.assertEqual(
            unknown_issue.stdout, "",
            "An issue absent from the frozen ledger is not shipped evidence",
        )

    def test_original_traversal_refuses_missing_canonical_gap_source(self):
        # A genuine authored vision gap is required to construct the
        # real source path, not simply a recognizable filename in a link.
        gap = self.scratch / "vision/gaps/AA-001-sustained-creative-work.md"
        canonical = gap.read_bytes()
        self.assertEqual(
            current_hash(canonical), "265a4fcfcf16a61b9fc0c1cde21db825e99ae0ab"
        )
        test_id = (
            "test_project_delivery.DeliveryCompositionTests."
            "test_actual_repository_delivery_traversal"
        )
        gap.unlink()
        try:
            result = subprocess.run(
                (sys.executable, "-m", "unittest", test_id),
                cwd=self.scratch, capture_output=True, text=True,
                env={
                    **os.environ,
                    "PYTHONPATH": str(self.scratch / "scripts"),
                    "PYTHONDONTWRITEBYTECODE": "1",
                },
                check=False,
            )
            self.assertNotEqual(
                result.returncode, 0,
                "Unresolved authored AA-001 was accepted as genuine source",
            )
            self.assertIn(
                "AA-001", result.stderr,
                "The failure must identify the missing authored gap",
            )
        finally:
            gap.write_bytes(canonical)
        self.assertEqual(
            current_hash(gap.read_bytes()),
            "265a4fcfcf16a61b9fc0c1cde21db825e99ae0ab",
        )

    def test_original_traversal_fails_without_canonical_plan72_record(self):
        # Negative control: the real original traversal must fail if the
        # authored project 72 source is missing, even when the release brief
        # still lists its membership. Modify ONLY our detached scratch tree.
        plan = self.scratch / "plans/72-composable-project-delivery/plan.md"
        original = plan.read_bytes()
        test_id = (
            "test_project_delivery.DeliveryCompositionTests."
            "test_actual_repository_delivery_traversal"
        )
        plan.unlink()
        try:
            result = subprocess.run(
                (sys.executable, "-m", "unittest", test_id),
                cwd=self.scratch, capture_output=True, text=True,
                env={
                    **os.environ,
                    "PYTHONPATH": str(self.scratch / "scripts"),
                    "PYTHONDONTWRITEBYTECODE": "1",
                },
                check=False,
            )
            self.assertNotEqual(
                result.returncode, 0,
                "Missing authored Plan72 source improperly passed the original test",
            )
            self.assertIn("Plan 72 names unknown folder", result.stderr)
        finally:
            # Restore the exact canonical blob regardless of failure.
            plan.write_bytes(original)
        self.assertEqual(current_hash(plan.read_bytes()), RECORD_BLOBS[
            "plans/72-composable-project-delivery/plan.md"
        ])

    def test_original_real_repository_delivery_traversal_on_native_release(self):
        # Run the EXISTING, UNMODIFIED end-to-end oracle from the actual
        # patched frozen checkout, not the current source PR's source tree.
        # An inferred plan membership or a mere branch-table row is not proof.
        test_id = (
            "test_project_delivery.DeliveryCompositionTests."
            "test_actual_repository_delivery_traversal"
        )
        result = subprocess.run(
            (sys.executable, "-m", "unittest", test_id),
            cwd=self.scratch, capture_output=True, text=True,
            env={
                **os.environ,
                "PYTHONPATH": str(self.scratch / "scripts"),
                "PYTHONDONTWRITEBYTECODE": "1",
            },
            check=False,
        )
        self.assertEqual(
            result.returncode, 0,
            "Original real-tree traversal on the frozen release source:\n"
            + result.stdout + result.stderr,
        )


if __name__ == "__main__":
    unittest.main()
