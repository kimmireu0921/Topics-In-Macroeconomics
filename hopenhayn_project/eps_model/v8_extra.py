"""Extra v8 results for the Nov 24 slides (v8_best.json). Writes v8_extra.json:
  caps2019   today's rule, equal limit and price under the 2019 caps (changes against today, 2019)
  binding    share of EPS users at their legal cap, share of EPS workers at capped plants, mean cap use
  by_h       share of all EPS workers by core Koreans h, today (2024 caps) and with a price
  premium_as_pay  net output changes if the Korean premium is pay (a transfer), not a resource cost
"""
import json
from multiprocessing import Pool

from run_eps import cap_2019
from run_v8 import build, M, NAMES, summary, flat

p = json.load(open("v8_best.json"))
p = {k: p[k] for k in NAMES}
H_BINS = [(0, 2), (2, 5), (5, 10), (10, 30), (30, 1e9)]


def solve(job):
    reg, cap19, e0 = job
    mod = build(p, M, cap=cap_2019, e0=e0) if cap19 else build(p, M, e0=e0)
    r = mod.solve(reg)
    out = r["out"]
    mu, h, k, m = flat(out, "mu"), flat(out, "h"), flat(out, "k"), flat(out, "m")
    u = m > 0
    q = mod.cap(h + k)
    d = summary(r)
    if reg == "current":
        at = u & (m >= q * (1 - 1e-6))
        d["binding"] = dict(users_at_cap=float(mu[at].sum() / mu[u].sum()), eps_at_capped=float(mu[at] @ m[at] / (mu @ m)),
                            mean_use=float(mu[u] @ (m[u] / q[u]) / mu[u].sum()))
    d["by_h"] = {f"{a:g}-{b:g}": float(mu[(h >= a) & (h < b)] @ m[(h >= a) & (h < b)] / (mu @ m)) for a, b in H_BINS}
    return d


if __name__ == "__main__":
    c24 = solve(("current", False, None))
    c19 = solve(("current", True, None))
    with Pool(3) as pool:
        f19, pr, f24 = pool.map(solve, [("flat", True, c19["x"]), ("neutral", False, None), ("flat", False, c24["x"])])
    ch = lambda a, b: dict(net=a["net_Y"] / b["net_Y"] - 1, gross=a["Y"] / b["Y"] - 1,
                           net_premium_as_pay=(a["net_Y"] + a["cost_premium"]) / (b["net_Y"] + b["cost_premium"]) - 1)
    res = dict(binding_2024=c24["binding"], binding_2019=c19["binding"], by_h=dict(today=c24["by_h"], price=pr["by_h"]),
               caps2019=dict(equal_limit=dict(ch(f19, c19), L=f19["x"]), price=ch(pr, c19), e=c19["x"]),
               caps2024=dict(equal_limit=dict(ch(f24, c24), L=f24["x"]), price=ch(pr, c24), e=c24["x"]))
    json.dump(res, open("v8_extra.json", "w"), indent=1)
    print(json.dumps(res, indent=1))
