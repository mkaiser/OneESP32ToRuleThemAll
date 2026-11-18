# Compare the visible entities of two `esphome config` dumps (see README.md).
"""Compare the entities of two `esphome config` dumps by (domain, name): presence and key fields."""
import sys, yaml
class L(yaml.SafeLoader): pass
L.add_multi_constructor('!', lambda l, s, n: l.construct_scalar(n) if isinstance(n, yaml.ScalarNode) else (l.construct_sequence(n) if isinstance(n, yaml.SequenceNode) else l.construct_mapping(n)))
KEYS = ['internal', 'icon', 'unit_of_measurement', 'accuracy_decimals', 'state_class', 'device_class', 'entity_category',
        'update_interval', 'disabled_by_default', 'mode', 'min_value', 'max_value', 'step', 'filters', 'options', 'platform']
def load(f):
    t = open(f).read(); c = yaml.load(t[t.index('esphome:'):], Loader=L); out = {}
    for dom, v in c.items():
        if isinstance(v, list):
            for e in v:
                if isinstance(e, dict) and e.get('name'):
                    out[(dom, e['name'])] = {k: e.get(k) for k in KEYS} | {'_id': e.get('id')}
    return out, c
a, ca = load(sys.argv[1]); b, cb = load(sys.argv[2])
vis = lambda d: {k for k, v in d.items() if not v['internal']}
print('visible entities: before', len(vis(a)), 'after', len(vis(b)))
for k in sorted(vis(a) - vis(b)): print('MISSING ', k)
for k in sorted(vis(b) - vis(a)): print('NEW     ', k)
for k in sorted(vis(a) & vis(b)):
    d = {f: (a[k][f], b[k][f]) for f in KEYS if a[k][f] != b[k][f]}
    if d: print('CHANGED ', k, d)
for k in sorted(set(b) - vis(b)):
    if k not in a: print('internal new', k)
