#!/usr/bin/env python3
"""Analyze an ESPHome log capture of the OneESP32ToRuleThemAll heat pump firmware.

Parses the detailed CAN lines written by processCanMessage():
  [15:05:09.122][D][Communication:235]: Message from 0x180 (Kessel) Read/Write ID 0xD2 0x00 (to 0x680/ESPClient) property QUELLENTEMP_MIN (0x01B0) raw value 65446 (0xFFA6)
  [16:25:18.914][V][Communication:229]: Request (dropped) from 0x100 (unknown) Read/Write ID 0x31 0x00 (to 0x180/Kessel) property RUECKLAUFISTTEMP (0x0016) raw value 0 (0x0000)
and entity state lines:
  [16:25:22.424][V][sensor:119]: 'TBD_04' >> 18

Usage:
  analyze_can.py LOG [--property NAME|0xADDR ...] [--entity TEXT ...] [--since HH:MM[:SS]] [--until HH:MM[:SS]]
                 [--changed-at HH:MM[:SS]]

--changed-at: time of the change on the control panel (log clock). Lines before it are the baseline; writes and
value changes after it that never occurred in the baseline are marked NEW.
"""
import argparse
import re
import sys
from collections import defaultdict

CAN_RE = re.compile(
    r"^\[(?P<time>\d\d:\d\d:\d\d)(?:\.\d+)?\]\[(?P<lvl>\w)\]\[Communication:\d+\]: "
    r"(?P<kind>Message|Request \(dropped\)) from 0x(?P<from>[0-9A-Fa-f]+) \((?P<fromname>[^)]*)\) "
    r"Read/Write ID 0x(?P<b0>[0-9A-Fa-f]{2}) 0x(?P<b1>[0-9A-Fa-f]{2}) \(to 0x(?P<to>[0-9A-Fa-f]+)/(?P<toname>[^),]*)(?:, [^)]*)?\) "
    r"property (?P<prop>\S+) \(0x(?P<addr>[0-9A-Fa-f]{4})\) raw value (?P<value>\d+)"
)
ENTITY_RE = re.compile(r"^\[(?P<time>\d\d:\d\d:\d\d)(?:\.\d+)?\]\[\w\]\[[\w.]+:\d+\]: '(?P<name>[^']+)' >> (?P<value>.*)$")
SEND_RE = re.compile(r"^\[(?P<time>\d\d:\d\d:\d\d)(?:\.\d+)?\]\[\w\]\[Communication:\d+\]: sendData\((?P<rest>.*)\)$")


TYPES = {0: "WRITE", 1: "read", 2: "response", 3: "ack", 4: "write-ack", 5: "write-resp", 6: "system", 7: "sys-resp"}
NODES = {0x100: "Bedienteil", 0x180: "Kessel", 0x301: "HK1", 0x302: "HK2", 0x480: "Manager", 0x601: "FEK?",
         0x680: "ESPClient", 0x700: "MFG"}


def msg_type(b0: int, b1: int) -> str:
    """Message type = low nibble of the first ID byte (0 write, 1 read, 2 response, ..., 6 system, 7 system resp)."""
    return TYPES.get(b0 & 0x0F, f"type{b0 & 0x0F}")


def addressed_id(b0: int, b1: int) -> int:
    """Addressed node from the ID bytes: ((b0 & 0xf0) << 3) | (b1 & 0x7f)."""
    return ((b0 & 0xF0) << 3) | (b1 & 0x7F)


def decodings(raw: int) -> str:
    signed = raw - 0x10000 if raw & 0x8000 else raw
    swapped = ((raw & 0xFF) << 8) | (raw >> 8)
    if raw == 0x8000:
        return "0x8000 = no value / not available"
    return (f"dec/10={signed / 10:g}  cent/100={signed / 100:g}  int={signed}  "
            f"lowbyte={raw & 0xFF}  little_endian={swapped}  bool={'on' if raw else 'off'}")


def in_window(t: str, since: str, until: str) -> bool:
    return (not since or t >= since) and (not until or t <= until)


def norm_time(t):
    if not t:
        return None
    return t if t.count(":") == 2 else t + ":00"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--property", action="append", default=[], help="property name or hex address (repeatable)")
    ap.add_argument("--entity", action="append", default=[], help="substring of an entity name (repeatable)")
    ap.add_argument("--since")
    ap.add_argument("--until")
    ap.add_argument("--changed-at", dest="changed_at")
    a = ap.parse_args()
    since, until, changed_at = norm_time(a.since), norm_time(a.until), norm_time(a.changed_at)

    frames, entities, sends = [], [], []
    for line in open(a.log, errors="replace"):
        line = line.rstrip("\n")
        if m := CAN_RE.match(line):
            d = m.groupdict()
            if in_window(d["time"], since, until):
                b0, b1 = int(d["b0"], 16), int(d["b1"], 16)
                d["type"] = msg_type(b0, b1)
                # recompute the addressed node (firmware before the type-aware logging decoded types 4-7 wrongly)
                to = addressed_id(b0, b1)
                d["to"] = f"{to:03X}"
                d["toname"] = NODES.get(to, d["toname"] if d["toname"] not in ("unknown",) else "unknown")
                frm = int(d["from"], 16)
                if d["fromname"] == "unknown" and frm in NODES:
                    d["fromname"] = NODES[frm]
                d["value"] = int(d["value"])
                d["addr"] = d["addr"].upper()
                frames.append(d)
        elif m := ENTITY_RE.match(line):
            if in_window(m["time"], since, until):
                entities.append(m.groupdict())
        elif m := SEND_RE.match(line):
            if in_window(m["time"], since, until):
                sends.append(m.groupdict())

    if not frames:
        print("No detailed CAN lines found. Is the firmware with detailed CAN logging (ttf07-port, commit 516ea7c+) running?")
        return 1

    print(f"Capture: {frames[0]['time']} .. {frames[-1]['time']}, {len(frames)} CAN lines, {len(entities)} entity updates")
    print()

    # 1. Target properties
    targets = [p.upper().removeprefix("0X") if p.lower().startswith("0x") else p.upper() for p in a.property]
    for t in targets:
        hits = [f for f in frames if f["addr"] == t.zfill(4) or f["prop"].upper() == t]
        print(f"=== Property {t}: {len(hits)} lines")
        last = {}
        for f in hits:
            key = (f["from"], f["to"])
            changed = "" if last.get(key) in (None, f["value"]) else "   <-- CHANGED"
            last[key] = f["value"]
            print(f"  {f['time']} {f['type']:8} 0x{f['from']}({f['fromname']}) -> 0x{f['to']}({f['toname']}) "
                  f"{f['prop']} (0x{f['addr']}) raw {f['value']} (0x{f['value']:04X}){changed}")
        vals = sorted({f["value"] for f in hits if f["type"] != "read"})
        for v in vals:
            print(f"    raw {v}: {decodings(v)}")
        print()

    # 2. Writes between other nodes (e.g. WPM3i -> Kessel after a change on the control panel).
    #    Identical writes are grouped; with --changed-at, combinations not seen in the baseline are marked NEW.
    writes = [f for f in frames if f["type"] in ("WRITE", "system", "sys-resp") and f["toname"] != "ESPClient"]
    baseline = {(f["from"], f["to"], f["addr"], f["value"]) for f in writes if changed_at and f["time"] < changed_at}
    groups = {}
    for f in writes:
        k = (f["from"], f["to"], f["addr"], f["value"])
        if k not in groups:
            groups[k] = {"f": f, "n": 0, "first": f["time"], "last": f["time"]}
        groups[k]["n"] += 1
        groups[k]["last"] = f["time"]
    print(f"=== Writes and system messages between heat pump nodes: {len(writes)} ({len(groups)} distinct)")
    for k, g in sorted(groups.items(), key=lambda kv: kv[1]["first"]):
        f = g["f"]
        new = "  NEW" if changed_at and k not in baseline and g["first"] >= changed_at else ""
        print(f"  {g['first']}..{g['last']} x{g['n']:<3} {f['type']:8} 0x{f['from']}({f['fromname']}) -> 0x{f['to']}({f['toname']}) "
              f"{f['prop']} (0x{f['addr']}) raw {f['value']} (0x{f['value']:04X}){new}  [{decodings(f['value'])}]")
    print()

    # 3. Value changes per (property, sender, receiver)
    series = defaultdict(list)
    for f in frames:
        if f["type"] == "read":
            continue
        series[(f["addr"], f["prop"], f["fromname"] or f["from"], f["toname"] or f["to"])].append((f["time"], f["value"]))
    changes = []
    for key, pts in series.items():
        trans = [(pts[i][0], pts[i - 1][1], pts[i][1]) for i in range(1, len(pts)) if pts[i][1] != pts[i - 1][1]]
        if trans:
            changes.append((trans[0][0], key, trans, len(pts)))
    changes.sort()
    print(f"=== Properties whose raw value changed: {len(changes)} (sorted by first change)")
    for first, (addr, prop, frm, to), trans, n in changes:
        unknown = "  [UNKNOWN property]" if prop.upper() in ("UNKNOWN", "INDEX_NOT_FOUND") else ""
        if changed_at:
            before = any(t < changed_at for t, _, _ in trans)
            after = any(t >= changed_at for t, _, _ in trans)
            if after and not before:
                unknown += "  NEW (stable before --changed-at)"
            elif after:
                unknown += "  (also fluctuates in baseline)"
        shown = ", ".join(f"{t} {o}->{v}" for t, o, v in trans[:6]) + (" ..." if len(trans) > 6 else "")
        print(f"  {prop} (0x{addr}) {frm}->{to}: {len(trans)} change(s) in {n} values: {shown}{unknown}")
    print()

    # 3b. Senders: first/last frame per node (shows nodes that appear or disappear, e.g. when plugging in the FEK)
    senders = {}
    for f in frames:
        k = f"0x{f['from']}({f['fromname']})"
        e = senders.setdefault(k, {"n": 0, "first": f["time"], "last": f["time"], "props": set()})
        e["n"] += 1
        e["last"] = f["time"]
        e["props"].add(f["prop"])
    print("=== Senders (first..last frame, count, properties)")
    for k, e in sorted(senders.items(), key=lambda kv: kv[1]["first"]):
        props = ", ".join(sorted(e["props"]))[:110]
        print(f"  {k:22} {e['first']}..{e['last']} n={e['n']:<5} {props}")
    print()

    # 4. Unknown properties seen at all
    unknown = sorted({(f["addr"], f["fromname"] or f["from"]) for f in frames if f["prop"].upper() in ("UNKNOWN", "INDEX_NOT_FOUND")})
    if unknown:
        print(f"=== Unknown addresses seen ({len(unknown)}): " + ", ".join(f"0x{a} from {n}" for a, n in unknown))
        print()

    # 5. Entity updates matching --entity
    for e in a.entity:
        hits = [x for x in entities if e.lower() in x["name"].lower()]
        print(f"=== Entity '{e}': {len(hits)} updates")
        for x in hits:
            print(f"  {x['time']} '{x['name']}' >> {x['value']}")
        print()

    if sends:
        print(f"=== Writes sent by the ESP itself (sendData): {len(sends)}")
        for s in sends:
            print(f"  {s['time']} {s['rest']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
