#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "ui-templates"
SCHEMAS = ROOT / "schemas"
LANG_RE = re.compile(r"^(?P<base>.+)-(?P<lang>de|fr|hu|ru)\.json$")
TEXT_KEYS = {"name", "title", "subtitle", "label", "text", "themeSwitcherText"}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def collect(base, localized, path=()):
    result = {}
    if isinstance(base, dict) and isinstance(localized, dict):
        for key, bvalue in base.items():
            if key not in localized:
                continue
            lvalue = localized[key]
            next_path = path + (key,)
            if key in TEXT_KEYS and isinstance(bvalue, str) and isinstance(lvalue, str):
                if lvalue != bvalue:
                    result[".".join(map(str, next_path))] = lvalue
                continue
            if key == "options" and isinstance(bvalue, list) and isinstance(lvalue, list):
                for i, (bv, lv) in enumerate(zip(bvalue, lvalue)):
                    if isinstance(bv, str) and isinstance(lv, str) and lv != bv:
                        result[".".join(map(str, next_path + (i,)))] = lv
                continue
            result.update(collect(bvalue, lvalue, next_path))
    elif isinstance(base, list) and isinstance(localized, list):
        for i, (bvalue, lvalue) in enumerate(zip(base, localized)):
            result.update(collect(bvalue, lvalue, path + (i,)))
    return result


def compact_existing_languages():
    changed = 0
    for path in sorted(UI.glob("*.json")):
        match = LANG_RE.match(path.name)
        if not match:
            continue
        base_path = UI / f"{match.group('base')}.json"
        if not base_path.exists():
            continue
        localized = load(path)
        if isinstance(localized, dict) and all(isinstance(v, str) for v in localized.values()):
            continue
        translations = collect(load(base_path), localized)
        dump(path, translations)
        changed += 1
    return changed


def add_dynamic_languages():
    values = {
        "hubitat-dynamic": {
            "de": {"name":"Hubitat Dynamisch","groups.0.name":"Gerätetyp","groups.1.name":"Schnellfilter","groups.1.controls.0.text":"Nur online","groups.2.name":"Suche","groups.2.controls.0.text":"Geräte suchen","groups.3.name":"Geräte"},
            "fr": {"name":"Hubitat dynamique","groups.0.name":"Type d’appareil","groups.1.name":"Filtre rapide","groups.1.controls.0.text":"En ligne uniquement","groups.2.name":"Recherche","groups.2.controls.0.text":"Rechercher des appareils","groups.3.name":"Appareils"},
            "hu": {"name":"Hubitat dinamikus","groups.0.name":"Eszköztípus","groups.1.name":"Gyorsszűrő","groups.1.controls.0.text":"Csak online","groups.2.name":"Keresés","groups.2.controls.0.text":"Eszközök keresése","groups.3.name":"Eszközök"},
            "ru": {"name":"Hubitat динамический","groups.0.name":"Тип устройства","groups.1.name":"Быстрый фильтр","groups.1.controls.0.text":"Только онлайн","groups.2.name":"Поиск","groups.2.controls.0.text":"Поиск устройств","groups.3.name":"Устройства"},
        },
        "dashboard-dynamic": {
            "de": {"name":"Dashboard Dynamisch","groups.0.name":"Suche","groups.0.controls.0.text":"Dashboards suchen","groups.1.name":"Dashboards"},
            "fr": {"name":"Dashboard dynamique","groups.0.name":"Recherche","groups.0.controls.0.text":"Rechercher des tableaux de bord","groups.1.name":"Tableaux de bord"},
            "hu": {"name":"Dashboard dinamikus","groups.0.name":"Keresés","groups.0.controls.0.text":"Dashboardok keresése","groups.1.name":"Dashboardok"},
            "ru": {"name":"Dashboard динамический","groups.0.name":"Поиск","groups.0.controls.0.text":"Поиск панелей","groups.1.name":"Панели"},
        },
    }
    for template, languages in values.items():
        if not (UI / f"{template}.json").exists():
            continue
        for lang, translations in languages.items():
            dump(UI / f"{template}-{lang}.json", translations)


def relax_schemas():
    for name in ("device-ui-template-v1.schema.json", "device-ui-template-v2.schema.json"):
        path = SCHEMAS / name
        if not path.exists():
            continue
        schema = load(path)
        # Only identity/routing information is structurally required. Every optional layout,
        # style, state and control property may simply be omitted and the app uses its model default.
        schema["required"] = ["schemaVersion", "id", "name", "deviceTypeId", "connections"]
        defs = schema.get("$defs", {})
        if "control" in defs:
            defs["control"].pop("required", None)
        if "group" in defs:
            defs["group"].pop("required", None)
        dump(path, schema)


def write_localization_schema():
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://github.com/sicsalad/HomeController-DeviceDB/schemas/ui-template-localization-v1.schema.json",
        "title": "HomeController UI template localization overlay v1",
        "description": "A language file contains only translation-code -> translated-text pairs. Layout and behavior belong exclusively to the language-neutral base template.",
        "type": "object",
        "propertyNames": {"type": "string", "minLength": 1},
        "additionalProperties": {"type": "string"}
    }
    dump(SCHEMAS / "ui-template-localization-v1.schema.json", schema)


def write_docs():
    text = """# UI template format and localization\n\n## Base template\n\nThe language-neutral `ui-templates/<id>.json` file is the complete source of truth. A property that is not needed does **not** have to be present. Missing optional properties are supplied by the HomeController model defaults. The schema documents the available properties even when a particular template omits them.\n\nThe identifying fields `schemaVersion`, `id`, `name`, `deviceTypeId` and `connections` remain required. `renderer` is optional; when omitted the runtime default is `declarative`. Group/control properties are optional unless the selected control behavior logically needs them (for example a command button needs `command`).\n\n### Available template properties\n\n`renderer`, `columns`, `useFullWidth`, `horizontalSpacing`, `verticalSpacing`, `backgroundColor`, `backgroundColor2`, `backgroundMode`, `backgroundImage`, `backgroundImageAspect`, `foregroundColor`, `mutedTextColor`, `surfaceColor`, `accentColor`, `buttonColor`, `buttonTextColor`, `borderColor`, `buttonCornerRadius`, `sectionCornerRadius`, `buttonHeight`, `buttonFontSize`, `iconFontSize`, `itemDefaults`, `itemStyles`, `sections`, `groups`, `initialStates`. Legacy theme-switcher properties remain supported for compatibility.\n\n### Group properties\n\n`id`, `name`, `order`, `type`, `columnSpan`, `rowSpan`, legacy `width`/`height`, `childItemsSource`, `childItemsColumns`, `filterScope`, `filterProperty`, `filterMode`, `filterValues`, `filterAutoValues`, `shape`, `borderColor`, `borderWidth`, `backgroundMode`, `backgroundColor`, `backgroundColor2`, `backgroundImage`, `backgroundImageAspect`, `cornerRadius`, `overlayKey`, `overlayState`, `controls`, `groups`.\n\n### Control properties\n\n`id`, `order`, `type`, `label`, `text`, `command`, `value`, `icon`, `shape`, `row`, `column`, `columnSpan`, `verticalAlign`, `sizeXPercent`, `sizeYPercent`, `minimum`, `maximum`, `step`, `stateField`, `options`, `backgroundColor`, `backgroundImage`, `textColor`, `borderColor`, `borderWidth`, `height`, `width`, `fontFamily`, `fontSize`, `fontAttribute`, `lines`, `iconSize`, `iconOnly`, `linkUrl`, `stateKey`, `setState`, `cycleStates`, `filterId`, `filterValue`, `filterMode`, `hideText`, `uncheckedImage`, `checkedImage`.\n\n## Language files\n\nA localized file such as `wifi-tv-default-hu.json` is **not another template**. It is only a translation overlay for `wifi-tv-default.json`. It must contain no layout, color, command, URL, filter or other behavioral data. The filename selects the language.\n\nThe file is a flat JSON object. Each key is a code/path identifying a text property in the base template and each value is the translated text. Example:\n\n```json\n{\n  \"name\": \"Modern TV távirányító\",\n  \"sections.0.subtitle\": \"Gyorsvezérlők\",\n  \"sections.1.title\": \"NAVIGÁCIÓ\",\n  \"sections.1.controls.0.label\": \"HANGERŐ +\"\n}\n```\n\nSupported translatable text is currently template `name`/`themeSwitcherText`, section `title`/`subtitle`, group `name`, control `label`/`text`, and string `options` entries. Unlisted strings fall back to the base template.\n\nThe runtime always loads the language-neutral base first, then overlays the current language file when it exists. If the language file is missing or contains a bad key, the base text remains. This keeps all rendering and behavior in one place and prevents language variants from drifting apart.\n\nThe language-file schema is `schemas/ui-template-localization-v1.schema.json`.\n"""
    (SCHEMAS / "UI_TEMPLATE_FORMAT.md").write_text(text, encoding="utf-8")


def main():
    changed = compact_existing_languages()
    add_dynamic_languages()
    relax_schemas()
    write_localization_schema()
    write_docs()
    print(f"Converted {changed} full language templates to compact overlays")


if __name__ == "__main__":
    main()
