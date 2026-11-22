#!/usr/bin/env python3
"""Record constrained Linux listener/process/manifest evidence, not socket contact."""
import json
import hashlib
import ast
import urllib.parse
import urllib.request
import os
import re
import subprocess
from pathlib import Path
import sys


def beneath(path, root):
    try:
        Path(path).relative_to(root)
        return True
    except ValueError:
        return False


def selected_version(pointer):
    pointer = Path(pointer)
    versions_path = pointer.parent.resolve(strict=True) / 'versions'
    versions = versions_path.resolve(strict=True)
    if versions != versions_path:
        raise ValueError('installation versions directory must not redirect elsewhere')
    if not pointer.is_file() or pointer.is_symlink():
        raise ValueError('current must be a regular version pointer file')
    version = pointer.read_text().strip()
    if not re.fullmatch(r'[A-Za-z0-9._-]+', version) or version in ('.', '..'):
        raise ValueError('invalid current version pointer')
    current = (versions / version).resolve(strict=True)
    if not current.is_dir() or current.parent != versions:
        raise ValueError('selected version must be a direct child of this installation versions directory')
    return current


def verify_runtime_tree(repo, sha, tree, prefix=""):
    """Compare Git-tracked bytes, links and modes and refuse extra Python imports."""
    if not re.fullmatch(r'[0-9a-f]{40}', sha):
        raise ValueError('Runtime manifest requires a full Git object ID')
    tree = Path(tree).resolve(strict=True)
    listing = subprocess.run(['git', '-C', str(repo), 'ls-tree', '-rz', '--full-tree', sha, '--', prefix] if prefix else ['git', '-C', str(repo), 'ls-tree', '-rz', '--full-tree', sha],
                             check=True, capture_output=True).stdout
    if not listing:
        raise ValueError('empty Runtime Git tree')
    tracked = set()
    for item in listing.split(b'\0'):
        if not item:
            continue
        meta, name = item.split(b'\t', 1)
        mode, kind, oid = meta.decode('ascii').split()
        if kind != 'blob' or mode not in ('100644', '100755', '120000'):
            raise ValueError('unsupported Runtime Git tree entry')
        relative = os.fsdecode(name)
        if prefix:
            if not relative.startswith(prefix + '/'):
                raise ValueError('invalid Git subtree entry')
            relative = relative[len(prefix) + 1:]
        parts = Path(relative).parts
        lower_parts = [part.lower() for part in parts]
        env_file = any(part == '.env' or part.startswith('.env.') for part in lower_parts)
        sensitive_directory = any('credential' in part or 'token' in part for part in lower_parts[:-1])
        sensitive_name = 'credential' in lower_parts[-1] or 'token' in lower_parts[-1]
        source_file = lower_parts[-1].endswith('.py')
        if env_file or sensitive_directory or (sensitive_name and not source_file):
            raise ValueError(f'sensitive Runtime path cannot be inspected: {relative}')
        path = tree / relative
        parent = tree
        for part in parts[:-1]:
            parent = parent / part
            if parent.is_symlink():
                raise ValueError(f'Runtime path traverses a symlink: {relative}')
        tracked.add(relative)
        expected = subprocess.run(['git', '-C', str(repo), 'cat-file', 'blob', oid],
                                  check=True, capture_output=True).stdout
        if mode == '120000':
            if not path.is_symlink() or os.fsencode(os.readlink(path)) != expected:
                raise ValueError(f'Runtime tree mismatch: {relative}')
        elif path.is_symlink() or not path.is_file() or path.read_bytes() != expected or bool(path.stat().st_mode & 0o111) != (mode == '100755'):
            raise ValueError(f'Runtime tree mismatch: {relative}')
    for path in tree.rglob('*'):
        if path.is_symlink() and path.is_dir():
            raise ValueError(f'unverified Runtime directory symlink: {path}')
        if path.is_file() and path.suffix in ('.py', '.pyc', '.so', '.pth') and str(path.relative_to(tree)) not in tracked:
            raise ValueError(f'untracked executable Runtime import: {path}')
    return {'git_commit': sha, 'tracked_files': len(tracked)}


def source_evidence(pointer, manifest):
    current = selected_version(pointer)
    wanted = json.loads(Path(manifest).read_text())
    installed = json.loads((current / 'manifest.json').read_text())
    sha = wanted['runtime']['sha']
    if installed['runtime']['sha'] != sha:
        raise ValueError('Runtime manifest mismatch')
    packages = list((current / 'py/lib').glob('python*/site-packages/runtime_protocol'))
    if len(packages) != 1:
        raise ValueError('expected exactly one installed Runtime protocol package')
    repo = os.environ['ASTRID_RUNTIME_SOURCE_REPO']
    return {'selected_version': str(current), 'runtime_sha': sha,
            'requested_manifest_sha256': hashlib.sha256(Path(manifest).read_bytes()).hexdigest(),
            'installed_manifest_sha256': hashlib.sha256((current / 'manifest.json').read_bytes()).hexdigest(),
            'source': verify_runtime_tree(repo, sha, current / 'r'),
            'protocol': verify_runtime_tree(repo, sha, packages[0], 'runtime_protocol')}


def owner_health(endpoint):
    parsed = urllib.parse.urlsplit(endpoint)
    if parsed.scheme != 'http' or parsed.hostname not in ('127.0.0.1', '::1') or not parsed.port:
        raise ValueError('owner endpoint must be loopback HTTP')
    req = urllib.request.Request(endpoint.rstrip('/') + '/v1/health', headers={'X-Astrid-Owner-Identity': '1'})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(req, timeout=3) as response:
        return json.loads(response.read(1024 * 1024))


def service_arguments(args):
    if len(args) != 6 or args[1:5] != ['-X', 'utf8', '-I', '-c']:
        raise ValueError('listener does not have the expected Runtime entrypoint')
    code = ast.parse(args[5])
    imports = [i for i, node in enumerate(code.body) if isinstance(node, ast.ImportFrom)
               and node.module == 'astrid_runtime.cli' and node.level == 0
               and len(node.names) == 1 and node.names[0].name == 'main' and node.names[0].asname is None]
    if len(imports) != 1:
        raise ValueError('listener does not have the expected Runtime entrypoint')
    tail = code.body[imports[0] + 1:]
    # The installer emits either a literal call or an _args assignment followed
    # by its managed-launch compatibility conditional. The small direct call
    # is also accepted by the original process fixture.
    arguments = None
    if len(tail) == 1 and isinstance(tail[0], ast.Expr):
        expr = tail[0].value
        if isinstance(expr, ast.Call) and isinstance(expr.func, ast.Attribute) and isinstance(expr.func.value, ast.Name) and expr.func.value.id == 'sys' and expr.func.attr == 'exit' and len(expr.args) == 1 and not expr.keywords:
            expr = expr.args[0]
        if isinstance(expr, ast.Call) and isinstance(expr.func, ast.Name) and expr.func.id == 'main' and len(expr.args) == 1 and not expr.keywords:
            try:
                arguments = ast.literal_eval(expr.args[0])
            except (ValueError, TypeError):
                pass
    elif len(tail) == 4:
        template = ast.parse("import inspect\n_args=[]\n_context={}\nsys.exit(main(_args, managed_launch=_context) if 'managed_launch' in inspect.signature(main).parameters else main(_args))").body
        if (isinstance(tail[1], ast.Assign) and isinstance(tail[2], ast.Assign)
                and ast.dump(tail[0]) == ast.dump(template[0])
                and ast.dump(tail[3]) == ast.dump(template[3])
                and len(tail[1].targets) == len(tail[2].targets) == 1
                and isinstance(tail[1].targets[0], ast.Name) and tail[1].targets[0].id == '_args'
                and isinstance(tail[2].targets[0], ast.Name) and tail[2].targets[0].id == '_context'):
            try:
                arguments = ast.literal_eval(tail[1].value)
                context = ast.literal_eval(tail[2].value)
                if (not isinstance(context, dict) or set(context) != {'profile', 'data_root'}
                        or not isinstance(arguments, list)
                        or not any(arguments[i:i+2] == ['--source-manifest', context['profile']] for i in range(len(arguments)-1))
                        or not any(arguments[i:i+2] == ['--data-root', context['data_root']] for i in range(len(arguments)-1))):
                    arguments = None
            except (ValueError, TypeError):
                arguments = None
    if not isinstance(arguments, list) or not all(isinstance(x, str) for x in arguments):
        raise ValueError('listener does not have the expected Runtime entrypoint')
    return arguments


def attest(port, current, requested, proc_root=Path('/proc')):
    current = selected_version(current)
    installed = json.loads((current / 'manifest.json').read_text())
    wanted = json.loads(Path(requested).read_text())
    shas = {}
    for name in ('agent', 'runtime', 'vibecomfy', 'lifecycle'):
        sha = installed[name]['sha']
        if not isinstance(sha, str) or not sha or sha != wanted[name]['sha']:
            raise ValueError(f'{name} manifest mismatch')
        shas[name] = sha
    inodes = set()
    for table in ('tcp', 'tcp6'):
        path = proc_root / 'net' / table
        if not path.exists():
            continue
        for line in path.read_text().splitlines()[1:]:
            fields = line.split()
            if len(fields) < 10 or fields[3] != '0A':
                continue
            address, encoded_port = fields[1].split(':')
            if int(encoded_port, 16) == port:
                inodes.add((fields[9], table, address))
    if len(inodes) != 1:
        raise ValueError('expected exactly one listener on the door port')
    inode, table, address = next(iter(inodes))
    if (table, address.upper()) not in (('tcp', '0100007F'), ('tcp6', '00000000000000000000000001000000')):
        raise ValueError('door listener must bind loopback')
    owners = []
    for proc in proc_root.iterdir():
        if not proc.name.isdigit():
            continue
        try:
            if any(os.readlink(fd) == f'socket:[{inode}]' for fd in (proc / 'fd').iterdir()):
                owners.append(proc)
        except (OSError, PermissionError):
            raise ValueError(f'cannot inspect process {proc.name} descriptors')
    if len(owners) != 1:
        raise ValueError('listener must have exactly one visible process owner')
    proc = owners[0]
    exe = Path(os.readlink(proc / 'exe')).resolve(strict=True)
    cwd = Path(os.readlink(proc / 'cwd')).resolve(strict=True)
    if beneath(cwd, current.parent) and not beneath(cwd, current):
        raise ValueError('listener cwd must be inside selected version when under versions')
    stat = (proc / 'stat').read_text()
    start = int(stat[stat.rfind(')') + 2:].split()[19])
    try:
        python = (current / 'py/bin/python').resolve(strict=True)
    except OSError as exc:
        raise ValueError('cannot securely identify Runtime entrypoint from listener process') from exc
    if exe != python:
        raise ValueError('listener is not using the selected Python interpreter')
    args = [os.fsdecode(x) for x in (proc / 'cmdline').read_bytes().split(b'\0') if x]
    arguments = service_arguments(args)
    profile = str(current / 'profile.json')
    program = current.parent.parent
    if not program.name.startswith('program'):
        raise ValueError('unexpected installation root')
    data = program.parent / ('data' + program.name[len('program'):])
    if not arguments or arguments[0] != 'run' or not any(arguments[i:i+2] == ['--source-manifest', profile] for i in range(len(arguments)-1)) or not any(arguments[i:i+2] == ['--data-root', str(data)] for i in range(len(arguments)-1)):
        raise ValueError('listener does not have the expected Runtime profile and data root')
    # Each fixed arm port must have its own listener; this owner must not
    # also hold a listener on another arm's port.
    other_inodes = set()
    for socket_table in ('tcp', 'tcp6'):
        path = proc_root / 'net' / socket_table
        if path.exists():
            for line in path.read_text().splitlines()[1:]:
                fields = line.split()
                if len(fields) >= 10 and fields[3] == '0A' and int(fields[1].split(':')[1], 16) in ({17340, 17341, 17342} - {port}):
                    other_inodes.add(fields[9])
    owner_fds = {os.readlink(fd) for fd in (proc / 'fd').iterdir()}
    if any(f'socket:[{other}]' in owner_fds for other in other_inodes):
        raise ValueError('Runtime owner also holds another arm door')
    matching = []
    for candidate in proc_root.iterdir():
        if not candidate.name.isdigit():
            continue
        try:
            if Path(os.readlink(candidate / 'exe')).resolve(strict=True) != python:
                continue
            candidate_args = [os.fsdecode(x) for x in (candidate / 'cmdline').read_bytes().split(b'\0') if x]
            candidate_service = service_arguments(candidate_args)
            if any(candidate_service[i:i+2] == ['--source-manifest', profile] for i in range(len(candidate_service)-1)) and any(candidate_service[i:i+2] == ['--data-root', str(data)] for i in range(len(candidate_service)-1)):
                matching.append(candidate.name)
        except ValueError:
            continue
        except FileNotFoundError:
            # A process can exit while /proc is scanned.
            continue
        except OSError as exc:
            raise ValueError(f'cannot inspect process {candidate.name} identity') from exc
    if matching != [proc.name]:
        raise ValueError('expected exactly one Runtime process for this arm')
    baseline = int(os.environ['ASTRID_ATTEST_START_TICKS'])
    if start <= baseline:
        raise ValueError('listener predates this wrapper invocation')
    evidence = json.loads(Path(str(requested) + '.source.json').read_text())
    if (evidence['selected_version'] != str(current) or evidence['runtime_sha'] != shas['runtime']
            or evidence['requested_manifest_sha256'] != hashlib.sha256(Path(requested).read_bytes()).hexdigest()
            or evidence['installed_manifest_sha256'] != hashlib.sha256((current / 'manifest.json').read_bytes()).hexdigest()):
        raise ValueError('source verification evidence does not match selected version')
    discovery = json.loads((data / 'runtime/discovery.json').read_text())
    birth = discovery['process_birth_id']
    if discovery['pid'] != int(proc.name) or not re.fullmatch(r'proc-start-ticks:' + str(start) + r'(?:;.*)?', birth):
        raise ValueError('listener and owner discovery process identities differ')
    if ';boot:' in birth:
        boot = (proc_root / 'sys/kernel/random/boot_id').read_text().strip()
        if ';boot:' + boot not in birth.split(';pidns:')[0]:
            raise ValueError('owner boot identity differs')
    if ';pidns:' in birth:
        namespace = (proc / 'ns/pid').stat().st_ino
        if not birth.endswith(';pidns:' + str(namespace)):
            raise ValueError('owner PID namespace identity differs')
    endpoint_port = urllib.parse.urlsplit(discovery['endpoint']).port
    health_sockets = set()
    for table in ('tcp', 'tcp6'):
        path = proc_root / 'net' / table
        if path.exists():
            for line in path.read_text().splitlines()[1:]:
                fields = line.split()
                if len(fields) >= 10 and fields[3] == '0A' and int(fields[1].split(':')[1], 16) == endpoint_port:
                    health_sockets.add(fields[9])
    owner_sockets = {os.readlink(fd) for fd in (proc / 'fd').iterdir()}
    if len(health_sockets) != 1 or f'socket:[{next(iter(health_sockets))}]' not in owner_sockets:
        raise ValueError('owner health listener is not held by the door owner')
    health = owner_health(discovery['endpoint'])
    instance = discovery['runtime_instance_id']
    if not isinstance(instance, str) or not instance or health.get('runtime_instance_id') != instance or health.get('identity') != discovery.get('identity'):
        raise ValueError('owner health identity differs from discovery')
    source, protocol = evidence['source'], evidence['protocol']
    return {'port': port, 'address_hex': address, 'socket_table': table, 'socket_inode': inode,
            'pid': int(proc.name), 'start_ticks': start, 'exe': str(exe), 'cwd': str(cwd),
            'selected_version': str(current), 'manifest_shas': shas, 'source': source,
            'protocol': protocol, 'runtime_instance_id': instance, 'owner_endpoint': discovery['endpoint'], 'scope': 'layered process and source evidence; does not prove per-command contact or immutable source'}



def main(args):
    if len(args) == 2 and args[0] == '--selected':
        print(selected_version(args[1]))
        return
    if len(args) == 3 and args[0] == '--source':
        result = source_evidence(args[1], args[2])
        with Path(args[2] + '.source.json').open('x') as f:
            json.dump(result, f, indent=2)
            f.write('\n')
        return
    if len(args) != 4:
        raise ValueError('usage: runtime_attestation.py PORT CURRENT REQUESTED_MANIFEST OUTPUT')
    port = int(args[0])
    if not 1 <= port <= 65535:
        raise ValueError('invalid port')
    result = attest(port, args[1], args[2])
    output = Path(args[3])
    with output.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except (OSError, ValueError, KeyError, TypeError, IndexError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        sys.exit(f'FAIL: Runtime listener attestation: {exc}')
