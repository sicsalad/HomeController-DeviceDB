#!/usr/bin/env python3
"""Generate the compact, manually reorderable feature list used by IR learning UIs.

Each feature is deliberately written on exactly one line so the display order can
be changed later simply by moving lines in learning-feature-order.json.
Device types are taken from the generated function-catalog.json.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'function-catalog.json'
OUT = ROOT / 'learning-feature-order.json'

# This list is the canonical learning-page order. Keep the most important remote
# controls first; climate/special functions follow the general TV/audio controls.
ORDER = [
    'Power', 'PowerOn', 'PowerOff',
    'VolumeUp', 'VolumeDown', 'Mute',
    'ChannelUp', 'ChannelDown', 'PreviousChannel',
    'Source',
    'Up', 'Down', 'Left', 'Right', 'Ok', 'Back', 'Home', 'Menu',
    'Guide', 'Info', 'Tools',
    'Play', 'Pause', 'PlayPause', 'Stop', 'Rewind', 'FastForward', 'Previous', 'Next', 'Record',
    'Digit0', 'Digit1', 'Digit2', 'Digit3', 'Digit4', 'Digit5', 'Digit6', 'Digit7', 'Digit8', 'Digit9',
    'Red', 'Green', 'Yellow', 'Blue',
    'Subtitle', 'TeletextMix',
    'TemperatureUp', 'TemperatureDown',
    'FanSpeed', 'FanSpeedAuto', 'FanSpeedUp', 'FanSpeedDown',
    'SwingVertical', 'SwingHorizontal',
    'Turbo', 'Powerful', 'Economy', 'PowerSave',
    'IFeel', 'SelfClean', 'XFanCleaning',
    'FootballMode',
]

doc = json.loads(SOURCE.read_text(encoding='utf-8'))
by_id = {f.get('id'): f for f in doc.get('functions', []) if f.get('id')}

features = []
for fid in ORDER:
    f = by_id.get(fid)
    if f is None:
        continue
    features.append({'id': fid, 'deviceTypes': sorted(set(f.get('deviceTypes', [])), key=str.lower)})

# Add no arbitrary Flipper names here: this file intentionally contains only the
# centralized/canonical learning features listed above.
lines = [
    '{',
    '  "schemaVersion": 1,',
    '  "purpose": "Canonical feature order for device learning pages",',
    '  "features": ['
]
for i, feature in enumerate(features):
    comma = ',' if i < len(features) - 1 else ''
    lines.append('    ' + json.dumps(feature, ensure_ascii=False, separators=(',', ':')) + comma)
lines += ['  ]', '}', '']
OUT.write_text('\n'.join(lines), encoding='utf-8')
print(f'Generated {len(features)} ordered learning features -> {OUT.name}')
