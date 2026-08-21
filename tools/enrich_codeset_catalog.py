#!/usr/bin/env python3
"""Enrich catalog-v2.json from generated TV captures when the IR signature is an exact known CodeSet match.

This deliberately uses conservative signatures. A generated file is only mapped when a set of core
commands, protocol and address all match an already curated CodeSet. Ambiguous captures remain in the
normal generated database and are NOT advertised as exact CodeSet mappings.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog-v2.json"

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

REMOTE_RE = re.compile(r"^(?:AA|BN)\d{2}-[A-Z0-9-]+$", re.I)
SKIP_NAMES = {"unknown", "remote", "tv", "samsung", "hitachi", "aa59"}


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
            if not canonical:
                continue
            commands[canonical] = (first_hex(cmd.get("address")), first_hex(cmd.get("command")))
        return protocol, commands
    return "", {}


def matches(doc: dict, sig: dict) -> bool:
    protocol, commands = commands_of(doc)
    if protocol.lower() != sig["protocol"].lower():
        return False
    for canonical, expected_cmd in sig["required"].items():
        actual = commands.get(canonical)
        if not actual:
            return False
        address, command = actual
        if address != sig["address"] or command != expected_cmd:
            return False
    return True


def add_unique(items: list[dict], entry: dict) -> bool:
    name = entry["name"].casefold()
    for existing in items:
        if str(existing.get("name", "")).casefold() == name:
            # Never lower an existing curated confidence value.
            return False
    items.append(entry)
    return True


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8-sig"))
    manufacturer_nodes = {
        (m.get("deviceType"), m.get("name")): m for m in catalog.get("manufacturers", [])
    }
    added_devices = 0
    added_remotes = 0

    for key, signatures in SIGNATURES.items():
        device_type, manufacturer = key
        node = manufacturer_nodes.get(key)
        if not node:
            continue
        folder = ROOT / "generated" / "television" / manufacturer
        if not folder.exists():
            continue

        for path in sorted(folder.glob("*.json")):
            try:
                doc = json.loads(path.read_text(encoding="utf-8-sig"))
            except Exception:
                continue
            model = str(doc.get("model") or "").strip()
            if len(model) < 4 or model.casefold() in SKIP_NAMES:
                continue

            matched = next((sig for sig in signatures if matches(doc, sig)), None)
            if not matched:
                continue

            entry = {
                "name": model,
                "codeSetId": matched["codeSetId"],
                "confidence": "auto-signature-match",
            }
            is_remote = bool(REMOTE_RE.match(model)) or (manufacturer == "Hitachi" and model.isdigit())
            target = node.setdefault("remoteModels" if is_remote else "deviceModels", [])
            if add_unique(target, entry):
                if is_remote:
                    added_remotes += 1
                else:
                    added_devices += 1

        node["deviceModels"] = sorted(node.get("deviceModels", []), key=lambda x: str(x.get("name", "")).casefold())
        node["remoteModels"] = sorted(node.get("remoteModels", []), key=lambda x: str(x.get("name", "")).casefold())

    CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"CodeSet catalog enrichment: +{added_devices} device models, +{added_remotes} remote models")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
