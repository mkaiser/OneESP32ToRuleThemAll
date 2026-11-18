# Errors (Fehler) of the WPM3i

See also: [Betriebsstatus](betriebsstatus.md), [CAN bus](can-bus.md), [TTF07 C registers](ttf07c-registers.md).

## Current error number: `0x1388`

The Manager (`0x480`) writes `0x1388` to the control panel (`0x100`) every ~3.5 min: 0 = no error, otherwise the
error code of the active error. Firmware: `FEHLERNUMMER_WPM`, HA "Fehlernummer"
(`sensor.hwr_warmepumpe_fehlernummer`, since 2026-11-17; was `TBD_12`). Upstream's `FEHLERMELDUNG` (`0x0001`) stays 0
on this heat pump. Error 21 (Keine Leistung) could not be acknowledged on the panel; a power cycle of the heat pump
cleared it ([log](log.md), 2026-11-17).

## Error list (Diagnose > Fehlerliste): `0x0B9A`–`0x0BA3`

The panel keeps no copy. When the list is opened, the panel **writes** `0x0B9A` = start index (0, then 6, 13, 15, 17,
18 while paging) to the Manager, and the Manager answers with one block of writes per entry, ~20 ms apart
([capture](../raw/captures/2026-11-17-1419-fehlerliste.log), [panel](../raw/2026-11-17-fehlerliste-panel.md)):

Fields (index, code, minute, hour, day, month, year; one register each): see [TTF07 C registers](ttf07c-registers.md),
Manager section. Example entry 0: index 0, code 21, 13:11 on 17.11.26.

Read requests for these addresses return `0x8000`, so the list can only be fetched the way the panel does (a write
of `0x0B9A`). 20 entries. The Manager answers to `0x100` even when the ESP (`0x680`) asks; the ESP listens.

**Cursor (test 2026-11-17 14:44):** the value written to `0x0B9A` is ignored; every request returns the **next**
entry (requests 0, 0, 0, 3, 0 returned entries 0, 1, 2, 3, 4), and after a pause of about a minute or more the next
request starts at entry 0 again. Each answer names its index in `0x0B9A`. With requests 2–4 s apart all fields
arrive; in the panel's fast burst and sometimes otherwise the ESP misses single frames.

**Firmware (since 2026-11-17, maintainer's decision):** script `fehlerliste_lesen` requests 5 entries 2 s apart, 2
min after boot, once a day and when "Fehlernummer" changes to a new error; if fields are missing it waits 2 min (cursor
reset) and reads the 5 entries again, keeping what it has. HA: "Fehlerliste" (5 newest, `DD.MM.YY HH:MM Text (Code)`,
missing fields `??`), "Letzter Fehler", "Fehler aktuell" (text of "Fehlernummer"). The write does nothing else (panel
reads continued normally, 14:33 test).

## Error codes

| Code | Panel text | Seen |
|---|---|---|
| 18 | HOCHDRUCK | 2026-11-17 20:24 (compressor started by Quick start; reset 21:45, compressor ran normally afterwards) |
| 21 | KEINE LEISTUNG | 2026-11-17 13:11 (compressor started without power, [test](betriebsstatus.md)) |
| 22 | NIEDERDRUCK | 2026-01-09 18:31 |
| 130 | FÜHLERBRUCH E 130 | 2026-01-09 18:28 |
| 8036 (`0x1F64`) | TO P SOL MFG | 2025-04-01 (timeouts of the MFG, probably during commissioning or an update) |
| 8039 (`0x1F67`) | TO PU SOL MFG | 2025-04-01 |
| 8040 (`0x1F68`) | TO VENTIL MFG | 2025-04-01 |
| 8041 (`0x1F69`) | TO DHC MFG | 2025-04-01 |

The codes 8036–8041 were matched by position in the list; the ESP log lost part of the burst, so 8037/8038 and
the gaps are open. "TO" = timeout; PU SOL = Sole pump, P SOL = probably the Sole pressure, VENTIL = valve, DHC = DHC
(probably the hot water / changeover). Unconfirmed.
