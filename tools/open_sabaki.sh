#!/bin/zsh
TMP="/tmp/sabaki-newgame.sgf"
cat > "$TMP" <<'EOF'
(;GM[1]FF[4]SZ[19]KM[6.5])
EOF
open -a "Sabaki" "$TMP"
