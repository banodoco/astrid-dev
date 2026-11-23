#!/usr/bin/env python3
"""Conservative Linux process identity and descendant cleanup helpers."""
import os
from pathlib import Path
import signal
import sys


def read_process(pid):
    """Return (ppid, starttime, executable, argv), or None if unavailable."""
    try:
        base = Path('/proc') / str(pid)
        stat = (base / 'stat').read_text()
        fields = stat[stat.rfind(')') + 2:].split()
        ppid, start = int(fields[1]), int(fields[19])
        try:
            exe = os.readlink(base / 'exe')
        except OSError:
            exe = ''
        argv = (base / 'cmdline').read_bytes().split(b'\0')
        return ppid, start, exe, tuple(os.fsdecode(a) for a in argv if a)
    except (OSError, ValueError, IndexError):
        return None


def beneath(path, roots):
    if not os.path.isabs(path):
        return False
    path = os.path.realpath(path)
    return any(path == root or path.startswith(root + os.sep) for root in roots)


def program_matches(proc, roots):
    """Match only the kernel-reported executable inside an eligible root."""
    return beneath(proc[2], roots)


def matching_chain(snapshot, pid, ancestor, ancestor_start, roots):
    """Return identity chain if PID is an eligible descendant, otherwise None."""
    proc = snapshot.get(pid)
    if not proc or pid == ancestor or not program_matches(proc, roots):
        return None
    chain, seen = [], set()
    while pid not in seen:
        seen.add(pid)
        proc = snapshot.get(pid)
        if proc is None:
            return None
        chain.append((pid, proc[1]))
        if pid == ancestor:
            return chain if proc[1] == ancestor_start else None
        pid = proc[0]
    return None


def chain_current(chain, snapshot, roots):
    for pid, start in chain:
        now = read_process(pid)
        old = snapshot[pid]
        if not now or now[1] != start or now[0] != old[0]:
            return False
        if pid == chain[0][0] and not program_matches(now, roots):
            return False
    return True


def signal_identity(pid, start, check=lambda: True):
    """Open a pidfd and recheck identity before signaling; fail closed."""
    try:
        fd = os.pidfd_open(pid)
    except (AttributeError, OSError):
        return False
    try:
        current = read_process(pid)
        if not current or current[1] != start or not check():
            return False
        signal.pidfd_send_signal(fd, signal.SIGTERM)
        return True
    except (AttributeError, OSError):
        return False
    finally:
        os.close(fd)


def main(args):
    command = args[0]
    if command == 'start' or (command == 'capture' and len(args) == 2):
        p = read_process(int(args[1]))
        if not p:
            return 1
        print(p[1])
    elif command == 'capture':
        pid, parent, parent_start = map(int, args[1:4])
        p, owner = read_process(pid), read_process(parent)
        if not p or p[0] != parent or not owner or owner[1] != parent_start:
            return 1
        print(p[1])
    elif command == 'signal':
        return 0 if signal_identity(int(args[1]), int(args[2])) else 1
    elif command == 'descendants':
        ancestor, ancestor_start = map(int, args[1:3])
        roots = tuple(os.path.realpath(p) for p in args[3:])
        snapshot = {}
        for name in os.listdir('/proc'):
            if name.isdigit():
                p = read_process(int(name))
                if p:
                    snapshot[int(name)] = p
        for pid in snapshot:
            if pid == os.getpid():
                continue
            chain = matching_chain(snapshot, pid, ancestor, ancestor_start, roots)
            if chain:
                signal_identity(pid, chain[0][1], lambda: chain_current(chain, snapshot, roots))
    else:
        return 2
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except (IndexError, ValueError):
        sys.exit(2)
