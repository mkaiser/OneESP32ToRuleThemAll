# Betriebsstatus (operating status word)

See also: [CAN bus](can-bus.md), [TTF07 C registers](ttf07c-registers.md), [Cooling](cooling.md).

On the TTF07 C with WPM3i, the useful status word is **`BETRIEBS_STATUS_WPM` = `0x4e5e` from the WPM3i**
(`CanNode::Manager`, `0x480`). It is read every 30 s and decoded in `yaml/ttf07_wpm3i.yaml`. The raw bits are
published as the diagnostic text sensor `DEBUG_BETRIEB` (bit 15 on the left).

Upstream's `yaml/ttf07.yaml` reads `BETRIEBS_STATUS` `0x0a20` from the Kessel instead, with a different bit layout
(bit 0/1 NHZ, 3 Verdichter, 4 Warmwasser, 5 Heizkreispumpe, 6 Pufferladepumpe, 8 Quellenpumpe, 9 Kühlbetrieb).
Comparison on this heat pump (passive capture from 2026-11-17 08:15): the Kessel sends `0x0A20` on its own to
`0x379` on every change (and answers reads); the WPM3i sends `0x4e5e` to the control panel (`0x100`) on every change.
Heating-circuit pump runs without compressor at 08:30, 08:51, 09:13 (5 min each): `0x0A20` = `0x0020` (upstream bit 5
Heizkreispumpe) exactly when `0x4e5e` = `0x0001` (bit 0 Heizkreispumpe). Compressor start 09:22–09:23 (heating):

| Time | `0x0A20` (Kessel) | upstream meaning | `0x4e5e` (WPM3i) |
|---|---|---|---|
| 09:22:41 | `0x0120` = bits 8, 5 | Quellenpumpe, Heizkreispumpe | `0x0040` → `0x0041` = bits 6, 0 (Quellenpumpe, Heizkreispumpe) |
| 09:23:11 | `0x016C` = bits 8, 6, 5, 3, 2 | + Pufferladepumpe, Verdichter, bit 2 (unknown upstream) | `0x4041` = + bit 14 (Verdichter); bit 7 (Pufferladepumpe) by 09:23:32 |

So far upstream's layout matches on this heat pump for bits 3, 5, 6, 8; bit 2 comes on with the compressor (meaning
open). Compressor stop 10:37:40: `0x0A20` `0x016C` → `0x006C` → `0x0020` (Quellenpumpe, Verdichter, bit 2 off at the same
time), `0x4e5e` `0x40C1` → `0x00C1` → `0x0041`, source pump off 10:38:39 (`0x0001`). Bit 2 follows the compressor
(on and off). NHZ (bits 0/1) seen in the Notbetrieb tests 2026-11-17: `0x0041`/`0x0042`/`0x0043` (bit 0, bit 1,
bits 0+1, plus bit 6) exactly with `0x4e5e` `0x0090`/`0x00A0`/`0x00B0` (stages 1/2/3), the Kessel a few seconds later
([capture](../raw/captures/2026-11-17-1143-notbetrieb-nhz-stages.log),
[capture](../raw/captures/2026-11-17-1348-nhz-stage-powers.log)), so upstream's NHZ1/2/3 decoding fits. Hot water
(bit 4) not seen in normal operation yet (the relay test set it with the Warmwasserventil).

## Bits of `0x4e5e`

| Bit | Mask | Meaning | Status |
|---|---|---|---|
| 0 | `0x0001` | Heizkreispumpe | seen on while heating |
| 1 | `0x0002` | Mischer Pumpe (Mischer aktiv) | **confirmed** (relay test 2026-11-17) |
| 2 | `0x0004` | Mischer auf | **confirmed** (relay test) |
| 3 | `0x0008` | Mischer zu | **confirmed** (relay test) |
| 4, 5, 7 | | NHZ **stages**: bit 7 with 4 = stage 1, 3 kW (`0x0090`), 7 with 5 = stage 2, 6 kW (`0x00A0`), 7 with 4 and 5 = stage 3, 9 kW (`0x00B0`); firmware "Nachheizregister 1/2/3" | **confirmed 2026-11-17** (Notbetrieb tests, power measured per stage) |
| 6 | `0x0040` | Quellenpumpe | seen on while heating |
| 7 | `0x0080` | Pufferladepumpe; with bit 9 = Warmwasserbereitung (`0x0280`) | seen on while heating |
| 9 | `0x0200` | Entleerung HYD | on with relay test 11 "Entleerung HYD" (2026-11-17); also on during hot water charging, so probably the same output as the hot water valve (relay 2 was not polled in `0x4e5e`) |
| 13 | `0x2000` | Kühlbetrieb | **confirmed** (relay test 10 "Kühlbetrieb", 2026-11-17) |
| 14 | `0x4000` | Verdichter | seen on while heating |

Derived in the firmware:
- **Heizbetrieb** = bit 7 and not bit 9 and not bit 13
- **Warmwasserbereitung** = bits 7 and 9

## Relay test (Diagnose > Relaistest Anlage), 2026-11-17

The panel (`0x100`) writes to the Kessel `0x0693` = 1 when the relay test is opened and 0 when it is left, and
`0x067A` (`TBD_16`) = number of the one relay switched on (only one at a time). Both status words follow at once:

| `0x067A` | Relay | `0x0A20` (Kessel) | `0x4e5e` (WPM3i) |
|---|---|---|---|
| 1 | Pufferladepumpe | bit 6 | bit 7 |
| 2 | Warmwasserventil | bits 6 + 4 | not polled |
| 3 | Heizkreispumpe | bit 5 | bit 0 |
| 4 / 5 / 6 | Mischerpumpe / Mischer auf / Mischer zu | – | bit 1 / 2 / 3 |
| 7 / 8 / 12 | NHZ 1 / 2 / 3 | bit 0 / bit 1 / bits 0 + 1 | `0x0090` / `0x00A0` / `0x00B0` |
| 9 | Quellenpumpe | bit 8 | bit 6 |
| 10 | Kühlbetrieb | bit 9 | bit 13 |
| 11 | Entleerung HYD | – | bit 9 |

The NHZ relays were on for 2–8 s each without flow (NHZ flow temperature unchanged). "Diagnose > Status Anlage" and
"Status Wärmepumpe" show these bits as check boxes (no reads of their own).
[raw](../raw/2026-11-17-expert-menus.md)

## Observed values

| Date | Raw | Bits set | Situation |
|---|---|---|---|
| 2026-11-15 13:42 local | `0100000011000001` | 14, 7, 6, 0 | heating: Verdichter, Pufferladepumpe, Quellenpumpe, Heizkreispumpe |
| 2026-11-15 15:30 local | `0000000000000000` | none | compressor off, pumps off |

## NHZ test in Notbetrieb, 2026-11-17

Programmschalter Notbetrieb (11:43:32) plus a heat demand (emulation flow setpoint 32 °C, 11:59) made the WPM3i step
up the backup heater, about every 2 min ([capture](../raw/captures/2026-11-17-1143-notbetrieb-nhz-stages.log)):

| Time | `0x0A20` (Kessel) | `0x4e5e` (WPM3i) | Stage |
|---|---|---|---|
| 12:01:06 | `0x0041` (bits 6, 0) | `0x0090` | NHZ1 |
| 12:03:04 | `0x0042` (bits 6, 1) | `0x00A0` | NHZ2 |
| 12:05:03 | `0x0043` (bits 6, 1, 0) | `0x00B0` | NHZ1 + NHZ2 |
| 12:17:57 | `0x0000` | `0x0000` | demand met (buffer 33.4 °C > 32 °C) |

Upstream's `0x0A20` layout is right on this heat pump for NHZ too: bit 0 = NHZ1, bit 1 = NHZ2, both = upstream's
"NHZ3". In Notbetrieb `0x0A20` bit 6 (Pufferladepumpe) is on without `0x4e5e` bit 7 being the hot-water flag.

The heater fuses were off until ~12:14: the WPM3i stepped up anyway and raised **no error** (FEHLERMELDUNG 0, no
fault frame); it does not notice missing heater power. With the fuses on, NHZ1 + NHZ2 drew **~8.95 kW** (house load
490 → 9440 W, about +1.75 kW grid per phase, the battery covered the rest); fuse 1 off took **3.0 kW from phase A
only**: probably three ~3 kW elements, one per phase. The MFG's `STROMAUFNAHME` stayed at 3.7 A, so it is not the
heater current. Stage powers (second run 13:48–13:59, all fuses on, [capture](../raw/captures/2026-11-17-1348-nhz-stage-powers.log)):
three ~2.95 kW elements, one per phase, switched as **stages**: stage 1 (`0x0090`, `0x0A20` bit 0) = phase A, 2.96 kW;
stage 2 (`0x00A0`, bit 1) = phases A + B, 5.9 kW; stage 3 (`0x00B0`, bits 0 + 1) = A + B + C, 8.9 kW. So the bits
encode the stage number in binary (bit 4 = 1, bit 5 = 2), not two separate heaters; "NHZ3" (upstream and firmware)
= stage 3 = all three elements. Steps every 2 min while the demand lasts; at 35 °C buffer it switched off from
stage 3 directly. The run-time counters `LAUFZEIT_NHZ1`, `LAUFZEIT_NHZ2`, `LAUFZEIT_NHZ1_2` are then probably hours per
stage (unconfirmed).

## Compressor start without power, 2026-11-17

Compressor fuses off (owner), Eco, heat demand from the emulation: source pump 13:10:06 (`0x4e5e` `0x0040`),
compressor on 13:10:36 (`0x0A20` `0x016C`, `0x4e5e` `0x4041`, `0x0052` `0x0100`), and **exactly 60 s later**
(13:11:36) compressor and heat demand off in both words, the WPM3i sends error number 21 (`0x1388`) to the panel, which
shows "Fehler / Keine Leistung". No NHZ fallback (its fuses were off too). Source pump off 13:12:34.
[capture](../raw/captures/2026-11-17-1310-verdichter-keine-leistung.log)
