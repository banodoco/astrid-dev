import io
import os
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import records
import release_issues as ri

BRIEF = '''# Release 15 — Sample release

**Release:** 15
**State:** Draft
**Kind:** minor

## Highlight

A sufficiently long highlight.

## Intent

Intent.

## Approach

Approach.

## Included plans

- [Plan 39](../plans/39-thing/plan.md) — One.
- [Plan 50](../plans/50-thing/plan.md) — Two.
- [Plan 40](../plans/40-thing/plan.md) — Three.

## Publication

Not pinned.
'''


def issue(n, labels, state="open", reason=None):
    return {"number": n, "labels": [{"name": x} for x in labels], "state": state,
            "state_reason": reason, "title": "UNTRUSTED TITLE"}


class IssuesTests(unittest.TestCase):
    def test_membership_refresh_freeze_and_validation(self):
        first = [issue(4, ["release:15", "plan:39", "bug"]), issue(2, ["plan:50"]),
                 issue(5, ["plan:40", "idea"]), issue(8, ["release:15"],),
                 {"number": 9, "pull_request": {}}]
        def api(method, path):
            self.assertEqual(method, "GET")
            if "?" in path:
                return first
            return issue(2, [], "closed", "completed")
        one = ri.refresh(BRIEF, 15, today=date(2026, 11, 16), api=api)
        rows = records.release_brief(one)["issues"]
        self.assertEqual([r['number'] for r in rows], [2, 4, 5, 8])
        self.assertEqual(rows[1]['via'], ['plan:39', 'release:15'])
        self.assertNotIn('UNTRUSTED TITLE', one)
        self.assertEqual(one, ri.refresh(one, 15, today=date(2026, 11, 17), api=api))
        first.pop(1)
        first[0]['labels'] = [{'name': 'bug'}]
        two = ri.refresh(one, 15, today=date(2026, 11, 17), api=api)
        rows = records.release_brief(two)['issues']
        self.assertEqual(rows[0]['state'], 'done')
        self.assertEqual(rows[1]['via'], ['plan:39', 'release:15'])
        self.assertIn('2026-11-17', two)
        frozen = ri.refresh(two, 15, freeze=True, today=date(2026, 11, 18), api=api)
        self.assertTrue(records.release_brief(frozen)['issues_frozen'])
        with self.assertRaisesRegex(ValueError, 'frozen'):
            ri.refresh(frozen, 15, api=lambda *a: self.fail('must not query'))
        bad = one.replace(' | bug | open |', ' | bug extra | open |')
        with self.assertRaises(ValueError):
            ri.refresh(bad, 15, api=api)

    def test_pagination_and_closed_reasons(self):
        calls = []
        def api(method, path):
            calls.append(path)
            return [issue(n, ['unrelated']) for n in range(1, 101)] if path.endswith('page=1') else [issue(101, ['plan:40'])]
        output = ri.refresh(BRIEF, 15, api=api, today=date(2026, 1, 1))
        self.assertEqual([r['number'] for r in records.release_brief(output)['issues']], [101])
        self.assertEqual(len(calls), 2)
        for reason, expected in [('completed','done'), (None,'done'), ('not_planned','decided not to act'), ('duplicate','duplicate')]:
            self.assertEqual(ri.issue_data(issue(1, [], 'closed', reason))[2], expected)
        for bad in [issue(1, ['bug','idea']), issue(1, [], 'mystery')]:
            with self.assertRaises(ValueError):
                ri.issue_data(bad)

    def test_irrelevant_issue_with_two_types_is_ignored(self):
        def api(method, path):
            return [issue(7, ['bug', 'idea']), issue(8, ['release:15', 'bug'])]
        output = ri.refresh(BRIEF, 15, api=api, today=date(2026, 11, 16))
        rows = records.release_brief(output)['issues']
        self.assertEqual([r['number'] for r in rows], [8])
        self.assertEqual(rows[0]['type'], 'bug')

    def test_relevant_issue_with_two_types_names_issue(self):
        def api(method, path):
            return [issue(962, ['plan:39', 'bug', 'idea'])]
        with self.assertRaisesRegex(ValueError, r'issue #962 has more than one type label \(bug, idea\); leave one'):
            ri.refresh(BRIEF, 15, api=api, today=date(2026, 11, 16))

    def test_existing_row_closed_without_reason_becomes_done(self):
        one = ri.refresh(BRIEF, 15, today=date(2026, 11, 16), api=lambda m, p: [issue(2, ['plan:50'])])
        def api(method, path):
            if '?' in path:
                return []
            return issue(2, ['plan:50'], 'closed', None)
        two = ri.refresh(one, 15, today=date(2026, 11, 17), api=api)
        rows = records.release_brief(two)['issues']
        self.assertEqual([(r['number'], r['state']) for r in rows], [(2, 'done')])

    def test_via_follows_current_routing_labels(self):
        one = ri.refresh(BRIEF, 15, today=date(2026, 11, 16), api=lambda m, p: [issue(4, ['plan:39', 'release:15'])])
        two = ri.refresh(one, 15, today=date(2026, 11, 17), api=lambda m, p: [issue(4, ['release:15'])])
        self.assertEqual(records.release_brief(two)['issues'][0]['via'], ['release:15'])
        def api(method, path):
            return [] if '?' in path else issue(4, ['plan:50'], 'closed', 'completed')
        three = ri.refresh(two, 15, today=date(2026, 11, 18), api=api)
        row = records.release_brief(three)['issues'][0]
        self.assertEqual((row['via'], row['state']), (['plan:50'], 'done'))

    def test_missing_token_gives_clear_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'scripts').mkdir()
            (root / 'releases').mkdir()
            path = root / 'releases/15.md'
            path.write_text(BRIEF)
            env = {k: v for k, v in os.environ.items() if k != 'GH_TOKEN'}
            with patch.object(ri, '__file__', str(root / 'scripts/release_issues.py')), \
                    patch.dict(os.environ, env, clear=True), \
                    patch('urllib.request.urlopen', side_effect=AssertionError('no network')), \
                    patch('sys.stderr', new_callable=io.StringIO) as err:
                self.assertEqual(ri.main(['15']), 1)
            self.assertEqual(err.getvalue(), 'release issues: set GH_TOKEN to a token that can read banodoco/astrid-dev issues\n')
            self.assertEqual(path.read_text(), BRIEF)

    def test_write_replaces_file_atomically(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'scripts').mkdir()
            (root / 'releases').mkdir()
            path = root / 'releases/15.md'
            path.write_text(BRIEF)
            expected = ri.refresh(BRIEF, 15, api=lambda *a: [issue(1, ['release:15'])])
            real_replace = os.replace
            with patch.object(ri, '__file__', str(root / 'scripts/release_issues.py')), \
                    patch.object(ri, 'request', return_value=[issue(1, ['release:15'])]), \
                    patch.object(ri.os, 'replace', wraps=real_replace) as rep:
                self.assertEqual(ri.main(['15']), 0)
            self.assertEqual(rep.call_count, 1)
            self.assertEqual(rep.call_args[0][1], path)
            self.assertEqual(path.read_text(encoding='utf-8'), expected)
            self.assertEqual([p.name for p in (root / 'releases').iterdir()], ['15.md'])

    def test_bad_blocks_refused(self):
        one = ri.refresh(BRIEF, 15, api=lambda *a: [issue(1, ['plan:39'])])
        for bad in [one.replace('<!-- release-issues:end -->', ''),
                    one.replace('## Issues', '## Issues\n\n## Issues'),
                    one.replace('<!-- release-issues:end -->', 'untrusted\n<!-- release-issues:end -->'),
                    one.replace('<!-- release-issues:end -->', one[one.index('| [#1]'):one.index('<!-- release-issues:end -->')] + '<!-- release-issues:end -->')]:
            with self.assertRaises(ValueError):
                ri.refresh(bad, 15, api=lambda *a: self.fail('must not query'))

    def test_cli_entrypoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'scripts').mkdir()
            (root / 'releases').mkdir()
            path = root / 'releases/15.md'
            path.write_text(BRIEF)
            with patch.object(ri, '__file__', str(root / 'scripts/release_issues.py')), patch.object(ri, 'request', return_value=[issue(1, ['release:15'])]):
                self.assertEqual(ri.main(['15']), 0)
                self.assertEqual(ri.main(['15', '--freeze']), 0)
                self.assertEqual(ri.main(['15']), 1)
            self.assertTrue(records.release_brief(path.read_text())['issues_frozen'])


if __name__ == '__main__':
    unittest.main()
