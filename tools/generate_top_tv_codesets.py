#!/usr/bin/env python3
"""Generate reusable TV CodeSets for major global TV brands from imported CC0 Flipper captures.

The generator is deliberately conservative about signal transport: only parsed protocols already
supported by HomeController are promoted. A CodeSet is a distinct full command signature, so models
with the exact same IR command map share one CodeSet. We keep up to five generated CodeSets per brand,
while preserving manually curated CodeSets and mappings in catalog-v2.json.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog-v2.json"
GENERATED_TV = ROOT / "generated" / "television"
CODESET_ROOT = ROOT / "codesets" / "television"

# 2025 global shipment top ten used by HomeController's broad-coverage TV catalog.
TOP_BRANDS = [
    "Samsung", "TCL", "Hisense", "LG", "Xiaomi",
    "Skyworth", "Philips", "Sony", "Sharp", "Vizio",
]

SUPPORTED_PROTOCOLS = {
    "samsung32", "nec", "necext", "nec42", "nec42ext",
    "rc5", "rc5x", "rc6", "sirc", "sirc15", "sirc20",
    "kaseikyo", "rca",
}

DEFAULT_FREQUENCY = {
    "samsung32": 38000,
    "nec": 38000,
    "necext": 38000,
    "nec42": 38000,
    "nec42ext": 38000,
    "rc5": 36000,
    "rc5x": 36000,
    "rc6": 36000,
    "sirc": 40000,
    "sirc15": 40000,
    "sirc20": 40000,
    "kaseikyo": 38000,
    "rca": 38000,
}

AUTO_PREFIX = "auto-tv-"
AUTO_CONFIDENCE = "community-signature-group"


def slug(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value or "tv"


def find_brand_folder(brand: str) -> Path | None:
    if not GENERATED_TV.exists():
        return None
    for p in GENERATED_TV.iterdir():
        if p.is_dir() and p.name.casefold() == brand.casefold():
            return p
    return None


def normalized_hex(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.strip().upper().split())


def extract_method(doc: dict) -> dict | None:
    for method in doc.get("controlMethods", []):
        if str(method.get("transport", "")).casefold() != "infrared":
            continue
        if str(method.get("kind", "")).casefold() != "commands":
            continue
        protocol = str(method.get("protocol", "")).strip()
        if protocol.casefold() not in SUPPORTED_PROTOCOLS:
            continue

        commands = []
        for cmd in method.get("commands", []):
            if str(cmd.get("type", "parsed")).casefold() != "parsed":
                continue
            canonical = str(cmd.get("canonical") or "").strip()
            address = normalized_hex(cmd.get("address"))
            command = normalized_hex(cmd.get("command"))
            if not canonical or not address or not command:
                continue
            commands.append({
                "name": str(cmd.get("name") or canonical),
                "canonical": canonical,
                "type": "parsed",
                "address": address,
                "command": command,
            })

        if len(commands) < 5:
            continue
        if not any(c["canonical"].casefold() in {"power", "poweron"} for c in commands):
            continue

        # Keep only one entry per canonical command in the generated CodeSet. When a capture contains
        # aliases, the first one is the stable representative and the model still maps to this signature.
        unique: dict[str, dict] = {}
        for c in commands:
            unique.setdefault(c["canonical"].casefold(), c)
        commands = list(unique.values())

        freq = method.get("frequencyHz")
        if not isinstance(freq, int) or freq <= 0:
            freq = DEFAULT_FREQUENCY.get(protocol.casefold(), 38000)

        return {"protocol": protocol, "frequencyHz": freq, "commands": commands}
    return None


def signature(method: dict) -> str:
    rows = [method["protocol"].casefold()]
    for c in sorted(method["commands"], key=lambda x: x["canonical"].casefold()):
        rows.append("|".join([
            c["canonical"].casefold(),
            c["address"].casefold(),
            c["command"].casefold(),
        ]))
    return "\n".join(rows)


def load_captures(brand: str) -> list[dict]:
    folder = find_brand_folder(brand)
    if folder is None:
        return []
    captures = []
    for path in sorted(folder.glob("*.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        model = str(doc.get("model") or "").strip()
        if len(model) < 2:
            continue
        method = extract_method(doc)
        if method is None:
            continue
        captures.append({"model": model, "path": path, "doc": doc, "method": method, "signature": signature(method)})
    return captures


def get_or_create_node(catalog: dict, brand: str) -> dict:
    for node in catalog.setdefault("manufacturers", []):
        if str(node.get("deviceType", "")).casefold() == "television" and str(node.get("name", "")).casefold() == brand.casefold():
            return node
    node = {"deviceType": "Television", "name": brand, "deviceModels": [], "remoteModels": [], "codeSets": []}
    catalog["manufacturers"].append(node)
    return node


def remove_previous_auto(node: dict) -> None:
    node["codeSets"] = [c for c in node.get("codeSets", []) if not str(c.get("id", "")).startswith(AUTO_PREFIX)]
    node["deviceModels"] = [m for m in node.get("deviceModels", []) if m.get("confidence") != AUTO_CONFIDENCE]
    node["remoteModels"] = [m for m in node.get("remoteModels", []) if m.get("confidence") != AUTO_CONFIDENCE]


def create_codeset(brand: str, group: list[dict]) -> tuple[dict, str]:
    # Prefer the richest capture as the CodeSet representative.
    representative = max(group, key=lambda x: len(x["method"]["commands"]))
    sig_hash = hashlib.sha256(representative["signature"].encode("utf-8")).hexdigest()[:10]
    code_set_id = f"{AUTO_PREFIX}{slug(brand)}-{sig_hash}"
    folder = CODESET_ROOT / brand
    folder.mkdir(parents=True, exist_ok=True)
    rel_path = f"codesets/television/{brand}/{code_set_id}.json"

    payload = {
        "schemaVersion": 2,
        "codeSetId": code_set_id,
        "deviceType": "Television",
        "manufacturer": brand,
        "verification": "community-capture-derived",
        "controlMethods": [{
            "transport": "infrared",
            "protocol": representative["method"]["protocol"],
            "kind": "commands",
            "frequencyHz": representative["method"]["frequencyHz"],
            "commands": representative["method"]["commands"],
        }],
        "sources": [{
            "type": "HomeController-DeviceDB generated capture",
            "path": str(representative["path"].relative_to(ROOT)).replace("\\", "/"),
            "license": "CC0-1.0 inherited from Flipper-IRDB import",
        }],
        "compatibleModels": sorted({x["model"] for x in group}, key=str.casefold),
    }
    (ROOT / rel_path).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    info = {
        "id": code_set_id,
        "name": f"{brand} TV {representative['method']['protocol']} {sig_hash[:5].upper()}",
        "path": rel_path,
        "testCommand": "Power",
    }
    return info, code_set_id


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8-sig")) if CATALOG.exists() else {"schemaVersion": 2, "manufacturers": []}
    catalog["schemaVersion"] = max(2, int(catalog.get("schemaVersion", 2)))

    report = []
    for brand in TOP_BRANDS:
        node = get_or_create_node(catalog, brand)
        remove_previous_auto(node)
        captures = load_captures(brand)

        grouped: dict[str, list[dict]] = defaultdict(list)
        for capture in captures:
            grouped[capture["signature"]].append(capture)

        # Prefer signatures used by multiple models, then richer remotes. Five distinct signatures are
        # enough to give users a useful manual choice without flooding the UI.
        groups = sorted(
            grouped.values(),
            key=lambda g: (len(g), max(len(x["method"]["commands"]) for x in g)),
            reverse=True,
        )[:5]

        existing_ids = {str(x.get("id", "")) for x in node.get("codeSets", [])}
        generated_ids = []
        for group in groups:
            info, code_set_id = create_codeset(brand, group)
            generated_ids.append(code_set_id)
            if code_set_id not in existing_ids:
                node.setdefault("codeSets", []).append(info)
                existing_ids.add(code_set_id)
            for capture in group:
                model_entry = {
                    "name": capture["model"],
                    "codeSetId": code_set_id,
                    "confidence": AUTO_CONFIDENCE,
                }
                if not any(str(m.get("name", "")).casefold() == capture["model"].casefold() for m in node.setdefault("deviceModels", [])):
                    node["deviceModels"].append(model_entry)

        node["deviceModels"] = sorted(node.get("deviceModels", []), key=lambda x: str(x.get("name", "")).casefold())
        node["remoteModels"] = sorted(node.get("remoteModels", []), key=lambda x: str(x.get("name", "")).casefold())
        node["codeSets"] = sorted(node.get("codeSets", []), key=lambda x: str(x.get("name", "")).casefold())
        report.append((brand, len(captures), len(grouped), len(generated_ids), len(node["codeSets"])))

    catalog["manufacturers"] = sorted(
        catalog.get("manufacturers", []),
        key=lambda x: (str(x.get("deviceType", "")).casefold(), str(x.get("name", "")).casefold()),
    )
    CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for brand, captures, unique, generated, total in report:
        print(f"{brand}: captures={captures}, distinct-signatures={unique}, generated={generated}, total-codesets={total}")
        if generated < 5 and total < 5:
            print(f"WARNING: {brand} has fewer than 5 evidence-backed CodeSets; no synthetic CodeSets were invented.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
