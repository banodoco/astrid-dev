"""Focused tests for the plan catalog generator and validator."""
import tempfile
import unittest
from pathlib import Path

from check_docs import (DIVIDER, HEADER, catalog_rows, local_links, obsolete_template_paths,
                        route_issues, unnamed_active_owners)


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

    def test_obsolete_project_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'docs').mkdir()
            (root / 'docs/guide.md').write_text('Use strategy/projects/01-alpha/plan.md.\n')
            errors = obsolete_template_paths(root)
            self.assertTrue(any('obsolete strategy/projects path' in error for error in errors))


PLAN_OK = ('# Alpha\n\n**Vision gaps:** [Thing](../../vision/gaps/F-009-thing.md) (primary).\n\n'
           '**Contributes to closure:** F-009: first evidence item.\n')
ROUTE = ('## Closure approach\n\nThe idea and the order.\n\n## Route to closure\n\n'
         '| Step | Plan | Contributes | Milestone |\n|---|---|---|---|\n'
         '| 1 | [Plan 40](../../plans/40-alpha/plan.md) | first evidence item | A |\n\n'
         '## Sources and reassessment\n\nLinks.\n')


class RouteToClosureTests(unittest.TestCase):
    def test_gap_without_route_needs_nothing(self):
        self.assertEqual(route_issues('g.md', 'F-009', '## Gap\n\nText.\n', {}), [])

    def test_valid_route_passes(self):
        self.assertEqual(route_issues('g.md', 'F-009', ROUTE, {'40-alpha': PLAN_OK}), [])

    def test_route_needs_closure_approach(self):
        text = ROUTE.replace('## Closure approach\n\nThe idea and the order.\n\n', '')
        self.assertTrue(any('Closure approach' in i for i in route_issues('g.md', 'F-009', text, {'40-alpha': PLAN_OK})))

    def test_routed_plan_must_point_back(self):
        plan = PLAN_OK.replace('F-009-thing', 'F-001-other').replace('F-009:', 'F-001:')
        issues = route_issues('g.md', 'F-009', ROUTE, {'40-alpha': plan})
        self.assertTrue(any('Vision gaps' in i for i in issues))
        self.assertTrue(any('Contributes to closure' in i for i in issues))

    def test_route_rejects_missing_plan_and_status_words(self):
        text = ROUTE.replace('| A |', '| A (active) |')
        issues = route_issues('g.md', 'F-009', text, {})
        self.assertTrue(any('missing plan' in i for i in issues))
        self.assertTrue(any("'active'" in i for i in issues))


if __name__ == '__main__':
    unittest.main()
