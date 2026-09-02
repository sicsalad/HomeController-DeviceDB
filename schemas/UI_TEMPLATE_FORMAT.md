# UI template format and localization

## Base template

The language-neutral `ui-templates/<id>.json` file is the complete source of truth. A property that is not needed does **not** have to be present. Missing optional properties are supplied by the HomeController model defaults. The schema documents the available properties even when a particular template omits them.

The identifying fields `schemaVersion`, `id`, `name`, `deviceTypeId` and `connections` remain required. `renderer` is optional; when omitted the runtime default is `declarative`. Group/control properties are optional unless the selected control behavior logically needs them (for example a command button needs `command`).

### Available template properties

`renderer`, `columns`, `useFullWidth`, `horizontalSpacing`, `verticalSpacing`, `backgroundColor`, `backgroundColor2`, `backgroundMode`, `backgroundImage`, `backgroundImageAspect`, `foregroundColor`, `mutedTextColor`, `surfaceColor`, `accentColor`, `buttonColor`, `buttonTextColor`, `borderColor`, `buttonCornerRadius`, `sectionCornerRadius`, `buttonHeight`, `buttonFontSize`, `iconFontSize`, `itemDefaults`, `itemStyles`, `sections`, `groups`, `initialStates`. Legacy theme-switcher properties remain supported for compatibility.

### Group properties

`id`, `name`, `order`, `type`, `columnSpan`, `rowSpan`, legacy `width`/`height`, `childItemsSource`, `childItemsColumns`, `filterScope`, `filterProperty`, `filterMode`, `filterValues`, `filterAutoValues`, `shape`, `borderColor`, `borderWidth`, `backgroundMode`, `backgroundColor`, `backgroundColor2`, `backgroundImage`, `backgroundImageAspect`, `cornerRadius`, `overlayKey`, `overlayState`, `controls`, `groups`.

### Control properties

`id`, `order`, `type`, `label`, `text`, `command`, `value`, `icon`, `shape`, `row`, `column`, `columnSpan`, `verticalAlign`, `sizeXPercent`, `sizeYPercent`, `minimum`, `maximum`, `step`, `stateField`, `options`, `backgroundColor`, `backgroundImage`, `textColor`, `borderColor`, `borderWidth`, `height`, `width`, `fontFamily`, `fontSize`, `fontAttribute`, `lines`, `iconSize`, `iconOnly`, `linkUrl`, `stateKey`, `setState`, `cycleStates`, `filterId`, `filterValue`, `filterMode`, `hideText`, `uncheckedImage`, `checkedImage`.

## Language files

A localized file such as `wifi-tv-default-hu.json` is **not another template**. It is only a translation overlay for `wifi-tv-default.json`. It must contain no layout, color, command, URL, filter or other behavioral data. The filename selects the language.

The file is a flat JSON object. Each key is a code/path identifying a text property in the base template and each value is the translated text. Example:

```json
{
  "name": "Modern TV távirányító",
  "sections.0.subtitle": "Gyorsvezérlők",
  "sections.1.title": "NAVIGÁCIÓ",
  "sections.1.controls.0.label": "HANGERŐ +"
}
```

Supported translatable text is currently template `name`/`themeSwitcherText`, section `title`/`subtitle`, group `name`, control `label`/`text`, and string `options` entries. Unlisted strings fall back to the base template.

The runtime always loads the language-neutral base first, then overlays the current language file when it exists. If the language file is missing or contains a bad key, the base text remains. This keeps all rendering and behavior in one place and prevents language variants from drifting apart.

The language-file schema is `schemas/ui-template-localization-v1.schema.json`.
