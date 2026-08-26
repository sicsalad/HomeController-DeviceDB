#!/usr/bin/env python3
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
WIFI = ROOT / "wifi"
ALLOWED_TRANSPORTS = {"udp","udp-unicast","udp-broadcast","tcp","http","https","websocket","websocket-secure","wss","webos-ssap","webos-ssap-button"}
ALLOWED_STATUS = {"stable","experimental","software-validated"}
FORBIDDEN_KEYS = {"script","javascript","csharp","assembly","eval","exec","nativeLibrary"}
errors=[]

def load(path):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception as ex: errors.append(f"{path}: invalid JSON: {ex}"); return None

def extract_json_path(obj, expr):
    if not isinstance(expr,str) or not expr.startswith("json:"): raise ValueError(f"unsupported expression: {expr}")
    cur=obj
    for part in expr[5:].lstrip("$.").split("."):
        if not part: continue
        if not isinstance(cur,dict) or part not in cur: raise KeyError(part)
        cur=cur[part]
    return cur

def expand(template,variables): return re.sub(r"\{\{([A-Za-z0-9_.-]+)\}\}",lambda m:str(variables.get(m.group(1),"")),template or "")
def wildcard(value,pattern): return re.fullmatch(re.escape(pattern).replace(r"\*",".*"),value,re.I) is not None

def walk_forbidden(value,path=""):
    if isinstance(value,dict):
        for k,v in value.items():
            if k in FORBIDDEN_KEYS: errors.append(f"{path}: forbidden executable field '{k}'")
            walk_forbidden(v,f"{path}.{k}" if path else k)
    elif isinstance(value,list):
        for i,v in enumerate(value): walk_forbidden(v,f"{path}[{i}]")

def validate_capabilities(profile,path):
    dtype=profile.get("deviceType")
    if dtype=="AirConditioner":
        caps=profile.get("climateCapabilities")
        if not isinstance(caps,dict): errors.append(f"{path}: climateCapabilities object required"); return
        temp=caps.get("targetTemperature")
        if temp:
            vals=(temp.get("min"),temp.get("max"),temp.get("step"))
            if not all(isinstance(x,(int,float)) for x in vals) or vals[0]>=vals[1] or vals[2]<=0: errors.append(f"{path}: invalid targetTemperature capability")
    elif dtype=="Television":
        if not isinstance(profile.get("tvCapabilities"),dict): errors.append(f"{path}: tvCapabilities object required")
    # Repository-defined device types may use their UI template controls as capabilities.

index=load(WIFI/"index.json")
if not index: sys.exit(1)
if index.get("schemaVersion")!=1: errors.append("wifi/index.json: schemaVersion must be 1")
drivers={}; profiles={}; seen_driver_ids=set(); seen_profile_ids=set()

for entry in index.get("drivers",[]):
    did=entry.get("id")
    if not did or did in seen_driver_ids: errors.append(f"wifi/index.json: missing/duplicate driver id: {did}"); continue
    seen_driver_ids.add(did); p=WIFI/entry.get("path","")
    if not p.is_file(): errors.append(f"driver {did}: missing file {p}"); continue
    d=load(p)
    if not d: continue
    drivers[did]=d
    if d.get("id")!=did: errors.append(f"{p}: id differs from index")
    if d.get("schemaVersion")!=1: errors.append(f"{p}: schemaVersion must be 1")
    if not isinstance(d.get("minimumRuntimeVersion",1),int): errors.append(f"{p}: minimumRuntimeVersion must be integer")
    if d.get("status") not in ALLOWED_STATUS: errors.append(f"{p}: unsupported status {d.get('status')}")
    types=d.get("deviceTypes")
    if not isinstance(types,list) or not types or any(not isinstance(x,str) or not x.strip() for x in types): errors.append(f"{p}: deviceTypes must be non-empty strings")
    walk_forbidden(d,str(p.relative_to(ROOT)))
    ops=d.get("operations",{})
    if not isinstance(ops,dict): errors.append(f"{p}: operations must be object"); continue
    for name,op in ops.items():
        tr=op.get("transport")
        if tr not in ALLOWED_TRANSPORTS: errors.append(f"{p}:{name}: unsupported transport {tr}")
        if op.get("timeoutMs",3000)>30000: errors.append(f"{p}:{name}: timeout > 30000ms")
        if op.get("retryCount",1)>5: errors.append(f"{p}:{name}: retryCount > 5")
        for hk,hv in op.get("headers",{}).items():
            if hk.lower() in {"authorization","x-api-key","api-key"} and isinstance(hv,str) and not hv.startswith("@secret:") and "{{" not in hv: errors.append(f"{p}:{name}: credential-like header must be secret/template")
        if isinstance(op.get("request"),str) and len(op["request"])>250000: errors.append(f"{p}:{name}: request template too large")

for entry in index.get("profiles",[]):
    pid=entry.get("id")
    if not pid or pid in seen_profile_ids: errors.append(f"wifi/index.json: missing/duplicate profile id: {pid}"); continue
    seen_profile_ids.add(pid); p=WIFI/entry.get("path","")
    if not p.is_file(): errors.append(f"profile {pid}: missing file {p}"); continue
    profile=load(p)
    if not profile: continue
    profiles[pid]=profile
    if profile.get("id")!=pid: errors.append(f"{p}: id differs from index")
    if profile.get("driverId") not in drivers: errors.append(f"{p}: unknown driverId {profile.get('driverId')}")
    if not isinstance(profile.get("deviceType"),str) or not profile.get("deviceType","").strip(): errors.append(f"{p}: deviceType must be a non-empty string")
    if not profile.get("manufacturer") or not profile.get("model"): errors.append(f"{p}: manufacturer/model required")
    match=profile.get("match",{})
    if not match.get("brand") and not match.get("modelPatterns"): errors.append(f"{p}: at least one match hint required")
    validate_capabilities(profile,p); walk_forbidden(profile,str(p.relative_to(ROOT)))

suite=load(WIFI/"validation-suite.json")
if not suite: errors.append("wifi/validation-suite.json required")
else:
    covered=set()
    for test in suite.get("stateTests",[]):
        did=test.get("driverId"); covered.add(did); driver=drivers.get(did)
        if not driver: errors.append(f"stateTest {test.get('name')}: unknown driver {did}"); continue
        op=driver.get("operations",{}).get(test.get("operation"))
        if not op: errors.append(f"stateTest {did}: operation missing"); continue
        for state_name,expected in test.get("expected",{}).items():
            expr=op.get("stateMap",{}).get(state_name)
            if not expr: errors.append(f"stateTest {did}: missing stateMap {state_name}"); continue
            try:
                actual=extract_json_path(test.get("response"),expr)
                if actual!=expected: errors.append(f"stateTest {did}/{test.get('name')}:{state_name}: expected {expected!r}, got {actual!r}")
            except Exception as ex: errors.append(f"stateTest {did}/{test.get('name')}:{state_name}: {ex}")
    for test in suite.get("commandTests",[]):
        did=test.get("driverId"); driver=drivers.get(did); op=(driver or {}).get("operations",{}).get(test.get("operation"))
        if not driver: errors.append(f"commandTest: unknown driver {did}"); continue
        if not op: errors.append(f"commandTest {did}: operation missing"); continue
        rendered=expand(op.get("request",""),test.get("variables",{}))
        for expected in test.get("expectedRequestContains",[]):
            if expected not in rendered: errors.append(f"commandTest {did}/{test.get('operation')}: request missing {expected!r}")
    for test in suite.get("negativeTests",[]):
        driver=drivers.get(test.get("driverId")); op=(driver or {}).get("operations",{}).get(test.get("operation"),{})
        for state_name in test.get("missingExpected",[]):
            expr=op.get("stateMap",{}).get(state_name)
            try: extract_json_path(test.get("response"),expr); errors.append(f"negativeTest {test.get('name')}: {state_name} unexpectedly resolved")
            except Exception: pass
    def score_profile(p,brand,model):
        m=p.get("match",{}); score=0
        if any(brand.lower()==b.lower() for b in m.get("brand",[])): score+=40
        if any(wildcard(model,pat) for pat in m.get("modelPatterns",[])): score+=60
        return score
    for test in suite.get("profileSelectionTests",[]):
        candidates=[p for p in profiles.values() if p.get("deviceType")==test.get("deviceType")]
        ranked=sorted(candidates,key=lambda p:score_profile(p,test.get("brand",""),test.get("model","")),reverse=True)
        winner=ranked[0].get("id") if ranked and score_profile(ranked[0],test.get("brand",""),test.get("model",""))>0 else None
        if winner!=test.get("expectedProfileId"): errors.append(f"profileSelection {test.get('brand')} {test.get('model')}: expected {test.get('expectedProfileId')}, got {winner}")
    base=suite.get("regressionBaseline",{})
    for did in base.get("requiredDriverIds",[]):
        if did not in drivers: errors.append(f"regression: required driver removed: {did}")
    for pid in base.get("requiredProfileIds",[]):
        if pid not in profiles: errors.append(f"regression: required profile removed: {pid}")
    for did,d in drivers.items():
        if d.get("status")=="software-validated" and d.get("operations",{}).get("getState") and did not in covered: errors.append(f"driver {did}: software-validated requires state fixture")

if errors:
    print("Wi-Fi DeviceDB validation FAILED")
    for e in errors: print(" -",e)
    sys.exit(1)
print(f"Wi-Fi DeviceDB validation OK: {len(drivers)} drivers, {len(profiles)} profiles, comprehensive regression suite passed")
