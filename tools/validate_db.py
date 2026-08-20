#!/usr/bin/env python3
"""Strict consistency validation for HomeController DeviceDB v1."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_PARSED = {
    "Samsung32", "NEC", "NECext", "NEC42", "NEC42ext", "RC5", "RC5X", "RC6",
    "SIRC", "SIRC15", "SIRC20", "Kaseikyo", "RCA"
}
SUPPORTED_STATEFUL = {"GreeV1", "WhirlpoolAc"}
REMOTE_COMMANDS = {
    "Unknown", "Power", "PowerOn", "PowerOff", "Source", "SmartHub", "SoccerMode",
    "VolumeUp", "VolumeDown", "Mute", "ChannelUp", "ChannelDown", "PreviousChannel", "ChannelList",
    "Up", "Down", "Left", "Right", "Ok", "Back", "Exit", "Menu", "Guide", "Tools", "Info",
    "Record", "EManual", "Subtitle", "TeletextMix", "Digit0", "Digit1", "Digit2", "Digit3", "Digit4",
    "Digit5", "Digit6", "Digit7", "Digit8", "Digit9", "Play", "Pause", "Stop", "Rewind", "FastForward",
    "Red", "Green", "Yellow", "Blue", "Custom1", "Custom2", "Custom3", "Custom4", "Custom5", "Custom6",
    "Custom7", "Custom8", "Temperature", "TemperatureUp", "TemperatureDown", "Mode", "ModeAuto", "ModeCool",
    "ModeHeat", "ModeDry", "ModeFan", "FanSpeed", "FanSpeedUp", "FanSpeedDown", "FanSpeedAuto", "Swing",
    "SwingVertical", "SwingHorizontal", "Light", "Powerful", "Turbo", "XFanCleaning", "SelfClean", "IFeel",
    "SixthSense", "OnTimer", "OffTimer", "Wifi", "Economy", "PowerSave", "Timer", "Sleep"
}

errors = []

def fail(msg):
    errors.append(msg)

try:
    index = json.loads((ROOT / "database.json").read_text(encoding="utf-8"))
except Exception as e:
    print(f"database.json cannot be parsed: {e}", file=sys.stderr)
    sys.exit(1)

if index.get("schemaVersion") != 1:
    fail("database.json schemaVersion must be 1")

seen_types = set()
entry_count = 0
for t in index.get("deviceTypes", []):
    type_name = t.get("name", "").strip()
    tk = type_name.lower()
    if not type_name or tk in seen_types:
        fail(f"invalid/duplicate device type: {type_name!r}")
    seen_types.add(tk)
    seen_makers = set()
    for maker in t.get("manufacturers", []):
        maker_name = maker.get("name", "").strip()
        mk = maker_name.lower()
        if not maker_name or mk in seen_makers:
            fail(f"duplicate manufacturer {maker_name!r} in {type_name}")
        seen_makers.add(mk)
        seen_models = set()
        for model in maker.get("models", []):
            entry_count += 1
            model_name = model.get("name", "").strip()
            path_value = model.get("path", "").strip()
            modk = model_name.lower()
            if not model_name or modk in seen_models:
                fail(f"duplicate/empty model {maker_name}/{model_name}")
            seen_models.add(modk)
            path = ROOT / path_value
            if not path_value or not path.is_file():
                fail(f"missing device file for {type_name}/{maker_name}/{model_name}: {path_value}")
                continue
            try:
                doc = json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                fail(f"invalid JSON {path_value}: {e}")
                continue
            if doc.get("schemaVersion") != 1:
                fail(f"{path_value}: schemaVersion must be 1")
            if doc.get("deviceType") != type_name:
                fail(f"{path_value}: deviceType {doc.get('deviceType')!r} != index {type_name!r}")
            if doc.get("manufacturer") != maker_name:
                fail(f"{path_value}: manufacturer {doc.get('manufacturer')!r} != index {maker_name!r}")
            methods = doc.get("controlMethods") or []
            if not methods:
                fail(f"{path_value}: no controlMethods")
            usable = 0
            for method in methods:
                if method.get("transport") != "infrared":
                    # v1 app may ignore future transports; they are legal DB content.
                    continue
                kind = method.get("kind")
                protocol = method.get("protocol", "")
                if kind == "stateful-climate":
                    if protocol not in SUPPORTED_STATEFUL:
                        fail(f"{path_value}: unsupported stateful runtime protocol {protocol}")
                    for cap in method.get("capabilities") or []:
                        if cap not in REMOTE_COMMANDS:
                            fail(f"{path_value}: unknown capability {cap}")
                        else:
                            usable += 1
                elif kind == "commands":
                    commands = method.get("commands") or []
                    for cmd in commands:
                        canonical = cmd.get("canonical")
                        if canonical not in REMOTE_COMMANDS or canonical == "Unknown":
                            fail(f"{path_value}: invalid canonical {canonical!r} for {cmd.get('name')!r}")
                            continue
                        typ = cmd.get("type", "parsed")
                        if typ == "raw":
                            freq = int(cmd.get("frequencyHz") or method.get("frequencyHz") or 0)
                            data = cmd.get("data") or []
                            if freq <= 0 or not data:
                                fail(f"{path_value}: unusable raw command {cmd.get('name')}")
                            else:
                                usable += 1
                        else:
                            if protocol not in SUPPORTED_PARSED:
                                fail(f"{path_value}: unsupported parsed protocol {protocol!r}")
                            if not cmd.get("address") or not cmd.get("command"):
                                fail(f"{path_value}: parsed command missing address/command: {cmd.get('name')}")
                            else:
                                usable += 1
                else:
                    fail(f"{path_value}: unknown infrared control kind {kind!r}")
            if usable == 0:
                fail(f"{path_value}: no usable infrared controls")

if errors:
    print(f"DeviceDB validation FAILED with {len(errors)} error(s):", file=sys.stderr)
    for e in errors[:300]:
        print(f" - {e}", file=sys.stderr)
    if len(errors) > 300:
        print(f" ... {len(errors)-300} more", file=sys.stderr)
    sys.exit(1)

print(f"DeviceDB validation OK: {entry_count} indexed device entries across {len(seen_types)} device types.")
