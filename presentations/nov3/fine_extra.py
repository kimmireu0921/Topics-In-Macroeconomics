import json, sys, os
sys.path.insert(0, os.getcwd())
import numpy as np
from multiprocessing import Pool
from run_v5 import NAMES, build
from run_eps import cap_2019, M
d = json.load(open('v6_best.json')); p = {k: d[k] for k in NAMES}
def quota(mult):
    return float(build(p, mult * M, nx=48, nz=21).solve('current')['net_Y'])
def hist(_):
    r = build(p, cap=cap_2019, nx=48, nz=21).solve('current'); out = r['out']
    cat = lambda key: np.concatenate([B[key] for B in out['blocks']])
    mu, h, k, m = cat('mu'), cat('h'), cat('k'), cat('m')
    u = m > 0; w = mu[u] / mu[u].sum(); n = (h + k)[u]
    # a worker count i has the same cap as any n in (i-1, i], so a plant just past a step falls in the next count
    c = np.ceil(n - 1e-9)
    return dict(by_korean=[float(w[c == i].sum()) for i in range(1, 21)], above_20=float(w[c > 20].sum()), mean_korean=float(w @ n))
if __name__ == '__main__':
    with Pool(3) as pool:
        a = pool.apply_async(quota, (1.0,)); b = pool.apply_async(quota, (1.5,)); c = pool.apply_async(hist, (0,))
        base, up, h = a.get(), b.get(), c.get()
    o = dict(base=base, up=up, up_change=up / base - 1, **h)
    json.dump(o, open(sys.argv[1], 'w'))
    print({k: ([round(x, 3) for x in v] if isinstance(v, list) else round(v, 4)) for k, v in o.items()})
