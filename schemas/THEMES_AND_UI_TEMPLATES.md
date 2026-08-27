# HomeController theme and Device UI schema reference

This is the public customization contract for HomeController runtime schema version 1. It documents the fields that are currently understood by the app, their inheritance rules, renderer limitations, compatibility aliases, and complete examples.

Machine-readable schemas are provided next to this file:

- `app-theme-v1.schema.json`
- `device-ui-template-v1.schema.json`
- `device-types-v1.schema.json`
- `custom-source-index-v1.schema.json`

## 1. Two independent customization layers

**Application themes** (`themes/*.json`) define application-wide colors. Default, Blue Eye, Red Eye and custom color themes belong here.

**Device UI templates** (`ui-templates/*.json`) define the layout and presentation of a device. Examples are Default, Modern, Compact, Grid and Round. Device UI templates must not be named after application color themes.

Changing an application theme does not change the selected Device UI template. A Device UI template should normally omit explicit colors so it follows the selected application theme.

---

# Part A — Application themes

## 2. Application theme file

```json
{
  "$schema": "../schemas/app-theme-v1.schema.json",
  "schemaVersion": 1,
  "id": "my-theme",
  "name": "My Theme",
  "mode": "dark",
  "minimumRuntimeVersion": 1,
  "colors": {
    "Primary": "#365E91",
    "PrimaryDark": "#243E60",
    "PrimaryLight": "#769BC7",
    "OnPrimary": "#FFFFFF",
    "Secondary": "#18212B",
    "OnSecondary": "#D7E5F4",
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
    "PageBackground": "#0B1118",
    "Surface": "#18212B",
    "SurfaceVariant": "#223041",
    "TextPrimary": "#FFFFFF",
    "TextSecondary": "#D7E5F4",
    "TextMuted": "#93A4B7",
    "Accent": "#6FA8E8",
    "OnAccent": "#07111D",
    "NavigationBackground": "#365E91",
    "NavigationText": "#FFFFFF",
    "CardBackground": "#18212B",
    "CardBorder": "#33475E",
    "InputBackground": "#111B27",
    "InputText": "#FFFFFF",
    "PlaceholderText": "#93A4B7",
    "ButtonBackground": "#243E60",
    "ButtonText": "#FFFFFF",
    "SecondaryButtonBackground": "#33475E",
    "SecondaryButtonText": "#FFFFFF",
    "DisabledBackground": "#33475E",
    "DisabledText": "#AEB9C5",
    "Separator": "#33475E",
    "Danger": "#B84A55",
    "OnDanger": "#FFFFFF",
    "Success": "#54A978",
    "OnSuccess": "#07111D"
  }
}
```

Top-level fields:

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `schemaVersion` | integer | yes | Must be `1`. |
| `id` | string | yes | Stable lowercase ID. Hyphenated IDs are recommended. |
| `name` | string | yes | User-visible theme name. |
| `mode` | `light` / `dark` | yes | Controls the platform light/dark mode. |
| `minimumRuntimeVersion` | integer | yes | Minimum HomeController runtime schema version. |
| `colors` | object | yes | Resource-name to color map. Use `#RRGGBB` or `#AARRGGBB`. |

The runtime validates every supplied color. An invalid color rejects the theme and falls back to a cached or built-in version.

## 3. Canonical application color resources

These names are the stable public resource names for new themes and new HomeController UI code.

### Core palette

| Key | Role |
| --- | --- |
| `Primary` | Main brand/action color. |
| `PrimaryDark` | Darker primary variant. |
| `PrimaryLight` | Lighter primary variant. |
| `OnPrimary` | Text/icon color displayed on primary. |
| `Secondary` | Secondary surface/accent palette color. |
| `OnSecondary` | Text/icon color displayed on secondary. |
| `Tertiary` | Third accent color. |
| `White`, `Black` | Explicit neutral endpoints. |
| `Gray100`, `Gray200`, `Gray300`, `Gray400`, `Gray500`, `Gray600`, `Gray900`, `Gray950` | Neutral scale from light to dark. |

### Semantic roles

| Key | Used for |
| --- | --- |
| `PageBackground` | Page/window background. |
| `Surface` | General panel/surface background. |
| `SurfaceVariant` | Secondary panel or highlighted surface. |
| `TextPrimary` | Main text. |
| `TextSecondary` | Secondary/supporting text. |
| `TextMuted` | Hints, metadata and low-emphasis status text. |
| `Accent` | Selected state, active controls, status emphasis. |
| `OnAccent` | Text/icon shown on Accent. |
| `NavigationBackground` | Top navigation/header background. |
| `NavigationText` | Navigation title/icons. |
| `CardBackground` | Cards/frames. |
| `CardBorder` | Card/frame border. |
| `InputBackground` | Entry/editor/picker background. |
| `InputText` | Text entered into controls. |
| `PlaceholderText` | Placeholder/picker hint text. |
| `ButtonBackground` | Default button background. |
| `ButtonText` | Default button text/icon. |
| `SecondaryButtonBackground` | Secondary button background. |
| `SecondaryButtonText` | Secondary button text. |
| `DisabledBackground` | Disabled control background. |
| `DisabledText` | Disabled text/icon. |
| `Separator` | Dividers and list separators. |
| `Danger` | Destructive/error emphasis. |
| `OnDanger` | Text/icon shown on Danger. |
| `Success` | Success/positive status. |
| `OnSuccess` | Text/icon shown on Success. |

The built-in themes explicitly define all of these roles. For compatibility, the runtime can derive missing semantic roles from the core palette in older/custom v1 themes. New themes should define the complete set so their appearance is intentional.

Additional custom color keys are accepted and loaded as MAUI resources, but they are **not part of the stable HomeController public contract** unless documented here. Do not rely on an arbitrary custom key for built-in HomeController controls.

## 4. Deprecated application resource aliases

These aliases are runtime compatibility only. Do not use them in new JSON or XAML.

| Deprecated | Canonical replacement |
| --- | --- |
| `PrimaryDarkText` | `OnPrimary` |
| `SecondaryDarkText` | `OnSecondary` |
| `BlueEyePrimary` | `Primary` |
| `BlueEyePrimaryDark` | `PrimaryDark` |
| `BlueEyePrimaryLight` | `PrimaryLight` |
| `BlueEyeDarkBg` | `PageBackground` |
| `BlueEyeSurface` | `Surface` |
| `BlueEyeAccent` | `Accent` |
| `RedEyePrimary` | `Primary` |
| `RedEyePrimaryDark` | `PrimaryDark` |
| `RedEyePrimaryLight` | `PrimaryLight` |
| `RedEyeDarkBg` | `PageBackground` |
| `RedEyeSurface` | `Surface` |
| `RedEyeAccent` | `Accent` |

The aliases are generated by the runtime after loading a theme so old cached themes and older compiled views continue to work. They should never appear in a new DeviceDB theme file.

## 5. Built-in semantic XAML styles

These are application styles, not DeviceDB JSON fields. They are useful when adding or maintaining HomeController pages:

| Style key | Target | Purpose |
| --- | --- | --- |
| implicit `ContentPage` | ContentPage | `PageBackground`. |
| implicit `Label` | Label | Default typography and `TextPrimary`. |
| implicit `Button` | Button | 48dp touch target, `ButtonBackground` / `ButtonText`, pressed/disabled states. |
| implicit `ImageButton` | ImageButton | 48dp touch target. |
| implicit `Entry` | Entry | Semantic input colors and 48dp height. |
| implicit `Editor` | Editor | Semantic multiline input colors. |
| implicit `Picker` | Picker | Semantic picker colors. |
| implicit `SearchBar` | SearchBar | Semantic search text/placeholder. |
| implicit `DatePicker`, `TimePicker` | picker | Semantic input colors. |
| implicit `CheckBox`, `Switch`, `Slider` | controls | Accent-based active state. |
| implicit `Frame` | Frame | Card background/border and standard radius. |
| implicit `ListView` | ListView | Semantic separator and refresh color. |
| implicit `ActivityIndicator`, `ProgressBar` | indicators | Accent color. |
| `AppPageTitle` | Label | Main page heading. |
| `AppSectionTitle` | Label | Section heading. |
| `AppCardTitle` | Label | Card heading. |
| `AppSecondaryText` | Label | Secondary text. |
| `AppStatusText` | Label | Accent status text. |
| `AppErrorText` | Label | Danger/error text. |
| `AppSuccessText` | Label | Success text. |
| `AppSecondaryButton` | Button | Secondary button role. |
| `AppDangerButton` | Button | Destructive action. |
| `AppToolbarButton` | Button | Transparent 48dp toolbar action. |
| `AppCompactButton` | Button | Compact visual button while preserving touch size. |
| `AppCard` | Frame | Standard app card. |
| `RemoteSectionTitle` | Label | Device remote section heading. |
| `RemoteStatusText` | Label | Device status emphasis. |

Use these style keys instead of hard-coded theme-specific colors whenever possible.

---

# Part B — Device types

## 6. `device-types.json`

Validated by `device-types-v1.schema.json`.

```json
{
  "schemaVersion": 1,
  "deviceTypes": [
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
  ]
}
```

| Field | Meaning |
| --- | --- |
| `id` | Stable ID referenced by templates. |
| `displayName` | User-visible type name. |
| `icon` | Emoji/text icon. |
| `connections` | Any of `infrared`, `wifi`, `bluetooth`. |
| `databaseTypeNames` | Device database category aliases. |
| `sourcePathHints` | Compatibility hints for identifying old saved devices. |
| `defaultUiTemplates` | Connection name to default template ID. |
| `setupHandler` | Built-in setup flow ID; empty string means no special handler. |

Built-in driver identity can override an old generic saved type. `PhilipsHueV2` resolves to `philips-hue`; `HubitatMakerApi` resolves to `hubitat`.

---

# Part C — Device UI templates

## 7. Complete top-level Device UI template

Validated by `device-ui-template-v1.schema.json`.

```json
{
  "$schema": "../schemas/device-ui-template-v1.schema.json",
  "schemaVersion": 1,
  "id": "hue-grid",
  "name": "Philips Hue Grid",
  "deviceTypeId": "philips-hue",
  "connections": ["wifi"],
  "renderer": "builtin-hue",
  "columns": 2,
  "useFullWidth": true,
  "backgroundColor": null,
  "foregroundColor": null,
  "mutedTextColor": null,
  "surfaceColor": null,
  "accentColor": null,
  "buttonColor": null,
  "buttonTextColor": null,
  "borderColor": null,
  "buttonCornerRadius": 12,
  "sectionCornerRadius": 12,
  "buttonHeight": 48,
  "buttonFontSize": 12,
  "iconFontSize": 20,
  "itemDefaults": { "columns": 2, "displayMode": "card" },
  "itemStyles": {},
  "sections": []
}
```

### Stable top-level fields

| Field | Type/default | Meaning |
| --- | --- | --- |
| `schemaVersion` | integer / `1` | Schema version. |
| `id` | string | Stable template ID. |
| `name` | string | Name listed in Device Settings. |
| `deviceTypeId` | string | Target type, e.g. `television`, `air-conditioner`, `hubitat`, `philips-hue`. |
| `connections` | string[] | Connections for which the template is selectable. |
| `renderer` | string | Rendering engine. |
| `columns` | integer / `3` | Base grid column count. |
| `useFullWidth` | bool / `true` | `true`: use all available page width inside responsive padding. `false`: deliberately constrain the remote to a narrower centered width. Current built-in templates should use/omit this as `true`. |
| `backgroundColor` | color/null | Optional page background override. |
| `foregroundColor` | color/null | Primary text override. |
| `mutedTextColor` | color/null | Secondary/status text override. |
| `surfaceColor` | color/null | Card/section surface override. |
| `accentColor` | color/null | Active/accent override. |
| `buttonColor` | color/null | Default template button background. |
| `buttonTextColor` | color/null | Default template button text. If omitted, supported renderers calculate contrast. |
| `borderColor` | color/null | Default border override. |
| `buttonCornerRadius` | int / `8` | Default button radius. |
| `sectionCornerRadius` | int / `14` | Default section/card radius. |
| `buttonHeight` | number / `54` | Default button height. Runtime accessibility rules may enforce a larger minimum. |
| `buttonFontSize` | number / `13` | Default button label size. |
| `iconFontSize` | number / `24` | Default icon size. |
| `itemDefaults` | object | General Hue/Hubitat discovered-item style. |
| `itemStyles` | object | Per-type/category Hue/Hubitat overrides. |
| `sections` | array | Declarative remote sections. |

All template colors are optional. Omit them when the device layout should follow the application theme.

### Legacy UI-switcher fields

`themeSwitcherBackgroundColor`, `themeSwitcherTextColor`, `themeSwitcherBorderColor`, `themeSwitcherText`, and `themeSwitcherOpacity` are accepted for old templates but are deprecated. Device UI selection now lives on the separate Device Settings page, so these fields have no guaranteed visible effect in current device views. Do not use them in new templates.

## 8. Renderers and what each renderer uses

| Renderer | Purpose | JSON layout support |
| --- | --- | --- |
| `declarative` | General remote generated from `sections`/`controls`. | Full declarative layout/control styling. |
| `builtin-ir-tv` | Built-in infrared TV remote. | Uses built-in TV structure; application theme drives colors. |
| `builtin-ir-ac` | Built-in infrared A/C remote. | Uses built-in A/C structure; application theme drives colors. |
| `builtin-wifi-ac` | Built-in supported Wi-Fi A/C page. | Built-in behavior with template/app styling where implemented. |
| `builtin-hubitat` | Hubitat Maker API UI. | `columns`, `useFullWidth`, top-level colors, `itemDefaults`, `itemStyles`. |
| `builtin-hue` | Philips Hue UI. | `columns`, `useFullWidth`, top-level colors, `itemDefaults`, `itemStyles`. |
| `builtin-dashboard` | Dashboard WebView page. | Built-in dashboard UI. |

Fields unsupported by a particular built-in renderer are ignored safely. For maximum portability, use declarative templates when the structure itself must come entirely from JSON.

## 9. Hue/Hubitat `itemDefaults` and `itemStyles`

Inheritance order is:

1. renderer/application defaults;
2. template top-level values;
3. `itemDefaults`;
4. matching `itemStyles[type-or-category]` non-null fields.

Matching is case-insensitive. The runtime also normalizes spaces and underscores to hyphens for category matching.

Complete `DeviceUiItemStyle` fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `columns` | int/null | Desired number of items per row for this type. |
| `columnSpan` | int/null | Explicit number of base-grid columns occupied; overrides span derived from `columns`. |
| `displayMode` | string/null | `card`, `compact`, `button`, or `hidden`. `hidden` removes the item. Renderer support for `button` is renderer-specific; `card`, `compact`, `hidden` are the common modes. |
| `shape` | string/null | `rounded`, `circle`, `pill`, `square` when the renderer uses shaped item containers/actions. |
| `backgroundColor` | color/null | Item/card background. |
| `textColor` | color/null | Main text. |
| `mutedTextColor` | color/null | Supporting text. |
| `borderColor` | color/null | Border. |
| `accentColor` | color/null | Active/accent action color. |
| `cornerRadius` | int/null | Explicit radius. |
| `height` | number/null | Requested height. |
| `width` | number/null | Requested fixed width. Prefer null for responsive layouts. |
| `fontSize` | number/null | Main label size. |
| `iconSize` | number/null | Icon size. |
| `showIcon` | bool/null | Show/hide icon if available. |
| `showName` | bool/null | Show/hide name. |
| `showType` | bool/null | Show/hide resource/category type. |
| `showState` | bool/null | Show/hide state details. |

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
    "dimmer": { "columns": 2, "displayMode": "card", "showType": true },
    "temperature": { "columns": 3, "displayMode": "compact" }
  }
}
```

### Philips Hue item keys

Common Bridge resource keys supported by the built-in categorization include:

`light`, `grouped-light` / `grouped_light`, `scene`, `motion`, `temperature`, `light-level` / `light_level`, `contact`, `button`, `relative-rotary` / `relative_rotary`, `switch-input-configuration`, `device-power`, `zigbee-connectivity`, `room`, `zone`, `bridge`, `bridge-home`, `entertainment-configuration`.

Unknown future Hue types fall back to `itemDefaults`.

### Hubitat item keys

Hubitat keys are the categories produced by HomeController's Maker API classifier. Common categories include `switch`, `dimmer`, `light`, `motion`, `contact`, `temperature` and other detected capabilities/categories. Unknown categories fall back to `itemDefaults`.

The selected Hubitat template is propagated into the child-device detail page.

## 10. Declarative `sections`

A section supports exactly:

| Field | Type | Meaning |
| --- | --- | --- |
| `title` | string/null | Section title. |
| `subtitle` | string/null | Secondary section text. |
| `backgroundColor` | color/null | Section background override. |
| `controls` | array | Controls in this section. |

## 11. Declarative control types and every control field

Supported `type` values:

- `button` — momentary command button;
- `tile` — tile-like command button;
- `toggle` — boolean state/action;
- `stepper` — increment/decrement numeric value;
- `slider` — continuous numeric value;
- `picker` — select from string options.

Every `UiTemplateControl` field:

| Field | Type/default | Meaning |
| --- | --- | --- |
| `type` | string / `button` | One of the six types above. |
| `label` | string / empty | Visible label. |
| `command` | string | Command dispatcher identifier. |
| `value` | any/null | Optional fixed command value. |
| `icon` | string/null | Emoji/text glyph. |
| `shape` | string/null | `rounded`, `circle`, `pill`, `square`. |
| `columnSpan` | int / `1` | Number of template grid columns occupied. |
| `minimum` | number/null | Minimum for slider/stepper. |
| `maximum` | number/null | Maximum for slider/stepper. |
| `step` | number/null | Numeric increment. |
| `stateField` | string/null | Associated device state field. |
| `options` | string[] | Picker values. |
| `backgroundColor` | color/null | Per-control background. |
| `textColor` | color/null | Per-control text. |
| `borderColor` | color/null | Per-control border. |
| `height` | number/null | Requested control height. Accessibility minimums may override smaller values. |
| `width` | number/null | Fixed width. Prefer null unless deliberately fixed. |
| `fontSize` | number/null | Label font size. |
| `iconSize` | number/null | Icon size. |
| `iconOnly` | bool / `false` | Hide the label and emphasize the icon where supported. |

### Shape examples

Circular icon button:

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

Pill action:

```json
{
  "type": "button",
  "label": "BACK",
  "command": "Back",
  "shape": "pill",
  "height": 54
}
```

Square button:

```json
{
  "type": "button",
  "label": "MENU",
  "command": "Menu",
  "shape": "square",
  "height": 54
}
```

## 12. Responsive layout rules

- `useFullWidth` defaults to `true`.
- Full-width templates fill the available width inside HomeController's responsive page padding.
- `useFullWidth: false` is intended only for deliberately narrow remote-style layouts; the content remains centered.
- The runtime keeps touch targets at least approximately 48dp where HomeController controls are involved.
- Portrait/landscape resizing changes density/available width but should not arbitrarily reorder a template's command sequence.
- Avoid fixed `width` unless the control truly must have a fixed width.

## 13. UI template index

`ui-templates/index.json`:

```json
{
  "schemaVersion": 1,
  "templates": [
    { "id": "hue-default", "path": "hue-default.json", "status": "stable" },
    { "id": "hue-grid", "path": "hue-grid.json", "status": "stable" }
  ]
}
```

`id` must match the template file's `id`. `path` is relative to `ui-templates/index.json`. `status` is repository metadata; `stable` is recommended for normal selectable templates.

---

# Part D — Custom source

## 14. Premium custom `index.json`

Validated by `custom-source-index-v1.schema.json`. The custom source requires **actively enabled Premium**. The Premium grace period does not unlock custom sources.

```json
{
  "$schema": "schemas/custom-source-index-v1.schema.json",
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
      "id": "my-tv-layout",
      "path": "ui/my-tv-layout.json",
      "status": "stable"
    }
  ],
  "deviceTypes": []
}
```

All paths are relative to the directory containing the custom `index.json`. Custom entries are merged into the public catalog. A matching ID replaces that ID in the merged runtime catalog; unrelated public entries remain available. An invalid or unreachable custom source is ignored rather than disabling the built-in DeviceDB.

## 15. Refreshing local UI data

Settings contains **Refresh themes and device UI templates**. It removes local application-theme/UI-template cache, downloads current theme/template metadata again, re-resolves saved device type IDs and refreshes UI snapshots. It does **not** delete device names, IP addresses, ports, drivers, IR commands, Hue/Hubitat pairing, dashboard URLs, hardware IDs or other protocol/device configuration.

## 16. Compatibility and authoring rules

1. Keep `schemaVersion: 1` until runtime version 2 is explicitly introduced.
2. Use stable lowercase hyphenated IDs.
3. Use `#RRGGBB` or `#AARRGGBB` colors.
4. New application themes should define the full canonical color set from section 3.
5. Do not use `BlueEye*`, `RedEye*`, `PrimaryDarkText` or `SecondaryDarkText` in new theme files.
6. Prefer semantic application resources (`PageBackground`, `TextPrimary`, `ButtonBackground`, etc.) in HomeController XAML/code.
7. Device UI templates should describe layout, not duplicate application color themes.
8. Omit Device UI colors when the template should follow the current application theme.
9. Prefer `useFullWidth: true`; choose `false` only intentionally.
10. Put broad Hue/Hubitat styling in `itemDefaults`, then override exceptions in `itemStyles`.
11. Unknown Hue/Hubitat types should be allowed to fall back to `itemDefaults`.
12. Prefer responsive column spans to fixed widths.
13. Use the machine-readable schemas during editing/CI whenever possible.

The machine-readable schema files and this document are intended to describe the same runtime contract. If they ever disagree, treat that as a repository bug and update both together.
