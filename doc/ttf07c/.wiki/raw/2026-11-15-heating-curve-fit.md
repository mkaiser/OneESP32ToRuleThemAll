# Heating curve fit, 2026-11-15

Source: Home Assistant history 2026-11-08 00:00 UTC to 2026-11-15 ~22:00 local of
`sensor.heatpump_vorlauf_soll_temperatur` (HK1 `0x0004`, the WPM2's flow setpoint, FEK unplugged),
`sensor.heatpump_aussentemperatur` and `select.heatpump_programmschalter`. WPM2 settings at the time: Komfort 23.0 °C,
Eco 19.5 °C, Steigung HK1 0.26, Raumeinfluss 10 (no room sensor, so no room influence).

Model: `Vorlauf - Raumsoll = S * (Raumsoll - Aussen) + b`, Raumsoll = Eco or Komfort temperature by Programmschalter.

| Outdoor temperature used | n | S | b | rms | max |
|---|---|---|---|---|---|
| instantaneous | 146 | 0.243 | 0.46 | 0.05 K | 0.09 K |
| instantaneous, S fixed 0.26 | 146 | 0.26 | 0.23 | 0.06 K | |
| 1 h mean | 146 | 0.253 | 0.33 | 0.10 K | 0.25 K |
| 3 h mean | 146 | 0.238 | 0.52 | 0.21 K | 0.48 K |

Rows: 139 in Eco, 7 in Komfort (2026-11-08 12:11-13:21, 26.7-26.9 °C at 9.0-9.5 °C outside).

Check against the real FEK (capture 2026-11-15 19:33): FEK settings Raumsoll 21.5 (verstellt), Steigung 0.24, outside
7.9 °C: 21.5 + 0.24 * 13.6 + 0.23 = 24.99 °C; the FEK sent 25.0 °C (room 21.1 °C) and 25.4 °C right after plug-in
(room 20.8 °C).
