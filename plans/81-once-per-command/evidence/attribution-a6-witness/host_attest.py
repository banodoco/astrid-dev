"""Untimed witness of real consume.py execution, enabled only for attestation."""
import hashlib
import json
import os
from pathlib import Path
import sys
import threading


def install(destination):
    # Runner creates its output directory after interpreter startup. Skip that
    # early process; subsequently launched fixture processes see the directory.
    if not destination or not Path(destination).parent.is_dir():
        return
    recorded = False
    def profile(frame, event, arg):
        nonlocal recorded
        if recorded or event != 'call':
            return
        filename = Path(frame.f_code.co_filename).resolve()
        if filename.as_posix().endswith('/vibecomfy/porting/object_info/consume.py'):
            recorded = True
            lineage = []
            pid = os.getpid()
            while pid > 1 and len(lineage) < 64:
                try:
                    stat = Path(f'/proc/{pid}/stat').read_text()
                    tail = stat[stat.rfind(')') + 2:].split()
                    cmdline = Path(f'/proc/{pid}/cmdline').read_bytes().replace(b'\0', b' ').decode(errors='replace')
                    lineage.append({'pid': pid, 'ppid': int(tail[1]), 'start_ticks': tail[19], 'cmdline': cmdline})
                    pid = int(tail[1])
                except (OSError, ValueError, IndexError):
                    break
            record = {'pid': os.getpid(), 'executable': sys.executable, 'prefix': sys.prefix,
                      'interpreter_sha256': hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(), 'file': str(filename),
                      'sha256': hashlib.sha256(filename.read_bytes()).hexdigest(), 'lineage': lineage}
            fd = os.open(destination, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
            try:
                os.write(fd, (json.dumps(record) + '\n').encode())
            finally:
                os.close(fd)
            sys.setprofile(None)
            threading.setprofile(None)
    threading.setprofile(profile)
    sys.setprofile(profile)
