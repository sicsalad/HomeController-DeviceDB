# HomeController themes and Device UI templates

This document describes the JSON files understood by the HomeController theme and DeviceDB UI-template runtime.

There are two independent customization layers:

1. **Application themes** (`themes/*.json`) change application-wide resource colors such as Primary, surfaces and gray shades.
2. **Device UI templates** (`ui-templates/*.json`) control the appearance and, for declarative devices, the layout and controls of a specific device type.

A user can also configure a premium custom source URL in HomeController Settings. That URL must point to an `index.json`. Custom sources are additive: the built-in public DeviceDB remains available. Custom sources require an actively enabled Premium entitlement; the Premium grace period does not enable this feature.

## 1. Application theme JSON

Example:

```json
{
  "schemaVersion": 1,
  "id": "my-dark-theme",
  "name": "My Dark Theme",
  "mode": "dark",
  "minimumRuntimeVersion": 1,
  "colors": {
    "Primary": "#365E91",
    "PrimaryDark": "#243E60",
    "PrimaryLight": "#769BC7",
    "PrimaryDarkText": "#FFFFFF",
    "Secondary": "#18212B",
    "SecondaryDarkText": "#D7E5F4",
    "Tertiary": "#557FAF",
    "White": "#FFFFFF",
    "Black": "#080A0D",
    "Gray100": "#E1E1E1",
    "Gray200": "#C8C8C8",
    "Gray300": "#ACACAC",
    "Gray400": "#919191",
    "Gray500": "#6E6E6E",
    "Gray600": "#404040",
    "Gray900": "#212121",
    "Gray950": "#141414",
    "BlueEyePrimary": "#365E91",
    "BlueEyePrimaryDark": "#243E60",
    "BlueEyePrimaryLight": "#769BC7",
    "BlueEyeDarkBg": "#0E141B",
    "BlueEyeSurface": "#18212B",
    "BlueEyeAccent": "#557FAF"
  }
}
```

### Application-theme fields

| Field | Type | Meaning |
| --- | --- | --- |
| `schemaVersion` | integer | Must currently be `1`. |
| `id` | string | Stable unique theme identifier. The file selected from the catalog must contain the same ID. |
| `name` | string | User-visible theme name. |
| `mode` | string | `light` or `dark`. Controls the MAUI application theme mode. |
| `minimumRuntimeVersion` | integer | Theme is offered only when the HomeController runtime is at least this version. Current runtime version is 1. |
| `colors` | object | Resource-name to color-value map. Values must be valid MAUI/ARGB colors, normally `#RRGGBB` or `#AARRGGBB`. |

The runtime applies every entry in `colors` to `Application.Current.Resources`, so custom themes may override additional existing color resources. For compatibility, custom themes should at least provide the standard keys used by the built-in themes:

- `Primary`, `PrimaryDark`, `PrimaryLight`, `PrimaryDarkText`
- `Secondary`, `SecondaryDarkText`, `Tertiary`
- `White`, `Black`
- `Gray100`, `Gray200`, `Gray300`, `Gray400`, `Gray500`, `Gray600`, `Gray900`, `Gray950`
- `BlueEyePrimary`, `BlueEyePrimaryDark`, `BlueEyePrimaryLight`, `BlueEyeDarkBg`, `BlueEyeSurface`, `BlueEyeAccent`

If `PrimaryDark` is present, HomeController automatically derives a high-contrast `PrimaryDarkText` at runtime. Dark backgrounds therefore receive white text when needed.

### Application theme catalog

The built-in catalog is `themes/index.json`:

```json
{
  "schemaVersion": 1,
  "themes": [
    {
      "id": "my-dark-theme",
      "name": "My Dark Theme",
      "file": "my-dark-theme.json",
      "minimumRuntimeVersion": 1
    }
  ]
}
```

`file` is resolved relative to the catalog's base URL.

## 2. Device type JSON

Device types are registered in `device-types.json`.

Example:

```json
{
  "id": "philips-hue",
  "displayName": "Philips Hue",
  "icon": "💡",
  "connections": ["wifi"],
  "databaseTypeNames": [],
  "sourcePathHints": ["PhilipsHueV2", "Philips Hue", "Hue"],
  "defaultUiTemplates": {
    "wifi": "hue-default"
  },
  "setupHandler": "philips-hue"
}
```

### Device-type fields

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Stable DeviceType ID used by templates. |
| `displayName` | string | User-visible type name. |
| `icon` | string | Emoji/text icon displayed by the application. |
| `connections` | string[] | Supported connections. Currently commonly `infrared`, `wifi`, or `bluetooth`. |
| `databaseTypeNames` | string[] | Names used when mapping the type to device-database categories. May be empty for integrations such as Hubitat and Hue. |
| `sourcePathHints` | string[] | Case-insensitive hints used to resolve older/saved devices to this DeviceType. |
| `defaultUiTemplates` | object | Connection name to default UI-template ID. Example: `{ "wifi": "hubitat-default" }`. |
| `setupHandler` | string | Optional built-in setup-flow identifier. |

## 3. Device UI template JSON

Example:

```json
{
  "schemaVersion": 1,
  "id": "hubitat-my-dark",
  "name": "Hubitat My Dark",
  "deviceTypeId": "hubitat",
  "connections": ["wifi"],
  "renderer": "builtin-hubitat",
  "columns": 2,
  "backgroundColor": "#0D0F12",
  "foregroundColor": "#F4F4F4",
  "mutedTextColor": "#A5AAB0",
  "surfaceColor": "#171A1F",
  "accentColor": "#7B3247",
  "buttonColor": "#3D2029",
  "buttonTextColor": "#FFFFFF",
  "borderColor": "#383D44",
  "themeSwitcherBackgroundColor": "#171A1F",
  "themeSwitcherTextColor": "#C4C8CD",
  "themeSwitcherBorderColor": "#383D44",
  "themeSwitcherText": "UI",
  "themeSwitcherOpacity": 0.72,
  "buttonCornerRadius": 8,
  "sectionCornerRadius": 11,
  "buttonHeight": 54,
  "buttonFontSize": 13,
  "iconFontSize": 22,
  "sections": []
}
```

### Top-level UI-template fields

| Field | Type | Meaning |
| --- | --- | --- |
| `schemaVersion` | integer | Currently `1`. |
| `id` | string | Stable unique template ID. |
| `name` | string | Name shown in the device UI selector. |
| `deviceTypeId` | string | Device type this template belongs to, e.g. `hubitat`, `philips-hue`, `television`, `air-conditioner`. |
| `connections` | string[] | Connections for which the template is selectable. |
| `renderer` | string | Rendering engine. See renderer table below. |
| `columns` | integer | Declarative grid column count. The Hubitat built-in renderer also uses it for the device-card grid and clamps it to 1-4. |
| `backgroundColor` | color/null | Page background. Omit to preserve the renderer/application default. |
| `foregroundColor` | color/null | Main text color. |
| `mutedTextColor` | color/null | Secondary/status text color. |
| `surfaceColor` | color/null | Cards/sections/surfaces. |
| `accentColor` | color/null | Active/selected/accent controls. Hubitat uses it for selected categories and ON-state actions. |
| `buttonColor` | color/null | Default button/control background. |
| `buttonTextColor` | color/null | Explicit button text color. If omitted, supported renderers calculate black/white text from button luminance. |
| `borderColor` | color/null | Card/button/control borders. |
| `themeSwitcherBackgroundColor` | color/null | Background of the small device UI selector beside the device name. |
| `themeSwitcherTextColor` | color/null | Text color of the device UI selector. |
| `themeSwitcherBorderColor` | color/null | Border color of the device UI selector. |
| `themeSwitcherText` | string | Selector caption. Defaults to `UI`. |
| `themeSwitcherOpacity` | number | Selector opacity. Built-in pages clamp it to a readable range. |
| `buttonCornerRadius` | integer | Button corner radius. |
| `sectionCornerRadius` | integer | Section/card corner radius. |
| `buttonHeight` | number | Default button height used by declarative and supported built-in controls. |
| `buttonFontSize` | number | Default button/compact text size. |
| `iconFontSize` | number | Default icon size. |
| `sections` | array | Declarative sections. Built-in integration renderers keep their functional layout and use the visual fields above. |

All color fields are optional. Omitting a visual field means “use the existing renderer/application fallback”. This is how `hubitat-default` and `hue-default` preserve the original HomeController appearance.

### Renderer values

| Renderer | Device/use |
| --- | --- |
| `declarative` | JSON-defined controls and sections. |
| `builtin-ir-tv` | Existing infrared TV page. |
| `builtin-ir-ac` | Existing infrared A/C page. |
| `builtin-wifi-ac` | Existing supported Wi-Fi A/C page. |
| `builtin-hubitat` | Hubitat device list and Hubitat child-device control pages. Visual styling comes from this template. |
| `builtin-hue` | Philips Hue resources/control page. Visual styling comes from this template. |
| `builtin-dashboard` | Dashboard page. |

Built-in renderers intentionally own protocol-specific behavior. A theme changes their appearance without replacing Hubitat/Hue command logic.

## 4. Declarative sections and controls

A declarative template may contain:

```json
{
  "title": "Power",
  "subtitle": "Main controls",
  "backgroundColor": "#171A1F",
  "controls": [
    {
      "type": "button",
      "label": "Power",
      "command": "power",
      "value": null,
      "icon": "⏻",
      "columnSpan": 1,
      "backgroundColor": "#3D2029",
      "textColor": "#FFFFFF",
      "borderColor": "#56313C",
      "height": 54,
      "fontSize": 13,
      "iconSize": 22,
      "iconOnly": false
    }
  ]
}
```

### Section fields

- `title`: optional section heading.
- `subtitle`: optional secondary heading.
- `backgroundColor`: optional section-specific surface color.
- `controls`: array of controls.

### Control fields

| Field | Type | Meaning |
| --- | --- | --- |
| `type` | string | Control type. Defaults to `button`. Renderer support depends on the declarative runtime. |
| `label` | string | Visible caption. |
| `command` | string | Command identifier sent by the device command dispatcher. |
| `value` | any/null | Optional fixed command value. |
| `icon` | string/null | Optional icon/emoji. |
| `columnSpan` | integer | Number of grid columns occupied. |
| `minimum` | number/null | Minimum value for ranged controls. |
| `maximum` | number/null | Maximum value for ranged controls. |
| `step` | number/null | Step for ranged controls. |
| `stateField` | string/null | Device state field associated with the control. |
| `options` | string[] | Options for choice controls. |
| `backgroundColor` | color/null | Per-control background override. |
| `textColor` | color/null | Per-control text override. |
| `borderColor` | color/null | Per-control border override. |
| `height` | number/null | Per-control height override. |
| `fontSize` | number/null | Per-control font-size override. |
| `iconSize` | number/null | Per-control icon-size override. |
| `iconOnly` | boolean | Render primarily as an icon control when supported. |

Per-control values override the top-level template defaults. On dark button backgrounds, HomeController can derive white text automatically when no explicit text color is supplied.

## 5. UI template index

The public DeviceDB uses `ui-templates/index.json`:

```json
{
  "schemaVersion": 1,
  "templates": [
    {
      "id": "hubitat-my-dark",
      "path": "hubitat-my-dark.json",
      "status": "stable"
    }
  ]
}
```

The application currently uses `id` and `path`; `status` is repository metadata and defaults to `stable` in the model.

## 6. Premium custom source `index.json`

A custom source can expose application themes, Device UI templates and additional/replacement DeviceTypes from one URL.

Example custom source root:

```text
https://example.com/homecontroller/index.json
https://example.com/homecontroller/themes/night.json
https://example.com/homecontroller/ui/hubitat-night.json
```

Example `index.json`:

```json
{
  "schemaVersion": 1,
  "themes": [
    {
      "id": "night",
      "name": "Night",
      "file": "themes/night.json",
      "minimumRuntimeVersion": 1
    }
  ],
  "templates": [
    {
      "id": "hubitat-night",
      "path": "ui/hubitat-night.json",
      "status": "stable"
    }
  ],
  "deviceTypes": []
}
```

Paths are resolved relative to the directory containing the custom `index.json`. The application merges custom data with the public DeviceDB. If a custom theme/template/DeviceType uses an existing ID, the custom entry replaces that ID in the merged runtime catalog; other public entries remain available.

For a custom theme, `file` should normally be supplied. If omitted, the app falls back to `themes/<id>.json` for a custom source. For a custom UI template, `path` must be supplied.

Invalid/unreachable custom sources are ignored without disabling the built-in DeviceDB.

## 7. Hubitat templates

Hubitat templates use:

```json
"deviceTypeId": "hubitat",
"connections": ["wifi"],
"renderer": "builtin-hubitat"
```

The selected template applies to both:

- the Hubitat device/card list,
- room/category filtering,
- quick ON/OFF controls,
- the detailed child-device state page,
- detailed child-device commands,
- the device UI selector beside the Hubitat name.

`columns` controls the Hubitat device-card grid (1-4). `accentColor` is used for selected categories and active/ON actions. `buttonColor` is used for inactive/default actions. `surfaceColor`, `borderColor`, foreground and muted colors theme cards and state text.

## 8. Philips Hue templates

Philips Hue templates use:

```json
"deviceTypeId": "philips-hue",
"connections": ["wifi"],
"renderer": "builtin-hue"
```

The built-in Hue renderer retains Hue-specific behavior (lights, grouped lights, scenes, sensors, switches/controllers, power/connectivity and system resources), while the template controls page, text, card, button, border and UI-selector styling.

## 9. Compatibility recommendations

- Keep `schemaVersion` at `1` until the runtime explicitly adds a new schema.
- Use unique lowercase IDs with hyphens.
- Prefer `#RRGGBB`/`#AARRGGBB` color strings.
- Treat unknown future fields as optional; HomeController's JSON deserializer ignores unknown properties.
- Do not remove required identity/routing fields (`id`, `deviceTypeId`, `connections`, `renderer`) from a UI template.
- Keep a Default template with omitted visual overrides when exact backward-compatible appearance is important.
- Test both light/dark application modes if a Device UI template intentionally leaves colors unspecified.
