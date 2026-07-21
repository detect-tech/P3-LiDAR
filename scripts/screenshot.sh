#!/bin/bash
# Screenshot a local HTML file using the installed macOS Chrome.app in headless mode.
# No Node/Playwright/chromium-cli needed — this machine doesn't have Node installed,
# but macOS Chrome.app works directly for this.
#
# Usage: ./screenshot.sh <path-to-html-or-file-url> <output.png> [width] [height]

set -e
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

INPUT="$1"
OUTPUT="${2:-screenshot.png}"
WIDTH="${3:-1728}"
HEIGHT="${4:-1200}"

if [ -z "$INPUT" ]; then
  echo "Usage: $0 <path-to-html-or-file-url> <output.png> [width] [height]"
  exit 1
fi

# accept a plain filesystem path or an already-formed file:// URL
if [[ "$INPUT" == file://* ]] || [[ "$INPUT" == http://* ]] || [[ "$INPUT" == https://* ]]; then
  URL="$INPUT"
else
  URL="file://$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"
fi

"$CHROME" --headless=new --disable-gpu --hide-scrollbars \
  --screenshot="$OUTPUT" \
  --window-size="${WIDTH},${HEIGHT}" \
  --virtual-time-budget=8000 \
  --run-all-compositor-stages-before-draw \
  "$URL" 2>&1 | grep -v "ERROR\|allocator" || true

echo "Wrote $OUTPUT"
