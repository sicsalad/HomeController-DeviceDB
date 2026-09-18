#!/usr/bin/env python3
"""Enrich function-catalog.json from a locally downloaded Flipper-IRDB tree.
The normal DeviceDB generator is run first, then every local .ir file is scanned
without per-file network requests.
"""
from __future__ import annotations
import json, os, re, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'function-catalog.json'
FLIPPER=Path(os.environ.get('FLIPPER_IRDB_DIR','/tmp/flipper-irdb'))
ALIASES={
 'Power':['power_toggle','powertoggle','onoff','on_off','standby'],'PowerOn':['power_on','on'],'PowerOff':['power_off','off'],
 'VolumeUp':['volume_up','volup','vol_up','vol+','volume+'],'VolumeDown':['volume_down','voldown','vol_down','voldn','vol_dn','vol-','volume-'],'Mute':['volumemute','volume_mute'],
 'ChannelUp':['channel_up','chup','ch_up','ch+','channel+'],'ChannelDown':['channel_down','chdown','ch_down','chdn','ch_dn','ch-','channel-'],'PreviousChannel':['previous_channel','prevchannel','prev_channel','lastchannel','last_channel','last'],
 'Source':['input','inputsource','input_source','source_select'],'Ok':['enter','select','confirm','center'],'Back':['return','previous'],'Rewind':['rew','backward','fastbackward','fast_backward'],'FastForward':['fast_forward','ff','forward'],
 'Subtitle':['subtitles','sub'],'TeletextMix':['teletext_mix','teletext','text'],'Record':['rec'],'Tools':['settings','setting'],'Guide':['epg'],'Info':['display'],
 'FootballMode':['football','football_mode','soccer','soccer_mode','sports','sports_mode','sport_mode'],'Turbo':['turbo_mode'],'Powerful':['powerful_mode','power_mode'],'Economy':['eco','economy_mode','eco_mode'],'PowerSave':['power_save','energy_saving','energysaving'],
 'SelfClean':['self_clean','clean','cleaning'],'XFanCleaning':['x_fan','xfan','x_fan_cleaning'],'IFeel':['i_feel','follow_me','followme'],'SwingVertical':['swing_vertical','vertical_swing'],'SwingHorizontal':['swing_horizontal','horizontal_swing']}
def key(s): return ''.join(c.lower() for c in s if c.isalnum())
def pascal(s):
 p=[x for x in re.split(r'[^A-Za-z0-9]+',s) if x]
 return ''.join(x[:1].upper()+x[1:] for x in p) if len(p)>1 else (p[0][:1].upper()+p[0][1:] if p else '')
def dtype(path):
 parts=[x.lower() for x in path.parts]
 mapping=[('tv','television'),('television','television'),('air_conditioner','air-conditioner'),('ac','air-conditioner'),('fan','fan'),('projector','projector'),('audio','audio'),('soundbar','soundbar'),('receiver','receiver'),('stb','set-top-box'),('dvd','dvd-player'),('blu_ray','blu-ray-player'),('camera','camera'),('led','light'),('light','light'),('heater','heater'),('fireplace','fireplace')]
 for token,value in mapping:
  if any(token==p or token in p for p in parts[:-1]): return value
 return parts[-2] if len(parts)>1 else 'unknown'

# First refresh only from our own DeviceDB. This is fast and preserves old external entries.
subprocess.run([sys.executable,str(ROOT/'tools/generate_function_catalog.py')],cwd=ROOT,check=True)
doc=json.loads(OUT.read_text(encoding='utf-8')); functions=doc.get('functions',[])
by_id={f['id']:f for f in functions if f.get('id')}; alias_to_id={}
for f in functions:
 fid=f.get('id','')
 if fid:
  alias_to_id[key(fid)]=fid
  for a in f.get('aliases',[]): alias_to_id[key(a)]=fid
for fid,als in ALIASES.items():
 alias_to_id[key(fid)]=fid
 for a in als: alias_to_id[key(a)]=fid

files=list(FLIPPER.rglob('*.ir'))
print(f'Flipper ZIP local scan: {len(files)} .ir files')
for i,path in enumerate(files,1):
 try: lines=path.read_text(encoding='utf-8',errors='replace').splitlines()
 except OSError as ex: print(f'warning: {path}: {ex}'); continue
 typ=dtype(path.relative_to(FLIPPER))
 for line in lines:
  line=line.strip()
  if not line or line.startswith('#') or ':' not in line: continue
  k,v=line.split(':',1)
  if k.strip().lower()!='name' or not v.strip(): continue
  raw=v.strip(); fid=alias_to_id.get(key(raw)) or pascal(raw)
  if not fid: continue
  f=by_id.get(fid)
  if f is None:
   f={'id':fid,'aliases':[],'deviceTypes':[]}; functions.append(f); by_id[fid]=f; alias_to_id[key(fid)]=fid
  aliases=set(f.get('aliases',[])); aliases.add(raw); aliases.discard(fid); f['aliases']=sorted(aliases,key=str.lower)
  types=set(f.get('deviceTypes',[])); types.add(typ); f['deviceTypes']=sorted(types,key=str.lower)
 if i%1000==0: print(f'  scanned {i}/{len(files)}')

functions.sort(key=lambda f:f['id'].lower())
sources=list(doc.get('generatedFrom',[]))
if 'Lucaslhm/Flipper-IRDB' not in sources: sources.append('Lucaslhm/Flipper-IRDB')
doc['schemaVersion']=2; doc['generatedFrom']=sources; doc['functions']=functions
OUT.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(f'Generated {len(functions)} functions from local ZIP scan')
