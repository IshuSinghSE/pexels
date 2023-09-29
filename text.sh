#!/bin/bash
f="input 1.mp4"
t="/tmp/text.png"
o="/tmp/output.mp4"
RAD=20

# create pic with text
ffmpeg -lavfi "color=black@0:size=1280x720,drawtext=text='test':box=1:boxborderw=30:boxcolor=blue:borderw=5:bordercolor=red:fontsize=h/2:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" -frames 1 "text.png" -y

# imagemagick trim text
mogrify -trim "$t"

# rounded corners from https://stackoverflow.com/a/62400465/14504785
ffmpeg -i "$f" -i "$t" -lavfi "
[1]geq=lum='p(X,Y)':a='if(gt(abs(W/2-X),W/2-${RAD})*gt(abs(H/2-Y),H/2-${RAD}),
if(lte(hypot(${RAD}-(W/2-abs(W/2-X)),${RAD}-(H/2-abs(H/2-Y))),${RAD}),125,0),125)'[t];
[0][t]overlay=(W-w)/2:(H-h)/2
" -c:v h264_nvenc -cq 20 -c:a copy $o -y