#!/usr/bin/env python3
"""Normalize generated DeviceDB command methods so protocol is method-level."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
generated = root / "generated"
paths = generated.rglob("*.json") if generated.exists() else []

for path in paths:
    doc = json.loads(path.read_text(encoding="utf-8"))
    new_methods = []
    for method in doc.get("controlMethods", []):
        if method.get("kind") != "commands":
            new_methods.append(method)
            continue
        groups = {}
        for cmd in method.get("commands", []):
            if cmd.get("type") == "raw":
                key = ("raw", "", int(cmd.get("frequencyHz") or 0))
            else:
                key = ("parsed", cmd.get("protocol", ""), 0)
            groups.setdefault(key, []).append(cmd)
        for (_, protocol, frequency), commands in groups.items():
            clean = []
            for cmd in commands:
                c = dict(cmd)
                c.pop("protocol", None)
                clean.append(c)
            new_methods.append({
                "transport": "infrared",
                "protocol": protocol,
                "kind": "commands",
                "frequencyHz": frequency,
                "commands": clean,
            })
    doc["controlMethods"] = new_methods
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
