# Entity names and Home Assistant identity

Why entity names in this firmware must not change, and how names are chosen. Rule: [`AGENTS.md`](../../AGENTS.md).

## Identity comes from the name

ESPHome derives the HA unique ID (and so the entity ID) from the entity's `name`. Renaming an entity in the
firmware or in the names package creates a new entity; the old one's history is lost (finding 2026-11-18).
Renaming the **entity ID** in the HA registry keeps the history: a naming scheme for HA is applied there, not in the
firmware.

## How entities are named

- Entities from templates are named by their id, like upstream (e.g. `HKISTTEMP`; energy/COP ids as in
  `txx_base.yaml`), so upstream users switching from `ttf07.yaml` keep their history.
- Human readable names only in the optional package `yaml/names/ttf07_wpm3i_de.yaml` (`!extend`); the maintainer's
  device includes it. A new template entity gets its German name there in the same change.
- Entities defined directly in the device file keep readable names.

## Statistics

For `total_increasing` energy sensors never change the value scale of an existing entity: HA's long-term statistics
would mix both scales. Add a new entity instead.

## HA 2026.11 naming scheme (open, T017)

The HA config renamed all other devices along HA's naming model (no area in device names, main entities without
own name, IDs `area_device_entity`; `plans/naming.md` in the HA config). The heat pump ("Wärmepumpe", `heatpump_*`,
~140 entities, 109 references in `lovelace.dashboard_warmepumpe`) was left out on purpose. If adopted, it is done in
the HA registry (e.g. `button.hwr_warmepumpe_synchronize_time`), together with the dashboard, the example dashboard
and the docs.
