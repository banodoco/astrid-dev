#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
# Real generated T1 source is copied byte-for-byte; never remux/re-encode it.
python3 evidence/measure.py
ffmpeg -y -hide_banner -loglevel error -loop 1 -framerate 24 -i assets/subject-bike.png -f lavfi -i anullsrc=r=44100:cl=stereo:d=3 -t 3 -r 24 -c:v libx264 -crf 0 -pix_fmt yuv444p -c:a aac -threads 1 -shortest assets/bike-still.mp4
python3 - <<'PY'
from PIL import Image
import numpy as np
m=np.zeros((576,1024),dtype=np.uint8)
m[190:526,290:768]=255
Image.fromarray(m).save('assets/frame-mask.png')
PY
