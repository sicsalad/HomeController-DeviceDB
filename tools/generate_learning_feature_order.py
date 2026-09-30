#!/usr/bin/env python3
"""Generate the compact, manually reorderable feature list used by IR learning UIs.

Each feature is deliberately written on exactly one line so the display order can
be changed later simply by moving lines in learning-feature-order.json.
Device types are taken from the generated function-catalog.json.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "function-catalog.json"
OUTPUT = ROOT / "learning-feature-order.json"

ORDER = [
    "Power", "PowerOn", "PowerOff", "Standby", "Source", "Input", "Menu", "Home", "Back", "Exit", "Ok",
    "Up", "Down", "Left", "Right", "VolumeUp", "VolumeDown", "Mute", "ChannelUp", "ChannelDown",
    "ChannelList", "PreviousChannel", "Guide", "Info", "Play", "Pause", "PlayPause", "Stop", "Record",
    "Rewind", "FastForward", "Previous", "Next", "Red", "Green", "Yellow", "Blue", "Digit0", "Digit1",
    "Digit2", "Digit3", "Digit4", "Digit5", "Digit6", "Digit7", "Digit8", "Digit9", "Sleep", "Timer",
    "Mode", "Auto", "Heat", "Cool", "Dry", "Fan", "FanSpeed", "FanSpeedUp", "FanSpeedDown",
    "TemperatureUp", "TemperatureDown", "Swing", "SwingVertical", "SwingHorizontal", "Eco", "Turbo", "Quiet",
    "Light", "Display", "Ionizer", "Health", "HeaterUp", "HeaterDown", "FireUp", "Oscillation", "SpeedUp",
    "SpeedDown", "BrightnessUp", "BrightnessDown", "ColorTemperatureUp", "ColorTemperatureDown", "Scene", "Color",
    "White", "Flash", "Strobe", "Fade", "Smooth", "RedUp", "RedDown", "GreenUp", "GreenDown", "BlueUp",
    "BlueDown", "WhiteUp", "WhiteDown", "Zone1On", "Zone1Off", "Zone2On", "Zone2Off", "Zone3On", "Zone3Off",
    "Zone4On", "Zone4Off", "Speed", "Breeze", "Natural", "Reverse", "Direction", "Mist", "TimerUp", "TimerDown",
    "Door", "DoorOpen", "DoorClose", "DoorStop", "Lock", "Unlock", "Alarm", "Siren", "Arm", "Disarm", "ArmStay",
    "ArmAway", "Panic", "Night", "Day", "ZoomIn", "ZoomOut", "FocusNear", "FocusFar", "Preset", "Preset1",
    "Preset2", "Preset3", "Preset4", "Patrol", "Cruise", "Scan", "Start", "Cancel", "Program", "Clock", "TimeUp",
    "TimeDown", "Set", "Memory", "Memory1", "Memory2", "Memory3", "Function", "Option", "Settings",
]


def main() -> int:
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    functions = payload.get("functions", [])
    by_id = {str(item.get("id", "")).strip().lower(): item for item in functions if str(item.get("id", "")).strip()}

    # ORDER is intentionally curated rather than a dump of all raw Flipper names.
    # Fail loudly when a curated ID no longer exists in the catalog so the two
    # central files cannot silently drift apart.
    missing = [wanted for wanted in ORDER if wanted.lower() not in by_id]
    if missing:
        raise SystemExit("Learning ORDER IDs missing from function-catalog.json: " + ", ".join(missing))

    rows = []
    seen = set()
    for wanted in ORDER:
        item = by_id[wanted.lower()]
        function_id = str(item["id"]).strip()
        key = function_id.lower()
        if key in seen:
            continue
        seen.add(key)
        rows.append({"id": function_id, "deviceTypes": item.get("deviceTypes") or ["all"]})

    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("[\n")
        for index, row in enumerate(rows):
            suffix = "," if index < len(rows) - 1 else ""
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + suffix + "\n")
        handle.write("]\n")

    omitted = len(by_id) - len(seen)
    print(f"Wrote {len(rows)} learning features to {OUTPUT}")
    print(f"Catalog functions outside the curated learning order: {omitted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
