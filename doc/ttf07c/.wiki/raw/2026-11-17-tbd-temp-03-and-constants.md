# TBD_TEMP_03 and the constant TBD values: HA history analysis, 2026-11-17

Source: Home Assistant history (REST `history/period`, `minimal_response`), 2026-11-15 16:15 UTC to 2026-11-17
07:15 UTC (40 h), all entities of the device `heatpump-ttf07c` plus `sensor.temperatur_haus_mittel`,
`sensor.openweathermap_temperatur`, `sensor.og_badezimmer_thermometer_temperatur`. Times below are UTC
(local = UTC + 1). Analysis by an agent; no frames were written to the heat pump.

Note: the HA history API returns one day by default; pass `end_time` for longer windows.

## TBD_TEMP_03 (`0xfe09`, MFG)

Range 18.2–19.8 °C over 40 h.

Correlation (5-min grid, best lag 0/30/60/120 min):

| Signal | r | Lag |
|---|---|---|
| Leistung Warmwasserbereitung | +0.85 | 0 |
| Vorlauf Ist NHZ / WP | +0.81 / +0.79 | 0 |
| Umschaltventil Warmwasser | +0.79 | 0 |
| Leistung Verdichter / Stromaufnahme | +0.71 | 0 |
| Haus mittel | +0.33 | 30 min |
| Außentemperatur | not in the top 20 (outdoor fell from 8 to −0.4 °C overnight, TBD_TEMP_03 stayed 18.5–18.8) |

Step response at compressor transitions (HA timestamps, the value is polled about every 5 s):

| Time | Event | TBD_TEMP_03 |
|---|---|---|
| 2026-11-16 18:21:06 | hot water valve 100 | 18.5 |
| 18:22:12 | compressor on (hot water, ~1.25 kW) | 18.5 → 19.2 → 19.5 within 5 s |
| 18:22–19:24 | hot water charging (flow up to 57 °C) | 19.3–19.8 |
| 19:24:37–19:24:57 | compressor stopping | 19.7 → 19.3 → 19.1 → 19.0 → 18.6 within 20 s |
| 19:25:02 | compressor off (power reading) | 18.6 |
| 20:27:07 | compressor on (heating, ~0.84 kW) | 18.4 → 18.5 → 18.7 within 5 s |
| heating runs overnight | | 18.7–18.8 while running, 18.5–18.6 while off |

Conclusion: the value follows the compressor **within seconds** (+0.2–0.3 K heating, +1 K hot water) and returns
as fast when it stops. A room or housing temperature cannot change 1 K in 5–20 s, and the outdoor temperature
has no influence. So it is **not the installation room**. It sits on the MFG next to `STROMAUFNAHME` (`0xfe07`) and
`VERSORGUNGSSPANNUNG` (`0xfe0a`), so it is probably measured on the electronics (a board/inverter temperature,
or a sensor whose reading shifts with the compressor load). Unconfirmed.

## Constant TBD values (40 h, including heating runs, hot water charging, and several reboots)

| Entity | Address | Node | Value |
|---|---|---|---|
| TBD_04 | `0xfe4c` | MFG | 18 |
| TBD_07_WPM2 / TBD_07_MFG | `0xfe1e` | Manager / MFG | 0 |
| TBD_09 | `0x06af` | Bedienteil | 1 |
| TBD_10_* | `0x00fe` | Kessel, Manager, MFG | 256 (`0x0100`) |
| TBD_11 | `0x4e8b` | Bedienteil | 2 |
| TBD_12 | `0x1388` | Manager | 0 |
| TBD_13 | `0x080e` | Manager | 0 |
| TBD_16 | `0x067a` | Bedienteil | no answer (unknown) |
| TBD_17 | `0x01c0` | Kessel | 36864 (`0x9000`) |
| TBD_18 | `0x068f` | Kessel | 1 |

None changed. They are settings or states that the operating cycle (heating, hot water) does not touch.
`TBD_10` = `0x00fe` is the index of the 7-min presence system message among the nodes (value `0x0100`; see
`can-bus.md`), so reading it as a property just returns that value: no setting behind it.

No NHZ activity in the 40 h: Betriebsstatus `0x4e5e` never had bit 4 or 5 set; the NHZ binary sensors stayed off.
Values seen in `DEBUG_BETRIEB`: `0000000000000000`, `…0001`, `…01000000`, `…01000001`, `…11000000`, `…11000001`,
`0000001001000000`, `0000001011000000`, `0100000001000001`, `0100000011000000`, `0100000011000001`,
`0100001011000000`.
