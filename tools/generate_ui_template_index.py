#!/usr/bin/env python3
"""Synchronize ui-templates/index.json with every DeviceDB UI template.

The index is derived from the JSON template files in ui-templates/.  This keeps
hand-authored/premium templates and generated learning-list templates equally
discoverable.  Existing index metadata is preserved when possible; missing
entries are created from the template's own id/name/deviceType/transport data.
"""
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
        entry["file"] = path.name
        for field in ("name", "deviceType", "transport"):
            if template.get(field) is not None:
                entry[field] = template[field]
        discovered[template_id] = entry

    stale = sorted(set(existing) - set(discovered))
    if stale:
        print("Removing stale index entries: " + ", ".join(stale))

    new_entries = [discovered[k] for k in sorted(discovered, key=str.lower)]
    output = new_entries if container is None else dict(container[0])
    if container is not None:
        output[container[1]] = new_entries
    INDEX_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Indexed {len(new_entries)} UI templates ({len(set(discovered) - set(existing))} added)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
