#!/bin/zsh
WEIGHTS="$HOME/.local/share/leela-zero/best-network"
if [ ! -f "$WEIGHTS" ]; then
  echo "Leela Zero weights not found: $WEIGHTS" >&2
  echo "Download weights and place as best-network first." >&2
  exit 1
fi
exec /opt/homebrew/bin/leelaz -g -w "$WEIGHTS"
