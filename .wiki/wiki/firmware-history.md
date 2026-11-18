# Firmware history and decisions

See also: [Device](device-heatpump-ttf07c.md), [development](../../dev/development.md) (branches and commit topics).

## Old implementation (branch `archive/ttf07-old`, named `ttf07` until 2026-11-18; used until 2026-11-15)

- Based on upstream before its restructuring: `src/*.h` included directly, everything in one `yaml/ttf07.yaml`
  (597 lines). Self-contained; did not use upstream's base files.
- Introduced: WPM3i node (`0x480`) for Betriebsstatus and Programmschalter, power/energy split, COP, operating hours,
  cooling switch, debug sensors, detailed CAN logging.
- Last commits: cooling properties and controls (`35e8ebe`); build fix for ESPHome 2026.10 (`8dc6529`), which
  replaced `raw_state` with `get_raw_state()` and removed `typeid` from `SimpleVariant` (ESPHome builds with `-fno-rtti`).

## Port to upstream (branch `ttf07-port`, 2026-11-15)

Upstream had moved on by 66 commits: `src/` became the external component `components/wp_core`, the yaml was split
into `core.yaml` → family base → device file plus `templates/`, and CAN nodes became configurable (`CanNode::*`).
A commit-by-commit rebase conflicted in 13 files on the first commit, so the work was ported in one go onto
upstream `master`, then split into topic commits.

Decisions:
- **Separate device file** `yaml/ttf07_wpm3i.yaml`; upstream's `yaml/ttf07.yaml` is unchanged. This keeps upstream
  updates easy and the WPM3i variant explicit.
- **WPM3i = `CanNode::Manager` at `0x480`** (upstream uses Manager for the same WPM in the WPL configs); no new node.
- **Keep the HA display names** through optional `sensor_name`/`sensor_id` template parameters (defaults keep
  upstream's behaviour), so no HA history is lost. Replaced 2026-11-18: template entities are named by id like
  upstream, German names come from the optional package `yaml/names/ttf07_wpm3i_de.yaml` (`!extend`), which keeps
  the same HA entities; debug sensors by address in `yaml/ttf07_wpm3i_debug.yaml`.
- **Upstream names for known addresses** (`QUELLE_IST`, `HEISSGAS_TEMP`, `LAUFZEIT_*`, `LEISTUNG_*PUMPE`, …).
- **Don't send room temperature/humidity from HA** (core.yaml would every minute; removed with `!remove`), as in the
  old firmware.
- **Arduino framework kept** on the ESP32-C3, to keep the change small.
- Detailed CAN logging re-implemented on upstream's code (optional sender ID parameter for `processCanMessage`).

Dropped or changed compared to the old firmware:
- COP uses upstream's filtering, not the fixed median window.
- Time sync: weekly (Sunday 03:05, HA time), not daily via SNTP; it now also sends the seconds.
- The cooling switch no longer writes "off" at boot (`restore_mode: DISABLED`).
- "Einphasiger Betrieb" is a binary sensor (bool property).

Verified after the flash (2026-11-15): all values plausible, no writes from the ESP at boot, 119 of 123 entity
names unchanged. The only firmware-caused difference was the missing `0x100` node for three debug sensors
([raw](../raw/2026-11-15-ha-history-observations.md)).

## 2026-11-16: emulation in daily use, esp-idf

- FEK emulation with flow setpoint passed its test and is the selected heating control ([Heating control](heating-control.md)).
- The emulation answers reads addressed to HK1 (the panel lagged ~10 s per screen without it).
- **Framework esp-idf** (decision: follow upstream). The Arduino decision of the port is reverted; the switch was
  one line in the device file plus an OTA flash, no code changes needed.
- Core: writes from the control panel (`CanNode::Bedienteil`) update the addressed node's entity at once.
- Deprecated "Energie Summe" removed; FEK protocol properties named (`KESSELSOLLTEMP`, …).
- Flashing while emulating: the WPM3i keeps HK1 reserved until its next presence check, so the emulation pauses for
  up to 8 min (observed 1–5 min); the compressor is not affected.
