# Device: heatpump-ttf07c

The one installation this fork runs on. See also: [CAN bus](can-bus.md).

## Hardware

- Heat pump: Tecalor TTF07 C (cool), brine/water, with WPM3i manager. External heating circuit pump with a constant
  41 W (shown on the pump's display; `static_leistung_heizkreispumpe`).
- ESP: ESP32-C3 (`esp32-c3-devkitm-1`), esp-idf framework (since 2026-11-16, Arduino before), internal CAN controller (`esp32_can`): TX `GPIO7`,
  RX `GPIO6`.
- Network: WiFi, `192.168.178.37`. OTA encrypted with the API key (since 2026-11-15, no password).
- FEK2 room unit: unplugged; the ESP emulates it permanently since 2026-11-16, see [Heating control](heating-control.md).

## Configuration

- Device file: `/homeassistant/esphome/heatpump-ttf07c.yaml` (Home Assistant repo, `mkaiser/homeassistant`).
  It sets the substitutions (intervals, `espclient_can_id: 0x680`, `static_leistung_heizkreispumpe: 41`, HA room
  sensors), loads `components/` as a local external component and includes `yaml/ttf07_wpm3i.yaml`.
- `friendly_name: " "`: entities have no device prefix in their names. HA shows them as "Wärmepumpe …" (HA device
  name). Old entity IDs start with `heatpump_`; entities created after the HA device was renamed start with
  `hwr_warmepumpe_`.

## Home Assistant

- Entity names come from `sensor_name` in `yaml/ttf07_wpm3i.yaml`. They were kept through the port, so the history
  is preserved (119 of 123 entities, 2026-11-15).
- Energy dashboard, individual devices (as of 2026-11-15):

| Device | Energy | Power | Included in |
|---|---|---|---|
| Wärmepumpe | `sensor.hwr_warmepumpe_energie_summe_kwh` (since 2026-11-16) | `sensor.heatpump_leistung_summe` | — |
| Heizung | `sensor.heatpump_el_energieaufnahme_heizen` | `sensor.heatpump_leistung_heizen` | Energie Summe |
| Warmwasser | `sensor.heatpump_el_energieaufnahme_warmwasser` | `sensor.heatpump_leistung_warmwasserbereitung` | Energie Summe |
| Heizkreispumpe | `sensor.heatpump_energie_ext_heizkreispumpe` | `sensor.heatpump_leistung_ext_heizkreispumpe` | Heizung |

- The old "Energie Summe" (`sensor.heatpump_energie_summe`) added kWh (pump) to MWh (El Energieaufnahme) and was
  ~1000x too small. The dashboard uses "Energie Summe kWh" since 2026-11-16 (18369 kWh); the old entity was removed
  from the firmware on 2026-11-16 (a new entity instead of a rescale, to keep the HA statistics clean).
- The "Energie ext. Heizkreispumpe" and "Leistung Summe integrated" integrations are restored across reboots since
  2026-11-15 (before, they restarted at 0).
- Settings (numbers) are re-requested every 15 min (`interval_very_slow`), not only at boot.
- Heating control (since 2026-11-15 23:02, see [Heating control](heating-control.md)):
  `select.hwr_warmepumpe_heizungssteuerung` (Wärmepumpe / FEK Emulation, restored, default Wärmepumpe),
  `sensor.hwr_warmepumpe_heizungssteuerung_aktiv`, `binary_sensor.hwr_warmepumpe_fek_installiert`,
  `select.hwr_warmepumpe_fek_emulation_betriebsart` (Komfort/Eco), `number.hwr_warmepumpe_fek_emulation_*`
  (Komfort/Eco temperature, Steigung, Offset, Raumeinfluss, Vorlauf min/max) and
  `sensor.hwr_warmepumpe_fek_emulation_vorlauf_soll`. Room values come from `sensor.temperatur_haus_mittel` /
  `sensor.luftfeuchtigkeit_haus_mittel`. Selected: FEK Emulation (since 2026-11-16 09:54). The old orphaned
  entities from earlier firmware are gone from HA (checked 2026-11-16).
- Dashboard "Wärmepumpe" (`/dashboard-warmepumpe`, redesigned 2026-11-16): tabs Übersicht (thermostat, control
  mode, temperatures, what runs now, hot water, 24 h history), Energie (kWh per day, COP, totals), Verlauf (7-day
  statistics), Einstellungen (heating control, FEK emulation curve, HK1 standalone, hot water, system, cooling),
  Diagnose (software, run times, hydraulics, refrigerant/electrical, reverse engineering, CAN IDs). Saved through
  the HA WebSocket API (`lovelace/config/save`). A copy for other users (entity IDs normalized to `warmepumpe_…`) is in
  `doc/ttf07c/dashboard-example/ttf07_wpm3i_dashboard.yaml` (since 2026-11-16; re-export with `.claude/tools/dashboard/export_dashboard.py`).
- Thermostat: `climate.hwr_warmepumpe_thermostat_heizung` ("Thermostat Heizung", follows the heating control; see
  [Heating control](heating-control.md)). Dashboard card "Heizung" on Übersicht.
- Hot water thermostat (since 2026-11-16): `climate.hwr_warmepumpe_thermostat_warmwasser`: preset comfort/eco ↔
  "Warmwasser Modus" (`select.hwr_warmepumpe_warmwasser_modus`, since 2026-11-18), target ↔ WW Komfort/WW Eco,
  current = Speicher Ist, action = Warmwasserbereitung. The hot water setpoint (Speicher Soll) is WW Komfort inside a
  Warmwasserprogramm window and WW Eco outside; the Programmschalter does not change it (test 2026-11-18). So
  "Warmwasser Modus" Komfort = window 00:00-24:00 on all days (Mo-So group `0x17A0` = `0x0060`, the WPM3i copies it to
  every day), Eco = no window, Programm = any other program (shown only, no preset). Tested 2026-11-18 10:39 and
  10:45: Speicher Soll follows within ~1 min, the preset doesn't flip . Switching overwrites a program
  set on the panel.
  Card on the dashboard's Übersicht, section Warmwasser.
- Community analytics (since 2026-11-16 20:44): `yaml/features/analytics.yaml` included in `heatpump-ttf07c.yaml`
  with all entities, district Bielefeld; diagnostic entities "Analytics MQTT Connected", "Analytics Last Update",
  "Analytics Global Device ID", "Github" (update available). What it sends: 2026-11-16. Own data on the community Grafana:
  `https://oneesp32torulethemall.freeddns.org/d/advz2wx/test?var-device_hash=<device-hash>` (anonymous; most comparison
  panels miss this device because of the entity names, 2026-11-17).
- CAN node activity (diagnostic, since 2026-11-16): `sensor.hwr_warmepumpe_can_*_frames` (frames per hour per
  sender, last 60 min; per minute until 2026-11-16) and `sensor.hwr_warmepumpe_can_unbekannte_sender`; see [CAN bus](can-bus.md).
- Software versions (diagnostic, since 2026-11-16): "Software WPM3i" (391.10; entity `sensor.hwr_warmepumpe_software_wpm2` until 2026-11-18) and
  `sensor.hwr_warmepumpe_software_hk1` ("391.10 (WPM3i)", "416.03 (FEK)", "416.03 (Emulation)").
- Cooling settings (since 2026-11-16, refreshed every 15 min): switches `switch.hwr_warmepumpe_kuhlen`,
  `…_kuhlmodus_aktivkuhlung`, `…_flachenkuhlung`, `…_geblasekuhlung`; numbers `number.hwr_warmepumpe_kuhlen_vorlauf_soll_temperatur`,
  `…_kuhlen_raum_soll_temperatur`, `…_kuhlen_hysterese`. Unknown values as diagnostic `sensor.hwr_warmepumpe_kuehlen_0x…`
  (`0xFDB2`, `0x06A5`, `0x06A6`, `0x068E`, `0xFDB6`); see [Cooling](cooling.md).
