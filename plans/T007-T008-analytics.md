# Plan: community analytics

T007, T008. Fork only.

## What and why

Upstream's analytics publish every entity to the community MQTT and show them in the community Grafana. Check it
keeps working for this device, and decide what the TTF07 C's new entities send.

## Known

- Live since 2026-11-16, all entities, district Bielefeld. "Analytics MQTT Connected" should stay on; "Github" shows
  when upstream has a newer version (then consider rebasing, `dev/development.md`).
- Own data: [community Grafana](https://oneesp32torulethemall.freeddns.org/d/advz2wx/test?var-device_hash=43d17174)
  (anonymous, device hash `43d17174` = "Analytics Global Device ID"). The panels check access with the selected
  "Numeric Sensor": select one this device sends (e.g. `&var-measurement=AUSSENTEMP`); the default `ABLUFTFEUCHTE`
  (THZ only) shows "No data" everywhere. Panel queries are readable anonymously (`/api/dashboards/uid/advz2wx`).
- 2026-11-18: CoP WW 2.45 vs community 2.96, heating 5.25 vs 5.62
  ([screenshot](../.wiki/raw/2026-11-18-community-grafana.png)).
- Possible hint upstream: default the numeric sensor to one every variant sends (e.g. `AUSSENTEMP`).
- To leave analytics: comment out the `analytics` line in `heatpump-ttf07c.yaml` (HA config repo) and flash.
- New entities (Taupunkt, Raum WPM3i, Partyprogramm, NHZ heat totals, …) are published under their firmware ids,
  which upstream's Grafana does not know. Options: keep them out (`exposed: "false"`) or map them to upstream names.
  Ignored for now (maintainer, 2026-11-17).

## Status log

- 2026-11-19: plan created from the `TODO.md` entries when `TODO.md` moved to `workflow.md`.
