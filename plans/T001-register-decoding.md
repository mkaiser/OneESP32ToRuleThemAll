# Plan: decode the unknown registers in the regular bus traffic (TTF07 C / WPM3i)

T001. Registers and their evidence: [`doc/ttf07c/.wiki/wiki/ttf07c-registers.md`](../doc/ttf07c/.wiki/wiki/ttf07c-registers.md)
(source of truth; update it with every result). Bus basics: [`doc/ttf07c/.wiki/wiki/can-bus.md`](../doc/ttf07c/.wiki/wiki/can-bus.md).

**Scope:** unknown registers that the heat pump's own nodes send **on their own, all the time**, without the panel
menus being open or the ESP asking. Registers read only in the panel menus (`0x068E`, `0x0074`, `0x0294`, `0x06AE`,
`0x4E68`, `0x4E5A`, …) are T006, not this plan.

**Rules:** passive listening and read requests only. Panel changes are made by the maintainer, and the ESP writes
nothing (`AGENTS.md`). Times in CET.

## Inventory (passive capture 2026-11-18 12:07–12:17, heating idle, emulation on)

10-min capture, 2389 frames. Rates from that capture; values also checked against all captures in `doc/ttf07c/.wiki/raw/captures/`.

| Group | Register | Path | Rate | Values seen | First hypothesis |
|---|---|---|---|---|---|
| A: WPM3i ↔ MFG | `0xFE4C` | WPM3i reads MFG | every 5 s | always 18 | **MFG software version** (Busteilnehmer: "04 MFG 18") |
| | `0xFE09` | WPM3i reads MFG | every 6 s | 18.5–18.9 °C (`et_dec_val`) | internal temperature (inverter/heat sink?), follows the compressor ([analysis](../doc/ttf07c/.wiki/raw/2026-11-17-tbd-temp-03-and-constants.md)) |
| | `0xFE1E` | WPM3i writes MFG | every ~20 s | always 0 | 4th actuator next to `PWM_LADEPUMPE`, `PWM_QUELLENPUMPE`, `UMSCHALTVENTIL_WW` (cooling valve? NHZ?) |
| B: Kessel block → `0x379` | `0x000A` | Kessel broadcast | every ~2.5 min | `0x110B` (2026-11-17), `0x120B` (2026-11-18) | **date**: high byte = day, low byte = month (like `0x0009` = minute/hour) |
| | `0x0010` | Kessel broadcast | every ~2.5 min | always `0x0051` = 81 | open (not the same as `0x601`'s `0x0010` = 2) |
| | `0x0053`, `0x005E`, `0x0073` | Kessel broadcast | every ~2.5 min | always 0 | state flags that are 0 at idle (defrost/EVU/cooling?) |
| | `0x005A` | Kessel broadcast, also `0x601` → HK1 | every ~2.5 min | always `0x0200` | open; same value from both senders |
| C: `0x601` block → HK1 | `0x0010` | `0x601` → HK1 | every ~2.5 min | always 2 | open (HK number? heating circuit type?) |
| | `0x0056`, `0x0057` | `0x601` → HK1 | every ~2.5 min | always 0 | open |
| D: FEK / emulation → `0x601`, Kessel | `0x0029`, `0x002A` | FEK → `0x601` | FEK block | `0x0A00`, `0x1E00` (10, 30) | `0x002A` very likely room setpoint max (30 °C); `0x0029` open ([FEK2](../doc/ttf07c/.wiki/wiki/fek2.md)) |
| | `0x006E` | FEK → Kessel | FEK block | `0x0100` / `0x0200` | changes only after plug-in; open |
| E: panel ↔ WPM3i | `0x06AF` | panel writes WPM3i | every 60 s | always 1 | keep-alive / "panel present" |
| | `0x4E8B` | panel writes WPM3i | every ~2.5 min | always 2 | open; sent together with `0x1388`/`0x080E` |
| | `0x080E` | WPM3i writes panel | every ~2.5 min | always 0 | goes with the error number `0x1388`: error sub-code or error count? |
| | `0x0B9D` | WPM3i writes panel | with the error list | 0 | error list related ([errors](../doc/ttf07c/.wiki/wiki/errors.md)) |
| F: rare | `0x4E5C`, `0x4E61`, `0x0645` | WPM3i writes panel | rare | `0x4E5C` 0x40/0x44, `0x4E61` 2254/2503, `0x0645` 1 | `0x4E61` changes: a counter or energy value? |

Group D does not show in this capture: the emulation runs and only the real FEK sends these.

## Method

Each register is decoded in the cheapest way that works. Stop as soon as one step gives a firm answer, then update
the registers page, `property.h` and the device file, and remove the debug sensor (`AGENTS.md`, "Unidentified registers").

1. **Hypothesis check.** Values that look like a date, version or constant are checked against a known
   reference (panel page, calendar, Busteilnehmer list). No test needed.
2. **Long passive capture.** A 24 h capture (ESP log, as in this inventory) with heating, hot water and idle
   phases. A script turns it into one time series per register and lists every register that changed, with the
   time and the known signals (`0x4e5e` status, compressor, NHZ, Umschaltventil) at that moment.
3. **Correlation.** Registers that change are compared with the HA history (outdoor temperature, flow and return,
   power, compressor, hot water). A register that changes with a known signal gets ✅ analysis.
4. **Provoked change.** Registers that never change get a matching action with `/test-sensor`: the maintainer
   changes a setting or state on the panel while the ESP records. One action per run.
5. **Leave open.** A register that stays constant through steps 2–4 is marked "constant, meaning open" and is
   not followed up further.

## Phases

### Phase 0: prepare (started 2026-11-18)

- Done 12:23: all "Debug …" sensors are enabled in HA (the 5 Manager menu registers `0x0074`, `0x0294`, `0x06AE`,
  `0x4E5A`, `0x4E68` were disabled by default; the others were on already), so the HA history collects them.
- Done: 24 h passive capture **2026-11-18 12:29:16 → 2026-11-19 12:29:16**, script `/share/heatpump-capture/capture.sh`
  (ESPHome API log, Communication lines only, reconnects on its own) → `/share/heatpump-capture/2026-11-18-passive-24h.log`
  (350k lines, 62 MB). One reconnect: gap ~30 s at 2026-11-19 07:47:33. Gotcha for later captures: stop early by
  killing `capture.sh` **and** the `esphome logs` process inside the ESPHome container (killing only `docker exec`
  leaves the client connected). **Flash 2026-11-18
  16:42:29–16:42:51** (ttf07_base refactor): ESP reboot, the capture continued without a reconnect; the FEK emulation
  re-registers within 8 min, so ignore FEK/`0x601`/HK1 traffic 16:42–16:51 in phase 2. Afterwards copy it to
  `doc/ttf07c/.wiki/raw/captures/` (filtered if too large).
- Done: `.claude/tools/can-capture/capture_series.py` (summary per register/sender/target, `--unknown`, `--changes
  0xFE09,...` with the status words and compressor current at each change, `--csv`, `--gaps`, `--exclude HH:MM-HH:MM`,
  midnight rollover). First look (12:29–17:00, heat pump idle): `0xFE09` flickers 18.7/18.8 °C, `0x4E5C`/`0x4E61`
  sent only at 16:44/16:47 (after the flash, probably with the emulation's re-registration), the rest constant.

### Phase 1: quick wins (step 1, no test)

- `0x000A` = date: **confirmed at midnight** (`0x120B` → `0x130B` between 23:57:04 and 00:04:04, 2026-11-19, 24 h
  capture). The frame's 6th data byte is `0x1A` = 26 = year (only `0x000A` has it in the Kessel block). Still to see:
  month change (2026-12-01 → `0x010C`). Firmware name goes into the phase 2 batch.
- `0xFE4C` = MFG software version: **checked 2026-11-18 17:15**, the panel shows "MFG 18" (panel photo, not kept), read from the Manager's `0x4E69` = 18; the MFG answers `0xFE4C` = 18.
  Status ◻️ plausible (same value, no change possible). Firmware: name it (e.g. `MFG_SOFTWARE`) with a diagnostic
  entity next to "Software WPM3i" and drop the debug sensor, batched with the phase 2 results (one flash, one
  dashboard update).
- `0x0645` / `0x4E5C` / `0x4E61` (group F): sent by the WPM3i at 16:44 and 16:47 after the flash, each followed by the
  panel reading the MFG software (`0x4E69`) and, at 16:47, the FEK software: probably a "bus participants changed"
  notice while the emulation re-registered (`0x4E5C` `0x40` → `0x44`: bit 2 = FEK present?). Test: the next flash
  or emulation off/on (maintainer's go) and check that `0x4E5C` drops bit 2 without the FEK.
- `0x06AF` = panel keep-alive: name only if it never changes (no entity needed).

### Phase 2: 24 h series (steps 2–3)

- Groups A, B, C, E, F from the 24 h capture: which register changes, when, and with what.
- `0xFE09` and `0xFE1E` are the most promising (`0xFE09` changes with the compressor; `0xFE1E` is a WPM3i command to
  the MFG). For `0xFE09`, also compare with the compressor current (`0xFE07`) and power: an inverter temperature
  rises with the load, a refrigerant temperature with the circuit.
- `0x4E61` and `0x4E5C`: capture them with the 24 h log; if `0x4E61` grows like a counter, compare with the energy
  and starts totals.

### Phase 3: provoked changes (step 4, with the maintainer)

Ordered by what a single action can tell:

| Action (panel, maintainer) | Watches | Decides |
|---|---|---|
| Hot water boost (WW Komfort / Programmschalter WW) | `0xFE1E`, Kessel `0x0053`/`0x005E`/`0x0073` | which flags follow hot water |
| Sommerbetrieb on/off | `0x0053`/`0x005E`/`0x0073`, `0x005A` | summer flags |
| Programmschalter Notbetrieb (NHZ) | `0xFE1E`, Kessel flags | NHZ command or flag |
| Heizkreis settings (HK1 Einstellungen) | `0x601` `0x0010`/`0x0056`/`0x0057`/`0x005A` | HK1 configuration values |
| Real FEK plugged in (only if needed) | `0x0029`, `0x006E` | FEK values (group D) |

**Run sheet (one action per `/test-sensor` run; the maintainer acts on the panel, the ESP only records):**

Before each run: heat pump not in a compressor lock-out (`Verdichter Reststillstand` = 0) and no hot water cycle running;
after: restore the setting and check it in HA.

1. **Hot water boost** (Programmschalter WW Komfort, or WW boost): watch `0xFE1E`, `0x0053`, `0x005E`, `0x0073`,
   `UMSCHALTVENTIL_WW`. Also tells whether `0x0053` pulses with the valve (the 19.11 burst).
2. **Sommerbetrieb on/off** (Heizen > Grundeinstellung > Sommerbetrieb; changes heating, restore at once): watch
   `0x0053`/`0x005E`/`0x0073`, `0x005A`, `0xFDB4`. Also answers whether Sommerbetrieb "on" means "enabled" or "active".
3. **Notbetrieb (NHZ)**: watch `0xFE1E`, the Kessel flags. Only with the maintainer present; the heating element runs.
4. **HK1 settings** (only without emulation: Heizungssteuerung "Wärmepumpe"): watch `0x601` `0x0010`/`0x0056`/`0x0057`/`0x005A`.
5. **Antilegionellen** (`0x0101`, Kessel; the panel switch only set the flag for 2 s on 2026-11-17 20:14, no run):
   a) look first, no change: the maintainer reads the panel's Warmwasser/Antilegionellen menu (day, time, temperature,
   interval, start function) and photographs it into `doc/ttf07c/.wiki/raw/`; b) passive: the ESP polls `0x0101` only every 15 min,
   so a short run can be missed; the 24 h capture shows 97 reads, all 0, and HA shows no "on" since 2026-11-17 22:26, so no
   run in 4 days (a weekly schedule is possible); capture ≥ 8 days or log the Kessel status changes; c) run only if
   a) shows a start function: the tank is heated to the disinfection temperature, the heating element (3-9 kW) may
   run, so start it in the afternoon after a hot water cycle, with the maintainer present. Watch `0x0101`, `0x4E5E`,
   Speicher-Ist (`0x000E`), Nachheizstufe, `UMSCHALTVENTIL_WW`.
6. **Real FEK** (group D): last, only if needed.
Passive extras that need no action: another 24 h capture (a second `0x0053` burst, month change `0x010C` on
2026-12-01).

Cooling-related candidates wait for the cooling season (T003–T005); EVU block and defrost cannot be
triggered on purpose and are covered by the 24 h captures as they happen.

### Phase 4: tidy up

- Per decoded register: property in `property.h` (TTF_07_C), entity in `yaml/ttf07_wpm3i.yaml` + German name in
  `yaml/names/ttf07_wpm3i_de.yaml`, remove the debug sensor, update `ttf07c-registers.md` and the log.
- Registers left "constant, meaning open" stay in the registers page only (no debug sensor).

## Status log

Newest first.

- **2026-11-22 (evening):** batch flashed and confirmed ("Software MFG" = 18). Also named from panel photos:
  `0x0658`–`0x065a` = Sensor Abgleich Vorlauf WP / Vorlauf NHZ / Rücklauf WP (registers page). Nothing uncommitted.
  **Next:** phase 3 step 1 (hot water boost) with the maintainer at the panel.

- **2026-11-22:** firmware batch: `0x000A` = `DATUM` (`et_datum`, no entity), `0xFE4C` = `MFG_SOFTWARE` (sensor
  "Software MFG"), debug sensor removed; config valid, compile running, flash waits for the maintainer's go. **Next:**
  phase 3 (run sheet), one panel action per run with the maintainer.

- **2026-11-21 (later):** the `0x0053` burst (19.11 09:43:21-09:45:16) coincides with `UMSCHALTVENTIL_WW` = 100 % and
  `0x4E5E` = `0x0200`, compressor off: a valve run without hot water production. Needs a second occurrence to confirm.
- **2026-11-21:** phase 2 run on the 24 h capture (not copied to git). Only `0x0053` (one burst 19.11 09:43-09:45,
  idle) and `0xFE09` (18.6-18.8 °C) changed besides time/date; all others constant. Results in the registers page and
  log. **Next:** phase 3 for the constant ones; decide whether to look at the `0x0053` burst in the HA history.

- **2026-11-19 ~12:45:** 24 h capture finished (12:29, one ~30 s gap at 07:47:33), `0x000A` = date confirmed at
  midnight; nothing committed from the capture. **Next:** copy it to
  `doc/ttf07c/.wiki/raw/captures/2026-11-18-1229-passive-24h.log` (proposed: only a filtered copy without the WPM3i → MFG read
  requests goes to git, the raw 62 MB stay in `/share/heatpump-capture/`; ask the maintainer before committing it),
  run `capture_series.py --unknown --exclude 16:42-16:51` and `--changes` on the registers that changed, then
  phase 2. Most promising: `0xFE09` (follows the compressor), `0xFE1E` (WPM3i command to the MFG), `0x4E61`
  (counter?). Registers that never changed go to phase 3.
- **2026-11-18 17:15:** `0xFE4C` = MFG software version confirmed by the maintainer's panel photo. Decided
  (maintainer, 2026-11-18): name `0x000A` and `0xFE4C` (`MFG_SOFTWARE`, diagnostic entity next to "Software WPM3i",
  debug sensor removed) in **one firmware batch with the phase 2 results** (one flash, one dashboard update).
- **2026-11-18:** decided (maintainer): HEISSGAS 76.6 °C was a one-off, not followed up; the fault-list item was
  dropped (list empty after the heat pump reset). Group D (FEK: `0x0029`, `0x002A`, `0x006E`) comes last: it needs
  the real FEK plugged in instead of the emulation.

Capture handling and the gotchas of stopping a capture: [`dev/development.md`](../dev/development.md). Phase 3 runs
with `/test-sensor`: propose one panel action per run to the maintainer; never change anything on the heat pump
yourself. Record every result in the registers page, the wiki log and the inventory above.
