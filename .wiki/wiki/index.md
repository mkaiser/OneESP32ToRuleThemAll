# Wiki index

Knowledge base for the Tecalor TTF07 C (WPM3i) and this firmware fork. How the wiki is maintained: [`../AGENTS.md`](../AGENTS.md). Chronology: [log](log.md). Sources: [`../raw/`](../raw/).

| Page | Summary |
|---|---|
| [CAN bus](can-bus.md) | Nodes and CAN IDs (`0x100` control panel, `0x601`, `0x680`), message types incl. system messages, short/long frame form, ID bytes, clock, how to observe and trigger reads |
| [TTF07 C registers](ttf07c-registers.md) | **All CAN registers in one table (source of truth):** address, property, type, node, HA entity, confirmation status (test, panel, analysis, plausible, no value, open), naming vs upstream |
| [Betriebsstatus](betriebsstatus.md) | Bit layout of the WPM3i status word `0x4e5e`, observed values |
| [Cooling](cooling.md) | What is known about cooling addresses (mostly `0x8000`), constraints |
| [FEK2](fek2.md) | Room unit: registration model, it **is** HK1 and sets the flow setpoint while registered, full protocol (raw), "Kühlen" menu needs it, emulation by the ESP and its status |
| [Heating control](heating-control.md) | Modes (FEK installiert / Wärmepumpe / FEK Emulation), FEK detection by software version, the WPM3i heating curve (fitted), what the emulation sends, the passed emulation test (2026-11-16) |
| [Device: heatpump-ttf07c](device-heatpump-ttf07c.md) | Hardware, network, configuration, HA entities and Energy dashboard |
| [Errors](errors.md) | Current error number `0x1388` (21 = Keine Leistung), the error list `0x0B9A`–`0x0BA3` and the error codes seen |
| [Firmware history](firmware-history.md) | Old implementation, port to upstream, decisions and what changed |
| [Screenshots](screenshots.md) | How the dashboard and device page screenshots in `docs/images/ttf07c/` (used by the user guide `docs/ttf07c.md`) are made (Playwright in a container, temporary user) and how to retake them |
| [Writes](writes.md) | Every write the firmware makes to the heat pump (error list request, Warmwasserprogramm, FEK emulation, HA entities) and who approved it |
| [Entity names](entity-names.md) | HA identity comes from the entity `name`; naming by id like upstream, German names package, statistics scale |
