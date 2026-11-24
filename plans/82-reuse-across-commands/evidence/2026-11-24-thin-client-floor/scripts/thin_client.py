# Plan 82 floor STUB thin client: run as `python -I -S thin_client.py MODE PROMPT SEED`.
# Imports only _socket (C) and sys; JSON is written and read by hand.
import sys, _socket
mode, prompt, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
req = '{"mode":"%s","prompt":"%s","seed":%d}\n' % (mode, prompt.replace("\\", "\\\\").replace('"', '\\"'), seed)
s = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)
s.connect("/root/plan82-floor/run/host.sock")
s.sendall(req.encode())
buf = b""
while not buf.endswith(b"\n"):
    chunk = s.recv(65536)
    if not chunk: break
    buf += chunk
s.close()
ok = b'"ok": true' in buf
i = buf.find(b'"task_id": "')
tid = buf[i + 12:i + 44].decode() if i >= 0 else "?"
sys.stdout.write(("task queued: %s\n" % tid) if ok else buf.decode())
sys.stderr.write(buf.decode())
sys.exit(0 if ok else 1)
