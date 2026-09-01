#!/usr/bin/env python3
import json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
errors=[]

def load(path):
    try:return json.loads(path.read_text(encoding='utf-8'))
    except Exception as ex:errors.append(f'{path}: invalid JSON: {ex}');return None

catalog=load(ROOT/'device-types.json')
if not catalog:sys.exit(1)
if catalog.get('schemaVersion')!=1:errors.append('device-types.json: schemaVersion must be 1')
connections={'infrared','wifi','bluetooth'}
types={}
for item in catalog.get('deviceTypes',[]):
    tid=item.get('id')
    if not tid or tid in types:errors.append(f'device-types.json: missing/duplicate id {tid}');continue
    if not item.get('displayName'):errors.append(f'device type {tid}: displayName required')
    c=item.get('connections',[])
    if not c or any(x not in connections for x in c):errors.append(f'device type {tid}: invalid connections {c}')
    types[tid]=item

idx=load(ROOT/'ui-templates'/'index.json')
if not idx:errors.append('ui-templates/index.json required');idx={}
if idx.get('schemaVersion')!=1:errors.append('ui-templates/index.json: schemaVersion must be 1')
seen=set();templates={}
allowed_renderers={'declarative','builtin-ir-ac','builtin-ir-tv','builtin-ir-simple','builtin-hubitat','builtin-hue','builtin-wifi-ac','builtin-dashboard'}
allowed_controls={'button','tile','toggle','stepper','slider','picker'}
for entry in idx.get('templates',[]):
    tid=entry.get('id');path=ROOT/'ui-templates'/entry.get('path','')
    if not tid or tid in seen:errors.append(f'ui template index: missing/duplicate id {tid}');continue
    seen.add(tid)
    if not path.is_file():errors.append(f'ui template {tid}: missing {path}');continue
    t=load(path)
    if not t:continue
    templates[tid]=t
    if t.get('id')!=tid:errors.append(f'{path}: id differs from index')
    if t.get('schemaVersion')!=1:errors.append(f'{path}: schemaVersion must be 1')
    dtype=t.get('deviceTypeId')
    if dtype not in types:errors.append(f'{path}: unknown deviceTypeId {dtype}')
    tc=t.get('connections',[])
    if not tc or any(x not in connections for x in tc):errors.append(f'{path}: invalid connections')
    if dtype in types and any(x not in types[dtype].get('connections',[]) for x in tc):errors.append(f'{path}: template connection not supported by device type')
    renderer=t.get('renderer','declarative')
    if renderer not in allowed_renderers:errors.append(f'{path}: unsupported renderer {renderer}')
    if renderer=='declarative':
        if not t.get('sections'):errors.append(f'{path}: declarative template requires sections')
        columns=max(1,int(t.get('columns',3)))
        for section in t.get('sections',[]):
            for control in section.get('controls',[]):
                ctype=control.get('type','button')
                if ctype not in allowed_controls:errors.append(f'{path}: unsupported control type {ctype}')
                if not control.get('command'):errors.append(f'{path}: control command required')
                span=int(control.get('columnSpan',1))
                if span<1 or span>columns:errors.append(f'{path}: invalid columnSpan {span}')
                if ctype=='picker' and not control.get('options'):errors.append(f'{path}: picker requires options')
                if ctype in {'stepper','slider'}:
                    lo=control.get('minimum',0);hi=control.get('maximum',100)
                    if lo>=hi:errors.append(f'{path}: {ctype} minimum must be lower than maximum')

for dtype,item in types.items():
    for connection,template_id in item.get('defaultUiTemplates',{}).items():
        if connection not in item.get('connections',[]):errors.append(f'device type {dtype}: default UI for unsupported connection {connection}')
        t=templates.get(template_id)
        if not t:errors.append(f'device type {dtype}: missing default UI template {template_id}')
        elif t.get('deviceTypeId')!=dtype:errors.append(f'device type {dtype}: default UI {template_id} belongs to {t.get("deviceTypeId")}')

if errors:
    print('Device/UI catalog validation FAILED')
    for e in errors:print(' -',e)
    sys.exit(1)
print(f'Device/UI catalog validation OK: {len(types)} types, {len(templates)} templates')