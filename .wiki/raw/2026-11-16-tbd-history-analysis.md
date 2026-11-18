# 2026-11-16: TBD_* values vs. known values (HA history)

Source: HA history API, 7 days back from 2026-11-16 13:47 (recorder keeps changes only; several TBD
entities have few points). Scripts: correlation on a 1-min grid (forward fill), value comparison, and
transition listing with the pump/compressor binary sensors 30 s after each change.

## Correlations (|r| top 6 per TBD entity)
```

== sensor.heatpump_tbd_04: n=2 changes, min=18.0 max=18.0 distinct=[18.0]

== sensor.heatpump_tbd_09: n=2 changes, min=1.0 max=1.0 distinct=[1.0]

== sensor.heatpump_tbd_11: n=2 changes, min=2.0 max=2.0 distinct=[2.0]

== sensor.heatpump_tbd_12: n=2 changes, min=0.0 max=0.0 distinct=[0.0]

== sensor.heatpump_tbd_13: n=2 changes, min=0.0 max=0.0 distinct=[0.0]

== sensor.heatpump_tbd_15: n=2 changes, min=10.0 max=10.0 distinct=[10.0]

== sensor.heatpump_tbd_19: n=1267 changes, min=233.0 max=556.0 distinct=[233.0, 234.0, 235.0, 236.0, 237.0, 238.0, 239.0, 240.0, 241.0, 242.0, 243.0, 244.0]...
   r=+1.00  sensor.heatpump_ruecklauf_ist_temperatur
   r=+0.89  sensor.heatpump_vorlauf_ist_temperatur_nhz
   r=+0.88  sensor.heatpump_vorlauf_ist_temperatur_wp
   r=+0.86  sensor.heatpump_leistung_warmwasserbereitung
   r=+0.86  binary_sensor.heatpump_warmwasserbereitung
   r=+0.85  binary_sensor.heatpump_entleerung_hyd

== sensor.heatpump_tbd_temp_01: n=1440 changes, min=23.1000003814697 max=59.2000007629395 distinct=[23.1000003814697, 23.2000007629395, 23.2999992370605, 23.3999996185303, 23.5, 23.6000003814697, 23.7000007629395, 23.7999992370605, 23.8999996185303, 24.0, 24.1000003814697, 24.2000007629395]...
   r=+1.00  sensor.heatpump_vorlauf_ist_temperatur_nhz
   r=+0.99  sensor.heatpump_vorlauf_ist_temperatur_wp
   r=+0.91  sensor.heatpump_heizgastemperatur
   r=+0.89  sensor.heatpump_ruecklauf_ist_temperatur
   r=+0.84  sensor.heatpump_stromaufnahme
   r=+0.84  sensor.heatpump_leistung_verdichter

== sensor.heatpump_tbd_temp_03: n=439 changes, min=18.2000007629395 max=19.7999992370605 distinct=[18.2000007629395, 18.2999992370605, 18.3999996185303, 18.5, 18.6000003814697, 18.7000007629395, 19.5, 19.6000003814697, 19.7000007629395, 19.7999992370605]
   r=+0.88  sensor.heatpump_leistung_warmwasserbereitung
   r=+0.88  binary_sensor.heatpump_warmwasserbereitung
   r=+0.87  binary_sensor.heatpump_entleerung_hyd
   r=+0.84  sensor.heatpump_vorlauf_ist_temperatur_nhz
   r=+0.84  sensor.heatpump_ruecklauf_ist_temperatur
   r=+0.81  sensor.heatpump_vorlauf_ist_temperatur_wp

== sensor.tbd_02_mfg: n=12 changes, min=33.0 max=100.0 distinct=[33.0, 100.0]
   r=-1.00  binary_sensor.heatpump_quellenpumpe
   r=-0.98  binary_sensor.heatpump_pufferladepumpe
   r=-0.97  sensor.heatpump_debug_betrieb
   r=-0.97  binary_sensor.heatpump_verdichter
   r=-0.96  sensor.heatpump_leistung_summe
   r=-0.96  sensor.heatpump_stromaufnahme

== sensor.tbd_02_wpm2: n=12 changes, min=33.0 max=100.0 distinct=[33.0, 100.0]
   r=-1.00  binary_sensor.heatpump_quellenpumpe
   r=-0.98  binary_sensor.heatpump_pufferladepumpe
   r=-0.97  sensor.heatpump_debug_betrieb
   r=-0.97  binary_sensor.heatpump_verdichter
   r=-0.96  sensor.heatpump_leistung_summe
   r=-0.96  sensor.heatpump_stromaufnahme

== sensor.tbd_06_mfg: n=6 changes, min=0.0 max=100.0 distinct=[0.0, 1.0, 98.0, 100.0]
   r=+1.00  binary_sensor.heatpump_entleerung_hyd
   r=+0.99  binary_sensor.heatpump_warmwasserbereitung
   r=+0.99  sensor.heatpump_leistung_warmwasserbereitung
   r=+0.85  sensor.heatpump_ruecklauf_ist_temperatur
   r=+0.74  sensor.heatpump_vorlauf_ist_temperatur_nhz
   r=+0.72  sensor.heatpump_vorlauf_ist_temperatur_wp

== sensor.tbd_06_wpm2: n=4 changes, min=0.0 max=100.0 distinct=[0.0, 100.0]
   r=+1.00  binary_sensor.heatpump_entleerung_hyd
   r=+0.99  binary_sensor.heatpump_warmwasserbereitung
   r=+0.99  sensor.heatpump_leistung_warmwasserbereitung
   r=+0.85  sensor.heatpump_ruecklauf_ist_temperatur
   r=+0.74  sensor.heatpump_vorlauf_ist_temperatur_nhz
   r=+0.72  sensor.heatpump_vorlauf_ist_temperatur_wp

== sensor.tbd_07_mfg: n=2 changes, min=0.0 max=0.0 distinct=[0.0]

== sensor.tbd_07_wpm2: n=2 changes, min=0.0 max=0.0 distinct=[0.0]

== sensor.tbd_08_mfg: n=15 changes, min=33.0 max=100.0 distinct=[33.0, 57.0, 100.0]
   r=-1.00  sensor.heatpump_leistung_summe
   r=-1.00  sensor.heatpump_leistung_verdichter
   r=-1.00  sensor.heatpump_stromaufnahme
   r=-0.98  binary_sensor.heatpump_pufferladepumpe
   r=-0.97  sensor.heatpump_debug_betrieb
   r=-0.97  binary_sensor.heatpump_verdichter

== sensor.tbd_08_wpm2: n=15 changes, min=33.0 max=100.0 distinct=[33.0, 57.0, 100.0]
   r=-1.00  sensor.heatpump_leistung_summe
   r=-1.00  sensor.heatpump_leistung_verdichter
   r=-1.00  sensor.heatpump_stromaufnahme
   r=-0.98  binary_sensor.heatpump_pufferladepumpe
   r=-0.97  sensor.heatpump_debug_betrieb
   r=-0.97  binary_sensor.heatpump_verdichter

== sensor.tbd_10_kessel: n=2 changes, min=256.0 max=256.0 distinct=[256.0]

== sensor.tbd_10_manager: n=2 changes, min=256.0 max=256.0 distinct=[256.0]
```

## Value comparison
```
TBD_TEMP_01 - Vorlauf WP: n=1440 mean diff=-0.00 median=+0.00 |diff|<=0.2: 91%
TBD_TEMP_01 - Vorlauf NHZ: n=1440 mean diff=-0.51 median=-0.40 |diff|<=0.2: 5%
TBD_19/10 - Ruecklauf: n=1440 mean diff=-0.00 median=+0.00 |diff|<=0.2: 99%
TBD_TEMP_03 - Quelle: n=1440 mean diff=+6.15 median=+5.50 |diff|<=0.2: 3%
```

## Transitions (local time; pump states 30 s after the change)
```

== sensor.tbd_02_wpm2
11-09 13:47:08 100.0  |  verdic=off quelle=off puffer=off warmwa=off heizkr=off
11-09 14:02:34 33.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=off
11-09 14:54:18 100.0  |  verdic=off quelle=off puffer=off warmwa=off heizkr=on
11-09 16:55:31 unavailable  |  verdic=off quelle=off puffer=off warmwa=off heizkr=off
11-09 16:55:32 100.0  |  verdic=off quelle=off puffer=off warmwa=off heizkr=off
11-09 20:53:41 33.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-09 21:58:17 100.0  |  verdic=off quelle=off puffer=off warmwa=off heizkr=on
11-10 00:25:03 33.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-10 01:23:43 100.0  |  verdic=off quelle=off puffer=off warmwa=off heizkr=on
11-10 02:51:21 33.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-10 03:54:51 100.0  |  verdic=off quelle=off puffer=off warmwa=off heizkr=on
11-10 06:04:33 33.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-10 07:05:53 100.0  |  verdic=off quelle=off puffer=off warmwa=off heizkr=on

== sensor.tbd_08_wpm2
11-09 13:47:08 100.0  |  verdic=off quelle=off puffer=off warmwa=off heizkr=off
11-09 14:04:46 33.0  |  verdic=on quelle=on puffer=on warmwa=on heizkr=off
11-09 14:51:19 57.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-09 14:51:39 100.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-09 14:53:01 57.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-09 14:53:19 100.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-09 16:55:31 unavailable  |  verdic=off quelle=off puffer=off warmwa=off heizkr=off
11-09 16:55:32 100.0  |  verdic=off quelle=off puffer=off warmwa=off heizkr=off
11-09 20:54:13 57.0  |  verdic=on quelle=on puffer=on warmwa=off heizkr=on
11-09 21:57:19 100.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-10 00:25:35 57.0  |  verdic=on quelle=on puffer=on warmwa=off heizkr=on
11-10 01:22:45 100.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-10 02:51:53 57.0  |  verdic=on quelle=on puffer=on warmwa=off heizkr=on
11-10 03:53:53 100.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-10 06:05:05 57.0  |  verdic=on quelle=on puffer=on warmwa=off heizkr=on
11-10 07:04:55 100.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on

== sensor.tbd_06_wpm2
11-09 13:47:08 0.0  |  verdic=off quelle=off puffer=off warmwa=off heizkr=off
11-09 14:03:44 100.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=off
11-09 14:51:59 0.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-09 16:55:31 unavailable  |  verdic=off quelle=off puffer=off warmwa=off heizkr=off
11-09 16:55:32 0.0  |  verdic=off quelle=off puffer=off warmwa=off heizkr=off

== sensor.tbd_06_mfg
11-09 13:47:08 1.0  |  verdic=off quelle=off puffer=off warmwa=off heizkr=off
11-09 14:03:44 100.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=off
11-09 14:04:03 98.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=off
11-09 14:51:59 0.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-09 14:52:18 1.0  |  verdic=off quelle=on puffer=off warmwa=off heizkr=on
11-09 16:55:31 unavailable  |  verdic=off quelle=off puffer=off warmwa=off heizkr=off
11-09 16:55:32 1.0  |  verdic=off quelle=off puffer=off warmwa=off heizkr=off
```

Settings at the time: Pumpenleistung Sole 65 %, Warmwasser 65 %, Heizkreis 40 %.
HA has no temperature sensor in the HWR to compare TBD_TEMP_03 with.
