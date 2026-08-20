#!/usr/bin/env python3
"""Normalize manufacturer display names and merge duplicate maker nodes."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIAL = {
    "gree": "Gree", "samsung": "Samsung", "hitachi": "Hitachi", "whirlpool": "Whirlpool",
    "lg": "LG", "jvc": "JVC", "tcl": "TCL", "rca": "RCA", "nec": "NEC", "aoc": "AOC",
    "sony": "Sony", "panasonic": "Panasonic", "philips": "Philips", "toshiba": "Toshiba",
    "daikin": "Daikin", "midea": "Midea", "mitsubishi": "Mitsubishi", "fujitsu": "Fujitsu",
    "haier": "Haier", "sharp": "Sharp", "hisense": "Hisense", "vizio": "Vizio",
}

def normalize(name: str) -> str:
    n = " ".join((name or "").replace("_", " ").split()).strip()
    if not n:
        return n
    return SPECIAL.get(n.lower(), n)

# Keep generated documents consistent with the public index.
generated = ROOT / "generated"
if generated.exists():
    for path in generated.rglob("*.json"):
        doc = json.loads(path.read_text(encoding="utf-8"))
        old = doc.get("manufacturer", "")
        new = normalize(old)
        if new and new != old:
            doc["manufacturer"] = new
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

index_path = ROOT / "database.json"
index = json.loads(index_path.read_text(encoding="utf-8"))
for type_node in index.get("deviceTypes", []):
    merged = {}
    for maker in type_node.get("manufacturers", []):
        name = normalize(maker.get("name", ""))
        key = name.lower()
        target = merged.setdefault(key, {"name": name, "models": []})
        known = {(m.get("name", "").lower(), m.get("path", "")) for m in target["models"]}
        for model in maker.get("models", []):
            k = (model.get("name", "").lower(), model.get("path", ""))
            if k not in known:
                target["models"].append(model)
                known.add(k)
    for maker in merged.values():
        # If curated and generated use the same displayed model name, keep the curated `devices/` one.
        by_name = {}
        for model in sorted(maker["models"], key=lambda m: (0 if str(m.get("path", "")).startswith("devices/") else 1, m.get("name", "").lower())):
            by_name.setdefault(model.get("name", "").lower(), model)
        maker["models"] = sorted(by_name.values(), key=lambda m: m.get("name", "").lower())
    type_node["manufacturers"] = sorted(merged.values(), key=lambda m: m["name"].lower())
index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
