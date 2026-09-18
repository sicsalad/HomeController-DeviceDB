#!/usr/bin/env python3
"""Build function-catalog.json from DeviceDB, optionally enriched from Flipper-IRDB."""
from __future__ import annotations
import argparse, json, re, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'function-catalog.json'
SCAN_DIRS=('ui-templates','ir','wifi','codesets','devices','generated','protocols'); SKIP={'function-catalog.json'}
FLIPPER_TREE_URL='https://api.github.com/repos/Lucaslhm/Flipper-IRDB/git/trees/main?recursive=1'; FLIPPER_RAW_BASE='https://raw.githubusercontent.com/Lucaslhm/Flipper-IRDB/main/'
ALIASES={
 'Power':['power_toggle','powertoggle','onoff','on_off','standby'],'PowerOn':['power_on','on'],'PowerOff':['power_off','off'],
 'VolumeUp':['volume_up','volup','vol_up','vol+','volume+'],'VolumeDown':['volume_down','voldown','vol_down','voldn','vol_dn','vol-','volume-'],'Mute':['volumemute','volume_mute'],
 'ChannelUp':['channel_up','chup','ch_up','ch+','channel+'],'ChannelDown':['channel_down','chdown','ch_down','chdn','ch_dn','ch-','channel-'],'PreviousChannel':['previous_channel','prevchannel','prev_channel','lastchannel','last_channel','last'],
 'Source':['input','inputsource','input_source','source_select'],'Ok':['enter','select','confirm','center'],'Back':['return','previous'],'Rewind':['rew','backward','fastbackward','fast_backward'],'FastForward':['fast_forward','ff','forward'],
 'Subtitle':['subtitles','sub'],'TeletextMix':['teletext_mix','teletext','text'],'Record':['rec'],'Tools':['settings','setting'],'Guide':['epg'],'Info':['display'],
 'FootballMode':['football','football_mode','soccer','soccer_mode','sports','sports_mode','sport_mode'],'Turbo':['turbo_mode'],'Powerful':['powerful_mode','power_mode'],'Economy':['eco','economy_mode','eco_mode'],'PowerSave':['power_save','energy_saving','energysaving'],
 'SelfClean':['self_clean','clean','cleaning'],'XFanCleaning':['x_fan','xfan','x_fan_cleaning'],'IFeel':['i_feel','follow_me','followme'],'SwingVertical':['swing_vertical','vertical_swing'],'SwingHorizontal':['swing_horizontal','horizontal_swing'],
 'FanSpeed':['fan_speed'],'FanSpeedAuto':['fan_speed_auto','fan_auto'],'FanSpeedUp':['fan_speed_up','fan_up'],'FanSpeedDown':['fan_speed_down','fan_down'],'TemperatureUp':['temperature_up','tempup','temp_up','temp+'],'TemperatureDown':['temperature_down','tempdown','temp_down','temp-']}

def key(s):return ''.join(c.lower() for c in s if c.isalnum())
def pascal(s):
 p=[x for x in re.split(r'[^A-Za-z0-9]+',s) if x]
 return ''.join(x[:1].upper()+x[1:] for x in p) if len(p)>1 else (p[0][:1].upper()+p[0][1:] if p else '')
def device_types(obj,path):
 out=set();
 if isinstance(obj,dict):
  for k in ('deviceTypeId','deviceType'):
   v=obj.get(k)
   if isinstance(v,str) and v:out.add(v)
  if isinstance(obj.get('deviceTypes'),list):out.update(str(x) for x in obj['deviceTypes'] if x)
 p=str(path).replace('\\','/').lower()
 if 'television' in p or '-tv-' in p or '/tv' in p:out.add('television')
 if 'air-condition' in p or '/climate/' in p or '-ac-' in p:out.add('air-conditioner')
 if 'fan' in p:out.add('fan')
 if 'ir-transceiver' in p:out.add('ir-transceiver')
 return out
def walk(obj,types,found):
 if isinstance(obj,dict):
  local=types|device_types(obj,Path(''))
  for k,v in obj.items():
   kl=k.lower()
   if kl in ('command','canonicalcommand','function','functioncode','action') and isinstance(v,str):found.append((v,local))
   elif kl in ('capabilities','commands','functions','testcommands') and isinstance(v,list):
    for x in v: found.append((x,local)) if isinstance(x,str) else walk(x,local,found)
   elif kl=='operations' and isinstance(v,dict):
    for op in v:found.append((op,local))
    walk(v,local,found)
   else:walk(v,local,found)
 elif isinstance(obj,list):
  for x in obj:walk(x,types,found)
def fetch_json(url):
 req=urllib.request.Request(url,headers={'User-Agent':'HomeController-DeviceDB-function-catalog'});return json.load(urllib.request.urlopen(req,timeout=60))
def fetch_text(url):
 req=urllib.request.Request(url,headers={'User-Agent':'HomeController-DeviceDB-function-catalog'});return urllib.request.urlopen(req,timeout=60).read().decode('utf-8','replace')
def flipper_type(path):
 p=path.lower().replace('\\','/');parts=[x for x in p.split('/') if x]
 mapping=[('tv','television'),('television','television'),('air_conditioner','air-conditioner'),('ac','air-conditioner'),('fan','fan'),('projector','projector'),('audio','audio'),('soundbar','soundbar'),('receiver','receiver'),('stb','set-top-box'),('dvd','dvd-player'),('blu_ray','blu-ray-player'),('camera','camera'),('led','light'),('light','light'),('heater','heater'),('fireplace','fireplace')]
 for token,dtype in mapping:
  if token in parts or any(token in x for x in parts[:-1]):return dtype
 return parts[0] if parts else 'unknown'
def scan_flipper(found):
 tree=fetch_json(FLIPPER_TREE_URL);paths=[x['path'] for x in tree.get('tree',[]) if x.get('type')=='blob' and x.get('path','').lower().endswith('.ir')];print(f'Flipper-IRDB: {len(paths)} .ir files')
 for i,path in enumerate(paths,1):
  try:text=fetch_text(FLIPPER_RAW_BASE+path)
  except Exception as ex:print(f'warning: {path}: {ex}');continue
  for line in text.splitlines():
   line=line.strip()
   if line and not line.startswith('#') and ':' in line:
    k,v=line.split(':',1)
    if k.strip().lower()=='name' and v.strip():found.append((v.strip(),{flipper_type(path)}))
  if i%500==0:print(f'  scanned {i}/{len(paths)}')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--include-flipper',action='store_true');args=ap.parse_args()
 old=json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else {'functions':[]};old_by_key={key(f['id']):f for f in old.get('functions',[]) if f.get('id')};alias_to_id={}
 for f in old.get('functions',[]):
  fid=f.get('id','')
  if fid:
   alias_to_id[key(fid)]=fid
   for a in f.get('aliases',[]):alias_to_id[key(a)]=fid
 for fid,als in ALIASES.items():
  alias_to_id[key(fid)]=fid
  for a in als:alias_to_id[key(a)]=fid
 files=[]
 for d in SCAN_DIRS:
  b=ROOT/d
  if b.exists():files.extend(b.rglob('*.json'))
 files += [ROOT/x for x in ('database.json','catalog-v2.json','curated-database.json','device-types.json') if (ROOT/x).exists()]
 found=[]
 for path in sorted(set(files)):
  if path.name in SKIP:continue
  try:obj=json.loads(path.read_text(encoding='utf-8-sig'))
  except Exception:continue
  walk(obj,device_types(obj,path) if isinstance(obj,dict) else set(),found)
 if args.include_flipper:scan_flipper(found)
 usage={};observed={}
 for raw,types in found:
  raw=raw.strip()
  if not raw or raw.startswith(('http://','https://')):continue
  fid=alias_to_id.get(key(raw)) or pascal(raw)
  if fid:usage.setdefault(fid,set()).update(types);observed.setdefault(fid,set()).add(raw)
 # Preserve all existing entries, including Flipper discoveries, during cheap local-only runs.
 ids=set(usage)|{f.get('id') for f in old.get('functions',[]) if f.get('id')}|set(ALIASES);functions=[]
 for fid in sorted(ids,key=lambda x:x.lower()):
  oldf=old_by_key.get(key(fid),{});aliases=set(oldf.get('aliases',[]))|set(ALIASES.get(fid,[]))|observed.get(fid,set());aliases.discard(fid)
  spaced=re.sub(r'(?<!^)(?=[A-Z])',' ',fid);aliases.update([fid.lower(),spaced.replace(' ','_').lower()]);aliases={a for a in aliases if a and (key(a)!=key(fid) or a.lower()!=fid.lower())}
  # Local scan refreshes local usage but retains external device types already learned from Flipper.
  oldtypes=set(oldf.get('deviceTypes',[]));types=usage.get(fid,set())|oldtypes
  functions.append({'id':fid,'aliases':sorted(aliases,key=str.lower),'deviceTypes':sorted(types,key=str.lower)})
 sources=['ui-templates','ir','wifi','codesets','devices','generated','protocols','database.json','catalog-v2.json','curated-database.json','device-types.json']
 if args.include_flipper or 'Lucaslhm/Flipper-IRDB' in old.get('generatedFrom',[]):sources.append('Lucaslhm/Flipper-IRDB')
 OUT.write_text(json.dumps({'schemaVersion':2,'generatedFrom':sources,'functions':functions},indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(f'Generated {len(functions)} functions; Flipper scan={args.include_flipper}')
if __name__=='__main__':main()
