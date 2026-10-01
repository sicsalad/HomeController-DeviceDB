#!/usr/bin/env python3
"""Generate the simple IR learning command-list template for every DeviceDB device type.

This generator intentionally owns ONLY ir-<type>-learning-list.json. Re-running it
replaces the same stable file; it never creates numbered/duplicate variants.

Rich/visual remote templates are hand-authored and are deliberately outside this
generator because their grouping, order, spans and visual hierarchy are specific
to each device type.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BY_TYPE_FILE = ROOT / "learning-features-by-device-type.json"
OUTPUT_DIR = ROOT / "ui-templates"
GENERATED_MARKER = "generated-learning-list-v2"


def words(value: str) -> str:
    value = value.replace("_", "-")
    value = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", value)
    value = value.replace("-", " ")
    return " ".join(part.capitalize() for part in value.split())


def button(feature: str) -> dict:
    item = {"type": "button", "label": words(feature), "feature": feature}
    if feature.lower() in {"power", "poweron", "poweroff", "standby"}:
        item["style"] = "danger"
    return item


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
        "sections": [{"title": "Commands", "rows": [[button(f)] for f in features]}]
    }


def main() -> int:
    by_type = json.loads(BY_TYPE_FILE.read_text(encoding="utf-8"))
    if not isinstance(by_type, dict):
        raise SystemExit("Invalid learning-features-by-device-type.json")

    expected: set[Path] = set()
    for device_type, raw_features in by_type.items():
        features = [str(v).strip() for v in raw_features if str(v).strip()]
        path = OUTPUT_DIR / f"ir-{device_type}-learning-list.json"
        path.write_text(json.dumps(make_list_template(device_type, features), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        expected.add(path)

    # Only clean stale LIST templates owned by this generator. Never touch rich,
    # default, modern or other hand-authored templates.
    for path in OUTPUT_DIR.glob("ir-*-learning-list.json"):
        if path in expected:
            continue
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if str(existing.get("generatedBy", "")).startswith("generated-learning-"):
                path.unlink()
        except Exception:
            pass

    print(f"Generated/updated {len(expected)} stable command-list templates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
