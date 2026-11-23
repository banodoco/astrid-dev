import os
from pathlib import Path
import subprocess
import sys
import unittest
from process_ownership import matching_chain

ROOT = Path(__file__).resolve().parent

class CleanupBoundary(unittest.TestCase):
    def test_data_argument_does_not_identify_service(self):
        root = '/install/program/versions'
        snapshot = {10: (1, 100, '/bin/bash', ('bash',)),
                    11: (10, 110, '/bin/cat', ('cat', root + '/data'))}
        self.assertIsNone(matching_chain(snapshot, 11, 10, 100, (root,)))

    def test_forged_program_arguments_do_not_identify_service(self):
        root = '/install/program/versions'
        snapshot = {10: (1, 100, '/bin/bash', ('bash',)),
                    11: (10, 110, '/usr/bin/python3', (root + '/runtime.py',)),
                    12: (10, 120, '/usr/bin/python3', ('python3', root + '/runtime.py')),
                    13: (10, 130, root + '/python', ('python',))}
        self.assertIsNone(matching_chain(snapshot, 11, 10, 100, (root,)))
        self.assertIsNone(matching_chain(snapshot, 12, 10, 100, (root,)))
        self.assertEqual(matching_chain(snapshot, 13, 10, 100, (root,)), [(13, 130), (10, 100)])

    def test_helper_does_not_signal_itself(self):
        start = Path(f'/proc/{os.getpid()}/stat').read_text().rsplit(')', 1)[1].split()[19]
        proc = subprocess.run([sys.executable, str(ROOT / 'process_ownership.py'), 'descendants', str(os.getpid()), start, str(ROOT)], capture_output=True)
        self.assertEqual(proc.returncode, 0)

    def test_legacy_runner_is_retired(self):
        proc = subprocess.run(['bash', str(ROOT / 'run-installed-baseline.sh')], capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('retired', proc.stderr)

if __name__ == '__main__': unittest.main()
