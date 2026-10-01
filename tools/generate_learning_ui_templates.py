#!/usr/bin/env python3
"""Generate two IR learning templates for every DeviceDB device type.

Generated files never replace the hand-authored templates already in ui-templates.
For each device type:
  * ir-<type>-learning-list.json: simple one-button-per-row list of all applicable
    learning features (including features tagged 'all').
  * ir-<type>-learning-grid.json: TV-style compact remote layout containing all
    applicable features, but only when that type has at least one type-specific
    feature in learning-feature-order.json.

The feature order always follows learning-features-by-device-type.json.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORDER_FILE = ROOT / "learning-feature-order.json"
BY_TYPE_FILE = ROOT / "learning-features-by-device-type.json"
OUTPUT_DIR = ROOT / "ui-templates"
GENERATED_MARKER = "generated-learning-template-v1"


def words(value: str) -> str:
    value = value.replace("_", "-")
    value = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", value)
    value = value.replace("-", " ")
    return " ".join(part.capitalize() for part in value.split())


def button(feature: str, *, compact: bool = False) -> dict:
    item = {"type": "button", "label": words(feature), "feature": feature}
    if feature.lower() in {"power", "poweron", "poweroff", "standby"}:
        item["style"] = "danger"
    elif compact:
        item["style"] = "secondary"
    return item


def write_template(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_list_template(device_type: str, features: list[str]) -> dict:
    return {
        "id": f"ir-{device_type}-learning-list",
        "name": f"{words(device_type)} - Command List",
        "deviceType": device_type,
        "transport": "ir",
        "generatedBy": GENERATED_MARKER,
        "style": {
            "backgroundColor": "#101114",
            "foregroundColor": "#F5F7FA",
            "buttonColor": "#252932",
            "buttonTextColor": "#F5F7FA",
            "accentColor": "#4DA3FF",
            "cornerRadius": 12,
            "spacing": 8
        },
        "sections": [
            {
                "title": "Commands",
                "rows": [[button(feature)] for feature in features]
            }
        ]
    }


def make_grid_template(device_type: str, features: list[str]) -> dict:
    rows: list[list[dict]] = []
    # Preserve the Learning Feature Order exactly; three buttons per row gives a
    # compact TV-remote-like layout without dropping any device-specific command.
    for index in range(0, len(features), 3):
        rows.append([button(feature, compact=True) for feature in features[index:index + 3]])
    return {
        "id": f"ir-{device_type}-learning-grid",
        "name": f"{words(device_type)} - Full Remote",
        "deviceType": device_type,
        "transport": "ir",
        "generatedBy": GENERATED_MARKER,
        "style": {
            "backgroundColor": "#0B0D10",
            "foregroundColor": "#F7F8FA",
            "buttonColor": "#20242B",
            "buttonTextColor": "#FFFFFF",
            "accentColor": "#4DA3FF",
            "dangerColor": "#E74C3C",
            "cornerRadius": 14,
            "spacing": 10,
            "buttonHeight": 52
        },
        "sections": [
            {
                "title": words(device_type),
                "subtitle": "Full learning remote",
                "rows": rows
            }
        ]
    }


def main() -> int:
    order = json.loads(ORDER_FILE.read_text(encoding="utf-8"))
    by_type = json.loads(BY_TYPE_FILE.read_text(encoding="utf-8"))
    if not isinstance(order, list) or not isinstance(by_type, dict):
        raise SystemExit("Invalid learning JSON input")

    specific_by_type: dict[str, set[str]] = {}
    for item in order:
        feature_id = str(item.get("id", "")).strip()
        for raw_type in item.get("deviceTypes") or ["all"]:
            device_type = str(raw_type).strip()
            if feature_id and device_type and device_type.lower() != "all":
                specific_by_type.setdefault(device_type.lower(), set()).add(feature_id.lower())

    expected: set[Path] = set()
    list_count = 0
    grid_count = 0
    for device_type, raw_features in by_type.items():
        features = [str(value).strip() for value in raw_features if str(value).strip()]
        list_path = OUTPUT_DIR / f"ir-{device_type}-learning-list.json"
        write_template(list_path, make_list_template(device_type, features))
        expected.add(list_path)
        list_count += 1

        has_specific = bool(specific_by_type.get(device_type.lower()))
        grid_path = OUTPUT_DIR / f"ir-{device_type}-learning-grid.json"
        if has_specific:
            write_template(grid_path, make_grid_template(device_type, features))
            expected.add(grid_path)
            grid_count += 1
        elif grid_path.exists():
            try:
                existing = json.loads(grid_path.read_text(encoding="utf-8"))
                if existing.get("generatedBy") == GENERATED_MARKER:
                    grid_path.unlink()
            except Exception:
                pass

    # Remove stale generated templates for device types that disappeared, but
    # never touch hand-authored templates.
    for path in OUTPUT_DIR.glob("ir-*-learning-*.json"):
        if path in expected:
            continue
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if existing.get("generatedBy") == GENERATED_MARKER:
                path.unlink()
        except Exception:
            pass

    print(f"Generated {list_count} command-list templates and {grid_count} full remote templates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
