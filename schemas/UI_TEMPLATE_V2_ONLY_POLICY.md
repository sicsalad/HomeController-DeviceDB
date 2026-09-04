# HomeController Device UI templates — V2-only policy

This file is normative for current HomeController Device UI template authoring and overrides older compatibility wording in historical documentation.

## Current rule

All active Device UI templates in `ui-templates/index.json` MUST use:

```json
{
  "$schema": "../schemas/device-ui-template-v2.schema.json",
  "schemaVersion": 2
}
```

`device-ui-template-v1.schema.json` is retained only as historical/migration reference. Current HomeController runtime catalog loading, local template loading, import and custom DeviceDB template loading must not select V1 templates for rendering.

AI generators MUST generate V2 only. Never generate a new V1 Device UI template.

## Runtime migration

The Settings action **Reset local UI schemas and reload DeviceDB V2** removes local UI/template copies and replaces saved device template snapshots with current DeviceDB V2 templates while keeping configured devices. Existing integration child pin selections (`pinnedProperties`, `pinnedCommands`, `pinnedSliders`) are migrated into the new V2 snapshot where possible.

The migration reader may deserialize an old snapshot only as migration input. That does not make V1 a supported rendering format.

## Language variants

Localized files such as `wifi-tv-default-hu.json` are language overlays for the language-neutral logical V2 template `wifi-tv-default.json`; they are not separate template versions and are not required to repeat the full V2 schema.

## Connection values

V2 supports `infrared`, `wifi`, `bluetooth`, and `local` where the target runtime/device type supports that connection family.

## Validation

Every primary template indexed by `ui-templates/index.json` is validated as V2 by `tools/validate_device_catalog.py`. The canonical machine-readable property contract is `device-ui-template-v2.schema.json`.
