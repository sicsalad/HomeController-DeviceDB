#!/usr/bin/env python3
"""Generate learning feature IDs grouped by canonical DeviceDB device type.

Only IDs declared in device-types.json are emitted. Raw/source-specific type names in
the function catalog are evidence, not UI device types.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEVICE_TYPES = ROOT / "device-types.json"
LEARNING_ORDER = ROOT / "learning-feature-order.json"
OUTPUT = ROOT / "learning-features-by-device-type.json"


def canonical_device_types() -> list[str]:
    payload = json.loads(DEVICE_TYPES.read_text(encoding="utf-8"))
    candidates = payload if isinstance(payload, list) else payload.get("deviceTypes", [])
    result: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        device_type = item.strip() if isinstance(item, str) else str(item.get("id") or "").strip() if isinstance(item, dict) else ""
        key = device_type.lower()
        if device_type and key != "all" and key not in seen:
            seen.add(key)
            result.append(device_type)
    if not result:
        raise SystemExit("device-types.json contains no canonical device type IDs")
    return result


def main() -> int:
    order = json.loads(LEARNING_ORDER.read_text(encoding="utf-8"))
    if not isinstance(order, list):
        raise SystemExit("learning-feature-order.json must contain a JSON array")

    device_types = canonical_device_types()
    canonical_by_key = {value.lower(): value for value in device_types}
    grouped: dict[str, list[str]] = {device_type: [] for device_type in device_types}

    for feature in order:
        feature_id = str(feature.get("id", "")).strip()
        if not feature_id:
            continue
        feature_types = [str(value).strip() for value in (feature.get("deviceTypes") or ["all"])]
        if any(value.lower() == "all" for value in feature_types):
            for device_type in device_types:
                grouped[device_type].append(feature_id)
            continue
        for raw_type in feature_types:
            device_type = canonical_by_key.get(raw_type.lower())
            if device_type is not None:
                grouped[device_type].append(feature_id)

    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("{\n")
        for index, device_type in enumerate(device_types):
            suffix = "," if index < len(device_types) - 1 else ""
            handle.write(json.dumps(device_type, ensure_ascii=False) + ":" + json.dumps(grouped[device_type], ensure_ascii=False, separators=(",", ":")) + suffix + "\n")
        handle.write("}\n")

    print(f"Wrote {len(device_types)} canonical device types to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
