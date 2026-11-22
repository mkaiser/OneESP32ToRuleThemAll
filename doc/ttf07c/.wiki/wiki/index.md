# TTF07 C wiki index

Knowledge base for the Tecalor TTF07 C (WPM3i). Schema: [`../AGENTS.md`](../AGENTS.md).
Sources: [`../raw/`](../raw/). Menu tree of the control panel: [control panel](../../control-panel.md).

| Page | Summary |
|---|---|
| [TTF07 C registers](ttf07c-registers.md) | **All CAN registers in one table (source of truth):** address, property, type, node, HA entity, confirmation status |
| [CAN bus](can-bus.md) | Nodes and CAN IDs (`0x100` control panel, `0x601`, `0x680`), message types incl. system messages, frame forms, ID bytes, clock, how to observe and trigger reads |
| [Betriebsstatus](betriebsstatus.md) | Bit layout of the WPM3i status word `0x4e5e`, observed values |
| [Heating control](heating-control.md) | Modes (FEK installiert / Wärmepumpe / FEK Emulation), FEK detection, heating curve, what the emulation sends, pump cycles, Eco, Antilegionellen run |
| [FEK2](fek2.md) | Room unit: registration model, it **is** HK1 and sets the flow setpoint, protocol, emulation |
| [Cooling](cooling.md) | What is known about cooling addresses (mostly `0x8000`), constraints |
| [Errors](errors.md) | Current error number `0x1388`, the error list `0x0B9A`–`0x0BA3`, error codes seen |
| [Device: heatpump-ttf07c](device-heatpump-ttf07c.md) | Hardware, network, configuration, HA entities and Energy dashboard |
| [Writes](writes.md) | Every write the firmware makes to the heat pump and who approved it; one-off writes on request |
| [Screenshots](screenshots.md) | How the dashboard and device page screenshots in `doc/ttf07c/images/` are made and retaken |
