# HomeController themes and Device UI V2

This document is the canonical human-facing reference for creating HomeController application themes and Device UI templates.

## Application themes

Application themes live under `themes/` and use `app-theme-v1.schema.json`. They control application-wide semantic colors and are independent from Device UI layouts.

Device UI templates should normally inherit semantic theme resources unless a template intentionally defines its own visual identity.

## Device UI templates

All newly created Device UI screens must use the current editable Device UI V2 format:

- schema: `device-ui-template-v2.schema.json`
- `schemaVersion`: `2`
- `renderer`: `declarative`
- layout: `groups`
- elements: `controls`
- every reusable group/control has a stable `id`

Do not create new UI layouts whose structure is hard-coded in application code. A new device UI must be editable from the HomeController UI editor and its groups and controls must be present in the template JSON.

### Minimal template

```json
{
  "$schema": "../schemas/device-ui-template-v2.schema.json",
  "schemaVersion": 2,
  "id": "example-device-default",
  "name": "Example Device",
  "deviceTypeId": "example-device",
  "connections": ["infrared"],
  "renderer": "declarative",
  "access": "free",
  "columns": 4,
  "useFullWidth": true,
  "groups": [
    {
      "id": "main",
      "name": "Main",
      "order": 10,
      "columnSpan": 4,
      "type": "normal",
      "controls": [
        {
          "id": "power",
          "order": 10,
          "type": "button",
          "label": "Power",
          "command": "Power",
          "row": 0,
          "column": 0,
          "columnSpan": 4
        }
      ]
    }
  ]
}
```

## V2 groups

Groups are the primary editable layout blocks. They may contain controls and nested groups. Important properties include:

- `id`, `name`, `order`
- `columnSpan`, `rowSpan`, `width`, `height`
- `type`
- `titlePlacement`
- `shape`, `cornerRadius`, `borderColor`, `borderWidth`
- `backgroundMode`, `backgroundColor`, `backgroundColor2`, `backgroundImage`
- `controls`, `groups`

Dynamic layouts may additionally use child-item, filter and capability group fields defined in `device-ui-template-v2.schema.json`.

## V2 controls

Use only control types declared by `device-ui-template-v2.schema.json`. Common controls include `label`, `multiline-label`, `edittext`, `button`, `list`, `checkbox`, `filter-toggle`, `on-off`, `link`, `tile`, `toggle`, `stepper`, `slider`, `picker`, and capability controls.

Controls can define grid position, span, sizing, commands, state binding and visual styling.

## Device-specific commands

Do not invent command names. Commands must come from the target driver, integration or DeviceDB canonical command set. If a device does not support a control, the runtime should handle that capability as unavailable rather than requiring a different UI format.

## Localization

Language variants are one logical UI template. For example:

- `wifi-tv-default.json`
- `wifi-tv-default-en.json`
- `wifi-tv-default-hu.json`

The template picker exposes only the logical base template. The current-language variant is applied when present and the language-neutral file is the fallback.

IDs, command names, state keys and capability keys remain language-neutral. Only user-visible text is localized.

## Default templates

`device-types.json` maps each device type/connection to its default V2 template through `defaultUiTemplates`.

When a DeviceDB UI template changes, bump `version.json` so HomeController refreshes its local DeviceDB cache.

## Authoring rule

From this point forward, every new HomeController Device UI is authored as editable Device UI V2 JSON using `groups` and `controls`. This is the only documented UI authoring path.
