#!/usr/bin/env python3
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
WIFI = ROOT / "wifi"
ALLOWED_TRANSPORTS = {"udp","udp-unicast","udp-broadcast","tcp","http","https","websocket","websocket-secure"}
ALLOWED_STATUS = {"stable","experimental","software-validated"}
FORBIDDEN_KEYS = {"script","javascript","csharp","assembly","eval","exec","nativeLibrary"}

errors = []

def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as ex:
        errors.append(f"{path}: invalid JSON: {ex}")
        return None

def extract_json_path(obj, expr):
    if not isinstance(expr, str) or not expr.startswith("json:"):
        raise ValueError(f"unsupported self-test expression: {expr}")
    cur = obj
    for part in expr[5:].lstrip("$.").split("."):
        if not part:
            continue
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(part)
        cur = cur[part]
    return cur

def walk_forbidden(value, path=""):
    if isinstance(value, dict):
        for k, v in value.items():
            if k in FORBIDDEN_KEYS:
                errors.append(f"{path}: forbidden executable field '{k}'")
            walk_forbidden(v, f"{path}.{k}" if path else k)
    elif isinstance(value, list):
        for i, v in enumerate(value):
            walk_forbidden(v, f"{path}[{i}]")

index = load(WIFI / "index.json")
if not index:
    sys.exit(1)
if index.get("schemaVersion") != 1:
    errors.append("wifi/index.json: schemaVersion must be 1")

seen_driver_ids = set()
drivers = {}
for entry in index.get("drivers", []):
    did = entry.get("id")
    if not did or did in seen_driver_ids:
        errors.append(f"wifi/index.json: missing/duplicate driver id: {did}")
        continue
    seen_driver_ids.add(did)
    p = WIFI / entry.get("path", "")
    if not p.is_file():
        errors.append(f"driver {did}: missing file {p}")
        continue
    d = load(p)
    if not d:
        continue
    drivers[did] = d
    if d.get("id") != did:
        errors.append(f"{p}: id differs from index ({d.get('id')} != {did})")
    if d.get("schemaVersion") != 1:
        errors.append(f"{p}: schemaVersion must be 1")
    if not isinstance(d.get("minimumRuntimeVersion", 1), int):
        errors.append(f"{p}: minimumRuntimeVersion must be integer")
    if d.get("status") not in ALLOWED_STATUS:
        errors.append(f"{p}: unsupported status {d.get('status')}")
    walk_forbidden(d, str(p.relative_to(ROOT)))
    operations = d.get("operations", {})
    if not isinstance(operations, dict):
        errors.append(f"{p}: operations must be object")
        continue
    for name, op in operations.items():
        transport = op.get("transport")
        if transport not in ALLOWED_TRANSPORTS:
            errors.append(f"{p}:{name}: unsupported transport {transport}")
        if op.get("timeoutMs", 3000) > 30000:
            errors.append(f"{p}:{name}: timeout > 30000ms")
        headers = op.get("headers", {})
        for hk, hv in headers.items():
            if hk.lower() in {"authorization","x-api-key","api-key"} and isinstance(hv, str):
                if not hv.startswith("@secret:") and "{{" not in hv:
                    errors.append(f"{p}:{name}: credential-like header must come from SecureStorage/template")
        request = op.get("request")
        if isinstance(request, str) and len(request) > 250000:
            errors.append(f"{p}:{name}: request template too large")

seen_profile_ids = set()
for entry in index.get("profiles", []):
    pid = entry.get("id")
    if not pid or pid in seen_profile_ids:
        errors.append(f"wifi/index.json: missing/duplicate profile id: {pid}")
        continue
    seen_profile_ids.add(pid)
    p = WIFI / entry.get("path", "")
    if not p.is_file():
        errors.append(f"profile {pid}: missing file {p}")
        continue
    profile = load(p)
    if not profile:
        continue
    if profile.get("id") != pid:
        errors.append(f"{p}: id differs from index")
    if profile.get("driverId") not in drivers:
        errors.append(f"{p}: unknown driverId {profile.get('driverId')}")
    if profile.get("deviceType") not in {"AirConditioner","Television"}:
        errors.append(f"{p}: unsupported deviceType {profile.get('deviceType')}")
    if not profile.get("manufacturer") or not profile.get("model"):
        errors.append(f"{p}: manufacturer/model required")
    match = profile.get("match", {})
    if not match.get("brand") and not match.get("modelPatterns"):
        errors.append(f"{p}: at least one match hint is required")
    walk_forbidden(profile, str(p.relative_to(ROOT)))

selftests = load(WIFI / "selftests.json")
if selftests:
    covered = set()
    for test in selftests.get("tests", []):
        did = test.get("driverId")
        covered.add(did)
        driver = drivers.get(did)
        if not driver:
            errors.append(f"selftest: unknown driver {did}")
            continue
        op = driver.get("operations", {}).get(test.get("operation"))
        if not op:
            errors.append(f"selftest {did}: operation missing")
            continue
        response = test.get("response")
        expected = test.get("expected", {})
        for state_name, expected_value in expected.items():
            expr = op.get("stateMap", {}).get(state_name)
            if not expr:
                errors.append(f"selftest {did}: missing stateMap for {state_name}")
                continue
            try:
                actual = extract_json_path(response, expr)
                if actual != expected_value:
                    errors.append(f"selftest {did}:{state_name}: expected {expected_value!r}, got {actual!r}")
            except Exception as ex:
                errors.append(f"selftest {did}:{state_name}: {ex}")
    for did, driver in drivers.items():
        if driver.get("status") == "software-validated" and driver.get("operations", {}).get("getState") and did not in covered:
            errors.append(f"driver {did}: software-validated driver requires offline getState self-test")

if errors:
    print("Wi-Fi DeviceDB validation FAILED")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print(f"Wi-Fi DeviceDB validation OK: {len(drivers)} drivers, {len(seen_profile_ids)} profiles")
