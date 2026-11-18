
# Einstellungen pass 2 (18:18–20:28, 2026-11-17)

Continuation of [2026-11-17-expert-menus.md](2026-11-17-expert-menus.md). The maintainer browsed the Einstellungen
menus (code 1000) page by page with photos; the panel's reads and writes were matched live. Panel frames:
[capture](captures/2026-11-17-2018-expert-settings-panel-traffic.txt). Several settings were changed on purpose and
set back; the panel's own writes are listed under "Changed and restored".

## Changed and restored (all back at the start value by 20:28)
- Festwert/Einsatzgrenze test (planned test 20): panel shows AUS; the Kessel answers `0x9000` to the panel, `0xA000` to the ESP (see TODO history).
- Programme > Warmwasserprogramm: time windows set and cleared (see the properties table).
- Programme > Aufheizprogramm on/off, Partyprogramm 3 h, Ferienprogramm read.
- Heizen > Pumpenzyklen off/on (`0xFDB2`).
- Heizen > Untere Einsatzgrenze HZG: −39.0 °C, back to AUS (`0x01AE`).
- Warmwasser > WW-Korrektur 0.5 (`0x0263`), WW Lernfunktion on (`0x027E`), Kombispeicher on (`0x070D`), Antilegionellen on for 2 s (`0x0101`); all back.
- Kühlen: Kühlen on/off, Kühlmodus aktiv/passiv (`0x0287`), Flächenkühlung and Gebläsekühlung on/off (`0x025F`, `0x025B`); all back. Flächen- and Gebläsekühlung exclude each other (the Manager writes the other to 0, and `0x0645` = 1).
- Inbetriebnahme > Quelle > Source medium: arrows stepped through all 9 values (`0xFDAE` 0–8); back to Ethylene glycol.
- Inbetriebnahme > Kompressor > Quick start on/off (`0x0669`, 1 = ON); back to OFF. Single phase operation on/off (`0x070E`); back to OFF.
- Inbetriebnahme > Sensorkalibrierung: the panel's arrows wrote the Manager offsets `0x0658`/`0x0659`/`0x065A` = 1, 2, 3 (0.1/0.2/0.3 °C); reset to 0 at 20:27.
- Inbetriebnahme > Sprache: English for a test (`0x4E8B` unchanged at 2); back to Deutsch 20:28.

## Newly named (confirmed by a change or a display)
- `0xFDB2` = Pumpenzyklen EIN/AUS (1 = EIN)
- `0x068F` = Pufferbetrieb (1 = EIN) — TBD_18 solved
- `0x0028` = Maximale Rücklauftemperatur 30.0 °C (firmware name SOLLWERT_MAX_HK1 is wrong)
- `0x01E8` = Maximale Vorlauftemperatur 40.0 °C
- `0x01C0` = Festwertbetrieb (AUS)
- `0x0679` (Manager) = Heizkreis optimal (`0x9000` = AUS)
- `0x0A00` = Frostschutz 4.0 °C
- `0x0FDB4` (`0xFDB4`) = Sommerbetrieb EIN (`0x0100`)
- `0x01BF` = Sommerbetrieb Außentemperatur 16.5 °C
- `0xFDB3` = Sommerbetrieb Gebäudedämpfung (high byte; 03)
- `0x0263` = WW-Korrektur (tenths of a degree)
- `0x027E` = WW Lernfunktion (1 = EIN)
- `0x070D` = Kombispeicher (1 = EIN)
- `0x0101` = Antilegionellenbehandlung (`0x0100` = EIN)
- `0x0288` = Dynamik aktiv (Aktivkühlung), 10
- `0x0645` = change notice of the Manager when cooling modes exclude each other (value 1)
- `0x0669` (Manager) = Quick start (1 = ON)
- `0x0658`/`0x0659`/`0x065A` (Manager) = sensor calibration offsets in tenths of a degree: Actual flow temperature WW, Actual flow temperature, Actual return temperature (0 = no offset)
- `0xFDAE` = Quellenmedium: 0 Ethylene glycol, 1 Potassium carbonate, 2–6 Extract air modules 0/30/60/120/180, 7 Water, 8 Groundwater module
- `0xFDDE`–`0xFDE1` (Manager) = Sommerzeit start day/month and end day/month (25.03. / 25.10.)
- `0x011A` Aufheizprogramm ON/OFF; `0x01BA`–`0x01BE` its settings (Steigung 10 K, Sockel 40.0 °C / 2 Tage, Maximal 45.0 °C / 5 Tage)
- `0x0A06`/`0x0013` WW Eco 45.0 / WW Komfort 52.0 °C; `0x0022` WW Hysterese 4.5 K
- `0x0263`, `0x070D`, `0x0101`, `0x027E`, `0x0135`, `0xFDBA`, `0xFDB9`, `0x0181`, `0x0181`: Warmwasser Grundeinstellung, see above

## Read, still unknown
- `0x059F`, `0x05A0` (no value on the NHZ page), `0x059D` (no value), `0x0135`, `0xFDBA`, `0xFDB9`, `0x0181`, `0x0705`
- `0xFDB6`, `0x0030`, `0x4EBA`, `0x0914`, `0xFDC0`, `0x070F`, `0xC32F` (no value)
- `0x0669`–`0x0669` answered; `0x4E5A`, `0x0658`–`0x065A`: see calibration above; `0x06AE` (0, polled in the Inbetriebnahme menus)
- `0x03E3` (no value; read with the active/passive cooling pages)

## Language
- `0x4E8B` (`TBD_11`) stayed 2 during an English test (20:23–20:24), so the language is not on the bus. The language list is not mapped on the bus.

## Not touched
- Notbetrieb, Reset (Wärmepumpe, Fehlerliste, System), Inbetriebnahme > Kompressor > Idle time, Sensorkalibrierung values (back to 0.0).
