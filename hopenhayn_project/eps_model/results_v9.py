"""All v9 results from one parameter file (default v9_best.json, else v8_best.json): baselines, the three
allocation experiments under both cap schedules, the cap-tilt family, quota size and welfare, the cap-use
histogram, EPS by size, where EPS workers go, and plant plans (small, median, top). Writes results_v9.json.

  python3 results_v9.py [params.json]
"""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

from calibrate_v9 import M, FIXED, start_params, moments
from moments_v9 import book
from eps_model import cap_2024
from run_eps import cap_2019
from run_v8 import build, summary, flat, NAMES, USE_EDGES

HERE = os.path.dirname(os.path.abspath(__file__))
PFILE = sys.argv[1] if len(sys.argv) > 1 else None
TILTS = [-1.0, -0.5, -0.25, 0.0, 0.15, 0.32, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
QUOTAS = [0.5, 0.75, 1.25, 1.5, 2.0]
H_BINS = [(0, 2), (2, 5), (5, 10), (10, 30), (30, 1e9)]


def params():
    if PFILE:
        d = json.load(open(PFILE))
        return dict({k: d[k] for k in NAMES}, **FIXED)
    return dict(start_params(), **FIXED)


def econ(regime, cap="2024", e0=None, scale=1.0, tilt=None):
    p = params()
    if tilt is not None:
        from v8_tilt import Tilt
        base = build(p, scale * M)
        mod = Tilt.__new__(Tilt)
        mod.__dict__.update(base.__dict__)
        mod._flat_cache, mod.S, mod.e0 = {}, tilt, e0
    else:
        mod = build(p, scale * M, cap=cap_2019 if cap == "2019" else cap_2024, e0=e0)
    r = mod.solve(regime)
    return mod, r


def welfare(mod, r, Mx):
    s = summary(r)
    return dict(welfare_korean=float(s["net_Y"] - s["w"] * Mx * mod.phi), welfare_total=float(s["net_Y"]))


def by_h(r):
    out = r["out"]
    mu, h, m = flat(out, "mu"), flat(out, "h"), flat(out, "m")
    return {f"{a:g}-{b:g}": float(mu[(h >= a) & (h < b)] @ m[(h >= a) & (h < b)] / max(mu @ m, 1e-300)) for a, b in H_BINS}


def job(j):
    kind, name, kw = j
    if kind == "exp":
        mod, r = econ(**kw)
        Mx = 0.0 if kw["regime"] == "none" else kw.get("scale", 1.0) * M
        d = dict(summary(r), **welfare(mod, r, Mx), by_h=by_h(r), book=book(mod, r, "current" if kw["regime"] == "current" else kw["regime"]))
        if kw["regime"] == "flat" and kw.get("tilt") is not None:
            d["A"] = float(r["out"]["x"])
        return name, d
    if kind == "hist":                      # cap-use histogram and size pattern, 2019 caps, plants with 1+ EPS worker
        mod, r = econ("current", cap="2019")
        out = r["out"]
        mu, h, k, m = flat(out, "mu"), flat(out, "h"), flat(out, "k"), flat(out, "m")
        u = m >= 1
        use = m[u] / mod.cap(h[u] + k[u])
        w = mu[u] / mu[u].sum()
        o = np.argsort(use)
        tot = h + k + m
        size = {}
        for a, b in [(0, 10), (10, 20), (20, 50), (50, 100), (100, 200), (200, 300)]:
            i = u & (tot >= a) & (tot < b)
            size[f"{a}-{b}"] = dict(share_of_users=float(mu[i].sum() / mu[u].sum()),
                                    eps_share=float(mu[i] @ (m[i] / tot[i]) / max(mu[i].sum(), 1e-300)))
        return name, dict(share=np.histogram(use, bins=USE_EDGES, weights=w)[0].tolist(), mean=float(w @ use),
                          median=float(use[o][np.searchsorted(np.cumsum(w[o]), 0.5)]), at_or_above_cap=float(w[use >= 1 - 1e-6].sum()),
                          size=size)
    if kind == "plans":                     # small (10th pct), median, top 1% eligible manual-intensive plants
        e0 = kw["e0"]
        mod, rc = econ("current")
        out = rc["out"]
        B = [b for b in out["blocks"] if b["type"] == 1 and b["eligible"]][0]
        o = np.argsort(mod.s)
        c = np.cumsum(B["mu"][o]) / B["mu"].sum()
        sg = [float(mod.s[o][np.searchsorted(c, q)]) for q in (0.10, 0.5, 0.99)]
        idx = [int(np.argmin(np.abs(mod.s - s))) for s in sg]
        res = dict(quantiles=[0.10, 0.5, 0.99], s=sg)
        for lab, reg, x, mm in [("today", "current", out["x"], mod)]:
            _, h, k, m, _, _ = mm.static_block(mm.blocks_def.index((1, True)), out["w"], x, reg)
            res[lab] = dict(h=h[idx].tolist(), k=k[idx].tolist(), m=m[idx].tolist())
        mp, rp = econ("neutral")
        _, h, k, m, _, _ = mp.static_block(mp.blocks_def.index((1, True)), rp["out"]["w"], rp["out"]["x"], "neutral")
        res["price"] = dict(h=h[idx].tolist(), k=k[idx].tolist(), m=m[idx].tolist())
        return name, res
    raise ValueError(kind)


if __name__ == "__main__":
    p = params()
    m24, r24 = econ("current")
    e0 = float(r24["out"]["x"])
    m19, r19 = econ("current", cap="2019")
    e19 = float(r19["out"]["x"])
    jobs = [("exp", "today_2024", dict(regime="current")), ("exp", "today_2019", dict(regime="current", cap="2019")),
            ("exp", "price", dict(regime="neutral")), ("exp", "equal_2024", dict(regime="flat", e0=e0)),
            ("exp", "equal_2019", dict(regime="flat", cap="2019", e0=e19)), ("exp", "no_eps", dict(regime="none")),
            ("hist", "hist_2019", {}), ("plans", "plans", dict(e0=e0))]
    jobs += [("exp", f"tilt_{s:+.2f}", dict(regime="flat", e0=e0, tilt=s)) for s in TILTS]
    jobs += [("exp", f"quota_x{q}", dict(regime="current", scale=q)) for q in QUOTAS]
    with Pool(8) as pool:
        out = dict(pool.map(job, jobs))
    mo = moments(p)
    base24, base19 = out["today_2024"], out["today_2019"]
    ch = lambda d, b, k: d[k] / b[k] - 1
    res = dict(params=p, e_2024=e0, e_2019=e19, quota_M=M, moments_2024=mo[2024], moments_2019={k: v for k, v in mo[2019].items()},
               runs=out,
               changes={
                   "price_vs_2024": {k: ch(out["price"], base24, k) for k in ("net_Y", "Y", "w", "firms", "welfare_korean", "welfare_total")},
                   "price_vs_2019": {k: ch(out["price"], base19, k) for k in ("net_Y", "Y")},
                   "equal_vs_2024": {k: ch(out["equal_2024"], base24, k) for k in ("net_Y", "Y", "welfare_korean")},
                   "equal_vs_2019": {k: ch(out["equal_2019"], base19, k) for k in ("net_Y", "Y")},
                   "no_eps_vs_2024": {k: ch(out["no_eps"], base24, k) for k in ("net_Y", "Y", "welfare_korean")},
                   "tilt": {s: {k: ch(out[f"tilt_{s:+.2f}"], base24, k) for k in ("net_Y", "Y", "welfare_korean")} for s in TILTS},
                   "quota": {q: {k: ch(out[f"quota_x{q}"], base24, k) for k in ("net_Y", "Y", "w", "welfare_korean")} for q in QUOTAS},
                   "price_premium_as_pay_vs_2024": (out["price"]["net_Y"] + out["price"]["cost_premium"]) / (base24["net_Y"] + base24["cost_premium"]) - 1,
               })
    json.dump(res, open(os.path.join(HERE, "results_v9.json"), "w"), indent=1, default=float)
    c = res["changes"]
    print(f"price {100 * c['price_vs_2024']['net_Y']:+.3f}% (2019 baseline {100 * c['price_vs_2019']['net_Y']:+.3f}%), as pay {100 * c['price_premium_as_pay_vs_2024']:+.3f}%")
    print(f"equal limit {100 * c['equal_vs_2024']['net_Y']:+.4f}% / {100 * c['equal_vs_2019']['net_Y']:+.4f}%;  no EPS {100 * c['no_eps_vs_2024']['net_Y']:+.2f}%")
    print("tilt", {s: round(100 * v["net_Y"], 4) for s, v in c["tilt"].items()})
    print("quota", {q: round(100 * v["net_Y"], 2) for q, v in c["quota"].items()})
    print("DONE")
