#!/bin/sh
# 紹介動画を作り直す: 自動プレイの録画 → BGMの書き出し → 合成
set -e
cd "$(dirname "$0")"

URL="jyarumen-ui.github.io/arena-card-tactics"
FONT="C\\:/Windows/Fonts/arialbd.ttf"

echo "■ 1/3 自動プレイを録画"
node record.js

echo "■ 2/3 BGMを書き出し"
node render-audio.js

echo "■ 3/3 動画に合成"
ffmpeg -hide_banner -loglevel error \
  -f concat -safe 0 -i frames/list.txt -i bgm.wav \
  -vf "fps=30,scale=1280:720:flags=lanczos,\
drawtext=fontfile='$FONT':text='$URL':x=w-tw-18:y=h-th-14:fontsize=17:fontcolor=white@0.72:\
box=1:boxcolor=black@0.42:boxborderw=7,format=yuv420p" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 160k -ar 48000 -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
  -shortest -movflags +faststart -y promo.mp4

ls -la promo.mp4
ffprobe -hide_banner promo.mp4 2>&1 | grep -E "Duration|Stream"
