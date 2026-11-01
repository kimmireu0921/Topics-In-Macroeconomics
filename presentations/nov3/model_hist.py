import json, sys, os
sys.path.insert(0, os.getcwd())
import numpy as np
from run_v5 import NAMES, build
from run_eps import cap_2019
d = json.load(open('v6_best.json')); p = {k: d[k] for k in NAMES}
r = build(p, cap=cap_2019, nx=48, nz=21).solve('current'); out = r['out']
cat = lambda key: np.concatenate([B[key] for B in out['blocks']])
mu, h, k, m = cat('mu'), cat('h'), cat('k'), cat('m')
u = m > 0; w = mu[u] / mu[u].sum(); n = (h + k)[u]; hu = h[u]
o = dict(by_korean=[float(w[(n >= i - .5) & (n < i + .5)].sum()) for i in range(1, 21)],
         by_core=[float(w[(hu >= i - .5) & (hu < i + .5)].sum()) for i in range(1, 21)],
         mean_korean=float(w @ n), mean_core=float(w @ hu), users=float(r['users']), theta=float(out['x']))
json.dump(o, open(sys.argv[1], 'w'))
print({k: ([round(x, 3) for x in v] if isinstance(v, list) else round(v, 3)) for k, v in o.items()})
