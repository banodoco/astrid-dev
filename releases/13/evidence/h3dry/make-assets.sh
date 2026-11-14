#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/assets"
ffmpeg -hide_banner -loglevel error -f lavfi -i testsrc2=size=1024x576:rate=24:d=3 -f lavfi -i sine=frequency=440:d=3 -t 3 -shortest -c:v libx264 -pix_fmt yuv420p -c:a aac bike.mp4
ffmpeg -hide_banner -loglevel error -f lavfi -i testsrc2=size=1024x576:rate=24:d=0.05 -frames:v 1 -threads 1 subject-bike.png
ffmpeg -hide_banner -loglevel error -loop 1 -framerate 24 -i subject-bike.png -f lavfi -i anullsrc=r=44100:cl=stereo:d=3 -t 3 -r 24 -c:v libx264 -crf 0 -pix_fmt yuv444p -c:a aac -shortest bike-still.mp4
ffmpeg -hide_banner -loglevel error -f lavfi -i color=c=black:s=1024x576:r=24:d=0.05 -vf 'drawbox=x=384:y=144:w=256:h=288:color=white:t=fill' -frames:v 1 -threads 1 frame-mask.png
