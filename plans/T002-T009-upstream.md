# Plan: upstream PRs for TTF07 C / WPM3i (kr0ner/OneESP32ToRuleThemAll)

T002, T009. Fork only. History of the earlier rebuilds: git.

## Goal

kr0ner gets a short series in upstream style: one commit per topic, no fork history, no wiki/TODO references, dates
or "maintainer" in code and yaml. Decisions: **everything goes upstream** (FEK emulation, heating control, debug
sensors, as separate packages later); upstream's `ttf07.yaml` is **not replaced** but becomes a variant on a shared
`ttf07_base.yaml`, the way upstream did it for the WPL/WPE family (`b7a9c1a`, `wxx_base.yaml`).

## The series on `ttf07-port` (on `upstream/master`)

| # | Commit | PR |
|---|---|---|
| 1 | Add detailed CAN message logging | 1 |
| 2 | Add CanNode Bedienteil and apply control panel writes at once | 1 |
| 3 | Analytics: publish under the entity id | 1 |
| 4 | Templates: number mode, write lock and no-value option, device class for wp_generic_combined | 1 |
| 5 | Templates: add wp_power and wp_debug | 1 |
| 6 | wp_climate: add preset thermostat type | 1 |
| 7 | txx_base: configurable VORLAUFISTTEMP target and HK1 settings write lock | 1 |
| 8 | Introduce ttf07_base.yaml as the shared base for TTF07 variants | 2a |
| 9 | Add TTF07 C properties (WPM3i) | 2b |
| 10 | Add TTF07 C with WPM3i manager | 2b |
| 11 | Add TTF07 C dashboard example (`doc/ttf07c/dashboard-example/`) | 2b |
| 12 | Add TTF07 C user guide (`doc/ttf07c.md`, `doc/ttf07c/images/`, README link) | 2b |
| 12b | Add TTF07 C knowledge base (`doc/ttf07c/`: README, control panel menu, llmwiki `.wiki/`) | 2b |
| 13 | docs: AGENTS.md, workflow.md, TODO, wiki, skills, plans, dev, tools (fork only) | never |

The list with one-line descriptions is in [`dev/development.md`](../dev/development.md) "Commits"; keep both in step.

## PRs

Texts: [`upstream/issue-text.md`](../upstream/issue-text.md).

Each PR from `ttf07-port` against `kr0ner:master`, in this order; a later PR waits for the earlier one (stacked PRs
from a fork show the earlier commits until those are merged: say so in the text).

- **PR 1, shared code (1–7).** No behaviour change for other heat pumps; every new template parameter defaults to the
  old behaviour. Mention in the text: "Message received" moves from INFO to DEBUG (commit 1).
- **PR 2a, `ttf07_base.yaml` (8).** Pure refactor, independent of PR 1. Proof for the description: `esphome config`
  of a plain TTF07 device before/after, all 61 entities identical (name, domain, unit, state class, device class,
  icon, interval); only the boot lambdas are split over two files.
- **PR 2b, TTF07 C with WPM3i (9–12).** The guide `doc/ttf07c.md` is the description's base. The `doc/` folder is
  new upstream: ask kr0ner whether he wants it; if not, drop commit 12 and upload the screenshots into the PR
  description instead.
- **Follow-ups, one PR each, only after asking kr0ner:** HK1 room values (`RAUMISTTEMP`, `VERSTELLTE_RAUMSOLLTEMP`,
  `RAUMFEUCHTE`) out of `txx_base.yaml` into a package that `ttf07.yaml`, `thz304.yaml`, `thz_base.yaml` include
  (then the WPM3i variant needs no hidden entities); pressure scaling ×10 for all TTF07; status from `0x0A20` for the
  WPM3i variant (bit 4 to confirm); FEK emulation and fault list as `yaml/features/` packages; English names package
  (T010).

## Design decisions to explain in the PR texts

- **`property.h`:** the TTF07 C registers are merged into upstream's `TTF_07_C` list in address order, without
  comments (the knowledge is in the fork's wiki). A name that also exists in another model's block is fine (one model
  per build). Upstream's `0x06Aa` → `0x06aa` fixed (the uniqueness check relies on lowercase).
- **`wp_climate`:** upstream's `heating`/`hot_water` types unchanged; new `type: preset` (`PresetClimate`) with
  upstream-style keys `current_temp`, `comfort_temp`, `eco_temp`.
- **Entity names:** template entities are named by id like upstream, so `ttf07.yaml` users keep their history when
  switching; German names only in the optional package `yaml/names/ttf07_wpm3i_de.yaml`. Analytics publish under
  the entity id (commit 3), so a renamed entity keeps its topic.
- **Unidentified registers:** no `TBD_*` in `property.h`; `wp_debug` takes a raw `address`, the sensors are in the
  optional package `yaml/ttf07_wpm3i_debug.yaml`.

## Reorganizing commits (no interactive rebase on this host)

1. Snapshot of the wanted end state: `git add -A && git commit -m "WIP final state (temporary)"`, note its hash `F`.
2. New branch at the last commit that stays as is: `git checkout -b ttf07-port-new <hash>`.
3. Per topic commit: `git checkout F -- <files of that topic>` and `git commit` (upstream style subject, body with
   the why; no `Co-Authored-By`), or `git cherry-pick <old>` and then `git checkout F -- <files> && git commit
   --amend --no-edit` to bring it to the end state.
4. Last commit (docs): `git cherry-pick <old docs>`, `git checkout F -- .`, `git add -A`, `git commit --amend`.
5. Must be empty: `git diff F HEAD`. Then `git checkout ttf07-port && git reset --hard ttf07-port-new` and delete the
   temporary branch (the files on disk do not change).
6. Each yaml refactor: prove "no entity changes" with `.claude/tools/config-compare/` (this installation and, for
   shared files, a plain upstream device), then `esphome compile`; flash only with the maintainer's go.
7. Update `dev/development.md` "Commits" and the table above; the maintainer force-pushes (no GitHub credentials here).

## Before opening a PR

- `git fetch upstream`; if upstream moved, `git rebase upstream/master`, compile, flash-test.
- Watch upstream PR **#389** (node-aware `PROPERTY_NODE`, touches `property.h`, `communication.cpp`,
  `callback_handler.h`): rebase if it lands first.
- Compile upstream's targets with the branch: `esp32-poe-technik.yaml` with `thz504.yaml` (wp_climate types),
  `ttf07.yaml` and `wpl25.yaml`; and this device (`/config/esphome/heatpump-ttf07c.yaml`).
- `git diff upstream/master -- yaml/thz*.yaml` is empty.
