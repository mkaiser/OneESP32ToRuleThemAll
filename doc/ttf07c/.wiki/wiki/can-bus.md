# CAN bus (TTF07 C with WPM3i)

How the heat pump's nodes talk, and how the ESP takes part. See also: [TTF07 C registers](ttf07c-registers.md),
[Betriebsstatus](betriebsstatus.md), [Device](device-heatpump-ttf07c.md).

> **The manager is a WPM3i**, not a WPM2 as assumed until 2026-11-17 (panel "Diagnose > System > Busteilnehmer", 2026-11-17): 01 WPM3i
> 391-10, 02 FES 417-07 (the control panel `0x100`), 03 FEK 416-03 (the ESP's emulation answered the panel's
> software read on `0x301`), 04 MFG 18 (Manager `0x4E69`). The fork was renamed on 2026-11-17 (`ttf07_wpm3i.yaml`, docs);
> the entity "Software WPM2" became "Software WPM3i" on 2026-11-18 (new entity). Wärmepumpentyp: "TTF MFG" (likely Manager `0x4E68` = 2).
> [raw](../raw/2026-11-17-expert-menus.md)

## Bus

- 20 kbit/s, standard (11-bit) IDs.
- The ESP sends with CAN ID `0x680` (`espclient_can_id`). Upstream's default is `0x6a2`; on this heat pump `0x680`
  "just works" (old notes, [raw](../raw/2026-11-15-old-ttf07-yaml-notes.md)).

## Nodes

| CAN ID | Firmware node | What it is | Evidence |
|---|---|---|---|
| `0x180` | `Kessel` | Heat pump controller: temperatures, pressures, energy, settings | answers reads, 2026-11-15 |
| `0x301` | `HK1` | Heating circuit 1: Komfort/Eco temperature, Steigung, Raumeinfluss, Vorlauf Soll. Without a FEK the WPM3i answers for it; **a registered FEK takes over `0x301`** (sends with this ID, answers with its own parameters) | [FEK2](fek2.md) |
| `0x302` | `HK2` | Heating circuit 2: unused on this installation | — |
| `0x602` | (none) | Answers the panel's read of `0x000F` (HK flow temperature) with `0x8000`: probably the HK2 counterpart of `0x601` (2026-11-17) | [raw](../raw/2026-11-17-expert-menus.md) |
| `0x514` | (none) | Answers the panel's read of `0xC32F` with `0x8000` in the expert menus (2026-11-17); not a listed bus participant, so an internal function of the WPM3i | [raw](../raw/2026-11-17-fachmann-code.md) |
| `0x480` | `Manager` | **WPM3i** (heat pump manager): Betriebsstatus `0x4e5e`, Programmschalter | answers reads; writes to MFG every ~10 s |
| `0x700` | `MFG` | Power/inverter board: supply voltage, current, Vorlauf NHZ | answers reads from WPM3i and ESP |
| `0x601` | (none) | **Not the FEK.** Exists without it (7-min system message to `0x301`). Receives the FEK's room values and parameters and configures the FEK: probably the WPM3i's room control logic for HK1 | [FEK2](fek2.md) Sends a configuration block to HK1 about every 7 min (`0x0010`, `0x000F`, `0x0004`, `0x0052`, `0x0056`, `0x0057`, `0x0028`, `0x005A`) and `0x0052` (= compressor/heating flag) at once when it changes, 2026-11-16 ([raw](../raw/2026-11-16-0x601-config-block-and-0x0052.md)) |
| `0x100` | `Bedienteil` | **The control panel/display** (confirmed 2026-11-16: WW Komfort changed on the panel was written by `0x100` to the Kessel, `30 00 13 02 12` = 53.0 °C, [capture](../raw/captures/2026-11-16-0954-fek-emulation-flow-setpoint.log)): reads Rücklauf, Außen, Speicher Ist from the Kessel every ~11 s; gets the minute from the WPM3i every 60 s; sends `TBD_09` = 1 to the WPM3i every 60 s (keep-alive) | [capture](../raw/captures/2026-11-15-1704-system-messages.log) |
| `0x680` | `ESPClient` | This ESP. **Another device seems to use `0x680` too**: type 6 frames with `0x00FD` = `0x0800` at full minutes (17:12:00, 17:20:00) that the ESP did not send | [capture](../raw/captures/2026-11-15-1704-system-messages.log) |

`0x100` was configured as "Manager" in the old firmware; debug sensors (now "Debug Bedienteil 0x06AF/0x4E8B") listen there
(via the node `Bedienteil`, added 2026-11-15). Since 2026-11-16, its writes to another node update that node's entity at
once (e.g. WW Komfort → Kessel).
Upstream also defines `FET` (`0x402`) and `Heizmodul` (`0x6a1`); they are not seen on this bus.
The CAN IDs can be changed at runtime with the "<node> CAN ID" text entities in HA.

## Node activity in HA (since 2026-11-16)

Diagnostic sensors "CAN <node> Frames" (frames **per hour** per sender CAN ID, unit `1/h`, since 2026-11-17: sum of
the last 60 minutes, updated every minute; unknown for 10 min after boot, extrapolated to one hour until 60 min of
data exist; 0 = the node is silent. Until 2026-11-16 it was frames per minute, `1/min`) for `0x180`, `0x301`, `0x480`, `0x700`, `0x100`, `0x601`, `0x680`, plus "CAN unbekannt Frames" (sum of all
other senders) and the text sensor "CAN unbekannte Sender" (unknown IDs with the time last seen, since boot; also
logged as `CAN nodes`). When a known node was last seen follows from the HA history of its rate. The ESP does not
receive its own frames: while it emulates the FEK, "HK1 0x301" counts only other senders' frames with that ID (the
WPM3i's presence check). Typical per-minute rates (2026-11-16 19:58, compressor off, emulation on): Manager 105, MFG 99,
Kessel 28, Bedienteil 17, `0x680` 1, HK1 1, `0x601` 0 (it sends only every ~7 min), unknown 0. Per hour: see
2026-11-17. Dashboard: Diagnose,
section CAN IDs.

## Frame format

7 data bytes, in two forms:
- **long:** `[id0, id1, 0xfa, addr_hi, addr_lo, value_hi, value_lo]`, for any address.
- **short:** `[id0, id1, addr, value_hi, value_lo, 0, 0]`, for addresses below `0x100`.

Who uses which: the WPM3i answers long-form reads in long form (the ESP always uses the long form). System messages
(types 6/7) are always short form. The FEK uses the short form for addresses below `0x100`, and the long form above
(e.g. RAUMEINFLUSS `0x010F`). The log shows the raw bytes at the end of each line (`data …`, since 2026-11-15).

The first two bytes encode the addressed node and the message type:
- addressed node = `((b0 & 0xf0) << 3) | (b1 & 0x7f)`
- message type = `b0 & 0x0f`

| Type | Meaning | Seen |
|---|---|---|
| 0 | write | WPM3i → MFG every ~10 s; WPM3i → Bedienteil (minute); Bedienteil → WPM3i (keep-alive) |
| 1 | read | all regular polling |
| 2 | response | answers to reads |
| 6 | system | every 7 min on `0x00FE` (value `0x0100`): `0x601` → HK1, then Kessel → `0x379`, WPM3i → `0x579` and `0x179`. Every 8 min (full minutes) on `0x00FD` (value `0x0800`): `0x301` → `0x301`, then `0x680` → `0x680`. FEK plug-in: `0x301` `0x00FD` = `0x0900` |
| 7 | system response | Bedienteil → WPM3i on `0x00FE` |

Upstream's code uses write ID = `((canId & 0x7c0) << 5) + (canId & 0x3f)`, read = `| 0x100`, response = `| 0x200`.
That is the same for types 0–2 but misreads types 4–7 (the log decodes them correctly since 2026-11-15).
The targets `0x379`, `0x579`, `0x179` (low part `0x79`) look like broadcast addresses.

| Node | Write to it | Read from it | Response addressed to it |
|---|---|---|---|
| Kessel `0x180` | `0x30 0x00` | `0x31 0x00` | `0x32 0x00` |
| HK1 `0x301` | `0x60 0x01` | `0x61 0x01` | `0x62 0x01` |
| Manager `0x480` | `0x90 0x00` | `0x91 0x00` | `0x92 0x00` |
| MFG `0x700` | `0xE0 0x00` | `0xE1 0x00` | `0xE2 0x00` |
| ESPClient `0x680` | `0xD0 0x00` | `0xD1 0x00` | `0xD2 0x00` |

The ID bytes always name the **addressed** node: a read to the Kessel carries `0x31 0x00`, and the Kessel's answer
to the ESP carries `0xD2 0x00`. The sender is the frame's CAN ID. Both values match the 2026-11-15 captures
(e.g. WPM3i → MFG write `0xE0 0x00`, MFG → WPM3i response `0x92 0x00`).

Raw value `0x8000` (32768) means "no value / not available". Value types (`et_dec_val` = signed /10,
`et_cent_val` = /100, `et_little_endian` = byte-swapped, …) are defined in `components/wp_core/type.h`.

## Observing the bus

The firmware logs every frame in one line (commit "core: detailed CAN message logging"):
```
Message from 0x180 (Kessel) Read/Write ID 0xD2 0x00 (to 0x680/ESPClient) property QUELLENTEMP_MIN (0x01B0) raw value 65446 (0xFFA6)
Request (dropped) from 0x100 (unknown) Read/Write ID 0x31 0x00 (to 0x180/Kessel) property RUECKLAUFISTTEMP (0x0016) raw value 0 (0x0000)
```
Responses and writes are logged at DEBUG, reads at VERBOSE (all properties, no filter since 2026-11-18).

To trigger a read yourself, use the HA action `esphome.heatpump_ttf07c_can_send_raw_data` with the read bytes, e.g.
`[49, 0, 250, 1, 176, 0, 0]` for QUELLENTEMP_MIN from the Kessel. The answer arrives in ~25 ms
([capture](../raw/captures/2026-11-15-1627-read-request-test.log)).
The `test-sensor` skill automates recording and analysis.

## Clock

`0x0009` on the Kessel holds the time: low byte = hour, high byte = minute (e.g. `0x2213` = 19:34). The FEK reads it
every ~66 s. The WPM3i writes MINUTE (`0x0126`) to the control panel every 60 s.

## Regular traffic (heating off, 2026-11-15)

- WPM3i → MFG writes, every ~10–20 s: `TBD_06` (`0xfe1d`) = 0, `TBD_02` (`0xfe1c`) = 100, `TBD_08` (`0xfe1b`) = 100,
  `TBD_07` (`0xfe1e`) = 0.
- WPM3i reads `TBD_04` (`0xfe4c`) from the MFG every 5 s (value 18).
- `0x100` reads RUECKLAUFISTTEMP and AUSSENTEMP from the Kessel every ~11 s.

## Kessel block to `0x379` (2026-11-17)

The Kessel writes a block to CAN ID `0x379` about every 3.5 min (nobody answers): `0x0009` = time of day (high
byte minute, low byte hour: `0x0B0D` = 13:11), `0x000A` = 4363, `0x0010` = 81,
`0x0053` = 0, `0x005A` = `0x0200`, `0x005E` = 0, `0x0073` = 0, `ANLAGENFROST` `0x0A00` = 4.0 °C, the storage, return
and outdoor temperatures, and `BETRIEBS_STATUS` `0x0A20` on every change (see [Betriebsstatus](betriebsstatus.md)).
Meaning of `0x379` and the unknown values open ([excerpt](../raw/captures/2026-11-17-0815-passive-0052-status-words.log)).
2026-11-18 12:12: `0x000A` = `0x120B` (2026-11-17: `0x110B`), so `0x000A` is probably the **date** (high byte day,
low byte month; unconfirmed until the next day change); the block came every ~2.5 min
([capture](../raw/captures/2026-11-18-1207-passive-10min.log)).


## WPM3i boot: node scan (2026-11-17)

After a power cycle of the heat pump (13:31) the nodes announce themselves with system `0x00FD` = `0x0900` on their
own ID: `0x100` (13:31:15), `0x480`, `0x180`, `0x601`, **`0x602`** (13:31:17). Then `0x00FD` = `0x0800` (the
presence check, as every 8 min) goes out on `0x301` (HK1/FEK; the emulation answered and registered at once),
`0x680`, **`0x302`** (HK2, i.e. a second FEK), **`0x528`** and **`0x546`**. The new IDs appear once and are listed by
"CAN unbekannte Sender". `0x602` is probably the HK2 counterpart of `0x601` (room control logic, unconfirmed);
`0x528`/`0x546` unknown (optional modules?). The error number `0x1388` was 0 again after the restart.
[capture](../raw/captures/2026-11-17-1331-wpm2-power-cycle.log)
