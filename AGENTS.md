# AGENTS.md

The rules for this fork of [kr0ner/OneESP32ToRuleThemAll](https://github.com/kr0ner/OneESP32ToRuleThemAll), and
where everything else is. The rules here outrank every other document, the wiki included. Each rule is written down
once; everywhere else links to it.

Upstream is ESPHome firmware for Stiebel Eltron / Tecalor heat pumps over CAN. This fork adds the **Tecalor TTF07 C
(cool) with WPM3i manager** and runs on one device, `heatpump-ttf07c`, in the maintainer's Home Assistant. Work
happens on `ttf07-port`: upstream `master` plus a stack of topic commits that goes upstream as is.

## Where everything is

| What | Where |
| --- | --- |
| **Everything about the TTF07 C (source of truth)**: heat pump, CAN bus, registers, control panel, raw captures | `doc/ttf07c/` (start at `doc/ttf07c/README.md`) |
| Two llmwiki workspaces: the root wiki (all heat pumps) and the TTF07 C wiki, each with index and log | `.wiki/wiki/index.md` and `doc/ttf07c/.wiki/wiki/index.md`; schema and ingest rules `.wiki/AGENTS.md` (+ `doc/ttf07c/.wiki/AGENTS.md`) |
| Every CAN register (source of truth) | `doc/ttf07c/.wiki/wiki/ttf07c-registers.md`, kept in step with `components/wp_core/property.h` |
| Branches, build, flash, logs, CAN captures, environment pitfalls, the commit stack | `dev/development.md` |
| What is next, open decisions, planned tests, what waits on the season, the upstream release | `TODO.md` |
| How work is written down and how agents share one tree: `TODO.md`, `plans/`, `T###` numbers, commits, closing a session (project-independent; this file's "Workflow in this project" fills it in) | `workflow.md` |
| Plans of running work, each with its status log, named by the `T###` they serve | `plans/` (`T002-T009-upstream.md`: the upstream PRs; `T001-register-decoding.md`: unknown registers; `T007-T008-analytics.md`) |
| Ready-to-paste upstream PR texts | `upstream/issue-text.md` |
| Recurring procedures: verify a sensor on the CAN bus, TODO housekeeping, closing a session | `.claude/skills/` (`test-sensor`, `todo-housekeeping`, `close-session`) |
| Tools: config compare, CAN capture, dashboard export and screenshots | `.claude/tools/` |
| C++ core: CAN nodes, communication, properties, types | `components/wp_core/` |
| Climates (upstream's `heating`/`hot_water` plus `preset`) | `components/wp_climate/` |
| Shared yaml base, entity templates | `yaml/core.yaml`, `yaml/templates/` |
| **The TTF07 C / WPM3i device file**, a variant on `yaml/ttf07_base.yaml` (shared with upstream's `yaml/ttf07.yaml`) | `yaml/ttf07_wpm3i.yaml` |
| Optional packages: German names, debug sensors for unidentified registers | `yaml/names/ttf07_wpm3i_de.yaml`, `yaml/ttf07_wpm3i_debug.yaml` |
| User guide for TTF07 C owners (upstream-ready: no wiki/TODO references); example dashboard | `doc/ttf07c.md`, `doc/ttf07c/dashboard-example/ttf07_wpm3i_dashboard.yaml` |
| The device configuration (outside this repo; this repo is its submodule) | `/homeassistant/esphome/heatpump-ttf07c.yaml` |

## Commands

```bash
C=$(docker ps --format '{{.Names}}' | grep -m1 '_esphome$')
docker exec $C esphome config  /config/esphome/heatpump-ttf07c.yaml   # the gate for any yaml or C++ change
docker exec $C esphome compile /config/esphome/heatpump-ttf07c.yaml
```
Flashing, logs and checks after a flash: `dev/development.md`. A docs-only change has no gate beyond links that
resolve.

## The rules

Each line below is the whole rule; the page beside it is the evidence and the how. Read that page before changing
code that relies on it.

**Hard constraints.** Broken, each of these changes somebody's heating, history or the upstream series, usually
without a failing build.

| In one line | Page |
| --- | --- |
| **The heat pump is live.** Write to it (numbers, switches, selects, `can_send_value`, write frames) only when the maintainer asked for that specific change; read requests are fine. A new automatic write needs the maintainer's approval first | [writes](doc/ttf07c/.wiki/wiki/writes.md) |
| **"Heizungssteuerung" writes to the heat pump**: change the selection only on the maintainer's request | [heating control](doc/ttf07c/.wiki/wiki/heating-control.md) |
| **HA history is keyed by the entity `name`**: never rename an entity; template entities are named by id like upstream, readable names only in the German names package (same change); never change the scale of a `total_increasing` sensor, add a new one | [entity names](.wiki/wiki/entity-names.md) |
| **Shared code stays upstream compatible**: `components/`, `yaml/core.yaml`, `yaml/templates/` keep upstream behaviour by default (new parameters default to the old behaviour); TTF07 C specifics go into `TTF_07_C` sections and `yaml/ttf07_wpm3i.yaml` | `plans/T002-T009-upstream.md` |
| **Never push to upstream; never `git push` without asking the maintainer first**, every time; commit only the paths you changed | `workflow.md` |
| **No attribution trailers**: no `Co-Authored-By:` or other agent/tool lines in commit messages, also when a tool suggests them. The author is the maintainer | `dev/development.md` |
| **Flashing reboots the ESP**: say when you do it, and check the result | `dev/development.md` |

**Verified on the heat pump.**

| In one line | Page |
| --- | --- |
| On a TTF07 C with WPM3i, upstream's `CanNode::Manager` is the WPM3i at `0x480` | [CAN bus](doc/ttf07c/.wiki/wiki/can-bus.md) |
| The FEK emulation never starts while a real FEK is detected; after a flash or reboot HK1 stays reserved for up to ~8 min, the compressor keeps running | [heating control](doc/ttf07c/.wiki/wiki/heating-control.md) |
| Writing `0x0B9A` only makes the WPM3i send its error list | [errors](doc/ttf07c/.wiki/wiki/errors.md) |
| `0x8000` is no value, `0x9000` is "AUS", `0xFE70` is no sensor | [registers](doc/ttf07c/.wiki/wiki/ttf07c-registers.md) |

**In the code and the tree.**

| In one line | Where |
| --- | --- |
| A register is named only once identified: until then a `wp_debug` sensor by `address:` in `yaml/ttf07_wpm3i_debug.yaml`, never in `property.h`; on identification, property + entity + German name + registers page in one change | [registers](doc/ttf07c/.wiki/wiki/ttf07c-registers.md) |
| `property.h` addresses are lowercase hex, so `PROPERTY()`'s compile-time uniqueness check catches duplicates | [registers](doc/ttf07c/.wiki/wiki/ttf07c-registers.md) |
| Upstream style: subjects like upstream's history, `git clang-format` on changed lines, no wiki/TODO references, dates or "maintainer" in code and yaml comments; new work goes into its topic commit | `dev/development.md` |
| Times are CET (`Europe/Berlin`) in the wiki, logs, `TODO.md` and replies; another zone is converted or marked (`12:00 UTC`) | `.wiki/AGENTS.md` |
| The login shell is zsh (`${VAR}`, not `$VAR:…`); host tools are BusyBox; `docker cp`, not bind mounts | `dev/development.md` |

## Do not hand-edit

- `doc/ttf07c/dashboard-example/ttf07_wpm3i_dashboard.yaml`: exported from the live dashboard by
  `.claude/tools/dashboard/export_dashboard.py`;
- `doc/ttf07c/images/`: taken by `.claude/tools/dashboard/take_screenshots.py`.

Both are redone after a change that adds, renames or removes entities (`dev/development.md`).

## Workflow in this project

`workflow.md` is the same in every project; this section is its detail here, and outranks it.

- **TODO file:** `TODO.md` (workflow.md's `Todo.md`), revised with `/todo-housekeeping`; sessions end with
  `/close-session`. Its first section is **Incoming items by maintainer**.
- **Extra sections:** **Planned tests** (runs on the heat pump, removed once run and ingested) between Open decisions
  and Blockers; **Release** is the upstream PR series (`plans/T002-T009-upstream.md`). Next steps, Blockers and Future
  work are grouped by area: Heat pump, Cooling, Firmware, Home Assistant, Analytics, Energy management.
- **Gate:** fast `esphome config`, full `esphome compile` (~10 min, give it a 20 min timeout), both under "Commands";
  docs-only: links resolve.
- **Generated files:** "Do not hand-edit" above. No gate catches a hand edit there; the tools redo them.
- **A decision about the code:** `.wiki/wiki/firmware-history.md`, or `plans/T002-T009-upstream.md` for the series,
  plus a `decision` entry in `.wiki/wiki/log.md` (the TTF07 C wiki keeps no history: TTF07 C decisions go to their page).
- **A measured or external fact:** its page in the wiki of its scope (TTF07 C: `doc/ttf07c/.wiki/wiki/`; all heat
  pumps: `.wiki/wiki/`), cited (root wiki: plus a `log.md` entry; the TTF07 C wiki keeps no log).
- **A trap in the development loop:** `dev/development.md`.

## The wiki

Two llmwiki workspaces hold this fork's knowledge: the TTF07 C wiki `doc/ttf07c/.wiki/` (the heat pump, its CAN bus
and registers: the source of truth for the TTF07 C) and the root wiki `.wiki/` (all heat pumps). Before working on a
register or a heat pump question, read `doc/ttf07c/.wiki/wiki/index.md` and the pages it points to. **Ingest is part
of the work**: a test, capture or finding updates its pages and the index in the same change (and the root `log.md` for root wiki findings). The rest is
`.wiki/AGENTS.md` and `doc/ttf07c/.wiki/AGENTS.md`.
