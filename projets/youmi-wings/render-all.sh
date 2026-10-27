#!/usr/bin/env bash
# Rendus finaux Youmi Wings. Usage : ./render-all.sh (depuis ce dossier)
set -euo pipefail
R=../../.claude/skills/studio-premium-motion/scripts/render.cjs
node $R youmi-story.html --still end --out livrables/YOUMI_VENDREDI_9x16_v01.png
node $R youmi-feed.html  --still end --out livrables/YOUMI_VENDREDI_4x5_v01.png
node $R youmi-story.html --out livrables/YOUMI_VENDREDI_9x16_v01.mp4 --motion-blur 4
node $R youmi-feed.html  --out livrables/YOUMI_VENDREDI_4x5_v01.mp4  --motion-blur 4
