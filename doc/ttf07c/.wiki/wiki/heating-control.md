# Heating control (FEK detection, modes, heating curve)

See also: [FEK2](fek2.md), [CAN bus](can-bus.md). Firmware: `yaml/ttf07_wpm3i.yaml`, section "Heating control".

## Modes

Who controls heating (HA: "Heizungssteuerung aktiv"):

| Mode | When | What the integration does |
|---|---|---|
| FEK installiert | a real FEK is detected | nothing: the FEK sets the flow setpoint; HK1 heating settings (Komfort/Eco, Steigung, Raumeinfluss) are locked; no emulation |
| Wärmepumpe | no FEK, "Heizungssteuerung" = Wärmepumpe | the WPM3i controls heating with its own curve; the HK1 settings and the Programmschalter (Komfort/Eco) are writable |
| FEK Emulation | no FEK, "Heizungssteuerung" = FEK Emulation, outdoor temperature valid | the ESP is the FEK: room values from HA, flow setpoint from its own heating curve; HK1 settings locked (the ESP *is* HK1) |
| Prüfung läuft | after boot, or 10 min after the last sign of a FEK | HK1 settings locked until the check has an answer (normally < 1 min) |

A locked number refuses the write and reads the value back (template option `write_lock` in `wp_number`).

## FEK detection (since 2026-11-15)

- **Active check, every minute:** read `FET_SOFTWARE` (`0x0199`) from HK1 and the Manager. Without a FEK the WPM3i
  answers for HK1 with its own version: HK1 = Manager = Kessel = **391** (`0x0187`), revision `0x019A` = **10**. A FEK
  answers with its own: FEK2 **416** / **3**. So "HK1 version ≠ Manager version" means a FEK owns HK1, without a
  hard-coded version ([capture](../raw/captures/2026-11-15-2255-fek-detection-probe.log)).
- **Passive, immediately:** frames with CAN ID `0x301` that only a FEK sends: registration (system `0x00FD` =
  `0x0900`), answer to the presence check (system response `0x00FD`), room temperature written to `0x601`. Without a
  FEK, `0x301` sends no system messages at all (17:04 capture: only `0x680` is checked).
- The ESP does not receive its own frames, so its emulation never looks like a real FEK.
- While the ESP emulates, HK1 reads stay unanswered (the WPM3i's HK1 is silent). If the WPM3i answers again with its
  own version, the registration was lost and the ESP registers again.
- Tested with the real FEK on 2026-11-16 ([capture](../raw/captures/2026-11-16-1123-real-fek-attached.log)): plugged in at 11:23:18 while emulating → detected by
  its registration at once, emulation stopped, "FEK installiert" 9 s later; the WPM3i accepted the FEK **immediately**
  (Kessel and `0x601` answered its `0x00FE` at 11:23:28, no wait for the 8-min check); active check reads 416.
  Unplugged ~11:38 → WPM3i released HK1 at its 11:44 check, the ESP read 391 at 11:45:02 and registered again
  (~7 min, no intervention).

## Thermostat (since 2026-11-16)

`climate.hwr_warmepumpe_thermostat_heizung` ("Thermostat Heizung", component `wp_climate`, since 2026-11-16 19:35;
replaces "Thermostat FEK Emulation"): mode heat only; current temperature/humidity = house average from HA; action
heating = Heizbetrieb. Komfort and Eco are presets. Its targets follow "Heizungssteuerung aktiv":

| Heizungssteuerung aktiv | Preset ↔ | Target ↔ | Writes |
|---|---|---|---|
| Wärmepumpe | Programmschalter (Komfort `0x0300` / Eco `0x0400`; other positions: no preset) | HK1 "Heizen Komfort/Eco Temperatur" | yes |
| FEK Emulation | "FEK Emulation Betriebsart" | "FEK Emulation Komfort/Eco Temperatur" | yes |
| FEK installiert, Prüfung läuft | Programmschalter | HK1 values (with a FEK: the FEK's answers) | refused |

`wp_climate` (`type: preset`) options: `alternative` (second select + numbers), `use_alternative` (here `id(fek_registered)`),
`writable` (here `id(fek_state) == 1`); the lambdas are checked every 2 s. The Programmschalter also sets the hot
water mode ("Thermostat Warmwasser"). While the emulation runs, the HK1 numbers stay `unknown` (HK1 reads are not
answered); they are read again by the 15-min refresh after a switch to "Wärmepumpe". Tested 19:36: after boot
("Prüfung läuft") preset eco from the Programmschalter, read only; with the emulation preset comfort, target 21.1 =
emulation Komfort; target write 19:54 went to "FEK Emulation Komfort Temperatur". Wärmepumpe mode tested 20:31–20:35:
emulation stopped 20:31:24, WPM3i check 20:32:00 unanswered (HK1 back); thermostat preset eco (Programmschalter),
target 19.5 = HK1 Eco (the WPM3i's own values: Komfort 23.0, Eco 19.5); a target write 19.5 went to HK1 `ECO_TEMP`
and was read back after 10 s. Emulation on again 20:35:05.

## Heating curve

The WPM3i's flow setpoint follows `Vorlauf = Raumsoll + Steigung · (Raumsoll − Aussen) + ~0.23 K` with the
instantaneous outdoor temperature, in Eco and Komfort alike (146 values, rms 0.06 K;
[fit](../raw/2026-11-15-heating-curve-fit.md)). The real FEK's setpoint (25.0 °C) fits the same curve with its own
settings (21.5 °C, Steigung 0.24, 7.9 °C outside).

The emulation uses this curve with its own parameters (HA, category config, restored): Komfort/Eco temperature
(selected by "FEK Emulation Betriebsart", which HA automations can switch), Steigung, Offset, Raumeinfluss (own
definition: K flow per K room deviation, from the HA house temperature, clamped ±5 K), Vorlauf min/max. Defaults are
the FEK2's settings (21.0/20.0 °C, 0.24) and offset 0.2.

Unknown: how the FEK/WPM3i weigh the room deviation (Raumeinfluss 2 on the FEK; 0.4 K higher setpoint at 0.7 K
room deviation, too few points to fit).

## What the emulation sends (copied from the FEK2, 2026-11-15 19:33 capture)

| When | Frames (CAN ID `0x301`) |
|---|---|
| registration | `66 01 FD 09 …`; after 10 s system `0x00FE` to Kessel and `0x601`, then the setpoint and the room values |
| every 3 min, and at once when "FEK Emulation Betriebsart" changes (since 2026-11-16) | to the Kessel: `0x0002` = flow setpoint, `0x0058` = phase (`0x0200` Komfort, `0x0100` Eco; before 2026-11-16 always `0x0200`), `0x006E` = `0x0100`; 2 s later to `0x601`: `0x0058` = phase, `0x0029` = `0x0A00`, `0x002A` = `0x1E00`, RAUMEINFLUSS = 2, VERSTELLTE_RAUMSOLLTEMP; 8 s later to `0x601`: VORLAUFSOLLTEMP |
| every minute | room temperature `0x0011` and humidity `0x0075` to `0x601` |
| every 7 min | system `0x00FE` to Kessel and `0x601` |
| on request | answer to the presence check, to `0x601`'s `0x00FE`, and to reads addressed to HK1 (since 2026-11-16), in the form of the read: `0x0199` 416, `0x019A` 3, VORLAUFSOLLTEMP (last sent setpoint), KOMF_TEMP, ECO_TEMP, VERSTELLTE_RAUMSOLLTEMP, STEIGUNG_HK1 (emulation settings), RAUMEINFLUSS 2; other reads are logged, not answered |

Frames go through a queue (one every 30 ms). Without answers to HK1 reads, the control panel (`0x100`) waited for its short-form read of VORLAUFSOLLTEMP
(`61 01 04 …`) and retried every ~6 s: a spinning wheel and ~10 s lag on the display (2026-11-16 morning). With the
answers (`22 00 04 00 F4` = 24.4 °C) the lag is gone (owner, 10:59;
[capture](../raw/captures/2026-11-16-1051-hk1-read-answers.log)).

After a reboot or flash of the ESP, the WPM3i keeps HK1 reserved for the old registration: HK1 reads stay unanswered,
the check shows "Prüfung läuft" until the next presence check releases HK1 (≤ 8 min), then the emulation registers
again (2026-11-16: flash 10:51, released 10:56:00, registered 10:56:19). The compressor kept running.

## Test 2026-11-16: emulation with flow setpoint (passed)

"Heizungssteuerung" = FEK Emulation at 09:54:23 (defaults: Komfort 21.0 °C, Steigung 0.24, offset 0.2, Raumeinfluss
0.5; outdoor 8.6 °C, house 20.45 °C). Before, the WPM3i ran Eco 19.5 °C / Steigung 0.26 → setpoint 22.6 °C, compressor
off since 07:00.
- Registered at once; Kessel and `0x601` answered the `0x00FE` system messages; first setpoint 24.5 °C at 09:54:34.
- **Compressor on ~45 s later** (~09:55:10), Heizbetrieb at 09:55:40, ~830 W; ran steadily for the 30 min
  (Vorlauf 29.7 → 30.9 °C, Rücklauf 22.6 → 24.6 °C).
- The panel showed **Puffersolltemperatur 24.5 °C** = the emulation's setpoint, so `0x0002` to the Kessel **is the
  flow setpoint** (confirmed). It also showed "Isttemperatur FEK" 20.5 °C, "Solltemperatur FEK" 21.0 °C,
  humidity 52.7 % (the HA values), the "Kühlen" menu, and no errors.
- Presence checks 10:00, 10:08, 10:24 answered; registration held; "FEK installiert" stayed off.
- Log: no errors; `max_frames_per_loop` warnings only during a burst of Manager frames while the panel was browsed.

- First compressor stop at 11:04:04 after 69 min (Rücklauf 25.5 °C, setpoint 24.4 °C): normal cycling.

Decision (owner): the emulation **stays on** as the heating control.
[capture](../raw/captures/2026-11-16-0954-fek-emulation-flow-setpoint.log)

## Pump cycles, compressor lock-out and Eco (2026-11-20)

Real FEK attached 11:59:46, emulation again from 21:38:35; all times CET, from the ESP log and HA history
(`doc/ttf07c/.wiki/raw` capture not copied yet).
- **The FEK sends no pump command.** Its frames are the flow setpoint `0x0002`, the phase `0x0058` (`0x0200` Komfort,
  `0x0100` Eco), `0x006E`, room setpoint/temperature/humidity (`0x0012`, `0x0011`, `0x0075`), `0x0029`/`0x002A`,
  Raumeinfluss, presence checks and software version answers. Every pump start is the WPM3i's own decision
  (Kessel status `0x0020` / `0x0120`, then `0x4e5e` bit 0).
- **Pumpenzyklen (setting EIN):** without heat demand the WPM3i runs the heating circuit pump alone for exactly
  5 min 00 s (`0x4e5e` = `0x0001`). Start to start 17-19 min at -3...5 °C outside (24 min on 17 Nov). Seen with the real
  FEK in Komfort (16:37, 18:24, 18:44, 19:02) and with the emulation in Komfort (21:39, 21:56). After every compressor
  stop the pump runs on for 5 min (16:14:02 → 16:19:02, 20:09:58 → 20:14:58). The first cycle after a
  registration came 23-33 s later (12:00:09 real FEK, 21:39:08 emulation).
- **Compressor lock-out:** `VERDICHTER_RESTSTILLSTAND` counts the 60 min "Verdichter Stillstand" down. Heating (and the
  cycles that precede it) only starts after it: stop 18:05:33 → source pump 19:05:33; hot water stop 21:02:08 → heating
  22:04:39. Until then a pump-only cycle ends without a start although the buffer is far below the setpoint.
- **Eco with the real FEK (16:49:20 - 18:17:58, Eco room setpoint 19.9 → 20.5 °C, flow setpoint 24.1-25.2 °C):** no pump
  cycle for 81 min (due ~17:00). The heating start at 18:03:25 (source pump) / 18:03:55 (compressor) came **without the
  heating circuit pump** (`0x4e5e` = `0x40C0`): Vorlauf 24.1 → 39.8 °C in 98 s, Rücklauf 24.4 → 32.1 °C, compressor stop
  18:05:33 at the Maximale Vorlauftemperatur (40.0 °C; Maximale Rücklauftemperatur 30 °C may also act). Buffer
  23.7 → 29.0 °C. This is the "compressor runs only minutes" symptom of 18-20 Nov, with the real FEK. On 16 Nov the
  real FEK in Eco (12:39:15) also stopped compressor and pump at once, then only 5 min cycles.
- **Komfort works:** real FEK 19:06:03 - 20:09:58 (64 min, pump on since the 19:02:39 cycle, Vorlauf 31-34 °C); emulation
  Komfort **22:04:39 - 03:25:18 (5 h 21 min)**, pump running 30 s before the compressor, Vorlauf 31-34.6 °C. House
  stayed at 20.4 °C for 4 h against Komfort 22.0 °C: the flat curve (Steigung 0.24, Raumeinfluss 0.5) is too weak.
- **Phase Eco switches the heating circuit pump off, independent of room and flow** (test 2026-11-22, emulation with
  the same flow setpoint in both phases): Komfort 23.0 °C (setpoint 29.4 °C) → pump 16:05, compressor 16:08:44
  (`0x4E5E` `0x40C1`), heat demand on. Eco 23.0 °C at 16:17:44, setpoint unchanged (29.6 °C) → **pump off 9 s later**
  (`0x40C0`, compressor still on), compressor off 16:18:56 (flow without circulation 33 → 39.5 °C), demand off 16:19.
  Raising Eco to 24.0 °C (setpoint 31.5 °C) brought nothing back. With the real FEK in Eco the same happened
  (2026-11-20 18:03). So in phase Eco (`0x0058` = `0x0100`) the WPM3i does not heat HK1. **Firmware since 2026-11-22: the
  emulation always sends phase Komfort**; "FEK Emulation Betriebsart" Eco only selects the Eco temperature (room and
  flow setpoint). Checked 18:22–18:27 in Eco: heat demand, pump and compressor stayed on.
- **Programmschalter while the emulation owns HK1:** no visible effect (switched Eco ↔ Komfort 2026-11-22 14:47 and
  15:34: nothing changed on the bus or in heating). The panel's start screen shows it in its status line
  ("ECO-BETRIEB" / "KOMFORTBETRIEB"), so that line does not show the emulation's phase.
- **`0x006E`:** the real FEK sends `0x0100` at registration, `0x0200` from 12:00:48 to 14:00:24, `0x0100` since;
  the emulation always sends `0x0100`. Effect unknown (the pump kept running through the change at 14:00).

## Antilegionellen run 2026-11-22 (NHZ fuses off)

Setting Antilegionellenbehandlung EIN since 2026-11-21 22:30 (panel); NHZ fuses off (owner). From the overnight
watch (HA states every 30 s, ESP log; HA link down 23:42–00:11):
- **Start 01:00:54**: Umschaltventil WW 100 %, Warmwasserbereitung 01:01:54, compressor 01:02:54, Vorlauf up to 63.5 °C.
  Heating stopped at 00:59:54 (FEK emulation, Komfort 21.5 °C). Tank 45.6 °C at the start (target 45 °C).
- 01:22:57 compressor off, Nachheizstufe Stufe 1 → 2 (01:24:57) → 3 (01:26:58): the WPM3i commands the backup heater
  in 2-min steps. With the fuses off the tank peaked at **49.7 °C** (01:47) and stayed at ~49 °C; no error.
- The run **never ended**: still at 05:26; heating stayed off ~4.7 h (house 20.6 °C, little loss).
- Antilegionellen set to 0 by the ESP (05:26:42, owner's request): the run went on. **Programmschalter
  "Bereitschaft" (05:40:18) ended it within ~30 s** (valve 0, NHZ Aus); Programmschalter back to Eco 05:41:55;
  heating restarted on its own (~06:00).
- Open: the start time (01:00 fixed or from the setting time?), the target temperature, how the run ends with
  working NHZ, a time-out. Next: a test with the fuses on.
