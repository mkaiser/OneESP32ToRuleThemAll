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
answers (`22 00 04 00 F4` = 24.4 °C) the lag is gone (maintainer, 10:59;
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

Decision (maintainer): the emulation **stays on** as the heating control.
[capture](../raw/captures/2026-11-16-0954-fek-emulation-flow-setpoint.log)
