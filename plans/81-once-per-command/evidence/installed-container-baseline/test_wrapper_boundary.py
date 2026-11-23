"""Exercise wrapper preflight with only local fake executables."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent

class WrapperBoundary(unittest.TestCase):
    def test_selected_wrong_tuple_stops_before_version_receipt(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            program = root / 'program'
            version = program / 'versions' / 'one'
            version.mkdir(parents=True)
            (program / 'current').write_text('one\n')
            (version / 'manifest.json').write_text((ROOT / 'manifest-candidate.json').read_text())
            launcher = program / 'run-astrid'
            launcher.write_text('#!/bin/sh\nexit 0\n')
            launcher.chmod(0o755)
            fakebin = root / 'bin'
            fakebin.mkdir()
            curl = fakebin / 'curl'
            curl.write_text('#!/bin/sh\n: > "$3"\n')
            curl.chmod(0o755)
            runtime_repo = root / 'runtime-repo'
            subprocess.run(['git', 'init', '-q', str(runtime_repo)], check=True)
            out = root / "evidence ' quoted"
            env = dict(os.environ, IB=str(root), EVIDENCE_DIR=str(out), ARMS='before', PATH=f'{fakebin}:{os.environ["PATH"]}', ASTRID_RUNTIME_SOURCE_REPO=str(runtime_repo))
            result = subprocess.run(['bash', str(ROOT / 'run-ab-installed.sh')], env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('arm: installed', result.stdout + result.stderr)
            self.assertFalse((out / 'astrid-version-before.txt').exists())
            self.assertIn('arm: installed', (out / 'console.log').read_text())

    def test_existing_evidence_is_not_modified(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            out = root / 'evidence'
            out.mkdir()
            sentinel = out / 'install.sh'
            sentinel.write_text('preserve')
            result = subprocess.run(['bash', str(ROOT / 'run-ab-installed.sh')], env=dict(os.environ, IB=t, EVIDENCE_DIR=str(out)), capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(sentinel.read_text(), 'preserve')
            self.assertEqual(list(out.iterdir()), [sentinel])

if __name__ == '__main__':
    unittest.main()
