"""Isolated lifecycle checks for the directly owned cleanup children."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parent
HELPER = ROOT / "process_ownership.py"


def starttime(pid):
    # The parenthesized comm may contain spaces; fields after it start at state.
    return Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[19]


def helper(*args):
    return subprocess.run([sys.executable, str(HELPER), *map(str, args)],
                          capture_output=True, text=True, check=True).stdout.strip()


class CleanupChildren(unittest.TestCase):
    def test_direct_standin_identity_stops_only_owned_process(self):
        owned = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
        decoy = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
        try:
            identity = helper("capture", owned.pid, os.getpid(), starttime(os.getpid()))
            self.assertEqual(identity, starttime(owned.pid))
            helper("signal", owned.pid, identity)
            self.assertNotEqual(owned.wait(timeout=5), 0)
            self.assertIsNone(decoy.poll())
        finally:
            for child in (owned, decoy):
                if child.poll() is None:
                    child.terminate()
                child.wait(timeout=5)

    def test_sampler_is_one_owned_process_and_stops(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "samples.txt"
            sampler = subprocess.Popen([sys.executable, str(ROOT / "load_sampler.py"), str(output)])
            try:
                identity = helper("capture", sampler.pid, os.getpid(), starttime(os.getpid()))
                deadline = time.monotonic() + 5
                while time.monotonic() < deadline and (not output.exists() or not output.stat().st_size):
                    self.assertIsNone(sampler.poll(), "sampler exited before producing a sample")
                    time.sleep(0.01)
                self.assertTrue(output.exists() and output.stat().st_size, "sampler did not write a sample")
                children = Path(f"/proc/{sampler.pid}/task/{sampler.pid}/children").read_text().strip()
                self.assertEqual(children, "", "sampler should not leave a sleep child")
                helper("signal", sampler.pid, identity)
                self.assertNotEqual(sampler.wait(timeout=5), 0)
            finally:
                if sampler.poll() is None:
                    sampler.terminate()
                sampler.wait(timeout=5)


if __name__ == "__main__":
    unittest.main()
