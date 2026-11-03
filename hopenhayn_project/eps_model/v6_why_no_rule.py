"""Where the no-size-rule change comes from at v6_best: costs by source, EPS by core size and
type, plants by type, permit rents. Run from hopenhayn_project/eps_model."""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.getcwd())
from run_eps import M
from run_v5 import NAMES, build, summary

d = json.load(open("v6_best.json"))
P = {k: d[k] for k in NAMES}
BINS = [(0, 5), (5, 10), (10, 30), (30, 50), (50, 100), (100, 300), (300, 1e9)]


def run(reg):
    mod = build(P, M)
    r = mod.solve(reg)
    s = summary(r)
    out = r["out"]
    res = dict(reg=reg, net_Y=s["net_Y"], Y=s["Y"], w=out["w"], x=out["x"], Me=out["Me"], types=[], bins=[])
    Y = rc = cf = cmc = prem = 0.0
    allb = []
    for t, B in enumerate(out["blocks"]):
        T = mod.types[t]
        mu = B["mu"]
        tot = mu.sum()
        users = mu[B["m"] > 0].sum()
        y_t = mu @ B["y"]
        res["types"].append(dict(lam=T["lam"], cf=T["cf"], plants=float(tot), users=float(users), output=float(y_t),
                                 eps=float(mu @ B["m"]), korean_core=float(mu @ B["h"]), korean_manual=float(mu @ B["k"]),
                                 avg_size=float(mu @ (B["h"] + B["k"] + B["m"]) / tot)))
        Y += y_t
        rc += mu @ B["rc"]
        cf += tot * T["cf"]
        cmc += mod.cm * users
        allb.append((mu, B["h"], B["k"], B["m"], B["y"]))
    res.update(Y_check=float(Y), rc=float(rc), recruit_premium=float(rc - cmc), eps_fixed=float(cmc), fixed=float(cf),
               entry=float(mod.ce * out["Me"]), permit_revenue=float(out["x"] * M) if reg == "neutral" else 0.0)
    res["net_check"] = res["Y_check"] - res["rc"] - res["fixed"] - res["entry"]
    mu, h, k, m, y = (np.concatenate(c) for c in zip(*allb))
    for a, b in BINS:
        i = (h >= a) & (h < b)
        res["bins"].append(dict(core=f"{a}-{b}", plants=float(mu[i].sum()), users=float(mu[i & (m > 0)].sum()),
                                eps=float(mu[i] @ m[i]), output=float(mu[i] @ y[i])))
    return res


if __name__ == "__main__":
    with Pool(2) as pool:
        a, b = pool.map(run, ["current", "neutral"])
    json.dump([a, b], open(sys.argv[1], "w"), indent=1, default=float)
    print("w", round(a["w"], 4), round(b["w"], 4), "theta", round(a["x"], 3), "p", round(b["x"], 3), "Me", round(a["Me"], 5), round(b["Me"], 5))
    psi, xi = P["psi"], P["xi"]
    print("core Koreans above which Korean manual is cheaper than EPS at p:", round((b["x"] / (b["w"] * psi)) ** (-1 / xi) - 1, 1))
    for k in ("Y_check", "net_check", "net_Y", "rc", "recruit_premium", "eps_fixed", "fixed", "entry", "permit_revenue"):
        print(f"{k:<16} {a[k]:.4f} {b[k]:.4f}  diff {b[k] - a[k]:+.4f}  index(Y=100) {100 * a[k] / a['Y']:.2f} -> {100 * b[k] / a['Y']:.2f}")
    for x, y in zip(a["types"], b["types"]):
        print("type lam", round(x["lam"], 3), {k: (round(x[k], 4), round(y[k], 4)) for k in ("plants", "users", "output", "eps", "korean_core", "korean_manual", "avg_size")})
    print("core bin | plants | users | share of EPS | share of output (current, then no rule)")
    Ma, Mb = sum(r["eps"] for r in a["bins"]), sum(r["eps"] for r in b["bins"])
    for x, y in zip(a["bins"], b["bins"]):
        print(f"{x['core']:<14} plants {x['plants']:.4f} {y['plants']:.4f}  users {x['users']:.4f} {y['users']:.4f}  "
              f"EPS {x['eps'] / Ma:.3f} {y['eps'] / Mb:.3f}  output {x['output'] / a['Y']:.3f} {y['output'] / b['Y']:.3f}")
    print("DONE")
