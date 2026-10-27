#!/usr/bin/env bash
# fetch-fonts.sh — download the SIL Open Font License typefaces used by build.py.
#
# The fonts are not committed: they are pulled on demand from the google/fonts
# repository, which keeps this repo small and keeps the OFL attribution honest.
# Every family below is licensed under the SIL Open Font License 1.1, which
# permits commercial and print use, embedding in PDFs, and redistribution.
#
#   https://openfontlicense.org
#
# Usage:  bash fetch-fonts.sh
set -euo pipefail

DEST="$(cd "$(dirname "$0")/../.." && pwd)/.tmp-fonts"
mkdir -p "$DEST"

PATHS=(
  "ofl/lobster/Lobster-Regular.ttf"
  "ofl/bevan/Bevan-Regular.ttf"
  "ofl/anton/Anton-Regular.ttf"
  "ofl/bebasneue/BebasNeue-Regular.ttf"
  "ofl/inter/Inter%5Bopsz,wght%5D.ttf"
  "ofl/archivoblack/ArchivoBlack-Regular.ttf"
  "ofl/archivo/Archivo%5Bwdth,wght%5D.ttf"
  "ofl/spacemono/SpaceMono-Regular.ttf"
  "ofl/spacemono/SpaceMono-Bold.ttf"
  "ofl/playfairdisplay/PlayfairDisplay-Italic%5Bwght%5D.ttf"
  "ofl/newsreader/Newsreader%5Bopsz,wght%5D.ttf"
)

for p in "${PATHS[@]}"; do
  name="$(basename "$p")"
  if [ -s "$DEST/$name" ]; then
    echo "· $name  (déjà présent)"
    continue
  fi
  code=$(curl -sL -w "%{http_code}" -H "Accept: application/vnd.github.raw" \
    -o "$DEST/$name" "https://api.github.com/repos/google/fonts/contents/$p")
  if [ "$code" != "200" ]; then
    echo "✗ $name  (HTTP $code)" >&2
    rm -f "$DEST/$name"
    exit 1
  fi
  echo "✔ $name"
done

echo
echo "Fontes prêtes dans $DEST"
