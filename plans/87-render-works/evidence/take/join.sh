#!/bin/bash
# Join four product-rendered ranges into one file: video stream-copied, audio decoded, trimmed to exact length, joined, encoded once.
set -eu
S=~/take
F=$HOME/astrid-release/release-14-plan-69/program/versions/5bf20639e293/tools/ffmpeg
OUT="$HOME/Desktop/Almost Ready - trial v2 - 2026-11-22.mp4"
[ -e "$OUT" ] && OUT="$HOME/Desktop/Almost Ready - trial v2 - 2026-11-22 ($(date +%H%M)).mp4"
cd $S
LEN=(50 50 50 46.566667)
: > concat.txt
for i in 0 1 2 3; do
  $F/ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames,r_frame_rate -of csv=p=0 part$i.mp4 | sed "s/^/part$i frames,rate: /"
  $F/ffprobe -v error -show_entries format=duration -of csv=p=0 part$i.mp4 | sed "s/^/part$i duration: /"
  # audio: decode, force exact sample count (pad with silence then trim), 48 kHz stereo
  $F/ffmpeg -v error -y -i part$i.mp4 -vn -af "apad,atrim=end=${LEN[$i]},asetpts=N/SR/TB" -ar 48000 -ac 2 -c:a pcm_s24le a$i.wav
  echo "file 'part$i.mp4'" >> concat.txt
done
$F/ffmpeg -v error -y -i a0.wav -i a1.wav -i a2.wav -i a3.wav -filter_complex "[0:a][1:a][2:a][3:a]concat=n=4:v=0:a=1[a]" -map "[a]" -c:a pcm_s24le audio-joined.wav
$F/ffmpeg -v error -y -f concat -safe 0 -i concat.txt -an -c:v copy video-joined.mp4
$F/ffmpeg -v error -y -i video-joined.mp4 -i audio-joined.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -movflags +faststart "$OUT"
$F/ffprobe -v error -show_entries format=duration,size,bit_rate:stream=codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels -of compact "$OUT"
echo "OUT=$OUT"
