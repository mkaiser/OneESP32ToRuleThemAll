# What the firmware writes to the heat pump

Every write the firmware makes to the TTF07 C / WPM3i, and who approved it. Rule: the firmware writes to the heat pump only what the owner approved.
("The heat pump is live"). Registers: [TTF07 C registers](ttf07c-registers.md).

## Automatic writes (approved)

| Write | When | Approved | Details |
|---|---|---|---|
| `0x0B9A` to the WPM3i (error list request, script `fehlerliste_lesen`) | 2 min after boot, once a day, and when "Fehlernummer" shows a new error | owner, 2026-11-17 | It only triggers the WPM3i's answer; [errors](errors.md) |
| Warmwasserprogramm time windows to the Kessel (`0x1710`–`0x1772`) | only when a text "Warmwasserprogramm Montag" … "Sonntag" is changed in HA | owner, 2026-11-17 | Reads every 15 min and 90 s after boot write nothing |
| FEK emulation: registration and flow setpoint as HK1's FEK | while the select "Heizungssteuerung" is "FEK Emulation" | owner, test passed 2026-11-16 | Never starts while a real FEK is detected; [heating control](heating-control.md) |

## Manual writes on request (one-off)

| Write | When | Requested | Details |
|---|---|---|---|
| Kessel `0x0101` = 0 (Antilegionellen setting off) via the ESP action `can_send_value` | 2026-11-22 05:26:42 | owner ("switch legionellen off") | Kessel confirmed 0; the running disinfection did not stop |
| Programmschalter "Bereitschaft", then back to "Eco" (HA select) | 2026-11-22 05:40:18 / 05:41:55 | owner ("try to end it by software") | ended the hot water run; Eco restored by Claude to the previous value |
| FEK emulation settings: Komfort 23.0 → 21.5 °C, Eco 19.5, Steigung 0.26, Betriebsart Eco → Komfort; Heizungssteuerung "FEK Emulation" | 2026-11-21 20:19–22:11 | owner | after the overnight failure of 2026-11-20/21; Eco 21.5 set by the owner |

## Writes from HA entities

Numbers, switches and selects write when they are changed in HA. HK1 settings are locked while the FEK emulation
owns HK1 (`hk1_settings_write_lock`). Change one only when the owner asked for that change.

Any other automatic write needs the owner's approval first, and a row here.
