<!-- Source: Home Assistant history API, queried 2026-11-15. Times in UTC. Values as recorded by HA. -->
# HA history observations, 2026-11-15

## number.heatpump_raumeinfluss (value changes since 2026-11-01)
- 2026-11-05 09:57  2.0
- 2026-11-15 12:11  10.0   (old firmware boot, FEK unplugged)
- 2026-11-15 12:36  2.0    (FEK re-attached around this time)
- 2026-11-15 13:27  10.0   (ported firmware, FEK removed)

## binary_sensor.heatpump_verdichter around the port flash (13:22:13)
- 13:22:32 on, 13:25:04 off (normal compressor stop, 3 min after the flash)

## Last value before the port flash vs. 2026-11-15 ~15:30 UTC (selection)
- HK Soll 24.2 -> 22.9 °C, Vorlauf Soll 25.1 -> 22.9 °C (FEK removed)
- Leistung Verdichter 829 -> 0 W, Stromaufnahme 3.7 -> 0 A, Heizgas 60 -> 23.7 °C (compressor off)
- TBD_02 (Manager/MFG) 33 -> 100, TBD_08 57 -> 100 (changed with compressor stop)
- TBD_09 1, TBD_11 2 -> no values (listened on node 0x100, which is no longer a configured node)
- Totals unchanged: El Energieaufnahme Heizen 13.153 MWh, WW 5.207 MWh, Wärmeertrag Heizen 76.828 MWh, WW 15.324 MWh,
  Verdichterstarts 24181, Betriebsstunden VD Heizen 7585, WW 1342

## Short API disconnects (1-2 s unavailable, values restored immediately = no reboot)
- 13:39:15, 14:31:44, 14:33:52
