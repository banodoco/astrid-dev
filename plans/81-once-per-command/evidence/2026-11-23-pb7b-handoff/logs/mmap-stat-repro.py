import mmap, os, tempfile, time
with tempfile.TemporaryFile() as f:
    f.write(b'abcdefgh'); f.flush()
    with mmap.mmap(f.fileno(), 8) as m:
        m[0] = 65
        s = os.fstat(f.fileno())
        time.sleep(.02)
        m[0] = 66
        t = os.fstat(f.fileno())
        print("size, mtime and ctime unchanged between distinct content versions:", (s.st_size,s.st_mtime_ns,s.st_ctime_ns) == (t.st_size,t.st_mtime_ns,t.st_ctime_ns))
