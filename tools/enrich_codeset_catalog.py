#!/usr/bin/env python3
"""Enrich catalog-v2.json from generated TV captures using conservative exact CodeSet signatures.

Only protocol/address/core-command matches are promoted to the exact-model catalog. Auto-generated
mappings are rebuilt on every run, so a stricter classifier also removes old ambiguous entries.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog-v2.json"
AUTO_CONFIDENCE = "auto-signature-match"

SIGNATURES = {
    ("Television", "Samsung"): [
        {
            "codeSetId": "samsung-tv-7-7-standard",
            "protocol": "Samsung32",
            "address": "07",
            "required": {
                "Power": "02",
                "VolumeUp": "07",
                "VolumeDown": "0B",
                "ChannelUp": "12",
                "ChannelDown": "10",
            },
        }
    ],
    ("Television", "Hitachi"): [
        {
            "codeSetId": "hitachi-tv-rc5-03",
            "protocol": "RC5",
            "address": "03",
            "required": {"Power": "0C", "VolumeUp": "10", "VolumeDown": "11"},
        },
        {
            "codeSetId": "hitachi-tv-nec-50",
            "protocol": "NEC",
            "address": "50",
            "required": {"Power": "17", "VolumeUp": "12", "VolumeDown": "15"},
        },
    ],
}

SAMSUNG_REMOTE_RE = re.compile(r"^(?:AA59|BN59)-[A-Z0-9][A-Z0-9 -]*$", re.I)
HITACHI_REMOTE_RE = re.compile(r"^(?:RC)?\d{5,}$", re.I)
DEVICE_MODEL_RE = re.compile(r"^[A-Z0-9][A-Z0-9._/-]{3,}$", re.I)
SKIP_WORDS = ("unknown", "generic", "smarttv", "smart tv", "remote", "universal")


def first_hex(value: object) -> str:
    if not isinstance(value, str):
        return ""
    text = value.strip().replace("0x", "").upper()
    return text.split()[0] if text else ""


def commands_of(doc: dict) -> tuple[str, dict[str, tuple[str, str]]]:
    for method in doc.get("controlMethods", []):
        if method.get("transport", "").lower() != "infrared" or method.get("kind", "").lower() != "commands":
            continue
        protocol = str(method.get("protocol", ""))
        commands: dict[str, tuple[str, str]] = {}
        for cmd in method.get("commands", []):
            canonical = str(cmd.get("canonical") or "")
            if canonical:
                commands[canonical] = (first_hex(cmd.get("address")), first_hex(cmd.get("command")))
        return protocol, commands
    return "", {}


def matches(doc: dict, sig: dict) -> bool:
    protocol, commands = commands_of(doc)
    if protocol.lower() != sig["protocol"].lower():
        return False
    for canonical, expected_cmd in sig["required"].items():
        actual = commands.get(canonical)
        if not actual or actual[0] != sig["address"] or actual[1] != expected_cmd:
            return False
    return True


def add_unique(items: list[dict], entry: dict) -> bool:
    name = entry["name"].casefold()
    if any(str(existing.get("name", "")).casefold() == name for existing in items):
        return False
    items.append(entry)
    return True


def classify_name(manufacturer: str, raw_model: str) -> tuple[str, str] | None:
    model = raw_model.strip()
    lowered = model.casefold()
    if len(model) < 4 or any(word in lowered for word in SKIP_WORDS):
        return None

    if manufacturer == "Samsung" and SAMSUNG_REMOTE_RE.match(model):
        # Captures occasionally contain a cosmetic space before the last suffix letter.
        return "remote", model.replace(" ", "").upper()
    if manufacturer == "Hitachi" and HITACHI_REMOTE_RE.match(model):
        return "remote", model.upper()

    # Exact-device list should contain model-like identifiers, not descriptions/series labels.
    if not DEVICE_MODEL_RE.match(model) or " " in model:
        return None
    return "device", model


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8-sig"))
    manufacturer_nodes = {(m.get("deviceType"), m.get("name")): m for m in catalog.get("manufacturers", [])}
    added_devices = 0
    added_remotes = 0

    for key, signatures in SIGNATURES.items():
        _, manufacturer = key
        node = manufacturer_nodes.get(key)
        if not node:
            continue

        # Rebuild generated mappings every time; manually curated/source/hardware entries survive.
        node["deviceModels"] = [x for x in node.get("deviceModels", []) if x.get("confidence") != AUTO_CONFIDENCE]
        node["remoteModels"] = [x for x in node.get("remoteModels", []) if x.get("confidence") != AUTO_CONFIDENCE]

        folder = ROOT / "generated" / "television" / manufacturer
        if not folder.exists():
            continue

        for path in sorted(folder.glob("*.json")):
            try:
                doc = json.loads(path.read_text(encoding="utf-8-sig"))
            except Exception:
                continue

            raw_model = str(doc.get("model") or "")
            classification = classify_name(manufacturer, raw_model)
            if classification is None:
                continue
            kind, model = classification

            matched = next((sig for sig in signatures if matches(doc, sig)), None)
            if not matched:
                continue

            entry = {"name": model, "codeSetId": matched["codeSetId"], "confidence": AUTO_CONFIDENCE}
            target = node.setdefault("remoteModels" if kind == "remote" else "deviceModels", [])
            if add_unique(target, entry):
                if kind == "remote":
                    added_remotes += 1
                else:
                    added_devices += 1

        node["deviceModels"] = sorted(node.get("deviceModels", []), key=lambda x: str(x.get("name", "")).casefold())
        node["remoteModels"] = sorted(node.get("remoteModels", []), key=lambda x: str(x.get("name", "")).casefold())

    CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"CodeSet catalog enrichment: +{added_devices} exact device models, +{added_remotes} exact remote models")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
