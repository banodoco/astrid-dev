import json
import shutil
import hashlib
import subprocess
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from runtime_attestation import attest, selected_version, verify_runtime_tree


class ListenerEvidence(unittest.TestCase):
    def test_runtime_tree_bytes_and_extra_imports(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / 'repo'
            repo.mkdir()
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            (repo / 'runtime_credentials.py').write_text('value = 1\n')
            subprocess.run(['git', '-C', str(repo), 'add', 'runtime_credentials.py'], check=True)
            subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture'], check=True)
            sha = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
            tree = Path(tmp) / 'tree'
            tree.mkdir()
            (tree / 'runtime_credentials.py').write_text('value = 1\n')
            self.assertEqual(verify_runtime_tree(repo, sha, tree)['tracked_files'], 1)
            (tree / 'extra.py').write_text('bad = True\n')
            with self.assertRaisesRegex(ValueError, 'untracked executable'):
                verify_runtime_tree(repo, sha, tree)
            (tree / 'extra.py').unlink()
            (tree / 'runtime_credentials.py').write_text('value = 2\n')
            with self.assertRaisesRegex(ValueError, 'tree mismatch'):
                verify_runtime_tree(repo, sha, tree)

    def test_installer_build_copies_match_pinned_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / 'repo'
            repo.mkdir()
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            files = {
                'runtime_protocol/__init__.py': '',
                'runtime_protocol/messages/request.py': 'kind = "request"\n',
                'astrid_runtime/__init__.py': '',
                'astrid_runtime/cli.py': 'def main(): pass\n',
            }
            for name, content in files.items():
                path = repo / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            subprocess.run(['git', '-C', str(repo), 'add', 'runtime_protocol', 'astrid_runtime'], check=True)
            subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture'], check=True)
            sha = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
            tree = Path(tmp) / 'tree'
            tree.mkdir()
            for package in ('runtime_protocol', 'astrid_runtime'):
                shutil.copytree(repo / package, tree / package)
                shutil.copytree(repo / package, tree / 'build/lib' / package)
            self.assertEqual(verify_runtime_tree(repo, sha, tree)['tracked_files'], len(files))
            copy = tree / 'build/lib/astrid_runtime/cli.py'
            copy.write_text('def main(): return 1\n')
            with self.assertRaisesRegex(ValueError, 'tree mismatch'):
                verify_runtime_tree(repo, sha, tree)
            copy.write_text(files['astrid_runtime/cli.py'])
            (tree / 'build/lib/runtime_protocol/extra.py').write_text('bad = True\n')
            with self.assertRaisesRegex(ValueError, 'untracked executable'):
                verify_runtime_tree(repo, sha, tree)

    def test_sensitive_tracked_paths_are_rejected_before_reading(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / 'repo'
            repo.mkdir()
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            (repo / '.env').write_text('fixture')
            subprocess.run(['git', '-C', str(repo), 'add', '-f', '.env'], check=True)
            subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture'], check=True)
            sha = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
            tree = Path(tmp) / 'tree'
            tree.mkdir()
            with patch('runtime_attestation.subprocess.run', wraps=subprocess.run) as run:
                with self.assertRaisesRegex(ValueError, 'sensitive Runtime path'):
                    verify_runtime_tree(repo, sha, tree)
                self.assertEqual(run.call_count, 1)

    def test_token_data_file_is_rejected_before_reading(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / 'repo'
            repo.mkdir()
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            (repo / 'access_token.json').write_text('fixture')
            subprocess.run(['git', '-C', str(repo), 'add', 'access_token.json'], check=True)
            subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture'], check=True)
            sha = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
            tree = Path(tmp) / 'tree'
            tree.mkdir()
            with patch('runtime_attestation.subprocess.run', wraps=subprocess.run) as run:
                with self.assertRaisesRegex(ValueError, 'sensitive Runtime path'):
                    verify_runtime_tree(repo, sha, tree)
                self.assertEqual(run.call_count, 1)

    def test_layered_fake_listener_requires_fresh_expected_entrypoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            selected = root / 'program' / 'versions' / 'one'
            (selected / 'py/bin').mkdir(parents=True)
            python = selected / 'py/bin/python'
            python.touch()
            (selected / 'r').mkdir()
            (selected / 'py/lib/python3.11/site-packages/runtime_protocol').mkdir(parents=True)
            manifest = {k: {'sha': 'a' * 40} for k in ('agent', 'runtime', 'vibecomfy', 'lifecycle')}
            (selected / 'manifest.json').write_text(json.dumps(manifest))
            requested = root / 'requested.json'
            requested.write_text(json.dumps(manifest))
            pointer = root / 'program' / 'current'
            pointer.write_text('one\n')
            proc = root / 'proc'
            (proc / 'net').mkdir(parents=True)
            (proc / 'net/tcp').write_text('header\n 0: 0100007F:43BC 00000000:0000 0A 0:0 0:0 0 0 0 42\n 1: 0100007F:270F 00000000:0000 0A 0:0 0:0 0 0 0 43\n')
            process = proc / '123'
            (process / 'fd').mkdir(parents=True)
            (process / 'fd/4').symlink_to('socket:[42]')
            (process / 'fd/5').symlink_to('socket:[43]')
            (process / 'exe').symlink_to(python)
            (process / 'cwd').symlink_to(selected)
            (process / 'stat').write_text('123 (runtime) ' + ' '.join(['S'] + ['0'] * 18 + ['55']))
            data = root / 'data'
            (data / 'runtime').mkdir(parents=True)
            discovery = {'pid': 123, 'process_birth_id': 'proc-start-ticks:55', 'runtime_instance_id': 'instance', 'identity': {'release': 14}, 'endpoint': 'http://127.0.0.1:9999'}
            (data / 'runtime/discovery.json').write_text(json.dumps(discovery))
            Path(str(requested) + '.source.json').write_text(json.dumps({'selected_version': str(selected), 'runtime_sha': 'a' * 40, 'requested_manifest_sha256': hashlib.sha256(requested.read_bytes()).hexdigest(), 'installed_manifest_sha256': hashlib.sha256((selected / 'manifest.json').read_bytes()).hexdigest(), 'source': {}, 'protocol': {}}))
            command = ['run', '--data-root', str(data), '--source-manifest', str(selected / 'profile.json')]
            script = 'from astrid_runtime.cli import main\nmain(' + repr(command) + ')'
            valid = ('python\0-X\0utf8\0-I\0-c\0' + script + '\0').encode()
            (process / 'cmdline').write_bytes(valid)
            health = {'runtime_instance_id': 'instance', 'identity': {'release': 14}}
            with patch.dict('os.environ', {'ASTRID_ATTEST_START_TICKS': '50'}), patch('runtime_attestation.owner_health', return_value=health):
                self.assertEqual(attest(17340, pointer, requested, proc)['pid'], 123)
                table = proc / 'net/tcp'
                original_table = table.read_text()
                table.write_text(original_table.replace('0100007F:43BC', '00000000:43BC'))
                with self.assertRaisesRegex(ValueError, 'loopback'):
                    attest(17340, pointer, requested, proc)
                table.write_text(original_table + ' 2: 0100007F:43BD 00000000:0000 0A 0:0 0:0 0 0 0 44\n')
                (process / 'fd/6').symlink_to('socket:[44]')
                with self.assertRaisesRegex(ValueError, 'another arm door'):
                    attest(17340, pointer, requested, proc)
                (process / 'fd/6').unlink()
                table.write_text(original_table)
                duplicate = proc / '124'
                (duplicate / 'fd').mkdir(parents=True)
                (duplicate / 'exe').symlink_to(python)
                (duplicate / 'cmdline').write_bytes(valid)
                with self.assertRaisesRegex(ValueError, 'exactly one Runtime process'):
                    attest(17340, pointer, requested, proc)
                (duplicate / 'cmdline').unlink()
                (duplicate / 'exe').unlink()
                (duplicate / 'fd').rmdir()
                duplicate.rmdir()
                requested.write_text(requested.read_text() + ' ')
                with self.assertRaisesRegex(ValueError, 'source verification evidence'):
                    attest(17340, pointer, requested, proc)
                requested.write_text(requested.read_text().rstrip())
                (process / 'cmdline').write_bytes(b'python\0-m\0unrelated\0start\0')
                with self.assertRaisesRegex(ValueError, 'entrypoint'):
                    attest(17340, pointer, requested, proc)
                (process / 'cmdline').write_bytes(valid)
                with patch.dict('os.environ', {'ASTRID_ATTEST_START_TICKS': '55'}):
                    with self.assertRaisesRegex(ValueError, 'predates'):
                        attest(17340, pointer, requested, proc)
                discovery['pid'] = 999
                (data / 'runtime/discovery.json').write_text(json.dumps(discovery))
                with self.assertRaisesRegex(ValueError, 'identities differ'):
                    attest(17340, pointer, requested, proc)

    def test_selected_listener_and_wrong_arm(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            selected = root / 'versions' / 'one'
            other = root / 'versions' / 'two'
            selected.mkdir(parents=True)
            other.mkdir()
            manifest = {k: {'sha': k + '-sha'} for k in ('agent', 'runtime', 'vibecomfy', 'lifecycle')}
            (selected / 'manifest.json').write_text(json.dumps(manifest))
            requested = root / 'requested.json'
            requested.write_text(json.dumps(manifest))
            exe = selected / 'runtime'
            exe.touch()
            proc = root / 'proc'
            (proc / 'net').mkdir(parents=True)
            (proc / 'net' / 'tcp').write_text('header\n 0: 0100007F:43BC 00000000:0000 0A 0:0 0:0 0 0 0 42\n')
            p = proc / '123'
            (p / 'fd').mkdir(parents=True)
            (p / 'fd' / '4').symlink_to('socket:[42]')
            (p / 'exe').symlink_to(exe)
            (p / 'cwd').symlink_to(selected)
            (p / 'stat').write_text('123 (runtime) ' + ' '.join(['S'] + ['0'] * 18 + ['55']))
            pointer = root / 'current'
            pointer.write_text('one\n')
            self.assertEqual(selected_version(pointer), selected)
            with self.assertRaisesRegex(ValueError, 'cannot securely identify'):
                attest(17340, pointer, requested, proc)
            (p / 'cwd').unlink()
            (p / 'cwd').symlink_to(other)
            with self.assertRaisesRegex(ValueError, 'inside selected version'):
                attest(17340, pointer, requested, proc)
            foreign = root / 'other-arm' / 'versions' / 'one'
            foreign.mkdir(parents=True)
            pointer.unlink()
            (root / 'versions' / 'escape').symlink_to(foreign)
            pointer.write_text('escape\n')
            with self.assertRaisesRegex(ValueError, 'direct child'):
                attest(17340, pointer, requested, proc)
            pointer.unlink()
            pointer.write_text('one\n')
            with self.assertRaisesRegex(ValueError, 'listener'):
                attest(17341, pointer, requested, proc)

if __name__ == '__main__': unittest.main()
