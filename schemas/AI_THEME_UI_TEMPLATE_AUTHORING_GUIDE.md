# HomeController — AI Theme & Device UI Template Authoring Guide

> Canonical AI-facing authoring reference for HomeController DeviceDB themes and Device UI templates.
>
> Purpose: an AI model should be able to create a valid theme or device UI template from this document together with the machine-readable schemas in this directory, without having to inspect the HomeController source code.

## 1. Source of truth and terminology

HomeController has two independent presentation layers:

1. **Application theme** — global colors and application visual identity. Stored under `themes/` and validated by `app-theme-v1.schema.json`.
2. **Device UI template** — layout, controls and presentation of a device screen. Stored under `ui-templates/` and validated primarily by `device-ui-template-v2.schema.json` for new templates. V1 remains a compatibility format.

Do not encode a color theme by duplicating a device template. A template should normally inherit semantic colors from the active application theme.

The historical/user-facing term "UI template" and any shorthand such as "JUHAS template" in project discussion refer to the **Device UI template system** documented here.

Machine-readable files to consult:

- `app-theme-v1.schema.json`
- `theme-catalog-v1.schema.json`
- `device-ui-template-v2.schema.json`
- `device-ui-template-v1.schema.json` (legacy/compatibility)
- `ui-template-index-v1.schema.json`
- `device-types-v1.schema.json`
- `device-images-v1.schema.json`
- `../images/catalog.json`

Human references:

- `THEMES_AND_UI_TEMPLATES.md`
- `UI_TEMPLATE_FORMAT.md`
- `DEVICE_UI_THEME_REFERENCES.md`
- this document

## 2. AI generation rules

When generating a new template:

1. Prefer `schemaVersion: 2`.
2. Use a stable lowercase hyphenated `id`.
3. Set `deviceTypeId` to the actual logical device type.
4. Set only applicable `connections` (`infrared`, `wifi`, `bluetooth`).
5. Prefer `renderer: "declarative"` when the complete layout must be controlled by JSON.
6. Use a built-in renderer only when the device/integration requires its runtime behavior.
7. Prefer semantic theme inheritance; omit explicit colors unless the design intentionally overrides the active theme.
8. Prefer assets from `images/catalog.json`; do not invent filenames.
9. Do not invent commands, state/property names, child sources or driver capabilities. They must exist in the target device/driver/integration.
10. Give every reusable group/control a stable `id`.
11. Keep touch controls large enough for mobile use; the runtime may enforce accessibility minimums.
12. Use localization variants instead of creating separate logical templates solely for language.
13. Validate generated JSON against the relevant schema and DeviceDB validation before publishing.

## 3. Localization and logical template identity

Language variants are one logical template. Example:

- `wifi-tv-default.json`
- `wifi-tv-default-en.json`
- `wifi-tv-default-hu.json`

The picker should expose one logical template: `wifi-tv-default`. At runtime the current-language file is preferred and the language-neutral file is the fallback. Language suffixes must not create separate visual template choices.

IDs, command names, state keys, image names and property names must remain language-neutral. Only user-visible text should be localized.

## 4. Application theme format

Minimal structure:

```json
{
  "$schema": "../schemas/app-theme-v1.schema.json",
  "schemaVersion": 1,
  "id": "example-dark",
  "name": "Example Dark",
  "mode": "dark",
  "minimumRuntimeVersion": 1,
  "colors": {}
}
```

Top-level theme properties:

| Property | Type | Meaning |
|---|---|---|
| `$schema` | string | Optional schema reference. |
| `schemaVersion` | integer | Theme schema version; currently `1`. |
| `id` | string | Stable theme ID. |
| `name` | string | User-visible theme name. |
| `mode` | `light`/`dark` | Platform/application mode. |
| `minimumRuntimeVersion` | integer | Minimum compatible HomeController runtime. |
| `colors` | object | Semantic color resource map. |

Canonical theme color keys:

`Primary`, `PrimaryDark`, `PrimaryLight`, `OnPrimary`, `Secondary`, `OnSecondary`, `Tertiary`, `White`, `Black`, `Gray100`, `Gray200`, `Gray300`, `Gray400`, `Gray500`, `Gray600`, `Gray900`, `Gray950`, `PageBackground`, `Surface`, `SurfaceVariant`, `TextPrimary`, `TextSecondary`, `TextMuted`, `Accent`, `OnAccent`, `NavigationBackground`, `NavigationText`, `CardBackground`, `CardBorder`, `InputBackground`, `InputText`, `PlaceholderText`, `ButtonBackground`, `ButtonText`, `SecondaryButtonBackground`, `SecondaryButtonText`, `DisabledBackground`, `DisabledText`, `Separator`, `Danger`, `OnDanger`, `Success`, `OnSuccess`.

Use `#RRGGBB` or `#AARRGGBB`. New themes should define the complete semantic set. Deprecated aliases such as `PrimaryDarkText`, `SecondaryDarkText`, `BlueEye*` and `RedEye*` exist only for compatibility and must not be generated in new themes.

### Theme inheritance into device UI

Effective visual value precedence is:

1. application theme semantic default;
2. Device UI template top-level override;
3. `itemDefaults`;
4. matching `itemStyles` or group/control override;
5. runtime state/interaction styling.

Therefore an AI should normally omit template colors when it wants a template to work correctly with every theme.

## 5. Device type definition and template selection

Device type fields understood by HomeController:

| Property | Type | Purpose |
|---|---|---|
| `id` | string | Stable logical type ID. |
| `displayName` | string | Default visible name. |
| `displayNames` | object | Localized display-name map where used. |
| `icon` | string | Legacy textual icon; new visual work should use the central image catalog. |
| `connections` | string[] | Supported connection families. |
| `databaseTypeNames` | string[] | DeviceDB category aliases. |
| `sourcePathHints` | string[] | Compatibility/type-identification hints. |
| `defaultUiTemplates` | object | Connection -> default template ID. |
| `testCommands` | string[] | Commands useful during add-device capability testing. |
| `setupHandler` | string | Built-in setup flow ID. |
| `selectable` | boolean | Whether the type is user-selectable. |

A template is applicable when its `deviceTypeId`, connection and renderer/runtime capabilities match the target device.

## 6. Device UI template — complete top-level property reference

The runtime model supports these top-level properties:

| Property | Type/default | Purpose |
|---|---|---|
| `schemaVersion` | int / `2` | Template format version. |
| `id` | string | Stable logical template ID. |
| `name` | string | User-visible template name. |
| `deviceTypeId` | string | Target logical device type. |
| `connections` | string[] | Applicable connection types. |
| `renderer` | string / `declarative` | Rendering engine. |
| `access` | string / `free` | Access level, e.g. free/premium. |
| `columns` | int / 3 | Base grid columns. |
| `useFullWidth` | bool / true | Use available page width. |
| `horizontalSpacing` | number / 10 | Horizontal item spacing. |
| `verticalSpacing` | number / 10 | Vertical item spacing. |
| `screenMarginLeft` | number / 12 | Left page margin. |
| `screenMarginTop` | number / 12 | Top page margin. |
| `screenMarginRight` | number / 12 | Right page margin. |
| `screenMarginBottom` | number / 12 | Bottom page margin. |
| `backgroundColor` | color/null | Primary page background override. |
| `backgroundColor2` | color/null | Secondary color for multi-color background modes. |
| `backgroundMode` | string / `solid` | Background rendering mode. |
| `backgroundImage` | string/null | Background asset. |
| `backgroundImageAspect` | string / `fill` | Background image fitting behavior. |
| `foregroundColor` | color/null | Main foreground/text override. |
| `mutedTextColor` | color/null | Secondary text override. |
| `surfaceColor` | color/null | Surface/card override. |
| `accentColor` | color/null | Accent override. |
| `buttonColor` | color/null | Default button background override. |
| `buttonTextColor` | color/null | Default button text override. |
| `borderColor` | color/null | Default border override. |
| `themeSwitcherBackgroundColor` | color/null | Legacy UI-switcher styling. Do not use in new templates unless compatibility requires it. |
| `themeSwitcherTextColor` | color/null | Legacy switcher text. |
| `themeSwitcherBorderColor` | color/null | Legacy switcher border. |
| `themeSwitcherText` | string / `UI` | Legacy switcher label. |
| `themeSwitcherOpacity` | number / .72 | Legacy switcher opacity. |
| `buttonCornerRadius` | int / 8 | Default button radius. |
| `sectionCornerRadius` | int / 14 | Section/group radius. |
| `buttonHeight` | number / 54 | Default button height. |
| `buttonFontSize` | number / 13 | Default button font size. |
| `iconFontSize` | number / 24 | Default legacy/text icon size. |
| `itemDefaults` | object | Default style for dynamically discovered child items. |
| `itemStyles` | object | Per category/type style overrides. |
| `sections` | array | Declarative sections. |
| `groups` | array | V2 layout groups. |
| `initialStates` | object | Initial template-local state key/value map. |
| `integrationChildPresentations` | object | Default pinned properties/commands/sliders for integration child device types. |

## 7. Renderers and program usage locations

| Renderer | Typical device/use location | Layout source | Notes |
|---|---|---|---|
| `declarative` | Generic remotes and JSON-defined device screens | `sections`, `groups`, controls | Preferred for AI-generated fully declarative screens. |
| `builtin-ir-tv` | Infrared television | Runtime TV remote + template styling | Commands must exist in IR data. |
| `builtin-ir-ac` | Infrared air conditioner | Runtime A/C behavior + styling | State-like controls depend on A/C capabilities. |
| `builtin-ir-simple` | Simple infrared device | Runtime/simple command UI | Suitable for simple command sets. |
| `builtin-wifi-ac` | Supported Wi-Fi A/C | Runtime Wi-Fi A/C behavior | Driver capabilities are authoritative. |
| `builtin-hubitat` | Hubitat parent/child UI | Dynamic integration items + item styles/pinning | Child properties/commands/sliders can be presented/pinned. |
| `builtin-hue` | Philips Hue parent/child UI | Dynamic Hue items + item styles | Lights and supported properties/actions are runtime-driven. |
| `builtin-dashboard` | Dashboard/multi-dashboard WebView | Runtime dashboard UI | Layout is mainly built in; URL entries are device data. |

Other HomeController device families such as Bluetooth, PC agent and Home-screen containers may use built-in pages rather than arbitrary declarative controls unless/until a renderer is exposed for them. Never assume a renderer supports a field merely because the JSON model contains it.

## 8. Sections

`sections` is an array of objects:

| Property | Type | Meaning |
|---|---|---|
| `title` | string/null | Section title. |
| `subtitle` | string/null | Supporting text. |
| `backgroundColor` | color/null | Optional section background override. |
| `controls` | control[] | Controls rendered in the section. |

Sections are the straightforward v1-compatible declarative structure. V2 `groups` provide more advanced nesting, filtering and child-item layouts.

## 9. Groups — complete property reference

A group may contain controls and nested groups.

| Property | Type/default | Meaning |
|---|---|---|
| `id` | string | Stable group ID. |
| `name` | string/null | Visible/logical group name. |
| `order` | int / 0 | Ordering value. |
| `columnSpan` | int / 1 | Grid columns occupied. |
| `rowSpan` | int / 1 | Grid rows occupied. |
| `width` | int / 1 | Logical width. |
| `height` | int / 1 | Logical height. |
| `type` | string / `normal` | `normal`, `child-items`, `filter`. |
| `childItemsSource` | string | Runtime child collection source. |
| `childItemsColumns` | int / 2 | Columns used for child items. |
| `filterScope` | string | Scope/target of filter. |
| `filterProperty` | string | Child/property field to filter. |
| `filterMode` | string / `in` | Comparison/composition mode. |
| `filterValues` | string[] | Explicit filter values. |
| `filterAutoValues` | bool | Derive selectable values from child items. |
| `filterAutoItemMargin` | number / 3 | Shared margin for generated filter items. |
| `filterAutoItemCornerRadius` | int / 8 | Radius for generated filter items. |
| `filterAutoItemContent` | string / `text` | Generated item content presentation, e.g. text/image where supported. |
| `shape` | string / `rounded` | Group shape. |
| `borderColor` | color/null | Border override. |
| `borderWidth` | number / 1 | Border width. |
| `backgroundMode` | string / `inherit` | Inherit/solid/image/etc. as supported by renderer. |
| `backgroundColor` | color/null | Primary group background. |
| `backgroundColor2` | color/null | Secondary group background. |
| `backgroundImage` | string/null | Group background asset. |
| `backgroundImageAspect` | string / `fill` | Asset fitting behavior. |
| `cornerRadius` | int / 14 | Group radius. |
| `overlayKey` | string/null | Runtime state/property key used for overlay behavior. |
| `overlayState` | string/null | State value associated with overlay. |
| `controls` | control[] | Direct controls. |
| `groups` | group[] | Nested groups. |

V2 filter modes defined by the schema: `in`, `notIn`, `equals`, `notEquals`, `contains`, `notContains`, `greaterThan`, `greaterOrEqual`, `lessThan`, `lessOrEqual`, `and`, `or`.

## 10. Controls — complete runtime property reference

Supported control `type` values currently declared by v2 are:

`label`, `multiline-label`, `edittext`, `button`, `list`, `checkbox`, `filter-toggle`, `on-off`, `link`, `tile`, `toggle`, `stepper`, `slider`, `picker`.

Control properties:

| Property | Type/default | Meaning |
|---|---|---|
| `id` | string | Stable control ID. |
| `order` | int / 0 | Rendering order. |
| `type` | string / `button` | Control kind. |
| `label` | string | Caption/label. |
| `text` | string | Main text. |
| `command` | string | Device command invoked by the control. |
| `value` | any/null | Command/control value. |
| `icon` | string/null | Icon/asset reference where renderer supports it. |
| `shape` | string/null | Visual shape override. |
| `columnSpan` | int / 1 | Grid column span. |
| `row` | int / 0 | Explicit row. |
| `column` | int / 0 | Explicit column. |
| `verticalAlign` | string / `center` | Vertical alignment. |
| `sizeXPercent` | number / 100 | Relative horizontal size. |
| `sizeYPercent` | number / 100 | Relative vertical size. |
| `minimum` | number/null | Minimum for numeric controls. |
| `maximum` | number/null | Maximum for numeric controls. |
| `step` | number/null | Numeric increment. |
| `stateField` | string/null | Device state/property field bound to control. |
| `options` | string[] | Picker/list/cycle options. |
| `backgroundColor` | color/null | Control background override. |
| `backgroundImage` | string/null | Control background asset. |
| `textColor` | color/null | Text override. |
| `borderColor` | color/null | Border override. |
| `borderWidth` | number / 1 | Border width. |
| `height` | number/null | Explicit height. |
| `width` | number/null | Explicit width. |
| `fontFamily` | string | Font family; empty means application default. |
| `fontSize` | number/null | Text size. |
| `fontAttribute` | string / `normal` | Font attribute. |
| `lines` | int / 1 | Text line count. |
| `iconSize` | number/null | Icon size. |
| `iconOnly` | bool | Hide label and present icon-only behavior where supported. |
| `linkUrl` | string/null | URL for link controls. |
| `stateKey` | string/null | Template-local state key. |
| `setState` | string/null | State assigned when activated. |
| `cycleStates` | string[] | States cycled by the control. |
| `group` | group/null | Embedded group. |
| `filterId` | string/null | Filter control/group association. |
| `filterValue` | string/null | Value selected/applied by a filter control. |
| `filterMode` | string | Filter operation/context. |
| `hideText` | bool | Hide text while retaining image/control behavior. |
| `uncheckedImage` | string/null | Image for unchecked/off state. |
| `checkedImage` | string/null | Image for checked/on state. |

### Recommended control usage

- `button`: stateless command/action.
- `on-off` / `toggle`: binary state + command where the driver exposes it.
- `slider`: continuous numeric property such as level/brightness/volume/temperature when supported.
- `stepper`: discrete numeric increments.
- `picker`: select from known options/modes.
- `checkbox`: boolean selection/state.
- `label`: one-line display.
- `multiline-label`: longer status/info.
- `edittext`: text input.
- `link`: open `linkUrl`.
- `tile`: card/tile-like action or state presentation.
- `filter-toggle`: controls a v2 filter using `filterId`/`filterValue`.
- `list`: renderer-dependent list presentation.

A control does not create a capability. `command`, `stateField` and values must match capabilities supplied by the device driver/integration.

## 11. Dynamic item style — complete property reference

`itemDefaults` and entries in `itemStyles` use the same object:

| Property | Type | Meaning |
|---|---|---|
| `columns` | int? | Inner item column count. |
| `columnSpan` | int? | Item column span. |
| `rowSpan` | int? | Item row span. |
| `displayMode` | string? | Renderer-specific presentation mode. |
| `shape` | string? | Item shape. |
| `backgroundColor` | color? | Background. |
| `textColor` | color? | Main text. |
| `mutedTextColor` | color? | Secondary text. |
| `borderColor` | color? | Border. |
| `accentColor` | color? | Active/accent. |
| `cornerRadius` | int? | Radius. |
| `height` | number? | Height. |
| `width` | number? | Width. |
| `fontSize` | number? | Main font size. |
| `iconSize` | number? | Main icon size. |
| `stateIconSize` | number? | State icon size. |
| `stateLabelFontSize` | number? | State label size. |
| `stateValueFontSize` | number? | State value size. |
| `stateButtonFontSize` | number? | State action button size. |
| `showIcon` | bool? | Show/hide icon. |
| `showName` | bool? | Show/hide name. |
| `showType` | bool? | Show/hide type. |
| `showState` | bool? | Show/hide state. |

These are especially relevant to Hubitat and Hue child-item rendering and other dynamic/discovered item renderers.

## 12. Integration child presentations

`integrationChildPresentations` maps a child device/category key to:

```json
{
  "pinnedProperties": ["temperature", "battery"],
  "pinnedCommands": ["on", "off"],
  "pinnedSliders": ["level"]
}
```

Properties:

- `pinnedProperties`: state/property values shown prominently on the integration parent/child card.
- `pinnedCommands`: command buttons shown prominently.
- `pinnedSliders`: numeric controls shown prominently.

This is intended for integrations such as Hubitat where child devices expose varying capabilities. The actual property/command names must come from the integration/device; do not fabricate them.

## 13. Initial and local UI state

`initialStates` is a string-to-string dictionary. Controls can interact with local UI state using:

- `stateKey`
- `setState`
- `cycleStates`

Use this for presentation state that belongs to the template. Do not use it as a substitute for a real device state unless the renderer explicitly synchronizes the state with the device.

## 14. Images and backgrounds

Use the central DeviceDB image catalog (`images/catalog.json`). Categories include device types, actions, properties, states, branding/integrations and backgrounds.

Do not invent image paths. Prefer catalog-backed semantic assets. Image naming and sizing conventions are documented under `images/README.md` and `images/REQUIRED_IMAGES.md`.

Common image-bearing template fields:

- top level: `backgroundImage`
- group: `backgroundImage`
- control: `icon`, `backgroundImage`, `uncheckedImage`, `checkedImage`

Image choice should be independent from localization. Theme colors should normally remain independent from semantic icon identity.

## 15. Device/use-location guidance

### Television

Typical capabilities: power, digits, navigation, volume, channel, source/input, menu/home/back, media transport. Infrared and Wi-Fi implementations can expose different command names; only use commands present in the target driver/profile. TV templates benefit from grouped navigation and media controls.

### Air conditioner

Typical capabilities may include power, target temperature, mode, fan, swing and model-specific functions. Prefer state-bound controls (`slider`, `picker`, `toggle`) only where the underlying driver has real state/capability support. Infrared A/C may be stateful at the protocol layer but not necessarily provide feedback from the physical unit.

### Fan

Typical controls may include power, speed, oscillation, timer and model-specific modes. Never assume all fans expose all of them.

### Hubitat

Use dynamic child presentation. `itemDefaults`, `itemStyles`, child-item groups, filters and `integrationChildPresentations` are especially useful. Child capabilities may include switches, temperatures, humidity, battery, contact/motion state, dimmers and commands, but the actual Maker API data is authoritative.

### Philips Hue

Use dynamic child presentation. Lights commonly expose on/off, brightness and potentially color/temperature depending on the resource. Do not add controls unsupported by the discovered Hue resource.

### Dashboard

The dashboard renderer is primarily a WebView/runtime screen. Do not model arbitrary dashboard web content as declarative device controls. Single/multi-dashboard URL/name/order are device/runtime data.

### Bluetooth

Bluetooth device capabilities vary greatly. A generic template cannot assume GATT characteristics or commands. HID remote behavior is a specialized built-in runtime feature. Generate declarative Bluetooth UI only when a concrete Bluetooth driver exposes stable commands/properties.

### PC agent/computer

PC remote/control capabilities belong to the PC agent runtime/driver. A template may present exposed commands/properties, but must not invent remote-desktop or input capabilities solely through JSON.

### Home-screen container

This is navigation/container behavior, not a normal appliance. It should use HomeController navigation/card semantics rather than appliance command assumptions.

## 16. Complete declarative v2 skeleton

```json
{
  "$schema": "../schemas/device-ui-template-v2.schema.json",
  "schemaVersion": 2,
  "id": "example-device-default",
  "name": "Example Device",
  "deviceTypeId": "general",
  "connections": ["wifi"],
  "renderer": "declarative",
  "access": "free",
  "columns": 3,
  "useFullWidth": true,
  "horizontalSpacing": 10,
  "verticalSpacing": 10,
  "screenMarginLeft": 12,
  "screenMarginTop": 12,
  "screenMarginRight": 12,
  "screenMarginBottom": 12,
  "backgroundMode": "solid",
  "backgroundImageAspect": "fill",
  "buttonCornerRadius": 8,
  "sectionCornerRadius": 14,
  "buttonHeight": 54,
  "buttonFontSize": 13,
  "iconFontSize": 24,
  "itemDefaults": {},
  "itemStyles": {},
  "initialStates": {},
  "integrationChildPresentations": {},
  "sections": [],
  "groups": [
    {
      "id": "main",
      "name": "Main",
      "order": 0,
      "type": "normal",
      "columnSpan": 3,
      "controls": [
        {
          "id": "power",
          "order": 0,
          "type": "button",
          "label": "Power",
          "command": "power",
          "columnSpan": 1
        }
      ],
      "groups": []
    }
  ]
}
```

Replace `deviceTypeId`, connection, commands and state bindings with real values supported by the target device.

## 17. AI pre-publication checklist

Before an AI-generated theme/template is accepted:

- JSON parses successfully.
- `$schema` points to the intended local schema.
- schema version is correct.
- ID is stable and does not collide unintentionally.
- device type exists.
- connection is supported by the device type/driver.
- renderer is valid and appropriate.
- every command/state/property is supported by the actual target.
- every referenced image exists in the catalog/repository.
- visible strings have appropriate localization strategy.
- template does not hard-code theme colors unnecessarily.
- controls have sensible mobile dimensions.
- filters reference real child properties/values.
- integration pinning references real child capabilities.
- premium/free access is intentional.
- language variants retain one logical template identity.
- DeviceDB validators pass.

## 18. Important schema/runtime distinction

The JSON Schema is the machine validation contract, while the C# runtime model can temporarily contain fields that are not yet constrained tightly by the schema. For AI generation, use the intersection of:

1. this documented runtime contract;
2. the current machine-readable schema;
3. the capabilities of the selected renderer/driver.

`additionalProperties: true` in a schema is **not permission to invent new HomeController features**. Unknown fields may be ignored by the runtime. Only fields documented here or in a newer canonical schema/document should be generated.

When a new runtime property is added, update this document and the machine-readable schema in the same change so AI-generated templates remain deterministic and maintainable.
