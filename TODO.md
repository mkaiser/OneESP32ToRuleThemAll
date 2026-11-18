Next free number: T018

# TODO

What is still to do, and only that. What belongs here, how long an entry may be and how items are numbered:
[`workflow.md`](workflow.md); how to revise it: [`todo-housekeeping`](.claude/skills/todo-housekeeping/SKILL.md).
This project adds **Planned tests** and groups items by area ([`AGENTS.md`](AGENTS.md), "TODO.md"). Done items go
to git and [`.wiki/wiki/log.md`](.wiki/wiki/log.md). More than one writer: re-read from disk, change only your part.

# From the maintainer

(empty)

# Next steps

## Heat pump

- **T001** Decode the unknown registers that are on the bus all the time; next: copy the 24 h capture to
  `.wiki/raw/captures/` and run phase 2 ([plan](plans/register-decoding.md)). Requires: the maintainer's go to commit
  the capture; `0x000A`/`0xFE4C` firmware names wait for the phase 2 batch (decision 2026-11-18).

## Firmware

- **T002** Review the series of 13 commits, commits 7, 8 and 12 first ([plan](plans/upstream.md)). Requires: the
  maintainer; delete the test device `/config/esphome/.ttf07check/` once the PRs are open.

# Open decisions

None open.

# Planned tests

None planned (the tests of T001 are in its plan).

# Blockers

## Cooling

- **T003** Test cooling with the ESP as FEK (room values from HA; dew point: house humidity ~65 %, FEK ~50 %).
  Unblocked by: the cooling season.
- **T004** Find what the Betriebsstatus bits do in real cooling and Sommerbetrieb (`DEBUG_BETRIEB`), then remove
  `DEBUG_BETRIEB` ([Betriebsstatus](.wiki/wiki/betriebsstatus.md)). Unblocked by: the cooling season.
- **T005** Confirm "Betriebsstunden Kuehlen" (`0x07ff`), which returns `0x8000` until there are cooling hours
  ([registers](.wiki/wiki/ttf07c-registers.md)). Unblocked by: the cooling season.

# Future work

## Heat pump

- **T006** Decode the registers read only in the panel menus (`0x068E`, `0x0074`, `0x0294`, `0x06AE`, `0x4E68`,
  `0x4E5A`, Kessel `PUFFERBETRIEB`/`PUMPENZYKLEN`) with a guided `/test-sensor` pass through the other Einstellungen
  menus ([raw](.wiki/raw/2026-11-17-expert-menus.md), [registers](.wiki/wiki/ttf07c-registers.md)). Requires: the
  maintainer at the panel; left open on purpose (2026-11-17).

## Analytics

- **T007** Recurrent check: community analytics stay connected and plausible ([plan](plans/analytics.md)).
- **T008** Decide whether the new entities go to the community analytics or stay out ([plan](plans/analytics.md)).
  Requires: the maintainer; ignored for now (2026-11-17).

## Upstream

- **T009** Open the upstream PRs 1 → 2a → 2b and the follow-ups ([plan](plans/upstream.md),
  [texts](upstream/issue-text.md)). Requires: T002; kr0ner's answer on the `docs/` folder.
- **T010** Offer an English names package `yaml/names/ttf07_wpm3i_en.yaml` for new installs. Requires: T009, kr0ner
  wants it.

## Energy management

- **T011** Research energy managers (EVCC, EMHASS, OpenEMS, HA automations) for this heat pump, PV and wallbox, and
  write a wiki page with a recommendation.

## Heat pump, Home Assistant, Firmware

- **T012** Recurrent check: after entity changes, update the HA dashboard, its export and the screenshots
  ([development](dev/development.md), "Dashboard and screenshots").
- **T013** Recurrent check: FEK emulation in daily use (comfort, compressor cycling, registration stays "FEK
  Emulation") ([heating control](.wiki/wiki/heating-control.md)).
- **T014** Recurrent check: the daily COP with upstream's filtering (throttled, clamped to 1–10) still makes sense.
- **T015** Find what registered CAN ID `0x680`, which the WPM3i checks every 8 min without an answer
  ([CAN bus](.wiki/wiki/can-bus.md)).
- **T016** Recurrent check: short API disconnects (1–2 s "unavailable" without reboot, 2026-11-15); watch WiFi and the
  `safe_mode took a long time` warning.
- **T017** Decide whether the heat pump's entity IDs adopt HA 2026.11's naming scheme (in the HA registry, not the
  firmware), then rename entities, dashboard, example and docs in one go ([entity names](.wiki/wiki/entity-names.md),
  `plans/naming.md` in the HA config). Requires: the maintainer's decision.
