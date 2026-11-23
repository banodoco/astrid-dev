"""Record WAL/DB file-stat changes on the isolated4 realm (read-only stat, no DB connection)."""
import glob, os, sys, time

DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 1800
db = glob.glob('/root/codex/le4/isolated4/data/runtime/realms/*/realm.sqlite3')[0]
w = db + '-wal'
t0 = time.time()
last = None
print('watch', db, 'start', time.strftime('%H:%M:%S'), flush=True)
while time.time() - t0 < DUR:
    try:
        s = os.stat(w)
        key = (s.st_mtime_ns, s.st_size)
    except FileNotFoundError:
        key = None
    if key != last:
        if last is not None and key is not None:
            print(time.strftime('%H:%M:%S'), 'WAL changed mtime=%s size=%s' % (
                time.strftime('%H:%M:%S', time.localtime(key[0] / 1e9)), key[1]), flush=True)
        last = key
    time.sleep(0.5)
print('watch end', time.strftime('%H:%M:%S'), flush=True)
