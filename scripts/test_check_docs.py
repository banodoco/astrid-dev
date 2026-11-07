"""Focused tests for the plan catalog generator and validator."""
import tempfile
import unittest
from pathlib import Path

from check_docs import (BEGIN, DIVIDER, END, HEADER, catalog_rows, local_links,
                        preview, replace_preview, unnamed_active_owners)


def example(status='active', key='01-alpha'):
    return f'| Alpha | Goal | {status} | Owner | TBD | — | [Plan 01]({key}/plan.md) |'


class CatalogTests(unittest.TestCase):
    def test_top_ten_ignores_terminal_statuses(self):
        lines = [example('done'), example('active', '02-beta'),
                 example('queued', '03-gamma')]
        # Completed work must follow prioritized rows.
        text = '# Index\n\n' + HEADER + '\n' + DIVIDER + '\n' + '\n'.join(lines[1:] + lines[:1])
        rows = catalog_rows(text)
        self.assertEqual(len(rows), 3)
        result = preview(rows)
        self.assertIn('](plans/02-beta/plan.md)', result)
        self.assertNotIn('](plans/01-alpha/plan.md)', result)

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

    def test_owner_only_change_does_not_change_readme_preview(self):
        before = catalog_rows(HEADER + '\n' + DIVIDER + '\n'
                              + example('queued').replace('| Owner |', '| Unassigned |'))
        after = catalog_rows(HEADER + '\n' + DIVIDER + '\n'
                             + example('queued').replace('| Owner |', '| @casey |'))
        self.assertEqual(preview(before), preview(after))
        self.assertNotIn('| Owner |', preview(before))

    def test_generated_preview_drift(self):
        before = f'# README\n{BEGIN}\noutdated\n{END}\n'
        after = replace_preview(before, 'updated')
        self.assertIn(f'{BEGIN}\nupdated\n{END}', after)
        self.assertEqual(after, replace_preview(after, 'updated'))
        self.assertNotEqual(before, after)

    def test_relative_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'plans').mkdir()
            (root / 'README.md').write_text('[ok](plans/) and [missing](absent.md)\n')
            self.assertEqual(len(local_links(root, Path('README.md'))), 1)


if __name__ == '__main__':
    unittest.main()
