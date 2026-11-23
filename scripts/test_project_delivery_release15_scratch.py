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
