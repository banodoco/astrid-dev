"""Focused tests for the plan catalog generator and validator."""
import tempfile
import unittest
from pathlib import Path

from check_docs import (ROOT, ledger_entry_errors, ledger_errors, release_errors, strategy_errors, local_links, obsolete_template_paths,
                        route_issues, unnamed_active_owners)


def example(status='active', key='01-alpha'):
    return f'| Alpha | Goal | {status} | Owner | TBD | — | [Plan 01]({key}/plan.md) |'


class CatalogTests(unittest.TestCase):
    def record_errors(self, *, status="active", owner="Owner", folders=None, priority=""):
        import checks
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder, state in (folders or {"01-alpha": status}).items():
                target = root / "plans" / folder / "plan.md"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    "# A title\n\n**Project:** Alpha\n\n**Goal:** Goal\n\n"
                    f"**Status:** {state}\n\n**Owner:** {owner}\n\n"
                    "**Estimate:** TBD\n\n**Waiting on:** —\n", encoding="utf-8")
            (root / "plans/priority.md").write_text("## Order\n" + priority, encoding="utf-8")
            context = checks.Context(root)
            return checks._catalog(context), checks._catalog_paths(context)

    def test_invalid_status(self):
        errors, _ = self.record_errors(status="maybe")
        self.assertEqual(errors, ["plans/01-alpha/plan.md: invalid status 'maybe'; use queued, active, blocked, paused, done or cancelled"])

    def test_terminal_order_is_the_views_job(self):
        errors, paths = self.record_errors(folders={"01-alpha": "done", "02-beta": "queued"},
                                           priority="- 01-alpha\n- 02-beta\n")
        # Terminal grouping is now a view's responsibility, not a refusal.
        self.assertEqual(errors, [])
        self.assertEqual(paths, [])

    def test_active_projects_require_a_named_owner_without_new_statuses(self):
        self.assertEqual(self.record_errors(), ([], []))
        for status in ("queued", "blocked", "paused", "done", "cancelled"):
            with self.subTest(status=status):
                self.assertEqual(self.record_errors(status=status, owner="Unassigned"), ([], []))
        for owner in ("Unassigned", "TBD", "none", "—", "-"):
            with self.subTest(owner=owner):
                self.assertEqual(self.record_errors(owner=owner),
                                 ([], ["active project needs a named accountable owner: Alpha"]))

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
    RELEASE = (
        "# Release 13 — GPU control\n\n**Release:** 13\n**State:** Draft\n\n"
        "## Highlight\n\nCreators can control rented GPU machine lifetime.\n\n"
        "## Intent\n\nMake cost and lifetime clear.\n\n"
        "## Approach\n\nFollow existing machine controls.\n\n"
        "## Included plans\n\n"
        "- [Plan 40](../plans/40-machine-lifetime-controls/plan.md) — Include spend control.\n\n"
        "## Publication\n\nNot pinned. No publication authority.\n"
    )
    GOOD = (
        "# Strategy\n\n**Last reviewed:** 2026-11-10\n\n## Focus now\n\n## Versions\n\n"
        "### Version 1.0\n\n**Aim:** Finished work.\n\n"
        + "".join(f"#### Version 0.{n}\n\n**Aim:** {'Fast.' if n == 1 else 'Open'}\n\n"
                  f"<!-- strategy-0.{n}:start -->\n<!-- strategy-0.{n}:end -->\n\n" for n in range(1, 10))
        + "## Not now\n\n## Decisions\n"
    )

    def test_valid_strategy_passes(self):
        self.assertEqual(strategy_errors(self.GOOD, {'13.md': self.RELEASE}), [])

    def test_real_strategy_passes(self):
        docs = {p.name: p.read_text(encoding='utf-8')
                for p in (ROOT / 'releases').glob('[0-9]*.md') if p.stem.isdigit()}
        self.assertTrue(docs)
        self.assertEqual(strategy_errors((ROOT / 'strategy.md').read_text(encoding='utf-8'), docs), [])
        for name, body in docs.items():
            self.assertEqual(release_errors(name, body), [])

    def test_valid_release_brief_passes(self):
        self.assertEqual(release_errors('13.md', self.RELEASE), [])

    def test_release_requires_sections_and_plans(self):
        bad = self.RELEASE.replace('## Approach', '## Notes').replace(
            '[Plan 40](../plans/40-machine-lifetime-controls/plan.md)', 'Plan 40')
        errors = release_errors('13.md', bad)
        self.assertTrue(any('Approach' in e for e in errors))
        self.assertTrue(any('Included plans' in e for e in errors))

    def test_draft_without_plans_and_strict_plan_bullets(self):
        line = '- [Plan 40](../plans/40-machine-lifetime-controls/plan.md) — Include spend control.'
        self.assertEqual(release_errors('13.md', self.RELEASE.replace(line, 'None yet')), [])
        self.assertTrue(any('Included plans' in e for e in release_errors('13.md', self.RELEASE.replace(line, '- Plan 40 — Include spend control.'))))
        mixed = self.RELEASE.replace(line, line + '\n- Plan 41 — Another contribution.')
        self.assertTrue(any('dash and sentence' in e for e in release_errors('13.md', mixed)))
        final = self.RELEASE.replace(line, 'None yet').replace('**State:** Draft', '**State:** Final')
        self.assertTrue(any('Included plans' in e for e in release_errors('13.md', final)))

    def test_kind_errors_are_reported_alongside_existing_errors(self):
        bad = self.RELEASE.replace('**State:** Draft', '**State:** Draft\n**Kind:**\n**Kind:** minor').replace('## Approach', '## Notes')
        errors = release_errors('13.md', bad)
        self.assertTrue(any('Kind duplicated' in e for e in errors))
        self.assertTrue(any('Kind empty' in e for e in errors))
        self.assertTrue(any('Approach' in e for e in errors))

    def test_draft_needs_no_pins_but_final_does(self):
        self.assertEqual(release_errors('13.md', self.RELEASE), [])
        final = self.RELEASE.replace('**State:** Draft', '**State:** Final')
        self.assertTrue(any('JSON payload' in e for e in release_errors('13.md', final)))

    def test_versions_must_reach_the_major_version_without_gaps(self):
        bad = self.GOOD.replace('#### Version 0.5', '#### Version 0.6', 1)
        self.assertTrue(any('expected version 0.5' in e for e in strategy_errors(bad)))

    def test_version_needs_an_aim_and_major_cannot_be_open(self):
        bad = self.GOOD.replace('**Aim:** Fast.', '')
        self.assertTrue(any('version 0.1 needs an' in e for e in strategy_errors(bad)))
        bad = self.GOOD.replace('**Aim:** Finished work.', '**Aim:** Open')
        self.assertTrue(any('major version 1.0 needs a real aim' in e for e in strategy_errors(bad)))
        bad = self.GOOD.replace('**Aim:** Fast.', '**Aim:** Fast.\n**Aim:** Again.')
        self.assertTrue(any('duplicate field' in e for e in strategy_errors(bad)))

    def test_only_one_major_version_is_allowed(self):
        extra = "\n### Version 2.0\n\n**Aim:** Later.\n\n" + "".join(
            f"#### Version 1.{n}\n\n**Aim:** Open\n\n" for n in range(1, 10))
        bad = self.GOOD.replace('## Not now', extra + '## Not now')
        self.assertTrue(any('exactly one major' in e for e in strategy_errors(bad)))

    def test_release_kinds_and_generated_regions(self):
        docs = {f'{n}.md': self.RELEASE.replace('**State:** Draft', '**State:** Draft\n**Kind:** minor') for n in range(1, 11)}
        self.assertTrue(any('more than nine' in e for e in strategy_errors(self.GOOD, docs)))
        docs = {'1.md': self.RELEASE.replace('**State:** Draft', '**State:** Draft\n**Kind:** major'), '2.md': self.RELEASE}
        self.assertTrue(any('major release brief must be last' in e for e in strategy_errors(self.GOOD, docs)))
        generated = self.GOOD.replace('<!-- strategy-0.1:end -->', '#### Version 9.9\n**Aim:** bogus\n<!-- strategy-0.1:end -->')
        self.assertEqual(strategy_errors(generated), [])
        self.assertTrue(any('ordered' in e for e in strategy_errors(self.GOOD.replace('<!-- strategy-0.1:end -->', ''))))

    def test_bad_release_link_and_missing_section_fail(self):
        bad = self.GOOD.replace('## Not now', '## Later stuff')
        self.assertTrue(any('## Not now' in e for e in strategy_errors(bad)))


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
