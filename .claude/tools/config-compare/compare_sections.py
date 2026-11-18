"""Order-independent diff of two `esphome config` dumps: each list item (and each on_boot entry) as a JSON string."""
import sys, json, yaml, collections
class L(yaml.SafeLoader): pass
L.add_multi_constructor('!', lambda l, s, n: l.construct_scalar(n) if isinstance(n, yaml.ScalarNode) else (l.construct_sequence(n) if isinstance(n, yaml.SequenceNode) else l.construct_mapping(n)))
def load(f):
    t = open(f).read(); return yaml.load(t[t.index('esphome:'):], Loader=L)
def items(c):
    out = collections.Counter()
    for k, v in c.items():
        if k == 'esphome':
            for b in v.get('on_boot', []): out[('on_boot', json.dumps(b, sort_keys=True, default=str))] += 1
            rest = {x: y for x, y in v.items() if x != 'on_boot'}
            out[('esphome', json.dumps(rest, sort_keys=True, default=str))] += 1
        elif isinstance(v, list):
            for e in v: out[(k, json.dumps(e, sort_keys=True, default=str))] += 1
        else: out[(k, json.dumps(v, sort_keys=True, default=str))] += 1
    return out
a, b = items(load(sys.argv[1])), items(load(sys.argv[2]))
for tag, d in (('ONLY BEFORE', a - b), ('ONLY AFTER', b - a)):
    for (sec, txt), n in sorted(d.items()):
        j = json.loads(txt); ident = j.get("id") if isinstance(j, dict) else None; print(tag, sec, n, ident or txt[:160].replace(chr(10), " "))
