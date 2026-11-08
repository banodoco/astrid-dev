"""Focused tests for the plan catalog generator and validator."""
import tempfile
import unittest
from pathlib import Path

from check_docs import (DIVIDER, HEADER, ROOT, RELEASE_DIVIDER, RELEASE_HEADER, catalog_rows,
                        local_links, obsolete_template_paths, release_log_rows, unnamed_active_owners)


def example(status='active', key='01-alpha'):
    return f'| Alpha | Goal | {status} | Owner | TBD | — | [Plan 01]({key}/plan.md) |'


APP = '915bfa84d87268038f396dc999dc2095683e5d8a'
AGENT = '709492fa5f4850b9caf0cea4a4c543023b73fa0a'
RUNTIME = 'f4c7a4623c84da077daac3e3a9366fc2e6a55051'
LEGACY = (f'| 9 | 0.0.9 | legacy | 2026-11-07 | {APP} | {AGENT} | {RUNTIME} | — | no '
          '| [Plan 01](01-installer-consent/plan.md) | Owner decision 9, 8 Nov 2026 |')


def release(number, version, kind='patch', app=APP, owner='Owner go 9 Nov 2026'):
    return (f'| {number} | {version} | {kind} | 2026-11-09 | {app} | {AGENT} | {RUNTIME} | — | no '
            f'| [Plan 01](01-installer-consent/plan.md) | {owner} |')


def release_text(*rows):
    return '\n'.join([RELEASE_HEADER, RELEASE_DIVIDER, *rows]) + '\n'


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

    def test_obsolete_project_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'docs').mkdir()
            (root / 'docs/guide.md').write_text('Use strategy/projects/01-alpha/plan.md.\n')
            errors = obsolete_template_paths(root)
            self.assertTrue(any('obsolete strategy/projects path' in error for error in errors))


class ReleaseLogTests(unittest.TestCase):
    def test_legacy_release_9_row_passes(self):
        self.assertEqual(len(release_log_rows(release_text(LEGACY))), 1)
        self.assertEqual(len(release_log_rows((ROOT / 'plans/releases.md').read_text(encoding='utf-8'))), 1)

    def test_minor_and_major_successors_pass(self):
        rows = release_log_rows(release_text(LEGACY, release(10, '0.0.10'), release(11, '0.1.0', 'minor'),
                                             release(12, '0.1.1'), release(13, '1.0.0', 'major')))
        self.assertEqual(len(rows), 5)

    def test_release_numbers_go_up_by_exactly_one(self):
        with self.assertRaisesRegex(ValueError, 'release gap'):
            release_log_rows(release_text(LEGACY, release(11, '0.0.11')))

    def test_version_must_be_the_successor_of_its_kind(self):
        with self.assertRaisesRegex(ValueError, 'wrong version step'):
            release_log_rows(release_text(LEGACY, release(10, '0.1.0')))
        with self.assertRaisesRegex(ValueError, 'wrong version step'):
            release_log_rows(release_text(LEGACY, release(10, '0.0.10', 'minor')))
        with self.assertRaisesRegex(ValueError, 'wrong version step'):
            release_log_rows(release_text(LEGACY, release(10, '0.0.10', 'major')))

    def test_sha_must_be_full(self):
        with self.assertRaisesRegex(ValueError, 'full 40-character SHA'):
            release_log_rows(release_text(LEGACY, release(10, '0.0.10', app=APP[:7])))

    def test_owner_go_must_not_be_empty(self):
        with self.assertRaisesRegex(ValueError, 'empty owner go'):
            release_log_rows(release_text(LEGACY, release(10, '0.0.10', owner='—')))

    def test_plan_links_use_the_relative_link_check(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'plans/01-installer-consent').mkdir(parents=True)
            (root / 'plans/01-installer-consent/plan.md').write_text('# Plan 01\n')
            (root / 'plans/releases.md').write_text(release_text(LEGACY))
            self.assertEqual(local_links(root, Path('plans/releases.md')), [])
            broken = release_text(LEGACY).replace('01-installer-consent/plan.md', '99-missing/plan.md')
            (root / 'plans/releases.md').write_text(broken)
            self.assertEqual(len(local_links(root, Path('plans/releases.md'))), 1)


if __name__ == '__main__':
    unittest.main()
