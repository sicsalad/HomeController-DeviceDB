#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
root=Path(__file__).resolve().parents[1]
images=root/'images'
required=(images/'REQUIRED_IMAGES.md').read_text(encoding='utf-8')
refs=sorted(set(re.findall(r'`((?:device-types|actions|states|properties|controls|branding)/[^`]+\.(?:svg|png|jpg|jpeg|webp))`', required)))
missing=[p for p in refs if not (images/p).exists()]
errors=[]
for p in images.rglob('*.svg'):
    text=p.read_text(encoding='utf-8')
    m=re.search(r'viewBox="([^"]+)"', text)
    if not m:
        errors.append(f'{p.relative_to(root)}: missing viewBox')
        continue
    rel=p.relative_to(images).as_posix()
    if rel.startswith(('device-types/','actions/','states/','properties/','controls/')) and m.group(1).strip()!='0 0 64 64':
        errors.append(f'{rel}: expected viewBox 0 0 64 64, got {m.group(1)}')
idx=json.loads((images/'index.json').read_text(encoding='utf-8'))
for item in idx.get('images',[]):
    path=item.get('path','')
    if path and not (images/path).exists():
        errors.append(f'index.json references missing file: {path}')
manifest=json.loads((images/'catalog.json').read_text(encoding='utf-8'))
for section in ('deviceTypes','actions','properties','states','branding','backgrounds'):
    for key,path in manifest.get(section,{}).items():
        if not (images/path).exists():
            errors.append(f'catalog.json {section}.{key} references missing file: {path}')
if missing:
    errors.extend(f'REQUIRED_IMAGES.md references missing file: {p}' for p in missing)
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'Image validation OK: {len(refs)} required icon refs, {sum(1 for _ in images.rglob("*.svg"))} SVG files; index.json and catalog.json paths verified.')
