# Expert menus, page by page: CAN traffic, 2026-11-17 17:38–18:18

Continuation of [2026-11-17-fachmann-code.md](2026-11-17-fachmann-code.md). The maintainer browsed the expert menus
(code 1000) page by page and sent a photo of each page; an agent matched the panel's reads (`0x100`) at that time.
Passive capture by the ESP, nothing written by the ESP. The panel itself wrote only in the relay test.
Panel frames: [capture](captures/2026-11-17-1738-expert-menus-panel-traffic.txt) (`time src>dst kind addr name value`).
Coverage: **all pages of the Info and Diagnose menus** (maintainer, 17:59) and the Einstellungen menu **Programme**
(18:03–18:18); the other Einstellungen menus are not browsed yet.
Values are raw unless stated; `0x8000` = no value, `0x9000` = "AUS" on the display.

## Info > Anlage > Raumtemperatur (17:39:31)
- Manager 0x4E64 = 212 -> Isttemperatur FEK 21.2 °C
- Manager 0x4E66 = 220 -> Solltemperatur FEK 22.0 °C (emulation Komfort 22.0)
- Manager 0x069E = 525 -> Raumfeuchte 52.5 % (upstream name VERDICHTERDREHZAHL, other models)
- Kessel 0x0264 = 111 -> Taupunkttemperatur 11.1 °C (upstream TAUPUNKT_HK1)
- Manager 0x4E63, 0x4E65 = 0x8000 (not shown; HK2 counterparts?)
## Info > Anlage > Heizung (17:40:41-17:41:01), 3 photos
- Aussentemperatur 10.0 = Kessel 0x000C; Isttemperatur HK1 25.4 = Kessel 0x02CA; Solltemperatur HK1 25.5 = Kessel 0x01D5 (same value as Puffersoll)
- Vorlaufisttemperatur WP 26.2 = Kessel 0x06A1; Vorlaufisttemperatur NHZ 27.3 = Kessel 0x06A0 (new)
- Ruecklaufisttemperatur 26.1 = 0x0016; Festwertsolltemperatur AUS = Kessel 0x01C0 (TBD_17) = 0x9000
- Pufferist 25.4 = 0x0078; Puffersoll 25.5 = 0x01D5; Heizungsdruck 1.34 bar = 0x0674; Volumenstrom 0.00 l/min = 0x0673; Anlagenfrost 4.0 = 0x0A00
- not shown: Kessel 0x068F (TBD_18) = 1, Kessel 0x06A2 = 0x8000, 0x602 0x000F = 0x8000 (HK2?)
## Info > Anlage > Warmwasser (17:43:45)
- Isttemperatur 42.8 = Kessel 0x000E; Solltemperatur 45.0 = Kessel 0x0003; Volumenstrom 0.00 l/min (no extra read: 0x0673 cached or same)
## Info > Anlage > Elektrische Nacherwärmung (17:44:06), read order = display order
- Bivalenztemperatur HZG -19.0 = Kessel 0x01AC (0xFF42); Einsatzgrenze HZG AUS = Kessel 0x01AE (0x9000)
- Bivalenztemperatur WW -19.0 = Kessel 0x01AD (0xFF42); Einsatzgrenze WW AUS = Kessel 0x01AF (0x9000)
## Quelle (17:45:25): Quelle Ist 0x01D4, Quellentemp min 0x01B0 (-9.0), Quellendruck 0x0675 (2.06 bar) - known
## Kältekreis (17:45:45): Heissgas 0x0265 (34.9), Hochdruck 0x0268 (15.6 bar), Niederdruck 0x07A5 (10.3 bar) - known
## Info > Wärmemenge (17:46:33-17:47:00), 2 photos
- VD Heizen Tag 58.027 kWh, VD Heizen Summe 76.982 MWh, VD WW Tag 0.213 kWh, VD WW Summe 15.349 MWh (known WAERMEERTRAG_* addresses)
- NHZ Heizen Summe 6.688 MWh = Kessel 0x0929 (MWh part, 6) + 0x0927 (kWh part, 0x02B0 = 688); 0x0928 = 0 (upstream calls 0x0928 the kWh part: wrong here, would give 6.000)
- NHZ Warmwasser Summe 0.538 MWh = Kessel 0x0925 (MWh, 0) + 0x0923 (kWh, 538); 0x0924 = 0
- So on the TTF07 C the NHZ sums use kWh at 0x0923/0x0927 (upstream: 2WE_*_TAG_KWH), MWh at 0x0925/0x0929.
## Info > Wärmemenge > Laufzeit (17:48:11), photo
- VD Heizen 7601 h = 0x07FC; VD Warmwasser 1344 h = 0x0802; NHZ 1 15 h = 0x0259; NHZ 2 13 h = 0x025A; NHZ 1/2 997 h = 0x0805 (panel label "NHZ 1/2": upstream name LAUFZEIT_NHZ1_2 confirmed)
- VD Kühlen 0x07FF read (0x8000) but not shown on the page
## Info > Wärmemenge > Leistungsaufnahme (17:47:18): known EL_ENERGIEAUFNAHME_* 0x091A-0x0921, values = HA
## Diagnose > Status Anlage (17:49:25), 2 photos
- Lines: Pufferladepumpe, Warmwasserventil, Heizkreispumpe, Mischerpumpe, Mischer auf, Mischer zu, Quellenpumpe, Kühlbetrieb, EVU-Sperre; all off; 0x4E5E = 0 at that time. No per-line reads: the page shows the 0x4E5E bits (bit 9 likely Warmwasserventil, not Entleerung HYD; EVU-Sperre bit unknown). Confirm with a photo while the pumps run.
- Reads when entering Diagnose: Manager 0x068E = 20, 0x0691 = 0, 0x0692 = 0, 0x0074 = 1 (meaning open)
## Diagnose > Status Wärmepumpe (17:51:30), photo
- Reststillstand 38 min = Manager 0x0668 (minutes, counts down: 53 at 17:37:09, 39 at 17:51:30, 38 at 17:51:35); compressor stopped ~17:30, VERDICHTER_STILLSTAND 0xFDB1 = 0x3C00 = 60 min -> ends ~18:30
- Verdichter, NHZ 1, NHZ 2 checkboxes: off (from status words, no extra read)
## Diagnose > System (17:52:25): menu Busteilnehmer / Wärmepumpentyp; read Manager 0x0294 = 63 on entering (meaning open)
## Diagnose > System > Busteilnehmer (17:53:01), photo
- 01 WPM3i 391-10 (!! the controller is a WPM3i, not WPM2), 02 FES 417-07 (the control panel itself), 03 FEK 416-03, 04 MFG 18
- Reads: Manager 0x4E69 = 18 (= MFG software), Manager 0x4E68 = 2 (not shown; MFG revision/count?), HK1 0x301 FET_SOFTWARE 0x0199 and FET_SOFTWARESTAND 0x019A: answered by the ESP's FEK emulation (416, 3) -> the panel lists the emulation as "FEK 416-03"
- WPM3i and FES versions: no bus read (panel-local / cached)
## Diagnose > System > Wärmepumpentyp (~17:53:30), photo: "TTF MFG"
- No read on this page; 0x4E68 = 2 (read with Busteilnehmer, not shown there) is the likely type code. Back in System: 0x0294 = 63 read again.
## Diagnose > Interne Berechnung (~17:54:30), photo: Zeitintervall 00, Eingeschaltete Stufen 00
- No read of its own after 17:54:30; the Diagnose-menu reads 0x0691 = 0 and 0x0692 = 0 are the likely sources (NHZ stage calculation: interval, stages on); 0x068E = 20 still open. Confirm while the NHZ runs.
## Diagnose > Relaistest Anlage (17:55:55-17:58:16), photos. PANEL WRITES to Kessel:
- 0x0693 = 1 on entering the relay test, = 0 on leaving (17:58:16) -> relay test active flag
- 0x067A (TBD_16, read gives no answer) = number of the relay switched on (only one at a time; rewritten ~every minute):
  1 Pufferladepumpe (0x0A20 bit 6, 0x4E5E bit 7) | 2 Warmwasserventil (0x0A20 bits 6+4) | 3 Heizkreispumpe (0x0A20 bit 5, 0x4E5E bit 0)
  4 Mischerpumpe (0x4E5E bit 1) | 5 Mischer auf (0x4E5E bit 2) | 6 Mischer zu (0x4E5E bit 3)
  7 NHZ 1 (0x0A20 bit 0, 0x4E5E 0x0090) | 8 NHZ 2 (0x0A20 bit 1, 0x4E5E 0x00A0) | 12 NHZ 3 (0x0A20 bits 0+1, 0x4E5E 0x00B0)
  9 Quellenpumpe (0x0A20 bit 8, 0x4E5E bit 6) | 10 Kühlbetrieb (0x0A20 bit 9, 0x4E5E bit 13) | 11 Entleerung HYD (0x4E5E bit 9, ~7 s)
- NHZ relays each only ~2-8 s, without flow; NHZ flow temperature unchanged (25.7 -> 25.4 °C). After leaving: 0x0A20 = 0, 0x4E5E = 0.
- This confirms 0x4E5E bits 1, 2, 3 (Mischer), 9 (Entleerung HYD) and 13 (Kühlbetrieb), and 0x0A20 bit 9 (Kühlbetrieb).

# Einstellungen pass: menu Programme (18:03–18:18)

Panel frames: [capture](captures/2026-11-17-1803-programme-panel-traffic.txt). Only the menu **Programme** was
browsed; the other Einstellungen menus are still open. Writes in this part: the maintainer changed values on the
panel on purpose (time windows, Aufheizprogramm, Partyprogramm) and the ESP wrote time windows on the maintainer's
go; everything was set back (see below).
## Programme (18:03:41), photo: Heizprogramm >, Warmwasserprogramm >, Partyprogramm 0 h, Ferienprogramm >, Aufheizprogramm AUS
- Reads in display order: Manager 0xFDBF = 0 -> Partyprogramm 0 h (likely), Kessel 0x011A = 0 -> Aufheizprogramm AUS (likely)
- Manager 0x068E = 20 read again on entering the main menu (18:03:22)
## Programme > Warmwasserprogramm (18:04:13; first reported as Heizprogramm, it was the Warmwasserprogramm): empty. Reads Kessel 0x1710, 0x1711, 0x1712 = 0x8080 each
- likely the 3 time windows of the first day/group (one byte start, one byte end in 15-min steps, 0x80 = not set)
- Test by the maintainer: Monday window 06:00-08:00 -> panel wrote Kessel 0x1710 = 0x1820 (18:04:59): high byte = start, low byte = end, in 15-min steps (0x18 = 24 = 06:00, 0x20 = 32 = 08:00). 0x1710 = Monday window 1 (0x1711/0x1712 = windows 2/3 likely).
- Deleted at 18:05:17: panel wrote 0x0000 (not 0x8080 as before); ESP read 18:05:27 = 0x0000.
- Layout test (maintainer's go, 18:08): the ESP wrote Mo-Fr window 1 = 0x1710/0x1720/0x1730/0x1740/0x1750 = 01-02, 02-03, 03-04, 04-05, 05-06 h; the maintainer confirmed all 5 days on the panel. Program: one day per 0x10, Mo 0x1710 ... So 0x1770, 3 windows each (x0..x2), x3..xF = 0x8000. Panel shows 0x0000 as 00:00-00:00 = whole day, 0x8080 as --:--.
- Restored 18:09:33: 0x1710-0x1750 = 0x8080 (the state before the test; Monday was 0x8080 before the maintainer's panel test).
- Other blocks with 0x8080 (second program?): 0x1700-0x170F, 0x1780-0x180F, 0x1880-0x18AF; 0x1810-0x1870 = 0x8000.
- Program = **Warmwasserprogramm** (maintainer 18:11). Panel writes: Saturday 00:15-00:30 -> 0x1760 = 0x0102 (18:10:54); Sunday 01:00-01:15 -> 0x1770.
- Day group Mo-Fr (18:12, photo): panel wrote only the group block 0x1780 = 0x0204 (00:30-01:00), 0x1781 = 0x0406 (01:00-01:30), 0x1782 = 0x0709 (01:45-02:15); the WPM3i copied the group into the single days (ESP read 18:12:24: 0x1710, 0x1720, 0x1750 = 0x0204), Sa/So unchanged. Other blocks 0x1790.. 0x1800 = probably Sa-So, Mo-So, and the Heizprogramm.
- Groups confirmed on the panel (photos): 0x1780 = Mo-Fr, 0x1790 = Sa-So, 0x17A0 = Mo-So (a group read returns its first day's windows).
- Cleanup test (maintainer's go, 18:15): the ESP wrote only the Mo-So group 0x17A0-0x17A2 = 0x8080; the WPM3i copied it into all 7 days and the Mo-Fr and Sa-So groups (read back: 0x1710-0x17A2 all 0x8080). The Warmwasserprogramm is empty again, as before the tests.
## Programme > Heizprogramm (18:16, photo): only "Zurück" - hidden while a FEK (here the emulation) owns HK1, like the HK1 settings. Blocks 0x1700-0x170F and 0x17B0-0x180F / 0x1880-0x18AF (all 0x8080) are candidates for the heating programs (HK1/HK2), not verified.
## Programme > Ferienprogramm (18:15:29-18:16:31), photo: Ferienbeginn 24.06.24, Ferienende 16.07.24 (confirmed)
- Manager 0x011B/0x011C/0x011D = start day/month/year (24, 6, 24), 0x011E/0x011F/0x0120 = end day/month/year (16, 7, 24); value in the high byte (0x1800 = 24)
## Programme > Aufheizprogramm (18:17, photo). Maintainer switched it ON on purpose at 18:17:04 (panel write Kessel 0x011A = 0x0100; 0 = AUS)
- Aufheizprogramm EIN/AUS = Kessel 0x011A (0x0100 = EIN, 0 = AUS) -> confirms Programme page line
- Sockeltemperatur 40.0 °C = Kessel 0x01BB (400); Dauer Sockel 2 Tage = 0x01BC (2); Maximal Temperatur 45.0 °C = 0x01BD (450); Dauer Maximaltemperatur 5 Tage = 0x01BE (5); 0x01BA = 10 read first (line further down? e.g. Anstieg K/Tag)
- Steigung pro Tag 10 K = Kessel 0x01BA (10) (photo)
## Programme > Partyprogramm (18:17:53, photo "3 h"): maintainer set 3 h -> panel wrote Manager 0xFDBF = 0x0300 (hours in the high byte). Confirms Partyprogramm = 0xFDBF.
- End state 18:18: Warmwasserprogramm empty everywhere (panel confirmed), Aufheizprogramm AUS, Partyprogramm 0 h, Programmschalter Eco.
