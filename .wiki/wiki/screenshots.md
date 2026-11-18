# Screenshots of the HA dashboard and device page

How the screenshots in [`docs/images/ttf07c/`](../../docs/images/ttf07c/) are made
(first taken 2026-11-18). They show the live "Wärmepumpe" dashboard (`lovelace` `dashboard-warmepumpe`, the
source of `yaml/examples/ttf07_wpm3i_dashboard.yaml`) and the HA device page of `heatpump-ttf07c`. The user
guide `docs/ttf07c.md` embeds two of them; they go upstream with it in PR 2b (commit 12) if kr0ner wants the
`docs/` folder, otherwise they are uploaded into the PR description (decision 2026-11-18 evening, replaces "fork
only, upload only" from earlier that day).

## Retake

```bash
python3 /homeassistant/esphome/OneESP32ToRuleThemAll/.claude/tools/dashboard/take_screenshots.py
```

Run it on the HA host (SSH add-on); it overwrites the PNGs in `docs/images/ttf07c/`. Look at every image before committing.
Retake after the dashboard changes (TODO recurrent check "update the HA dashboard").

| File | Content |
|---|---|
| `dashboard-1-uebersicht.png` … `dashboard-5-diagnose.png` | the five views of the dashboard, full page, 1440 px wide |
| `device-0-top.png` | top of the device page (device info, start of Steuerung, activity) |
| `device-1-steuerung.png` … `device-4-diagnose.png` | one card each: Steuerung, Sensoren, Konfiguration, Diagnose |

## How it works

Pattern taken from the Sungrow integration repo (`/homeassistant/integrations/git_Sungrow-SHx-Inverter-Modbus-Home-Assistant`,
branch `proper-ha-integration`: `scripts/dev/screenshot.py`, `doc/development.md` "Screenshots for the docs"):
Playwright with headless Chromium logs in **through HA's login form** as a person would, waits for the page to
settle, and writes PNGs. Differences here:

- **Browser in a container.** The SSH add-on is Alpine (musl); Playwright's Chromium needs glibc, so the Sungrow
  repo's venv setup (`scripts/dev/setup.sh`, Debian devcontainer) does not work. `take_screenshots.py` runs
  `screenshots_playwright.py` in the official image `mcr.microsoft.com/playwright/python:v1.49.1-noble`
  (~1.5 GB, pulled once) with `--network host`, so the browser reaches HA at `http://127.0.0.1:8123`.
- **No bind mounts.** The Docker daemon resolves `-v` paths on the host OS, where `/homeassistant` and the add-on's
  `/tmp` do not exist ("read-only file system"). The script uses `docker create`, `docker cp` (script in, PNGs
  out), `docker start -a` and removes the container.
- **Login.** The Sungrow script logs in as `dev`/`dev` on a scratch instance; this is the live instance. The add-on's
  `SUPERVISOR_TOKEN` only works through the Supervisor proxy, not for the frontend, and HA refuses long-lived
  tokens for the system user "Supervisor". So the script creates a **temporary local-only admin user** with a
  random password through the websocket API (`config/auth/create`, `config/auth_provider/homeassistant/create`,
  helper `/homeassistant/.claude/tools/naming/ha.py`), passes it to the container as environment variables, and
  deletes it in a `finally` (`config/auth/delete`), also when the run fails. Admin is needed for the device page.
- **No private data.** Right after login the script sets `localStorage.dockedSidebar = "always_hidden"`: the
  sidebar lists the owner's dashboards and the user name. Browser locale `de-DE`, time zone Europe/Berlin, light theme.
- **Waiting.** `networkidle` plus 6 s per page: history graphs and statistics load after `networkidle`.
- **Device page.** It scrolls inside a container (a full-page screenshot only gets the first screen) and is
  longer than one image can be (> 9000 px with ~200 entities). The script renders it in a 1440 × 14000 viewport and
  clips each card by its bounding box; the cards sit in shadow DOM, so a small script walks the shadow roots and
  finds the `ha-card` whose `header` property is the card title.

## Pitfalls seen

- The container installs `playwright` with pip on every run; the download timed out twice on 2026-11-18
  (`No module named 'playwright'`). Since then pip runs with `--default-timeout=120 --retries 5`; if it still fails,
  rerun.
- zsh: `$B:scripts/...` is a modifier; write `"${B}:path"` in `git show` (also [development](../../dev/development.md)).
- BusyBox on the host: no `grep --line-buffered`/`sed -u` (affects log capture, not this script).
- The device page shows the ESP's MAC address (`device-0-top.png`); it is the ESP's, not a secret, but check
  before publishing.
