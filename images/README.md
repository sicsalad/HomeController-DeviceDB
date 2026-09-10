# HomeController image assets

All non-app-branding UI/device artwork belongs in this DeviceDB repository. `images/index.json` is the single source of truth for image identity, target dimensions and semantic mapping.

## Folder layout

- `images/` — base image style
- `images_modern/` — optional modern image style; it uses the same relative file names as `images/`
- `images/device-types/` — device category images
- `images/actions/` — reusable UI action images
- `images/states/` — state images
- `images/controls/` — declarative UI-template images
- `images/backgrounds/` — UI-template backgrounds
- `images/branding/` — integration/vendor artwork where licensing permits
- `images/index.json` — master image index

Additional styles follow the `images_<style>` naming convention. A style may override only part of the base set; missing files inherit the base image during HomeController's image synchronization.

## Index format

Each `images` entry starts with the stable `id` followed immediately by the target `size`, for example:

```json
{"id":"device-television","size":"64x64","path":"device-types/device_television.svg","deviceTypes":["television"],"category":"device","tags":["tv","screen"]}
```

`size` is the required output size used by HomeController when materializing the DeviceDB image locally. It describes the intended normalized asset size, not whatever width/height happens to be present in the source file.

## Naming convention

Use lowercase snake_case and a semantic prefix:

- device type: `device_<type>.svg`
- action: `action_<action>.svg`
- state: `state_<subject>_<state>.svg`
- control: `control_<name>.svg`
- background: `background_<name>.<svg|png|webp>`
- branding: `brand_<vendor>[_<variant>].<svg|png|webp>`

Names must stay stable between image styles. `images/device-types/device_television.svg` and `images_modern/device-types/device_television.svg` represent the same semantic image in different styles.

## Size and rendering rules

The current icon schema uses `64x64` targets. Prefer SVG with a matching `64 x 64` viewBox and keep important artwork inside roughly a 56 x 56 safe area. HomeController normalizes the local materialized image to the `size` from `index.json` before MAUI packages/rasterizes it.

Typical display sizes remain independent of source resolution: compact/action 20–24 dp, list/property 24–32 dp, Home/device card 36–48+ dp, picker 64–80 dp, hero 48–96 dp.

## Style packs

Image style is independent from the color theme, but it is selected under Themes in HomeController. If only `images/` exists, no image-style selector is shown. As soon as a second root folder such as `images_modern/` exists, HomeController exposes the available image styles.

The base `images/index.json` applies to every style pack. Do not create a second index inside `images_modern`; all packs must obey the same IDs, relative paths and target sizes.
