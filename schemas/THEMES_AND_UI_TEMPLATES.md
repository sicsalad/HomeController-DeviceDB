# HomeController themes and Device UI templates

This document describes the JSON customization formats supported by HomeController.

## 1. Application themes and Device UI templates are separate

HomeController has two independent customization layers:

- **Application themes** (`themes/*.json`) change application-wide colors and light/dark mode. `Default`, `Blue Eye` and `Red Eye` belong here.
- **Device UI templates** (`ui-templates/*.json`) define the layout and presentation of one device type. Device UI choices should describe layouts such as `Default`, `Compact`, `Grid`, `Modern` or `Round`; they are not copies of the application color themes.

Changing an application theme must not change which Device UI template is selected. A Device UI template may omit colors entirely so that it follows the current application theme/fallback appearance.

## 2. Application theme JSON

```json
{
  "schemaVersion": 1,
  "id": "my-theme",
  "name": "My Theme",
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
    "Gray950": "#141414"
  }
}
```

Theme fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `schemaVersion` | integer | Currently `1`. |
| `id` | string | Stable unique ID. |
| `name` | string | User-visible name. |
| `mode` | string | `light` or `dark`. |
| `minimumRuntimeVersion` | integer | Minimum compatible HomeController runtime. |
| `colors` | object | Application resource name to MAUI color value. `#RRGGBB` or `#AARRGGBB` is recommended. |

The theme catalog is `themes/index.json` and contains `id`, `name`, `file` and `minimumRuntimeVersion` for each application theme.

## 3. Device types

Device types are registered in `device-types.json`.

```json
{
  "id": "philips-hue",
  "displayName": "Philips Hue",
  "icon": "💡",
  "connections": ["wifi"],
  "databaseTypeNames": [],
  "sourcePathHints": ["PhilipsHueV2", "Philips Hue", "Hue"],
  "defaultUiTemplates": { "wifi": "hue-default" },
  "setupHandler": "philips-hue"
}
```

| Field | Meaning |
| --- | --- |
| `id` | Stable device type ID used by UI templates. |
| `displayName` | User-visible type name. |
| `icon` | Emoji/text icon. |
| `connections` | Supported connection names: normally `infrared`, `wifi`, `bluetooth`. |
| `databaseTypeNames` | Device-database category aliases. May be empty for integrations. |
| `sourcePathHints` | Hints for identifying older saved devices. |
| `defaultUiTemplates` | Connection name to default UI-template ID. |
| `setupHandler` | Optional built-in setup flow. |

For built-in integrations, driver identity can also be authoritative. For example, `PhilipsHueV2` resolves to `philips-hue` and `HubitatMakerApi` resolves to `hubitat`, including devices saved by older HomeController versions as `general`.

## 4. Device UI template top-level fields

```json
{
  "schemaVersion": 1,
  "id": "hue-grid",
  "name": "Philips Hue Grid",
  "deviceTypeId": "philips-hue",
  "connections": ["wifi"],
  "renderer": "builtin-hue",
  "columns": 2,
  "buttonCornerRadius": 12,
  "sectionCornerRadius": 12,
  "buttonHeight": 48,
  "buttonFontSize": 12,
  "iconFontSize": 20,
  "itemDefaults": { "columns": 2, "displayMode": "card" },
  "itemStyles": {
    "scene": { "columns": 3, "displayMode": "compact" }
  },
  "sections": []
}
```

Supported top-level fields:

| Field | Meaning |
| --- | --- |
| `schemaVersion` | Currently `1`. |
| `id` | Stable unique template ID. |
| `name` | Name shown by the device `UI` selector. |
| `deviceTypeId` | Target device type, e.g. `television`, `air-conditioner`, `hubitat`, `philips-hue`. |
| `connections` | Connections for which the template is selectable. |
| `renderer` | Rendering engine. See below. |
| `columns` | General grid column count. |
| `backgroundColor` | Optional page background. |
| `foregroundColor` | Optional primary text color. |
| `mutedTextColor` | Optional secondary/status text color. |
| `surfaceColor` | Optional cards/sections background. |
| `accentColor` | Optional active/selected color. |
| `buttonColor` | Optional default control background. |
| `buttonTextColor` | Optional control text color. When omitted, supported renderers choose black or white from background luminance. |
| `borderColor` | Optional border color. |
| `themeSwitcherBackgroundColor` | Optional background for the small `UI` selector beside the device title. |
| `themeSwitcherTextColor` | Optional selector text color. |
| `themeSwitcherBorderColor` | Optional selector border color. |
| `themeSwitcherText` | Selector caption; default `UI`. |
| `themeSwitcherOpacity` | Selector opacity. |
| `buttonCornerRadius` | Default control corner radius. |
| `sectionCornerRadius` | Default card/section corner radius. |
| `buttonHeight` | Default control height. |
| `buttonFontSize` | Default control text size. |
| `iconFontSize` | Default icon size. |
| `itemDefaults` | General style/layout for dynamically discovered Hue/Hubitat items. |
| `itemStyles` | Item-type/category-specific overrides. |
| `sections` | Declarative sections and controls. |

All visual colors are optional. Omitting them is recommended for a neutral/default Device UI that follows the normal HomeController appearance.

### Renderers

- `declarative`: controls and layout come from JSON.
- `builtin-ir-tv`: legacy built-in infrared TV page.
- `builtin-ir-ac`: legacy built-in infrared A/C page.
- `builtin-wifi-ac`: supported built-in Wi-Fi A/C page.
- `builtin-hubitat`: Hubitat integration with DeviceDB layout/style configuration.
- `builtin-hue`: Philips Hue integration with DeviceDB layout/style configuration.
- `builtin-dashboard`: dashboard page.

## 5. Dynamic item layout: `itemDefaults` and `itemStyles`

Hue and Hubitat contain resources discovered at runtime, so their individual cards cannot be listed in advance like TV remote buttons. Instead, templates use two levels:

1. `itemDefaults` is applied to every discovered item.
2. If `itemStyles` contains a matching item type/category, its non-null fields override `itemDefaults`.

Example:

```json
{
  "columns": 3,
  "itemDefaults": {
    "columns": 3,
    "displayMode": "compact",
    "showName": true,
    "showType": false,
    "showState": true
  },
  "itemStyles": {
    "light": {
      "columns": 2,
      "displayMode": "card",
      "showType": true
    },
    "temperature": {
      "columns": 3,
      "displayMode": "compact"
    }
  }
}
```

### `DeviceUiItemStyle` fields

| Field | Type | Meaning |
| --- | --- | --- |
| `columns` | integer/null | Desired number of items per row for this type. The renderer derives the required column span from the section's base grid. |
| `columnSpan` | integer/null | Explicit base-grid column span. If present, it overrides the span derived from `columns`. |
| `displayMode` | string/null | `card`, `compact`, or `hidden`. `hidden` removes this type from the rendered list. |
| `shape` | string/null | `rounded`, `circle`, `pill`, or `square` where the renderer supports shaped cards/actions. |
| `backgroundColor` | color/null | Item/card/control background. |
| `textColor` | color/null | Main item text. |
| `mutedTextColor` | color/null | Secondary item text. |
| `borderColor` | color/null | Border. |
| `accentColor` | color/null | Active/accent action. |
| `cornerRadius` | integer/null | Explicit corner radius when `shape` does not determine it. |
| `height` | number/null | Requested item/control height. |
| `width` | number/null | Requested fixed width. |
| `fontSize` | number/null | Main item/control text size. |
| `iconSize` | number/null | Icon size. |
| `showIcon` | boolean/null | Show/hide item icon when available. |
| `showName` | boolean/null | Show/hide item name. |
| `showType` | boolean/null | Show/hide resource/category type text. |
| `showState` | boolean/null | Show/hide state details. |

Per-type matching is case-insensitive. The runtime also tries a normalized key where spaces and underscores become hyphens.

## 6. Philips Hue item type keys

Hue `itemStyles` can target the resource types returned by the Bridge. Common supported keys include:

- `light`
- `grouped-light` (`grouped_light` also matches exactly)
- `scene`
- `motion`
- `temperature`
- `light-level`
- `contact`
- `button`
- `relative-rotary`
- `switch-input-configuration`
- `device-power`
- `zigbee-connectivity`
- `room`
- `zone`
- `bridge`
- `bridge-home`
- `entertainment-configuration`

Example:

```json
"itemDefaults": {
  "columns": 2,
  "displayMode": "card"
},
"itemStyles": {
  "scene": {
    "columns": 3,
    "displayMode": "compact",
    "showType": false,
    "showState": false
  },
  "temperature": {
    "columns": 3,
    "displayMode": "compact"
  }
}
```

The built-in Hue renderer keeps protocol behavior such as ON/OFF, brightness, color temperature, color presets, grouped lights and scene recall; the DeviceDB template changes their layout/presentation.

## 7. Hubitat category keys

Hubitat `itemStyles` keys match the category produced by HomeController's Maker API classifier. Matching is case-insensitive and also supports normalized names with spaces/underscores replaced by hyphens.

Typical examples are `switch`, `dimmer`, `light`, `motion`, `contact`, `temperature` and other categories returned by the classifier. Unknown/new categories automatically fall back to `itemDefaults`, so a template remains forward compatible.

Example:

```json
"itemDefaults": {
  "columns": 3,
  "displayMode": "compact",
  "showType": false
},
"itemStyles": {
  "dimmer": {
    "columns": 2,
    "displayMode": "card",
    "showType": true
  }
}
```

The selected Hubitat template is carried into the detailed child-device page as well.

## 8. Declarative remote sections and controls

A declarative template contains sections with `title`, `subtitle`, optional `backgroundColor`, and `controls`.

Supported control types currently include `button`, `tile`, `toggle`, `stepper`, `slider`, and `picker`.

Control fields:

| Field | Meaning |
| --- | --- |
| `type` | Control type. |
| `label` | Caption. |
| `command` | Command dispatcher identifier. |
| `value` | Optional fixed command value. |
| `icon` | Optional emoji/text icon. |
| `shape` | `rounded`, `circle`, `pill`, or `square` for buttons/tiles. |
| `columnSpan` | Grid columns occupied. |
| `minimum`, `maximum`, `step` | Range settings for stepper/slider controls. |
| `stateField` | Optional associated state field. |
| `options` | Picker options. |
| `backgroundColor`, `textColor`, `borderColor` | Per-control visual overrides. |
| `height` | Per-control height. For a `circle`, height defines its diameter when no separate sizing is needed. |
| `width` | Optional fixed width. |
| `fontSize` | Per-control text size. |
| `iconSize` | Per-control icon size. |
| `iconOnly` | Hide label and emphasize the icon where supported. |

### Round remote example

```json
{
  "type": "tile",
  "label": "",
  "command": "Power",
  "icon": "⏻",
  "iconOnly": true,
  "shape": "circle",
  "height": 60
}
```

A pill-shaped action:

```json
{
  "type": "tile",
  "label": "BACK",
  "command": "Back",
  "shape": "pill",
  "height": 54
}
```

This makes it possible to create remote layouts with circular navigation/media buttons without hard-coding a specific third-party remote design.

## 9. UI-template index

`ui-templates/index.json` registers selectable Device UI templates:

```json
{
  "schemaVersion": 1,
  "templates": [
    { "id": "hue-default", "path": "hue-default.json", "status": "stable" },
    { "id": "hue-grid", "path": "hue-grid.json", "status": "stable" }
  ]
}
```

The application uses `id` and `path`; `status` is repository metadata.

## 10. Premium custom source `index.json`

A custom source URL configured in Settings must point to an `index.json`. It requires **actively enabled Premium**; the Premium grace period does not unlock it.

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
      "id": "my-hue-layout",
      "path": "ui/my-hue-layout.json",
      "status": "stable"
    }
  ],
  "deviceTypes": []
}
```

Paths are relative to the directory containing `index.json`. Custom data is merged with the public DeviceDB. A matching ID replaces that ID in the merged runtime catalog; unrelated built-in entries remain available. Invalid/unreachable custom sources are ignored rather than disabling the built-in DeviceDB.

## 11. Refreshing local UI data

HomeController Settings contains a **Refresh themes and device UI templates** action. It:

- deletes the local application-theme cache,
- forces fresh DeviceDB theme/template downloads,
- re-resolves saved device type IDs,
- refreshes each saved device's `UiTemplateSnapshotJson` from the currently selected template or its default fallback.

It does **not** delete or reset non-UI device configuration such as IP addresses, pairing data, drivers, IR commands, dashboard URLs, device names, hardware IDs or protocol configuration.

## 12. Compatibility recommendations

- Keep `schemaVersion` at `1` until a newer runtime schema is explicitly introduced.
- Use stable lowercase IDs with hyphens.
- Prefer `#RRGGBB`/`#AARRGGBB` colors.
- Keep identity/routing fields (`id`, `deviceTypeId`, `connections`, `renderer`).
- Omit device-template colors when the layout should follow the application theme/default appearance.
- Put broad behavior in `itemDefaults`, then override only exceptional resource/category types in `itemStyles`.
- Unknown JSON fields are ignored by the current deserializer, allowing forward-compatible additions.
