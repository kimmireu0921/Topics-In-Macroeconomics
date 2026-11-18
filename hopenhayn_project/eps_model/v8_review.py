"""Diagnostics for the review of v8 (Nov 18). Changes nothing in v8: every run starts from
v8_best.json and varies one thing. Writes v8_review.json.

  closure   who is near the exit margin under the 2019 caps, users against non-users; how much a
            two-year 20% cut lowers users' profits; the closure slope when one parameter moves
  premium   moments and the price gain when psi moves, other parameters fixed (not recalibrated)
  gross     why gross output rises with a price: plants, EPS use and output by type and eligibility
"""
import json
from multiprocessing import Pool

import numpy as np

from run_eps import cap_2019, SHOCK_YEARS
from run_v8 import build, M, NAMES, T, lpy_design, moments, flat

P0 = json.load(open("v8_best.json"))
P0 = {k: P0[k] for k in NAMES}


def margin(p):
    """Under the 2019 caps: Pr(stay) and the shock's effect for users and non-users of EPS."""
    mod = build(p, M, cap=cap_2019)
    r = mod.solve("current")
    out = r["out"]
    disc = mod.beta * (1 - mod.delta)
    rows = {}
    for B in out["blocks"]:
        name = f"{'manual' if B['type'] else 'light'}_{'eligible' if B['eligible'] else 'not'}"
        u = B["m"] > 0
        pi_sh, *_ = mod.static_block(B["block"], out["w"], out["x"], "current", m_limit_by_s=0.8 * B["m"] + 1e-12)
        Vsh = B["V"]
        for _ in range(SHOCK_YEARS):
            Vsh, _ = mod._bellman(pi_sh, Vsh)
        p_sh = 1 / (1 + np.exp(-(disc * mod.P @ Vsh) / mod.sig_e))
        extra = (1 - mod.delta) * (B["stay"] - p_sh)
        for lab, sel in (("users", u), ("nonusers", ~u)):
            w = B["mu"][sel]
            if w.sum() <= 0:
                continue
            w = w / w.sum()
            rows[f"{name}_{lab}"] = dict(
                mass=float(B["mu"][sel].sum()), endogenous_exit=float(w @ ((1 - mod.delta) * (1 - B["stay"][sel]))),
                near_margin=float(w[(B["stay"][sel] < 0.99)].sum()), extra_closure=float(w @ extra[sel]),
                profit_loss=float(w @ ((B["pi"] - pi_sh)[sel] / np.maximum(np.abs(B["pi"][sel]), 1e-9))),
                min_s=float(mod.s[sel][B["mu"][sel] > 1e-9].min()) if (B["mu"][sel] > 1e-9).any() else None)
    # productivity below which plants close for sure, and the lowest productivity that uses EPS
    return rows


def run(job):
    name, change = job
    p = dict(P0, **change)
    r = moments(p)
    d = dict(name=name, change=change, fit={k: float(r[k]) for k in T}, slope=float(r["slope_lpy"]),
             at_cap_2019=float(r["lpy"]["at_cap"]), e=float(r["e_2024"]))
    if name.startswith("psi") or name == "base":
        cur = r
        pr = build(p, M).solve("neutral")
        d["price_net"] = float(pr["net_Y"] / cur["net_Y"] - 1)
        d["price_net_premium_as_pay"] = float((pr["net_Y"] + pr["cost_premium"]) / (cur["net_Y"] + cur["cost_premium"]) - 1)
        d["price_gross"] = float(pr["Y"] / cur["Y"] - 1)
        d["premium_cost_share"] = float(cur["cost_premium"] / cur["Y"])
    return d


def by_group(reg):
    mod = build(P0, M)
    r = mod.solve(reg)
    out = r["out"]
    g = {}
    for B in out["blocks"]:
        key = "light" if B["type"] == 0 else "manual"
        d = g.setdefault(key, dict(plants=0.0, users=0.0, eps=0.0, Y=0.0, workers=0.0, korean_manual=0.0))
        d["plants"] += float(B["mu"].sum()); d["users"] += float(B["mu"][B["m"] > 0].sum())
        d["eps"] += float(B["mu"] @ B["m"]); d["Y"] += float(B["mu"] @ B["y"])
        d["workers"] += float(B["mu"] @ (B["h"] + B["k"] + B["m"])); d["korean_manual"] += float(B["mu"] @ B["k"])
    return reg, dict(groups=g, w=float(out["w"]), Y=float(r["Y"]), net_Y=float(r["net_Y"]), firms=float(r["firms"]),
                     cost_premium=float(r["cost_premium"]), cost_eps_fixed=float(r["cost_eps_fixed"]),
                     cost_fixed=float(r["cost_fixed"]), cost_entry=float(r["cost_entry"]))


if __name__ == "__main__":
    jobs = [("base", {}), ("cm x0.5", dict(cm=0.5 * P0["cm"])), ("cm x0.25", dict(cm=0.25 * P0["cm"])),
            ("sigma_s x2", dict(sigma_s=2 * P0["sigma_s"])), ("psi = 0.92 (v6)", dict(psi=0.915)),
            ("psi x0.8", dict(psi=0.8 * P0["psi"])), ("psi x1.2", dict(psi=1.2 * P0["psi"]))]
    with Pool(8) as pool:
        sens = pool.map(run, jobs)
        mg = pool.map(margin, [P0, dict(P0, cm=0.25 * P0["cm"])])
        grp = dict(pool.map(by_group, ["current", "neutral"]))
    res = dict(sensitivity=sens, margin_base=mg[0], margin_cm_quarter=mg[1], gross=grp)
    json.dump(res, open("v8_review.json", "w"), indent=1)
    for d in sens:
        print(d["name"], "slope", round(d["slope"], 3), "fit", {k: round(v, 3) for k, v in d["fit"].items()},
              {k: round(d[k], 4) for k in ("price_net", "price_net_premium_as_pay", "price_gross", "premium_cost_share") if k in d})
    for k, v in mg[0].items():
        print("base", k, {a: (round(b, 4) if isinstance(b, float) else b) for a, b in v.items()})
    for k, v in mg[1].items():
        print("cm/4", k, {a: (round(b, 4) if isinstance(b, float) else b) for a, b in v.items()})
    print(json.dumps(grp, indent=1))
