# REQUIRED_IMAGES.md

This file is the **source-of-truth checklist for artwork required by HomeController**.

It answers four questions:

1. What semantic image IDs/file names should exist?
2. What is each image used for?
3. What format/source size is expected?
4. Which assets already exist in `images/` and which are still missing?

The list is derived from the current `device-types.json`, HomeController command model, integrations, Home/Home-screen UI and the Bluetooth/open-database direction (BTHome/Theengs/standard BLE sensor capabilities).

> **Important:** application code and templates should reference semantic IDs / DeviceDB paths. The artwork is stored in **HomeController-DeviceDB** and downloaded/cache-resolved at runtime. Normal UI/device artwork must not be compiled into the HomeController APK.

---

## 1. Global image rules

### Preferred format

- **Icons / device silhouettes / actions / states:** SVG.
- **SVG master canvas:** `viewBox="0 0 64 64"`.
- Do **not** create separate 24/32/48/64 px copies of an SVG.
- The UI scales the same vector asset to the required logical size.
- **Photos / textured backgrounds:** PNG/JPG/WebP only when vector artwork is inappropriate.

### Recommended rendered size by use

| Use | Approx. rendered size |
|---|---:|
| Small property/status icon | 18–24 dp |
| Toolbar/action icon | 22–28 dp |
| Compact list / picker | 28–36 dp |
| Home device card | 40–48 dp |
| Device-add tile | 56–72 dp |
| Large device hero / remote header | 72–96 dp |
| Android Home widget | 32–48 dp |
| Full-screen/background raster | minimum ~1440 px on short side |

### Safe SVG artwork area

Although the SVG viewBox is 64×64, keep the important shape roughly inside **4..60** on both axes so strokes are not clipped. Prefer a visually balanced icon with about 6–10% breathing room.

### Naming convention

All names are lower-case ASCII `snake_case`.

- Device: `images/device-types/device_<type>.svg`
- Action: `images/actions/action_<action>.svg`
- State: `images/states/state_<state>.svg`
- Property/capability: `images/properties/property_<property>.svg`
- Control: `images/controls/control_<control>.svg`
- Background: `images/backgrounds/background_<purpose>_<variant>.<svg|png|jpg|webp>`
- Brand/integration: `images/branding/brand_<provider>.<svg|png>`

Do not put language codes or theme names in normal semantic image names.

Status legend:

- ✅ = currently present in DeviceDB
- 🟡 = generic/fallback exists but dedicated image is still desirable
- ❌ = dedicated image still needed
- ◻️ = planned/open-database expansion; not required for the current IR catalog, but should be prepared

---

# 2. Device type images — current HomeController/DeviceDB catalog

Every selectable/known `device-types.json` type should ultimately have a dedicated image. Unknown types always fall back to `device_general.svg`.

| Status | Device type id | Required file | Main use | SVG master | Typical Home size |
|---|---|---|---|---:|---:|
| ✅ | `general` | `device-types/device_general.svg` | Unknown / fallback device | 64×64 | 40–48 dp |
| ✅ | `air-conditioner` | `device-types/device_air_conditioner.svg` | Air conditioner | 64×64 | 40–48 dp |
| ✅ | `air-purifier` | `device-types/device_air_purifier.svg` | Air purifier | 64×64 | 40–48 dp |
| ✅ | `av-receiver` | `device-types/device_av_receiver.svg` | AV receiver / amplifier | 64×64 | 40–48 dp |
| ❌ | `bidet` | `device-types/device_bidet.svg` | Smart/IR bidet | 64×64 | 40–48 dp |
| ❌ | `blu-ray-player` | `device-types/device_blu_ray_player.svg` | Blu-ray player | 64×64 | 40–48 dp |
| ❌ | `cameras` | `device-types/device_camera.svg` | Camera | 64×64 | 40–48 dp |
| ❌ | `car-multimedia` | `device-types/device_car_multimedia.svg` | Car multimedia unit | 64×64 | 40–48 dp |
| ❌ | `cctv` | `device-types/device_cctv.svg` | CCTV / security video | 64×64 | 40–48 dp |
| ❌ | `cd-player` | `device-types/device_cd_player.svg` | CD player | 64×64 | 40–48 dp |
| ❌ | `ceiling-lift` | `device-types/device_ceiling_lift.svg` | Ceiling lift | 64×64 | 40–48 dp |
| ❌ | `clocks` | `device-types/device_clock.svg` | Clock / timer device | 64×64 | 40–48 dp |
| ✅ | `computers` | `device-types/device_computer.svg` | Computer / PC | 64×64 | 40–48 dp |
| 🟡 | `converted` | `device-types/device_general.svg` | Imported/converted IR data | 64×64 | 40–48 dp |
| ❌ | `converters` | `device-types/device_converter.svg` | Signal/media converter | 64×64 | 40–48 dp |
| ❌ | `digital-picture-frame` | `device-types/device_digital_picture_frame.svg` | Digital picture frame | 64×64 | 40–48 dp |
| ❌ | `digital-sign` | `device-types/device_digital_sign.svg` | Digital signage display | 64×64 | 40–48 dp |
| ❌ | `dust-collector` | `device-types/device_dust_collector.svg` | Dust collector | 64×64 | 40–48 dp |
| ❌ | `dvb-t` | `device-types/device_dvb_t.svg` | DVB-T receiver | 64×64 | 40–48 dp |
| ❌ | `dvd-player` | `device-types/device_dvd_player.svg` | DVD player | 64×64 | 40–48 dp |
| ✅ | `fan` | `device-types/device_fan.svg` | Fan | 64×64 | 40–48 dp |
| ❌ | `fireplaces` | `device-types/device_fireplace.svg` | Electric fireplace | 64×64 | 40–48 dp |
| ❌ | `consoles` | `device-types/device_game_console.svg` | Game console | 64×64 | 40–48 dp |
| ❌ | `head-unit` | `device-types/device_head_unit.svg` | Car head unit | 64×64 | 40–48 dp |
| ❌ | `heater` | `device-types/device_heater.svg` | Heater | 64×64 | 40–48 dp |
| ✅ | `hubitat` | `device-types/device_hubitat.svg` | Hubitat integration container | 64×64 | 40–48 dp |
| ❌ | `humidifier` | `device-types/device_humidifier.svg` | Humidifier | 64×64 | 40–48 dp |
| ❌ | `ir-transceiver` | `device-types/device_ir_transceiver.svg` | IR bridge/transceiver | 64×64 | 40–48 dp |
| ❌ | `kvm` | `device-types/device_kvm.svg` | KVM switch | 64×64 | 40–48 dp |
| ❌ | `laserdisc` | `device-types/device_laserdisc.svg` | LaserDisc player | 64×64 | 40–48 dp |
| ✅ | `light` | `device-types/device_light.svg` | Lamp / LED lighting | 64×64 | 40–48 dp |
| ❌ | `minidisc` | `device-types/device_minidisc.svg` | MiniDisc player | 64×64 | 40–48 dp |
| ❌ | `monitors` | `device-types/device_monitor.svg` | Monitor/display | 64×64 | 40–48 dp |
| ❌ | `multimedia` | `device-types/device_multimedia.svg` | Generic multimedia device | 64×64 | 40–48 dp |
| 🟡 | `miscellaneous` | `device-types/device_general.svg` | Other IR device | 64×64 | 40–48 dp |
| ✅ | `philips-hue` | `device-types/device_hue.svg` | Philips Hue integration | 64×64 | 40–48 dp |
| ❌ | `projector` | `device-types/device_projector.svg` | Projector | 64×64 | 40–48 dp |
| ❌ | `set-top-box` | `device-types/device_set_top_box.svg` | Cable/IPTV/set-top box | 64×64 | 40–48 dp |
| ❌ | `soundbar` | `device-types/device_soundbar.svg` | Soundbar | 64×64 | 40–48 dp |
| ❌ | `speakers` | `device-types/device_speaker.svg` | Speaker/audio device | 64×64 | 40–48 dp |
| ❌ | `streaming-device` | `device-types/device_streaming_device.svg` | Streaming box/stick | 64×64 | 40–48 dp |
| ✅ | `television` | `device-types/device_television.svg` | Television | 64×64 | 40–48 dp |
| ❌ | `touchscreen-displays` | `device-types/device_touchscreen_display.svg` | Touch display | 64×64 | 40–48 dp |
| ❌ | `toys` | `device-types/device_toy.svg` | IR toy | 64×64 | 40–48 dp |
| ❌ | `tv-tuner` | `device-types/device_tv_tuner.svg` | TV tuner | 64×64 | 40–48 dp |
| ❌ | `universal-tv-remotes` | `device-types/device_universal_remote.svg` | Universal TV remote | 64×64 | 40–48 dp |
| ❌ | `vacuum-cleaners` | `device-types/device_vacuum_cleaner.svg` | Vacuum cleaner | 64×64 | 40–48 dp |
| ❌ | `vcr` | `device-types/device_vcr.svg` | VCR | 64×64 | 40–48 dp |
| ❌ | `videoconferencing` | `device-types/device_videoconferencing.svg` | Video conferencing | 64×64 | 40–48 dp |
| ❌ | `whiteboards` | `device-types/device_whiteboard.svg` | Interactive whiteboard | 64×64 | 40–48 dp |
| ❌ | `window-cleaners` | `device-types/device_window_cleaner.svg` | Window cleaning robot/device | 64×64 | 40–48 dp |

## HomeController-specific device/container images

These are not all IR database device types but are required by the application UI.

| Status | Semantic id | Required file | Use |
|---|---|---|---|
| ✅ | `home-screen` | `device-types/device_home_screen.svg` | Nested Home/sub-Home block |
| ✅ | `folder` | `device-types/device_folder.svg` | Local folder/file device |
| ✅ | `bluetooth` | `device-types/device_bluetooth.svg` | Generic Bluetooth/BLE device |
| ✅ | `dashboard` | `device-types/device_dashboard.svg` | Dashboard device |
| ✅ | `switch` / `plug` / `outlet` | `device-types/device_switch.svg` | Smart switch/outlet |
| ✅ | `temperature` / `thermometer` | `device-types/device_temperature.svg` | Temperature sensor |
| ✅ | `sensor` | `device-types/device_sensor.svg` | Generic sensor fallback |

---

# 3. Open Bluetooth database / sensor expansion

The Bluetooth architecture can receive device data from standard GATT, BTHome and Theengs-style advertisement decoders. These sources often describe **capabilities/properties**, not only a single product type. For that reason HomeController needs both device icons and property icons.

These are planned semantic device images so a newly recognized broadcast device does not have to use the generic controller icon.

| Status | Semantic type | Required file | Typical sources |
|---|---|---|---|
| ◻️ | humidity sensor | `device-types/device_humidity_sensor.svg` | BTHome, Theengs, GATT |
| ◻️ | temperature+humidity sensor | `device-types/device_climate_sensor.svg` | Xiaomi, Govee, Qingping, Inkbird, BTHome |
| ◻️ | contact sensor | `device-types/device_contact_sensor.svg` | BTHome, BLE door/window sensors |
| ◻️ | motion sensor | `device-types/device_motion_sensor.svg` | BTHome/PIR BLE |
| ◻️ | presence sensor | `device-types/device_presence_sensor.svg` | BLE presence devices |
| ◻️ | button/remote | `device-types/device_button.svg` | BTHome buttons, BLE remotes |
| ◻️ | leak/water sensor | `device-types/device_water_leak_sensor.svg` | BTHome/BLE sensors |
| ◻️ | CO2 sensor | `device-types/device_co2_sensor.svg` | Qingping/air-quality BLE/GATT |
| ◻️ | air quality sensor | `device-types/device_air_quality_sensor.svg` | PM/VOC/air quality BLE |
| ◻️ | scale | `device-types/device_scale.svg` | BLE body/kitchen scales |
| ◻️ | plant sensor | `device-types/device_plant_sensor.svg` | Xiaomi/Mi Flora-style BLE |
| ◻️ | beacon | `device-types/device_beacon.svg` | iBeacon/Eddystone/general beacon |
| ◻️ | tracker | `device-types/device_tracker.svg` | BLE trackers |
| ◻️ | lock | `device-types/device_lock.svg` | BLE smart locks |
| ◻️ | thermostat | `device-types/device_thermostat.svg` | BLE/GATT climate controllers |
| ◻️ | dehumidifier | `device-types/device_dehumidifier.svg` | BLE/Wi-Fi/IR climate devices |
| ◻️ | robot vacuum | `device-types/device_robot_vacuum.svg` | BLE/Wi-Fi integrations |

When an open database reports a model that HomeController cannot classify, use `device_sensor.svg` for sensor-like devices and `device_general.svg` otherwise until a semantic type is added.

---

# 4. Property / capability images

These are especially important for Hubitat, Hue, Bluetooth/BTHome/Theengs and future integrations because child cards can expose individual properties.

All use `64×64` SVG masters. Typical render size is **18–28 dp**.

| Status | Property | Required file | Meaning |
|---|---|---|---|
| ❌ | temperature | `properties/property_temperature.svg` | °C/°F temperature |
| ❌ | humidity | `properties/property_humidity.svg` | relative humidity |
| ❌ | battery | `properties/property_battery.svg` | battery level |
| ❌ | voltage | `properties/property_voltage.svg` | voltage |
| ❌ | current | `properties/property_current.svg` | electrical current |
| ❌ | power | `properties/property_power.svg` | instantaneous power |
| ❌ | energy | `properties/property_energy.svg` | accumulated energy |
| ❌ | illuminance | `properties/property_illuminance.svg` | lux/light level |
| ❌ | pressure | `properties/property_pressure.svg` | atmospheric pressure |
| ❌ | CO2 | `properties/property_co2.svg` | CO₂ ppm |
| ❌ | VOC | `properties/property_voc.svg` | VOC/air quality |
| ❌ | PM2.5 | `properties/property_pm25.svg` | particulate matter |
| ❌ | moisture | `properties/property_moisture.svg` | soil/material moisture |
| ❌ | signal | `properties/property_signal.svg` | RSSI/signal strength |
| ❌ | motion | `properties/property_motion.svg` | motion detected |
| ❌ | presence | `properties/property_presence.svg` | presence/occupancy |
| ❌ | contact | `properties/property_contact.svg` | open/closed contact |
| ❌ | water leak | `properties/property_water_leak.svg` | leak detection |
| ❌ | brightness | `properties/property_brightness.svg` | lamp/display brightness |
| ❌ | color temperature | `properties/property_color_temperature.svg` | warm/cool light |
| ❌ | color | `properties/property_color.svg` | RGB/HSV color |
| ❌ | speed | `properties/property_speed.svg` | fan/motor speed |
| ❌ | target temperature | `properties/property_target_temperature.svg` | thermostat setpoint |
| ❌ | mode | `properties/property_mode.svg` | current operating mode |
| ❌ | online | `properties/property_online.svg` | connectivity/availability |

---

# 5. Common action/control images

The canonical HomeController `RemoteCommand` model contains TV/media/navigation/climate actions. These should use shared semantic images instead of per-device copies.

All are **64×64 SVG** masters. Toolbar/remote buttons normally render them at **22–36 dp**.

## Core/navigation

| Status | Required file | Command/use |
|---|---|---|
| ✅ | `actions/action_settings.svg` | Settings |
| ✅ | `actions/action_add.svg` | Add |
| ✅ | `actions/action_theme.svg` | Theme/UI design |
| ✅ | `actions/action_back.svg` | Back |
| ✅ | `actions/action_delete.svg` | Delete/trash |
| ✅ | `actions/action_pin.svg` | Pin/unpin |
| ❌ | `actions/action_power.svg` | Power toggle |
| ❌ | `actions/action_power_on.svg` | Power on |
| ❌ | `actions/action_power_off.svg` | Power off |
| ❌ | `actions/action_home.svg` | Home |
| ❌ | `actions/action_menu.svg` | Menu |
| ❌ | `actions/action_up.svg` | Up |
| ❌ | `actions/action_down.svg` | Down |
| ❌ | `actions/action_left.svg` | Left |
| ❌ | `actions/action_right.svg` | Right |
| ❌ | `actions/action_ok.svg` | OK/Enter |
| ❌ | `actions/action_exit.svg` | Exit |
| ❌ | `actions/action_info.svg` | Information |
| ❌ | `actions/action_refresh.svg` | Refresh/reload |

## TV/media

| Status | Required file | Command/use |
|---|---|---|
| ❌ | `actions/action_source.svg` | Source/input |
| ❌ | `actions/action_volume_up.svg` | VolumeUp |
| ❌ | `actions/action_volume_down.svg` | VolumeDown |
| ❌ | `actions/action_mute.svg` | Mute |
| ❌ | `actions/action_channel_up.svg` | ChannelUp |
| ❌ | `actions/action_channel_down.svg` | ChannelDown |
| ❌ | `actions/action_previous_channel.svg` | PreviousChannel |
| ❌ | `actions/action_channel_list.svg` | ChannelList |
| ❌ | `actions/action_play.svg` | Play |
| ❌ | `actions/action_pause.svg` | Pause |
| ❌ | `actions/action_stop.svg` | Stop |
| ❌ | `actions/action_rewind.svg` | Rewind |
| ❌ | `actions/action_fast_forward.svg` | FastForward |
| ❌ | `actions/action_record.svg` | Record |
| ❌ | `actions/action_guide.svg` | Guide/EPG |
| ❌ | `actions/action_subtitle.svg` | Subtitle |
| ❌ | `actions/action_tools.svg` | Tools/options |
| ❌ | `actions/action_digit_0.svg` … `action_digit_9.svg` | Numeric remote keys; optional images, text buttons are acceptable |
| ❌ | `actions/action_red.svg` | Red function key |
| ❌ | `actions/action_green.svg` | Green function key |
| ❌ | `actions/action_yellow.svg` | Yellow function key |
| ❌ | `actions/action_blue.svg` | Blue function key |

## Climate/fan

| Status | Required file | Command/use |
|---|---|---|
| ❌ | `actions/action_temperature_up.svg` | TemperatureUp |
| ❌ | `actions/action_temperature_down.svg` | TemperatureDown |
| ❌ | `actions/action_mode.svg` | Mode |
| ❌ | `actions/action_mode_auto.svg` | ModeAuto |
| ❌ | `actions/action_mode_cool.svg` | ModeCool |
| ❌ | `actions/action_mode_heat.svg` | ModeHeat |
| ❌ | `actions/action_mode_dry.svg` | ModeDry |
| ❌ | `actions/action_mode_fan.svg` | ModeFan |
| ❌ | `actions/action_fan_speed.svg` | FanSpeed |
| ❌ | `actions/action_fan_speed_up.svg` | FanSpeedUp |
| ❌ | `actions/action_fan_speed_down.svg` | FanSpeedDown |
| ❌ | `actions/action_fan_auto.svg` | FanSpeedAuto |
| ❌ | `actions/action_swing.svg` | Swing |
| ❌ | `actions/action_swing_vertical.svg` | SwingVertical |
| ❌ | `actions/action_swing_horizontal.svg` | SwingHorizontal |
| ❌ | `actions/action_light.svg` | Light/display light |
| ❌ | `actions/action_quiet.svg` | Quiet |
| ❌ | `actions/action_turbo.svg` | Turbo/Powerful |
| ❌ | `actions/action_clean.svg` | SelfClean/XFanCleaning |
| ❌ | `actions/action_i_feel.svg` | IFeel |
| ❌ | `actions/action_timer.svg` | Timer |
| ❌ | `actions/action_timer_on.svg` | OnTimer |
| ❌ | `actions/action_timer_off.svg` | OffTimer |
| ❌ | `actions/action_sleep.svg` | Sleep |
| ❌ | `actions/action_economy.svg` | Economy/PowerSave |
| ❌ | `actions/action_wifi.svg` | Wi-Fi function |

Custom1..Custom8 deliberately do not require fixed artwork. They should use text, user-selected artwork, or `action_custom.svg` fallback.

---

# 6. State images

State assets represent **status**, not an action. Keep them separate from `action_*` icons.

All are `64×64` SVG masters, normally rendered at **18–28 dp**.

| Status | Required file | State |
|---|---|---|
| ❌ | `states/state_on.svg` | On |
| ❌ | `states/state_off.svg` | Off |
| ❌ | `states/state_open.svg` | Open |
| ❌ | `states/state_closed.svg` | Closed |
| ❌ | `states/state_locked.svg` | Locked |
| ❌ | `states/state_unlocked.svg` | Unlocked |
| ❌ | `states/state_active.svg` | Active/running |
| ❌ | `states/state_inactive.svg` | Inactive/idle |
| ❌ | `states/state_online.svg` | Online |
| ❌ | `states/state_offline.svg` | Offline |
| ❌ | `states/state_detected.svg` | Motion/presence detected |
| ❌ | `states/state_clear.svg` | No alarm/no detection |
| ❌ | `states/state_low_battery.svg` | Low battery |
| ❌ | `states/state_charging.svg` | Charging |
| ❌ | `states/state_warning.svg` | Warning |
| ❌ | `states/state_error.svg` | Error/fault |

---

# 7. Brand/integration artwork

Brand logos are optional. Prefer semantic device icons when a logo is not necessary. If a provider logo is used, it belongs in `branding/`, never in device/action folders.

| Status | Suggested file | Use |
|---|---|---|
| ◻️ | `branding/brand_hubitat.svg` | Hubitat branding |
| ◻️ | `branding/brand_philips_hue.svg` | Hue branding |
| ◻️ | `branding/brand_tuya.svg` | Tuya BLE/Wi-Fi branding |
| ◻️ | `branding/brand_bluetooth.svg` | Bluetooth mark only if licensing/brand usage is appropriate; otherwise use semantic device icon |
| ◻️ | `branding/brand_bthome.svg` | BTHome source label, if required |
| ◻️ | `branding/brand_theengs.svg` | Theengs source label, if required |

Provider logos may have their native aspect ratio. A square 64×64 viewBox is **not mandatory** for brand marks; preserve the official proportions.

---

# 8. Background images

Backgrounds are optional and only required when a UI template explicitly references them.

Recommended raster requirements:

- phone portrait full-screen: **at least 1440×2560**
- phone landscape: **at least 2560×1440**
- use JPG/WebP for photographic backgrounds, PNG for transparency/flat artwork
- keep file size preferably below about **500 KB** for runtime download where practical
- templates must specify aspect/fill behavior; do not create language-specific copies unless the artwork itself contains unavoidable text (normally it should not)

Suggested convention:

- `backgrounds/background_tv_default.webp`
- `backgrounds/background_air_conditioner_default.webp`
- `backgrounds/background_home_default.webp`

No generic background is mandatory for the application to function.

---

# 9. What should be added to `images/index.json`?

Every actual runtime asset must have an entry in `images/index.json` (or the successor catalog schema) containing at least:

- stable semantic `id`
- relative `path`
- `category`
- applicable `deviceTypes`
- useful `tags`

Example:

```json
{
  "id": "property-humidity",
  "path": "properties/property_humidity.svg",
  "deviceTypes": ["*"],
  "category": "property",
  "tags": ["humidity", "sensor", "bthome", "ble"]
}
```

A file that exists in Git but is not listed in the catalog should not be considered an official runtime asset.

---

# 10. Priority order for artwork creation

If artwork is created in batches, use this order:

1. **P0 — core application:** power, navigation, volume, media, add/settings/theme/back/delete/pin, on/off/online/offline.
2. **P0 — common device types:** television, air-conditioner, fan, light, switch, temperature/sensor, computer, Home screen, dashboard, Hubitat, Hue, Bluetooth.
3. **P1 — current IR catalog device types:** projector, set-top box, soundbar, speaker, AV receiver, air purifier, heater, humidifier, vacuum, streaming device, monitor, media players.
4. **P1 — integration properties:** temperature, humidity, battery, power, energy, motion, contact, illuminance, presence, color/brightness.
5. **P2 — open BLE expansion:** CO2, VOC, PM2.5, leak, plant/moisture, beacon/tracker, scale, lock, thermostat.
6. **P3 — rare legacy IR categories:** ceiling lift, LaserDisc, MiniDisc, VCR, toys, converters, etc.

---

# 11. Maintenance rule

Whenever any of these changes, update this file in the same change:

- a new `device-types.json` type is introduced,
- a new canonical `RemoteCommand` is introduced,
- a new integration exposes a reusable property/capability,
- a UI template introduces a new semantic image,
- a new runtime image is added to `images/index.json`.

The long-term goal is that this document can be mechanically validated: every **required** row should correspond to an indexed DeviceDB asset and every indexed production asset should have a documented purpose.
