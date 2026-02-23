#!/bin/bash
# simple wrapper to call lotto_send.py
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON=${PYTHON:-python3}
export PATH="$PATH"
$PYTHON "$SCRIPT_DIR/lotto_send.py" "$@"
