# Theengs BLE device implementation catalog

Tracking list for HomeController's independent BLE decoders. `[x]` means a HomeController DeviceDB profile exists and is indexed; `[-]` means a generic/protocol-family entry or not yet a normal sensor profile; `[ ]` means pending. Theengs is used as protocol research/provenance; HomeController does not embed the GPL decoder.

Source catalog: https://decoder.theengs.io/devices/devices.html

**Maintenance rule:** whenever a new HomeController profile is implemented and indexed, its corresponding device entry/entries in this file must be changed to `[x]` in the same change/batch. This catalog is the implementation checklist and must stay synchronized with `bluetooth/profiles` and `bluetooth/catalogs`.

## Implemented / first priority

- [x] HHCCJCY01HHCC / HHCCJCY10 — Xiaomi MiFlora / Flower Care (stable HomeController generic GATT profile)
- [x] ABN07 — April Brother Sensor N07
- [x] CGC1 / CGD1 — Qingping/ClearGrass Alarm Clock
- [x] RuuviTag_RAWv2 — RuuviTag RAW v2
- [x] BM6 — Generic BM6 Battery Monitor

## Full Theengs catalog

- [x] ABN03 — April Brother Sensor N03
- [x] ABN07 — April Brother Sensor N07
- [x] ABTemp — April Brother ABTemp
- [x] ADHS — Amphiro/Oras/Hansa Hydractiva/Activejet Digital
- [x] Amazfit — Amazfit Smart Watch/Band
- [x] APPLEAIRPODS — Apple AirPods (Pro)
- [x] APPLEDEVICE — Apple iPhone/iPad
- [x] APPLEWATCH — Apple Watch
- [x] ARANET4 — Aranet4 CO2 Monitor
- [x] BEATSBUDS — Beats Solo/Studio Buds
- [x] BM2 — Generic BM2 Battery Monitor
- [x] BM6 — Generic BM6 Battery Monitor
- [x] BPv1.0-2.0 — b-parasite environmental/soil sensor
- [x] BSDOO — Otio/BeeWi Door & Window Sensor
- [x] BTH01 — Tuya BTH01
- [x] CGC1 — ClearGrass/Qingping Alarm Clock (shared CGC1/CGD1 profile)
- [x] CGD1 — ClearGrass/Qingping Alarm Clock
- [x] CGDK2 — Qingping TH Lite
- [x] CGDN1 — Qingping Air Monitor Lite
- [x] CGG1 — Qingping Round Hygro Thermometer
- [x] CGH1 — Qingping Contact Sensor
- [x] CGP1W — Qingping Weather Station
- [x] CGP22C — Qingping Thermo-Hygrometer CO2 Detector
- [x] CGP23W — Qingping Barometer Pro
- [x] CGPR1 — Qingping Motion & Light
- [x] ECOFLOW_ADV — EcoFlow Power Station
- [x] F525/F51C — Jaalee TH sensor
- [x] FEASY — Feasycom Bluetooth Beacon
- [x] H10 — Polar Heart Rate Sensor
- [x] H5055 — Govee BBQ Thermometer
- [x] H5072 — Govee Thermo-Hygrometer
- [x] H5074 — Govee Smart Thermo-Hygrometer
- [x] H5075 — Govee Thermo-Hygrometer
- [x] H5100 — Govee Smart Thermo Hygrometer
- [x] H5101 — Govee Smart Thermo-Hygrometer
- [x] H5102 — Govee Smart Thermo-Hygrometer
- [x] H5104 — Govee Smart Thermo Hygrometer
- [x] H5105 — Govee Smart Thermo Hygrometer
- [x] H5106 — Govee Smart Air Quality Monitor
- [x] H5108 — Govee Smart Probe Thermometer
- [x] H5140 — Govee Smart CO2 Monitor
- [x] H5174 — Govee Smart Thermo-Hygrometer
- [x] H5177 — Govee Thermo-Hygrometer
- [x] H5179 — Govee Smart Thermo-Hygrometer
- [x] HHCCJCY01HHCC — Xiaomi/VegTrug MiFlora (covered by Flower Care profile)
- [x] HHCCJCY10 — Xiaomi MiFlora / Flower Care family
- [x] HHCCPOT002 — Xiaomi RoPot
- [-] IBEACON — Generic iBeacon protocol family
- [x] IBS-P01B — Inkbird Pool Thermometer
- [x] IBS-P02B — Inkbird Pool Thermometer
- [x] IBS-TH1 — Inkbird Thermometer Hygrometer
- [x] IBS-TH2 — Inkbird Thermometer Hygrometer
- [x] IBT_2X(S) — Inkbird BBQ 2-probe
- [x] IBT_4X(S/C) — Inkbird BBQ 4-probe
- [x] IBT_6X(S) — Inkbird BBQ 6-probe
- [x] INEM — iNode Energy Meter
- [x] ITH-12S — Inkbird Thermometer Hygrometer
- [x] JQJCY01YM — Xiaomi Formaldehyde Detector
- [x] K6P — KKM Long Range K6P
- [x] K9 — KKM Tracking K9
- [x] KSensor — BlueCharm/KKM Beacon
- [ ] LYWSD02 — Xiaomi/Mijia e-ink Clock
- [ ] LYWSD03MMC_ATC/PVVX/BTHOME — Xiaomi Compact Temperature Sensor
- [ ] LYWSDCGQ — Xiaomi Mi Jia TH sensor
- [ ] M1017 — Mopeka/Lippert LPG Tank Sensor
- [x] MBXPRO — MOKOSMART H4
- [ ] MHO/MMC-C401_ATC/PVVX — Xiaomi Compact Temperature Sensor
- [x] MiBand — Xiaomi Mi Band
- [ ] MJWSD05MMC_ATC/PVVX/BTHOME — Xiaomi Compact Temperature Sensor
- [x] MokoBeacon — MOKOSMART Beacon
- [x] MUE4094RT — Xiaomi Motion and Light
- [ ] MX2001 — Onset Hobo Water Level Sensor
- [x] NODONNIU — NodOn NIU smart button
- [ ] ORALB_BT — Oral-B Bluetooth Toothbrush
- [ ] ORAS — Amphiro/Oras/Hansa Smart Faucet
- [ ] RC1010 — Otodata RC1010 Level Monitor
- [ ] RDL52832 — Radioland sensor iBeacon
- [x] RuuviTag_RAWv1 — RuuviTag RAW v1
- [x] RuuviTag_RAWv2 — RuuviTag RAW v2
- [ ] SBBT-002C — ShellyBLU Button1
- [ ] SBBT-004CEU — ShellyBLU Wall Switch4
- [ ] SBBT-004CUS — ShellyBLU RC Button4
- [ ] SBDW-002C — ShellyBLU Door/Window
- [ ] SBHT-003C — ShellyBLU H&T
- [ ] SBMO-003Z — ShellyBLU Motion
- [x] SCD4X — Sensirion MyCO2/CO2 Gadget
- [x] SDLS — SmartDry Laundry Sensor
- [ ] SE_MAG — Sensor Easy Door/Window Pro
- [ ] SE_RHT — Sensor Easy Temperature and Humidity Pro
- [ ] SE_TEMP — Sensor Easy Temperature
- [ ] SE_TEMP_PRO — Sensor Easy Temperature Pro
- [ ] SE_TPROBE — Sensor Easy External Probe Pro
- [-] ServiceData — Generic Bluetooth SIG service-data family
- [x] SHT4X — Sensirion TH Sensor
- [x] SKALE — Atomax Skale I/II
- [x] SOLIS_6 — Ternergy BBQ 6-probe (shared IBT-6X/SOLIS-6 wire format)
- [ ] SPHT — SensorPush HT.w
- [ ] SPHTP — SensorPush HTP.xw
- [x] T201 — Oria/Brifit/SigmaWit/SensorPro TH
- [x] T301 — Oria/Brifit/SigmaWit/SensorPro TH
- [x] TD1in1 — BlueMaestro Tempo Disc
- [x] TD3in1 — BlueMaestro Tempo Disc
- [x] TD4in1 — BlueMaestro Tempo Disc
- [x] TG-BT5 — MikroTik TG-BT5-IN/-OUT
- [x] TH05F — Tuya TH05F
- [x] THB1 — Tuya THB1
- [x] THX1(W230150X) — SwitchBot Meter (Plus)
- [x] TILT — Tilt Brewing Hydro-Thermometer
- [x] TP350 — ThermoPro TH sensor
- [x] TP357 — ThermoPro TH sensor
- [x] TP358 — ThermoPro TH sensor
- [x] TP359 — ThermoPro TH sensor
- [x] TP393 — ThermoPro TH sensor
- [x] TPMS — Generic Tire Pressure Monitoring System
- [x] TPMSBR — Generic TPMS
- [x] UT363BT — UNI-T Anemometer
- [x] VCH6003 — VCHON TH sensor
- [x] VICTBSC — Victron Blue Smart Charger
- [x] VICTORIONXS — Victron Orion XS
- [x] VICTSBP — Victron Smart BatteryProtect
- [ ] VICTSBS — Victron Smart Battery Sense
- [ ] VICTSCC — Victron SmartSolar MPPT
- [x] W070160X — SwitchBot Curtain 2/3
- [x] W110150X — SwitchBot Motion Sensor
- [x] W120150X — SwitchBot Contact Sensor
- [x] W270160X — SwitchBot Blind Tilt
- [x] W340001X — SwitchBot Outdoor Meter
- [x] W490001X — SwitchBot Meter Pro CO2
- [x] WS02/WS08 — SensorBlue/Oria/Brifit ThermoBeacon
- [x] X1 — SwitchBot Bot
- [ ] XMTZC01HM/XMTZC04HM — Xiaomi Mi Smart Scale
- [ ] XMTZC02HM/XMTZC05HM — Xiaomi Mi Body Composition Scale
- [ ] XOSSX2 — XOSS X2 Heart Rate Sensor

## Next implementation order

Continue from the first unchecked device in the full catalog, five devices per batch. A device is checked only after a HomeController profile exists and is indexed; hardware-unverified ports remain `experimental`. Every future implementation batch must update this checklist in the same commit/batch so completed devices cannot remain unchecked.
