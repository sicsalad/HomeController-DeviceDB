# Device UI theme color references

Device UI template schema v1 supports both application-theme color references and literal colors. The canonical reference syntax is `$ResourceName`.

Examples:

```json
{
  "backgroundColor": "$PageBackground",
  "foregroundColor": "$TextPrimary",
  "surfaceColor": "$Surface",
  "accentColor": "$Accent",
  "buttonColor": "$ButtonBackground",
  "buttonTextColor": "$ButtonText",
  "borderColor": "$CardBorder"
}
```

A literal color can be used instead whenever a control intentionally has its own color:

```json
{
  "type": "button",
  "label": "Power",
  "command": "Power",
  "backgroundColor": "$ButtonBackground",
  "textColor": "$ButtonText"
}
```

or:

```json
{
  "type": "button",
  "label": "RED",
  "command": "Red",
  "backgroundColor": "#B3261E",
  "textColor": "#FFFFFF"
}
```

## Where references are supported

Every color-valued field in `device-ui-template-v1.schema.json` accepts either `$ThemeResource` or a literal `#RRGGBB` / `#AARRGGBB` value. This includes:

- template-level `backgroundColor`, `foregroundColor`, `mutedTextColor`, `surfaceColor`, `accentColor`, `buttonColor`, `buttonTextColor`, `borderColor`;
- `itemDefaults` and every `itemStyles[type]` `backgroundColor`, `textColor`, `mutedTextColor`, `borderColor`, `accentColor`;
- section `backgroundColor`;
- control `backgroundColor`, `textColor`, `borderColor`.

## Recommended application-theme resources

Use the stable semantic resources documented in `THEMES_AND_UI_TEMPLATES.md`: `PageBackground`, `Surface`, `SurfaceVariant`, `TextPrimary`, `TextSecondary`, `TextMuted`, `Accent`, `OnAccent`, `NavigationBackground`, `NavigationText`, `CardBackground`, `CardBorder`, `InputBackground`, `InputText`, `PlaceholderText`, `ButtonBackground`, `ButtonText`, `SecondaryButtonBackground`, `SecondaryButtonText`, `DisabledBackground`, `DisabledText`, `Separator`, `Danger`, `OnDanger`, `Success`, and `OnSuccess`. Core palette entries such as `Primary`, `PrimaryDark`, `PrimaryLight`, `Secondary`, and `Tertiary` can also be referenced when their palette meaning is intentional.

## Resolution and override rules

A reference is resolved against the currently active application theme when the device page is created. Templates are resolved on a fresh per-page copy, so changing Default / Blue Eye / Red Eye does not permanently replace `$...` references in the cached catalog.

For a declarative control, the most specific value wins: control value → section/template defaults → active application-theme fallback. For Hue and Hubitat discovered items, the order is type-specific `itemStyles[type]` → `itemDefaults` → template-level styling → active application-theme semantic fallback.

Omitting a template-level color is equivalent to following the appropriate semantic application-theme role. Therefore layout-only templates usually do not need to repeat all color references.

The runtime also accepts `@Accent` and `theme:Accent` for compatibility, but new DeviceDB files should use `$Accent`.

## Important separation

Default / Blue Eye / Red Eye are **application themes**. Default / Modern / Round / Compact / Grid are **Device UI templates**. A Device UI template should normally inherit application-theme colors and describe layout/shape. Use literal colors only where the color is part of the control's meaning (for example TV red/green/yellow/blue function keys) or where the template intentionally overrides the application theme.
