#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
TMP_TEST=$(mktemp -d)
trap 'rm -rf "$TMP_TEST"' EXIT
# Decode to RGB before alteration, then encode losslessly as RGB FFV1: no YUV roundtrip changes the protected pixels.
make_copy() {
 ffmpeg -v error -i assets/bike.mp4 -t 3 -vf "format=rgb24,$1" -an -c:v ffv1 -pix_fmt bgr0 -threads 1 "$2"
}
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
check 0 assets/bike.mp4 "$TMP_TEST/tail.mkv" --kept 0-35 --changed 36-71
check 1 assets/bike.mp4 "$TMP_TEST/tail.mkv" --kept 0-71
check 0 assets/bike.mp4 "$TMP_TEST/inside.mkv" --kept 0-71 --mask assets/frame-mask.png --outside-only --require-change
check 1 assets/bike.mp4 "$TMP_TEST/outside.mkv" --kept 0-71 --mask assets/frame-mask.png --outside-only
printf 'ALL SELF-TEST EXPECTATIONS PASSED\n'
