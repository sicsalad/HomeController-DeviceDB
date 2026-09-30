#!/usr/bin/env python3
"""Synchronize the IR learning feature order with function-catalog.json.

The existing learning-feature-order.json is the authoritative manual display order:
existing feature IDs keep their relative order. New catalog feature IDs are appended
at the end. IDs removed from the catalog are removed from the learning list.
Device types are always refreshed from function-catalog.json.

Each feature is deliberately written on exactly one line so the order can still be
changed manually by moving lines in learning-feature-order.json.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "function-catalog.json"
OUTPUT = ROOT / "learning-feature-order.json"


def load_existing_order() -> list[str]:
    if not OUTPUT.exists():
        return []
    payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
    result: list[str] = []
    seen: set[str] = set()
    for item in payload if isinstance(payload, list) else []:
        feature_id = str(item.get("id", "")).strip()
        key = feature_id.lower()
        if feature_id and key not in seen:
            seen.add(key)
            result.append(feature_id)
    return result


def main() -> int:
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    functions = payload.get("functions", [])
    catalog_items = [item for item in functions if str(item.get("id", "")).strip()]
    by_id = {str(item["id"]).strip().lower(): item for item in catalog_items}

    existing_order = load_existing_order()
    ordered_ids: list[str] = []
    seen: set[str] = set()
    removed: list[str] = []

    # Preserve every existing ID in exactly the same relative order.
    for existing_id in existing_order:
        key = existing_id.lower()
        item = by_id.get(key)
        if item is None:
            removed.append(existing_id)
            continue
        canonical_id = str(item["id"]).strip()
        canonical_key = canonical_id.lower()
        if canonical_key not in seen:
            seen.add(canonical_key)
            ordered_ids.append(canonical_id)

    # Append every new catalog feature, in catalog order.
    added: list[str] = []
    for item in catalog_items:
        feature_id = str(item["id"]).strip()
        key = feature_id.lower()
        if key in seen:
            continue
        seen.add(key)
        ordered_ids.append(feature_id)
        added.append(feature_id)

    rows = [
        {"id": feature_id, "deviceTypes": by_id[feature_id.lower()].get("deviceTypes") or ["all"]}
        for feature_id in ordered_ids
    ]

    # A successful generation must be a complete 1:1 catalog projection.
    if len(rows) != len(by_id) or {row["id"].lower() for row in rows} != set(by_id):
        raise SystemExit("learning-feature-order.json would not contain exactly all function-catalog IDs")

    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("[\n")
        for index, row in enumerate(rows):
            suffix = "," if index < len(rows) - 1 else ""
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + suffix + "\n")
        handle.write("]\n")

    print(f"Wrote {len(rows)} learning features to {OUTPUT}")
    print(f"Preserved existing ordered features: {len(rows) - len(added)}")
    print(f"Appended new catalog features: {len(added)}")
    if added:
        print("Added: " + ", ".join(added))
    if removed:
        print("Removed because no longer present in catalog: " + ", ".join(removed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
