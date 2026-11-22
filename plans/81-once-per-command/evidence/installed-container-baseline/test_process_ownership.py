import unittest
from unittest.mock import patch
from process_ownership import chain_current, matching_chain


class OwnershipMatcherTests(unittest.TestCase):
    def setUp(self):
        self.root = '/install/program/versions'
        self.snapshot = {
            10: (1, 100, '/bin/bash', ('script',)),
            11: (10, 110, self.root + '/python', (self.root + '/runtime.py',)),
            12: (10, 120, '/elsewhere/runtime', ()),
            13: (1, 130, self.root + '/runtime', ()),
        }

    def match(self, pid, ancestor_start=100):
        return matching_chain(self.snapshot, pid, 10, ancestor_start, (self.root,))

    def test_owned_child(self):
        self.assertEqual(self.match(11), [(11, 110), (10, 100)])

    def test_other_path_child(self):
        self.assertIsNone(self.match(12))

    def test_allowed_path_unrelated_parent(self):
        self.assertIsNone(self.match(13))

    def test_stale_pid_and_reused_ancestor(self):
        self.assertIsNone(self.match(99))
        self.assertIsNone(self.match(11, ancestor_start=99))

    def test_live_path_change_rejects_previously_matched_child(self):
        chain = self.match(11)
        current = dict(self.snapshot)
        current[11] = (10, 110, '/elsewhere/runtime', ('/elsewhere/runtime',))
        with patch('process_ownership.read_process', side_effect=current.get):
            self.assertFalse(chain_current(chain, self.snapshot, (self.root,)))
        current[11] = self.snapshot[11]
        with patch('process_ownership.read_process', side_effect=current.get):
            self.assertTrue(chain_current(chain, self.snapshot, (self.root,)))

    def test_prefix_is_not_a_directory_boundary(self):
        self.snapshot[14] = (10, 140, self.root + '-other/runtime', ())
        self.assertIsNone(self.match(14))


if __name__ == '__main__':
    unittest.main()
