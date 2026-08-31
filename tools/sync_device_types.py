#!/usr/bin/env python3
"""Synchronize HomeController IR device types with Flipper-IRDB top-level categories.

Device types are metadata only: stable HomeController ids, localized display names,
a single icon and the upstream Flipper category aliases. Existing curated HomeController
entries are preserved; Flipper categories are added/updated as infrared-capable types.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SPECIAL_IDS = {
    "ACs": "air-conditioner",
    "Air_Purifiers": "air-purifier",
    "Audio_and_Video_Receivers": "av-receiver",
    "Blu-Ray": "blu-ray-player",
    "CD_Players": "cd-player",
    "Cable_Boxes": "set-top-box",
    "Car_Multimedia": "car-multimedia",
    "DVD_Players": "dvd-player",
    "Digital_Signs": "digital-sign",
    "Dust_Collectors": "dust-collector",
    "Fans": "fan",
    "Handicap_Ceiling_Lifts": "ceiling-lift",
    "Head_Units": "head-unit",
    "Heaters": "heater",
    "Humidifiers": "humidifier",
    "LED_Lighting": "light",
    "MiniDisc": "minidisc",
    "Picture_Frames": "digital-picture-frame",
    "Projectors": "projector",
    "SoundBars": "soundbar",
    "Streaming_Devices": "streaming-device",
    "TV_Tuner": "tv-tuner",
    "TVs": "television",
}

# en, hu, de, fr, ru. Unknown future Flipper folders still get a stable id and
# a readable fallback; adding a translation here later does not change identity.
NAMES = {
    "air-conditioner": ("Air Conditioner", "Légkondicionáló", "Klimaanlage", "Climatiseur", "Кондиционер"),
    "air-purifier": ("Air Purifier", "Légtisztító", "Luftreiniger", "Purificateur d’air", "Очиститель воздуха"),
    "av-receiver": ("AV Receiver", "AV-erősítő", "AV-Receiver", "Ampli-tuner AV", "AV-ресивер"),
    "bidet": ("Bidet", "Bidé", "Bidet", "Bidet", "Биде"),
    "blu-ray-player": ("Blu-ray Player", "Blu-ray lejátszó", "Blu-ray-Player", "Lecteur Blu-ray", "Blu-ray проигрыватель"),
    "cctv": ("CCTV", "Biztonsági kamera", "Überwachungskamera", "Vidéosurveillance", "Видеонаблюдение"),
    "cd-player": ("CD Player", "CD-lejátszó", "CD-Player", "Lecteur CD", "CD-проигрыватель"),
    "set-top-box": ("Set-top Box", "Beltéri egység", "Set-Top-Box", "Décodeur TV", "ТВ-приставка"),
    "camera": ("Camera", "Kamera", "Kamera", "Caméra", "Камера"),
    "cameras": ("Camera", "Kamera", "Kamera", "Caméra", "Камера"),
    "car-multimedia": ("Car Multimedia", "Autós multimédia", "Auto-Multimedia", "Multimédia automobile", "Автомультимедиа"),
    "clock": ("Clock", "Óra", "Uhr", "Horloge", "Часы"),
    "clocks": ("Clock", "Óra", "Uhr", "Horloge", "Часы"),
    "computer": ("Computer", "Számítógép", "Computer", "Ordinateur", "Компьютер"),
    "computers": ("Computer", "Számítógép", "Computer", "Ordinateur", "Компьютер"),
    "console": ("Game Console", "Játékkonzol", "Spielkonsole", "Console de jeux", "Игровая приставка"),
    "consoles": ("Game Console", "Játékkonzol", "Spielkonsole", "Console de jeux", "Игровая приставка"),
    "converter": ("Converter", "Átalakító", "Konverter", "Convertisseur", "Преобразователь"),
    "converters": ("Converter", "Átalakító", "Konverter", "Convertisseur", "Преобразователь"),
    "dvb-t": ("DVB-T Receiver", "DVB-T vevő", "DVB-T-Empfänger", "Récepteur DVB-T", "DVB-T ресивер"),
    "dvd-player": ("DVD Player", "DVD-lejátszó", "DVD-Player", "Lecteur DVD", "DVD-проигрыватель"),
    "digital-sign": ("Digital Sign", "Digitális kijelző", "Digital Signage", "Affichage numérique", "Цифровая вывеска"),
    "dust-collector": ("Dust Collector", "Porelszívó", "Staubabscheider", "Collecteur de poussière", "Пылеуловитель"),
    "fan": ("Fan", "Ventilátor", "Ventilator", "Ventilateur", "Вентилятор"),
    "fireplace": ("Fireplace", "Kandalló", "Kamin", "Cheminée", "Камин"),
    "fireplaces": ("Fireplace", "Kandalló", "Kamin", "Cheminée", "Камин"),
    "ceiling-lift": ("Ceiling Lift", "Mennyezeti emelő", "Deckenlift", "Lève-personne plafonnier", "Потолочный подъёмник"),
    "head-unit": ("Head Unit", "Autórádió / fejegység", "Autoradio", "Autoradio", "Автомагнитола"),
    "heater": ("Heater", "Fűtőberendezés", "Heizgerät", "Chauffage", "Обогреватель"),
    "humidifier": ("Humidifier", "Párásító", "Luftbefeuchter", "Humidificateur", "Увлажнитель воздуха"),
    "kvm": ("KVM Switch", "KVM kapcsoló", "KVM-Switch", "Commutateur KVM", "KVM-переключатель"),
    "light": ("LED Lighting", "LED világítás", "LED-Beleuchtung", "Éclairage LED", "LED-освещение"),
    "laserdisc": ("LaserDisc Player", "LaserDisc lejátszó", "LaserDisc-Player", "Lecteur LaserDisc", "LaserDisc-проигрыватель"),
    "minidisc": ("MiniDisc Player", "MiniDisc lejátszó", "MiniDisc-Player", "Lecteur MiniDisc", "MiniDisc-проигрыватель"),
    "miscellaneous": ("Other IR Device", "Egyéb infrás eszköz", "Sonstiges IR-Gerät", "Autre appareil IR", "Другое ИК-устройство"),
    "monitor": ("Monitor", "Monitor", "Monitor", "Moniteur", "Монитор"),
    "monitors": ("Monitor", "Monitor", "Monitor", "Moniteur", "Монитор"),
    "multimedia": ("Multimedia", "Multimédia", "Multimedia", "Multimédia", "Мультимедиа"),
    "digital-picture-frame": ("Digital Picture Frame", "Digitális képkeret", "Digitaler Bilderrahmen", "Cadre photo numérique", "Цифровая фоторамка"),
    "projector": ("Projector", "Projektor", "Projektor", "Projecteur", "Проектор"),
    "soundbar": ("Soundbar", "Hangprojektor", "Soundbar", "Barre de son", "Саундбар"),
    "speaker": ("Speaker", "Hangszóró", "Lautsprecher", "Enceinte", "Колонка"),
    "speakers": ("Speaker", "Hangszóró", "Lautsprecher", "Enceinte", "Колонка"),
    "streaming-device": ("Streaming Device", "Streaming eszköz", "Streaming-Gerät", "Appareil de streaming", "Стриминговое устройство"),
    "tv-tuner": ("TV Tuner", "TV tuner", "TV-Tuner", "Tuner TV", "ТВ-тюнер"),
    "television": ("Television", "Televízió", "Fernseher", "Téléviseur", "Телевизор"),
}

ICONS = {
    "television": "📺", "air-conditioner": "❄️", "fan": "🌀", "air-purifier": "🌬️",
    "av-receiver": "🎚️", "soundbar": "🔊", "speaker": "🔊", "speakers": "🔊",
    "projector": "📽️", "set-top-box": "📦", "streaming-device": "📺", "tv-tuner": "📡",
    "dvd-player": "💿", "blu-ray-player": "💿", "cd-player": "💿", "minidisc": "💿", "laserdisc": "💿",
    "light": "💡", "heater": "♨️", "humidifier": "💧", "camera": "📷", "cameras": "📷",
    "cctv": "📹", "computer": "💻", "computers": "💻", "console": "🎮", "consoles": "🎮",
    "clock": "🕒", "clocks": "🕒", "fireplace": "🔥", "fireplaces": "🔥", "monitor": "🖥️", "monitors": "🖥️",
}

TESTS = {
    "television": ["Power", "VolumeUp", "Mute", "ChannelUp", "Source"],
    "air-conditioner": ["Power", "TemperatureUp", "Mode", "FanSpeed", "Swing"],
    "fan": ["Power", "FanSpeed", "Swing", "Timer"],
    "soundbar": ["Power", "VolumeUp", "Mute", "Source"],
    "av-receiver": ["Power", "VolumeUp", "Mute", "Source"],
    "projector": ["Power", "Source", "Menu"],
    "light": ["Power", "BrightnessUp", "BrightnessDown"],
}


def kebab(value: str) -> str:
    value = value.replace("_", " ")
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return value or "general"


def pretty(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").strip().title()


def names_for(type_id: str, folder: str) -> dict[str, str]:
    values = NAMES.get(type_id)
    if values is None:
        en = pretty(folder)
        values = (en, en, en, en, en)
    return dict(zip(("en", "hu", "de", "fr", "ru"), values))


def has_ir_files(folder: Path) -> bool:
    try:
        return next(folder.rglob("*.ir"), None) is not None
    except OSError:
        return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Checked-out Flipper-IRDB root")
    parser.add_argument("--output", default=".", help="HomeController-DeviceDB checkout")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    root = Path(args.output).resolve()
    target = root / "device-types.json"
    doc = json.loads(target.read_text(encoding="utf-8"))
    types = doc.setdefault("deviceTypes", [])
    by_id = {x.get("id", "").lower(): x for x in types if x.get("id")}

    upstream_ids: set[str] = set()
    for folder in sorted((x for x in source.iterdir() if x.is_dir() and not x.name.startswith(".")), key=lambda x: x.name.lower()):
        if not has_ir_files(folder):
            continue
        type_id = SPECIAL_IDS.get(folder.name, kebab(folder.name))
        upstream_ids.add(type_id)
        localized = names_for(type_id, folder.name)
        node = by_id.get(type_id)
        if node is None:
            node = {
                "id": type_id,
                "displayName": localized["en"],
                "displayNames": localized,
                "icon": ICONS.get(type_id, "🎛️"),
                "connections": ["infrared"],
                "databaseTypeNames": [folder.name],
                "sourcePathHints": [folder.name],
                "defaultUiTemplates": {},
                "testCommands": TESTS.get(type_id, ["Power"]),
            }
            types.append(node)
            by_id[type_id] = node
        else:
            node["displayName"] = localized["en"]
            node["displayNames"] = localized
            node["icon"] = node.get("icon") or ICONS.get(type_id, "🎛️")
            connections = node.setdefault("connections", [])
            if "infrared" not in [x.lower() for x in connections]:
                connections.append("infrared")
            aliases = node.setdefault("databaseTypeNames", [])
            if folder.name.lower() not in [x.lower() for x in aliases]:
                aliases.append(folder.name)
            hints = node.setdefault("sourcePathHints", [])
            if folder.name.lower() not in [x.lower() for x in hints]:
                hints.append(folder.name)
            if not node.get("testCommands"):
                node["testCommands"] = TESTS.get(type_id, ["Power"])

    # Ensure every existing type also has localized metadata. Non-IR integrations
    # (Hubitat, Hue, IR transceiver) remain untouched otherwise.
    for node in types:
        type_id = node.get("id", "general")
        if not node.get("displayNames"):
            base = node.get("displayName") or pretty(type_id)
            known = NAMES.get(type_id)
            node["displayNames"] = dict(zip(("en", "hu", "de", "fr", "ru"), known or (base, base, base, base, base)))
        if not node.get("icon"):
            node["icon"] = ICONS.get(type_id, "🎛️")

    types.sort(key=lambda x: (x.get("displayName", "").lower(), x.get("id", "").lower()))
    target.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Synchronized {len(upstream_ids)} infrared device types from Flipper-IRDB; DeviceDB now has {len(types)} device types.")


if __name__ == "__main__":
    main()
