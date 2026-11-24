"""Cap-tilt experiment (Prof. Hur, Nov 24): replace the legal cap schedule by cap = A * n^S, n = h + k Korean
workers (eligible plants only, n < 300), for a range of tilts S. The same eligible plants as today (share e0 of
entrants); A adjusts so total EPS use equals the quota. S = 0 is the equal limit; S ~ 0.32 fits today's 2024
schedule (9.4 n^0.32); S = 1 is proportional to Korean workers; S < 0 gives small plants bigger caps.
Changes nothing in v8: the tilted cap is a subclass used only here. Writes v8_tilt.json.

The largest feasible m at each grid point is found on a grid of 401 fractions of manual work (the bisection in
eps_model_v8 needs a cap that rises with n, which fails for S < 0); the cap is smooth, so this is accurate to
0.25% of a plant's manual work.
"""
import json
import sys
from multiprocessing import Pool

import numpy as np

from eps_model_v8 import EPSModelV8, ELIG_MAX
from run_v8 import build, M, NAMES, summary, flat

P = {k: v for k, v in json.load(open("v8_best.json")).items() if k in NAMES}
NF = np.linspace(0.0, 1.0, 401)


def max_m_grid(H, L, capfun, chunk=8000):
    out = np.zeros_like(H)
    for a in range(0, len(H), chunk):
        h, l = H[a:a + chunk, None], L[a:a + chunk, None]
        m = l * NF[None, :]
        n = h + l - m
        ok = (m <= capfun(np.maximum(n, 1e-9))) & (n < ELIG_MAX) & (h >= 1)
        out[a:a + chunk] = np.where(ok, m, 0.0).max(1)
    return out


class Tilt(EPSModelV8):
    S = 0.0

    def _mcap(self, regime, x, eligible):
        if regime == "flat" and eligible:
            key = round(float(x), 10)
            if key not in self._flat_cache:
                if len(self._flat_cache) > 64:
                    self._flat_cache.clear()
                S = self.S
                self._flat_cache[key] = max_m_grid(self.H, self.Lab, lambda n: x * n ** S)
            return self._flat_cache[key]
        return super()._mcap(regime, x, eligible)


def make(S, e0):
    base = build(P, M)
    mod = Tilt.__new__(Tilt)
    mod.__dict__.update(base.__dict__)
    mod._flat_cache = {}
    mod.S, mod.e0 = S, e0
    return mod


def run(job):
    S, e0 = job
    r = make(S, e0).solve("flat")
    out = r["out"]
    mu, h, k, m = flat(out, "mu"), flat(out, "h"), flat(out, "k"), flat(out, "m")
    n = h + k
    u = m > 0
    cap = out["x"] * np.maximum(n, 1e-9) ** S
    d = summary(r)
    d.update(S=S, A=float(out["x"]), users_at_cap=float(mu[u & (m >= cap * (1 - 2e-3))].sum() / mu[u].sum()),
             cap_at_n={str(v): float(out["x"] * v ** S) for v in (1, 5, 10, 50, 100, 200)})
    return d


if __name__ == "__main__":
    base = build(P, M).solve("current")
    e0 = float(base["out"]["x"])
    grid = [float(s) for s in sys.argv[1:]] or [-1.0, -0.5, -0.25, 0.0, 0.15, 0.32, 0.5, 0.75, 1.0, 1.5]
    with Pool(5) as pool:
        res = pool.map(run, [(S, e0) for S in grid])
    b = summary(base)
    for d in res:
        d["net_change"] = d["net_Y"] / b["net_Y"] - 1
        d["gross_change"] = d["Y"] / b["Y"] - 1
        d["welfare_change"] = d["net_change"]          # households consume net output (no permit fee here)
    json.dump(dict(baseline=b, e0=e0, fit_today=dict(A=9.42, S=0.323), runs=res), open("v8_tilt.json", "w"), indent=1)
    for d in sorted(res, key=lambda d: d["S"]):
        print(f"S {d['S']:+.2f}  A {d['A']:8.3f}  cap at n=5/50/200: {d['cap_at_n']['5']:6.1f} {d['cap_at_n']['50']:6.1f} {d['cap_at_n']['200']:6.1f}"
              f"  net {100 * d['net_change']:+.4f}%  gross {100 * d['gross_change']:+.4f}%  users {100 * d['users']:.2f}%  at cap {100 * d['users_at_cap']:.1f}%  eq_err {d['eq_error']:.4f}", flush=True)
    print("DONE")
