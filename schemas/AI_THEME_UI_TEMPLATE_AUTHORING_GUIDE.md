# HomeController — AI Theme & Device UI V2 Authoring Guide

This is the canonical AI-facing rule set for generating HomeController themes and Device UI templates.

## Source of truth

HomeController has two independent presentation layers:

1. Application themes under `themes/`, using `app-theme-v1.schema.json`.
2. Device UI templates under `ui-templates/`, using `device-ui-template-v2.schema.json`.

For all newly created Device UI screens, use only the editable V2 JSON layout model.

## Mandatory Device UI rules

Every new Device UI template must:

1. use `schemaVersion: 2`;
2. reference `device-ui-template-v2.schema.json`;
3. use `renderer: "declarative"`;
4. define its editable layout through `groups` and `controls`;
5. give reusable groups and controls stable IDs;
6. use actual driver/DeviceDB command names and capability keys;
7. remain fully editable in the HomeController UI editor;
8. use localization variants for user-visible text rather than creating language-specific logical templates;
9. be registered in `ui-templates/index.json` when it is a DeviceDB template;
10. trigger a DeviceDB `version.json` bump when published or changed.

Do not generate a Device UI whose visible structure exists only in application code. Do not create a second authoring format for a specific device family.

## Minimal Device UI V2 template

```json
{
  "$schema": "../schemas/device-ui-template-v2.schema.json",
  "schemaVersion": 2,
  "id": "example-default",
  "name": "Example",
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

## Groups

Groups are the editable building blocks of a screen. Use them for visual sections, nested areas, dynamic child items, filters and capabilities. The machine-readable schema defines all supported fields.

Common group fields include `id`, `name`, `order`, `columnSpan`, `rowSpan`, `type`, `titlePlacement`, border/background styling, `controls`, and nested `groups`.

## Controls

Use only control types accepted by `device-ui-template-v2.schema.json`. Common controls include buttons, labels, toggles, steppers, sliders, pickers, links, tiles, filters and capability-bound controls.

For device actions, never invent command names. Use canonical commands present in DeviceDB or the corresponding driver/integration.

## Layout and styling

Prefer a clear mobile-first hierarchy with touch-friendly controls. Use `columns`, explicit `row`/`column`, `columnSpan`, spacing, corner radii, borders and group backgrounds to build the layout.

Application theme inheritance is preferred for general templates. Explicit template colors are allowed where the template intentionally has its own visual identity.

## Localization

Language variants represent the same logical template. Example:

- `wifi-tv-default.json`
- `wifi-tv-default-en.json`
- `wifi-tv-default-hu.json`

The picker exposes only `wifi-tv-default`; the current-language variant is applied automatically and the neutral file is fallback.

Keep IDs, commands, state keys and capability keys language-neutral.

## Application themes

Application themes continue to use `app-theme-v1.schema.json` and semantic color resources. Device UI layout and application theme are independent concepts.

## Final authoring rule

When asked to create, redesign or update a HomeController device UI, always produce editable Device UI V2 `groups` + `controls` JSON. This is the only supported authoring approach described to AI agents.
