# Text for my old issue thread

Hey,

the 'ttf07 cool submarine engineer' is back. With some time and Claude's help I made big progress ([my branch](https://github.com/mkaiser/OneESP32ToRuleThemAll/tree/ttf07-port)):
- [FEK emulation](https://github.com/mkaiser/OneESP32ToRuleThemAll/blob/749f69f/yaml/ttf07_wpm3i.yaml#L573-L600) fully working
- Turns out my pump has a WPM3i controller (not WPM2): [ttf07_wpm3i.yaml](https://github.com/mkaiser/OneESP32ToRuleThemAll/blob/ttf07-port/yaml/ttf07_wpm3i.yaml)
- [Thermostats](https://github.com/mkaiser/OneESP32ToRuleThemAll/blob/749f69f/yaml/ttf07_wpm3i.yaml#L1303-L1337) for heating and hot water with some eco/komf/heating time window quirks (new [`preset` type](https://github.com/mkaiser/OneESP32ToRuleThemAll/commit/75ac683) in wp_climate)
- Many more registers decoded: [property.h](https://github.com/mkaiser/OneESP32ToRuleThemAll/commit/c3e7001), [register notes](https://github.com/mkaiser/OneESP32ToRuleThemAll/blob/ttf07-port/.wiki/wiki/ttf07c-registers.md)
- New Can member [Control panel (Bedienteil) writes](https://github.com/mkaiser/OneESP32ToRuleThemAll/commit/428f323) now show up immediately
- [Detailed CAN logging](https://github.com/mkaiser/OneESP32ToRuleThemAll/commit/cc0ffdd) (sender, node, type, raw bytes)
- New templates: [`wp_power`, `wp_debug`](https://github.com/mkaiser/OneESP32ToRuleThemAll/commit/8c58daa); [number `write_lock`/`mode`](https://github.com/mkaiser/OneESP32ToRuleThemAll/commit/86ef1be)
- [`ttf07_base.yaml`](https://github.com/mkaiser/OneESP32ToRuleThemAll/commit/b240a2e) shared by both TTF07 variants (no change for `ttf07.yaml` users)
- PoC for supporting German/English entity names: [`yaml/names/ttf07_wpm3i_de.yaml`](https://github.com/mkaiser/OneESP32ToRuleThemAll/blob/ttf07-port/yaml/names/ttf07_wpm3i_de.yaml)

I had Claude adapt your style and prepare 3 PRs: shared improvements → ttf07_base → TTF07 C/WPM3i.
Before that, some questions:
- I organized my reverse engineering using Claude + LLMwiki. In [`.wiki/wiki`](https://github.com/mkaiser/OneESP32ToRuleThemAll/tree/ttf07-port/.wiki/wiki) there is much knowledge which was written down by testing at the heatpumps panel, reading the bus and writing findings down. I will keep this in my repo. Do you maybe want to adopt this mechanism? 
- Should I add a `docs/` folder? I have a [TTF07 C user guide](https://github.com/mkaiser/OneESP32ToRuleThemAll/blob/ttf07-port/docs/ttf07c.md) plus a [dashboard](https://github.com/mkaiser/OneESP32ToRuleThemAll/blob/ttf07-port/yaml/examples/ttf07_wpm3i_dashboard.yaml) and screenshots.
- How do you want to handle namings? e.g. I named my entites not by the register property names, but directly with the names I want to see in Home Assistant. Also what about translation to english? 

Will work on this and test more for at least one week. Then I would update and finalize the PRs for you [prelimiary PR text](https://github.com/mkaiser/OneESP32ToRuleThemAll/blob/ttf07-port/upstream/issue-text.md)


# Upstream PR texts (fork only)

Ready to paste. Open from `mkaiser:ttf07-port` against `kr0ner:master`. Order: PR 1 → PR 2a (independent) → PR 2b.

---

## PR 1

**Title:** Shared improvements for the TTF07 C with WPM3i (logging, templates, preset climate)

Groundwork for TTF07 C (cool) with WPM3i support (PR 2b). No device-specific code; defaults keep today's behaviour.

**Commits**
- **Add detailed CAN message logging** – sender, addressed node, message type, raw bytes per frame; `sendData` logged.
  ⚠️ "Message received" moves INFO → DEBUG; dropped requests at VERBOSE.
- **Add CanNode Bedienteil and apply control panel writes at once** – panel writes (e.g. `0x100`) update the
  addressed node's entity immediately. Only active if a device file sets the node; `core.yaml` doesn't.
- **Analytics: publish under the entity id** – templates register the id as analytics name. Same as today for all
  device files; lets a device rename entities (`!extend`) and still publish under the common names.
- **Templates: number mode and write lock, device class for wp_generic_combined** – optional:
  - `wp_number` `mode` (auto/slider/box)
  - `wp_number` `write_lock` (C++ expression; refuses writes, reads back)
  - `wp_generic_combined` `device_class` (e.g. energy)
- **Templates: add wp_power and wp_debug**
  - `wp_power`: current × voltage, recalculated on input change
  - `wp_debug`: diagnostic sensor by raw address (no `property.h` entry), optional `type`; listen-only by default
- **wp_climate: add preset thermostat type** – `type: preset`: thermostat from existing entities (Komfort/Eco
  numbers, preset select, current temp/humidity sensors, action binary sensor). Optional setpoint sensor,
  alternative select/numbers, `writable` lambda. `heating`/`hot_water` unchanged.
- **txx_base: configurable VORLAUFISTTEMP target and HK1 settings write lock** – substitutions
  `vorlaufisttemp_target` (default `HK1`), `hk1_settings_write_lock` (default `false`).

**Tested**
- `esp32-poe-technik.yaml` + `thz504.yaml` (CI target): compiles (commits 1–7 on `ae1d414`).
- Whole series on a TTF07 C with WPM3i, running since 2026-11.

---

## PR 2a

**Title:** Introduce ttf07_base.yaml as the shared base for TTF07 variants

Same pattern as `wxx_base.yaml` (b7a9c1a). Prepares a second TTF07 variant (TTF07 C with WPM3i, PR 2b).
Independent of PR 1.

**Changes**
- `ttf07_base.yaml`: `txx_base.yaml` + what every TTF07 has (status binary sensors, temperatures, pressures,
  `EINPHASIGER_BETRIEB`).
- `ttf07.yaml`: variant on it; keeps Kessel status decoding (`0x0a20`), pump power, `VERDICHTER_STILLSTAND`,
  `REGLERDYNAMIK`, `KUEHLEN_EINGESCHALTET`, Programmschalter.
- New substitution `druck_kaeltekreis_scaler` (default `1.0`).
- README hierarchy: `txx_base → ttf07_base → ttf07`.

**No change for `ttf07.yaml` users**
- `esphome config` before/after: same 61 entities (name, domain, unit, state class, device class, icon, interval).
- Only difference: boot lambdas split over two files.
- `esp32-poe-technik.yaml` + `ttf07.yaml`: compiles, cherry-picked alone onto `ae1d414`.

---

## PR 2b

Not before PR 1 is merged. Base: `docs/ttf07c.md`. Ask first whether a `docs/` folder is wanted (else drop commit 12,
upload screenshots into the PR).
