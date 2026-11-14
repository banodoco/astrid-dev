#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
TMP_TEST=$(mktemp -d)
trap 'rm -rf "$TMP_TEST"' EXIT
# Decode to RGB before alteration, then encode losslessly as RGB FFV1: no YUV roundtrip changes the protected pixels.
make_copy() {
 ffmpeg -v error -i assets/bike.mp4 -t 3 -vf "scale=iw:ih:flags=lanczos+accurate_rnd+full_chroma_int,format=rgb24,$1" -an -c:v ffv1 -pix_fmt bgr0 -threads 1 "$2"
}
make_copy "null" "$TMP_TEST/accurate.mkv"
make_copy "drawbox=x=0:y=0:w=iw:h=ih:color=white@1:t=fill:enable='gte(n,36)'" "$TMP_TEST/tail.mkv"
make_copy "drawbox=x=384:y=144:w=256:h=288:color=white@1:t=fill" "$TMP_TEST/inside.mkv"
make_copy "drawbox=x=0:y=0:w=64:h=64:color=white@1:t=fill" "$TMP_TEST/outside.mkv"
check() {
 local expected=$1; shift
 printf 'COMMAND: python3 check_edit.py'; printf ' %q' "$@"; printf '\n'
 set +e
 python3 check_edit.py "$@"
 local actual=$?
 set -e
 printf 'expected=%s actual=%s\n' "$expected" "$actual"
 test "$actual" = "$expected"
}
check 0 assets/bike.mp4 assets/bike.mp4 --kept 0-71
check 0 assets/bike.mp4 "$TMP_TEST/accurate.mkv" --kept 0-71 --mask assets/frame-mask.png --outside-only
check 1 assets/bike.mp4 "$TMP_TEST/accurate.mkv" --kept 0-71 --mask assets/frame-mask.png --outside-only --decode-default
# Measure outside-mask maximum channel differences across all 72 frames.
python3 - "$TMP_TEST/accurate.mkv" <<'PYCODE'
import sys
import numpy as np
from check_edit import decoder, frame, probe

source, candidate = 'assets/bike.mp4', sys.argv[1]
for default in (True, False):
    procs = [decoder(path, probe(path), default) for path in (source, candidate)]
    maximum = count = 0
    while True:
        a, b = (frame(proc) for proc in procs)
        if a is None or b is None:
            assert a is None and b is None
            break
        diff = np.abs(a.astype(np.int16) - b.astype(np.int16))
        diff[144:432, 384:640] = 0
        maximum = max(maximum, int(diff.max()))
        count += 1
    for proc in procs:
        proc.stdout.close()
        assert proc.wait() == 0
    print(f'outside_max_diff decode={"default" if default else "accurate"} max={maximum} frames={count}')
    assert count == 72 and (maximum > 0 if default else maximum == 0)
PYCODE
check 0 assets/bike.mp4 "$TMP_TEST/tail.mkv" --kept 0-35 --changed 36-71
check 1 assets/bike.mp4 "$TMP_TEST/tail.mkv" --kept 0-71
check 0 assets/bike.mp4 "$TMP_TEST/inside.mkv" --kept 0-71 --mask assets/frame-mask.png --outside-only --require-change
check 1 assets/bike.mp4 "$TMP_TEST/outside.mkv" --kept 0-71 --mask assets/frame-mask.png --outside-only
printf 'ALL SELF-TEST EXPECTATIONS PASSED\n'
