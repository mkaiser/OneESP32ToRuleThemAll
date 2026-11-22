# Control panel (WPM3i / FES): menu tree

Source of truth for the layout of the control panel "FES" (CAN node `0x100`, software 417-07) of the TTF07 C with WPM3i,
reconstructed from the owner's photos (2026-11-16..22) and the panel-traffic captures in [raw](.wiki/raw/).
Values are examples from the photo date (times CET), not current settings; some were set on purpose during tests.
Access: every menu and page can be **browsed without the code**, including Inbetriebnahme (photos 2026-11-22); the
panel asks for the expert code (1000, user manual) only when a value is changed. The code is checked by the panel
itself (not visible on the bus).
HK1 heating pages (Heizkreis 1 settings, Heizprogramm) are hidden while a FEK or the ESP's FEK emulation owns HK1;
the Kühlen menu appears only with a FEK (real or emulated), see [heating control](.wiki/wiki/heating-control.md) and [cooling](.wiki/wiki/cooling.md).

Conventions: labels as on the panel (upper case); `[ENGLISH]` = only the English label is known (photos with the panel
set to English, 2026-11-17 20:20–20:27); `(?)` = uncertain transcription; `>` = submenu; "–" = register unknown;
"panel-local" = the notes say no bus read happens. Navigation: MENU goes one level up; the start screen appears after a timeout or after pressing MENU at the top. Breadcrumbs on the panel are abbreviated to three letters
("HAU / EIN / HEI < GRUNDEINSTELLUNG").

## Tree overview

- Start screen (date, time, alarm box, operating mode)
- HAUPTMENÜ (photo 2026-11-22, no code: INFO, DIAGNOSE, PROGRAMME, EINSTELLUNGEN, INBETRIEBNAHME, ZURÜCK)
  - INFO (ANLAGE, WÄRMEPUMPE, ZURÜCK)
    - ANLAGE
      - RAUMTEMPERATUR
      - HEIZUNG
      - WARMWASSER
      - ELEKTRISCHE NACHERWÄRMUNG
      - QUELLE
    - WÄRMEPUMPE
      - PROZESSDATEN
      - WÄRMEMENGE
      - LEISTUNGSAUFNAHME
      - LAUFZEIT
      - STARTS (last entry)
  - DIAGNOSE
    - STATUS ANLAGE
    - STATUS WÄRMEPUMPE
    - SYSTEM
      - BUSTEILNEHMER
      - WÄRMEPUMPENTYP
    - INTERNE BERECHNUNG
    - FEHLERLISTE (count on the list: 00 on 2026-11-22)
    - RELAISTEST ANLAGE (second screen, then ZURÜCK)
  - PROGRAMME
    - HEIZPROGRAMM
    - WARMWASSERPROGRAMM
    - PARTYPROGRAMM
    - FERIENPROGRAMM
    - AUFHEIZPROGRAMM
  - EINSTELLUNGEN
    - ALLGEMEIN
      - SOMMERZEIT EINSTELLEN
    - HEIZEN
      - HEIZKREIS 1
      - GRUNDEINSTELLUNG
        - SOMMERBETRIEB
      - PUMPENZYKLEN (EIN/AUS editor)
      - ELEKTRISCHE NACHERWÄRMUNG
    - WARMWASSER
      - WARMWASSERTEMPERATUREN
      - GRUNDEINSTELLUNG
      - ELEKTRISCHE NACHERWÄRMUNG
    - KÜHLEN
      - KÜHLMODUS
      - PASSIVKÜHLUNG (shown with Kühlmodus passiv)
        - FLÄCHENKÜHLUNG
        - GEBLÄSEKÜHLUNG
      - AKTIVKÜHLUNG (shown with Kühlmodus aktiv)
        - FLÄCHENKÜHLUNG
        - GEBLÄSEKÜHLUNG
  - INBETRIEBNAHME (visible without code)
    - CODE EINGEBEN
    - SPRACHE
    - QUELLE
      - QUELLENMEDIUM
    - HEIZEN
    - WARMWASSER
    - VERDICHTER
    - NOTBETRIEB
    - RESET
    - SENSOR ABGLEICH

## Pages

### Start screen

| Line (as displayed) | Example value (2026-11-17 20:28) | Register (node, address, name) | Notes |
|---|---|---|---|
| Header DIENSTAG 17.11.26 / 20:28 UHR; SONNTAG 22.11.26 / 10:09 UHR | – | – | panel clock |
| AUSSENTEMPERATUR (normal operation) | 3.6 °C (2026-11-22) | Kessel `0x000c` AUSSENTEMP | shown instead of the alarm box when there is no error |
| WW-ISTTEMPERATUR | 48.3 °C (2026-11-22) | Kessel `0x000e` SPEICHERISTTEMP | |
| RÜCKLAUFISTTEMPERATUR | 26.9 °C (2026-11-22) | Kessel `0x0016` RUECKLAUFISTTEMP | |
| Alarm box FEHLER / HOCHDRUCK / BITTE KUNDENDIENST INFORMIEREN | HOCHDRUCK | Manager `0x1388` FEHLERNUMMER_WPM | 18 = Hochdruck; [registers](.wiki/wiki/ttf07c-registers.md) |
| ECO-BETRIEB / KOMFORTBETRIEB (status line) | ECO-BETRIEB; KOMFORTBETRIEB (2026-11-22 15:22) | Manager `0x0112` PROGRAMMSCHALTER | follows the Programmschalter (switched 2026-11-22), **not** the FEK/emulation phase; below it a row of symbols for what runs (compressor, pump, heating) |

### Info > Anlage > Raumtemperatur

Registers: [registers](.wiki/wiki/ttf07c-registers.md). Also photographed 2026-11-16 10:14 (20.5 / 21.0 / 52.7 % / 10.5 °C).

| Line (as displayed) | Example value (2026-11-17 17:40) | Register (node, address, name) | Notes |
|---|---|---|---|
| ISTTEMPERATUR FEK | 21.2 °C | Manager `0x4e64` RAUMISTTEMP_WPM | |
| SOLLTEMPERATUR FEK | 22.0 °C (?) | Manager `0x4e66` RAUMSOLLTEMP_WPM | value faint; read gave 220 = 22.0 (emulation Komfort) |
| RAUMFEUCHTE | 52.5 % | Manager `0x069e` RAUMFEUCHTE_WPM | |
| TAUPUNKTTEMPERATUR | 11.1 °C | Kessel `0x0264` TAUPUNKT_HK1 | |
| ZURÜCK | | | Manager `0x4e63`, `0x4e65` also read (`0x8000`, not shown) |

### Info > Anlage > Heizung

Registers: [registers](.wiki/wiki/ttf07c-registers.md). Three screens. Also photographed 2026-11-16 10:14.

| Line (as displayed) | Example value (2026-11-17 17:41) | Register (node, address, name) | Notes |
|---|---|---|---|
| AUSSENTEMPERATUR | 10.0 °C | Kessel `0x000c` AUSSENTEMP | |
| ISTTEMPERATUR HK 1 | 25.4 °C | Kessel `0x02ca` HKISTTEMP | |
| SOLLTEMPERATUR HK 1 | 25.5 °C | Kessel `0x01d5` PUFFERSOLLTEMP | same register as Puffersolltemperatur; line absent on 2026-11-16 10:14 |
| VORLAUFISTTEMPERATUR WP | 26.2 °C | Kessel `0x06a1` VORLAUFISTTEMP | |
| VORLAUFISTTEMPERATUR NHZ | 27.3 °C | Kessel `0x06a0` (Vorlauf Ist NHZ) | = MFG `0xfdf5` |
| RÜCKLAUFISTTEMPERATUR | 26.1 °C | Kessel `0x0016` RUECKLAUFISTTEMP | |
| FESTWERTSOLLTEMPERATUR | AUS | Kessel `0x01c0` FESTWERTBETRIEB | `0x9000` = AUS |
| PUFFERISTTEMPERATUR | 25.4 °C | Kessel `0x0078` PUFFERISTTEMP | |
| PUFFERSOLLTEMPERATUR | 25.5 °C | Kessel `0x01d5` PUFFERSOLLTEMP | = FEK/emulation flow setpoint |
| HEIZUNGSDRUCK | 1.34 bar | Kessel `0x0674` DRUCK_HEIZKREIS | |
| VOLUMENSTROM | 0.00 l/min | Kessel `0x0673` VOLUMENSTROM | 19.01 l/min on 2026-11-16 10:14 |
| ANLAGENFROST | 4.0 °C | Kessel `0x0a00` ANLAGENFROST | |
| ZURÜCK | | | also read, not shown: Kessel `0x068f` (= 1), `0x06a2`, `0x602` `0x000f` |

### Info > Anlage > Warmwasser

| Line (as displayed) | Example value (2026-11-17 17:43) | Register (node, address, name) | Notes |
|---|---|---|---|
| ISTTEMPERATUR | 42.8 °C | Kessel `0x000e` SPEICHERISTTEMP | [registers](.wiki/wiki/ttf07c-registers.md) |
| SOLLTEMPERATUR | 45.0 °C | Kessel `0x0003` SPEICHERSOLLTEMP | = WW Eco at that time |
| VOLUMENSTROM | 0.00 l/min | – | no read of its own (`0x0673` cached?) |
| ZURÜCK | | | |

### Info > Anlage > Elektrische Nacherwärmung

Title truncated on screen ("ELEKTRISCHE NACHERWÄR"). Read order = display order. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 17:44) | Register (node, address, name) | Notes |
|---|---|---|---|
| BIVALENZTEMPERATUR HZG | -19.0 °C | Kessel `0x01ac` BIVALENZTEMPERATUR_HZG | |
| EINSATZGRENZE HZG | AUS | Kessel `0x01ae` EINSATZGRENZE_HZG | `0x9000` = AUS |
| BIVALENZTEMPERATUR WW | -19.0 °C | Kessel `0x01ad` BIVALENZTEMPERATUR_WW | |
| EINSATZGRENZE WW | AUS | Kessel `0x01af` EINSATZGRENZE_WW | |
| ZURÜCK | | | |

### Info > Wärmepumpe > Wärmemenge

Breadcrumb "HAU / INF / WÄR < WÄRMEMENGE"; parent confirmed as WÄRMEPUMPE (photo 2026-11-22). Two screens. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 17:47; 2026-11-22) | Register (node, address, name) | Notes |
|---|---|---|---|
| VD HEIZEN TAG | 58.027 kWh (?); 35.848 kWh | Kessel `0x092a–0x0931` WAERMEERTRAG_* | per-line address not in the notes |
| VD HEIZEN SUMME | 76.982 MWh; 77.189 MWh | Kessel `0x092a–0x0931` WAERMEERTRAG_* | |
| VD WARMWASSER TAG | 0.213 kWh; 3.094 kWh | Kessel `0x092a–0x0931` WAERMEERTRAG_* | |
| VD WARMWASSER SUMME | 15.349 MWh; 15.384 MWh | Kessel `0x092a–0x0931` WAERMEERTRAG_* | |
| NHZ HEIZEN SUMME | 6.688 MWh; 6.688 MWh | Kessel `0x0929` + `0x0927` | MWh + kWh part (upstream `0x0928` is 0 here) |
| NHZ WARMWASSER SUMME | 0.538 MWh; 0.541 MWh | Kessel `0x0925` + `0x0923` | second screen |
| ZURÜCK | | | |

### Info > Wärmepumpe > Laufzeit

Breadcrumb "HAU / INF / WÄ < LAUFZEIT" (Info > Wärmepumpe > Laufzeit; the notes' "Info > Wärmemenge > Laufzeit" is wrong). [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 17:48) | Register (node, address, name) | Notes |
|---|---|---|---|
| VD HEIZEN | 7601 h | Kessel `0x07fc` LAUFZEIT_VD_HEIZEN | |
| VD WARMWASSER | 1344 h | Kessel `0x0802` LAUFZEIT_VD_WW | |
| NHZ 1 | 15 h | Kessel `0x0259` LAUFZEIT_NHZ1 | |
| NHZ 2 | 13 h | Kessel `0x025a` LAUFZEIT_NHZ2 | |
| NHZ 1/2 | 997 h (?) | Kessel `0x0805` LAUFZEIT_NHZ1_2 | value faint; read gave 997 |
| ZURÜCK | | | no more lines (owner, 2026-11-22); `0x07ff` LAUFZEIT_VD_KUEHLEN read, hidden (`0x8000`) |

### Info > Wärmepumpe > Prozessdaten

Breadcrumb "HAU / INF / WÄR < PROZESSDATEN"; the whole page is three lines (photo 2026-11-22, Heißgas is the first
line). The notes' page "Kältekreis" (17:45:45: 34.9 °C, 15.6 bar, 10.3 bar) reads the same three registers: it is
this page. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 22:00; 2026-11-22) | Register (node, address, name) | Notes |
|---|---|---|---|
| HEISSGASTEMPERATUR | 60.0 °C; 30.9 °C | Kessel `0x0265` HEISSGAS_TEMP | |
| DRUCK HOCHDRUCK | 20.4 bar; 10.1 bar | Kessel `0x0268` DRUCK_HOCHDRUCK | refrigerant high pressure, raw/10 |
| DRUCK NIEDERDRUCK | 8.0 bar; 9.9 bar | Kessel `0x07a5` DRUCK_NIEDERDRUCK | refrigerant low pressure, raw/10 |
| ZURÜCK | | | |

### Info > Anlage > Quelle

Breadcrumb "HAU / INF / ANL < QUELLE" (photo 2026-11-22). [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-22; 2026-11-17 notes) | Register (node, address, name) | Notes |
|---|---|---|---|
| QUELLENTEMPERATUR | 7.5 °C | Kessel `0x01d4` QUELLE_IST | |
| QUELLENTEMPERATUR MIN | -9.0 °C | Kessel `0x01b0` QUELLENTEMP_MIN | |
| QUELLENDRUCK | 2.08 bar; 2.06 bar | Kessel `0x0675` QUELLENDRUCK | |
| ZURÜCK | | | |

### Info > Wärmepumpe > Leistungsaufnahme

Breadcrumb "HAU / INF / WÄR < LEISTUNGSAUFNAHME" (photo 2026-11-22). [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-22) | Register (node, address, name) | Notes |
|---|---|---|---|
| VD HEIZEN TAG | 7.854 kWh | Kessel `0x091a–0x0921` EL_ENERGIEAUFNAHME_* | per-line address not in the notes |
| VD HEIZEN SUMME | 13.218 MWh | Kessel `0x091a–0x0921` EL_ENERGIEAUFNAHME_* | |
| VD WARMWASSER TAG | 3.152 kWh | Kessel `0x091a–0x0921` EL_ENERGIEAUFNAHME_* | |
| VD WARMWASSER SUMME | 5.226 MWh | Kessel `0x091a–0x0921` EL_ENERGIEAUFNAHME_* | |
| ZURÜCK | | | |

### Info > Wärmepumpe > Starts

Photo 2026-11-22 ("HAU / INF / WÄR < STARTS"). [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-22 15:3x) | Register (node, address, name) | Notes |
|---|---|---|---|
| VERDICHTER | 24221 | Kessel `0x071c`/`0x071d` VERDICHTER_STARTS (likely) | same count as HA "Verdichterstarts" |
| ZURÜCK | | | |

### Diagnose > Status Anlage

No per-line reads: the page shows bits of Manager `0x4e5e` BETRIEBS_STATUS_WPM (bits from the relay test,
[Betriebsstatus](.wiki/wiki/betriebsstatus.md)). Two screens. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 17:49 idle; 2026-11-22 ~17:3x heating) | Register (node, address, name) | Notes |
|---|---|---|---|
| PUFFERLADEPUMPE | ☐; ☑ | Manager `0x4e5e` bit 7 | on while heating (status `0x40C1`) |
| WARMWASSERVENTIL | ☐; ☐ | Manager `0x4e5e` bit 9 (?) | the notes conflict: bit 9 = Entleerung HYD in the relay test; off while heating |
| HEIZKREISPUMPE | ☐; ☑ | Manager `0x4e5e` bit 0 | on while heating |
| MISCHERPUMPE | ☐; ☐ | Manager `0x4e5e` bit 1 | |
| MISCHER AUF | ☐; ☐ | Manager `0x4e5e` bit 2 | |
| MISCHER ZU | ☐; ☐ | Manager `0x4e5e` bit 3 | |
| QUELLENPUMPE | ☐; ☑ | Manager `0x4e5e` bit 6 | on while heating |
| KÜHLBETRIEB | ☐; ☐ | Manager `0x4e5e` bit 13 | |
| EVU-SPERRE | ☐; ☐ | – | bit unknown; checkbox drawn slightly above the line |
| ZURÜCK | | | entering Diagnose reads Manager `0x068e` (20), `0x0691`, `0x0692`, `0x0074` |

### Diagnose > Status Wärmepumpe

| Line (as displayed) | Example value (2026-11-17 17:52 idle; 2026-11-22 ~17:3x heating) | Register (node, address, name) | Notes |
|---|---|---|---|
| RESTSTILLSTAND | 38 min; 00 min | Manager `0x0668` VERDICHTER_RESTSTILLSTAND | counts down from Kessel `0xfdb1` (60 min); [registers](.wiki/wiki/ttf07c-registers.md) |
| VERDICHTER | ☐; ☑ | Manager `0x4e5e` bit 14 | from the status word, no read |
| NHZ 1 | ☐; ☐ | Manager `0x4e5e` stage bits (`0x0090`) | from the status word, no read |
| NHZ 2 | ☐; ☐ | Manager `0x4e5e` stage bits (`0x00A0`) | from the status word, no read |
| ZURÜCK | | | |

### Diagnose > System

| Line (as displayed) | Example value (2026-11-17 17:52) | Register (node, address, name) | Notes |
|---|---|---|---|
| BUSTEILNEHMER > | | | entering reads Manager `0x0294` = 63 (meaning open) |
| WÄRMEPUMPENTYP > | | | |
| ZURÜCK | | | |

### Diagnose > System > Busteilnehmer

Columns # / BUSTEILNEHMER / SOFTWARE. Same on 2026-11-18 17:15. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 17:53) | Register (node, address, name) | Notes |
|---|---|---|---|
| 01. WPM3i | 391 - 10 | panel-local | no bus read (cached) |
| 02. FES | 417 - 07 | panel-local | the control panel itself |
| 03. FEK | 416 - 03 | HK1 `0x0199` FET_SOFTWARE + `0x019a` FET_SOFTWARESTAND | on 2026-11-17 answered by the ESP's FEK emulation |
| 04. MFG | 18 | Manager `0x4e69` (MFG software) | also read: Manager `0x4e68` = 2, not shown |

### Diagnose > System > Wärmepumpentyp

| Line (as displayed) | Example value (2026-11-17 17:54) | Register (node, address, name) | Notes |
|---|---|---|---|
| TTF MFG (large text) | TTF MFG | – | no read on the page; Manager `0x4e68` = 2 is the likely type code |

### Diagnose > Interne Berechnung

| Line (as displayed) | Example value (2026-11-17 17:54) | Register (node, address, name) | Notes |
|---|---|---|---|
| ZEITINTERVALL | 00 | Manager `0x0691` (likely) | no read of its own; source from the Diagnose-menu reads; [registers](.wiki/wiki/ttf07c-registers.md) |
| EINGESCHALTETE STUFEN | 00 | Manager `0x0692` (likely) | same; confirm while the NHZ runs |

### Diagnose > Fehlerliste

10 screens ("1/10" … "10/10"), 2 entries each, newest first; the second entry shows only "." instead of its number.
Full list: [Fehlerliste note](.wiki/raw/2026-11-17-fehlerliste-panel.md), codes: [errors](.wiki/wiki/errors.md). [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 14:20 / 20:46) | Register (node, address, name) | Notes |
|---|---|---|---|
| Page indicator n/10 | 1/10 | – | |
| 01. (error text) | KEINE LEISTUNG (14:20) / HOCHDRUCK (20:46) | Manager `0x0b9b` FEHLERLISTE_CODE | panel writes Manager `0x0b9a` FEHLERLISTE_INDEX to request entries |
| (time date) | 13:11 17.11.26 / 20:24 17.11.26 | Manager `0x0b9f`–`0x0ba3` FEHLERLISTE_MINUTE … _JAHR | |
| . (error text) | NIEDERDRUCK 18:31 09.01.26 (14:20) / ABTAUEN 13:11 17.11.26 (20:46) | Manager `0x0b9b` FEHLERLISTE_CODE | ABTAUEN at 13:11 contradicts KEINE LEISTUNG 13:11 seen earlier |

### Diagnose > Relaistest Anlage

The panel writes Kessel `0x0693` RELAISTEST_AKTIV = 1 on entering, 0 on leaving, and Kessel `0x067a`
RELAISTEST_RELAIS = relay number of the line switched on (one at a time). The filled box on the selected line may be
highlight styling. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 17:56–17:58) | Register (node, address, name) | Notes |
|---|---|---|---|
| PUFFERLADEPUMPE | ■ (selected) | Kessel `0x067a` = 1 | |
| WARMWASSERVENTIL | ☐ | Kessel `0x067a` = 2 | |
| HEIZKREISPUMPE | ☐ | Kessel `0x067a` = 3 | |
| MISCHERPUMPE | ☐ | Kessel `0x067a` = 4 | |
| MISCHER AUF | ☐ | Kessel `0x067a` = 5 | |
| MISCHER ZU | ■ (selected) | Kessel `0x067a` = 6 | |
| NHZ 1 | ☐ | Kessel `0x067a` = 7 | |
| NHZ 2 | ☐ | Kessel `0x067a` = 8 | |
| NHZ 3 | ☐ | Kessel `0x067a` = 12 | |
| QUELLENPUMPE | (?) | Kessel `0x067a` = 9 | checkbox cut off |
| KÜHLBETRIEB | ■ (selected) | Kessel `0x067a` = 10 | |
| ENTLEERUNG HYD | ☐ | Kessel `0x067a` = 11 | |
| ZURÜCK | | | |

### Programme

| Line (as displayed) | Example value (2026-11-17 18:03) | Register (node, address, name) | Notes |
|---|---|---|---|
| HEIZPROGRAMM > | | | |
| WARMWASSERPROGRAMM > | | | |
| PARTYPROGRAMM > | 0 h | Manager `0xfdbf` PARTYPROGRAMM | [registers](.wiki/wiki/ttf07c-registers.md) |
| FERIENPROGRAMM > | | | |
| AUFHEIZPROGRAMM > | AUS | Kessel `0x011a` AUFHEIZPROGRAMM | |
| ZURÜCK | | | no more lines (owner, 2026-11-22) |

### Programme > Heizprogramm

| Line (as displayed) | Example value (2026-11-17 18:15) | Register (node, address, name) | Notes |
|---|---|---|---|
| (time windows) | hidden | HK1 `0x1410`… (groups `0x1480`/`0x1490`/`0x14a0`) | hidden while FEK/emulation owns HK1; read without FEK 2026-11-17 22:12: every day 10:00–16:00 (no photo); [registers](.wiki/wiki/ttf07c-registers.md) |
| ZURÜCK | | | only line shown; cursor shape suggests lines above |

### Programme > Warmwasserprogramm

Two screens: day/group selector (+/−) and day page (24-h ring + 3 windows). Day d window w = Kessel
`0x1710 + 0x10·d + w`; start/end bytes in 15-min steps; `0x8080` = "--:-- --:--", `0x0000` = "00:00 - 00:00" (whole day).
Values are test values, all cleared again by 18:15. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 18:06–18:13) | Register (node, address, name) | Notes |
|---|---|---|---|
| Day selector MONTAG … SONNTAG | MONTAG | Kessel `0x1710–0x1772` WW_PROGRAMM_MO_1 … SO_3 | |
| Group Mo - Fr (MONTAG-FREITAG) | ■■■■■☐☐ | Kessel `0x1780` (group) | writing a group fills its days |
| Group Sa - So (SAMSTAG-SONNTAG) | ☐☐☐☐☐■■ | Kessel `0x1790` (group) | |
| Group Mo - So (MONTAG-SONNTAG) | ■■■■■■■ | Kessel `0x17a0` (group) | |
| Window 1 | 00:30 - 01:00 (Mo - Fr) | Kessel `0x1780` / day `+0` | Monday alone showed 00:00 - 00:00 at 18:06 |
| Window 2 | 01:00 - 01:30 | Kessel `0x1781` / day `+1` | |
| Window 3 | 01:45 - 02:15 | Kessel `0x1782` / day `+2` | |

### Programme > Partyprogramm

| Line (as displayed) | Example value (2026-11-17 18:18) | Register (node, address, name) | Notes |
|---|---|---|---|
| PARTYPROGRAMM (edit screen) | 3 h | Manager `0xfdbf` PARTYPROGRAMM | hours in the high byte; test, back to 0 h; [registers](.wiki/wiki/ttf07c-registers.md) |

### Programme > Ferienprogramm

| Line (as displayed) | Example value (2026-11-17 18:16) | Register (node, address, name) | Notes |
|---|---|---|---|
| FERIENBEGINN > | 24.06.24 | Manager `0x011b`–`0x011d` (day, month, year) | high byte; [registers](.wiki/wiki/ttf07c-registers.md) |
| FERIENENDE > | 16.07.24 | Manager `0x011e`–`0x0120` | |
| ZURÜCK | | | |

### Programme > Aufheizprogramm

| Line (as displayed) | Example value (2026-11-17 18:17) | Register (node, address, name) | Notes |
|---|---|---|---|
| AUFHEIZPROGRAMM > | EIN | Kessel `0x011a` AUFHEIZPROGRAMM | switched on for the test, back to AUS; [registers](.wiki/wiki/ttf07c-registers.md) |
| SOCKELTEMPERATUR > | 40.0 °C | Kessel `0x01bb` | |
| DAUER SOCKEL > | 2 TAGE | Kessel `0x01bc` | |
| MAXIMAL TEMPERATUR > | 45.0 °C | Kessel `0x01bd` | |
| DAUER MAXIMALTEMPERATUR > | 5 TAGE | Kessel `0x01be` | |
| STEIGUNG PRO TAG > | 10 K | Kessel `0x01ba` | |
| ZURÜCK | | | |

### Einstellungen > Allgemein

| Line (as displayed) | Example value (2026-11-17 20:07) | Register (node, address, name) | Notes |
|---|---|---|---|
| ZEIT / DATUM > | 20:07 17.11.26 | – | page read not matched |
| SOMMERZEIT EINSTELLEN > | | | |
| KONTRAST > | 05 | – | |
| HELLIGKEIT > | 50 % | – | |
| HELLIGKEIT AUS > | 00 % | – | |
| ZURÜCK | | | no more lines (owner, 2026-11-22) |

### Einstellungen > Allgemein > Sommerzeit einstellen

| Line (as displayed) | Example value (2026-11-17 20:08) | Register (node, address, name) | Notes |
|---|---|---|---|
| TAG ANFANG > | 25.MÄR | Manager `0xfdde`/`0xfddf` (day, month) | high byte; [registers](.wiki/wiki/ttf07c-registers.md) |
| TAG ENDE > | 25.OKT | Manager `0xfde0`/`0xfde1` (day, month) | |
| ZURÜCK | | | |

### Einstellungen > Heizen > Heizkreis 1

Same on 2026-11-16 11:32. Other HK1 lines are hidden while FEK/emulation owns HK1.

| Line (as displayed) | Example value (2026-11-17 20:10) | Register (node, address, name) | Notes |
|---|---|---|---|
| MINIMAL TEMPERATUR > | 15.0 °C | `0x601` `0x4ea7` MINTEMP | [registers](.wiki/wiki/ttf07c-registers.md) |
| ZURÜCK | | | |

### Einstellungen > Heizen > Pumpenzyklen

Value editor, not a list (photo 2026-11-22): `+`/`-` arrows around the value. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-22) | Register (node, address, name) | Notes |
|---|---|---|---|
| PUMPENZYKLEN | EIN | Kessel `0xfdb2` PUMPENZYKLEN | EIN/AUS |

### Einstellungen > Heizen > Grundeinstellung

Two screens. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 20:10) | Register (node, address, name) | Notes |
|---|---|---|---|
| PUFFERBETRIEB > | EIN | Kessel `0x068f` PUFFERBETRIEB | 1 = EIN |
| SOMMERBETRIEB > | | | submenu |
| MAXIMALE RÜCKLAUFTEMP > | 30.0 °C | Kessel `0x0028` MAXRUECKLAUFTEMP | |
| MAXIMALE VORLAUFTEMP > | 40.0 °C | Kessel `0x01e8` MAXVORLAUFTEMP | |
| FESTWERTBETRIEB > | AUS | Kessel `0x01c0` FESTWERTBETRIEB | `0x9000` = AUS |
| HEIZKREIS OPTIMAL > | AUS | Manager `0x0679` (Heizkreis optimal) | `0x9000` = AUS |
| FROSTSCHUTZ > | 4.0 °C | Kessel `0x0a00` ANLAGENFROST | |
| ZURÜCK | | | |

### Einstellungen > Heizen > Grundeinstellung > Sommerbetrieb

Same values on 2026-11-21 22:26. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 20:10) | Register (node, address, name) | Notes |
|---|---|---|---|
| SOMMERBETRIEB > | EIN | Kessel `0xfdb4` SOMMERBETRIEB | `0x0100` = EIN |
| AUSSENTEMPERATUR > | 16.5 °C | Kessel `0x01bf` SOMMERBETRIEB_HEIZGRENZE | |
| GEBÄUDEDÄMPFUNG > | 03 | Kessel `0xfdb3` (Gebäudedämpfung) | high byte |
| ZURÜCK | | | |

### Einstellungen > Heizen > Elektrische Nacherwärmung

| Line (as displayed) | Example value (2026-11-17 20:12) | Register (node, address, name) | Notes |
|---|---|---|---|
| BIVALENZTEMPERATUR HZG > | -19.0 °C | Kessel `0x01ac` BIVALENZTEMPERATUR_HZG | [registers](.wiki/wiki/ttf07c-registers.md) |
| UNTERE EINSATZGRENZE HZG > | AUS | Kessel `0x01ae` EINSATZGRENZE_HZG | tested −39.0 °C, back to AUS |
| ZURÜCK | | | also read: Kessel `0x059f`, `0x05a0`, `0x059d` (no value) |

### Einstellungen > Warmwasser > Warmwassertemperaturen

Title truncated on screen ("WARMWASSERTEMPERATU"); full name from the Warmwasser list (photo 2026-11-22: WARMWASSERTEMPERATUREN, GRUNDEINSTELLUNG, ELEKTRISCHE NACHERWÄRMUNG, ZURÜCK).

| Line (as displayed) | Example value (2026-11-17 20:13) | Register (node, address, name) | Notes |
|---|---|---|---|
| KOMFORT TEMPERATUR > | 52.0 °C | Kessel `0x0013` WW_KOMF_TEMP | [registers](.wiki/wiki/ttf07c-registers.md) |
| ECO TEMPERATUR > | 45.0 °C | Kessel `0x0a06` WW_ECO_TEMP | |
| ZURÜCK | | | |

### Einstellungen > Warmwasser > Grundeinstellung

[registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 20:13) | Register (node, address, name) | Notes |
|---|---|---|---|
| WARMWASSERHYSTERESE > | 4.5 K | Kessel `0x0022` WW_HYSTERESE | |
| WW LERNFUNKTION > | AUS | Kessel `0x027e` (WW Lernfunktion) | 1 = EIN |
| WW-KORREKTUR > | 0.0 °C | Kessel `0x0263` (WW-Korrektur) | tenths of a degree |
| KOMBISPEICHER > | AUS | Kessel `0x070d` (Kombispeicher) | 1 = EIN |
| ANTILEGIONELLENBEHANDLUN[G] > | AUS | Kessel `0x0101` ANTILEGIONELLEN | EIN on 2026-11-21 22:24 |
| (last line) | | | Antilegionellenbehandlung is the last entry (owner, 2026-11-22); the page also reads Kessel `0x0135`, `0xfdba`, `0xfdb9`, `0x0181`, not shown (meaning open) |

### Einstellungen > Warmwasser > Elektrische Nacherwärmung

| Line (as displayed) | Example value (2026-11-17 20:13) | Register (node, address, name) | Notes |
|---|---|---|---|
| BIVALENZTEMPERATUR WW > | -19.0 °C | Kessel `0x01ad` BIVALENZTEMPERATUR_WW | [registers](.wiki/wiki/ttf07c-registers.md) |
| UNTERE EINSATZGRENZE WW > | AUS | Kessel `0x01af` EINSATZGRENZE_WW | |
| ZURÜCK | | | |

### Einstellungen > Kühlen

Shown only with a FEK (real or emulated). [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-16 17:58) | Register (node, address, name) | Notes |
|---|---|---|---|
| KÜHLEN > | EIN | Kessel `0x06a4` KUEHLEN_EIN | |
| KÜHLMODUS > | PASSIV | Kessel `0x0287` KUEHLMODE | 0 = passiv, 1 = aktiv |
| PASSIVKÜHLUNG > | | | submenu; with Kühlmodus AKTIV the line reads AKTIVKÜHLUNG > (photo 2026-11-22: KÜHLEN EIN, KÜHLMODUS AKTIV, AKTIVKÜHLUNG, ZURÜCK) |
| ZURÜCK | | | menu also reads Kessel `0xfdb2`, `0x06a5`, `0x06a6`, `0x03e3`, Manager `0x068e`, `0xfdb6` |

### Einstellungen > Kühlen > Kühlmodus

| Line (as displayed) | Example value (2026-11-16 17:58) | Register (node, address, name) | Notes |
|---|---|---|---|
| PASSIVKÜHLUNG | ☑ | Kessel `0x0287` KUEHLMODE = 0 | [registers](.wiki/wiki/ttf07c-registers.md) |
| AKTIVKÜHLUNG | ☐ | Kessel `0x0287` KUEHLMODE = 1 | |
| ZURÜCK | | | |

### Einstellungen > Kühlen > Passivkühlung

Shown with Kühlmodus passiv (photo 2026-11-22). [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-22) | Register (node, address, name) | Notes |
|---|---|---|---|
| FLÄCHENKÜHLUNG > | AUS | Kessel `0x025f` FLAECHENKUEHLUNG | |
| GEBLÄSEKÜHLUNG > | AUS | Kessel `0x025b` GEBLAESEKUEHLUNG | |
| ZURÜCK | | | |

### Einstellungen > Kühlen > Passivkühlung > Gebläsekühlung

Photo 2026-11-22. Same values as Aktivkühlung > Gebläsekühlung, but **no "Dynamik aktiv" line**. The lines below
the switch (Vorlauf/Hysterese/Raum soll) are **shown only while the function is EIN** (owner, 2026-11-22); the same
holds for Flächenkühlung, in both cooling modes. Flächen- and Gebläsekühlung exclude each other.

| Line (as displayed) | Example value (2026-11-22) | Register (node, address, name) | Notes |
|---|---|---|---|
| GEBLÄSEKÜHLUNG > | EIN | Kessel `0x025b` GEBLAESEKUEHLUNG | the on/off switch of the function; set to EIN for the photo and back to AUS |
| VORLAUFSOLLTEMPERATUR > | 15.0 °C | – | |
| HYSTERESE VORLAUFTEMP > | 5.0 K | – | |
| RAUMSOLLTEMPERATUR > | 25.0 °C | – | |
| ZURÜCK | | | |

### Einstellungen > Kühlen > Passivkühlung > Flächenkühlung

Three identical photos 17:44–17:55. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-16 17:44) | Register (node, address, name) | Notes |
|---|---|---|---|
| FLÄCHENKÜHLUNG > | EIN | Kessel `0x025f` FLAECHENKUEHLUNG | excludes Gebläsekühlung |
| VORLAUFSOLLTEMPERATUR > | 17.0 °C | Kessel `0x0260` VORLAUFSOLLTEMP_KUEHLEN | `0x8000` while cooling is off |
| HYSTERESE VORLAUFTEMP > | 1.5 K | Kessel `0x0262` HYSTERESE_VORLAUFTEMP_KUEHLEN | |
| RAUMSOLLTEMPERATUR > | 22.5 °C | Kessel `0x0261` RAUMSOLLTEMP_KUEHLEN | |
| ZURÜCK | | | |

### Einstellungen > Kühlen > Aktivkühlung

| Line (as displayed) | Example value (2026-11-17 20:17) | Register (node, address, name) | Notes |
|---|---|---|---|
| FLÄCHENKÜHLUNG > | AUS | Kessel `0x025f` FLAECHENKUEHLUNG | on/off tests running; EIN on the sub-page at 20:17:54; [registers](.wiki/wiki/ttf07c-registers.md) |
| GEBLÄSEKÜHLUNG > | AUS | Kessel `0x025b` GEBLAESEKUEHLUNG | Manager writes `0x0645` = 1 when the two exclude each other |
| ZURÜCK | | | |

### Einstellungen > Kühlen > Aktivkühlung > Flächenkühlung

| Line (as displayed) | Example value (2026-11-17 20:17) | Register (node, address, name) | Notes |
|---|---|---|---|
| FLÄCHENKÜHLUNG > | EIN | Kessel `0x025f` FLAECHENKUEHLUNG | [registers](.wiki/wiki/ttf07c-registers.md) |
| VORLAUFSOLLTEMPERATUR > | 17.0 °C | – | same value as the Passivkühlung page; read not matched |
| HYSTERESE VORLAUFTEMP > | 1.5 K | – | same |
| RAUMSOLLTEMPERATUR > | 22.5 °C | – | same |
| DYNAMIK AKTIV > | 10 | Kessel `0x0288` (Dynamik aktiv) | |
| ZURÜCK | | | second screen, nothing else (photo 2026-11-22) |

### Einstellungen > Kühlen > Aktivkühlung > Gebläsekühlung

Photo 2026-11-22; two screens. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-22) | Register (node, address, name) | Notes |
|---|---|---|---|
| GEBLÄSEKÜHLUNG > | EIN | Kessel `0x025b` GEBLAESEKUEHLUNG | the list above showed AUS before; excludes Flächenkühlung |
| VORLAUFSOLLTEMPERATUR > | 15.0 °C | – | own values, not those of Flächenkühlung |
| HYSTERESE VORLAUFTEMP > | 5.0 K | – | |
| RAUMSOLLTEMPERATUR > | 25.0 °C | – | |
| DYNAMIK AKTIV > | 10 | Kessel `0x0288` (Dynamik aktiv) (?) | same value as on Flächenkühlung; shared or own register unknown |
| ZURÜCK | | | second screen |

### Inbetriebnahme

Upper part in German (photos 2026-11-22: one before and one after entering the code show the same five lines),
lower part in English (2026-11-17, "MAI < COMMISSIONING").

| Line (as displayed) | Example value (2026-11-22; 2026-11-17 20:26) | Register (node, address, name) | Notes |
|---|---|---|---|
| CODE EINGEBEN > | | panel-local | code 1000, checked by the panel |
| SPRACHE > | DEUTSCH | panel-local | |
| QUELLE > | | | |
| HEIZEN > | | | page below |
| WARMWASSER > | | | = the English [DHW] page |
| VERDICHTER > [COMPRESSOR] | | | German label from photo 2026-11-22 |
| NOTBETRIEB > | AUS | – | not touched |
| RESET > | | | |
| SENSOR ABGLEICH > [SENSOR CALIBRATION] | | | German label from photo 2026-11-22 |
| ZURÜCK | | | Inbetriebnahme menus poll Manager `0x06ae` (0) |

### Inbetriebnahme > Sprache

| Line (as displayed) | Example value (2026-11-17 20:18) | Register (node, address, name) | Notes |
|---|---|---|---|
| DEUTSCH | ☑ | panel-local | language not on the bus (`0x4e8b` stayed 2) |
| ENGLISH | ☐ | panel-local | set 20:20–20:28 for a test |
| FRANCAIS | ☐ | panel-local | |
| NEDERLANDS | ☐ | panel-local | |
| ITALIANO | ☐ | panel-local | |
| SVENSKA, POLSKI, CESKY, MAGYAR, ESPAÑOL | ☐ | panel-local | photo 2026-11-22 |
| SUOMI, DANSK, SLOVENSKO, NORSK, РУССКИЙ | ☐ | panel-local | photo 2026-11-22; РУССКИЙ is the last entry (owner) |

### Inbetriebnahme > Quelle

German photo 2026-11-22 ("HAU / INB < QUELLE"), English 2026-11-17. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-22) | Register (node, address, name) | Notes |
|---|---|---|---|
| QUELLENTEMPERATUR MIN > | -9.0 °C | Kessel `0x01b0` QUELLENTEMP_MIN | matched by read order and value (17:36:48) |
| LEISTUNG SOLEPUMPE > | 65 % | Kessel `0x070c` LEISTUNG_SOLEPUMPE | same |
| QUELLENMEDIUM > | ETHYLEN | Kessel `0xfdae` QUELLENMEDIUM | confirmed by stepping 0–8 |
| ZURÜCK | | | |

### Inbetriebnahme > Quelle > Quellenmedium

Two screens; `0xfdae` value per option. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 20:21) | Register (node, address, name) | Notes |
|---|---|---|---|
| [ETHYLENE GLYCOL] | ☑ | Kessel `0xfdae` = 0 | |
| [POTASSIUM CARBONATE] | ☐ | Kessel `0xfdae` = 1 | |
| [EXTRACT AIR MODULE 0] | ☐ | Kessel `0xfdae` = 2 | |
| [EXTRACT AIR MODULE 30] | ☐ | Kessel `0xfdae` = 3 | |
| [EXTRACT AIR MODULE 60] | ☐ | Kessel `0xfdae` = 4 | |
| [EXTRACT AIR MODULE 120] | ☐ | Kessel `0xfdae` = 5 | |
| [EXTRACT AIR MODULE 180] | ☐ | Kessel `0xfdae` = 6 | |
| [WATER] | ☐ | Kessel `0xfdae` = 7 | |
| [GROUNDWATER MODULE] | ☐ | Kessel `0xfdae` = 8 | |
| ZURÜCK [BACK] | | | |

### Inbetriebnahme > Heizen

Photo 2026-11-22 ("HAU / INB < HEIZEN"). [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-22) | Register (node, address, name) | Notes |
|---|---|---|---|
| REGLERDYNAMIK > | 30 | Kessel `0xfdb0` (Reglerdynamik) | read together with the two below |
| HD SENSOR MAX > | 44.0 bar | Kessel `0x01a2` (HD-Sensor max) | |
| LEISTUNG HEIZKREISPUMPE > | 40 % | Kessel `0x070a` LEISTUNG_HEIZKREISPUMPE | |
| ZURÜCK | | | |

### Inbetriebnahme > Warmwasser

| Line (as displayed) | Example value (2026-11-17 20:22) | Register (node, address, name) | Notes |
|---|---|---|---|
| LEISTUNG WARMWASSERPUM[PE] > | 65 % (2026-11-22) | Kessel `0x070b` LEISTUNG_WARMWASSERPUMPE (likely) | by name and value (read 17:36:52); label cut on the panel; [registers](.wiki/wiki/ttf07c-registers.md) |
| ZURÜCK | | | |

### Inbetriebnahme > Verdichter

[registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 20:22) | Register (node, address, name) | Notes |
|---|---|---|---|
| STILLSTANDSZEIT > | 60 min | Kessel `0xfdb1` VERDICHTER_STILLSTAND (likely) | by value (`0x3C00` = 60); not touched |
| EINPHASIGER BETRIEB > | AUS | Kessel `0x070e` EINPHASIGER_BETRIEB | edit screen showed ON at 20:24 (test), back to OFF |
| SOFORTSTART > | AUS | Manager `0x0669` (Quick start) | 1 = ON; starting shows "PLEASE WAIT / 50 SECONDS" (20:23); error HOCHDRUCK followed at 20:24 |
| ZURÜCK | | | |

### Inbetriebnahme > Notbetrieb

| Line (as displayed) | Example value (2026-11-17 20:25) | Register (node, address, name) | Notes |
|---|---|---|---|
| [EMERGENCY OPERATION] (edit screen) | [OFF] | – | not touched |

### Inbetriebnahme > Reset

German photos 2026-11-17 20:39 and 2026-11-22; same lines in English 20:25.

| Line (as displayed) | Example value (2026-11-17 20:39) | Register (node, address, name) | Notes |
|---|---|---|---|
| WÄRMEPUMPE > | AUS | – | not touched |
| FEHLERLISTE > | AUS | – | not touched |
| SYSTEM > | AUS | – | not touched |
| ZURÜCK | | | |

### Inbetriebnahme > Sensor Abgleich

Offsets in tenths of a degree; 0.1/0.2/0.3 were written by accident at 20:26–20:27 and reset to 0. [registers](.wiki/wiki/ttf07c-registers.md)

| Line (as displayed) | Example value (2026-11-17 20:26) | Register (node, address, name) | Notes |
|---|---|---|---|
| VORLAUFISTTEMPERATUR WP > | 0.0 °C | Manager `0x0658` | German photo 2026-11-22: flow of the heat pump (not "WW") |
| VORLAUFISTTEMPERATUR NHZ > | 0.0 °C | Manager `0x0659` | flow after the backup heater |
| RÜCKLAUFISTTEMPERATUR W[P] > | 0.0 °C | Manager `0x065a` | label cut on the panel |
| ZURÜCK | | | |

## Gaps

Photo request list (panel in Deutsch, one photo per screen including scrolled continuations):

1. Diagnose > Status Anlage during a hot water run (Warmwasserventil bit) and during an EVU block (EVU-Sperre bit).
2. Diagnose > Interne Berechnung while the backup heater runs.
3. HK1 heating pages: with Heizungssteuerung "Wärmepumpe" (no FEK, no emulation): Programme > Heizprogramm and Einstellungen > Heizen > Heizkreis 1 (all lines).

## FEK2 room unit (for comparison)

The FEK has its own menu (rotary wheel, MENU/OK); photos 2026-11-16 12:33–12:39 and 2026-11-17 15:35–15:37, plus
[FEK2 menus](.wiki/raw/2026-11-17-fek2-menus.md). Protocol: [FEK2](.wiki/wiki/fek2.md).

- Boot screen: STIEBEL ELTRON, V416 03 (software 416-03)
- Start screen: weekday, date, analog clock, room 21.7 °C, outdoor 8.8 °C (2026-11-17); page dots (5 on 2026-11-17, 6 on 2026-11-16)
- Info pages: page 4/5 = RAUM MAX 21.7 °C, RAUM MIN 20.6 °C, FEUCHTE MAX 57.0 %, FEUCHTE MIN 49.4 %; other pages not photographed
- HAUPTMENÜ: first entry unreadable (INFO (?)), HEIZPROGRAMM, EINSTELLUNGEN, ZURÜCK
  - HEIZPROGRAMM: day selector (Mo, MONTAG …)
  - EINSTELLUNGEN > HEIZEN: KOMFORT TEMPERATUR 21.0 °C (HK1 `0x0005`, max 30.0), ECO TEMPERATUR 19.9 °C (HK1 `0x0008`, min 5.0), RAUMEINFLUSS 02 (`0x010f`, 0–20), STEIGUNG HEIZKURVE 0.24 (`0x010e`), ANSICHT HEIZKURVE (view), more lines below
  - EINSTELLUNGEN > ALLGEMEIN: SPRACHE DEUTSCH, KONTRAST 05, HELLIGKEIT 50 %, HELLIGKEIT AUS 00 %, RAUMTEMPERATUR KORREKT 0.0 °C, RAUMFEUCHTE KORREKTUR 0.0 %, TOUCH EMPFINDLICHKEIT 04, MIN / MAX LÖSCHEN, WERKSEINSTELLUNG, ZURÜCK

## Sources

- [raw/2026-11-17-fachmann-code.md](.wiki/raw/2026-11-17-fachmann-code.md): code entry, first reads in the expert menus
- [raw/2026-11-17-expert-menus.md](.wiki/raw/2026-11-17-expert-menus.md): Info, Diagnose, Programme page by page
- [raw/2026-11-17-expert-settings.md](.wiki/raw/2026-11-17-expert-settings.md): Einstellungen and Inbetriebnahme
- [raw/2026-11-17-fehlerliste-panel.md](.wiki/raw/2026-11-17-fehlerliste-panel.md): full error list
- [raw/2026-11-17-fek2-menus.md](.wiki/raw/2026-11-17-fek2-menus.md): FEK2 menus
- Register names and addresses: [wiki/ttf07c-registers.md](.wiki/wiki/ttf07c-registers.md)
- The owner's 100 photos (2026-11-16..21) were transcribed for this page, not stored: no photos in the repo by the owner's rule.
