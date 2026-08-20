# HomeController Device Database

`HomeController-DeviceDB` is the public, app-independent registry used by HomeController.

The database is deliberately broader than infrared. A device may eventually expose IR, LAN/Wi-Fi, Bluetooth, Matter, Zigbee, MQTT or other control methods. The v1 runtime starts with infrared.

## Structure

- `database.json` – compact Type → Manufacturer → Model browse index consumed by the app.
- `curated-database.json` – manually reviewed entries that always override generated imports.
- `devices/` – curated model definitions.
- `generated/` – automatically normalized community captures.
- `protocols/` – reusable protocol metadata.
- `schemas/` – schema documentation.
- `tools/` – import/normalization tools.

## Updating the open database

A GitHub Actions workflow imports useful TV and A/C captures from `Lucaslhm/Flipper-IRDB`, normalizes only protocols the HomeController runtime can actually transmit, rejects very sparse captures, merges the result with curated entries, and publishes the generated model JSON files plus a new `database.json`.

Because the app reads this repository at runtime, a new model that uses an already supported protocol can become available without publishing a new APK.

## Runtime protocol coverage in HomeController v1

Stateless/raw IR: raw patterns, Samsung32, NEC, NECext, NEC42, NEC42ext, RC5, RC5X, RC6, SIRC, SIRC15, SIRC20, Kaseikyo and RCA.

Stateful A/C: GreeV1 and WhirlpoolAc. Stateful families are curated more carefully because an A/C usually transmits its complete state rather than an independent code for each button.

## Quality levels

- `hardware-verified-in-HomeController` – tested against the physical device during HomeController development.
- `source-tested` – upstream capture explicitly says it was tested on the named model.
- `source-model-labelled` – upstream capture is directly labelled with the model.
- `community-capture` – automatically imported, usable capture with enough controls, but not independently verified by HomeController.

Generated entries retain their original source path. Flipper-IRDB currently publishes its database under CC0-1.0; source provenance is kept in each generated definition.
