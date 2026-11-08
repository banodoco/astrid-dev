"""Focused tests for the plan catalog generator and validator."""
import tempfile
import unittest
from pathlib import Path

from check_docs import (ROOT, ledger_entry_errors, ledger_errors, strategy_errors, DIVIDER, HEADER, catalog_rows, local_links, obsolete_template_paths,
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


class StrategyTests(unittest.TestCase):
    GOOD = (
        "# Strategy\n\n**Last reviewed:** 2026-11-08, by the owner.\n\n## Focus now\n\nF-001.\n\n## Sequence\n\n"
        "| Order | When | Gap | Plans | What creators get | Waiting on |\n|---|---|---|---|---|---|\n"
        "| 1 | Now | [F-001](vision/gaps/F-001-platform-reliability.md) | [Plan 29](plans/29-update-and-release/plan.md) | Update now | owner go |\n"
        "| 2 | Next | [F-001](vision/gaps/F-001-platform-reliability.md) | Green mains (proposed) | Green checks | Plan 31 |\n"
        "\n## Not now\n\n- Other gaps.\n\n## Decisions\n\n- 2026-11-08: Release 10 first.\n")

    def test_valid_strategy_passes(self):
        self.assertEqual(strategy_errors(self.GOOD), [])

    def test_real_strategy_passes(self):
        self.assertEqual(strategy_errors((ROOT / 'strategy.md').read_text(encoding='utf-8')), [])

    def test_row_without_gap_link_fails(self):
        bad = self.GOOD.replace('[F-001](vision/gaps/F-001-platform-reliability.md) | [Plan 29]', 'F-001 | [Plan 29]')
        self.assertTrue(any('Gap must link' in e for e in strategy_errors(bad)))

    def test_row_without_plan_or_proposed_fails(self):
        bad = self.GOOD.replace('Green mains (proposed)', 'Green mains')
        self.assertTrue(any('Plans must link' in e for e in strategy_errors(bad)))

    def test_bad_when_and_missing_section_fail(self):
        bad = self.GOOD.replace('| 1 | Now |', '| 1 | Soon |').replace('## Not now', '## Later stuff')
        errors = strategy_errors(bad)
        self.assertTrue(any('When must be' in e for e in errors))
        self.assertTrue(any('## Not now' in e for e in errors))


class LedgerTests(unittest.TestCase):
    ENTRY = 'Date: 2026-11-08\nKind: fix\nSource: PR 1\nResolved by: —\n\nShort text.\n'
    EXISTING = {'2026-11-07-old.md', '2026-11-08-new.md'}

    def test_valid_entry_passes(self):
        self.assertEqual(ledger_entry_errors('2026-11-08-new.md', self.ENTRY, self.EXISTING), [])

    def test_bad_name_fails(self):
        errors = ledger_entry_errors('Ledger_1.md', self.ENTRY, self.EXISTING)
        self.assertTrue(any('file name' in e for e in errors))

    def test_bad_kind_fails(self):
        errors = ledger_entry_errors('2026-11-08-new.md', self.ENTRY.replace('fix', 'bug'), self.EXISTING)
        self.assertTrue(any('Kind must be' in e for e in errors))

    def test_date_must_match_name(self):
        errors = ledger_entry_errors('2026-11-09-new.md', self.ENTRY, {'2026-11-09-new.md'})
        self.assertTrue(any('Date must match' in e for e in errors))

    def test_dangling_references_fail(self):
        follows = self.ENTRY + '\nFollows: 2026-11-01-missing\n'
        self.assertTrue(any('Follows' in e for e in ledger_entry_errors('2026-11-08-new.md', follows, self.EXISTING)))
        resolved = self.ENTRY.replace('Resolved by: —', 'Resolved by: 2026-11-01-missing')
        self.assertTrue(any('Resolved by' in e for e in ledger_entry_errors('2026-11-08-new.md', resolved, self.EXISTING)))
        ok = self.ENTRY + '\nFollows: 2026-11-07-old\n'
        self.assertEqual(ledger_entry_errors('2026-11-08-new.md', ok, self.EXISTING), [])

    def test_real_ledger_passes(self):
        self.assertEqual(ledger_errors(ROOT), [])


if __name__ == '__main__':
    unittest.main()
