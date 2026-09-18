#!/usr/bin/env python3
"""Build function-catalog.json from every command/capability in DeviceDB plus Flipper-IRDB.

Sources: UI templates, IR runtime/codesets, Wi-Fi protocols/profiles, legacy/device
catalogs and every .ir file reachable in Lucaslhm/Flipper-IRDB. Existing aliases
are preserved. Each function records all device types in which it is used.
"""
from __future__ import annotations
import json, re, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'function-catalog.json'
SCAN_DIRS=('ui-templates','ir','wifi','codesets','devices','generated','protocols')
SKIP={'function-catalog.json'}
FLIPPER_TREE_URL='https://api.github.com/repos/Lucaslhm/Flipper-IRDB/git/trees/main?recursive=1'
FLIPPER_RAW_BASE='https://raw.githubusercontent.com/Lucaslhm/Flipper-IRDB/main/'

ALIASES={
 'Power':['power_toggle','powertoggle','onoff','on_off','standby'],
 'PowerOn':['power_on','on'], 'PowerOff':['power_off','off'],
 'VolumeUp':['volume_up','volup','vol_up','vol+','volume+'],
 'VolumeDown':['volume_down','voldown','vol_down','voldn','vol_dn','vol-','volume-'],
 'Mute':['volumemute','volume_mute'],
 'ChannelUp':['channel_up','chup','ch_up','ch+','channel+'],
 'ChannelDown':['channel_down','chdown','ch_down','chdn','ch_dn','ch-','channel-'],
 'PreviousChannel':['previous_channel','prevchannel','prev_channel','lastchannel','last_channel','last'],
 'Source':['input','inputsource','input_source','source_select'],
 'Ok':['enter','select','confirm','center'], 'Back':['return','previous'],
 'Rewind':['rew','backward','fastbackward','fast_backward'],
 'FastForward':['fast_forward','ff','forward'],
 'Subtitle':['subtitles','sub'], 'TeletextMix':['teletext_mix','teletext','text'],
 'Record':['rec'], 'Tools':['settings','setting'], 'Guide':['epg'], 'Info':['display'],
 'FootballMode':['football','football_mode','soccer','soccer_mode','sports','sports_mode','sport_mode'],
 'Turbo':['turbo_mode'], 'Powerful':['powerful_mode','power_mode'],
 'Economy':['eco','economy_mode','eco_mode'], 'PowerSave':['power_save','energy_saving','energysaving'],
 'SelfClean':['self_clean','clean','cleaning'], 'XFanCleaning':['x_fan','xfan','x_fan_cleaning'],
 'IFeel':['i_feel','follow_me','followme'],
 'SwingVertical':['swing_vertical','vertical_swing'], 'SwingHorizontal':['swing_horizontal','horizontal_swing'],
 'FanSpeed':['fan_speed'], 'FanSpeedAuto':['fan_speed_auto','fan_auto'],
 'FanSpeedUp':['fan_speed_up','fan_up'], 'FanSpeedDown':['fan_speed_down','fan_down'],
 'TemperatureUp':['temperature_up','tempup','temp_up','temp+'],
 'TemperatureDown':['temperature_down','tempdown','temp_down','temp-'],
}

def key(s:str)->str:return ''.join(c.lower() for c in s if c.isalnum())
def pascal(s:str)->str:
    parts=[p for p in re.split(r'[^A-Za-z0-9]+',s) if p]
    if len(parts)>1:return ''.join(p[:1].upper()+p[1:] for p in parts)
    if not parts:return ''
    p=parts[0]
    return p[:1].upper()+p[1:]

def device_types(obj,path:Path)->set[str]:
    out=set()
    for k in ('deviceTypeId','deviceType'):
        v=obj.get(k) if isinstance(obj,dict) else None
        if isinstance(v,str) and v: out.add(v)
    v=obj.get('deviceTypes') if isinstance(obj,dict) else None
    if isinstance(v,list):out.update(str(x) for x in v if x)
    p=str(path).replace('\\','/').lower()
    if 'television' in p or '-tv-' in p or '/tv' in p:out.add('television')
    if 'air-condition' in p or '/climate/' in p or '-ac-' in p:out.add('air-conditioner')
    if 'fan' in p:out.add('fan')
    if 'ir-transceiver' in p:out.add('ir-transceiver')
    return out

def flipper_type_from_path(path:str)->str:
    p=path.lower().replace('\\','/')
    mapping=[
        ('tv','television'),('television','television'),('air_conditioner','air-conditioner'),('air conditioner','air-conditioner'),
        ('ac','air-conditioner'),('fan','fan'),('projector','projector'),('audio','audio'),('soundbar','soundbar'),
        ('receiver','receiver'),('stb','set-top-box'),('set_top_box','set-top-box'),('dvd','dvd-player'),('blu_ray','blu-ray-player'),
        ('camera','camera'),('led','light'),('light','light'),('heater','heater'),('fireplace','fireplace')]
    parts=[x for x in p.split('/') if x]
    for token,dtype in mapping:
        if token in parts or any(token in part for part in parts[:-1]): return dtype
    return parts[0] if parts else 'unknown'

def walk(obj,types:set[str],found:list[tuple[str,set[str]]]):
    if isinstance(obj,dict):
        local=types|device_types(obj,Path(''))
        for k,v in obj.items():
            kl=k.lower()
            if kl in ('command','canonicalcommand','function','functioncode','action') and isinstance(v,str):found.append((v,local))
            elif kl in ('capabilities','commands','functions','testcommands') and isinstance(v,list):
                for x in v:
                    if isinstance(x,str):found.append((x,local))
                    else:walk(x,local,found)
            elif kl=='operations' and isinstance(v,dict):
                for op in v:found.append((op,local))
                walk(v,local,found)
            else:walk(v,local,found)
    elif isinstance(obj,list):
        for x in obj:walk(x,types,found)

def fetch_json(url:str):
    req=urllib.request.Request(url,headers={'User-Agent':'HomeController-DeviceDB-function-catalog'})
    with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)

def fetch_text(url:str)->str:
    req=urllib.request.Request(url,headers={'User-Agent':'HomeController-DeviceDB-function-catalog'})
    with urllib.request.urlopen(req,timeout=60) as r:return r.read().decode('utf-8','replace')

def scan_flipper(found:list[tuple[str,set[str]]]):
    tree=fetch_json(FLIPPER_TREE_URL)
    ir_paths=[x['path'] for x in tree.get('tree',[]) if x.get('type')=='blob' and x.get('path','').lower().endswith('.ir')]
    print(f'Flipper-IRDB: {len(ir_paths)} .ir files')
    for i,path in enumerate(ir_paths,1):
        try:text=fetch_text(FLIPPER_RAW_BASE+path)
        except Exception as ex:
            print(f'warning: cannot read Flipper file {path}: {ex}')
            continue
        dtype=flipper_type_from_path(path)
        types={dtype}
        for line in text.splitlines():
            line=line.strip()
            if not line or line.startswith('#') or ':' not in line:continue
            k,v=line.split(':',1)
            if k.strip().lower()=='name':
                name=v.strip()
                if name:found.append((name,types))
        if i%500==0:print(f'  scanned {i}/{len(ir_paths)} Flipper files')

def main():
    old=json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else {'functions':[]}
    old_by_key={key(f['id']):f for f in old.get('functions',[]) if f.get('id')}
    alias_to_id={}
    for f in old.get('functions',[]):
        fid=f.get('id','')
        if fid:
            alias_to_id[key(fid)]=fid
            for a in f.get('aliases',[]):alias_to_id[key(a)]=fid
    for fid,als in ALIASES.items():
        alias_to_id[key(fid)]=fid
        for a in als:alias_to_id[key(a)]=fid

    usage:dict[str,set[str]]={}
    observed:dict[str,set[str]]={}
    files=[]
    for d in SCAN_DIRS:
        base=ROOT/d
        if base.exists():files.extend(base.rglob('*.json'))
    files += [ROOT/x for x in ('database.json','catalog-v2.json','curated-database.json','device-types.json') if (ROOT/x).exists()]
    found=[]
    for path in sorted(set(files)):
        if path.name in SKIP:continue
        try:obj=json.loads(path.read_text(encoding='utf-8-sig'))
        except Exception:continue
        base_types=device_types(obj,path) if isinstance(obj,dict) else set()
        walk(obj,base_types,found)

    scan_flipper(found)

    for raw,types in found:
        raw=raw.strip()
        if not raw or raw.startswith(('http://','https://')):continue
        fid=alias_to_id.get(key(raw)) or pascal(raw)
        if not fid:continue
        usage.setdefault(fid,set()).update(types)
        observed.setdefault(fid,set()).add(raw)

    ids=set(usage)|{f.get('id') for f in old.get('functions',[]) if f.get('id')}|set(ALIASES)
    functions=[]
    for fid in sorted(ids,key=lambda x:x.lower()):
        oldf=old_by_key.get(key(fid),{})
        aliases=set(oldf.get('aliases',[]))|set(ALIASES.get(fid,[]))|observed.get(fid,set())
        aliases.discard(fid)
        spaced=re.sub(r'(?<!^)(?=[A-Z])',' ',fid)
        underscored=spaced.replace(' ','_').lower()
        aliases.update([fid.lower(),underscored])
        aliases={a for a in aliases if a and (key(a)!=key(fid) or a.lower()!=fid.lower())}
        functions.append({'id':fid,'aliases':sorted(aliases,key=str.lower),'deviceTypes':sorted(usage.get(fid,set()),key=str.lower)})
    OUT.write_text(json.dumps({'schemaVersion':2,'generatedFrom':['ui-templates','ir','wifi','codesets','devices','generated','protocols','database.json','catalog-v2.json','curated-database.json','device-types.json','Lucaslhm/Flipper-IRDB'],'functions':functions},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Generated {len(functions)} canonical functions from {len(set(files))} local JSON files plus Flipper-IRDB')

if __name__=='__main__':main()
