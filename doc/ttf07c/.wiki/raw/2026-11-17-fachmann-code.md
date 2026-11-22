# Expert code on the control panel: CAN traffic, 2026-11-17

The maintainer entered the expert code (1000, accepted) on the WPM2 control panel (`0x100`) at ~17:36:21–17:36:33
and then browsed several expert menus (pages not noted). Passive capture by the ESP, nothing written by the ESP.
Panel frames: [capture](captures/2026-11-17-1736-fachmann-code-panel-traffic.txt) (`time src>dst kind addr name value`).

## Code entry

No frame carries the code. Between 17:36:14 and 17:36:33 the panel sent only its presence message (`0x00FE`) and
`TBD_11` (`0x4e8b`) = 2 to the Manager, as it does without code entry. The panel checks the code locally; the access
level is not visible on the bus.

## After the code (17:36:33–17:38)

- The panel reads `0x06AE` from the Manager about every 2 s (always 0; also read once at 17:36:13 before the code).
- Writes by the panel: only `TBD_09` (`0x06af`) = 1 (about every 5–30 s while browsing) and the error list requests
  `0x0B9A` = 0…18 at 17:37:17 (no setting was changed).
- First reads per address (node, value):

| First read | Node | Address | Name in `property.h` | Value |
|---|---|---|---|---|
| 17:36:48 | Kessel | `0x01b0` | `QUELLENTEMP_MIN` | `0xFFA6` = −9.0 °C |
| 17:36:48 | Kessel | `0x070c` | `LEISTUNG_SOLEPUMPE` | 65 % |
| 17:36:48 | Kessel | `0xfdae` | `QUELLENMEDIUM` | 0 |
| 17:36:50 | Kessel | `0xfdb0` | `REGLERDYNAMIK` | `0x1E00` |
| 17:36:50 | Kessel | `0x070f` | ? | `0x8000` |
| 17:36:50 | Kessel | `0x01a2` | `HDSENSORMAX` | 440 (44.0 bar) |
| 17:36:50 | Kessel | `0x070a` | `LEISTUNG_HEIZKREISPUMPE` | 40 % |
| 17:36:52 | Kessel | `0x070b` | `LEISTUNG_WARMWASSERPUMPE` | 65 % |
| 17:36:52 | Kessel | `0x0705` | ? | `0x8000` |
| 17:36:53 | Manager | `0x0030` | ? | `0x8000` |
| 17:36:53 | Kessel | `0xfdc0` | ? | `0x8000` |
| 17:36:53 | Kessel | `0xfdb1` | `VERDICHTER_STILLSTAND` | `0x3C00` |
| 17:36:53 | Kessel | `0x0914` | ? | `0x8000` |
| 17:36:53 | **`0x514`** (new node) | `0xc32f` | ? | `0x8000` |
| 17:36:53 | Manager | `0x4eba` | ? | `0x8000` |
| 17:36:53 | Kessel | `0x070e` | `EINPHASIGER_BETRIEB` | 0 |
| 17:36:53 | Manager | `0x0669` | ? | 0 |
| 17:36:57 | Manager | `0x4e5a` | ? | 0 |
| 17:36:59 | Manager | `0x0658`, `0x0659`, `0x065a` | ? | 0 |
| 17:37:04 | Manager | `0x0112`, `0x0122`–`0x0126` | `PROGRAMMSCHALTER`, date/time | Eco, 17.11.26 |
| 17:37:04 | Kessel | `0x011a` | ? | 0 |
| 17:37:04 | Kessel | `0x000c`, `0x000e`, `0x0016` | outdoor, hot water, return | 10.0, 42.8, 26.0 °C |
| 17:37:05 | Manager | `0x068e` | `KUEHLEN_TBD_068E` | 20 |
| 17:37:06 | Manager | `0x0691`, `0x0692` | ? | 0 |
| 17:37:07 | Manager | `0x0074` | ? | 1 |
| 17:37:09 | Manager | `0x0668` | ? | 53 |
| 17:37:15 | Manager | `0x0294` | ? | 63 |
| 17:37:21 | Manager | `0xfdbf` | ? | 0 |
| 17:37:26 | Kessel | `0xfdb2`, `0x0013`, `0x0a06` | `KUEHLEN_TBD_FDB2`, hot water setpoints | `0x0100`, 52.0, 45.0 °C |

To name the unknown addresses, a guided pass is needed: one expert page at a time with its displayed values.
