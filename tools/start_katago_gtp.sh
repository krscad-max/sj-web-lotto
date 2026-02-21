#!/bin/zsh
KATAGO_BIN="/opt/homebrew/bin/katago"
CFG="/opt/homebrew/Cellar/katago/1.16.4/share/katago/configs/gtp_example.cfg"
MODEL="/opt/homebrew/Cellar/katago/1.16.4/share/katago/kata1-b18c384nbt-s9996604416-d4316597426.bin.gz"

exec "$KATAGO_BIN" gtp -config "$CFG" -model "$MODEL"
