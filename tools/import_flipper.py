#!/usr/bin/env python3
"""Build HomeController DeviceDB generated TV/AC entries from Flipper-IRDB.

The importer is intentionally conservative. It only publishes files that contain
commands the current HomeController runtime can actually transmit, and it applies
minimum usefulness checks so tiny/sparse captures do not flood the public index.
Curated entries always win over generated entries with the same type/maker/model.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

SUPPORTED_PARSED = {
    "NEC", "NECext", "NEC42", "NEC42ext", "Samsung32",
    "RC5", "RC5X", "RC6", "SIRC", "SIRC15", "SIRC20", "Kaseikyo", "RCA"
}

DIRECT = {
    "power": "Power", "power toggle": "Power", "on off": "Power",
    "source": "Source", "input": "Source",
    "mute": "Mute", "menu": "Menu", "tools": "Tools", "info": "Info",
    "guide": "Guide", "back": "Back", "return": "Back", "exit": "Exit", "ok": "Ok",
    "enter": "Ok", "select": "Ok", "up": "Up", "down": "Down", "left": "Left", "right": "Right",
    "red": "Red", "green": "Green", "yellow": "Yellow", "blue": "Blue",
    "play": "Play", "pause": "Pause", "stop": "Stop", "record": "Record",
    "rewind": "Rewind", "fast back": "Rewind", "fast backward": "Rewind",
    "fast forward": "FastForward", "fast fw": "FastForward",
    "sleep": "Sleep", "timer": "Timer", "light": "Light", "turbo": "Turbo",
    "economy": "Economy", "eco": "Economy", "wifi": "Wifi", "i feel": "IFeel", "ifeel": "IFeel",
    "swing": "Swing", "swing vertical": "SwingVertical", "swing horizontal": "SwingHorizontal",
    "xfan": "XFanCleaning", "x fan": "XFanCleaning", "self clean": "SelfClean",
}


def norm_name(value: str) -> str:
    value = value.strip().lower().replace("_", "-")
    value = re.sub(r"[^a-z0-9+\- ]+", " ", value)
    value = re.sub(r"[- ]+", " ", value).strip()
    return value


def canonical_for(name: str) -> str | None:
    n = norm_name(name)
    if n in DIRECT:
        return DIRECT[n]
    if n in {str(i) for i in range(10)}:
        return f"Digit{n}"
    if any(x in n for x in ("vol up", "volume up", "vol+", "volume+")):
        return "VolumeUp"
    if any(x in n for x in ("vol down", "volume down", "vol dn", "vol-", "volume-")):
        return "VolumeDown"
    if any(x in n for x in ("ch up", "channel up", "pr up", "ch next")):
        return "ChannelUp"
    if any(x in n for x in ("ch down", "channel down", "pr down", "ch prev")):
        return "ChannelDown"
    if any(x in n for x in ("last ch", "previous ch", "pre ch")):
        return "PreviousChannel"
    if "channel list" in n or "ch list" in n:
        return "ChannelList"
    if "temp" in n and any(x in n for x in ("up", "+", "plus")):
        return "TemperatureUp"
    if "temp" in n and any(x in n for x in ("down", "-", "minus")):
        return "TemperatureDown"
    if "fan" in n and "auto" in n:
        return "FanSpeedAuto"
    if "fan" in n and any(x in n for x in ("up", "+")):
        return "FanSpeedUp"
    if "fan" in n and any(x in n for x in ("down", "-")):
        return "FanSpeedDown"
    if "mode" in n and "cool" in n:
        return "ModeCool"
    if "mode" in n and "heat" in n:
        return "ModeHeat"
    if "mode" in n and "dry" in n:
        return "ModeDry"
    if "mode" in n and "fan" in n:
        return "ModeFan"
    if "mode" in n and "auto" in n:
        return "ModeAuto"
    return None


def parse_ir(path: Path) -> list[dict]:
    commands: list[dict] = []
    current: dict | None = None

    def finish() -> None:
        nonlocal current
        if not current or not current.get("name"):
            current = None
            return
        typ = current.get("type", "").lower()
        if typ == "parsed":
            if current.get("protocol") in SUPPORTED_PARSED and current.get("address") and current.get("command"):
                commands.append(current)
        elif typ == "raw":
            if current.get("frequencyHz", 0) > 0 and current.get("data"):
                commands.append(current)
        current = None

    text = path.read_text(encoding="utf-8", errors="replace")
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower().startswith("name:"):
            finish()
            current = {"name": line.split(":", 1)[1].strip()}
            continue
        if current is None or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip().lower(), value.strip()
        if key == "type":
            current["type"] = value.lower()
        elif key == "protocol":
            current["protocol"] = value
        elif key == "address":
            current["address"] = value
        elif key == "command":
            current["command"] = value
        elif key == "frequency":
            try:
                current["frequencyHz"] = int(value)
            except ValueError:
                pass
        elif key == "data":
            vals = []
            for tok in re.split(r"[\s,]+", value):
                try:
                    v = int(tok)
                    if v > 0:
                        vals.append(v)
                except ValueError:
                    pass
            if vals:
                current["data"] = vals
    finish()
    return commands


def sanitize_filename(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._")
    return value or "device"


def display_model(stem: str, manufacturer: str) -> str:
    s = stem
    prefix = manufacturer.replace(" ", "_") + "_"
    if s.lower().startswith(prefix.lower()):
        s = s[len(prefix):]
    return s.replace("_", " ").strip() or stem


def useful(device_type: str, commands: list[dict]) -> bool:
    canon = {c.get("canonical") for c in commands}
    names = {norm_name(c.get("name", "")) for c in commands}
    has_power = "Power" in canon or any("power" in n for n in names)
    if device_type == "Television":
        return has_power and len(commands) >= 8
    # Climate captures are often sparse. Require power plus at least two other useful controls.
    climate_markers = {"TemperatureUp", "TemperatureDown", "ModeCool", "ModeHeat", "ModeAuto",
                       "FanSpeedUp", "FanSpeedDown", "Swing", "Turbo", "Sleep"}
    return has_power and len(commands) >= 3 and bool(canon & climate_markers or len(commands) >= 5)


def enrich_canonicals(commands: list[dict]) -> list[dict]:
    custom = 1
    out = []
    for c in commands:
        item = dict(c)
        canonical = canonical_for(item["name"])
        if canonical is None and custom <= 8:
            canonical = f"Custom{custom}"
            custom += 1
        if canonical is None:
            continue
        item["canonical"] = canonical
        out.append(item)
    return out


def load_curated(root: Path) -> dict:
    return json.loads((root / "curated-database.json").read_text(encoding="utf-8"))


def key_of(type_name: str, maker: str, model: str) -> tuple[str, str, str]:
    return type_name.lower(), maker.lower(), model.lower()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="Path to checked-out Flipper-IRDB")
    ap.add_argument("--output", default=".", help="Path to HomeController-DeviceDB checkout")
    args = ap.parse_args()

    source = Path(args.source).resolve()
    root = Path(args.output).resolve()
    generated = root / "generated"
    if generated.exists():
        shutil.rmtree(generated)

    curated = load_curated(root)
    existing = set()
    for t in curated.get("deviceTypes", []):
        for m in t.get("manufacturers", []):
            for model in m.get("models", []):
                existing.add(key_of(t["name"], m["name"], model["name"]))

    index_map: dict[str, dict[str, list[dict]]] = {}
    total_files = total_devices = 0

    for folder, type_name in (("TVs", "Television"), ("ACs", "Air Conditioner")):
        base = source / folder
        if not base.exists():
            continue
        for ir in sorted(base.rglob("*.ir")):
            total_files += 1
            rel = ir.relative_to(base)
            if len(rel.parts) < 2 or any(p.startswith((".", "_")) for p in rel.parts):
                continue
            manufacturer = rel.parts[0]
            model = display_model(ir.stem, manufacturer)
            commands = enrich_canonicals(parse_ir(ir))
            if not useful(type_name, commands):
                continue
            if key_of(type_name, manufacturer, model) in existing:
                continue

            safe_maker = sanitize_filename(manufacturer)
            safe_model = sanitize_filename(ir.stem)
            type_dir = "television" if type_name == "Television" else "air-conditioner"
            out_rel = f"generated/{type_dir}/{safe_maker}/{safe_model}.json"
            out_file = root / out_rel
            out_file.parent.mkdir(parents=True, exist_ok=True)

            # Protocol may vary per command, so generated captures keep protocol on command level.
            method_commands = []
            for c in commands:
                item = {"name": c["name"], "canonical": c["canonical"], "type": c.get("type", "parsed")}
                if c.get("type") == "raw":
                    item["frequencyHz"] = c.get("frequencyHz", 38000)
                    item["data"] = c["data"]
                else:
                    item["protocol"] = c["protocol"]
                    item["address"] = c["address"]
                    item["command"] = c["command"]
                method_commands.append(item)

            doc = {
                "schemaVersion": 1,
                "deviceType": type_name,
                "manufacturer": manufacturer,
                "model": model,
                "verification": "community-capture",
                "controlMethods": [{
                    "transport": "infrared",
                    "protocol": "",
                    "kind": "commands",
                    "frequencyHz": 0,
                    "commands": method_commands,
                }],
                "sources": [{
                    "type": "Flipper-IRDB",
                    "path": str(ir.relative_to(source)).replace("\\", "/"),
                    "license": "CC0-1.0",
                }],
            }
            out_file.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            index_map.setdefault(type_name, {}).setdefault(manufacturer, []).append({"name": model, "path": out_rel})
            total_devices += 1

    # Merge curated + generated. Curated entries always come first and win on duplicate names.
    merged = json.loads(json.dumps(curated))
    type_nodes = {t["name"].lower(): t for t in merged.setdefault("deviceTypes", [])}
    for type_name, makers in index_map.items():
        tnode = type_nodes.get(type_name.lower())
        if tnode is None:
            tnode = {"name": type_name, "manufacturers": []}
            merged["deviceTypes"].append(tnode)
            type_nodes[type_name.lower()] = tnode
        maker_nodes = {m["name"].lower(): m for m in tnode.setdefault("manufacturers", [])}
        for maker, models in makers.items():
            mnode = maker_nodes.get(maker.lower())
            if mnode is None:
                mnode = {"name": maker, "models": []}
                tnode["manufacturers"].append(mnode)
                maker_nodes[maker.lower()] = mnode
            known = {x["name"].lower() for x in mnode["models"]}
            for model in sorted(models, key=lambda x: x["name"].lower()):
                if model["name"].lower() not in known:
                    mnode["models"].append(model)
                    known.add(model["name"].lower())
            mnode["models"].sort(key=lambda x: x["name"].lower())
        tnode["manufacturers"].sort(key=lambda x: x["name"].lower())
    merged["deviceTypes"].sort(key=lambda x: x["name"].lower())
    merged["name"] = "HomeController DeviceDB"
    merged["generatedFrom"] = "Flipper-IRDB + curated HomeController definitions"
    (root / "database.json").write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Scanned {total_files} IR files; generated {total_devices} useful DeviceDB entries.")


if __name__ == "__main__":
    main()
