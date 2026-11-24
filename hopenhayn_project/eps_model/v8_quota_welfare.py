"""Quota size and welfare (Prof. Hur, Nov 24), v8_best.json, 2024 caps. Changes nothing in v8.

Quota: today's rule with the quota M scaled by 0.5 ... 2 (the eligible share e adjusts); no EPS for scale.
Welfare: households have linear utility, so welfare is consumption.
  - Korean households consume net output minus the wage bill of EPS workers (w per EPS worker; their income
    leaves the Korean household). Permit revenue in the price case is collected from plants and returned to
    Korean households, so it stays in.
  - Everyone, including EPS workers: net output (all income).
EPS workers make no consumption or saving decisions in the model; their welfare is only their wage income.
Writes v8_quota_welfare.json.
"""
import json
from multiprocessing import Pool

from run_v8 import build, M, NAMES, summary

P = {k: v for k, v in json.load(open("v8_best.json")).items() if k in NAMES}


def run(job):
    name, regime, scale, e0 = job
    mod = build(P, scale * M, e0=e0)
    r = mod.solve(regime)
    d = summary(r)
    Mx = 0.0 if regime == "none" else scale * M
    d.update(name=name, regime=regime, quota_scale=scale, M=Mx,
             eps_wage_bill=float(d["w"] * Mx * mod.phi),
             welfare_korean=float(d["net_Y"] - d["w"] * Mx * mod.phi),
             welfare_total=float(d["net_Y"]))
    return d


if __name__ == "__main__":
    base = build(P, M).solve("current")
    e0 = float(base["out"]["x"])
    jobs = [("today", "current", 1.0, e0), ("price", "neutral", 1.0, e0), ("equal limit", "flat", 1.0, e0), ("no EPS", "none", 1.0, e0)]
    jobs += [(f"quota x{s}", "current", s, e0) for s in (0.5, 0.75, 1.25, 1.5, 2.0)]
    with Pool(5) as pool:
        res = pool.map(run, jobs)
    b = next(d for d in res if d["name"] == "today")
    for d in res:
        for k in ("net_Y", "Y", "w", "firms", "welfare_korean", "welfare_total"):
            d[k + "_change"] = d[k] / b[k] - 1
    json.dump(res, open("v8_quota_welfare.json", "w"), indent=1)
    print(f"{'case':<14}{'e or x':>9}{'net Y':>10}{'gross Y':>10}{'wage':>9}{'plants':>9}{'Korean welfare':>16}{'total welfare':>15}{'eq err':>8}")
    for d in res:
        print(f"{d['name']:<14}{d['x']:>9.3f}{100 * d['net_Y_change']:>+9.2f}%{100 * d['Y_change']:>+9.2f}%{100 * d['w_change']:>+8.2f}%"
              f"{100 * d['firms_change']:>+8.2f}%{100 * d['welfare_korean_change']:>+15.2f}%{100 * d['welfare_total_change']:>+14.2f}%{d['eq_error']:>8.4f}", flush=True)
    print("DONE")
