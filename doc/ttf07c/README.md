# Tecalor TTF07 C (WPM3i): source of truth

Everything known about the TTF07 C with WPM3i manager lives here; other documents link to it and do not repeat it.
The knowledge base is an [llmwiki](https://github.com/microsoft/llmwiki) workspace in [`.wiki/`](.wiki/): schema
[`.wiki/AGENTS.md`](.wiki/AGENTS.md), index [`.wiki/wiki/index.md`](.wiki/wiki/index.md). The user guide for owners is [`../ttf07c.md`](../ttf07c.md).

| Path | Content |
|---|---|
| [`.wiki/wiki/`](.wiki/wiki/) | Pages: registers (source of truth, in step with `components/wp_core/property.h`), CAN bus, Betriebsstatus, heating control, FEK2, cooling, errors, device, writes, screenshots |
| [`.wiki/raw/`](.wiki/raw/) | Immutable sources: notes and CAN captures (`raw/captures/`); no photos |
| [`control-panel.md`](control-panel.md) | Control panel menu tree: every page and line with its register (source of truth for the panel) |
| [`dashboard-example/`](dashboard-example/ttf07_wpm3i_dashboard.yaml) | Home Assistant dashboard for this firmware, exported from a live installation (made by `.claude/tools/dashboard/export_dashboard.py`; do not hand-edit) |
| [`images/`](images/) | Dashboard and device page screenshots used by the user guide (made by `.claude/tools/dashboard/take_screenshots.py`; do not hand-edit) |

