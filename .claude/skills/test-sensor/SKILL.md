---
name: test-sensor
description: Verify a heat pump sensor/parameter of the TTF07 C (OneESP32ToRuleThemAll ESPHome firmware, device heatpump-ttf07c) by recording the live CAN data stream while the user changes the value on the heat pump control panel, then analyzing which CAN frames/addresses changed. Use when the user says "test sensor <x>", "teste Sensor <x>", "check the CAN data for <parameter>", "I change <x> on the heat pump, watch the CAN bus", or similar.
---

# Test a heat pump sensor via the CAN data stream

The user names a sensor/parameter (`$ARGUMENTS`, e.g. "WW Eco Temperatur", `KOMF_TEMP`, `0x0008`, or a control panel
parameter that is not in the firmware yet). They change it on the heat pump; you record the CAN stream and confirm
what happened on the bus.

**Read-only.** Never send write frames, never use the `can_send_value` action, never change heat pump settings, never
reflash, unless the user explicitly asks for that specific action. Read requests (step 3) are allowed.

## Environment

| What | Value |
|---|---|
| ESPHome add-on container | `docker ps --format '{{.Names}}' \| grep -m1 '_esphome$'` (was `app_5c53de3b_esphome`) |
| Device config (in container) | `/config/esphome/heatpump-ttf07c.yaml` (host: `/homeassistant/esphome/heatpump-ttf07c.yaml`) |
| Device address | `192.168.178.37` (if unreachable, try `heatpump-ttf07c.local`) |
| Firmware source | `/homeassistant/esphome/OneESP32ToRuleThemAll` (branch `ttf07-port`) |
| Properties | `components/wp_core/property.h` (TTF07 C: sections with `TTF_07_C`, plus common section 1) |
| Entities | `yaml/ttf07_wpm3i.yaml` (`sensor_name` = HA display name, `property`, `target` node) |
| HA API | `curl -H "Authorization: Bearer $SUPERVISOR_TOKEN" http://supervisor/core/api/...` |
| Analysis script | `.claude/skills/test-sensor/scripts/analyze_can.py` in the firmware repo (`~/.claude/skills/test-sensor` links there) |
| Knowledge | `.wiki/wiki/` in the firmware repo: read `index.md`, `can-bus.md`, `ttf07c-registers.md` first |
| Scratch files | the session scratchpad directory |

CAN nodes: Kessel `0x180`, HK1 `0x301`, Manager/WPM3i `0x480`, MFG `0x700`, Bedienteil `0x100` (most likely the
control panel: settings changed on the panel probably show up as writes from `0x100`), ESPClient (the ESP) `0x680`,
`0x601` (FEK2?). Details and message types: `doc/ttf07c/.wiki/wiki/can-bus.md`.

The firmware logs every CAN frame (needs the detailed CAN logging, commit `516ea7c` or later on `ttf07-port`):
```
[15:05:09.122][D][Communication:235]: Message from 0x180 (Kessel) Read/Write ID 0xD2 0x00 (to 0x680/ESPClient) property QUELLENTEMP_MIN (0x01B0) raw value 65446 (0xFFA6)
[16:25:18.914][V][Communication:229]: Request (dropped) from 0x100 (unknown) Read/Write ID 0x31 0x00 (to 0x180/Kessel) property RUECKLAUFISTTEMP (0x0016) raw value 0 (0x0000)
```
Timestamps are the log clock (local time). Raw `0x8000` (32768) means "no value / not available".
The message type is the low nibble of the first ID byte (0 write, 1 read, 2 response, 6 system, 7 system response);
the script decodes it, and lists all senders with their first/last frame.
All received messages are logged (no property filter); unknown addresses show as `UNKNOWN`.

## Workflow

### 1. Resolve the sensor
- Search `property.h` and `ttf07_wpm3i.yaml` for the name, display name or address: property name, address, type,
  target node, HA display name.
- Get the current HA state of the entity via the HA API (match on `friendly_name`, which is prefixed with "Wärmepumpe ").
- If it is not in the firmware, say so; the test then relies on change detection only (step 5).
- Keep this short; don't block on it.

### 2. Start the recording
Run it with `run_in_background` (default 10 minutes, or what the user asks for):
```bash
C=$(docker ps --format '{{.Names}}' | grep -m1 '_esphome$')
F=<scratchpad>/capture-<name>-$(date +%H%M%S).log
docker exec $C timeout 600 esphome logs --device 192.168.178.37 /config/esphome/heatpump-ttf07c.yaml > $F 2>&1
```
- Only one recording at a time.
- Within ~15 s, check that `$F` contains `Communication` lines. If not, check the device/firmware before telling
  the user to start.

### 3. Baseline snapshot (if the property is known)
Request the property once, so the baseline contains a fresh value. Use the HA action `can_send_raw_data`, which may
only be used for **read** requests: `[readId_hi, readId_lo, 0xfa, addr_hi, addr_lo, 0, 0]` as decimal ints.

| Target | readId bytes |
|---|---|
| Kessel `0x180` | `49, 0` (0x31 0x00) |
| HK1 `0x301` | `97, 1` (0x61 0x01) |
| Manager `0x480` | `145, 0` (0x91 0x00) |
| MFG `0x700` | `225, 0` (0xE1 0x00) |

(readId = `((canId & 0x7c0) << 5) + (canId & 0x3f) | 0x100`)
```bash
curl -s -X POST -H "Authorization: Bearer $SUPERVISOR_TOKEN" -H "Content-Type: application/json" \
  http://supervisor/core/api/services/esphome/heatpump_ttf07c_can_send_raw_data -d '{"data":[49,0,250,1,176,0,0]}'
```
The response appears in the log within a fraction of a second.

### 4. Hand over to the user
Tell them briefly:
- the recording runs until HH:MM (log clock) and the current value is …
- now change `<x>` on the control panel; wait ~30 s after this message first, so there is a baseline
- afterwards, tell me old → new value and roughly when

Then end the turn and wait for their reply.

### 5. Analyze
After the user's reply:
- If the change happened less than ~30 s ago, request the property once more (step 3) so the new value is on the bus.
- Run the script on the (still growing) file:
```bash
python3 ~/.claude/skills/test-sensor/scripts/analyze_can.py $F --property <NAME or 0xADDR> --entity "<display name>" --changed-at HH:MM:SS
```
- `--changed-at` is the change time on the log clock. If the user gives none, use a time shortly before their
  reply, taken from the log timestamps at that point.
- Look at:
  - **target property lines** (value before/after, who sent it)
  - **NEW writes between nodes** (e.g. Manager → Kessel right after the change: that is usually the real address)
  - **NEW value changes**, especially `[UNKNOWN property]` addresses
- Compare the decodings with the value the user set: dec/10, cent/100, int, low byte, little endian, bool. This gives
  the correct `Type::et_*` (`et_dec_val`, `et_cent_val`, `et_default`, `et_byte`, `et_little_endian`, `et_bool`).
- If nothing shows up: the WPM may keep the value internally. Request the property from the other nodes
  (Kessel/HK1/Manager/MFG), or wait for the next poll and analyze again.

### 6. Report
Give the verdict first:
- **confirmed:** address, node and type match, and the entity showed the new value
- **partly:** seen on the bus, but wrong type/scaling/node, or the entity didn't update
- **not seen**

Then give the evidence (the relevant frames with times), the decoding, and a concrete fix if needed: the
`property.h` line and/or the `ttf07_wpm3i.yaml` entry. Don't edit firmware files or flash without asking.

Then file the result (firmware repo, see `.wiki/AGENTS.md` and `workflow.md`):
- **Ingest:** copy the relevant capture lines (the `Communication` and `>>` lines around the change) to
  `doc/ttf07c/.wiki/raw/captures/YYYY-MM-DD-HHMM-<parameter>.log`. Update every affected wiki page (usually
  `ttf07c-registers.md`, plus `can-bus.md`, `cooling.md`, … as needed) and `index.md` if you add a page. The TTF07 C
  wiki keeps no log: the verdict goes to the registers page, the test details to the commit message.
- **TODO.md:** use the `todo-housekeeping` skill. Remove a planned test that was run, and add new open questions or fixes
  as items.
- Don't commit unless the user asks.

If the recording is no longer needed and is still running, it ends by itself through `timeout`.
