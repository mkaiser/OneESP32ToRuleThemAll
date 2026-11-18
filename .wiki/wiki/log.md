# Log

Append-only. Newest at the bottom. Format: `## YYYY-MM-DD <kind>: <title>` (kinds: ingest, change, test, decision,
lint). Times are local (log clock) unless marked UTC.

## 2026-11-15 change: build fix for ESPHome 2026.10 (old `ttf07` branch)
`raw_state` → `get_raw_state()`, `SimpleVariant` without `typeid`. Flashed and running.

## 2026-11-15 decision: port to upstream instead of rebasing
66 upstream commits incl. restructuring; the first of 11 commits conflicted in 13 files. Ported in one go onto
upstream `master` as `yaml/ttf07_wpm2.yaml` plus template and property extensions. See
[firmware history](firmware-history.md).

## 2026-11-15 test: ported firmware flashed
All values plausible, no writes at boot. 119 of 123 HA entity names unchanged. On the first boot the HK1 numbers
stayed `unknown` (single request at boot, answer lost while the FEK was being unplugged); fine after a reboot.

## 2026-11-15 ingest: FEK attached / removed
FEK sends room temperature/humidity via HK1 → `0x601`; cooling values still `0x8000` with the FEK attached.
Raumeinfluss 2 with the FEK, 10 without. Pages: [FEK2](fek2.md), [Cooling](cooling.md).

## 2026-11-15 change: detailed CAN logging re-implemented
One line per frame with sender, addressed node, property and raw value; log filter for frequent properties.

## 2026-11-15 test: comparison before/after the port (HA history)
Differences were physical (compressor stopped, FEK removed), except node `0x100`: debug sensors `TBD_09/11/16` lost
their values. Source: [raw](../raw/2026-11-15-ha-history-observations.md).

## 2026-11-15 change: settings refresh, energy total, restore, OTA encryption
- Numbers/switch re-requested every 15 min.
- New "Energie Summe kWh" (18360 kWh); old "Energie Summe" kept until the Energy dashboard is switched.
- Integration sensors restored across reboots.
- OTA encrypted with the API key; password removed.

Flashed and checked: all settings have values, encrypted OTA works.

## 2026-11-15 change: repo organized
Added `AGENTS.md`, `TODO.md` (forward looking), this wiki, and the skills `test-sensor` and `revise-todo`.
Branch `ttf07-port` rebuilt as topic commits on upstream `master`.

## 2026-11-15 ingest: initial wiki pages
Created all pages from the port work, the old notes ([raw](../raw/2026-11-15-old-ttf07-yaml-notes.md)), CAN
captures ([baseline](../raw/captures/2026-11-15-1625-baseline-heating-off.log),
[read request](../raw/captures/2026-11-15-1627-read-request-test.log)) and HA history.

## 2026-11-15 test: settings refresh confirmed
At 17:12:56 (boot + 15 min) the ESP re-requested all settings; HK1 and Kessel answered within 3 s
(KOMF_TEMP 23.0, ECO_TEMP 19.5, STEIGUNG_HK1 0.26, RAUMEINFLUSS raw 0x0A00 = 10 little endian, WW_KOMF_TEMP 52.0).
No errors in 16 min of log.

## 2026-11-15 ingest: node 0x100, system messages, second 0x680 sender
From a 16-min capture ([raw](../raw/captures/2026-11-15-1704-system-messages.log)): `0x100` is most likely the
control panel (polls display values, gets the minute, sends a keep-alive). Message types are the low nibble of the
first ID byte; type 6/7 system messages every 7 min on `0x00FE`, starting with `0x601` → HK1 (also with the FEK
unplugged). Another device sends with CAN ID `0x680` (the ESP's ID). Pages: [CAN bus](can-bus.md), [FEK2](fek2.md).

## 2026-11-15 change: node Bedienteil (0x100), type-aware CAN log
New `CanNode::Bedienteil` (default `0x123`, set to `0x100` in `ttf07_wpm2.yaml`); `TBD_09/11/16` listen there again.
The log decodes the addressed node and message type from the ID bytes (`to 0x301/HK1, system`). Flashed 17:45.
`analyze_can.py` decodes types and lists senders.

## 2026-11-15 decision: goal is to replace the FEK with HA room sensors
Maintainer wants to remove the FEK and give the heat pump the house sensors. FEK traffic recording started 17:46.

## 2026-11-15 test: FEK plugged in (17:50 local)
The compressor stopped in the same second as the first FEK-related write (`0x601` → HK1, `0x0052` = 0). HK1 stopped
answering the ESP's reads. No room value frames in 20 min (earlier today: every minute). The 7-min `0x00FE` and
8-min `0x00FD` system messages also occur without the FEK. Pages: [FEK2](fek2.md), [CAN bus](can-bus.md). Sources:
[capture](../raw/captures/2026-11-15-1746-fek-plugged-in.log), [analysis](../raw/2026-11-15-1746-fek-plugged-in-analysis.txt).

## 2026-11-15 test: FEK unplugged (18:37)
The WPM2 deregistered `0x301` after one unanswered 8-min check (18:40); HK1 answered the ESP again 34 s later. See
[FEK2](fek2.md).

## 2026-11-15 decision: emulate the FEK with the ESP (test)
Maintainer asked to emulate the FEK and check the "Kühlung" menu entry on the heat pump.

## 2026-11-15 change: raw bytes in the CAN log, FEK emulation switches
The log line ends with `data <bytes>`. Found: system messages use the short form (`D6 00 FD 08 00 00 00`).

## 2026-11-15 test: FEK emulation
Long form (18:51): not understood. Short form (19:13): accepted (HK1 silent, check at 19:20 answered in 13 ms), room
values sent from HA. **No "Kühlung" menu entry.** Emulation off at 19:21. See [FEK2](fek2.md).

## 2026-11-15 test: real FEK as reference (19:33 local)
FEK fully active: registration, system messages, clock reads, flow setpoint to the Kessel, room values every
10–45 s, and answers to the control panel's identification reads (`0x0199` = 416, `0x019A` = 3). **The "Kühlen" menu
entry appeared.** Protocol table in [FEK2](fek2.md). Source:
[capture](../raw/captures/2026-11-15-1933-real-fek-plug-in-raw.log).

## 2026-11-15 change: FEK emulation answers the control panel and system messages (compiled, not flashed yet)
Answers `0x0199`/`0x019A` reads from the control panel, takes part in the `0x00FE` system messages (on registration,
every 7 min, answers to `0x601`). No flow setpoint yet, so it does not take over heating.

## 2026-11-15 lint: FEK findings consolidated
FEK2 page: status summary, confirmed hypothesis, open questions with the unknown properties. CAN bus page: short/long
form rules, `0x601` is not the FEK, `0x301` taken over by a registered FEK, clock `0x0009`. Device page: emulation
switches. Index summaries updated.

## 2026-11-15 test: emulation with identification makes "Kühlen" appear (21:06 local)
Emulation answers the control panel's `0x0199` read (416) and takes part in the `0x00FE` system messages: the
"Kühlen" menu entry appeared. The menu values are read from the Kessel (`0xFDB2`, `0x06A4`, `0x0287`, `0x025F`,
`0x025B`, `0x06A5`, `0x06A6`) and the WPM2 (`0x068E`, `0xFDB6`). Pages: [FEK2](fek2.md), [Cooling](cooling.md).

## 2026-11-15 test: Gebläsekühlung = Kessel 0x025B (21:37 local)
With the FEK emulation on, the maintainer switched "Gebläsekühlung" on and off on the control panel: the panel
wrote `0x025B` = 1, then 0, to the Kessel. Confirmed. Page: [Cooling](cooling.md). Source:
[capture](../raw/captures/2026-11-15-2137-geblaesekuehlung-on-off.log).

## 2026-11-15 test: compressor stops while the emulation is on
Emulation on 21:06 → compressor off at 21:07 (same pattern as the real FEK). Off until the emulation was switched
off at 21:40:36; the WPM2 took HK1 back at the 21:44 check. Conclusion: the heat pump probably waits for the FEK's
flow setpoint. Rule added to `AGENTS.md`: do not leave the emulation on unattended. Page: [FEK2](fek2.md).

## 2026-11-15 change: cooling settings as diagnostic entities
`property.h`: `GEBLAESEKUEHLUNG` (`0x025b`, confirmed) and `KUEHLEN_TBD_*` (`0xfdb2`, `0x06a4`, `0x0287`, `0x06a5`,
`0x06a6` Kessel; `0x068e`, `0xfdb6` WPM2). Read at boot and every 15 min; readable without the FEK. Values on
2026-11-15: 0, 0x0100, 1, 0, 0x8000, 0x8000, 20, 0x8000. Page: [Cooling](cooling.md).

## 2026-11-15 summary: what was learned today
- Port to upstream done; HA entities preserved; energy total fixed (new entity); OTA encrypted.
- CAN: message types (low nibble), short/long form, system messages, clock `0x0009`, nodes `0x100` (control panel)
  and `0x601` (room control logic, not the FEK).
- FEK: registration model (register `0x0900`, 8-min check, answer `0x0100`, one missed check releases HK1); the FEK
  is HK1 and sets the flow setpoint; full protocol captured.
- Emulation: accepted by the WPM2 with short-form frames; with the identification answer (`0x0199`) the "Kühlen" menu
  appears; the cooling settings live in the Kessel (Gebläsekühlung = `0x025B` confirmed).
- Open: flow setpoint for permanent emulation (decision), remaining cooling setting mapping, unknown FEK properties.

## 2026-11-15 test: FEK detection by software version (22:55 local)
Read `0x0199`/`0x019A` from HK1, Manager and Kessel without the FEK: all 391 / 10 (the WPM2's version). The FEK2
answered 416 / 3. So "HK1 ≠ Manager" detects a FEK. `0x0199`/`0x019A` = upstream `FET_SOFTWARE`/`FET_SOFTWARESTAND`
(`TBD_15` renamed). Source: [capture](../raw/captures/2026-11-15-2255-fek-detection-probe.log).
Pages: [Heating control](heating-control.md), [TTF07 C registers](ttf07c-registers.md).

## 2026-11-15 ingest: heating curve of the WPM2
Fitted to one week of HA history: `Vorlauf = Raumsoll + Steigung · (Raumsoll − Aussen) + 0.23 K` (rms 0.06 K); the
FEK's setpoint fits too. Source: [fit](../raw/2026-11-15-heating-curve-fit.md). Page: [Heating control](heating-control.md).

## 2026-11-15 change: heating control modes (decision 8: the ESP computes the setpoint)
Maintainer decision: implement both, FEK emulation with heating control and standalone (Eco/Komfort on the WPM2);
if a FEK is installed, it controls heating and the integration's heating settings are disabled. Firmware: select
"Heizungssteuerung" (Wärmepumpe / FEK Emulation, default Wärmepumpe), "Heizungssteuerung aktiv", "FEK installiert",
emulation parameters, flow setpoint every 3 min; the switches "FEK Emulation" and "FEK Emulation Raumwerte" are gone.
`wp_number` got the option `write_lock`. Flashed 23:02; detection verified ("Wärmepumpe"). The emulation with flow
setpoint is untested on the heat pump. Page: [Heating control](heating-control.md).

## 2026-11-16 change: deprecated "Energie Summe" removed
The HA Energy dashboard uses "Energie Summe kWh" (maintainer, checked in `.storage/energy`). `ENERGIE_SUMME` removed
from `yaml/ttf07_wpm2.yaml`, flashed 09:48. The orphaned HA entities from older firmware are gone as well.

## 2026-11-16 test: FEK emulation with flow setpoint (passed)
"Heizungssteuerung" = FEK Emulation at 09:54:23 with the defaults (setpoint 24.5 °C). Compressor on ~45 s later,
running steadily for 30 min; the panel shows Puffersolltemperatur 24.5 °C, the "Kühlen" menu and no errors;
presence checks answered. Confirms `0x0002` = flow setpoint. Cooling setpoints `0x0260`–`0x0262` still `0x8000`.
Source: [capture](../raw/captures/2026-11-16-0954-fek-emulation-flow-setpoint.log).
Pages: [Heating control](heating-control.md), [FEK2](fek2.md).

## 2026-11-16 decision: FEK emulation stays on
The maintainer keeps "Heizungssteuerung" = FEK Emulation permanently; the goal "replace the FEK with the house
sensors" is reached. Follow-up: recurrent check of the emulation in daily use (`TODO.md`).

## 2026-11-16 decision: upstream questions deferred, esp-idf follows upstream
Maintainer: the upstream PR and "one TTF07 file or two" are decided once the fork's open issues are resolved (moved to
future work in `TODO.md`). The framework follows upstream: switch from Arduino to esp-idf (next step in `TODO.md`).

## 2026-11-16 test: `0x100` = control panel (confirmed)
WW Komfort 52 → 53 → 52 on the WPM2 panel (10:46:21 / 10:47:42): `0x100` wrote `WW_KOMF_TEMP` (`0x0013`) short form to
the Kessel and read it back. The firmware ignores writes from `0x100` (no callback), so HA updated only on the next
read. Source: [capture](../raw/captures/2026-11-16-0954-fek-emulation-flow-setpoint.log). Page: [CAN bus](can-bus.md).

## 2026-11-16 change: the emulation answers reads addressed to HK1
The maintainer saw a spinning wheel and ~10 s lag on the panel: it read VORLAUFSOLLTEMP from HK1 (= the ESP) and
retried every ~6 s without an answer. The emulation now answers HK1 reads like the real FEK (form of the read kept).
Flashed 10:51; the WPM2 released the old registration at its 10:56 check, re-registered 10:56:19; panel lag gone.
Source: [capture](../raw/captures/2026-11-16-1051-hk1-read-answers.log). Page: [Heating control](heating-control.md).

## 2026-11-16 change: framework esp-idf (follows upstream)
Device file `/homeassistant/esphome/heatpump-ttf07c.yaml`: `framework: type: arduino` → `esp-idf`. Compiles without
warnings (OTA image 1.29 MB vs 1.33 MB, flash 70 %, RAM 45 %). Flashed by OTA at 11:02; boot without errors (ESPHome
2026.10.2), CAN and HA entities fine; emulation re-registered at 11:05:02 after the WPM2's 11:04 presence check.

## 2026-11-16 test: compressor cycling with the emulation
First stop under the emulation: compressor on 09:55–11:04:04 (69 min), stopped with Rücklauf 25.5 °C at setpoint
24.4 °C (+1.1 K), i.e. the WPM2's normal stop. Page: [Heating control](heating-control.md).

## 2026-11-16 test: Raumeinfluss is a FEK-internal setting
With the FEK attached, the WPM2 panel's "Heizkreis 1" shows only "Minimal Temperatur" (Komfort/Eco/Steigung/
Raumeinfluss are set on the FEK); the panel then reads KOMF_TEMP, ECO_TEMP, STEIGUNG_HK1, `0x4EA7` from `0x601`
(unanswered). Raumeinfluss 2 → 4 on the FEK (11:34:57): the FEK wrote `0x010F` = `0x0400` (little endian) to `0x601`
only, and answers HK1 reads with it; nothing to the Kessel/WPM2. The FEK applies it internally and sends only the
flow setpoint (`0x0002`). Effect not measurable (room 20.8 °C vs 21.0 °C set). Set back to 2.
Source: [capture](../raw/captures/2026-11-16-1123-real-fek-attached.log). Page: [FEK2](fek2.md).

## 2026-11-16 test: FEK detection with the real FEK attached (passed)
FEK plugged in 11:23:18 while emulating: detected by its registration, emulation stopped, "FEK installiert" 11:23:27;
the WPM2 accepted the FEK immediately; active check 416. Unplugged ~11:38: WPM2 released HK1 at 11:44, emulation
registered again at 11:45:02. Source: [capture](../raw/captures/2026-11-16-1123-real-fek-attached.log). Page: [Heating control](heating-control.md).

## 2026-11-16 change: control panel writes update HA at once
Core (`yaml/core.yaml`, `CallbackHandler::hasCallback`): a write from the node Bedienteil (`0x100`) to another node is
passed to that node's entity callback (e.g. WW Komfort → Kessel `WW_KOMF_TEMP`); without such a callback the frame is
handled as before (Bedienteil debug sensors `TBD_09`/`TBD_11` unchanged). Upstream unchanged (Bedienteil defaults to
`0x123`). FEK log: ANMELDUNG values named (`0x0800` presence check, `0x0900` FEK registration, `0x0100` FEK answer).
Flashed 11:57, emulation back 12:01:03; the panel path itself is untested (planned test in `TODO.md`).

## 2026-11-16 change: FEK protocol properties named
`property.h` (TTF_07_C): `KESSELSOLLTEMP` (`0x0002`), `VORLAUFISTTEMP_HK1` (`0x000f`), `SOLLWERT_MAX_HK1` (`0x0028`),
`MINTEMP` (`0x4ea7`); the log shows these names instead of UNKNOWN. Flashed 12:07. `0x006E` differs between the
two FEK captures (`0x0100` / `0x0200`), planned test in `TODO.md`. Page: [FEK2](fek2.md).

## 2026-11-16 ingest: `0x601` configuration block and `0x0052` = compressor flag
`0x601` sends a configuration block to HK1 about every 7 min, independent of registrations; some blocks arrive
incomplete (frames missing, not a firmware filter). `0x0052` in that block is `0x0100` while the compressor runs and 0
while it is off (4 of 4 transitions: 09:55, 11:04, 12:04), and is sent on its own at the change. Source:
[raw](../raw/2026-11-16-0x601-config-block-and-0x0052.md). Pages: [FEK2](fek2.md), [CAN bus](can-bus.md). Also updated: [Device](device-heatpump-ttf07c.md) (esp-idf,
energy dashboard, heating control selected) and [Firmware history](firmware-history.md).

## 2026-11-16 test: control panel writes reach HA at once (passed)
WW Komfort 52 → 53 (12:31:57.674) and back (12:32:27.431) on the WPM2 panel: "Control panel wrote WW_KOMF_TEMP to
Kessel", the number updated in the same millisecond, HA ~0.1 s later. Source: [capture](../raw/captures/2026-11-16-1226-panel-writes-and-fek-modes.log).

## 2026-11-16 test: FEK Betriebsart vs `0x0058`/`0x006E`
Real FEK attached 12:33:33–~13:04, Betriebsart switched on the FEK: `0x0058` = active phase (`0x0200` Komfort,
`0x0100` Eco/Aus), sent at once on change; Aus = 5.0 °C; `0x006E` stays `0x0200` in all modes (meaning still open).
The emulation always sends `0x0058` = `0x0200`, also in Eco: to be fixed. Emulation registered again 13:04:52.
Source: [capture](../raw/captures/2026-11-16-1226-panel-writes-and-fek-modes.log). Page: [FEK2](fek2.md).

## 2026-11-16 change: emulation sends the phase, software version sensors
`0x0058` from the emulation follows "FEK Emulation Betriebsart" (`0x0200` Komfort, `0x0100` Eco) and the block is
sent at once on a change, like the FEK2. New diagnostic text sensors "Software WPM2" (391.10) and "Software HK1"
(416.03 (Emulation) while emulating; "(WPM2)"/"(FEK)" otherwise); `FET_SOFTWARESTAND` is read with the version.
Flashed 13:22; emulation registered 13:29:04. Tested 13:32:54 Eco (via HA): at once flow setpoint 22.6 °C,
`0x0058` = `0x0100`, room setpoint 20.0 °C; 13:33:10 back to Komfort: 24.3 °C, `0x0200`, 21.0 °C. Software sensors:
WPM2 391.10, HK1 416.03 (Emulation). Source: [capture](../raw/captures/2026-11-16-1322-phase-and-versions.log).

## 2026-11-16 ingest: TBD_* values identified from the HA history
7 days of HA history, correlation and value comparison ([analysis](../raw/2026-11-16-tbd-history-analysis.md)): `TBD_TEMP_01` (`0xfdf3`) = Vorlauf Ist
WP, `TBD_19` (`0xfdf4`) = Rücklauf Ist × 10 (duplicates of existing entities); `TBD_02` (`0xfe1c`) = source pump PWM,
`TBD_08` (`0xfe1b`) = charging pump PWM (inverted, 100 = off; matches 100 − Pumpenleistung), `TBD_06` (`0xfe1d`) =
hot water changeover valve. `TBD_TEMP_03` (`0xfe09`) unclear. `TBD_04/07/09/10/11/12/13` were constant all week.
Page: [TTF07 C registers](ttf07c-registers.md).

## 2026-11-16 change: identified TBD values named (maintainer decision)
Duplicates removed as entities, named in `property.h` only: `VORLAUFISTTEMP_MFG` (`0xfdf3`), `RUECKLAUFISTTEMP_MFG`
(`0xfdf4`). New diagnostic sensors (from the WPM2's command to the MFG): "Quellenpumpe PWM", "Ladepumpe PWM",
"Umschaltventil Warmwasser" (%). Old entities `TBD_TEMP_01`, `TBD_19`, `TBD_02/06/08_*` are orphaned in HA. Flashed
14:09; at 14:17 the compressor ran: Quellenpumpe 33 %, Ladepumpe 57 %, Umschaltventil 0 %.

## 2026-11-16 change: thermostat for the FEK emulation
New external component `wp_climate` (fork): a climate entity built from existing entities. "Thermostat FEK
Emulation": presets comfort/eco ↔ "FEK Emulation Betriebsart", target ↔ the active preset's temperature number,
current temperature/humidity from HA, action from Heizbetrieb. Device file: `external_components` lists
`wp_climate`. Flashed 14:21; tested via HA: preset eco/comfort and target 21.5/21.0 set the select and number.
Page: [Heating control](heating-control.md).

## 2026-11-16 change: Wärmepumpe dashboard redesigned
Maintainer request: five tabs (Übersicht, Energie, Verlauf, Einstellungen, Diagnose) instead of one page; thermostat
"Thermostat FEK Emulation" with preset buttons on top; the old "Energie Summe" replaced by "Energie Summe kWh"; all
122 entities checked to exist. Page: [Device](device-heatpump-ttf07c.md).

## 2026-11-16 change: hot water thermostat
"Thermostat Warmwasser" (`wp_climate`): presets comfort/eco ↔ Programmschalter (WPM2), target ↔ `WW_KOMF_TEMP` /
`WW_ECO_TEMP`, current `SPEICHERISTTEMP`, action Warmwasserbereitung. `wp_climate` now treats any select option other
than Komfort/Eco as "no preset": the target then shows the new optional `setpoint` sensor (here `SPEICHERSOLLTEMP`)
and target writes are refused (before, such options were shown as Komfort). Flashed 15:35; in HA preset eco, target
45 (= WW Eco = Speicher Soll), current 44, idle; nothing written. Thermostat card added to the dashboard (Übersicht,
Warmwasser). Preset/target round trips not tested (they write to the heat pump). Page: [Device](device-heatpump-ttf07c.md).

## 2026-11-16 test: Kühlen menu mapped
`/test-sensor` 17:45–17:59 with the emulation on, values changed on the panel one at a time and set back. All settings
are on the Kessel and written there by the panel (`0x100`): `0x06A4` = Kühlen EIN/AUS, `0x0287` = Kühlmodus
(0 passiv, 1 aktiv), `0x025F` = Flächenkühlung (firmware `KUEHLEN_AKTIVIERT`), `0x0260` Vorlaufsoll Kühlen, `0x0261`
Raumsoll Kühlen, `0x0262` Hysterese Vorlauf Kühlen (all `et_dec_val`, 0.1 steps). `0x0260`–`0x0262` now answer
(17.0 °C, 22.5 °C, 1.5 K) instead of `0x8000`. `0xFDB2` did not react. Two Hysterese writes from the panel were
ignored by the Kessel (no error frame). All values set back. Verdict: confirmed. Page: [Cooling](cooling.md);
[capture](../raw/captures/2026-11-16-1745-kuehlen-menu-mapping.log).

## 2026-11-16 test: Programmschalter positions
Programmschalter turned through all positions on the panel at 18:01. The panel (`0x100`) writes `0x0112` to the
Manager (`0x480`), which echoes the value back to the panel within ~1 s. Values seen: `0x0500`, `0x0000`, `0x0400`,
`0x0300`, `0x0200`, `0x0100`, back to `0x0400` (Eco). All six match the firmware's TTF07 C map (Notbetrieb,
Bereitschaft, Programm, Komfort, Eco, Warmwasser); the HA select followed (Eco at 18:01:32). Verdict: confirmed.
[capture](../raw/captures/2026-11-16-1801-programmschalter-positions.log).

## 2026-11-16 test: real FEK plug-in and FEK settings
Emulation released (Heizungssteuerung → Wärmepumpe 18:04:13, unanswered WPM2 check 18:08:00), real FEK registered
18:14:10. `0x006E` went `0x0200` → `0x0100` about 60 s after registration (opposite of the 12:33 plug-in). Raumeinfluss
2 → 3 → 2 on the FEK: sent at once as `0x010F` to `0x601`; `0x0029`/`0x002A` unchanged. Steigung, Eco, Komfort
changed on the FEK: no frame; visible only in HK1 read answers and in the next periodic block (Raumsoll `0x0012`,
flow setpoint `0x0002`). All set back. FEK unplugged after 18:40 (the 18:40:00 check was still answered), 18:48:00
check unanswered, emulation back on at 18:49:08. Page: [FEK2](fek2.md).

## 2026-11-16 change: cooling entities
`property.h` (TTF07 C): `KUEHLEN_EIN` (`0x06a4`), `KUEHLMODE` (`0x0287`), `FLAECHENKUEHLUNG` (`0x025f`, was
`KUEHLEN_AKTIVIERT`), `GEBLAESEKUEHLUNG` now `et_bool`; `KUEHLEN_TBD_06A4/0287` removed. Device file: switches "Kühlen",
"Kühlmodus Aktivkühlung", "Flächenkühlung", "Gebläsekühlung"; numbers "Kühlen Vorlauf Soll Temperatur" (15–25),
"Kühlen Raum Soll Temperatur" (18–30), "Kühlen Hysterese" (0.5–5 K, step 0.1, was step 1); the old sensors for the
setpoints are gone. Templates `wp_number`/`wp_switch`: new opt-in `read_back` (read 3 s after a write). Flashed 19:07;
values matched the panel; HA write Vorlaufsoll 17.0 at 19:11:25, read back 17.0 at 19:11:28 (it was 16.9 after an
accidental panel write at 17:55). HA removed the old entities itself; dashboard section Kühlen (Einstellungen) and
the Diagnose card updated. Emulation registered again at 19:12:25. Page: [Cooling](cooling.md).

## 2026-11-16 change: one heating thermostat for all heating controls
`wp_climate`: optional `alternative` source (select + Komfort/Eco numbers), `use_alternative` and `writable`
lambdas. "Thermostat Heizung" replaces "Thermostat FEK Emulation": Wärmepumpe → Programmschalter + HK1 Komfort/Eco,
FEK Emulation → emulation Betriebsart + Komfort/Eco, FEK installiert / Prüfung läuft → read only. Flashed 19:35;
checked "Prüfung läuft" (eco, read only) and "FEK Emulation" (comfort, 21.1; target write went to the emulation's
Komfort number). Dashboard card switched. Wärmepumpe mode not tested yet. Page: [Heating control](heating-control.md).

## 2026-11-16 change: read_back option removed again
`sendData()` already reads every written value back after 10 s, so the templates' `read_back` (3 s) was redundant
(seen at 19:11: reads at +3 s and +10 s). Removed from `wp_number`/`wp_switch` and the cooling entities.

## 2026-11-16 change: CAN nodes as diagnostic entities
`ttf07_wpm2`: frames per minute per sender CAN ID (Kessel, HK1, Manager, MFG, Bedienteil, `0x601`, `0x680`, unknown)
and "CAN unbekannte Sender" (IDs with time last seen). "Last seen" of known nodes = HA history of the rate (no
separate entities). Flashed 19:56; first values: Manager 105, MFG 99, Kessel 28, Bedienteil 17, `0x680` 1, HK1 1,
unknown 0. Dashboard Diagnose › CAN IDs. Page: [CAN bus](can-bus.md).

## 2026-11-16 change: dashboard example for other TTF07 C users
`dashboard-examples/ttf07c/`: `dashboard_warmepumpe.yaml` (the Wärmepumpe dashboard, 5 views, 132 entities),
README (how to import, entity IDs) and `export_dashboard.py`. Entity IDs are normalized to what a fresh install with
the friendly name "Wärmepumpe" gets (`<domain>.warmepumpe_<name>`; this installation mixes `hwr_warmepumpe_`,
`heatpump_` and unprefixed IDs); the house temperature group is the placeholder `sensor.HOUSE_TEMPERATURE`.

## 2026-11-16 decision: community analytics checked (open)
`yaml/features/analytics.yaml` needs nothing more from `ttf07_wpm2.yaml` (`heat_pump_variant` exists, template
entities are whitelisted by default). What it would send is listed in `TODO.md` (open decision); not enabled.

## 2026-11-16 test: Thermostat Heizung in mode Wärmepumpe
Heizungssteuerung → Wärmepumpe 20:31:24, WPM2 check 20:32:00 unanswered. Thermostat: preset eco (Programmschalter),
target 19.5 = HK1 Eco; HK1 read: Komfort 23.0, Eco 19.5. Target write 19.5 → `ECO_TEMP` to HK1, read back 19.5.
Back to FEK Emulation 20:35:05 (registered, flow setpoint 25.0 °C). Verdict: confirmed. Page:
[Heating control](heating-control.md).

## 2026-11-16 decision: community analytics with all entities, not live yet
Maintainer: join with all entities, prepare only. `heatpump-ttf07c.yaml` (HA config repo) has the analytics line
commented out with the placeholder district; a copy with it enabled compiled (20:31), then the real config was
rebuilt so no analytics firmware is left in the build directory. What it sends: plain MQTT (no TLS, shared
credentials, retained) to `oneesp32torulethemall.freeddns.org`: MAC-hash ID, variant, district, git hash; every
15 min all whitelisted sensor values; every change of numbers, switches, selects, binary sensors; every 12 h a
GitHub version check. Not sent: FEK emulation, house values, CAN rates, debug/TBD sensors.

## 2026-11-16 change: community analytics live; firmware flashed
Maintainer: go live with district Bielefeld. `heatpump-ttf07c.yaml`: analytics line enabled. Flashed 20:44 (also
contains the `read_back` removal): "Analytics MQTT Connected" on, first update 20:44, "Github" off (no newer
upstream version). Emulation registered again 20:48 (thermostat comfort 21.1).

## 2026-11-17 change: CAN node rates per hour
"CAN <node> Frames" now count frames per hour: sum of the last 60 minutes (ring buffer of 60 × 8 counters,
~1 KB), updated every minute, unknown for the first 10 minutes after boot, extrapolated to one hour until 60
minutes of data exist. Unit `1/min` → `1/h`, names and entity IDs unchanged. Flashed 08:15; first values 08:26
(10 min, extrapolated): Manager 5405, MFG 4790, Kessel 2390, Bedienteil 1010, `0x601` 135, HK1 20, `0x680` 10,
unknown 0. Emulation registered again 08:18. Dashboard card title "Frames pro Stunde, letzte 60 min" (HA and
`dashboard-examples/`). Page: [CAN bus](can-bus.md).

## 2026-11-17 ingest: TBD_TEMP_03 and the constant TBD values
40 h of HA history ([analysis](../raw/2026-11-17-tbd-temp-03-and-constants.md)). `TBD_TEMP_03` (`0xfe09`, MFG)
steps with the compressor within 5 s (+0.3 K heating, +1 K hot water) and back within 20 s at stop, and does not
follow the outdoor temperature: not the installation room; probably measured on the MFG electronics (unconfirmed).
`TBD_04/07/09/11/12/13/17/18` constant over heating and hot water. `TBD_10` = `0x00FE` = the presence system
message index (value `0x0100`), not a setting. No NHZ run in 40 h. The orphaned HA entities of the old TBD names
(`TBD_TEMP_01`, `TBD_19`, `TBD_02/06/08_*`) are already gone from the entity registry. Page:
[TTF07 C registers](ttf07c-registers.md).

## 2026-11-17 ingest: community analytics dashboard
The analytics broker host serves the community Grafana (anonymous, Grafana 12.4, dashboard "Test",
`/d/advz2wx/test`, variable `device_hash`). This device: hash `43d17174`. Its panels query upstream's entity names
(`VERDICHTER_STARTS`, `EL_ENERGIEAUFNAHME_HEIZ_SUMME_KWH`, `WAERMEERTRAG_*_TAG_SUMME_KWH`, `device_identity`, a
status sensor such as `NE_STUFE_WW`); this fork publishes under its German display names, so the comparison panels
miss it (TODO item 3). Page: [Device](device-heatpump-ttf07c.md).

## 2026-11-17 change: analytics names and TBD_10 (compiled, not flashed yet)
Analytics: `getAnalyticsNames()` (`util.h`) maps whitelisted entities to the name published in the 15-min analytics
update; the sensor templates fill it with the optional `analytics_name` (default = the entity id; only when built
with `ANALYTICS`). `ttf07_wpm2.yaml` overrides the daily sums (`EL_ENERGIEAUFNAHME_*_SUMME_KWH`,
`WAERMEERTRAG_*_TAG_SUMME_KWH`), the totals (`*_SUMME_MWH`) and `COP_HEIZ_TAG`, so 43 sensors now go out under
upstream's names (checked in the generated `main.cpp`). Events of numbers, switches and binary sensors already used
the property names. `TBD_10` → `SYSTEM_PRAESENZ` (`0x00fe`), entities `TBD_10_Kessel/Manager/MFG` removed.
Compiled 08:40; flash waits for the end of the passive capture (11:15).

## 2026-11-17 ingest: passive capture, first hour (08:15–09:16)
No compressor run yet, so `0x0052` stayed 0. Values unchanged: `0x601` → HK1 `0x0010` = 2, `0x0056`/`0x0057` = 0,
`0x005A` = `0x0200`. New: the Kessel writes its own block to `0x379` (`0x0010` = `0x0051` = 81, `0x005A` = `0x0200`,
`0x0A20`). Heating-circuit pump runs without compressor at 08:30, 08:51, 09:13: Kessel `0x0A20` = `0x0020` (upstream
bit 5) together with WPM2 `0x4e5e` = `0x0001` (bit 0). Page: [Betriebsstatus](betriebsstatus.md).

## 2026-11-17 ingest: passive capture, compressor start 09:23
Kessel `0x0A20` and WPM2 `0x4e5e` agree on source pump (upstream bit 8 / bit 6), heating-circuit pump (5 / 0),
charging pump (6 / 7) and compressor (3 / 14); `0x0A20` bit 2 also comes on with the compressor (unknown upstream).
`0x0052` (`0x601` → HK1) went `0x0100` at 09:25:04, ~2 min after the compressor start. `0x0010`, `0x0056`,
`0x0057`, `0x005A` unchanged. Pages: [Betriebsstatus](betriebsstatus.md), [FEK2](fek2.md).

## 2026-11-17 ingest: passive capture, compressor stop 10:37
Compressor off 10:37:40: `0x0A20` bits 3 and 2 off together, then bit 6; `0x4e5e` bit 14, then 7, then source pump
(10:38:39). `0x0052` → 0 at 10:42:04, the next scheduled send of `0x601` (sends at :35:05, :37:02, :42:04 …, two
per 7 min); the 09:25:04 change was also the first send after the start. So `0x0052` follows the compressor (6 of 6),
with the send schedule as the only delay. A hot-water run would separate "compressor" from "HK1 heat demand".
Pages: [FEK2](fek2.md), [Betriebsstatus](betriebsstatus.md).

## 2026-11-17 change: analytics names and TBD_10 flashed
Flashed 11:15 after the passive capture ended. Log: no errors (the analytics MQTT had a DNS resolve error at boot
and connected on retry, as at 08:15); "Analytics MQTT Connected" on 11:16; no heat pump entity unavailable; the
`TBD_10_*` entities are gone from the HA registry; emulation registered again 11:21. Whether the community panels
now show this device is not verified (TODO item 3).

## 2026-11-17 ingest: passive capture 08:15–11:15, summary
42,719 frames, no errors, no unknown senders ([excerpt](../raw/captures/2026-11-17-0815-passive-0052-status-words.log)).
One compressor run (heating, 09:23:11–10:37:40), five pump-only runs of the heating circuit, no hot water, no NHZ.
`0x0052` followed the compressor (see above). `0x601` → HK1 `0x0010` = 2, `0x0056`/`0x0057` = 0, `0x005A` =
`0x0200` throughout. The Kessel's own block to `0x379` (51 times, about every 3.5 min): `0x000A` = 4363 (`0x110B`),
`0x0010` = 81, `0x0053` = 0, `0x005A` = `0x0200`, `0x005E` = 0, `0x0073` = 0, `ANLAGENFROST` `0x0A00` = 40
(4.0 °C), `0x0A20` on change, plus `SPEICHERISTTEMP`, `RUECKLAUFISTTEMP`, `AUSSENTEMP` (all constant except the
temperatures and `0x0A20`). `0x379` is not a known node; it is probably the Kessel's broadcast address for HK
values (meaning open).

## 2026-11-17 test: backup heater (NHZ) in Notbetrieb
Maintainer's request: Programmschalter → Notbetrieb 11:43:32 (`0x0000`, echoed to the panel), emulation Vorlauf min
32 °C 11:59:14 (heat demand). NHZ fuses off at first: NHZ1 12:01:06, NHZ2 12:03:04, NHZ1+2 12:05:03 in both status
words, no error. Fuses on ~12:14:20: +8.95 kW; fuse 1 off 12:16:31–12:17:31: −3.0 kW on phase A only. Demand met
12:17:57 (buffer 33.4 °C). Vorlauf min 35 °C at 12:19:52, but the buffer was already at 36.6 °C (no new demand);
the maintainer then switched the compressor and NHZ fuses off to let it cool. Verdict: NHZ bits confirmed, "NHZ3" =
NHZ1 + NHZ2, upstream's `0x0A20` bits 0/1 right; `0x0052` = HK1 heat demand (on without compressor). Thermometer next
to the heat pump: 24.3 °C vs. `TBD_TEMP_03` 18.7 °C (not the room). Pages: [Betriebsstatus](betriebsstatus.md),
[FEK2](fek2.md), [TTF07 C registers](ttf07c-registers.md).

## 2026-11-17 change: Notbetrieb test paused, settings back
Maintainer's request: Programmschalter → Eco 12:34:47 (WPM2 echoed `0x0400` to the panel 12:34:48), emulation
Vorlauf min → 15 °C; the emulation sent the new flow setpoint 26.8 °C at 12:36:54 (it recalculates about every 2
min). Compressor and NHZ fuses still off (maintainer). Open: NHZ stage powers and the compressor error test (TODO).

## 2026-11-17 test: compressor start without power
Compressor and NHZ fuses off (maintainer), Eco. Source pump 13:10:06, compressor on 13:10:36 in both status words,
off again exactly 60 s later (13:11:36) with the heat demand; at that moment the Manager sent `0x1388` (`TBD_12`)
= 21 to the panel (0 before). The panel showed "Fehler / Keine Leistung". `FEHLERMELDUNG` stayed 0. Verdict:
`0x1388` is very likely the WPM2's error number, 21 = Keine Leistung. Also: `0x0009` in the Kessel's `0x379` block is
the time of day. Pages: [Betriebsstatus](betriebsstatus.md), [TTF07 C registers](ttf07c-registers.md),
[CAN bus](can-bus.md).

## 2026-11-17 test: error 21 cleared by a power cycle; WPM2 boot scan
The panel could not acknowledge "Keine Leistung". Fuses back on ~13:27, error number still 21 at 13:14/13:18/13:23
(no start attempt). Maintainer power-cycled the heat pump ~13:30: `0x1388` = 0 at 13:31:29, emulation registered
at the first presence check 13:31:17, Programmschalter Eco, no entity unavailable. Boot scan: nodes register with
`0x00FD` = `0x0900` (`0x100`, `0x480`, `0x180`, `0x601`, `0x602`), checks `0x0800` on `0x301`, `0x680`, `0x302`,
`0x528`, `0x546`. Pages: [CAN bus](can-bus.md), [TTF07 C registers](ttf07c-registers.md).

## 2026-11-17 test: compressor runs again after the power cycle
Heat demand 13:34: source pump 13:34:05, compressor 13:34:35 (both status words), still running at 13:36:10 with
~840 W ("Leistung Verdichter"), no error number (`0x1388` 0). "Verdichterstarts" 24196 → 24197: the failed start at
13:10 without power was not counted. Capture stopped 13:36.

## 2026-11-17 test: NHZ stage powers
Maintainer's request, all fuses on: Notbetrieb + Vorlauf min 35 °C 13:48:41, back to Eco + 15 °C 13:59:01 (Eco
echoed 13:59:09). Stage 1 13:49:05 (+2.96 kW, phase A), stage 2 13:51:04 (+2.95 kW, phase B, A stays on), stage 3
13:53:03 (+2.97 kW, phase C), off 13:54:47 at 35.3 °C buffer. The NHZ bits are a stage number (1, 2, 3 = 3, 6,
9 kW), not separate heaters. Planned test 4 (NHZ) closed; the error-number part stays as TODO item 4. Page:
[Betriebsstatus](betriebsstatus.md).

## 2026-11-17 change + ingest: error number entity and the error list
Maintainer's decision: `TBD_12` → `FEHLERNUMMER_WPM`, HA "Fehlernummer" (`sensor.hwr_warmepumpe_fehlernummer`);
flashed 14:17, HA dropped the old entity. Then the maintainer opened Diagnose > Fehlerliste (14:19:20) with a capture
running and photographed all 10 pages: the panel writes `0x0B9A` = start index to the Manager, which streams the 20
entries as writes `0x0B9A`–`0x0BA3` (index, code, ?, minute, hour, day, month, year). Codes: 21 Keine Leistung, 22
Niederdruck, 130 Fühlerbruch E 130, 8036/8039/8040/8041 = TO P SOL / PU SOL / VENTIL / DHC MFG. Reads of these
addresses return `0x8000`. New page: [Errors](errors.md).

## 2026-11-17 change: error list in HA
Maintainer's decision (option a). Test 14:33: one write of `0x0B9A` = 0 from the ESP; the Manager answered entry 0
to the panel within 20 ms, nothing else changed. Test 14:44: the Manager has a cursor (each request = next entry,
resets after ~1 min idle). Firmware: properties `FEHLERLISTE_*` (`0x0b9a`–`0x0ba3`), script `fehlerliste_lesen`
(5 requests, second pass after 2 min if fields are missing), text sensors "Fehlerliste", "Letzter Fehler", "Fehler
aktuell". Flashed 14:36, 14:40, 14:45, 14:52; result 14:48: all 5 entries, one day field missed. AGENTS.md: the
request write is allowed. Page: [Errors](errors.md).

## 2026-11-17 test: real FEK, settings ranges and replug
FEK plugged in 14:46:21 (registered at once, emulation off, "FEK installiert"). Menus photographed: no setting
reads 10 or 30. Ranges: Komfort max 30.0 °C (matches `0x002A`), Eco min 5.0 °C, Raumeinfluss 0–20; set back to 21.0 /
19.9. Replugs 15:39:23 and 15:45:31: `0x006E` `0x0200` → `0x0100` after ~50 s both times. Page: [FEK2](fek2.md).

## 2026-11-17 change: `0x0052` named
`FEK_TBD_0052` → `HEIZ_ANFORDERUNG_HK1` in `property.h` (HK1 heat demand, evidence in [FEK2](fek2.md)); log names
only, no entity. Compiled 16:47, not flashed yet.

## 2026-11-17 read: `WW_ANFORDERUNG` `0x4eb2`
Read from Kessel, Manager and HK1 at 16:50: all answer `0x8000` (no value), so the TTF07 C has no such property
under this address; no entity. Page: [TTF07 C registers](ttf07c-registers.md).

## 2026-11-17 test: Komfort minimum, FEK unplugged, emulation back
FEK Komfort goes down to 5.0 °C (like Eco), so `0x0029` (10) is not the room setpoint minimum. Komfort set back to
21.0, FEK unplugged ~16:53. The ESP's presence check found HK1 free at 16:58:13 and registered as FEK on `0x301`;
`0x601` sent its configuration block at 16:58:24 and the emulation sends a flow setpoint again (25.5 °C at 9.9 °C
outdoor). TODO planned test 5 closed. Pages: [FEK2](fek2.md);
[capture](../raw/captures/2026-11-17-1653-fek-unplug-emulation.log).

## 2026-11-17 check: `TBD_TEMP_03` again, statistics repairs
Zigbee thermometer next to the heat pump 23.9 °C, `TBD_TEMP_03` 18.7 °C (17:10, compressor heating at 0.84 kW):
second check, still ~5 K below the room, so not the installation room. The unit change of the 8 CAN rate sensors
(1/min → 1/h) raised 8 "unit changed" repairs in HA; their old long-term statistics were cleared (maintainer's go)
and `recorder/update_statistics_issues` removed the repairs.

## 2026-11-17 change: `0xfe09` renamed `TBD_INTERNAL_HEATPUMP_TEMP`
Web search (Elster tables, forums) found nothing on `0xfe09`. Not the brine: Quelle Ist 6.4 °C while `0xfe09` read
18.7 °C, and brine cools when the compressor starts while `0xfe09` warms. Property and YAML id renamed
`TBD_INTERNAL_HEATPUMP_TEMP`; the display name stays `TBD_TEMP_03` so the HA entity keeps its ID and history.
Compiled, not flashed. Page: [TTF07 C registers](ttf07c-registers.md).

## 2026-11-17 change: flash, HA name, handover folded into TODO
Flashed 17:28 (`HEIZ_ANFORDERUNG_HK1`, `TBD_INTERNAL_HEATPUMP_TEMP`); all 98 entities back, emulation registered
again 17:30:50. HA entity `sensor.heatpump_tbd_temp_03` renamed in the registry to "TBD_INTERNAL_HEATPUMP_TEMP"
(ID and history unchanged). The session handover's open points went into TODO items 4 and 5; the file is deleted.

## 2026-11-17 test: expert code on the panel
Code 1000 accepted 17:36; no frame carries the code (checked locally by the panel, access level invisible on the
bus). Browsing the expert menus: the panel polls `0x06AE` (Manager) every ~2 s, writes only `TBD_09` = 1 and the
error list requests, and reads ~40 addresses, 20 of them unknown, plus a new node `0x514` (`0xC32F`, no value).
[raw](../raw/2026-11-17-fachmann-code.md). Next: guided pass, one page at a time, to name them.

## 2026-11-17 test: expert menus page by page, relay test
The maintainer went through all Info and Diagnose pages (code 1000) with photos; the panel's reads were matched live.
Findings: the manager is a **WPM3i** (Busteilnehmer: WPM3i 391-10, FES 417-07, FEK 416-03 = the ESP's emulation,
MFG 18); `TBD_17` = Festwertsolltemperatur (AUS); Reststillstand = Manager `0x0668` (min); room values the WPM3i
uses (`0x4E64`, `0x4E66`, `0x069E`, dew point `0x0264`); NHZ flow `0x06A0`; Bivalenz/Einsatzgrenze `0x01AC`–`0x01AF`;
NHZ energy totals use `0x0927`/`0x0923` as kWh part (not upstream's `0x0928`/`0x0924`); `0x0805` is "NHZ 1/2". In the
relay test the panel writes `0x0693` (active) and `0x067A` (`TBD_16`, relay number 1–12) to the Kessel; the status
words confirmed `0x4e5e` bits 1–3, 9, 13 and `0x0A20` bit 9. NHZ relays ran only seconds, without heating.
[raw](../raw/2026-11-17-expert-menus.md), [first pass](../raw/2026-11-17-fachmann-code.md). Pages:
[Betriebsstatus](betriebsstatus.md), [CAN bus](can-bus.md), [TTF07 C registers](ttf07c-registers.md). TODO: 1, 7, 8,
new 19 (sensors), 20 (WPM3i naming).

## 2026-11-17 change + test: WPM3i rename, Einstellungen > Programme
Renamed WPM2 → WPM3i (maintainer's decision): `yaml/ttf07_wpm2.yaml` → `yaml/ttf07_wpm3i.yaml` (include in
`heatpump-ttf07c.yaml` updated), comments, docs, skill and dashboard example; entity display names "Software WPM2"
and "TBD_07_WPM2" kept (entity IDs). Not flashed yet.
Einstellungen > Programme browsed 18:03–18:18 ([raw](../raw/2026-11-17-expert-menus.md)): Warmwasserprogramm fully
decoded (Kessel `0x1710`–`0x1772` per day, groups `0x1780`/`0x1790`/`0x17A0`; 15-min steps, `0x8080` = empty) with
test windows set by the maintainer on the panel and, on the maintainer's go, written by the ESP; Partyprogramm
`0xFDBF`, Aufheizprogramm `0x011A` and its parameters `0x01BA`–`0x01BE`, Ferienprogramm `0x011B`–`0x0120`. The
Heizprogramm is hidden while the FEK emulation owns HK1. Everything set back (Warmwasserprogramm empty, Aufheiz AUS,
Party 0 h). Page: [TTF07 C registers](ttf07c-registers.md).

## 2026-11-17 change: Reststillstand sensor, Warmwasserprogramm texts, flash
New entities (flashed 18:26, also the WPM3i rename): sensor "Verdichter Reststillstand" (Manager `0x0668`, min, every
60 s) and 7 texts "Warmwasserprogramm Montag" … "Sonntag" (Kessel `0x1710` + `0x10` · day + window; format
"06:00-08:00, 17:00-18:30", "-" = none; read 90 s after boot and every 15 min; a change in HA writes only the windows
that differ and reads the day back). An HA schedule helper can't be fed by ESPHome, so the program is exposed as
texts per day. Page: [TTF07 C registers](ttf07c-registers.md).

## 2026-11-17 change: expert-menu entities, register table
Flashed 18:50/18:52: Taupunkt, Raum Ist/Soll/Feuchte WPM3i, Bivalenztemperatur Heizen/WW, Einsatzgrenze Heizen/WW and
Festwertsolltemperatur (text, "Aus" for `0x9000`), Wärmeertrag NHZ Heizen/WW (TTF07 C kWh parts), Partyprogramm,
Aufheizprogramm (binary), Ferienprogramm (text); `TBD_15`/`TBD_16`/`TBD_17` entities removed (`TBD_16` = relay test
number, `TBD_17` = Festwert); HA names "Software WPM3i", "TBD_07_WPM3i" (registry only). Fixed: negative float → uint16
cast gave −2457.6 for `0x9000`. New page [TTF07 C registers](ttf07c-registers.md): one table of all registers with how each
is confirmed.

## 2026-11-17 change: dashboard, registers as source of truth
HA dashboard `dashboard-warmepumpe` (live, backup in the scratch directory) and `dashboard-examples/ttf07c` updated:
Übersicht tile "Verdichter Sperrzeit"; Energie: Wärme Heizstab Heizen/Warmwasser; Einstellungen: Bivalenz,
Einsatzgrenze, Festwert in "Anlage", new sections "Warmwasserprogramm" (7 texts) and "Programme" (Party, Aufheiz,
Ferien); Diagnose: new section "Raum (wie die WPM3i ihn sieht)" with Taupunkt and Reststillstand; removed TBD_16/17;
labels WPM3i. `AGENTS.md` names [TTF07 C registers](ttf07c-registers.md) the source of truth for registers. TODO planned test 20:
Festwert/Einsatzgrenze `0x9000` vs `0xA000`.

## 2026-11-17 change: registers in one place
New page [TTF07 C registers](ttf07c-registers.md) (type column, conventions, naming vs upstream) replaces
`ttf07c-properties.md` and `registers.md` (both deleted; links updated, also in older log entries). The register
tables in [Cooling](cooling.md), [FEK2](fek2.md) and [Errors](errors.md) were moved into it; those pages now link.
`AGENTS.md`: registers are listed only there. Dashboard backups in the scratch directory deleted. TODO: blocker 21
(Heizprogramm registers need the emulation off), future work 22 (analytics for new entities).

## 2026-11-17 test: NHZ flow temperature, two sources
Kessel `0x06A0` (the panel's "Vorlaufisttemperatur NHZ") and MFG `0xFDF5` (HA "Vorlauf Ist NHZ") read identical
values (25.8–25.9 °C, 19:23). `0x06A0` is the Kessel's copy of the MFG value, like `0xfdf3`/`0x06a1`; no second
entity. `0xFDF5` is now "panel"-confirmed in [TTF07 C registers](ttf07c-registers.md); TODO item 19 closed.

## 2026-11-17 test: Einstellungen pass 2 (Programme done before; Heizen, Warmwasser, Kühlen, Inbetriebnahme)
Browsed with photos 18:18–20:28; every change the maintainer made was set back and confirmed on the bus. Details:
[expert settings](../raw/2026-11-17-expert-settings.md), panel traffic in `raw/captures/2026-11-17-2018-*`. Newly named:
`0xFDB2` Pumpenzyklen, `0x068F` Pufferbetrieb (TBD_18 solved), `0x0028` Maximale Rücklauftemperatur, `0x01E8`
Maximale Vorlauftemperatur, `0x01C0` Festwertbetrieb, `0x0679` Heizkreis optimal, `0x0A00` Frostschutz, Sommerbetrieb
(`0xFDB4` EIN, `0x01BF` 16.5 °C, `0xFDB3` Gebäudedämpfung), WW-Korrektur `0x0263`, WW Lernfunktion `0x027E`,
Kombispeicher `0x070D`, Antilegionellen `0x0101`, `0x0288` Dynamik aktiv, `0x0645` Kühlung change notice, Quick start
`0x0669`, sensor offsets `0x0658`–`0x065A`, source medium list `0xFDAE` (0–8), Sommerzeit `0xFDDE`–`0xFDE1`.
Open: `0x0135`, `0xFDBA`, `0xFDB9`, `0x0181`, `0x0705`, `0x059F`/`0x05A0`; language not on the bus (`0x4E8B` stayed 2).
Sensor offsets 0.1–0.3 °C for ~25 s by the panel's arrows (20:26), reset to 0.0 at 20:27.
Fault: "FEHLER HOCHDRUCK, bitte Kundendienst informieren" on the panel at 20:28 (last bus error number 18 from 19:24).
Power cycle by the maintainer after the recording was started (~20:31). TODO blocker 23.

## 2026-11-17 finding: Hochdruck fault came from Quick start
Bus: `0x0669` (Quick start) 1 at 20:23:23; pumps on (`0x4E5E` 0x0041); compressor on at 20:24:23 (`0x40C1`); error
18 at 20:24:25; compressor off by 20:24:25 (`0x0081` → `0x0001`). Panel Fehlerliste: HOCHDRUCK 20:24 17.11.26 (entry 1),
KEINE LEISTUNG 13:11 17.11.26 (entry 2). Pressures after the stop: Hochdruck 10.4 bar, Niederdruck 10.0 bar.
HEISSGAS 76.6 °C at 20:23:55 with the compressor off, not explained. TODO blocker 23.

## 2026-11-17 change + finding: debug sensors, refrigerant pressure scale, Hochdruck research
- Flashed 21:01: debug sensors `DEBUG_MGR_0074/0294/06AE/4E68/4E5A` (Manager, every 5 min, disabled by default);
  `wp_debug.yaml` got an optional `disabled_by_default` (default false).
- `DRUCK_HOCHDRUCK` `0x0268` / `DRUCK_NIEDERDRUCK` `0x07A5` were 100x too small in HA (type `et_cent_val` /100 and
  YAML scaler 0.1): now scaler 10.0 = raw/10 bar, flashed 21:15. These are the **refrigerant** pressures (the
  heating water is "Druck Heizkreis" 1.34 bar). Scale plausible, not yet confirmed on the panel (TODO 24).
- Dashboard: "Hochdruck (Kältekreis)" and "Niederdruck (Kältekreis)" added to Diagnose > Hydraulik (live and example).
- Hochdruck fault still active after the power cycle; heat pump switched off by the maintainer ~21:20. Web search:
  typical causes are no heat removal (closed circuits, no flow), too high flow temperature, sensor/board faults.
- ESP fault-list request (raw write `0x0B9A`) got no answer at 20:38–20:40 (TODO 26). Pages: [registers](ttf07c-registers.md).
- HA registry names: `sensor.heatpump_druck_heizkreis_max` = "Hochdruck Kältekreis", `_min` = "Niederdruck Kältekreis" (entity IDs unchanged).

## 2026-11-17 fix: Hochdruck fault reset, compressor runs
Fehlerliste deleted by the maintainer (fault stayed: latched), then Inbetriebnahme > Reset > Wärmepumpe (~21:45):
error number 0, compressor on at about 850 W; read at 21:49: Hochdruck raw 199 = 19.9 bar, Niederdruck raw 82 = 8.2
bar; HEISSGAS 30 → 54 °C in 2 min. Error 18 = Hochdruck ([Errors](errors.md)); firmware text added (compiled, not
flashed). [Registers](ttf07c-registers.md) updated (operating pressures, debug sensors, code 18).

## 2026-11-17 test: refrigerant pressure scale confirmed; ESP fault-list read fails
Panel Info > Wärmemenge > Prozessdaten (photo ~22:00): Heißgastemperatur 60.0 °C, Druck Hochdruck 20.4 bar, Druck
Niederdruck 8.0 bar; ESP read 22:00: `0x0265` 605, `0x0268` 205, `0x07A5` 79. So raw/10 bar is right (TODO 24
closed). The ESP published Fehlerliste "keine" at 21:17 while the panel still had two entries (TODO 26).

## 2026-11-17 test: Heizprogramm registers (HK1)
"Heizungssteuerung" switched to Wärmepumpe at 22:01:14 (maintainer's go), emulation off; the WPM3i's presence check at
22:05:59 went unanswered and the panel showed Programme > Heizprogramm again. Panel reads at 22:12 from **HK1** `0x301`:
`0x1410` … `0x1470` (Mo–So), groups `0x1480` (Mo–Fr), `0x1490` (Sa–So), `0x14A0` (Mo–So); window 1 = `0x2840`
(10:00–16:00) everywhere, windows 2–3 `0x8080`. Same layout as the Warmwasserprogramm (Kessel `0x1710`). Switched back
to FEK Emulation afterwards. TODO blocker 21 closed. Page: [registers](ttf07c-registers.md).

## 2026-11-17 change: register table with bus traffic; unknown registers left open
[TTF07 C registers](ttf07c-registers.md) got a column "Traffic (seen on the bus)": who sends each address to whom, from
a scan of all 31 captures (277 addresses), e.g. `0xFE1B` Manager→MFG write, `0x0B9A` Panel→Manager and
Manager→Panel write. Rows sorted into their node groups. Unknown registers are left open on purpose (maintainer):
TODO item 1 moved to future work (28).

## 2026-11-17 change: settings entities, Heizprogramm, heat demand; flash 22:25
New (flashed 22:25:28, also error text 18 = Hochdruck): binary "Sommerbetrieb" (`0xFDB4`), "Antilegionellenbehandlung"
(`0x0101`), "Heizanforderung HK1" (`0x0052`, decoded from `0x601` frames in the device file's CAN handler, since
`0x601` is no CanNode); sensors "Sommerbetrieb Heizgrenze" (`0x01BF`), "Maximale Vorlauftemperatur" (`0x01E8`),
"Maximale Rücklauftemperatur" (`0x0028`, renamed from SOLLWERT_MAX_HK1); texts "Heizprogramm Montag" … "Sonntag" (HK1
`0x1410`…, read-only, requested only while no FEK is registered). Renamed properties `TBD_18` → `PUFFERBETRIEB`,
`KUEHLEN_TBD_FDB2` → `PUMPENZYKLEN` (entities kept; HA names "Pufferbetrieb", "Pumpenzyklen"). Dashboard updated
(Einstellungen > Anlage, new section Heizprogramm, tile "Heizanforderung"). The ESP's fault-list run after boot
(22:27:38) sent its requests; the Manager answered nothing (list deleted) → "keine", consistent (TODO 26 stays open).
Compressor normal: Heißgas 62 °C, Hochdruck 20.9 / Niederdruck 7.6 bar (22:26).

## 2026-11-17 change: committed
The work of 2026-11-17 committed on `ttf07-port` as topic commits on top of `6f6c245` (core analytics names,
templates, properties, `ttf07_wpm3i` incl. rename, dashboard example, docs); the HA config repo commits the submodule
and the include of `yaml/ttf07_wpm3i.yaml`. Not pushed (the host has no GitHub credentials).

## 2026-11-17 change: branch rebuilt for upstream
`ttf07-port` rebuilt on upstream `ae1d414` (WPL 25) as 9 upstream topic commits plus this docs commit (plan:
`plan/upstream.md`; old head kept as `ttf07-port-backup-20261117`). `wp_climate` keeps upstream's `heating`/`hot_water`
types; the thermostat is the new `type: preset` (keys `current_temp`, `comfort_temp`, `eco_temp`). The dashboard
example moved to `yaml/examples/ttf07_wpm3i_dashboard.yaml`; code comments no longer point to the wiki.

## 2026-11-18 test: Programmschalter Komfort does not switch the hot water setpoint
Maintainer switched "Thermostat Warmwasser" to comfort at 10:00:06 (HA): ESP wrote `0x0112` = `0x0300` to the
Manager, the Manager echoed it to the panel (10:00:07) and answered `0x0300` on every read after (stable > 2 min).
Speicher Soll (Kessel `0x0003`) stayed 44.5 = WW Eco (reads 10:00:56, 10:01:56); WW Komfort is 50.0. The
Warmwasserprogramm is empty on all days. Probably: the Programmschalter Komfort/Eco only sets the heating circuit;
hot water uses WW Komfort inside Warmwasserprogramm windows and WW Eco outside (unconfirmed, test with a window).
So "Thermostat Warmwasser" mapping its preset to the Programmschalter is wrong. Earlier preset flips back to eco
(06:23:58, 08:56:11 UTC) were not reproduced in this clean test.
[capture](../raw/captures/2026-11-18-1000-programmschalter-komfort-ww.log).

## 2026-11-18 test: Warmwasserprogramm window switches the hot water setpoint
Maintainer's go. Programmschalter Komfort (from the test above), Warmwasserprogramm Mittwoch set to 10:00-12:00 via
HA 10:06:42 (Kessel `0x1730` = `0x2830`, read back). Speicher Soll 44.5 → **50.0 = WW Komfort** at 10:07:05 (~22 s).
Window cleared ("-", `0x8080`) and Programmschalter → Eco 10:07:18 (Manager echoed `0x0400` to the panel); Speicher
Soll back to 44.5 by 10:08:26. Speicher Ist was ~50 °C, so no hot water heating started. Verdict: confirmed: WW
Komfort/Eco comes from the Warmwasserprogramm (Komfort inside a window), not from the Programmschalter (Komfort and Eco
both gave WW Eco with an empty program). Not tested: Programmschalter Eco with a window (probably also WW Komfort),
positions Programm/Warmwasser. Consequence: "Thermostat Warmwasser" preset ↔ Programmschalter is wrong.
[capture](../raw/captures/2026-11-18-1006-ww-programm-window.log).

## 2026-11-18 change: "Warmwasser Modus" replaces the Programmschalter as hot water preset (not flashed)
Maintainer's request. `yaml/ttf07_wpm3i.yaml`: new template select "Warmwasser Modus" (`WW_MODUS`, Komfort / Eco /
Programm). Komfort writes the Warmwasserprogramm Mo-So group `0x17A0`-`0x17A2` = `0x0060`, `0x8080`, `0x8080`
(00:00-24:00), Eco writes all three `0x8080`, then reads the 21 day windows back after 5 s. The state is computed from
the read-back windows (global `ww_programm_update_modus`): all days `0x0060` + empty → Komfort, all empty → Eco, else
Programm (not selectable). "Thermostat Warmwasser" uses it as `preset_select`. Config valid; not flashed because the
working tree also holds another session's unfinished refactor. Restored after the tests: WW Komfort 52.0, WW Eco 50.0,
FEK Emulation Eco 21.0.

## 2026-11-18 change: commit rework after the maintainer's review (compiled, not flashed)
Series rebuilt on upstream `ae1d414` (old head `ttf07-port-backup-20261118`, see `plan/upstream.md`), no
`Co-Authored-By` trailers any more (rule in `AGENTS.md`). Changes:
- Logging: `PROPERTIES_NO_LOGGING` removed; every received message is logged.
- Entity names (maintainer's decision): template entities are named by their id like upstream (switching from
  `ttf07.yaml` keeps history); energy/COP ids are upstream's (`EL_ENERGIEAUFNAHME_WW_SUMME_KWH`, `COP_HEIZ_TAG`, …).
  German names come from the new optional package `yaml/names/ttf07_wpm3i_de.yaml` (`!extend`), included in
  `heatpump-ttf07c.yaml`, so the HA entities stay the same. Investigated: ESPHome 2026.10.2 still derives the entity's
  object_id/unique ID from `name`; HA has no translation for ESPHome entity names; `!extend` fails on a missing id, so
  a names package works for one device file only. Analytics publishes under the entity id (`getAnalyticsNames()` is
  filled by the sensor templates), so the names package doesn't change the topics.
- Debug registers: no `TBD_*`/`DEBUG_*`/`KUEHLEN_TBD_*` in `property.h`. `wp_debug` takes a raw `address` (optional
  `type` to decode); the debug sensors moved to the optional package `yaml/ttf07_wpm3i_debug.yaml`, renamed
  "Debug <node> 0x<address> (hint)" (new entities). `PUFFERBETRIEB` and `PUMPENZYKLEN` are binary sensors now.
- `property.h`: TTF07 C registers merged into upstream's `TTF_07_C` list in address order, no comments.
- "Software WPM2" → "Software WPM3i" (new entity).
Config check against the old firmware: 174 of 189 entity names unchanged, the 15 others are the intended renames.
`esphome config`/`compile` OK with the "Warmwasser Modus" change of the same morning in the tree.

## 2026-11-18 test: rework and "Warmwasser Modus" flashed and tested
Flashed 10:37 (maintainer's go). HA: all existing entities kept their IDs, values and history (e.g. the energy sums);
new: "Software WPM3i" (391.10), 13 "Debug …" sensors (values as before: MFG `0xFE4C` 18, `0xFE09` 18.9 °C, Bedienteil
`0x06AF` 1 / `0x4E8B` 2), binary "Pufferbetrieb"/"Pumpenzyklen" (on), "Warmwasser Modus" (Eco). The old `TBD_*`,
`Kuehlen 0x…` and "Software WPM2" entities were removed by HA itself. No errors in the log. Dashboard "Wärmepumpe":
the 10 references to removed entities point to their successors (websocket `lovelace/config/save`).
Warmwasser Modus (handover of the other session): thermostat → comfort 10:39:26: the ESP wrote `0x17A0`-`0x17A2` =
`0x0060`, `0x8080`, `0x8080`; the Kessel answered all 7 days with `0x0060` (end 24:00 accepted) + 2 × `0x8080`;
Speicher Soll 50.0 → 52.0 (WW Komfort) at 10:40:31. → eco 10:40:42: all windows `0x8080`, Speicher Soll 50.0 at
10:41:31. Flaw: during the read back the mode showed "Programm" for ~5 s (first day new, others old). Fix: global
`ww_modus_pending` (the mode is evaluated again only when all 21 windows are back), flashed 10:44; retest 10:45-10:48:
Komfort/Eco without the intermediate "Programm", Speicher Soll 52.0 / 50.0. End state as before: Warmwasser Modus Eco
(program empty), Programmschalter Eco, WW Komfort 52.0, WW Eco 50.0.
[capture](../raw/captures/2026-11-18-1039-ww-modus-test.log), [retest](../raw/captures/2026-11-18-1045-ww-modus-retest.log).

## 2026-11-18 change: branches on GitHub cleaned up
Maintainer: `ttf07-port` pushed (force) and made the default branch; `ttf07` renamed to `archive/ttf07-old`; `pr/*`,
`main` and `kr0ner_main` deleted on GitHub. Duplicate remotes `mkaiser_OneESP32ToRuleTHemAll` and `kr0ner` removed
locally (same URLs as `origin`/`upstream`). `AGENTS.md` branch table updated.

## 2026-11-18 decision: entity naming and debug registers (session summary)
Maintainer's decisions from the review: (1) template entities are named by id like upstream, German names only in
the optional names package; HA history of upstream users matters more than the fork's own (which is kept anyway via
the package). (2) Unidentified registers are never added to `property.h`; they live as address-based `wp_debug`
sensors in `yaml/ttf07_wpm3i_debug.yaml`. (3) One branch (`ttf07-port`) for the upstream series, no attribution
trailers. Findings: ESPHome 2026.10.2 derives object_id/unique ID from the entity name; HA translation keys are not
available for ESPHome entities; `!extend` errors on a missing id (a names package fits one device file only);
renaming the entity ID in the HA registry keeps history, renaming the ESPHome name does not. TODO revised: items 3,
10, 11, 18 updated; new 30 (English names package), 31 (dashboard export without the lock), 32 (old local branches).

## 2026-11-18 decision: TODO revised, register decoding plan
Maintainer: the HEISSGAS reading of 76.6 °C with the compressor off (2026-11-17 20:23:55) was a one-off event, not
followed up. The fault list is empty after the heat pump reset, so the open question about the ESP's error-list
request (no answer at 20:38–20:40, "keine" at 21:17) is dropped; the missing-fields item waits for a new fault entry
(blocker). New plan [`plans/register-decoding.md`](../../plans/register-decoding.md) for the unknown registers that are
sent regularly on the bus (Kessel block to `0x379`, `0x601` block to HK1, FEK/emulation frames, WPM3i ↔ MFG,
panel keep-alives), based on a 10-min passive capture (12:07–12:17). TODO: the FEK-unknowns item merged into the
plan item 1; the open-questions section removed; items renumbered (1–21).

## 2026-11-18 change: register decoding phase 0 started
All "Debug …" sensors enabled in HA 12:23 (the 5 Manager menu registers were disabled by default; values at once:
`0x0074` 1, `0x0294` 63, `0x4E68` 2, `0x4E5A` 0, `0x06AE` 0). 24 h passive capture started 12:29
(`/share/heatpump-capture/`, see [plan](../../plans/register-decoding.md) phase 0). Lesson: killing the host-side
`docker exec … esphome logs` leaves the client running inside the ESPHome container with its API connection; 7 such
clients had piled up during the start attempts and were killed there.

## 2026-11-18 change: dashboard and device page screenshots
Maintainer: screenshots of the "Wärmepumpe" dashboard and the device page, stored in the fork-only
`dashboard-examples/ttf07c/images/` (for upstream PR 2: upload to the PR description). Taken with Playwright in the
official Playwright container (the Alpine add-on cannot run its Chromium) after the Sungrow repo's pattern, logged in
as a temporary local-only admin user that is deleted after each run; sidebar hidden. 5 dashboard views, the device
page as top + 4 cards (it is longer than one image). Scripts `take_screenshots.py` / `screenshots_playwright.py`;
how-to and pitfalls: [Screenshots](screenshots.md).

## 2026-11-18 decision: ttf07_wpm3i.yaml extends upstream's ttf07.yaml (prototype)
Maintainer: no replacement of upstream's `yaml/ttf07.yaml` (contributions #99, #123); generalize it in this branch
and let `ttf07_wpm3i.yaml` extend it (TODO option (c)). Comparison before: 53 of the 62 entities of `ttf07.yaml` +
`txx_base.yaml` had the same name in ours; a switching upstream user would have lost 9. Blockers found: templates
register `on_boot` callbacks with the target node and the entity id, which `!extend` cannot change; the callback
handler merges callbacks per (node, register), so two entities can follow one register.
Prototype (working tree, not flashed): substitutions with upstream defaults in `ttf07.yaml`
(`ttf07_status_from_kessel` true, `programmschalter_target` Kessel, `druck_kaeltekreis_scaler` 1.0) and
`txx_base.yaml` (`vorlaufisttemp_target` HK1, `hk1_settings_write_lock` false); `wp_number.yaml` var `id_suffix`
(internal id ≠ name). `ttf07_wpm3i.yaml` includes `ttf07.yaml` as package `TTF07`, 45 duplicate packages removed,
status stays on `0x4e5e` (`ttf07_status_from_kessel: "false"`), the 5 pump/controller settings stay numbers
(`*_SETTING` ids, same names), the base's sensors for them, the HK1 room values and `KUEHLEN_EINGESCHALTET` are
internal. Check: `esphome config` before/after, all 190 visible entities identical in name, domain and the
fields that matter to HA; other differences: the hidden base entities, one boot read each for them, the internal
`*_SUM_KWH` helpers now `total_increasing`. `esphome compile` OK. The subagent's claim that our energy totals were
`measurement` was wrong (they are `total_increasing`, like upstream). Flash after the 24 h capture (TODO item 3).

## 2026-11-18 decision: ttf07_base.yaml instead of switches in ttf07.yaml
Maintainer: upstream it the clean way, like upstream's `wxx_base.yaml` (commit `b7a9c1a`, a contributor's refactor
that kr0ner merged): new `yaml/ttf07_base.yaml` with what every TTF07 has; `ttf07.yaml` becomes a thin variant
(status from the Kessel `0x0a20`, pump powers / Verdichter Stillstand / Reglerdynamik as read-only sensors,
`KUEHLEN_EINGESCHALTET`, Programmschalter on the Kessel); `ttf07_wpm3i.yaml` is the WPM3i variant (status from
`0x4e5e`, those settings as numbers, Programmschalter on the Manager). This replaces the prototype's switches in
`ttf07.yaml` and the `id_suffix` template var (no hidden duplicates any more). Left in `txx_base.yaml`:
`vorlaufisttemp_target` (HK1) and `hk1_settings_write_lock` (false). Checks with `esphome config`: this installation
190/190 visible entities identical; a plain TTF07 test device (`/config/esphome/.ttf07check/`, before = `HEAD`)
61/61 identical, only the boot lambdas are split over two files. Compile OK. NHZ bits of `0x0A20` are already
confirmed by the Notbetrieb captures of 2026-11-17 (`0x0041`/`0x0042`/`0x0043` with `0x4e5e` `0x0090`/`0x00A0`/`0x00B0`);
bit 4 (hot water) is left for the 24 h capture.

## 2026-11-18 change: ttf07_base refactor flashed
Flashed 16:42:29–16:42:51 (maintainer's go) during the 24 h capture, which continued without a reconnect. Log after
boot: only the usual warnings (canbus/mqtt "took a long time", one MQTT DNS resolve error that cleared). Series
rebuilt into topic commits (`plan/upstream.md`, "Rework 2"), old head `ttf07-port-backup-20261118b`.

## 2026-11-18 change: capture analysis script, dashboard export, community Grafana checked
- `.claude/tools/can-capture/capture_series.py`: value series per (register, sender, target, type) from a capture,
  with the status words and compressor current at every change (plan phase 0 done).
- `export_dashboard.py` unwraps the restriction-card locks (`--keep-locks` keeps them); the example
  `yaml/examples/ttf07_wpm3i_dashboard.yaml` re-exported from the live dashboard: it had fallen behind (grid options,
  Programmschalter tile, section visibility by heating control, "Automatischer Sommerbetrieb"). TODO 13 closed.
- Community Grafana (TODO 2 closed): every panel shows this device once the selected "Numeric Sensor" is one it sends
  (`AUSSENTEMP`); the default `ABLUFTFEUCHTE` (THZ only) fails the dashboard's per-device access check, hence "No data".
  CoP hot water 2.45 (community 2.96), heating 5.25 (5.62), 5 compressor starts today
  ([screenshot](../raw/2026-11-18-community-grafana.png)). Possible upstream hint: default to a sensor every variant sends.
- `take_screenshots.py`: pip with `--default-timeout=120 --retries 5` (the download timed out twice).
- New TODO 2: README for TTF07 C users (FEK emulation, room values into the ESP, hot water window quirk).

## 2026-11-18 ingest: Busteilnehmer photo, 0xFE4C, the participant notice
Maintainer's photo of Diagnose > System > Busteilnehmer (17:15, [photo](../raw/2026-11-18-busteilnehmer-panel.jpg)):
01 WPM3i 391-10, 02 FES 417-07, 03 FEK 416-03 (the ESP's emulation), 04 MFG 18. The capture shows the panel reading
`0x4E69` (18), the HK1 software and `0x4E68` (2) for this page. MFG `0xFE4C` = 18 too → MFG software version
(◻️ plausible; firmware naming batched with phase 2). `0x0645`/`0x4E5C`/`0x4E61`: sent by the WPM3i only at 16:44 and
16:47 after the ESP flash, each followed by the panel's `0x4E69` read, not when the menu was opened → probably a
"bus participants changed" notice (`0x4E5C` 0x40 → 0x44 when the FEK emulation was back). Pages:
[registers](ttf07c-registers.md), [plan](../../plans/register-decoding.md).

## 2026-11-18 change: TTF07 C user guide in docs/, tools moved, plans and TODO tidied
- User guide [`docs/ttf07c.md`](../../docs/ttf07c.md) (was TODO 2 "README for TTF07 C users"): installation,
  heating control and FEK emulation, room values, hot water window quirk, energy dashboard, dashboard example, known
  limitations. Upstream-ready (no wiki/TODO references); new commit 12 "Add TTF07 C user guide" for PR 2b, the
  README links it. Maintainer's decision: a `docs/` folder instead of `dashboard-examples/ttf07c/`.
- Screenshots moved to `docs/images/ttf07c/`; `export_dashboard.py`, `take_screenshots.py`,
  `screenshots_playwright.py` to `.claude/tools/dashboard/`; `dashboard-examples/` removed.
- Two findings while writing: the ESPHome option "Allow the device to perform Home Assistant actions" is not needed
  (off on this device, room values arrive); invalid room values do not stop the emulation (no room influence, room
  values not sent, warning in the log); only an invalid outdoor temperature stops the setpoint.
- README: hierarchy diagram and the `ttf07_wpm3i.yaml` line still said "builds on core.yaml"; now
  `txx_base → ttf07_base → ttf07 / ttf07_wpm3i` (commits 8 and 10).
- `plan/upstream.md` trimmed to the current state (series of 13, PRs, design decisions for the PR texts, reorganize
  procedure moved there from TODO); the history of the rebuilds stays in this log and git.
- Git: all old local branches and the `ttf07-port-backup*` branches deleted (maintainer); left: `ttf07-port`,
  `master`, `archive/ttf07-old`. `origin/ttf07-port` still has the pre-rework series.
- TODO: README item done, branch cleanup done, Fehlerliste blocker dropped (maintainer: the fault list was deleted,
  nothing to test with); renumbered.

## 2026-11-18 change: ttf07-port force-pushed
The maintainer force-pushed the rebuilt series of 13 commits; `origin/ttf07-port` = `749f69f`. Upstream unchanged.

## 2026-11-18 change: PR texts, PR 1/2a compile on upstream, TODO revised
- `upstream/issue-text.md`: ready-to-paste texts for PR 1 and PR 2a.
- Compile checks (`esp32-poe-technik.yaml`, upstream's CI target): commits 1–7 on `ae1d414` with `thz504.yaml` OK;
  commit 8 cherry-picked alone onto `ae1d414` (clean) with `ttf07.yaml` OK, so PR 2a is independent of PR 1.
- TODO: new open decision 3 (external heating circuit pump for users without one; with the default 0 the values are
  correct, only two entities stay 0); item 10 links the PR texts; renumbered.

## 2026-11-18 decision: ext. Heizkreispumpe entities stay (TODO 3)
- Maintainer chose option A: keep "Leistung/Energie ext. Heizkreispumpe" as they are. With
  `static_leistung_heizkreispumpe: "0"` they stay 0 W / 0 kWh and "Leistung Heizen" = compressor only, so results are
  correct; the guide already says "0 if you have none".
- Rejected: B (`internal` substitution hiding both entities; a second setting, and existing installs with a pump would
  lose the entities unless they set the flag) and C (optional package; needs a hook in "Leistung Heizen").
- TODO: decision 3 removed, items renumbered; references in `plan/` updated (item 11 → 10, item 7 → 6).

## 2026-11-19 test: 24 h passive capture finished (TODO 1, phase 0)
- Ran 2026-11-18 12:29:16 → 2026-11-19 12:29:16 CET, read-only (ESPHome API log, Communication lines only) →
  `/share/heatpump-capture/2026-11-18-passive-24h.log`, 350k lines, 62 MB.
- One API drop: reconnect at 2026-11-19 07:47:33, gap ~30 s. Flash window 2026-11-18 16:42–16:51 to exclude.
- Phase 0 of `plans/register-decoding.md` done; next: copy to `.wiki/raw/captures/`, run `capture_series.py`, phase 2.

## 2026-11-19 ingest: Kessel `0x000A` = date (TODO 1, phase 1)
- 24 h capture: Kessel → `0x379` write `0x000A` = `0x120B` until 23:57:04, `0x130B` from 00:04:04 (2026-11-19), so
  high byte = day, low byte = month (like `0x0009` = minute/hour).
- Its frames carry a 6th data byte `0x1A` = 26 (`60 79 0A 12 0B 1A 00`), the only register in the Kessel block that
  does: the year (two digits). Status ✅ analysis; month change (2026-12-01) still to see.
- Registers page row split from the open group; firmware name goes into the phase 2 batch.

## 2026-11-19 change: agent docs restructured (rules index, workflow, T### numbers)
`AGENTS.md` rewritten as a short index: where everything is, and the rules as one-line rows linking to their evidence.
New: `workflow.md` (how work is written down, multi-agent git rules, `TODO.md` inbox and `T###` numbers),
`dev/development.md` (branches, build/flash, captures, pitfalls, commit stack), `.wiki/AGENTS.md` (wiki schema),
wiki pages [writes](writes.md) and [entity names](entity-names.md). `plan/` → `plans/` (handover folded into the
status log of `plans/register-decoding.md`; new `plans/analytics.md`); `TODO.md` items 1–17 became T001–T017 with a
**From the maintainer** inbox; skill `revise-todo` → `todo-housekeeping`.
