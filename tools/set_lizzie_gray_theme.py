#!/usr/bin/env python3
import json

CFG = "/Applications/Lizzie/config.txt"

with open(CFG, "r", encoding="utf-8") as f:
    j = json.load(f)

ui = j.setdefault("ui", {})
ui["board-color"] = [128, 128, 128]
ui["fancy-board"] = False
ui["fancy-stones"] = False
ui["shadows-enabled"] = False

with open(CFG, "w", encoding="utf-8") as f:
    json.dump(j, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("Lizzie gray theme applied.")
