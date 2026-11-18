"""Export a Home Assistant dashboard as the TTF07 C example (yaml/examples/ttf07_wpm3i_dashboard.yaml). Fork only.

Input: two JSON files from the Home Assistant websocket API,
  - the dashboard:        {"type": "lovelace/config", "url_path": "<dashboard>"}
  - the entity registry:  {"type": "config/entity_registry/list"}
(either the full result message or just its "result").

Cards wrapped in custom:restriction-card (the live dashboard's hold-to-unlock lock, a Marketplace card) are
unwrapped: the inner card takes the wrapper's place and its grid_options. --keep-locks keeps them.

Every entity of the heat pump's ESPHome device is renamed to "<domain>.warmepumpe_<slug of its name>", the ID a
fresh install with the friendly name "Wärmepumpe" gets. Entities from elsewhere can be mapped with --map.

Usage:
  python3 export_dashboard.py dashboard.json registry.json --device-entity climate.<any entity of the device> \
      --map sensor.my_house_temperature=sensor.HOUSE_TEMPERATURE > ../../../yaml/examples/ttf07_wpm3i_dashboard.yaml
"""

import argparse
import json
import re
import sys
import unicodedata

import yaml

ENTITY = re.compile(r'"((?:sensor|binary_sensor|switch|number|select|climate|text|button)\.[a-z0-9_]+)"')
HEADER = """# Home Assistant dashboard for a Tecalor TTF07 C with WPM3i running yaml/ttf07_wpm3i.yaml.
# Use: Settings > Dashboards > Add dashboard > "New dashboard from scratch", then Edit dashboard >
# Raw configuration editor, paste this file and save.
# Entity IDs assume the ESPHome device's friendly name "Wärmepumpe" (prefix "warmepumpe_"); for another name,
# replace ".warmepumpe_" with your prefix. sensor.HOUSE_TEMPERATURE: replace with your room/house temperature sensor.
# The FEK emulation and cooling cards need the matching parts of ttf07_wpm3i.yaml; "Community Analytics" needs
# yaml/features/analytics.yaml. Entity IDs follow the German names of yaml/names/ttf07_wpm3i_de.yaml; the
# "Reverse Engineering" card needs yaml/ttf07_wpm3i_debug.yaml (registers not identified yet, may change).
"""


def slug(text: str) -> str:
    text = text.replace("ß", "ss")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


def unwrap_locks(node):
    """Replace every custom:restriction-card by its inner card (keeping the wrapper's grid_options)."""
    if isinstance(node, list):
        return [unwrap_locks(item) for item in node]
    if not isinstance(node, dict):
        return node
    if node.get("type") == "custom:restriction-card" and isinstance(node.get("card"), dict):
        inner = dict(node["card"])
        if "grid_options" in node and "grid_options" not in inner:
            inner["grid_options"] = node["grid_options"]
        return unwrap_locks(inner)
    return {key: unwrap_locks(value) for key, value in node.items()}


def load_result(path: str):
    data = json.load(open(path, encoding="utf-8"))
    return data["result"] if isinstance(data, dict) and "result" in data else data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("dashboard")
    parser.add_argument("registry")
    parser.add_argument("--device-entity", required=True, help="any entity ID of the heat pump's ESPHome device")
    parser.add_argument("--map", action="append", default=[], help="old=new for entities outside the device")
    parser.add_argument("--keep-locks", action="store_true", help="keep custom:restriction-card wrappers")
    args = parser.parse_args()

    config = load_result(args.dashboard)
    if not args.keep_locks:
        config = unwrap_locks(config)
    registry = {entry["entity_id"]: entry for entry in load_result(args.registry)}
    device = registry[args.device_entity]["device_id"]
    mapping = {
        entity_id: f"{entity_id.split('.')[0]}.warmepumpe_{slug(entry.get('original_name') or entry.get('name') or '')}"
        for entity_id, entry in registry.items()
        if entry.get("device_id") == device
    }
    mapping.update(item.split("=", 1) for item in args.map)

    text = json.dumps(config, ensure_ascii=False)
    used = sorted(set(ENTITY.findall(text)))
    unmapped = [entity_id for entity_id in used if entity_id not in mapping]
    if unmapped:
        sys.exit(f"entities outside the device, map them with --map: {', '.join(unmapped)}")
    new_ids = [mapping[entity_id] for entity_id in used]
    duplicates = {entity_id for entity_id in new_ids if new_ids.count(entity_id) > 1}
    if duplicates:
        sys.exit(f"two entities map to the same ID: {', '.join(sorted(duplicates))}")

    text = ENTITY.sub(lambda match: f'"{mapping[match.group(1)]}"', text)
    sys.stdout.write(HEADER + yaml.safe_dump(json.loads(text), allow_unicode=True, sort_keys=False, width=120))


if __name__ == "__main__":
    main()
