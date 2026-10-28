"""
EPS model v5 (Pareto tail, bunching-ready size grid): calibration, experiments and
the bunching check. v4 (run_eps.py, recal_best.json) is left unchanged.

Parameters: as in v4, with the Pareto tail gamma replacing nu_top.
Targets: the seven v4 targets plus the share of plants with 50 or more workers
(2.1%, MDIS census 2024), which v4 missed (0.5%).

  python3 run_v5.py time                       # one evaluation, with timing
  python3 run_v5.py calib 200                  # local search + Nelder-Mead from v4 (writes v5_best.json)
  python3 run_v5.py results                    # experiments + bunching (writes v5_results.json)
  python3 run_v5.py fine                       # current vs. no size rule with 4x the productivity
                                               # levels, for the histogram (writes v5_results_fine.json)
"""
import json
import sys
import time

import numpy as np
from scipy.optimize import minimize

from eps_model import cap_2024
from eps_model_v5 import EPSModelV5, STEPS
from run_eps import cap_2019, FIRM, N, M, SHOCK_YEARS, SIG_E

T = dict(avg_size=7.5, share_small=0.70, exit_rate=0.08, users=0.10, eps_share_users=0.37,
         users_size=13.0, slope_lpy=0.15, share_50plus=0.021)
NAMES = ["rho", "cm", "psi", "xi", "lamA", "cfA", "lamB", "cfB", "shB", "sigma_s", "gamma", "ce", "delta"]
BOUNDS = dict(rho=(-1.5, 0.8), cm=(0.01, 3), psi=(0.5, 10), xi=(0.1, 1.5), lamA=(0.005, 0.5),
              cfA=(0.1, 2.5), lamB=(0.3, 4), cfB=(0.5, 15), shB=(0.05, 0.6),
              sigma_s=(0.05, 0.5), gamma=(1.5, 8), ce=(0.3, 30), delta=(0.003, 0.05))


def build(p, M_=M, cap=cap_2024, **grid):
    types = [dict(lam=p["lamA"], cf=p["cfA"], share=1 - p["shB"]),
             dict(lam=p["lamB"], cf=p["cfB"], share=p["shB"])]
    return EPSModelV5(types, N=N, M=M_, rho=p["rho"], cm=p["cm"], psi=p["psi"], xi=p["xi"],
                      sig_e=SIG_E, cap=cap, alpha=FIRM["alpha"], rho_s=FIRM["rho_s"],
                      sigma_s=p["sigma_s"], gamma=p["gamma"], ce=p["ce"], delta=p["delta"], **grid)


def moments(p):
    r = build(p).solve("current")                       # 2024 caps: today's moments
    mod19 = build(p, cap=cap_2019)
    r19 = mod19.solve("current")                        # 2019 caps: Jan 2020 and the 2020-21 shock
    c = mod19.closure_response(r19, periods=SHOCK_YEARS)
    r["eps_share_users"] = r19["eps_share_users"]
    r["slope_lpy"], r["slope"] = c["slope_lpy"], c["slope"]
    r["eq_error"] = max(r["eq_error"], r19["eq_error"])
    r["type_share"] = [min(a, b) for a, b in zip(r["type_share"], r19["type_share"])]
    return r


def loss(r):
    if r.get("eq_error", 1) > 0.05 or not np.isfinite(r["avg_size"]) or min(r["type_share"]) < 0.03:
        return 50.0
    return sum(((r[k] - v) / v) ** 2 for k, v in T.items())


def safe(p):
    if abs(p["rho"]) < 0.02:
        p = dict(p, rho=0.02)
    try:
        r = moments(p)
        return loss(r), r
    except Exception:
        return 50.0, None


def show(r):
    return " ".join(f"{k} {r[k]:.3f}" for k in T)


def bunching(r):
    """Plant mass by Korean core workers h around each cap step: just below (h in
    [0.9t, t]) vs at or just past it (h in (t, 1.1t]), per worker of width, and
    the mass sitting exactly on the step points the grid adds."""
    out = r["out"]
    cat = lambda key: np.concatenate([B[key] for B in out["blocks"]])
    mu, h = cat("mu"), cat("h")
    mu = mu / mu.sum()
    rows = {}
    for t in list(STEPS) + [300]:
        below = mu[(h >= 0.9 * t) & (h <= t * (1 - 1e-7))].sum() / (0.1 * t)
        above = mu[(h > t * (1 - 1e-7)) & (h <= 1.1 * t)].sum() / (0.1 * t)
        at = mu[np.isclose(h, t * (1 + 1e-6), rtol=1e-9) | np.isclose(h, t, rtol=1e-9)
                | np.isclose(h, t * (1 - 1e-6), rtol=1e-9)].sum()
        rows[t] = dict(density_below=float(below), density_above=float(above), mass_on_step=float(at))
    # bins about 8% wide, with every cap step as an edge (a plant on step t sits in [t, ...))
    knots = [20, 30, 50, 100, 150, 200, 300, 400]
    edges = np.unique(np.concatenate([np.geomspace(a, b, max(int(round(np.log(b / a) / 0.08)), 1) + 1)
                                      for a, b in zip(knots[:-1], knots[1:])]))
    for t in STEPS:                                  # plants exactly on t fall left, those just past it right
        edges[np.isclose(edges, t)] = t * (1 + 5e-7)
    edges[np.isclose(edges, 300)] = 300 * (1 - 5e-7)  # plants just under 300 fall left
    hist = np.histogram(h, bins=edges, weights=mu)[0]
    return dict(steps=rows, hist_edges=edges.tolist(), hist=hist.tolist(),
                share_h_ge_100=float(mu[h >= 100].sum()), max_h=float(h[mu > 1e-7].max()))


def summary(r):
    keys = ["net_Y", "Y", "firms", "avg_size", "share_small", "share_50plus", "exit_rate",
            "endo_exit_share", "users", "eps_share_users", "users_size", "eps_share", "w", "x", "eq_error"]
    d = {k: float(r[k]) for k in keys}
    d["type_share"] = [float(v) for v in r["type_share"]]
    return d


if __name__ == "__main__" and sys.argv[1] == "time":
    d = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "recal_best.json"))
    p = {k: d.get(k, 3.0) for k in NAMES}
    t0 = time.time()
    L, r = safe(p)
    print(f"loss {L:.4f} | {show(r) if r else 'failed'} | {time.time() - t0:.1f}s", flush=True)

if __name__ == "__main__" and sys.argv[1] == "calib":
    # Start: v4 calibration with gamma = 5, sigma_s = 0.08, cfA = 0.4 (best point of a
    # coarse scan), or v5_best.json if it exists. Parallel local search (8 candidates
    # per round, step shrinks after 6 rounds without improvement), then Nelder-Mead.
    from multiprocessing import Pool
    d = json.load(open("recal_best.json"))
    best = dict({k: d.get(k, 3.0) for k in NAMES}, gamma=5.0, sigma_s=0.08, cfA=0.4)
    try:
        best.update({k: v for k, v in json.load(open("v5_best.json")).items() if k in NAMES})
    except FileNotFoundError:
        pass
    rng = np.random.default_rng(7)
    best_L, r = safe(best)
    print(f"start loss {best_L:.4f} | {show(r) if r else ''}", flush=True)
    step, stall = 0.2, 0
    with Pool(8) as pool:
        for i in range(int(sys.argv[2]) if len(sys.argv) > 2 else 100):
            cands = []
            for _ in range(8):
                cand = {}
                for k in NAMES:
                    lo, hi = BOUNDS[k]
                    v = best[k] * np.exp(rng.normal(0, step)) if best[k] > 0 else best[k] + rng.normal(0, step / 2)
                    cand[k] = float(min(max(v, lo), hi))
                cands.append(cand)
            res = pool.map(safe, cands)
            j = int(np.argmin([L for L, _ in res]))
            if res[j][0] < best_L:
                best_L, best, stall = res[j][0], cands[j], 0
                print(f"round {i} (step {step:.3f}): loss {best_L:.4f} | {show(res[j][1])}", flush=True)
                json.dump(dict(loss=best_L, **best), open("v5_best.json", "w"), indent=1)
            else:
                stall += 1
                if stall >= 6:
                    step, stall = max(step / 2, 0.02), 0

    def obj(x):
        p = dict(zip(NAMES, x))
        if any(not (BOUNDS[k][0] <= p[k] <= BOUNDS[k][1]) for k in NAMES):
            return 50.0
        L, r = safe(p)
        if L < obj.best:
            obj.best = L
            json.dump(dict(loss=L, **p), open("v5_best.json", "w"), indent=1)
            print(f"nm: loss {L:.4f} | {show(r)}", flush=True)
        return L
    obj.best = best_L
    print("== local search done; Nelder-Mead", flush=True)
    minimize(obj, [best[k] for k in NAMES], method="Nelder-Mead",
             options=dict(maxiter=int(sys.argv[3]) if len(sys.argv) > 3 else 400, adaptive=True,
                          xatol=1e-4, fatol=1e-5))
    print("DONE", flush=True)

if __name__ == "__main__" and sys.argv[1] == "results":
    d = json.load(open("v5_best.json"))
    p = {k: d[k] for k in NAMES}
    r = moments(p)
    res = dict(params=p, loss=loss(r), targets=T, fit={k: float(r[k]) for k in T}, experiments={})
    for name, reg, Mx, cap in [("no EPS", "none", 0.0, cap_2024), ("current rule", "current", M, cap_2024),
                               ("size-neutral, same quota (by price)", "neutral", M, cap_2024),
                               ("current rule, quota +50%", "current", 1.5 * M, cap_2024),
                               ("current rule, quota -50%", "current", 0.5 * M, cap_2024),
                               ("2019 caps, same quota", "current", M, cap_2019)]:
        ri = build(p, Mx, cap=cap).solve(reg)
        res["experiments"][name] = dict(summary(ri), bunching=bunching(ri))
        print(name, {k: round(v, 4) for k, v in summary(ri).items() if k != "type_share"}, flush=True)
    base = res["experiments"]["current rule"]["net_Y"]
    res["net_Y_change_vs_current"] = {k: v["net_Y"] / base - 1 for k, v in res["experiments"].items()}
    json.dump(res, open("v5_results.json", "w"), indent=1)
    print(json.dumps(res["net_Y_change_vs_current"], indent=1))
    print(json.dumps(res["experiments"]["current rule"]["bunching"]["steps"], indent=1))
    print("DONE", flush=True)

if __name__ == "__main__" and sys.argv[1] == "fine":
    d = json.load(open("v5_best.json"))
    p = {k: d[k] for k in NAMES}
    res = dict(params=p, grid=dict(nx=48, nz=21), experiments={})
    for name, reg in [("current rule", "current"), ("size-neutral, same quota (by price)", "neutral")]:
        ri = build(p, nx=48, nz=21).solve(reg)
        res["experiments"][name] = dict(summary(ri), bunching=bunching(ri))
    a, b = (res["experiments"][k]["net_Y"] for k in res["experiments"])
    res["net_Y_change_neutral"] = b / a - 1
    json.dump(res, open("v5_results_fine.json", "w"), indent=1)
    print(f"no size rule vs current: {100 * res['net_Y_change_neutral']:+.2f}%", flush=True)
