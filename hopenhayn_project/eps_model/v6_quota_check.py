"""Check of the quota experiments: rerun at v6_best across quota levels, on both grids, and
confirm the labor and quota markets clear. Run from hopenhayn_project/eps_model."""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.getcwd())
from eps_model import cap_2024
from run_eps import M
from run_v5 import NAMES, build, summary

d = json.load(open("v6_best.json"))
P = {k: d[k] for k in NAMES}
MULTS = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]


def run(job):
    mult, grid = job
    reg = "none" if mult == 0 else "current"
    r = build(P, mult * M, cap=cap_2024, **grid).solve(reg)
    s = summary(r)
    out = r["out"]
    m_tot = sum(float(B["mu"] @ B["m"]) for B in out["blocks"]) if mult else 0.0
    n_tot = sum(float(B["mu"] @ (B["h"] + B["k"])) for B in out["blocks"])
    return dict(mult=mult, grid=grid, net_Y=s["net_Y"], Y=s["Y"], firms=s["firms"], users=s["users"], w=s["w"],
                theta=float(out["x"]), eq_error=s["eq_error"], m_tot=m_tot, M_target=mult * M, n_tot=n_tot)


if __name__ == "__main__":
    jobs = [(m, {}) for m in MULTS] + [(m, dict(nx=48, nz=21)) for m in (0.0, 0.5, 1.0, 1.5)]
    with Pool(8) as pool:
        out = pool.map(run, jobs, chunksize=1)
    for label, f in (("default grid", lambda x: not x["grid"]), ("finer grid", lambda x: bool(x["grid"]))):
        rows = [x for x in out if f(x)]
        base = next(x for x in rows if x["mult"] == 1.0)
        print(f"\n{label}\nquota  net vs current  gross vs current  firms     users   wage    theta   eq_error   EPS demand/quota  N")
        for x in rows:
            ratio = x["m_tot"] / x["M_target"] if x["M_target"] else float("nan")
            print(f"{x['mult']:>4.2f}  {100 * (x['net_Y'] / base['net_Y'] - 1):+8.3f}%  {100 * (x['Y'] / base['Y'] - 1):+8.3f}%  "
                  f"{x['firms']:.4f}  {x['users']:.4f}  {x['w']:.4f}  {x['theta']:.3f}  {x['eq_error']:.2e}  {ratio:.5f}  {x['n_tot']:.5f}")
        s = [(a["mult"], b["mult"], 100 * (b["net_Y"] - a["net_Y"]) / base["net_Y"] / (b["mult"] - a["mult"]) * 0.5)
             for a, b in zip(rows, rows[1:])]
        print("change in net output per 50% of quota, by step:", [(f"{a}-{b}", round(v, 3)) for a, b, v in s])
    json.dump(out, open(sys.argv[1], "w"), indent=1, default=float)
    print("DONE")
