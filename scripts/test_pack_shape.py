"""Tests-first contract for the shape of new project packs."""
import contextlib
import io
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import astrid_dev
import checks
from check_project_planning import LABELS
from pack_shape import new_packs, shape_errors, template_shape

ROOT = Path(__file__).resolve().parent.parent
FILES = ('plan.md', 'inputs.md', 'tasks.md')


def headings(text):
    return re.findall(r'^## (.+)$', text, re.M)


def labels(text):
    block = text.split('## Planning evidence\n', 1)[1].split('\n## ', 1)[0]
    return re.findall(r'^\*\*(.+?):\*\*', block, re.M)


class PackFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.templates = self.root / 'templates/project'
        self.templates.mkdir(parents=True)
        for name in FILES:
            shutil.copy(ROOT / 'templates/project' / name, self.templates / name)
        self.pack = self.root / 'plans/99-example'
        self.pack.parent.mkdir()
        shutil.copytree(self.templates, self.pack)

    def read(self, name):
        return (self.pack / name).read_text(encoding='utf-8')

    def write(self, name, text):
        (self.pack / name).write_text(text, encoding='utf-8')

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, text=True, stderr=subprocess.PIPE).strip()

    def init_git(self):
        self.git('init', '-q')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.com')
        self.git('add', '.')
        self.git('commit', '-qm', 'baseline')
        return self.git('rev-parse', 'HEAD')

    def errors(self):
        return shape_errors('99-example', template_shape(self.root), self.root)

    def one_error(self, name, fragment):
        result = self.errors()
        self.assertEqual(len(result), 1, result)
        self.assertTrue(result[0].startswith(f'plans/99-example/{name}: '), result)
        self.assertIn(fragment, result[0])


class TemplateTests(PackFixture):
    def test_shape_reads_template_declarations_in_order(self):
        shape = template_shape(self.root)
        # Inspect the returned declaration without prescribing a container type.
        rendered = repr(shape)
        for name in ('plan.md', 'inputs.md'):
            expected = headings((self.templates / name).read_text(encoding='utf-8'))
            self.assertEqual(len(expected), 5 if name == 'plan.md' else 4)
            positions = [rendered.index(value) for value in expected]
            self.assertEqual(positions, sorted(positions))
        evidence = labels((self.templates / 'inputs.md').read_text(encoding='utf-8'))
        self.assertEqual(len(evidence), 7)
        self.assertEqual([rendered.index(x) for x in evidence], sorted(rendered.index(x) for x in evidence))
        table = next(line for line in (self.templates / 'tasks.md').read_text(encoding='utf-8').splitlines() if line.startswith('|'))
        cells = [cell.strip() for cell in table.strip('|').split('|')]
        self.assertEqual(len(cells), 6)
        self.assertEqual([rendered.index(x) for x in cells], sorted(rendered.index(x) for x in cells))
        before = shape
        path = self.templates / 'plan.md'
        path.write_text(path.read_text(encoding='utf-8').replace('## Completion', '## Changed declaration'), encoding='utf-8')
        self.assertNotEqual(before, template_shape(self.root))

    def test_older_labels_are_all_in_the_template(self):
        evidence = labels((self.templates / 'inputs.md').read_text(encoding='utf-8'))
        self.assertEqual(len(set(evidence) - set(LABELS)), 2)
        self.assertTrue(set(LABELS) <= set(evidence))

    def test_unchanged_template_and_extra_headings_and_labels(self):
        self.assertEqual(self.errors(), [])
        self.write('plan.md', self.read('plan.md').replace('## Completion', '## Extra\n\nExtra text.\n\n## Completion'))
        self.write('inputs.md', self.read('inputs.md').replace('## Owner decisions', '**Extra label:** text\n\n## Extra section\n\nText\n\n## Owner decisions'))
        self.assertEqual(self.errors(), [])

    def test_missing_heading(self):
        heading = headings(self.read('plan.md'))[-1]
        self.write('plan.md', self.read('plan.md').replace('## ' + heading, 'Removed heading'))
        self.one_error('plan.md', heading)

    def test_headings_out_of_order(self):
        text = self.read('plan.md')
        first, second = headings(text)[:2]
        text = text.replace('## ' + first, '## SWAP').replace('## ' + second, '## ' + first).replace('## SWAP', '## ' + second)
        self.write('plan.md', text)
        result = self.errors()
        self.assertEqual(len(result), 1, result)
        self.assertTrue(result[0].startswith('plans/99-example/plan.md: '), result)

    def test_missing_uncovered_labels(self):
        original = self.read('inputs.md')
        uncovered = set(labels(original)) - set(LABELS)
        self.assertEqual(len(uncovered), 2)
        for label in sorted(uncovered):
            with self.subTest(label=label):
                self.write('inputs.md', re.sub(r'^\*\*' + re.escape(label) + r':\*\*.*\n', '', original, flags=re.M))
                self.one_error('inputs.md', label)

    def test_older_check_owns_missing_evidence_and_its_labels(self):
        original = self.read('inputs.md')
        self.write('inputs.md', original.replace('## Planning evidence', 'Removed evidence'))
        self.assertEqual(self.errors(), [])
        for label in LABELS:
            with self.subTest(label=label):
                self.write('inputs.md', re.sub(r'^\*\*' + re.escape(label) + r':\*\*.*\n', '', original, flags=re.M))
                self.assertEqual(self.errors(), [])

    def test_missing_files_and_plan_fields_are_owned_elsewhere(self):
        for name in FILES:
            with self.subTest(name=name):
                path = self.pack / name
                text = self.read(name)
                path.unlink()
                try:
                    self.assertEqual(self.errors(), [])
                finally:
                    self.write(name, text)
        text = self.read('plan.md')
        self.write('plan.md', re.sub(r'^\*\*(Project|Goal|Status|Owner|Estimate|Waiting on):\*\*.*\n', '', text, flags=re.M))
        self.assertEqual(self.errors(), [])

    def test_different_table_header(self):
        text = self.read('tasks.md')
        self.write('tasks.md', text.replace('| Task / outcome |', '| Different |', 1))
        result = self.errors()
        self.assertEqual(len(result), 1, result)
        self.assertTrue(result[0].startswith('plans/99-example/tasks.md: '), result)

    def test_no_table(self):
        text = self.read('tasks.md')
        self.write('tasks.md', '\n'.join(line for line in text.splitlines() if not line.startswith('|')) + '\n')
        result = self.errors()
        self.assertEqual(len(result), 1, result)
        self.assertTrue(result[0].startswith('plans/99-example/tasks.md: '), result)


class NewPackTests(PackFixture):
    def test_new_packs_in_each_git_state_and_existing_edits(self):
        base = self.init_git()
        # An existing pack stays existing after a claim, status edit and new inputs.
        self.write('plan.md', self.read('plan.md').replace('**Owner:**', '**Owner:** Claimed '))
        (self.pack / 'inputs.md').unlink()
        self.git('add', '-A')
        self.write('inputs.md', 'New inputs for an old pack\n')
        for folder in ('100-committed', '101-staged', '102-untracked'):
            shutil.copytree(self.templates, self.root / 'plans' / folder)
        self.git('add', 'plans/100-committed')
        self.git('commit', '-qm', 'new pack and old edit')
        self.git('add', 'plans/101-staged')
        shutil.copytree(self.templates, self.root / 'plans/not-a-project')
        self.assertEqual(set(new_packs(base, self.root)), {'100-committed', '101-staged', '102-untracked'})

    def test_renames_are_not_new_packs(self):
        base = self.init_git()
        self.git('mv', 'plans/99-example', 'plans/98-renamed')
        self.assertEqual(set(new_packs(base, self.root)), set())
        self.git('commit', '-qm', 'rename')
        self.assertEqual(set(new_packs(base, self.root)), set())

    def test_invalid_base_raises_value_error(self):
        self.init_git()
        with self.assertRaises(ValueError):
            new_packs('revision-that-does-not-exist', self.root)


class CommandTests(PackFixture):
    def registry(self, base):
        entry = next((entry for entry in checks.REGISTRY if entry.id == 'pack-shape'), None)
        if entry is None:
            # Reach the tests-first stub until the registry entry is implemented.
            new_packs(base, self.root)
        self.assertIsNotNone(entry, 'pack-shape must be registered')
        self.assertEqual(entry.trigger, 'pr')
        return (entry,)

    def invoke(self, base):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = astrid_dev.main(['check', '--base', base, '--body-file', str(self.root / 'body')], root=self.root, registry=self.registry(base))
        return status, output.getvalue()

    def test_new_fault_is_reported_by_command(self):
        base = self.init_git()
        shutil.copytree(self.templates, self.root / 'plans/100-new')
        path = self.root / 'plans/100-new/plan.md'
        text = path.read_text(encoding='utf-8')
        heading = headings(text)[-1]
        path.write_text(text.replace('## ' + heading, 'Removed heading'), encoding='utf-8')
        status, output = self.invoke(base)
        self.assertEqual(status, 1)
        self.assertEqual(len(output.splitlines()), 1)
        self.assertIn('ERROR pack-shape: plans/100-new/plan.md: ', output)
        self.assertIn(heading, output)

    def test_no_new_pack_is_silent(self):
        base = self.init_git()
        self.write('plan.md', self.read('plan.md') + '\nAn existing pack changed.\n')
        self.assertEqual(self.invoke(base), (0, ''))


if __name__ == '__main__':
    unittest.main()
