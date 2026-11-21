"""Independent original-versus-reader feed-byte proof for Plan 72.

This does not call the proposed relationship reader. Both feeds are generated
by the original exporter within each immutable Git source tree.
Scratch experiment: never merge this test into the production branches.
"""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
BASE = "4b3e3841af3921d9846389a4cd744f027c1db0b3"
READER = "16eaf64899f2dde82c7cb79ad92b88928afbd374"
REPORTED_SIZE = 161224
REPORTED_SHA256 = "df1a3a245f88e0771464ac586802b4c9c7b5b4a7056e1e2e02787de94fe3faf1"


def _source_tree(commit: str, destination: Path) -> None:
    archive = subprocess.run(
        ["git", "archive", "--format=tar", commit],
        cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:") as tar:
        for member in tar:
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts:
                raise AssertionError("unsafe tracked path")
            target = destination / path
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                handle = tar.extractfile(member)
                if handle is None:
                    raise AssertionError(f"unreadable archive file: {member.name}")
                target.write_bytes(handle.read())


def _snapshot(source: Path, revision: str) -> bytes:
    # Execute the exporter from its OWN source snapshot, not the PR's copy.
    saved = {name: sys.modules.pop(name, None)
             for name in ("export_public_vision", "records", "check_docs",
                          "gap_relationships", "project_contract",
                          "vision_subject", "lifecycle")}
    sys.path.insert(0, str(source / "scripts"))
    try:
        from export_public_vision import build
        blob = json.dumps(build(source, revision), ensure_ascii=False, indent=2)
        return (blob + "\n").encode("utf-8")
    finally:
        sys.path.pop(0)
        for name, old in saved.items():
            sys.modules.pop(name, None)
            if old is not None:
                sys.modules[name] = old


class FixedRevisionPublicFeedPairTests(unittest.TestCase):
    def test_original_vs_reader_exact_serialized_bytes(self):
        with tempfile.TemporaryDirectory(prefix="plan72-feed-source-pair-") as td:
            root = Path(td)
            left, right = root / "base", root / "reader"
            left.mkdir()
            right.mkdir()
            _source_tree(BASE, left)
            _source_tree(READER, right)
            # Test multiple explicitly fixed revisions because the supplied
            # supplementary digest did not include its revision argument.
            revisions = ("0" * 40, BASE, READER)
            matches_reported_digest = []
            for revision in revisions:
                with self.subTest(revision=revision):
                    original = _snapshot(left, revision)
                    candidate = _snapshot(right, revision)
                    original_hash = hashlib.sha256(original).hexdigest()
                    candidate_hash = hashlib.sha256(candidate).hexdigest()
                    match = (len(original) == REPORTED_SIZE
                             and original_hash == REPORTED_SHA256)
                    print(f"PLAN72_FEED_PAIR base={BASE} reader={READER} "
                          f"revision={revision} base_bytes={len(original)} "
                          f"reader_bytes={len(candidate)} "
                          f"base_sha256={original_hash} "
                          f"reader_sha256={candidate_hash} "
                          f"reported_digest_match={match}", flush=True)
                    matches_reported_digest.append(match)
                    self.assertEqual(candidate, original,
                        "fixed-revision public-feed bytes differ")
            print("PLAN72_REPORTED_DIGEST_MATCHED="
                  + str(any(matches_reported_digest)), flush=True)


if __name__ == "__main__":
    unittest.main()
