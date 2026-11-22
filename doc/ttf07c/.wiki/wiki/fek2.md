# FEK2 (room control unit)

See also: [CAN bus](can-bus.md), [Cooling](cooling.md), [Heating control](heating-control.md) (modes, FEK detection, emulation with flow setpoint).

The FEK2 measures room temperature and humidity. It is normally **unplugged** on this installation.

## Goal

Remove the FEK for good and let the ESP provide the room temperature and humidity from the house sensors in Home
Assistant, so the heat pump keeps control and cooling is not blocked (owner, 2026-11-15). For that, the ESP has
to reproduce what the FEK sends.

Status (2026-11-16): **replaced.** The ESP emulates the FEK with its own flow setpoint, the WPM3i heats with it and
shows the "Kühlen" menu; it runs permanently since 2026-11-16 (test: [Heating control](heating-control.md)). The
real FEK is detached.

Summary of what is known:
- The FEK registers as node `0x301` (HK1) and **is** HK1 while registered: the WPM3i's own HK1 goes silent, and the
  FEK answers HK1 reads with its own parameters.
- It **sets the flow setpoint** (Kessel `0x0002`, `0x601` `0x0004`), so it controls heating. With the real FEK the
  compressor stopped right at registration (17:51) and waits for this setpoint.
- Registration is kept by answering the WPM3i's 8-min presence check; one missed check gives HK1 back to the WPM3i.
- The "Kühlen" menu entry needs the FEK; its identification for the control panel (`0x0199` software version 416,
  `0x019A` revision 3) is enough for the emulation (confirmed 21:06).

## Behaviour

- **With the FEK attached, it takes over control.** It sets the target temperatures for HK Soll, and the heat pump
  stops regulating by itself (old notes, [raw](../raw/2026-11-15-old-ttf07-yaml-notes.md)).
  - 2026-11-15 ~13:2x UTC, FEK removed: HK Soll / Vorlauf Soll went from 24.2 to 22.9 °C, and the compressor stopped
    about 3 minutes later ([raw](../raw/2026-11-15-ha-history-observations.md)).
  - 2026-11-15 17:50 local, FEK plugged in: **the compressor stopped in the same second as the FEK's first write**
    (test below).
- **Without the FEK, the WPM blocks cooling** (no room temperature or humidity, so no dew point protection).
- **Room values:** on 2026-11-15 around 13:40 local (FEK attached), frames from `0x301` wrote `RAUMISTTEMP` (`0x0011`)
  and `RAUMFEUCHTE` (`0x0075`) to `0x601` about every minute (20.9 °C, 44.2 %; ID bytes `0xC0 0x01` = write to
  `0x601`). The firmware shows them as "FEK2 Raumtemperatur/Raumfeuchte HK1" (listen only).
  In the plug-in test (17:50–18:11) **no room value frames appeared at all**; at 19:33 they came every 10–45 s on
  change (raw `C0 01 11 00 D0 00 00` = 20.8 °C, short form). Why the FEK was silent at 17:50 is unknown.
- **Raumeinfluss** (`0x010f` on HK1) reads **10 without the FEK and 2 with it attached** (HA history 2026-11-05 to
  2026-11-15, [raw](../raw/2026-11-15-ha-history-observations.md)). The FEK apparently brings its own value.
  Confirmed 2026-11-16: Raumeinfluss is set **on the FEK** (the WPM3i panel's "Heizkreis 1" then shows only "Minimal
  Temperatur"; Komfort/Eco/Steigung/Raumeinfluss move to the FEK. In that menu the panel reads KOMF_TEMP, ECO_TEMP,
  STEIGUNG_HK1 and `0x4EA7` from `0x601`, which does not answer). Changing it 2 → 4 on the FEK sent only `0x010F` = `0x0400` to `0x601`; the FEK applies it itself and
  sends the finished flow setpoint ([capture](../raw/captures/2026-11-16-1123-real-fek-attached.log)).
- **FEK settings are not sent when they change** (2026-11-16 18:35, [capture](../raw/captures/2026-11-16-1833-fek-settings.log)):
  Steigung 0.24 → 0.25, Eco 19.9 → 20.0 and Komfort 21.0 → 21.1 on the FEK produced no frame. The FEK keeps them; they
  appear only in answers to HK1 reads (`0x010E`, `0x0008`, `0x0005` answered by `0x301` with the new values) and,
  for the active phase, in the next periodic block (18:37:59: Raumsoll `0x0012` 21.0 → 21.1, flow setpoint `0x0002`
  24.7 → 24.8 °C). Only the Raumeinfluss `0x010F` is sent at once (again 2026-11-16 18:32:30 2 → 3, 18:33:12 → 2,
  [capture](../raw/captures/2026-11-16-1804-fek-plugin-raumeinfluss.log)). `0x0029`/`0x002A` did not change with any
  of these.
- `0x006E` to the Kessel is **not constant**: `0x0100` on 2026-11-15, `0x0200` on 2026-11-16 (the emulation copies
  `0x0100`). The FEK sent its setpoint at irregular intervals on 2026-11-16 (11:30:21, 11:31:00, 11:37:18, 11:37:58).

## Plug-in test, 2026-11-15 17:46–18:11 local

Recorded with the type-aware log ([capture](../raw/captures/2026-11-15-1746-fek-plugged-in.log),
[analysis](../raw/2026-11-15-1746-fek-plugged-in-analysis.txt)). FEK plugged in at ~17:50:30, heating running.

| Time | Frame | Meaning (interpretation) |
|---|---|---|
| 17:50:35 | `0x301` → `0x301`, system, `0x00FD` = `0x0900` | registration / presence (value differs from the regular `0x0800`) |
| 17:51:34 | `0x601` → HK1 `0x301`, **write**, `0x0052` = 0 | unknown property `0x0052`; same second as the compressor stop |
| 17:51:34 | WPM3i status `0x40C1` → `0x00C1` | compressor off; pumps stopped by 17:56 (`0x0041` → `0x0001` → `0`) |
| from 17:51 | **HK1 (`0x301`) no longer answers the ESP's reads** | Vorlauf Soll (every minute) and the 18:01 settings refresh unanswered; before, answers in < 1 s |
| every 7 min | `0x601` → HK1, system, `0x00FE` = `0x0100` | also without the FEK (seen 17:04–17:20), so not caused by the FEK |
| every 8 min | `0x301` system `0x00FD` = `0x0800` + system response `0x0100`, then `0x680` system `0x00FD` = `0x0800` | also without the FEK |

Confirmed later (19:33 capture): without the FEK the WPM3i answers for `0x301` (HK1) itself; an attached FEK takes
over `0x301`, writes the room values to `0x601`, and the WPM3i's own HK1 goes silent.

## Unplug test, 2026-11-15 18:37 local

FEK unplugged at ~18:37. At the next 8-min round (18:40:00) the WPM3i's check for `0x301` stayed unanswered; 34 s
later HK1 answered the ESP again. At 18:48 the WPM3i no longer checked `0x301` at all: the FEK was deregistered after
one unanswered check. Sources: captures 18:13–18:28 and 18:35–18:55 (in the log of the
[emulation test](../raw/captures/2026-11-15-1851-fek-emulation-long-form.log)).

Registration model (consistent with all captures): a device registers for a node with a system message
`ANMELDUNG` (`0xfd`) = `0x0900`. The WPM3i then checks the node every 8 minutes (system message `0x0800`, sent with the
node's own CAN ID); the device answers with a system response `0x0100`. While registered, the WPM3i's own HK1 stays
silent. One unanswered check deregisters it. The checks for `0x680` (the ESP's ID) work the same way; something
registered `0x680` once, and the checks are never answered.

## FEK emulation by the ESP, 2026-11-15

Firmware at the time of these tests: switches "FEK Emulation" (registration + answers to the check) and "FEK
Emulation Raumwerte" (room values from HA every 60 s). Since 23:02 replaced by the select "Heizungssteuerung" with flow
setpoint, see [Heating control](heating-control.md).

- **First attempt (18:51, long-form frames `66 01 FA 00 FD 09 00`):** not understood. HK1 kept answering, and `0x301`
  was not checked. `0x601` did write `0x0052` = `0x0100` to `0x301` once (18:53:44), at the start of hot water
  ([capture](../raw/captures/2026-11-15-1851-fek-emulation-long-form.log)).
- **System messages use the short form** `[id0, id1, property, value_hi, value_lo, 0, 0]`, e.g. the check
  `D6 00 FD 08 00 00 00` (raw bytes logged since 19:09).
- **Second attempt (19:13:47, short form `66 01 FD 09 00 00 00`, room values `C0 01 11 …` / `C0 01 75 …`):
  accepted.** HK1 went silent. At 19:20:00 the WPM3i checked `0x301` (`66 01 FD 08 00 00 00`), and the ESP answered
  after 13 ms (`67 01 FD 01 00 00 00`), like the real FEK
  ([capture](../raw/captures/2026-11-15-1913-fek-emulation-short-form.log)).
- **The cooling menu entry did not appear**, neither with registration only nor with room values (19:01–19:21).
  Emulation switched off at 19:21:42.
- Unknown: whether the entry appears with the real FEK at all. The real FEK's room-value frames have not been
  captured with raw bytes yet (short or long form?).

## Real FEK protocol, 2026-11-15 19:33 local (raw bytes)

The FEK was fully active this time, and **the "Kühlen" menu entry appeared**
([capture](../raw/captures/2026-11-15-1933-real-fek-plug-in-raw.log)). The FEK uses CAN ID `0x301`. Frames
are short form unless marked "long".

| When | Frame(s) | Meaning (interpretation) |
|---|---|---|
| +0 s | `66 01 FD 09 00 00 00` | registration for `0x301` |
| +10 s, then every 7 min | system `0x00FE` to Kessel `36 00 FE 01 …` and to `0x601` `C6 01 FE 01 …`; both answer (system response) | presence among the nodes |
| +10 s | reads JAHR, MONAT, TAG (long), `0x0009`, AUSSENTEMP, `0x000B` from the Kessel | clock and outdoor temperature |
| every ~66 s | read `0x0009` from the Kessel, e.g. `0x2213` | time: low byte = hour (19), high byte = minute (34) |
| +11 s, then every ~3.5 min | writes to Kessel: `0x0002` = flow setpoint (250–254 = 25.0–25.4 °C), `0x0058` = `0x0200`, `0x006E` = `0x0100` | **the FEK sets the flow setpoint** |
| +11 s, then every ~3.5 min | `0x601` writes to the FEK: `0x0010` = 2, `0x000F` = `0xFE70`, `0x0004` = `0xFE70`, `0x0052` = `0x0100`, `0x0056` = 0, `0x0057` = 0, `0x0028` = 300 | configuration / status from `0x601` (`0xFE70` = -40.0 = no value) |
| +13 s, then every ~3.5 min | FEK writes to `0x601`: `0x0058` = `0x0200`, `0x0029` = `0x0A00`, `0x002A` = `0x1E00`, RAUMEINFLUSS (long) = `0x0200` (2), VERSTELLTE_RAUMSOLLTEMP = 215 (21.5 °C); reads `0x0011`, `0x0012`, `0x000F`, `0x0004` from `0x601` (answers `0xFE70`) | FEK parameters to the room control |
| every 10–45 s, on change | `C0 01 11 00 D0 …` (RAUMISTTEMP 20.8 °C), `C0 01 75 02 32 …` (RAUMFEUCHTE 56.2 %) | room values |
| every ~3 min | write VORLAUFSOLLTEMP `0x0004` to `0x601` (250/253) | flow setpoint again |
| +23 s, once | control panel `0x100` reads `0x0199` and `0x019A` (long) from `0x301`; FEK answers `22 00 FA 01 99 01 A0` (= 416) and `22 00 FA 01 9A 00 03` (= 3) | **FEK identification (type/version?), likely the trigger for the "Kühlen" menu** |
| 8-min check | `66 01 FD 08 …` → FEK `67 01 FD 01 …` | presence check, see above |
| on request | answers HK1 reads with **its own** parameters: KOMF_TEMP 21.0, ECO_TEMP 19.9, STEIGUNG_HK1 0.24, RAUMEINFLUSS 2, VORLAUFSOLLTEMP 25.0–25.2 | the FEK *is* HK1 while registered |

Consequence for replacing the FEK: answering the control panel and the system messages is probably enough for the
menu. Taking over heating means computing the flow setpoint (heating curve + room influence) and sending it to the
Kessel (`0x0002`) and `0x601` (`0x0004`), and answering HK1 reads.

## Emulation with identification, 2026-11-15 21:06 local: "Kühlen" menu appears

After the real FEK was released (21:04 check unanswered), the ESP registered with the extended emulation: system
messages `0x00FE` to Kessel and `0x601` (both answered), room values, and the answer to the control panel's
identification read. `0x601` sent the same configuration set as to the real FEK. The control panel read `0x0199`
(21:06:26), the ESP answered `22 00 FA 01 99 01 A0` within 3 ms; the panel did **not** read `0x019A` afterwards.
**The "Kühlen" menu entry appeared** (confirmed by the owner). The menu's values come from the Kessel and the
WPM3i, see [Cooling](cooling.md). No flow setpoint is sent by the emulation.

**Heating with the emulation on:** the compressor stopped at 21:07, one minute after the emulation registered (status
`0x40C0` → `0x0040`), the same pattern as with the real FEK at 17:51. HK Soll stayed at 22.7 °C (the WPM3i's last
value). It stayed off until the emulation was switched off at 21:40:36 (released at the 21:44 check). Most likely the
heat pump waits for the FEK's flow setpoint (`0x0002` to the Kessel), which the emulation does not send. Confirmed
on 2026-11-16: with the flow setpoint the compressor starts and runs ([Heating control](heating-control.md)).
([capture](../raw/captures/2026-11-15-2059-emulation-identification-menu.log))

## Open

- Meaning of the unknown properties. Named on 2026-11-16 in `property.h` (TTF_07_C):
  The names, evidence and status of these registers are in [TTF07 C registers](ttf07c-registers.md).

  FEK behaviour seen in that test: changes are sent **at once** (`0x0058`, `0x0012`, `0x0002` within a second of
  the change), besides the periodic block. Betriebsart **Aus** = room setpoint 5.0 °C (frost protection) and flow
  setpoint 5.0 °C. The FEK's own room sensor needed ~20 min after plug-in to settle (19.8 → 21.2 °C).

  Plug-in 2026-11-16 18:14:10 (after the emulation was released at the 18:08 check): `0x006E` = `0x0200` in the first
  block (18:14:21), `0x0100` from 18:15:12 on, i.e. the opposite direction of the 12:33 plug-in (`0x0100` → `0x0200`).
  Also the registration sequence: `0x00FE` system message to the Kessel and `0x601` (+10 s), Kessel answers with
  date, time, outdoor temperature and `0x000B` (`0x8000`), first block at +11 s
  ([capture](../raw/captures/2026-11-16-1804-fek-plugin-raumeinfluss.log)).

  `0x006E` (FEK → Kessel) is **not** the Betriebsart, the phase, the room setpoint or the compressor: `0x0200` in
  Eco, Komfort, Aus and Zeit, and with the compressor on or off; `0x0100` only after plug-in (2026-11-16 12:33:44
  → `0x0200` at 12:34:35 without a known action; 2026-11-15 19:33–20:15 the whole time). Meaning open.

  Still unknown (values identical in all captures): FEK → `0x601` `0x0029` = `0x0A00`, `0x002A` = `0x1E00` (10 and 30 if little endian, like RAUMEINFLUSS);
  `0x601` → HK1 `0x0010` = 2, `0x0056`/`0x0057` = 0, `0x005A` = `0x0200`; FEK reads `0x000B` from the
  Kessel (`0x8000`). (`0x0199`/`0x019A` = software version/revision, upstream `FET_SOFTWARE`/`FET_SOFTWARESTAND`.)
  A web search for the Elster index table found nothing usable (2026-11-16).
- 2026-11-17 ([menus and ranges](../raw/2026-11-17-fek2-menus.md),
  [capture](../raw/captures/2026-11-17-1446-fek-replug-006e.log)): no FEK setting shows 10 or 30 (Heizen: Komfort,
  Eco, Raumeinfluss, Steigung; Allgemein: Sprache, Kontrast, Helligkeit, Korrekturen, Touch). Ranges: Komfort max
  **30.0 °C** (= `0x002A` = 30 and `0x601`'s `SOLLWERT_MAX_HK1` 30.0), Eco min 5.0 °C, Raumeinfluss 0–20. So
  `0x002A` is very likely the room setpoint maximum (30 °C). Komfort goes down to **5.0 °C** (checked 16:55), like
  Eco, so `0x0029` (10) is **not** the setpoint minimum; its meaning is open. `0x0029`/`0x002A` did not change while Komfort/Eco were changed.
  `0x006E` after plug-in: 14:46 (plugged in during an ESP reboot) `0x0100` for 50 min without a flip; replugs 15:39:23 and
  15:45:31: first block `0x0200`, `0x0100` after ~50 s both times (as on 2026-11-16 18:14). Only 2026-11-16 12:33 went the other way.
  Meaning still open (a start-up state of the FEK?).
  **Decision 2026-11-22:** across all captures the FEK sends `0x0200` in the first block after
  registration and `0x0100` ~50 s later (2026-11-16 18:14, 2026-11-17 15:39 and 15:45); longer `0x0200` phases only
  after a cold start (2026-11-16 from 12:34 for hours, 2026-11-20 12:00:48–14:00:24, ~2 h; room ≥ setpoint from 12:43, so
  not a heat demand). Likely a start-up state (e.g. the FEK's own room sensor settling). No effect seen (the pump kept
  running through the 14:00 change); the emulation keeps sending `0x0100` (the steady state). Not followed up.
- What is `0x601`? It exists without the FEK, receives the room values and the FEK's parameters, and configures the
  FEK: probably the WPM3i's room control logic for HK1.
- Why did the real FEK send no room values in the 17:50 test?
- Heating curve and compressor with the emulation: answered, see [Heating control](heating-control.md).
