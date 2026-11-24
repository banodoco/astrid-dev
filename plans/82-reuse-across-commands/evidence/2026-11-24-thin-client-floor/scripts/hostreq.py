import json, socket, sys
def call(req, sock="/root/plan82-floor/run/host.sock"):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); s.connect(sock)
    f = s.makefile("rwb"); f.write(json.dumps(req).encode() + b"\n"); f.flush()
    out = json.loads(f.readline()); s.close(); return out
if __name__ == "__main__":
    print(json.dumps(call(json.loads(sys.argv[1])), default=str)[:int(sys.argv[2]) if len(sys.argv) > 2 else 4000])
