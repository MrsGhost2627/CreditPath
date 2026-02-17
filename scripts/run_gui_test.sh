#!/usr/bin/env bash
# Simple wrapper to run the GUI test under Xvfb when available.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"

CMD=(python3 "$ROOT/WilsonThaija.py" --test-gui)

if command -v xvfb-run >/dev/null 2>&1; then
  echo "Found xvfb-run — launching GUI test under virtual display..."
  xvfb-run -s "-screen 0 1024x768x24" "${CMD[@]}"
  exit $?
else
  cat <<'MSG'
No xvfb-run found in PATH. To run the automated GUI test install Xvfb and try again.

On Debian/Ubuntu:
  sudo apt-get update && sudo apt-get install -y xvfb

Then run:
  ./scripts/run_gui_test.sh

Alternatively, run the headless GUI check without Xvfb:
  python3 WilsonThaija.py --test-gui

MSG
  exit 2
fi
