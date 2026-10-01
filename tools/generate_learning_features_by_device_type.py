#!/usr/bin/env python3
"""Generate learning feature IDs grouped by device type.

The order of feature IDs for every device type follows learning-feature-order.json.
Features tagged with deviceTypes=["all"] are included for every known device type.
Each device type is deliberately written on one JSON line for easy review/editing.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEVICE_TYPES = ROOT / "device-types.json"
LEARNING_ORDER = ROOT / "learning-feature-order.json"
OUTPUT = ROOT / "learning-features-by-device-type.json"


def collect_known_device_types(order: list[dict]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()

    if DEVICE_TYPES.exists():
        payload = json.loads(DEVICE_TYPES.read_text(encoding="utf-8"))
        candidates = payload if isinstance(payload, list) else payload.get("deviceTypes", [])
        for item in candidates:
            if isinstance(item, str):
                device_type = item.strip()
            elif isinstance(item, dict):
                device_type = str(item.get("id") or item.get("type") or item.get("name") or "").strip()
            else:
                device_type = ""
            key = device_type.lower()
            if device_type and key != "all" and key not in seen:
                seen.add(key)
                result.append(device_type)

    # Never lose a type merely because device-types.json uses a different schema.
    for feature in order:
        for raw_type in feature.get("deviceTypes") or ["all"]:
            device_type = str(raw_type).strip()
            key = device_type.lower()
            if device_type and key != "all" and key not in seen:
                seen.add(key)
                result.append(device_type)

    return result


def main() -> int:
    order = json.loads(LEARNING_ORDER.read_text(encoding="utf-8"))
    if not isinstance(order, list):
        raise SystemExit("learning-feature-order.json must contain a JSON array")

    device_types = collect_known_device_types(order)
    grouped: dict[str, list[str]] = {device_type: [] for device_type in device_types}

    for feature in order:
        feature_id = str(feature.get("id", "")).strip()
        if not feature_id:
            continue
        feature_types = [str(value).strip() for value in (feature.get("deviceTypes") or ["all"])]
        applies_to_all = any(value.lower() == "all" for value in feature_types)
        allowed = {value.lower() for value in feature_types}
        for device_type in device_types:
            if applies_to_all or device_type.lower() in allowed:
                grouped[device_type].append(feature_id)

    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("{\n")
        for index, device_type in enumerate(device_types):
            suffix = "," if index < len(device_types) - 1 else ""
            handle.write(json.dumps(device_type, ensure_ascii=False) + ":" + json.dumps(grouped[device_type], ensure_ascii=False, separators=(",", ":")) + suffix + "\n")
        handle.write("}\n")

    print(f"Wrote {len(device_types)} device types to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
