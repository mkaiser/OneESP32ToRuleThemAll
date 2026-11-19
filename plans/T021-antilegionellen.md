# Plan: Antilegionellen run with working backup heater (T021), 2026-11-22 16:00 CET

T021. What is known: [heating control](../doc/ttf07c/.wiki/wiki/heating-control.md), "Antilegionellen run 2026-11-22
(NHZ fuses off)"; setting `0x0101` ([registers](../doc/ttf07c/.wiki/wiki/ttf07c-registers.md)).

**Goal:** see a complete disinfection run: when it starts (fixed 01:00?), the target temperature, how long it takes,
how it ends, and that heating resumes on its own.

**Rules:** the maintainer approved the plan and asked Claude to do every step itself (2026-11-22 14:25), so the
setting and the clock are written by the ESP (`can_send_value`). Also agreed in advance (both are existing,
approved writes): the abort (Programmschalter "Bereitschaft", then back to "Eco") and the clock reset with the HA
button "Synchronize Time" (`syncTime`, the same write the ESP makes every night at 03:00).

## Before (15:45–15:58)

| Who | Step |
|---|---|
| Claude | Start a full CAN capture (all `Communication` lines, one log client, `timeout` inside the container) and the HA state watch every 30 s, until 23:00 |
| Claude | Check: no hot water run, compressor lock-out 0, no error, FEK emulation active, tank temperature noted |
| Owner | NHZ fuses **on** (done 14:25) |
| Owner | Warn the household: the tank may reach 60–65 °C, scalding risk at the taps until it has cooled |

## Start (16:00)

| Who | Step |
|---|---|
| Claude | Antilegionellenbehandlung **EIN**: Kessel `0x0101` = `0x0100` (it is AUS since 05:26) |
| Claude | Clock **00:58:00** like `syncTime`: Kessel `0x0127` = 0, `0x0126` = `0x3A00`, `0x0125` = 0 (date unchanged); check the Manager reports 00:58 |
| Claude | Watch 01:00 panel time (≈ 16:02 CET): Umschaltventil WW, Warmwasserbereitung, compressor, Nachheizstufe |

## During

- Every 10 min: tank temperature, Vorlauf, compressor, Nachheizstufe, error, heating status.
- Expected (first run): compressor to its limit, then NHZ stages 1 → 3 in 2-min steps; tank rises above 49.7 °C.
- **Abort** if: an error, the tank above 70 °C, NHZ running without the tank rising for 30 min, or the run is not
  finished by 20:00. Abort = Programmschalter "Bereitschaft" (ends the run within ~30 s), then "Eco".

## After the run

| Who | Step |
|---|---|
| Claude | Note: end time and how it ended, peak tank temperature, energy (NHZ counters, WW energy), heating resumed? |
| Owner or Claude | Clock back: HA button "Synchronize Time" (or set it on the panel); check the panel clock |
| Owner | Decide: Antilegionellenbehandlung stays EIN (weekly/daily at 01:00?) or AUS; NHZ fuses stay on? |
| Claude | Ingest: capture to `doc/ttf07c/.wiki/raw/captures/2026-11-22-1600-antilegionellen.log`, results to the heating control and registers pages; close T021 |

## Open questions the run answers

- Start: exactly at 01:00 panel time, or relative to when the setting was switched on?
- Target temperature and hold time; does the WPM3i end the run itself (and after how long without reaching it)?
- Which registers change at start and end (`0x0101`, Kessel flags `0x0053`/`0x005E`/`0x0073`, `0xFE1E`, `0x4E5E`).

## Status log

Newest first.

- **2026-11-22 15:47:** deferred by the maintainer before the start (the Eco test took the slot). State: NHZ fuses
  ON, Antilegionellenbehandlung AUS (since 05:26), panel clock untouched. The steps above stand; the writes (setting
  EIN, clock 00:58) were approved for Claude to do. **Next:** pick a new date; Interne Berechnung photo during the run.
