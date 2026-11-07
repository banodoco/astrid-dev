"""Focused tests for the plan catalog generator and validator."""
import tempfile
import unittest
from pathlib import Path

from check_docs import (DIVIDER, HEADER, catalog_rows, local_links,
                        unnamed_active_owners)


def example(status='active', key='01-alpha'):
    return f'| Alpha | Goal | {status} | Owner | TBD | — | [Plan 01]({key}/plan.md) |'


class CatalogTests(unittest.TestCase):
    def test_invalid_status(self):
        text = HEADER + '\n' + DIVIDER + '\n' + example('maybe')
        with self.assertRaisesRegex(ValueError, 'invalid status'):
            catalog_rows(text)

    def test_terminal_not_before_active(self):
        text = HEADER + '\n' + DIVIDER + '\n' + example('done') + '\n' + example('queued', '02-beta')
        with self.assertRaisesRegex(ValueError, 'follow'):
            catalog_rows(text)

    def test_active_projects_require_a_named_owner_without_new_statuses(self):
        named = catalog_rows(HEADER + '\n' + DIVIDER + '\n' + example('active'))
        self.assertEqual(unnamed_active_owners(named), [])
        unnamed = catalog_rows(HEADER + '\n' + DIVIDER + '\n'
                               + example('active').replace('| Owner |', '| Unassigned |'))
        self.assertEqual(len(unnamed_active_owners(unnamed)), 1)

    def test_relative_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'plans').mkdir()
            (root / 'README.md').write_text('[ok](plans/) and [missing](absent.md)\n')
            self.assertEqual(len(local_links(root, Path('README.md'))), 1)


if __name__ == '__main__':
    unittest.main()
