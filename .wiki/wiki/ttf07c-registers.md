# TTF07 C registers

**The one place for all CAN registers of this TTF07 C with WPM3i** (source of truth, [`.wiki/AGENTS.md`](../AGENTS.md)): address,
firmware property, type, node, HA entity, and **how well each is confirmed by our own tests**. Other pages explain
behaviour and tests and link here instead of repeating register tables. Keep it in step with
`components/wp_core/property.h` and `yaml/ttf07_wpm3i.yaml`. Status 2026-11-18.
Addresses in `property.h` are lowercase hex and unique: `PROPERTY()` defines `unique<addr>` at compile time, so a
duplicate fails the build only when both are spelled the same way.
Unidentified registers have no property: they are debug sensors by address in `yaml/ttf07_wpm3i_debug.yaml`
("– (debug)"). HA entity column: names as shown with `yaml/names/ttf07_wpm3i_de.yaml`.

See also: [CAN bus](can-bus.md) (nodes, frame format), [Betriebsstatus](betriebsstatus.md) (bits of `0x4e5e` /
`0x0A20`, relay test), [Errors](errors.md), [FEK2](fek2.md), [Cooling](cooling.md), [Heating control](heating-control.md).
Plan for the unknown registers in the regular bus traffic (inventory with rates, phases):
[`plans/register-decoding.md`](../../plans/register-decoding.md) (2026-11-18).

## Conventions

- Values: `0x8000` (shown as `-3276.8` / `32768`) = no value; `0x9000` = "AUS" on the panel (`0xA000` seen
  since 2026-11-17 18:54 for the same settings, meaning open); `0xFE70` = −40.0 °C = no sensor.
- Types (`property.h`): `et_dec_val` = value / 10, `et_double_val`/`et_default` = raw, `et_little_endian` =
  value in the high byte. Time windows: high byte = start, low byte = end, in 15-min steps, `0x8080` = empty.
- Naming vs upstream's TTF07: cooling uses `KUEHLEN_EIN` `0x06a4`, `KUEHLMODE` `0x0287`, `FLAECHENKUEHLUNG`
  `0x025f` (was `KUEHLEN_AKTIVIERT`), `GEBLAESEKUEHLUNG` `0x025b` instead of `KUEHLEN_EINGESCHALTET` `0x06aa`;
  the status comes from `BETRIEBS_STATUS_WPM` `0x4e5e` (WPM3i); old fork names (`QUELLEISTTEMP`, `HEIZGASTEMP`,
  `PUMPENLEISTUNG_*`, `VORLAUFISTTEMPWP`, `VD_*`, `ZEIT_NHZ*`) were replaced by upstream's names.

Columns **Node** and **Traffic**:
- **Node**: where the value lives and can be read (Kessel, Manager = WPM3i, MFG, HK1 …).
- **Traffic (seen on the bus)**: who sends the address to whom without being asked by the ESP, from all captures in
  `raw/captures/` (up to 2026-11-17): "A→B write" = A writes to B (also periodic sends), "A reads B" = A asks B.
  HK1 as a sender is the FEK or the ESP's emulation (it sends as `0x301`); Panel = control panel `0x100`; "ESP reads
  only" = no traffic seen except the ESP's own polling. Regenerate with the capture scan when captures are added.

Status:

| Status | Meaning |
|---|---|
| ✅ test | confirmed by a test: the value was changed on purpose (panel, FEK, HA, relay test) and the frame seen |
| ✅ panel | the value matches the control panel's display (expert menus 2026-11-17, settings menus) |
| ✅ analysis | confirmed by HA history analysis (correlation with known signals) |
| ◻️ plausible | sensible value and upstream name, but not compared with the panel or tested |
| – no value | the node answers `0x8000` (not used on this installation) or the address does not react |
| ❓ open | meaning unknown or only guessed. **Left unknown on purpose for now** (maintainer, 2026-11-17): no further tests planned; the debug sensors keep collecting |
| · unused | defined in `property.h` (upstream, common section), not read on this installation |

Rows (updated 2026-11-17 evening): ✅ test 30, ✅ panel 55, ✅ analysis 8, ◻️ plausible 17, – no value 14, ❓ open 22, · unused 2 (a row may cover several registers).

## Kessel (0x180)

| Address | Property (firmware) | Type | Node | Traffic (seen on the bus) | HA entity | Status | Evidence / meaning |
|---|---|---|---|---|---|---|---|
| `0x0003` | `SPEICHERSOLLTEMP` | `et_dec_val` | Kessel | Panel reads Kessel; HK1 reads Kessel | Speicher Soll Temperatur | ✅ panel | 45.0 °C on Info > Warmwasser |
| `0x000c` | `AUSSENTEMP` | `et_dec_val` | Kessel | Panel reads Kessel; Kessel→0x379 write; HK1 reads Kessel | Aussentemperatur | ✅ panel | Info > Heizung |
| `0x000e` | `SPEICHERISTTEMP` | `et_dec_val` | Kessel | Panel reads Kessel; Kessel→0x379 write; HK1 reads Kessel | Speicher Ist Temperatur | ✅ panel | Info > Warmwasser |
| `0x0016` | `RUECKLAUFISTTEMP` | `et_dec_val` | Kessel | Panel reads Kessel; Kessel→0x379 write | Rücklauf Ist | ✅ panel | Info > Heizung |
| `0x0078` | `PUFFERISTTEMP` | `et_dec_val` | Kessel | Panel reads Kessel | Puffer Ist | ✅ panel | Info > Heizung |
| `0x01d4` | `QUELLE_IST` | `et_dec_val` | Kessel | Panel reads Kessel | Quelle Ist | ✅ panel | Info > Quelle |
| `0x01b0` | `QUELLENTEMP_MIN` | `et_dec_val` | Kessel | Panel reads Kessel; Manager→Panel write | Quellentemperatur min | ✅ panel | −9.0 °C, Info > Quelle |
| `0x01d5` | `PUFFERSOLLTEMP` | `et_dec_val` | Kessel | Panel reads Kessel | Puffer Soll | ✅ panel | Puffersoll = Solltemperatur HK 1 on Info > Heizung |
| `0x01d7` | `HKSOLLTEMP` | `et_dec_val` | Kessel | HK1 reads Kessel | HK Soll | ◻️ plausible |  |
| `0x02ca` | `HKISTTEMP` | `et_dec_val` | Kessel | Panel reads Kessel; HK1 reads Kessel | HK Ist | ✅ panel | Isttemperatur HK 1, Info > Heizung |
| `0x06a1` | `VORLAUFISTTEMP` | `et_dec_val` | Kessel | Panel reads Kessel | Vorlauf Ist WP | ✅ panel | Vorlaufisttemperatur WP, Info > Heizung |
| `0x06a0` | (Vorlauf Ist NHZ, Kessel copy) |  | Kessel | Panel reads Kessel | – | ✅ panel | Vorlaufisttemperatur NHZ 27.3 °C, Info > Heizung; **the same value as MFG `0xfdf5`** (identical in 3 of 3 paired reads, 2026-11-17 19:23), so not read separately; upstream MOTORLEISTUNG elsewhere |
| `0x0265` | `HEISSGAS_TEMP` | `et_dec_val` | Kessel | Panel reads Kessel | Heissgastemperatur | ✅ panel | Info > Kältekreis |
| `0x0268` | `DRUCK_HOCHDRUCK` | `et_cent_val` | Kessel | Panel reads Kessel | Druck Heizkreis max (dashboard: Hochdruck (Kältekreis)) | ✅ panel | **refrigerant high pressure**, raw/10 bar (10.3 at rest, 19.9 in operation 2026-11-17 21:49); firmware scaler 10.0 since 2026-11-17 21:15 (before: 100x too small); confirmed on the panel: Info > Wärmemenge > Prozessdaten "Druck Hochdruck 20.4 bar / Druck Niederdruck 8.0 bar" = raw 205 / 79 (2026-11-17 22:00) |
| `0x07a5` | `DRUCK_NIEDERDRUCK` | `et_cent_val` | Kessel | Panel reads Kessel | Druck Heizkreis min (dashboard: Niederdruck (Kältekreis)) | ✅ panel | **refrigerant low pressure**, raw/10 bar (10.1 at rest, 8.2 in operation 2026-11-17 21:49); same fix, confirmed on the panel like `0x0268` |
| `0x0674` | `DRUCK_HEIZKREIS` | `et_cent_val` | Kessel | Panel reads Kessel | Druck Heizkreis | ✅ panel | Heizungsdruck 1.34 bar, Info > Heizung |
| `0x0675` | `QUELLENDRUCK` | `et_cent_val` | Kessel | Panel reads Kessel | Druck Quelle | ✅ panel | 2.06 bar, Info > Quelle |
| `0x0673` | `VOLUMENSTROM` | `et_cent_val` | Kessel | Panel reads Kessel | Volumenstrom | ✅ panel | 0.00 l/min, Info > Heizung (always 0: no flow meter?) |
| `0x0264` | `TAUPUNKT_HK1` | `et_dec_val` | Kessel | Panel reads Kessel | Taupunkt | ✅ panel | 11.1 °C, Info > Raumtemperatur (added 2026-11-17) |
| `0x0a00` | `ANLAGENFROST` | `et_dec_val` | Kessel | Kessel→0x379 write; Panel reads Kessel | Anlagenfrost | ✅ panel | 4.0 °C, Info > Heizung |
| `0x01a2` | `HDSENSORMAX` | `et_dec_val` | Kessel | Panel reads Kessel | HD-Sensor max | ◻️ plausible | 44.0 bar, read by the panel in the expert menus |
| `0x0013` | `WW_KOMF_TEMP` | `et_dec_val` | Kessel | Panel reads Kessel; Panel→Kessel write | WW Komfort | ✅ test | changed on the panel 2026-11-16, write `0x100` → Kessel seen |
| `0x0a06` | `WW_ECO_TEMP` | `et_dec_val` | Kessel | Panel reads Kessel | WW Eco | ◻️ plausible |  |
| `0x0022` | `WW_HYSTERESE` | `et_dec_val` | Kessel | Panel reads Kessel | WW Hysterese | ◻️ plausible |  |
| `0x01e8` | `MAXVORLAUFTEMP` | `et_dec_val` | Kessel | Panel reads Kessel | Maximale Vorlauftemperatur (since 2026-11-17) | ◻️ plausible | 40.0 °C, read by the panel |
| `0xfdb0` | `REGLERDYNAMIK` | `et_little_endian` | Kessel | Panel reads Kessel | Reglerdynamik | ◻️ plausible | `0x1E00` |
| `0xfdb1` | `VERDICHTER_STILLSTAND` | `et_little_endian` | Kessel | Panel reads Kessel | Verdichter Stillstand | ✅ panel | 60 min; Reststillstand counts down from it |
| `0x070a` | `LEISTUNG_HEIZKREISPUMPE` | `et_byte` | Kessel | Panel reads Kessel | Leistung Heizkreispumpe | ◻️ plausible | 40 % |
| `0x070b` | `LEISTUNG_WARMWASSERPUMPE` | `et_byte` | Kessel | Panel reads Kessel | Leistung Warmwasserpumpe | ◻️ plausible | 65 % |
| `0x070c` | `LEISTUNG_SOLEPUMPE` | `et_byte` | Kessel | Panel reads Kessel | Leistung Solepumpe | ◻️ plausible | 65 % |
| `0x070e` | `EINPHASIGER_BETRIEB` | `et_bool` | Kessel | Panel reads Kessel; Panel→Kessel write | Einphasiger Betrieb | ◻️ plausible | 0 |
| `0xfdae` | `QUELLENMEDIUM` | `et_byte` | Kessel | Panel→Kessel write; Panel reads Kessel | – | ◻️ plausible | 0, read by the panel |
| `0x01ac` | `BIVALENZTEMPERATUR_HZG` | `et_dec_val` | Kessel | Panel reads Kessel | Bivalenztemperatur Heizen | ✅ panel | −19.0 °C, Info > Elektrische Nacherwärmung (added 2026-11-17) |
| `0x01ad` | `BIVALENZTEMPERATUR_WW` | `et_dec_val` | Kessel | Panel reads Kessel | Bivalenztemperatur Warmwasser | ✅ panel | −19.0 °C (added 2026-11-17) |
| `0x01ae` | `EINSATZGRENZE_HZG` | `et_default` | Kessel | Panel reads Kessel; Panel→Kessel write | Einsatzgrenze Heizen | ✅ panel | `0x9000` = AUS (added 2026-11-17) |
| `0x01af` | `EINSATZGRENZE_WW` | `et_default` | Kessel | Panel reads Kessel | Einsatzgrenze Warmwasser | ✅ panel | `0x9000` = AUS (added 2026-11-17) |
| `0x01c0` | FESTWERTBETRIEB (was TBD_17) | `et_default` | Kessel | Panel reads Kessel | Festwertsolltemperatur | ✅ panel | `0x9000` = AUS, Info > Heizung (added 2026-11-17) |
| `0x011a` | `AUFHEIZPROGRAMM` | `et_little_endian` | Kessel | Panel reads Kessel; Panel→Kessel write; Manager→Panel write | Aufheizprogramm | ✅ test | switched EIN/AUS on the panel 2026-11-17: `0x0100` / 0 |
| `0x01ba` | (Aufheiz: Steigung pro Tag) |  | Kessel | Panel reads Kessel | – | ✅ panel | 10 K |
| `0x01bb` | (Aufheiz: Sockeltemperatur) |  | Kessel | Panel reads Kessel | – | ✅ panel | 40.0 °C |
| `0x01bc` | (Aufheiz: Dauer Sockel) |  | Kessel | Panel reads Kessel | – | ✅ panel | 2 Tage |
| `0x01bd` | (Aufheiz: Maximal Temperatur) |  | Kessel | Panel reads Kessel | – | ✅ panel | 45.0 °C |
| `0x01be` | (Aufheiz: Dauer Maximaltemperatur) |  | Kessel | Panel reads Kessel | – | ✅ panel | 5 Tage |
| `0x1710–0x1772` | WW_PROGRAMM_MO_1 … SO_3 | `et_default` | Kessel | Panel reads Kessel; Panel→Kessel write | Warmwasserprogramm Montag … Sonntag | ✅ test | day d window w at `0x1710 + 0x10·d + w`; start/end bytes in 15-min steps, `0x8080` = empty; written and checked on the panel 2026-11-17 |
| `0x1780 / 0x1790 / 0x17a0` | (WW day groups Mo–Fr / Sa–So / Mo–So) |  | Kessel | Panel reads Kessel; Panel→Kessel write | – | ✅ test | writing a group fills its days (2026-11-17) |
| `0x1700–0x170f, 0x17b0–0x180f, 0x1880–0x18af` | (unknown blocks) |  | Kessel | ESP reads only | – | ❓ open | all `0x8080`; not the Heizprogramm (that is on HK1) |
| `0x0693` | `RELAISTEST_AKTIV` | `et_default` | Kessel | Panel→Kessel write | – | ✅ test | panel writes 1 entering, 0 leaving the relay test (2026-11-17) |
| `0x067a` | RELAISTEST_RELAIS (was TBD_16) | `et_default` | Kessel | Panel→Kessel write | – | ✅ test | relay number 1–12 written by the panel in the relay test; reads give no answer |
| `0x068f` | `PUFFERBETRIEB` (was TBD_18) | `et_default` | Kessel | Panel reads Kessel | Pufferbetrieb (binary, since 2026-11-18) | ❓ open | 1; read with Info > Heizung, not shown |
| `0x06a2` | (upstream INVERTERTEMPERATUR) |  | Kessel | Panel reads Kessel | – | – no value |  |
| `0x070f, 0x0705, 0xfdc0, 0x0914` | – |  | Kessel | Panel reads Kessel | – | – no value | read by the panel in the expert menus |
| `0xfdb2` | `PUMPENZYKLEN` (was KUEHLEN_TBD_FDB2) | `et_default` | Kessel | Panel reads Kessel; Panel→Kessel write | Pumpenzyklen (binary, since 2026-11-18) | ❓ open | `0x0100`; not Kühlen EIN/AUS (tested 2026-11-16) |
| `0x06a5, 0x06a6` | – (debug) | | Kessel | Panel reads Kessel | Debug Kessel 0x06A5 / 0x06A6 (Kühlen) | – no value | read by the panel in the Kühlen menu |
| `0x06a4` | `KUEHLEN_EIN` | `et_bool` | Kessel | Panel reads Kessel; Panel→Kessel write | Kühlen | ✅ test | switched on the panel 2026-11-16 (panel Kühlen → Kühlen EIN/AUS; [capture](../raw/captures/2026-11-16-1745-kuehlen-menu-mapping.log)) |
| `0x0287` | `KUEHLMODE` | `et_bool` | Kessel | Panel reads Kessel; Panel→Kessel write | Kühlmode | ✅ test | 2026-11-16 (0 = passiv, 1 = aktiv) |
| `0x025f` | `FLAECHENKUEHLUNG` | `et_bool` | Kessel | Panel reads Kessel; Panel→Kessel write; Manager→Panel write | Flächenkühlung | ✅ test | 2026-11-16 (Passivkühlung → Flächenkühlung EIN/AUS) |
| `0x025b` | `GEBLAESEKUEHLUNG` | `et_bool` | Kessel | Panel reads Kessel; Panel→Kessel write; Manager→Panel write | Gebläsekühlung | ✅ test | 2026-11-16 (Passivkühlung → Gebläsekühlung; [capture](../raw/captures/2026-11-15-2137-geblaesekuehlung-on-off.log)) |
| `0x0260` | `VORLAUFSOLLTEMP_KUEHLEN` | `et_dec_val` | Kessel | Panel reads Kessel; Panel→Kessel write | Vorlauf Soll Kühlen | ✅ test | 17.0 °C once Kühlen is EIN (2026-11-16); answers `0x8000` while Kühlen/Flächenkühlung are off |
| `0x0261` | `RAUMSOLLTEMP_KUEHLEN` | `et_dec_val` | Kessel | Panel reads Kessel; Panel→Kessel write | Raum Soll Kühlen | ✅ test | 22.5 °C once Kühlen is EIN |
| `0x0262` | `HYSTERESE_VORLAUFTEMP_KUEHLEN` | `et_dec_val` | Kessel | Panel reads Kessel; Panel→Kessel write | Hysterese Vorlauf Kühlen | ✅ test | 1.5 K once Kühlen is EIN |
| `0x0001` | `FEHLERMELDUNG` | `et_default` | Kessel | Kessel→0x379 write | Fehlermeldung | ◻️ plausible | 0; stayed 0 in the error tests (the WPM3i error is `0x1388`) |
| `0x0121–0x0127` | date/time (TAG … SEKUNDE) | `et_little_endian` | Kessel, Manager | Manager→Panel write | Zeitstempel | ◻️ plausible | weekly time sync; Manager writes MINUTE to the panel every minute |
| `0x0199` | `FET_SOFTWARE` | `et_default` | Kessel, Manager, HK1 | Panel reads HK1; Manager→Panel write | Software WPM3i, Software HK1 | ✅ panel | 391 WPM3i, 416 FEK; Diagnose > Busteilnehmer |
| `0x019a` | `FET_SOFTWARESTAND` | `et_default` | Kessel, Manager, HK1 | Panel reads Kessel; Panel reads HK1; Manager→Panel write | (part of the software sensors) | ✅ panel | 10 WPM3i, 3 FEK |
| `0x00fd` | `ANMELDUNG` | `et_default` | all | HK1→HK1 system; ESP→ESP system; Panel→Panel system | – | ✅ test | system message: 0x0900 register, 0x0800 presence check, 0x0100 answer (FEK tests) |
| `0x00fe` | SYSTEM_PRAESENZ (was TBD_10) | `et_default` | all | 0x601→HK1 system; Panel→Manager system; Kessel→0x379 system | – | ✅ analysis | 7-min presence message index, value `0x0100` |
| `0x0a20` | `BETRIEBS_STATUS` | `et_default` | Kessel | Kessel→0x379 write | (status bits) | ✅ test | bits confirmed by the NHZ tests and the relay test 2026-11-17 |
| `0x091a–0x0921` | EL_ENERGIEAUFNAHME_* (WW/HEIZ, TAG/SUM) |  | Kessel | Panel reads Kessel | El. Energie Heizen/WW Tag/Summe | ✅ panel | Info > Leistungsaufnahme matches HA |
| `0x092a–0x0931` | WAERMEERTRAG_* (WW/HEIZ, TAG/SUM) |  | Kessel | ESP reads only | Wärmeertrag Heizen/WW Tag/Summe | ✅ panel | Info > Wärmemenge |
| `0x0929 + 0x0927` | WAERMEERTRAG_2WE_HEIZ_SUM_MWH + NHZ_WAERME_HEIZ_SUM_KWH | `et_double_val` | Kessel | Panel reads Kessel | Wärmeertrag NHZ Heizen | ✅ panel | 6.688 MWh; kWh part at `0x0927` (upstream `0x0928` is 0 here); added 2026-11-17 |
| `0x0925 + 0x0923` | NHZ_WAERME_WW_SUM_MWH + _KWH | `et_double_val` | Kessel | Panel reads Kessel | Wärmeertrag NHZ Warmwasser | ✅ panel | 0.538 MWh; added 2026-11-17 |
| `0x0928, 0x0924` | (upstream NHZ kWh parts) |  | Kessel | Panel reads Kessel | – | ❓ open | always 0 on this heat pump |
| `0x07fc` | `LAUFZEIT_VD_HEIZEN` | `et_default` | Kessel | Panel reads Kessel | Laufzeit VD Heizen | ✅ panel | 7601 h, Info > Laufzeit |
| `0x0802` | `LAUFZEIT_VD_WW` | `et_default` | Kessel | Panel reads Kessel | Laufzeit VD WW | ✅ panel | 1344 h |
| `0x07ff` | `LAUFZEIT_VD_KUEHLEN` | `et_default` | Kessel | Panel reads Kessel | Laufzeit VD Kühlen | – no value | the panel reads it and hides the line: no cooling hours yet |
| `0x0259` | `LAUFZEIT_NHZ1` | `et_default` | Kessel | Panel reads Kessel | Laufzeit NHZ1 | ✅ panel | 15 h |
| `0x025a` | `LAUFZEIT_NHZ2` | `et_default` | Kessel | Panel reads Kessel | Laufzeit NHZ2 | ✅ panel | 13 h |
| `0x0805` | `LAUFZEIT_NHZ1_2` | `et_default` | Kessel | Panel reads Kessel | Laufzeit NHZ1/2 | ✅ panel | 997 h; panel label "NHZ 1/2" |
| `0x071c / 0x071d` | VERDICHTER_STARTS_K / _STARTS | `et_default` | Kessel | Panel reads Kessel | Verdichterstarts | ✅ panel | 24 × 1000 + 198 = 24198 |
| `0x4eb2` | (upstream WW_ANFORDERUNG) |  | Kessel, Manager, HK1 | ESP reads only | – | – no value | read 2026-11-17 |
| `0x000a` | (date, not named yet) |  | Kessel → 0x379 | Kessel→0x379 write | – | ✅ analysis | date: high byte = day, low byte = month; the frame's 6th data byte = year − 2000 (`60 79 0A 12 0B 1A 00` = 18.11.(20)26). Changed `0x120B` → `0x130B` between 23:57:04 and 00:04:04 on 2026-11-19 (24 h capture); every ~7 min. Month change (2026-12-01 → `0x010C`) and year byte still to see |
| `0x0010, 0x0053, 0x005a, 0x005e, 0x0073` | – |  | Kessel → 0x379 | Kessel→0x379 write; 0x601→HK1 write; Kessel→0x679 write | – | ❓ open | sent all the time; 0x0009 = time, `0x000a` = date; see [plan](../../plans/register-decoding.md) |
| `0x06aa` | `KUEHLEN_EINGESCHALTET` | `et_little_bool` | Kessel | ESP reads only | – | – no value | upstream's cooling address; does not react on this heat pump (2026-11-16); `KUEHLEN_EIN` `0x06a4` is used |
| `0x03e3` | – |  | Kessel | Panel reads Kessel | – | – no value | read by the panel in the Kühlen menu |
| `0x059d` | `ANTEIL_VORLAUF_HK1` | `et_default` | Kessel | Panel reads Kessel | – | – no value | read by the panel (expert menus) |
| `0x059f, 0x05a0` | (upstream EL_NACHERW_ANZ_STUFEN / _VERZ_ZEIT, WPL) |  | Kessel | Panel reads Kessel | – | – no value | read by the panel (expert menus) |
| `0x059e` | `FUSSPUNKT_HK1` | `et_dec_val` | Kessel | ESP reads only | – | · unused | defined by upstream (common), not read here |
| `0x0014` | `VERDAMPFERTEMP` | `et_dec_val` | Kessel | ESP reads only | – | · unused | defined by upstream (common), not read here |
| `0x0288` | (Dynamik aktiv) |  | Kessel | Panel reads Kessel | – (panel only) | ✅ panel | 10, Aktivkühlung > Flächenkühlung (2026-11-17 20:16) |
| `0xfdb3` | (Sommerbetrieb Gebäudedämpfung) |  | Kessel | Panel reads Kessel | – (panel only) | ✅ panel | 3 (high byte), Heizen > Grundeinstellung > Sommerbetrieb |
| `0xfdb4` | `SOMMERBETRIEB` |  | Kessel | Panel reads Kessel | Sommerbetrieb (binary, since 2026-11-17) | ✅ panel | 0x0100 = EIN, Heizen > Grundeinstellung > Sommerbetrieb |
| `0x027e` | (WW Lernfunktion) |  | Kessel | Panel reads Kessel; Panel→Kessel write | – (panel only) | ✅ test | 1 = EIN, written by the panel and back to 0 (2026-11-17 20:14) |
| `0x0101` | `ANTILEGIONELLEN` |  | Kessel | Panel reads Kessel; Panel→Kessel write | Antilegionellenbehandlung (binary, since 2026-11-17) | ✅ test | 0x0100 = EIN, switched on for 2 s and back (2026-11-17 20:14) |
| `0x0263` | (WW-Korrektur) |  | Kessel | Panel reads Kessel; Panel→Kessel write | – (panel only) | ✅ test | tenths of a degree; 0.5 °C tested and back to 0.0 (2026-11-17 20:14) |
| `0x070d` | (Kombispeicher) |  | Kessel | Panel reads Kessel; Panel→Kessel write | – (panel only) | ✅ test | 1 = EIN, tested and back to 0 (2026-11-17 20:14) |
| `0x01bf` | `SOMMERBETRIEB_HEIZGRENZE` |  | Kessel | Panel reads Kessel | Sommerbetrieb Heizgrenze (since 2026-11-17) | ✅ panel | 16.5 °C; the heating limit in summer mode (Heizen > Grundeinstellung > Sommerbetrieb) |
| `0x0135` | (Warmwasser Grundeinstellung, unknown) |  | Kessel | Panel reads Kessel | – | ❓ open | read on the WW Grundeinstellung page, no value |
| `0xfdba` | (Warmwasser Grundeinstellung, unknown) |  | Kessel | Panel reads Kessel | – | ❓ open | read on the WW Grundeinstellung page, no value |
| `0xfdb9` | (Warmwasser Grundeinstellung, unknown) |  | Kessel | Panel reads Kessel | – | ❓ open | read on the WW Grundeinstellung page, no value |
| `0x0181` | (Warmwasser Grundeinstellung, unknown) |  | Kessel | Panel reads Kessel | – | – no value | read on the WW Grundeinstellung page |
| `0x0705` | (Pumpen page, unknown) |  | Kessel | Panel reads Kessel | – | – no value | read on the Pumpen page next to the pump rates; meaning open |

## Manager / WPM3i (0x480)

| Address | Property (firmware) | Type | Node | Traffic (seen on the bus) | HA entity | Status | Evidence / meaning |
|---|---|---|---|---|---|---|---|
| `0x011b–0x0120` | FERIEN_BEGINN_* / FERIEN_ENDE_* |  | Manager | Panel reads Manager | Ferienprogramm | ✅ panel | 24.06.24 – 16.07.24 (added 2026-11-17) |
| `0x4e5e` | `BETRIEBS_STATUS_WPM` | `et_default` | Manager | Manager→Panel write | status binary sensors, DEBUG_BETRIEB | ✅ test | bits confirmed by NHZ, compressor and relay tests |
| `0x0112` | `PROGRAMMSCHALTER` | `et_betriebsart` | Manager | Panel reads Manager; Manager→Panel write; Panel→Manager write | Programmschalter | ✅ test | all six positions 2026-11-16 |
| `0x1388` | FEHLERNUMMER_WPM (was TBD_12) | `et_default` | Manager | Manager→Panel write | Fehlernummer, Fehler aktuell | ✅ test | 21 = Keine Leistung, compressor test 2026-11-17; **18 = Hochdruck** (panel, 2026-11-17) |
| `0x0668` | `VERDICHTER_RESTSTILLSTAND` | `et_default` | Manager | Panel reads Manager | Verdichter Reststillstand | ✅ panel | minutes, Diagnose > Status Wärmepumpe (added 2026-11-17) |
| `0x4e64` | `RAUMISTTEMP_WPM` | `et_dec_val` | Manager | Panel reads Manager | Raum Ist WPM3i | ✅ panel | 21.2 °C, Info > Raumtemperatur (added 2026-11-17) |
| `0x4e66` | `RAUMSOLLTEMP_WPM` | `et_dec_val` | Manager | Panel reads Manager | Raum Soll WPM3i | ✅ panel | 22.0 °C (added 2026-11-17) |
| `0x069e` | `RAUMFEUCHTE_WPM` | `et_dec_val` | Manager | Panel reads Manager | Raumfeuchte WPM3i | ✅ panel | 52.5 % (added 2026-11-17) |
| `0x4e63, 0x4e65` | – |  | Manager | Panel reads Manager | – | – no value | probably HK2 room values |
| `0xfdbf` | `PARTYPROGRAMM` | `et_little_endian` | Manager | Panel reads Manager; Panel→Manager write | Partyprogramm | ✅ test | set to 3 h and back on the panel 2026-11-17 |
| `0x4e69` | (MFG software) |  | Manager | Panel reads Manager | – | ✅ panel | 18, Diagnose > Busteilnehmer ([photo](../raw/2026-11-18-busteilnehmer-panel.jpg)); the panel also reads it right after the Manager's `0x0645`/`0x4e5c`/`0x4e61` notification |
| `0x4e68` | – |  | Manager | Panel reads Manager | – | ❓ open | 2; probably Wärmepumpentyp "TTF MFG"; debug sensor "Debug Manager 0x4E68" |
| `0x0691, 0x0692` | – |  | Manager | Panel reads Manager | – | ❓ open | 0, 0; probably Diagnose > Interne Berechnung (Zeitintervall, Stufen) |
| `0x068e` | – (debug) | | Manager | Panel reads Manager | Debug Manager 0x068E (Kühlen) | ❓ open | 20; read whenever a main menu opens |
| `0xfdb6` | – (debug) | | Manager | Panel reads Manager | Debug Manager 0xFDB6 (Kühlen) | – no value |  |
| `0x0074, 0x0294, 0x06ae` | – |  | Manager | Panel reads Manager; Manager→Panel write | – | ❓ open | 1, 63, 0; read in the Diagnose menus; debug sensors "Debug Manager 0x0074/0x0294/0x06AE" (disabled by default) |
| `0x0669, 0x4e5a, 0x0658–0x065a` | – |  | Manager | Panel reads Manager; Panel→Manager write | – | ❓ open | 0; read in the expert menus; `0x0669` = Quick start, `0x0658`–`0x065a` = sensor offsets (own rows); debug sensor "Debug Manager 0x4E5A" |
| `0x0030, 0x4eba` | – |  | Manager | Panel reads Manager | – | – no value | read in the expert menus |
| `0x4e5c, 0x4e61, 0x0645` | – |  | Manager | Manager→Panel write | – | ❓ open | seen only rarely (Manager → panel); 2026-11-18 only at 16:44:03 and 16:47:23 after a flash of the ESP, sent by the WPM3i on its own (not when the panel menu was opened at 17:15): `0x0645` = 1, `0x4e5c` `0x0040`→`0x0044`, `0x4e61` 2503→2254; each time the panel then read `0x4e69` (MFG software), at 16:47 also the HK1/FEK software. Hypothesis: a "bus participants changed" notification while the FEK emulation re-registered; `0x4e5c` bit 2 = FEK present? ([plan](../../plans/register-decoding.md)) |
| `0x080e` | – (debug) | | Manager | Manager→Panel write | Debug Manager 0x080E | ❓ open | 0; Manager → panel with the error number |
| `0xfe1e` | – (debug) | | Manager, MFG | Manager→MFG write | Debug Manager 0xFE1E, Debug MFG 0xFE1E | ❓ open | 0 |
| `0xfe1b` | `PWM_LADEPUMPE` | `et_default` | Manager, MFG | Manager→MFG write | Ladepumpe PWM | ✅ analysis | inverted PWM; history analysis 2026-11-16 ([analysis](../raw/2026-11-16-tbd-history-analysis.md)) |
| `0xfe1c` | `PWM_QUELLENPUMPE` | `et_default` | Manager, MFG | Manager→MFG write | Quellenpumpe PWM | ✅ analysis | inverted PWM |
| `0xfe1d` | `UMSCHALTVENTIL_WW` | `et_default` | Manager, MFG | Manager→MFG write | Umschaltventil Warmwasser | ✅ analysis | 100 during hot water |
| `0x0b9a` | `FEHLERLISTE_INDEX` | `et_default` | Manager | Manager→Panel write; Panel→Manager write | Fehlerliste, Letzter Fehler | ✅ test | entry index (0 = newest); the panel (and the ESP, approved) writes it to request the list, the Manager answers with one block per entry; reads give `0x8000` |
| `0x0b9b` | `FEHLERLISTE_CODE` | `et_default` | Manager | Manager→Panel write | (Fehlerliste) | ✅ panel | error code, e.g. 21 = Keine Leistung; matches Diagnose > Fehlerliste |
| `0x0b9d` | – | | Manager | Manager→Panel write | – | ❓ open | always 0 so far |
| `0x0b9f` | `FEHLERLISTE_MINUTE` | `et_default` | Manager | Manager→Panel write | (Fehlerliste) | ✅ panel | minute |
| `0x0ba0` | `FEHLERLISTE_STUNDE` | `et_default` | Manager | Manager→Panel write | (Fehlerliste) | ✅ panel | hour |
| `0x0ba1` | `FEHLERLISTE_TAG` | `et_default` | Manager | Manager→Panel write | (Fehlerliste) | ✅ panel | day |
| `0x0ba2` | `FEHLERLISTE_MONAT` | `et_default` | Manager | Manager→Panel write | (Fehlerliste) | ✅ panel | month |
| `0x0ba3` | `FEHLERLISTE_JAHR` | `et_default` | Manager | Manager→Panel write | (Fehlerliste) | ✅ panel | year − 2000 |
| `0x0645` | (Kühlung change notice) |  | Manager | Manager→Panel write | – | ✅ test | the Manager writes 1 to the panel when Flächen- and Gebläsekühlung change (they exclude each other), 2026-11-17 20:15 |
| `0x0669` | QUICK_START (Kompressor) |  | Manager | Panel reads Manager; Panel→Manager write | – (panel only) | ✅ test | 1 = ON; panel toggle 20:23 confirmed on the bus; back to 0 at 20:24 (Kompressor page: Idle time 60 min, single phase OFF) |
| `0x0658` | (Sensorkalibrierung Vorlauf WW) |  | Manager | Panel reads Manager; Panel→Manager write | – (panel only) | ✅ test | offset in tenths of a degree; the panel's arrows wrote 1 (0.1 °C) at 20:26 by accident, back to 0 at 20:27 |
| `0x0659` | (Sensorkalibrierung Vorlauf) |  | Manager | Panel reads Manager; Panel→Manager write | – (panel only) | ✅ test | offset in tenths of a degree; 2 (0.2 °C) by accident at 20:26, back to 0 at 20:27 |
| `0x065a` | (Sensorkalibrierung Rücklauf) |  | Manager | Panel reads Manager; Panel→Manager write | – (panel only) | ✅ test | offset in tenths of a degree; 3 (0.3 °C) by accident at 20:26, back to 0 at 20:27 |
| `0xfdde`–`0xfde1` | (Sommerzeit start/end day and month) |  | Manager | Panel reads Manager | – (panel only) | ✅ panel | 25.03. start, 25.10. end (Einstellungen > Allgemein > Sommerzeit); high byte |
| `0x0679` | (Heizkreis optimal) |  | Manager | Panel reads Manager | – (panel only) | ✅ panel | `0x9000` = AUS (Heizen > Grundeinstellung), 2026-11-17 |

## MFG (0x700)

| Address | Property (firmware) | Type | Node | Traffic (seen on the bus) | HA entity | Status | Evidence / meaning |
|---|---|---|---|---|---|---|---|
| `0xfdf3` | `VORLAUFISTTEMP_MFG` | `et_dec_val` | MFG | Manager reads MFG | – | ✅ analysis | = Vorlauf Ist WP |
| `0xfdf4` | `RUECKLAUFISTTEMP_MFG` | `et_dec_val` | MFG | Manager reads MFG | – | ✅ analysis | = Rücklauf Ist × 10 |
| `0xfdf5` | `VORLAUFISTTEMPNHZ` | `et_dec_val` | MFG | Manager reads MFG | Vorlauf Ist NHZ | ✅ panel | = Kessel `0x06a0`, which the panel shows as Vorlaufisttemperatur NHZ (identical values 2026-11-17 19:23); the Manager polls it every 5 s |
| `0xfe07` | `STROMAUFNAHME` | `et_dec_val` | MFG | Manager reads MFG | Stromaufnahme | ✅ analysis | compressor current; not the NHZ |
| `0xfe0a` | `VERSORGUNGSSPANNUNG` | `et_default` | MFG | Manager reads MFG | Versorgungsspannung | ◻️ plausible | ~226 V |
| `0xfe09` | – (debug, was TBD_TEMP_03) | `et_dec_val` | MFG | Manager reads MFG | Debug MFG 0xFE09 (Temperatur) | ❓ open | ~5 K below the room, follows the compressor; not room, not brine ([analysis](../raw/2026-11-17-tbd-temp-03-and-constants.md)) |
| `0xfe4c` | – (debug) | | MFG | Manager reads MFG | Debug MFG 0xFE4C | ◻️ plausible | **MFG software version**: 18, constant (3436 answers 2026-11-18), the same 18 the panel shows for the MFG under Diagnose > System > Busteilnehmer (read from the Manager's `0x4e69`; [photo](../raw/2026-11-18-busteilnehmer-panel.jpg), 2026-11-18 17:15). The WPM3i reads it every 5 s (alive check?). To name in the firmware with the next batch |

## HK1, FEK, 0x601, control panel and other nodes

| Address | Property (firmware) | Type | Node | Traffic (seen on the bus) | HA entity | Status | Evidence / meaning |
|---|---|---|---|---|---|---|---|
| `0x1410` … `0x1470` (+0…+2), groups `0x1480` / `0x1490` / `0x14a0` | (Heizprogramm HK1) |  | **HK1** (`0x301`) | Panel reads HK1 | Heizprogramm Montag … Sonntag (text, read-only, only without FEK; since 2026-11-17) | ✅ panel | **Heizprogramm**: same layout as the Warmwasserprogramm (day every `0x10`, 3 windows, start/end bytes in 15-min steps, `0x8080` = empty), groups Mo–Fr / Sa–So / Mo–So. Here every day 10:00–16:00 (`0x2840`). Only visible while the WPM3i owns HK1 (no FEK); read 2026-11-17 22:12 |
| `0x0005` | `KOMF_TEMP` | `et_dec_val` | HK1 | Panel reads 0x601 | Komfort Temperatur | ✅ test | FEK/emulation tests |
| `0x0008` | `ECO_TEMP` | `et_dec_val` | HK1 | Panel reads 0x601 | Eco Temperatur | ✅ test | FEK/emulation tests |
| `0x010e` | `STEIGUNG_HK1` | `et_cent_val` | HK1 | Panel reads 0x601 | Steigung | ✅ test | FEK/emulation tests |
| `0x010f` | `RAUMEINFLUSS` | `et_little_endian` | HK1 | HK1→0x601 write | Raumeinfluss | ✅ test | set on the FEK 2026-11-16 |
| `0x0004` | `VORLAUFSOLLTEMP` | `et_dec_val` | HK1 | 0x601→HK1 write; HK1→0x601 write; Panel reads HK1 | Vorlauf Soll | ◻️ plausible |  |
| `0x0011` | `RAUMISTTEMP` | `et_dec_val` | HK1 | HK1→0x601 write; HK1 reads 0x601 | Raum Ist | ✅ test | FEK room value; emulation sends it |
| `0x0075` | `RAUMFEUCHTE` | `et_dec_val` | HK1 | HK1→0x601 write | Raumfeuchte | ✅ test | FEK room value |
| `0x0002` | `KESSELSOLLTEMP` | `et_dec_val` | FEK → Kessel | HK1→Kessel write | FEK Emulation Vorlauf Soll | ✅ test | FEK → Kessel: the flow setpoint; the panel shows it as Puffersolltemperatur ([test](heating-control.md)) |
| `0x000f` | `VORLAUFISTTEMP_HK1` | `et_dec_val` | 0x601 → HK1 | 0x601→HK1 write; HK1 reads 0x601; Panel reads 0x602 | – | ✅ analysis | `0x601` → HK1: `0xFE70` = −40.0 °C = no sensor; upstream THZ name `VORLAUFISTTEMP` |
| `0x0028` | `MAXRUECKLAUFTEMP` (was SOLLWERT_MAX_HK1) | `et_dec_val` | 0x601 → HK1 | 0x601→HK1 write; Panel reads Kessel | Maximale Rücklauftemperatur (since 2026-11-17) | ◻️ plausible | `0x601` → HK1: 30.0 °C; upstream THZ name |
| `0x4ea7` | `MINTEMP` | `et_dec_val` | 0x601 | Panel reads 0x601 | – | ✅ panel | panel reads it from `0x601` in "Heizkreis 1"; the panel shows "Minimal Temperatur 15.0 °C"; upstream WPL name |
| `0x0052` | `HEIZ_ANFORDERUNG_HK1` | `et_default` | 0x601 → HK1 | 0x601→HK1 write; 0x602→HK2 write | Heizanforderung HK1 (binary, decoded from 0x601 frames, since 2026-11-17) | ✅ test | `0x601` → HK1: `0x0100` while the compressor runs, 0 when it is off; 4 of 4 transitions on 2026-11-16 ([raw](../raw/2026-11-16-0x601-config-block-and-0x0052.md)). **Heat demand of HK1** (2026-11-17: `0x0100` from 12:01:09 to 12:17:57 in Notbetrieb with the compressor off, so not a compressor flag). 2026-11-17 (6 of 6 transitions now): `0x601` sends it on a fixed schedule, two sends per 7 min (gaps ~5 and ~2 min, e.g. 10:35:05, 10:37:02, 10:42:04), and not at once on change; compressor on 09:23:11 → `0x0100` at the next send 09:25:04, off 10:37:40 → 0 at the next send 10:42:04 |
| `0x0058` | (FEK phase) |  | FEK | HK1→Kessel write; HK1→0x601 write | – | ✅ test | FEK → Kessel and `0x601`: active phase, `0x0200` = Komfort, `0x0100` = Eco or Aus. Betriebsart on the FEK 2026-11-16: Eco 12:39:15 → `0x0100` (room setpoint 19.9), Komfort 12:47:13 → `0x0200` (21.0), Aus 13:01:32 → `0x0100` (5.0), Zeit in a Komfort phase 13:03:13 → `0x0200` (21.0) ([capture](../raw/captures/2026-11-16-1226-panel-writes-and-fek-modes.log)) |
| `0x002a` | – |  | FEK → 0x601 | HK1→0x601 write | – | ❓ open | 30; very likely the room setpoint maximum |
| `0x0029` | – |  | FEK → 0x601 | HK1→0x601 write | – | ❓ open | 10; not the setpoint minimum (Komfort goes to 5.0) |
| `0x006e` | – |  | FEK → Kessel | HK1→Kessel write | – | ❓ open | 0x0200 right after plug-in, then 0x0100 |
| `0x0010, 0x0056, 0x0057, 0x005a` | – |  | 0x601 → HK1 | 0x601→HK1 write; Kessel→0x379 write; 0x602→HK2 write | – | ❓ open | 2, 0, 0, 0x0200; never changed |
| `0x000b` | – |  | FEK reads Kessel | HK1 reads Kessel | – | – no value |  |
| `0x06af` | – (debug) | | Bedienteil → Manager | Panel→Manager write | Debug Bedienteil 0x06AF | ❓ open | panel writes 1, more often in the expert menus |
| `0x4e8b` | – (debug) | | Bedienteil → Manager | Panel→Manager write | Debug Bedienteil 0x4E8B | ❓ open | panel writes 2 every few minutes |
| `0xc32f` | – |  | 0x514 | Panel reads 0x514 | – | – no value | read by the panel in the expert menus |
| `0x0012` | `VERSTELLTE_RAUMSOLLTEMP` | `et_dec_val` | FEK → 0x601 | HK1→0x601 write; HK1 reads 0x601 | – | ✅ test | room setpoint of the FEK (215 = 21.5 °C); changes at once with Komfort/Eco on the FEK (2026-11-16) |
