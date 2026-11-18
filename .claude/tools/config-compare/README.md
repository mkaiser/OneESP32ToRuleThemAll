# Config compare (fork only)

Proves that a refactor of the yaml files changes no Home Assistant entity: compare `esphome config` before and after.

```bash
C=$(docker ps --format '{{.Names}}' | grep -m1 '_esphome$')
# before: a snapshot of the old commit, e.g.
mkdir -p /homeassistant/esphome/.ttf07check/before && git archive <old-commit> components yaml | tar -x -C /homeassistant/esphome/.ttf07check/before
docker exec $C esphome config /config/esphome/heatpump-ttf07c.yaml > before.yaml   # this installation (run before the change)
# after the change:
docker exec $C esphome config /config/esphome/heatpump-ttf07c.yaml > after.yaml
python3 -I compare_entities.py before.yaml after.yaml   # visible entities by (domain, name): missing / new / changed fields
python3 -I compare_sections.py before.yaml after.yaml   # everything else, order independent (on_boot, scripts, intervals, ...)
```

Write stdout and stderr to separate files (`2>err`), the dump must contain only the YAML.

`ttf07-check-device.yaml`: a minimal device for upstream's `ttf07.yaml` (no hardware needed). Copy it to
`/config/esphome/.ttf07check/after.yaml` (and a copy whose paths point to the `before` snapshot) and run
`esphome config` / `compile` on both. Used for "Introduce ttf07_base.yaml" (61/61 entities identical, 2026-11-18).
