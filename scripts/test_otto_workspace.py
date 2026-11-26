"""Check that the actual repository declares a loadable Otto workspace."""
from pathlib import Path
import unittest

from otto.config import load_workspace


class OttoWorkspaceTests(unittest.TestCase):
    def test_repository_workspace_loads(self):
        root = Path(__file__).resolve().parent.parent
        workspace = load_workspace(root)
        self.assertEqual(workspace.root, root)
        self.assertEqual(workspace.name, "astrid-dev")
        self.assertEqual(workspace.skill_namespace, "astrid-dev-")


if __name__ == "__main__":
    unittest.main()
