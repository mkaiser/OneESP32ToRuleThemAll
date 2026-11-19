# Development: build, flash, observe, commit

For agents and the maintainer working on this fork. Fork only, never upstream. The rules are in
[`AGENTS.md`](../AGENTS.md); this page is the how.

## Branches and remotes

| Branch | Purpose |
|---|---|
| `ttf07-port` | **Current work, default branch on GitHub.** Upstream `master` plus the topic commits below, rebased onto upstream. The only branch for these commits: no `pr/*` branches; PRs are opened from `ttf07-port` later (maintainer's decision 2026-11-18). |
| `archive/ttf07-old` | Archive of the old implementation (pre-component `src/` structure; was `ttf07` until 2026-11-18). Do not develop on it. |
| `master` | Local mirror of upstream; never commit to it. |

Remotes: `origin` = the fork (`mkaiser/OneESP32ToRuleThemAll`), `upstream` = `kr0ner/OneESP32ToRuleThemAll`.
This host has no GitHub credentials: the maintainer pushes.

The device configuration lives in the Home Assistant repo: `/homeassistant/esphome/heatpump-ttf07c.yaml`. It
includes `yaml/ttf07_wpm3i.yaml` and loads `components/` as a local external component (this repo is a submodule
at `esphome/OneESP32ToRuleThemAll`).

## Build and flash

ESPHome runs in the Home Assistant ESPHome add-on:
```bash
C=$(docker ps --format '{{.Names}}' | grep -m1 '_esphome$')
docker exec $C esphome config  /config/esphome/heatpump-ttf07c.yaml   # validate
docker exec $C esphome compile /config/esphome/heatpump-ttf07c.yaml   # build
docker exec $C esphome run --no-logs --device 192.168.178.37 /config/esphome/heatpump-ttf07c.yaml  # build + OTA
docker exec $C timeout 60 esphome logs --device 192.168.178.37 /config/esphome/heatpump-ttf07c.yaml
```
- OTA is encrypted with the API key (no password).
- Flashing reboots the ESP. Fine for testing, but say when you do it. After a flash the FEK emulation is off for
  up to ~8 min ([heating control](../.wiki/wiki/heating-control.md)).
- After a flash, check: the log has no errors, the entities have values in HA, nothing writes to the heat pump
  unintentionally.
- Home Assistant states: `curl -H "Authorization: Bearer $SUPERVISOR_TOKEN" http://supervisor/core/api/states`.
- A yaml refactor proves "no entity changes" with [`.claude/tools/config-compare/`](../.claude/tools/config-compare/README.md).

## Long CAN captures

`.claude/tools/can-capture/`: `capture.sh` (run detached with `setsid nohup`; reconnects after a drop and marks it
`# reconnect <time>`), `filter.py` (keeps the `Communication` lines), `capture_series.py <log>` (value changes per
register; `--unknown`, `--changes`, `--csv`, `--gaps`, `--exclude HH:MM-HH:MM`).

- Alive: `wc -l` on the log, `ps -eo pid,args | grep capture.sh`; a finished log ends with `# Passive capture end`.
- **Stopping early:** kill `capture.sh` by PID (`pkill -f capture.sh` also kills your own shell when its command
  line contains the pattern) **and** the `esphome logs` client inside the ESPHome container. Killing only the
  host-side `docker exec` leaves that client connected to the ESP (2026-11-18: 7 leftovers blocked the log). Exactly
  one client may be connected.

## Environment pitfalls

- The SSH add-on's shell tools are BusyBox: no `grep --line-buffered`, no `sed -u`. Use Python for stream filters.
- Docker bind mounts (`-v`) are resolved on the host OS, not in the add-on: use `docker cp`
  (see `.claude/tools/dashboard/take_screenshots.py`, [screenshots](../.wiki/wiki/screenshots.md)).
- The login shell is zsh: `$VAR:c…` is a modifier (`$FINAL:components/…` breaks). Write `${VAR}` or run such
  scripts with `bash`.
- HA websocket from the host: `/homeassistant/.claude/tools/naming/ha.py` (`ws([...])`).

## Dashboard and screenshots

After a change that adds, renames or removes entities: update `lovelace.dashboard_warmepumpe`, re-export
`yaml/examples/ttf07_wpm3i_dashboard.yaml` with `.claude/tools/dashboard/export_dashboard.py`, retake
`docs/images/ttf07c/` with `.claude/tools/dashboard/take_screenshots.py` ([screenshots](../.wiki/wiki/screenshots.md)).

## Commits

`ttf07-port` is a stack of topic commits on top of upstream `master`, so it can go upstream as is
([`plans/T002-T009-upstream.md`](../plans/T002-T009-upstream.md)). Commits 1–7 are PR 1 (shared code), 8 is PR 2a (TTF07 refactor, no
entity change), 9–12 PR 2b (TTF07 C):

1. Add detailed CAN message logging
2. Add CanNode Bedienteil and apply control panel writes at once
3. Analytics: publish under the entity id
4. Templates: number mode and write lock, device class for wp_generic_combined
5. Templates: add wp_power and wp_debug
6. wp_climate: add preset thermostat type (upstream's `heating`/`hot_water` stay unchanged)
7. txx_base: configurable VORLAUFISTTEMP target and HK1 settings write lock
8. Introduce ttf07_base.yaml as the shared base for TTF07 variants (`ttf07.yaml` becomes a variant, entities unchanged)
9. Add TTF07 C properties (WPM3i)
10. Add TTF07 C with WPM3i manager (`yaml/ttf07_wpm3i.yaml` on `ttf07_base.yaml`, names and debug packages, README, esp32-*.yaml)
11. Add TTF07 C dashboard example (`yaml/examples/ttf07_wpm3i_dashboard.yaml`)
12. Add TTF07 C user guide (`docs/ttf07c.md`, `docs/images/ttf07c/`, README link)
13. docs: AGENTS.md, workflow.md, TODO, wiki, skills, plans, dev, tools (fork only, never upstream)

- **Upstream style:** subjects like upstream's history; C++ formatted with `.clang-format` on changed lines only
  (`git clang-format`).
- **New work goes into its topic commit.** `git rebase -i --autosquash` is not available here: rebuild with
  `git checkout <final> -- <files>` per topic ([`plans/T002-T009-upstream.md`](../plans/T002-T009-upstream.md), "Reorganizing commits").
  While commit 13 is the last one, fork-only doc changes go in with `git commit --amend -- <paths>`.
- **Update from upstream:** `git fetch upstream && git rebase upstream/master`, then compile and flash-test.
