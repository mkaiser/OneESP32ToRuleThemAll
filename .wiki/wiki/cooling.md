# Cooling (Kühlen)

See also: [FEK2](fek2.md), [Betriebsstatus](betriebsstatus.md), [TTF07 C registers](ttf07c-registers.md).

The heat pump is a TTF07 C ("cool"). Cooling has not been tested yet (it was winter when it was ported).

## Known

All cooling settings live on the **Kessel** (`0x180`); the Manager (`0x480`) answers the same addresses with the same
values. The control panel (`0x100`) writes changes directly to the Kessel. Mapped on 2026-11-16 by changing each
value on the panel ([capture](../raw/captures/2026-11-16-1745-kuehlen-menu-mapping.log)).

The cooling registers (Kühlen EIN/AUS `0x06A4`, Kühlmodus `0x0287`, Flächenkühlung `0x025F` with its Vorlauf/Raum
setpoints and Hysterese `0x0260`–`0x0262`, Gebläsekühlung `0x025B`, the unknown menu reads) with their panel paths
and test status are in [TTF07 C registers](ttf07c-registers.md). Kühlbetrieb = bit 13 of `0x4e5e`, confirmed by the
relay test 2026-11-17 ([Betriebsstatus](betriebsstatus.md)).

Firmware (2026-11-16): switches "Kühlen" (`KUEHLEN_EIN`), "Kühlmodus Aktivkühlung" (`KUEHLMODE`), "Flächenkühlung"
(`FLAECHENKUEHLUNG`), "Gebläsekühlung"; numbers "Kühlen Vorlauf Soll Temperatur", "Kühlen Raum Soll Temperatur",
"Kühlen Hysterese" (0.1 steps). Every write is read back after 10 s (`sendData`), and the values are refreshed every 15 min.

`0x0260`–`0x0262` returned `0x8000` until 2026-11-16; since then (Kühlen EIN, Flächenkühlung EIN) they return values.
Probably they answer only while cooling (or Flächenkühlung) is enabled. Not checked: whether they go back to `0x8000`
when Flächenkühlung is AUS (the 15 s AUS phase had no read of them).

**Dropped writes:** twice the Kessel kept the old Hysterese although the panel wrote a new one (17:52:54 1.6 K, 17:55:27
1.4 K; no error frame). A repeated write was accepted. The firmware reads every written value back after 10 s, so HA shows the real value.

## Cooling menu settings (2026-11-15)

The "Kühlen" menu entry on the control panel appears only with a FEK (real or emulated, see [FEK2](fek2.md)).
Its values are **read from the Kessel and the WPM3i, not from the FEK**
([capture](../raw/captures/2026-11-15-2059-emulation-identification-menu.log)). Shown on 2026-11-15: Kühlen
enabled, mode passive (Passivkühlung on, Aktivkühlung off), Flächenkühlung aus, Gebläsekühlung aus.

The panel reads Kessel `0xFDB2`, `0x06A4`, `0x0287`, `0x025F`, `0x025B`, `0x06A5`, `0x06A6`, `0x03E3` and WPM3i
`0x068E`, `0xFDB6` for this menu; values and meanings in [TTF07 C registers](ttf07c-registers.md).

The Kessel and the WPM3i answer these reads **also without a FEK** (only the menu is hidden). The unknown ones are read
every 15 min as diagnostic entities "Kuehlen 0x…".

While a screen is open, the panel polls its pair every ~20 s (`0x06A4` + `0x0287`, `0x025F` + `0x025B`).
A change on the panel is written by the control panel (`0x100`) directly to the Kessel (write, long form) and read back.

## Constraints

- Without the FEK, the WPM blocks cooling. With the FEK, the FEK takes over HK Soll ([FEK2](fek2.md)).
- Whether cooling actually runs with these settings waits for the cooling season (blockers in `TODO.md`).

## Cooling test with the FEK emulation (waits for the season, T003)

The emulation makes the panel's "Kühlen" menu appear; the test runs with the room values from HA. Mind the dew
point: the house humidity sensor read ~65 % where the FEK read ~50 % (2026-11-16).
