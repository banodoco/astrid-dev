#!/bin/bash
# usage: join-n.sh N OUTFILE  : join part0..part(N-1); video stream-copied, audio decoded/trimmed/joined/encoded once
set -eu
N=$1; OUT="$2"
S=~/take
F=$HOME/astrid-release/release-14-plan-69/program/versions/5bf20639e293/tools/ffmpeg
cd $S
LEN=(50 50 50 46.566667)
: > concat-$N.txt; INS=""; FC=""
for i in $(seq 0 $((N-1))); do
  echo "part$i: frames $($F/ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 part$i.mp4), duration $($F/ffprobe -v error -show_entries format=duration -of csv=p=0 part$i.mp4)"
  $F/ffmpeg -v error -y -i part$i.mp4 -vn -af "apad,atrim=end=${LEN[$i]},asetpts=N/SR/TB" -ar 48000 -ac 2 -c:a pcm_s24le a$i.wav
  echo "file 'part$i.mp4'" >> concat-$N.txt; INS="$INS -i a$i.wav"; FC="$FC[$i:a]"
done
$F/ffmpeg -v error -y $INS -filter_complex "${FC}concat=n=$N:v=0:a=1[a]" -map "[a]" -c:a pcm_s24le audio-joined-$N.wav
$F/ffmpeg -v error -y -f concat -safe 0 -i concat-$N.txt -an -c:v copy video-joined-$N.mp4
$F/ffmpeg -v error -y -i video-joined-$N.mp4 -i audio-joined-$N.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -movflags +faststart "$OUT"
$F/ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,nb_frames -of compact "$OUT"
