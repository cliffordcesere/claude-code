#!/usr/bin/env bash
# Rendus finaux Youmi Wings. Usage : ./render-all.sh (depuis ce dossier)
set -euo pipefail
R=../../.claude/skills/studio-premium-motion/scripts/render.cjs
node $R youmi-story.html --still end --out livrables/YOUMI_VENDREDI_9x16_v02.png
node $R youmi-feed.html  --still end --out livrables/YOUMI_VENDREDI_4x5_v02.png
node $R youmi-story.html --out livrables/YOUMI_VENDREDI_9x16_v02.mp4 --motion-blur 4
node $R youmi-feed.html  --out livrables/YOUMI_VENDREDI_4x5_v02.mp4  --motion-blur 4
# Son : sound design synthétisé, calé sur la timeline (voir son-cues.json)
python3 ../../.claude/skills/studio-premium-motion/scripts/sfx.py son-cues.json --out livrables/son.wav \
  --video livrables/YOUMI_VENDREDI_9x16_v02.mp4 --mux livrables/YOUMI_VENDREDI_9x16_v02_son.mp4
ffmpeg -y -v error -i livrables/YOUMI_VENDREDI_4x5_v02.mp4 -i livrables/son.wav -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart livrables/YOUMI_VENDREDI_4x5_v02_son.mp4
