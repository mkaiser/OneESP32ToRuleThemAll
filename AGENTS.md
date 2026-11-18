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
| What we know about the heat pump, the CAN bus and this firmware | the wiki: start at `.wiki/wiki/index.md`; its schema and ingest rules are `.wiki/AGENTS.md` |
| Every CAN register (source of truth) | `.wiki/wiki/ttf07c-registers.md`, kept in step with `components/wp_core/property.h` |
| Branches, build, flash, logs, CAN captures, environment pitfalls, the commit stack | `dev/development.md` |
| What is next, open decisions, planned tests, what waits on the season | `TODO.md` |
| How work is written down and how agents share one tree: `TODO.md`, `plans/`, `T###` numbers, commits | `workflow.md` |
| Plans of running work, each with its status log | `plans/` (`upstream.md`: the upstream PRs; `register-decoding.md`: unknown registers) |
| Ready-to-paste upstream PR texts | `upstream/issue-text.md` |
| Recurring procedures: verify a sensor on the CAN bus, TODO housekeeping | `.claude/skills/` (`test-sensor`, `todo-housekeeping`) |
| Tools: config compare, CAN capture, dashboard export and screenshots | `.claude/tools/` |
| C++ core: CAN nodes, communication, properties, types | `components/wp_core/` |
| Climates (upstream's `heating`/`hot_water` plus `preset`) | `components/wp_climate/` |
| Shared yaml base, entity templates | `yaml/core.yaml`, `yaml/templates/` |
| **The TTF07 C / WPM3i device file**, a variant on `yaml/ttf07_base.yaml` (shared with upstream's `yaml/ttf07.yaml`) | `yaml/ttf07_wpm3i.yaml` |
| Optional packages: German names, debug sensors for unidentified registers | `yaml/names/ttf07_wpm3i_de.yaml`, `yaml/ttf07_wpm3i_debug.yaml` |
| User guide for TTF07 C owners (upstream-ready: no wiki/TODO references); example dashboard | `docs/ttf07c.md`, `yaml/examples/ttf07_wpm3i_dashboard.yaml` |
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
| **The heat pump is live.** Write to it (numbers, switches, selects, `can_send_value`, write frames) only when the maintainer asked for that specific change; read requests are fine. A new automatic write needs the maintainer's approval first | [writes](.wiki/wiki/writes.md) |
| **"Heizungssteuerung" writes to the heat pump**: change the selection only on the maintainer's request | [heating control](.wiki/wiki/heating-control.md) |
| **HA history is keyed by the entity `name`**: never rename an entity; template entities are named by id like upstream, readable names only in the German names package (same change); never change the scale of a `total_increasing` sensor, add a new one | [entity names](.wiki/wiki/entity-names.md) |
| **Shared code stays upstream compatible**: `components/`, `yaml/core.yaml`, `yaml/templates/` keep upstream behaviour by default (new parameters default to the old behaviour); TTF07 C specifics go into `TTF_07_C` sections and `yaml/ttf07_wpm3i.yaml` | `plans/upstream.md` |
| **Never push to upstream; never `git push` without asking the maintainer first**, every time; commit only the paths you changed | `workflow.md` |
| **No attribution trailers**: no `Co-Authored-By:` or other agent/tool lines in commit messages, also when a tool suggests them. The author is the maintainer | `dev/development.md` |
| **Flashing reboots the ESP**: say when you do it, and check the result | `dev/development.md` |

**Verified on the heat pump.**

| In one line | Page |
| --- | --- |
| On a TTF07 C with WPM3i, upstream's `CanNode::Manager` is the WPM3i at `0x480` | [CAN bus](.wiki/wiki/can-bus.md) |
| The FEK emulation never starts while a real FEK is detected; after a flash or reboot HK1 stays reserved for up to ~8 min, the compressor keeps running | [heating control](.wiki/wiki/heating-control.md) |
| Writing `0x0B9A` only makes the WPM3i send its error list | [errors](.wiki/wiki/errors.md) |
| `0x8000` is no value, `0x9000` is "AUS", `0xFE70` is no sensor | [registers](.wiki/wiki/ttf07c-registers.md) |

**In the code and the tree.**

| In one line | Where |
| --- | --- |
| A register is named only once identified: until then a `wp_debug` sensor by `address:` in `yaml/ttf07_wpm3i_debug.yaml`, never in `property.h`; on identification, property + entity + German name + registers page in one change | [registers](.wiki/wiki/ttf07c-registers.md) |
| `property.h` addresses are lowercase hex, so `PROPERTY()`'s compile-time uniqueness check catches duplicates | [registers](.wiki/wiki/ttf07c-registers.md) |
| Upstream style: subjects like upstream's history, `git clang-format` on changed lines, no wiki/TODO references, dates or "maintainer" in code and yaml comments; new work goes into its topic commit | `dev/development.md` |
| Times are CET (`Europe/Berlin`) in the wiki, logs, `TODO.md` and replies; another zone is converted or marked (`12:00 UTC`) | `.wiki/AGENTS.md` |
| The login shell is zsh (`${VAR}`, not `$VAR:…`); host tools are BusyBox; `docker cp`, not bind mounts | `dev/development.md` |

## Do not hand-edit

- `yaml/examples/ttf07_wpm3i_dashboard.yaml`: exported from the live dashboard by
  `.claude/tools/dashboard/export_dashboard.py`;
- `docs/images/ttf07c/`: taken by `.claude/tools/dashboard/take_screenshots.py`.

Both are redone after a change that adds, renames or removes entities (`dev/development.md`).

## TODO.md

`workflow.md` says what belongs in it; `todo-housekeeping` is how to revise it. This project's file is `TODO.md`
(not `Todo.md`), its inbox is **From the maintainer**, it adds **Planned tests** (runs on the heat pump, removed once
run and ingested), and groups items by area: Heat pump, Cooling, Firmware, Home Assistant, Upstream.

## The wiki

The wiki is this fork's knowledge about the heat pump. Before working on a register or a heat pump question, read
`.wiki/wiki/index.md` and the pages it points to. **Ingest is part of the work**: a test, capture or finding updates
its pages, the index and `log.md` in the same change. The rest is `.wiki/AGENTS.md`.
