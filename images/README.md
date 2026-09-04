# HomeController runtime image assets

All non-app-branding UI/device artwork belongs in this DeviceDB repository and is downloaded at runtime by HomeController. Device/action images must not be compiled into the application package.

## Folder layout

- `images/device-types/` — device category icons/images
- `images/actions/` — reusable UI action icons
- `images/states/` — state images (on/off/open/closed/etc.)
- `images/controls/` — images used by declarative UI-template controls
- `images/backgrounds/` — UI-template backgrounds
- `images/branding/` — integration/vendor artwork where licensing permits
- `images/catalog.json` — semantic key -> relative asset path mapping

Only the application icon and splash screen are application resources; those must exist before DeviceDB/network access is available.

## Naming convention

Use lowercase snake_case and a semantic prefix:

- device type: `device_<type>.svg`
- action: `action_<action>.svg`
- state: `state_<subject>_<state>.svg`
- control: `control_<name>.svg`
- background: `background_<name>.<svg|png|webp>`
- branding: `brand_<vendor>[_<variant>].<svg|png|webp>`

Names must be stable. Templates and catalogs should refer to semantic keys or repository-relative paths, never a device-local file path.

## Master size and display sizes

Prefer SVG for icons. Author SVGs with a `64 x 64` viewBox and keep important artwork inside roughly a 56 x 56 safe area. The app scales them at runtime.

Typical display sizes:

- compact inline/action icon: 20–24 dp
- list/property icon: 24–32 dp
- Home/device card: 36–48 dp
- device-type picker tile: 64–80 dp
- widget/device hero image: 48–96 dp

PNG/WebP should only be used for photographic/complex images. Provide at least 2x the largest intended logical display size.

## Runtime rules

`images/catalog.json` is the central semantic catalog. HomeController resolves the catalog entry to `https://raw.githubusercontent.com/sicsalad/HomeController-DeviceDB/main/images/...` and lets the MAUI image loader download/cache it at runtime. Updating an image in DeviceDB therefore does not require rebuilding the app.

If an image cannot be downloaded, the UI must remain functional and may fall back to a glyph/text placeholder. Image availability must never block device control.

## Themes, UI templates and localization

Images are content, not theme colors. Themes control semantic colors and general appearance. UI templates decide where an image is shown and its logical size/aspect. Localization changes text only; image keys/paths remain language-independent unless a genuinely language-specific illustration is required.

A UI template should prefer semantic image IDs/paths from this repository. Do not embed base64 images in templates and do not add template-specific artwork to the application project.
