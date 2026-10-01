#!/usr/bin/env python3
"""Synchronize ui-templates/index.json with every DeviceDB UI template."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "ui-templates"
INDEX_FILE = TEMPLATE_DIR / "index.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    raw_index = load_json(INDEX_FILE)
    if isinstance(raw_index, list):
        entries = raw_index
        container = None
    elif isinstance(raw_index, dict):
        key = next((k for k in ("templates", "items", "entries") if isinstance(raw_index.get(k), list)), None)
        if key is None:
            raise SystemExit("ui-templates/index.json has no templates/items/entries array")
        entries = raw_index[key]
        container = (raw_index, key)
    else:
        raise SystemExit("Invalid ui-templates/index.json")

    existing = {str(e.get("id", "")): e for e in entries if isinstance(e, dict) and e.get("id")}
    discovered: dict[str, dict] = {}
    for path in sorted(TEMPLATE_DIR.glob("*.json")):
        if path.name == "index.json":
            continue
        try:
            template = load_json(path)
        except Exception as exc:
            raise SystemExit(f"Invalid JSON template {path.name}: {exc}") from exc
        if not isinstance(template, dict) or not template.get("id"):
            continue
        template_id = str(template["id"])
        if template_id in discovered:
            raise SystemExit(f"Duplicate UI template id {template_id}: {path.name}")
        entry = dict(existing.get(template_id, {}))
        entry["id"] = template_id
        # HomeController's UiTemplateIndexEntry consumes `path`; `file` is only
        # optional descriptive metadata. Missing path makes the whole catalog
        # refresh fail and leaves the mobile app on its previous cached index.
        entry["path"] = path.name
        entry["file"] = path.name
        entry.setdefault("status", "stable")
        if template.get("access") is not None:
            entry["access"] = template["access"]
        else:
            entry.setdefault("access", "free" if "learning-list" in template_id else "premium")
        if template.get("name") is not None:
            entry["name"] = template["name"]
        if template.get("deviceTypeId") is not None:
            entry["deviceType"] = template["deviceTypeId"]
        if template.get("connections"):
            connections = template["connections"]
            if isinstance(connections, list) and connections:
                entry["transport"] = "ir" if str(connections[0]).lower() == "infrared" else str(connections[0]).lower()
        discovered[template_id] = entry

    new_entries = [discovered[k] for k in sorted(discovered, key=str.lower)]
    output = new_entries if container is None else dict(container[0])
    if container is not None:
        output[container[1]] = new_entries
    INDEX_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Indexed {len(new_entries)} UI templates; every entry has a loadable path.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
