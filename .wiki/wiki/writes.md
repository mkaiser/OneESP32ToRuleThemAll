# What the firmware writes to the heat pump

Every write the firmware makes to the TTF07 C / WPM3i, and who approved it. Rule: [`AGENTS.md`](../../AGENTS.md)
("The heat pump is live"). Registers: [TTF07 C registers](ttf07c-registers.md).

## Automatic writes (approved)

| Write | When | Approved | Details |
|---|---|---|---|
| `0x0B9A` to the WPM3i (error list request, script `fehlerliste_lesen`) | 2 min after boot, once a day, and when "Fehlernummer" shows a new error | maintainer, 2026-11-17 | It only triggers the WPM3i's answer; [errors](errors.md) |
| Warmwasserprogramm time windows to the Kessel (`0x1710`–`0x1772`) | only when a text "Warmwasserprogramm Montag" … "Sonntag" is changed in HA | maintainer, 2026-11-17 | Reads every 15 min and 90 s after boot write nothing |
| FEK emulation: registration and flow setpoint as HK1's FEK | while the select "Heizungssteuerung" is "FEK Emulation" | maintainer, test passed 2026-11-16 | Never starts while a real FEK is detected; [heating control](heating-control.md) |

## Writes from HA entities

Numbers, switches and selects write when they are changed in HA. HK1 settings are locked while the FEK emulation
owns HK1 (`hk1_settings_write_lock`). Change one only when the maintainer asked for that change.

Any other automatic write needs the maintainer's approval first, and a row here.
