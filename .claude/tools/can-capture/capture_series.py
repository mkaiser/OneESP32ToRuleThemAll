#!/usr/bin/env python3
"""Value series per CAN register from a firmware log capture (plans/T001-register-decoding.md, phase 2).

Input: an ESPHome log of heatpump-ttf07c, raw or filtered to the `Communication` lines, e.g.
/share/heatpump-capture/2026-11-18-passive-24h.log or doc/ttf07c/.wiki/raw/captures/*.log. Line format: can-bus.md,
"Observing the bus":
    [12:29:50.018] Message from 0x180 (Kessel) Read/Write ID 0x67 0x01 (to 0x301/HK1, system response)
                   property SYSTEM_PRAESENZ (0x00FE) raw value 256 (0x0100) data ...

A series is one (register, sender, target, message type). Read requests carry no value and are skipped
unless --reads is given.

    capture_series.py LOG                          # summary: every series, changed ones first
    capture_series.py LOG --unknown                # only registers without a firmware name (UNKNOWN, TBD_*)
    capture_series.py LOG --changes 0xFE09,0x000A  # every value change of these registers, with time
    capture_series.py LOG --csv changes.csv        # all value changes as CSV (for HA history comparison)
    capture_series.py LOG --gaps                   # reconnects and gaps > 60 s in the log
    capture_series.py LOG --exclude 16:42-16:51    # ignore a time window (e.g. a flash), repeatable

Times are the log clock (CET). The date comes from the "# Passive capture start YYYY-MM-DD" header or --date;
a clock that jumps back by more than an hour counts as midnight.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field

LINE = re.compile(
    r'^\[(?P<t>\d\d:\d\d:\d\d)(?:\.(?P<ms>\d+))?\]\s*(?:\[[A-Z]\]\[[^\]]+\]:\s*)?'
    r'(?P<kind>Message|Request \(dropped\)) from (?P<src>0x[0-9A-Fa-f]+) \((?P<srcname>[^)]*)\)'
    r' Read/Write ID \S+ \S+ \(to (?P<dst>0x[0-9A-Fa-f]+)/[^,]*, (?P<mtype>[^)]*)\)'
    r' property (?P<name>\S+) \((?P<addr>0x[0-9A-Fa-f]{4})\) raw value -?\d+ \((?P<raw>0x[0-9A-Fa-f]+)\)')
HEADER_DATE = re.compile(r'start (\d{4}-\d{2}-\d{2})')
# Known signals shown next to every change: status words (WPM3i, Kessel) and the compressor current (MFG)
CONTEXT = {'0x4E5E': 'wpm', '0x0A20': 'kessel', '0xFE07': 'amp'}


@dataclass
class Series:
    addr: str
    name: str
    src: str
    dst: str
    mtype: str
    frames: int = 0
    values: dict = field(default_factory=lambda: defaultdict(int))
    changes: list = field(default_factory=list)  # (datetime, old, new, context)
    first: tuple | None = None                   # (datetime, value)
    last: tuple | None = None

    @property
    def unknown(self) -> bool:
        return self.name in ('UNKNOWN', '?') or self.name.startswith(('TBD', 'DEBUG'))


def signed(raw: int) -> int:
    return raw - 0x10000 if raw >= 0x8000 else raw


def fmt(raw: int) -> str:
    """Raw value with the common readings: signed, /10, high/low byte."""
    if raw in (0x8000, 0x8080, 0x9000, 0xA000, 0xFE70):
        return f'0x{raw:04X} ({ {0x8000: "no value", 0x8080: "empty", 0x9000: "AUS", 0xA000: "AUS?", 0xFE70: "-40.0 no sensor"}[raw] })'
    s = signed(raw)
    return f'0x{raw:04X} ({s}, /10={s / 10:g}, hi={raw >> 8} lo={raw & 0xFF})'


def parse_window(text: str) -> tuple[dt.time, dt.time]:
    a, b = text.split('-')
    return dt.time.fromisoformat(a), dt.time.fromisoformat(b)


def read(path: str, date: dt.date | None, reads: bool, exclude: list[tuple[dt.time, dt.time]]):
    series: dict[tuple, Series] = {}
    gaps: list[str] = []
    day = date
    prev: dt.datetime | None = None
    context: dict[str, int] = {}
    with open(path, errors='replace') as f:
        for line in f:
            if line.startswith('#'):
                m = HEADER_DATE.search(line)
                if m and day is None:
                    day = dt.date.fromisoformat(m.group(1))
                if 'reconnect' in line or 'end' in line:
                    gaps.append(line.strip())
                continue
            m = LINE.search(line)
            if not m:
                continue
            if day is None:
                day = dt.date.today()
            t = dt.time.fromisoformat(m['t'])
            now = dt.datetime.combine(day, t)
            if prev and now < prev - dt.timedelta(hours=1):  # midnight
                day += dt.timedelta(days=1)
                now = dt.datetime.combine(day, t)
            if prev and now - prev > dt.timedelta(seconds=60):
                gaps.append(f'gap {prev:%Y-%m-%d %H:%M:%S} -> {now:%H:%M:%S} ({(now - prev).seconds} s)')
            prev = now
            if any(a <= t <= b for a, b in exclude):
                continue
            mtype = m['mtype']
            if mtype == 'read' and not reads:
                continue
            key = (m['addr'].upper(), m['src'].upper(), m['dst'].upper(), mtype)
            s = series.get(key)
            if s is None:
                s = series[key] = Series(m['addr'].upper().replace('0X', '0x'), m['name'], m['src'], m['dst'], mtype)
            raw = int(m['raw'], 16)
            addr = '0x' + m['addr'][2:].upper()
            if addr in CONTEXT and mtype != 'read':
                context[addr] = raw
            s.frames += 1
            s.values[raw] += 1
            if s.last is not None and s.last[1] != raw:
                ctx = ' '.join(f'{CONTEXT[a]}=0x{v:04X}' for a, v in context.items())
                s.changes.append((now, s.last[1], raw, ctx))
            if s.first is None:
                s.first = (now, raw)
            s.last = (now, raw)
    return series, gaps


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('log')
    ap.add_argument('--date', type=dt.date.fromisoformat, help='date of the first line (default: from the header)')
    ap.add_argument('--unknown', action='store_true', help='only registers without a firmware name')
    ap.add_argument('--changes', help='comma separated addresses: print every value change')
    ap.add_argument('--csv', help='write all value changes to this CSV file')
    ap.add_argument('--gaps', action='store_true', help='print reconnects and gaps > 60 s')
    ap.add_argument('--reads', action='store_true', help='include read requests (no values)')
    ap.add_argument('--exclude', action='append', default=[], type=parse_window, help='HH:MM-HH:MM to ignore')
    args = ap.parse_args()

    series, gaps = read(args.log, args.date, args.reads, args.exclude)
    rows = sorted(series.values(), key=lambda s: (not s.changes, s.addr, s.src, s.dst))
    if args.unknown:
        rows = [s for s in rows if s.unknown]

    if args.gaps:
        print('\n'.join(gaps) or 'no gaps')
        return 0

    if args.changes:
        wanted = {a.strip().lower() for a in args.changes.split(',')}
        for s in rows:
            if s.addr.lower() not in wanted:
                continue
            print(f'== {s.addr} {s.name} {s.src}->{s.dst} {s.mtype}: {s.frames} frames, first {s.first[0]:%d.%m %H:%M:%S} {fmt(s.first[1])}')
            for when, old, new, ctx in s.changes:
                print(f'   {when:%d.%m %H:%M:%S}  {fmt(old)}  ->  {fmt(new)}   [{ctx}]')
        return 0

    if args.csv:
        with open(args.csv, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['time', 'addr', 'name', 'src', 'dst', 'type', 'old', 'new', 'new_signed', 'context'])
            for s in rows:
                for when, old, new, ctx in s.changes:
                    w.writerow([when.isoformat(), s.addr, s.name, s.src, s.dst, s.mtype, f'0x{old:04X}', f'0x{new:04X}', signed(new), ctx])
        print(f'wrote {args.csv}', file=sys.stderr)
        return 0

    span = [s.first[0] for s in rows if s.first] + [s.last[0] for s in rows if s.last]
    if span:
        print(f'capture {min(span):%Y-%m-%d %H:%M:%S} .. {max(span):%Y-%m-%d %H:%M:%S}, {len(rows)} series, '
              f'{sum(1 for s in rows if s.changes)} changed, gaps/reconnects: {len(gaps)}')
    print(f'{"addr":7} {"name":28} {"path":24} {"frames":>6} {"vals":>4} {"chg":>4}  values (most frequent first)')
    for s in rows:
        vals = sorted(s.values.items(), key=lambda kv: -kv[1])
        shown = ', '.join(f'0x{v:04X}x{n}' for v, n in vals[:4]) + (' …' if len(vals) > 4 else '')
        print(f'{s.addr:7} {s.name[:28]:28} {s.src + "->" + s.dst + " " + s.mtype[:9]:24} {s.frames:6} {len(vals):4} '
              f'{len(s.changes):4}  {shown}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
