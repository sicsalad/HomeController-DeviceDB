#!/usr/bin/env python3
"""Improve canonical HomeController control mappings in generated captures."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
generated = root / "generated"


def norm(s: str) -> str:
    s = s.lower().replace("_", " ")
    s = re.sub(r"[^a-z0-9+\- ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def map_name(name: str):
    n = norm(name)
    exact = {
        "on": "PowerOn", "off": "PowerOff", "power": "Power", "power on": "PowerOn", "power off": "PowerOff",
        "vol +": "VolumeUp", "volume +": "VolumeUp", "vol up": "VolumeUp", "volume up": "VolumeUp",
        "vol -": "VolumeDown", "volume -": "VolumeDown", "vol down": "VolumeDown", "volume down": "VolumeDown",
        "p +": "ChannelUp", "ch +": "ChannelUp", "channel +": "ChannelUp", "program +": "ChannelUp", "programme +": "ChannelUp",
        "p -": "ChannelDown", "ch -": "ChannelDown", "channel -": "ChannelDown", "program -": "ChannelDown", "programme -": "ChannelDown",
        "temp +": "TemperatureUp", "temperature +": "TemperatureUp", "temp up": "TemperatureUp",
        "temp -": "TemperatureDown", "temperature -": "TemperatureDown", "temp down": "TemperatureDown",
        "fan +": "FanSpeedUp", "fan up": "FanSpeedUp", "fan -": "FanSpeedDown", "fan down": "FanSpeedDown",
        "fan auto": "FanSpeedAuto", "swing": "Swing", "sleep": "Sleep", "turbo": "Turbo", "eco": "Economy",
        "economy": "Economy", "light": "Light", "wifi": "Wifi", "i feel": "IFeel", "ifeel": "IFeel",
        "self clean": "SelfClean", "clean": "SelfClean", "xfan": "XFanCleaning", "x fan": "XFanCleaning",
        "menu": "Menu", "home": "Custom1", "source": "Source", "input": "Source", "mute": "Mute",
        "ok": "Ok", "enter": "Ok", "select": "Ok", "return": "Back", "back": "Back", "exit": "Exit",
        "up": "Up", "down": "Down", "left": "Left", "right": "Right", "info": "Info", "guide": "Guide",
        "red": "Red", "green": "Green", "yellow": "Yellow", "blue": "Blue",
        "play": "Play", "pause": "Pause", "stop": "Stop", "record": "Record", "rewind": "Rewind",
        "fast forward": "FastForward", "fast fw": "FastForward", "fast back": "Rewind",
    }
    if n in exact:
        return exact[n]
    if n in {str(i) for i in range(10)}:
        return f"Digit{n}"
    if "previous" in n and "ch" in n or "last ch" in n:
        return "PreviousChannel"
    if "channel list" in n or "ch list" in n:
        return "ChannelList"
    if "mode" in n:
        if "cool" in n: return "ModeCool"
        if "heat" in n: return "ModeHeat"
        if "dry" in n: return "ModeDry"
        if "fan" in n: return "ModeFan"
        if "auto" in n: return "ModeAuto"
        return "Mode"
    return None


if generated.exists():
    for path in generated.rglob("*.json"):
        doc = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for method in doc.get("controlMethods", []):
            for cmd in method.get("commands", []):
                mapped = map_name(cmd.get("name", ""))
                if mapped and cmd.get("canonical") != mapped:
                    cmd["canonical"] = mapped
                    changed = True
        if changed:
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
