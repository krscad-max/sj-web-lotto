#!/usr/bin/env python3
import json
import sys

CFG = "/Applications/Lizzie/config.txt"

ENGINES = {
    "katago": "/opt/homebrew/bin/katago gtp -config /opt/homebrew/Cellar/katago/1.16.4/share/katago/configs/gtp_example.cfg -model /opt/homebrew/Cellar/katago/1.16.4/share/katago/g170-b40c256x2-s5095420928-d1229425124.bin.gz",
    "gnugo": "/opt/homebrew/bin/gnugo --mode gtp --level 10",
}

if len(sys.argv) != 2 or sys.argv[1] not in ENGINES:
    print("Usage: set_lizzie_engine.py [katago|gnugo]")
    sys.exit(1)

engine = sys.argv[1]
with open(CFG, "r", encoding="utf-8") as f:
    j = json.load(f)

j.setdefault("leelaz", {})["engine-command"] = ENGINES[engine]

with open(CFG, "w", encoding="utf-8") as f:
    json.dump(j, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"Lizzie engine set to: {engine}")
