import tempfile
import unittest
from pathlib import Path

import migrate_catalog


class MigrateCatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / 'plans/01-alpha').mkdir(parents=True)
        (self.root / 'plans/index.md').write_text(
            '# Catalog\n\n| Project | Goal | Status | Owner | Estimate | Waiting on | Plan |\n'
            '|---|---|---|---|---:|---|---|\n'
            '| Alpha | Goal [link](../release.md) | active | Ada | 2 | — | [Plan 1](01-alpha/plan.md) |\n'
            '\n## Delivery context\n\nNotes here.\n', encoding='utf-8')
        self.plan = self.root / 'plans/01-alpha/plan.md'
        self.plan.write_text('# Alpha\n\n## Goal\n\nKeep this.\n', encoding='utf-8')
        self.rows = migrate_catalog._table.__globals__['check_docs'].catalog_rows(
            (self.root / 'plans/index.md').read_text(encoding='utf-8'))

    def tearDown(self):
        self.tmp.cleanup()

    def migrate(self, suffix=None):
        return migrate_catalog.migrate(self.root, self.rows, suffix)

    def test_dry_plan_and_write_are_idempotent(self):
        original = self.plan.read_bytes()
        planned = self.migrate()
        self.assertEqual(self.plan.read_bytes(), original)
        self.plan.write_text(planned[Path('plans/01-alpha/plan.md')], encoding='utf-8')
        once = self.plan.read_bytes()
        self.plan.write_text(self.migrate()[Path('plans/01-alpha/plan.md')], encoding='utf-8')
        self.assertEqual(self.plan.read_bytes(), once)
        self.assertEqual(self.plan.read_text().count('**Project:** Alpha'), 1)

    def test_changed_catalog_value_replaces_block(self):
        initial = self.migrate()[Path('plans/01-alpha/plan.md')]
        self.plan.write_text(initial, encoding='utf-8')
        self.rows[0][0] = 'New Alpha'
        updated = self.migrate()[Path('plans/01-alpha/plan.md')]
        self.assertIn('**Project:** New Alpha', updated)
        self.assertNotIn('**Project:** Alpha\n', updated)

    def test_relative_links_are_rebased(self):
        content = self.migrate()[Path('plans/01-alpha/plan.md')]
        self.assertIn('[link](../../release.md)', content)

    def test_suffix_tree(self):
        fixture = self.root / 'plans/01-alpha/plan.md.fixture'
        fixture.write_text('# Alpha\n\n## Goal\n', encoding='utf-8')
        index = self.root / 'plans/index.md.fixture'
        index.write_text((self.root / 'plans/index.md').read_text(), encoding='utf-8')
        planned = self.migrate('.fixture')
        self.assertIn(Path('plans/01-alpha/plan.md.fixture'), planned)

    def test_refuses_missing_plan(self):
        self.plan.unlink()
        with self.assertRaisesRegex(ValueError, 'missing plan'):
            self.migrate()

    def test_refuses_folder_without_row(self):
        (self.root / 'plans/02-orphan').mkdir()
        (self.root / 'plans/02-orphan/plan.md').write_text('# Orphan\n\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'folder has no catalog row'):
            self.migrate()

    def test_refuses_non_title(self):
        self.plan.write_text('Alpha\n\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'line 1 is not a title'):
            self.migrate()

    def test_refuses_field_outside_block(self):
        self.plan.write_text('# Alpha\n\n**Owner:** Ada\n\n## Goal\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'outside migration block'):
            self.migrate()


if __name__ == '__main__':
    unittest.main()
