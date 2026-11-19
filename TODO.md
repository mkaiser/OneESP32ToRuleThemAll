Next free number: T024

# TODO

What is still to do, and only that. What belongs here, how long an entry may be and how items are numbered:
[`workflow.md`](workflow.md); how to revise it: [`todo-housekeeping`](.claude/skills/todo-housekeeping/SKILL.md).
This project adds **Planned tests** and **Release** (the upstream PRs) and groups items by area
([`AGENTS.md`](AGENTS.md), "Workflow in this project"). Done items go to git (and the root [`.wiki/wiki/log.md`](.wiki/wiki/log.md) for findings about all heat pumps).
More than one writer: re-read from disk, change only your part.

# Incoming items by maintainer


# Next steps

None.

# Open decisions

None open.

# Planned tests

- **T021** Antilegionellen run with the backup heater fuses ON, today 16:00 CET
  ([plan](plans/T021-antilegionellen.md)). Requires: the maintainer at the panel (fuses, setting, clock).

# Blockers

## Heat pump

- **T001** Decode the unknown registers on the bus: phase 3, one panel action per `/test-sensor` run (hot water boost
  first; [plan](plans/T001-register-decoding.md), run sheet). Unblocked by: the maintainer at the panel.

## Cooling

- **T003** Test cooling with the ESP as FEK (room values from HA; dew point: house humidity ~65 %, FEK ~50 %).
  Unblocked by: the cooling season.
- **T004** Find what the Betriebsstatus bits do in real cooling and Sommerbetrieb (`DEBUG_BETRIEB`), then remove
  `DEBUG_BETRIEB` ([Betriebsstatus](doc/ttf07c/.wiki/wiki/betriebsstatus.md)). Unblocked by: the cooling season.
- **T005** Confirm "Betriebsstunden Kuehlen" (`0x07ff`), which returns `0x8000` until there are cooling hours
  ([registers](doc/ttf07c/.wiki/wiki/ttf07c-registers.md)). Unblocked by: the cooling season.

# Release

- **T002** Review the series of 14 upstream commits (1–12b), commits 7, 8, 12 and 12b first ([plan](plans/T002-T009-upstream.md)). Requires: the
  maintainer; delete the test device `/config/esphome/.ttf07check/` once the PRs are open.
- **T009** Open the upstream PRs 1 → 2a → 2b and the follow-ups ([plan](plans/T002-T009-upstream.md),
  [texts](upstream/issue-text.md)). Requires: T002; kr0ner's answer on the `doc/` folder.
- **T010** Offer an English names package `yaml/names/ttf07_wpm3i_en.yaml` for new installs. Requires: T009, kr0ner
  wants it.

# Future work

## Heat pump

- **T006** Decode the registers read only in the panel menus (`0x068E`, `0x0074`, `0x0294`, `0x06AE`, `0x4E68`,
  `0x4E5A`) with a guided `/test-sensor` pass through the other Einstellungen
  menus ([control panel](doc/ttf07c/control-panel.md), [registers](doc/ttf07c/.wiki/wiki/ttf07c-registers.md)). Requires: the
  maintainer at the panel; left open on purpose (2026-11-17).
- **T022** Control panel menu `doc/ttf07c/control-panel.md`: 3 gaps left (Status pages and Interne
  Berechnung while running, HK1 pages with Heizungssteuerung "Wärmepumpe"), listed in the page's "Gaps". Deferred by the maintainer.

## Analytics

- **T007** Recurrent check: community analytics stay connected and plausible ([plan](plans/T007-T008-analytics.md)).
- **T008** Decide whether the new entities go to the community analytics or stay out ([plan](plans/T007-T008-analytics.md)).
  Requires: the maintainer; ignored for now (2026-11-17).

## Energy management

- **T011** Research energy managers (EVCC, EMHASS, OpenEMS, HA automations) for this heat pump, PV and wallbox, and
  write a wiki page with a recommendation.

## Heat pump, Home Assistant, Firmware

- **T012** Recurrent check: after entity changes, update the HA dashboard, its export
  (`doc/ttf07c/dashboard-example/`) and the screenshots ([development](dev/development.md), "Dashboard and screenshots").
- **T013** Recurrent check: FEK emulation in daily use (comfort, compressor cycling, registration stays "FEK
  Emulation") ([heating control](doc/ttf07c/.wiki/wiki/heating-control.md)).
- **T014** Recurrent check: the daily COP with upstream's filtering (throttled, clamped to 1–10) still makes sense.
- **T015** Find what registered CAN ID `0x680`, which the WPM3i checks every 8 min without an answer
  ([CAN bus](doc/ttf07c/.wiki/wiki/can-bus.md)).
- **T016** Recurrent check: short API disconnects (1–2 s "unavailable" without reboot, 2026-11-15); watch WiFi and the
  `safe_mode took a long time` warning.
- **T017** Decide whether the heat pump's entity IDs adopt HA 2026.11's naming scheme (in the HA registry, not the
  firmware), then rename entities, dashboard, example and docs in one go ([entity names](.wiki/wiki/entity-names.md),
  `plans/naming.md` in the HA config). Requires: the maintainer's decision.
