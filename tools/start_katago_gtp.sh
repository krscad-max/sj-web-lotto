#!/bin/zsh
KATAGO_BIN="/opt/homebrew/bin/katago"
CFG="/opt/homebrew/Cellar/katago/1.16.4/share/katago/configs/gtp_example.cfg"
MODEL="/opt/homebrew/Cellar/katago/1.16.4/share/katago/g170-b40c256x2-s5095420928-d1229425124.bin.gz"

exec "$KATAGO_BIN" gtp -config "$CFG" -model "$MODEL"
