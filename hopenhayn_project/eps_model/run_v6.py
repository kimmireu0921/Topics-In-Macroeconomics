"""
EPS model v5 recalibrated with the Lee-Peri-Yang targets measured their way ("v6"
results). The model (eps_model_v5.py) is unchanged; v5 files are left in place.

Three moments change, all computed under the 2019 caps (their survey: 2019-21):
  eps_share_users  simple average of the EPS share across EPS firms, 0.369 (Table 3).
                   v5 used an employment-weighted share against 0.37.
  users_size       average total workers at EPS firms, 20.78 (Table 3). v5 used 13
                   against the model's total workers, under the 2024 caps.
  slope_lpy        closure slope on statutory exposure with size controls: average of
                   the size-bin and cubic specifications, 0.152 (Table 6, cols 4-5).
                   v5 used no size control against 0.15.

  python3 run_v6.py time [params.json]         # one evaluation, with timing
  python3 run_v6.py calib 120 150              # local search + Nelder-Mead from v5 (writes v6_best.json)
  python3 run_v6.py results                    # experiments + bunching (writes v6_results.json)
  python3 run_v6.py fine                       # current vs. no size rule, finer grid (writes v6_results_fine.json)
"""
import json
import sys
import time

import numpy as np
from scipy.optimize import minimize

from eps_model import cap_2024
from run_eps import cap_2019, M, SHOCK_YEARS
from run_v5 import BOUNDS, NAMES, build, bunching, summary

T = dict(avg_size=7.5, share_small=0.70, exit_rate=0.08, users=0.10, eps_share_users=0.369,
         users_size=20.78, slope_lpy=0.152, share_50plus=0.021)
A2_BINS = [(0, 10), (10, 20), (20, 50), (50, 100), (100, 200), (200, 300), (300, np.inf)]
A2_DATA = [0.41, 0.26, 0.25, 0.04, 0.02, 0.01, 0.0]          # Lee-Peri-Yang Table A2
KOREAN_BINS = [10, 30, 50, 100, 150, 200]                    # their size-bin controls


def lpy_design(mod, res, kappa=0.2, periods=SHOCK_YEARS):
    """Lee-Peri-Yang's sample and regressions in the model: EPS firms only, weighted
    by plant mass. Extra closure and the EPS drop (share of employment) are regressed
    on statutory exposure q/(n+q), with size-bin dummies (Koreans) or a cubic in total
    workers. Closure as in EPSModel.closure_response."""
    out = res["out"]
    disc = mod.beta * (1 - mod.delta)
    rows = []
    for t, B in enumerate(out["blocks"]):
        pi_sh, *_ = mod.static(t, out["w"], out["x"], "current", m_limit_by_s=(1 - kappa) * B["m"] + 1e-12)
        Vsh = B["V"]
        for _ in range(periods):
            Vsh, _ = mod._bellman(pi_sh, Vsh)
        p_sh = 1.0 / (1.0 + np.exp(-(disc * mod.P @ Vsh) / mod.sig_e))
        u = B["m"] > 0
        rows.append((B["mu"][u], (B["h"] + B["k"])[u], B["m"][u], (1 - mod.delta) * (B["stay"] - p_sh)[u]))
    wgt, n, m, extra = (np.concatenate(c) for c in zip(*rows))
    wgt = wgt / wgt.sum()
    tot, share = n + m, m / (n + m)
    q = mod.cap(n)
    exposure = q / (n + q)
    bins = np.eye(len(KOREAN_BINS) + 1)[np.digitize(n, KOREAN_BINS, right=True)]
    bins = bins[:, bins.sum(0) > 0]
    z = (tot - wgt @ tot) / np.sqrt(wgt @ (tot - wgt @ tot) ** 2)
    cubic = np.column_stack([np.ones_like(z), z, z ** 2, z ** 3])

    def coef(y, controls):
        X = np.column_stack([exposure, controls])
        return float(np.linalg.lstsq(X * np.sqrt(wgt)[:, None], y * np.sqrt(wgt), rcond=None)[0][0])

    mean_share = float(wgt @ share)
    return dict(mean_share=mean_share, sd_share=float(np.sqrt(wgt @ (share - mean_share) ** 2)),
                workers=float(wgt @ tot), koreans=float(wgt @ n), weighted_share=float((wgt @ m) / (wgt @ tot)),
                slope_bins=coef(extra, bins), slope_cubic=coef(extra, cubic),
                first_stage_bins=coef(kappa * share, bins), first_stage_cubic=coef(kappa * share, cubic),
                mean_drop=float(wgt @ (kappa * share)), use_of_cap=float(wgt @ (m / q)),
                size_bins=[float(wgt[(tot >= a) & (tot < b)].sum()) for a, b in A2_BINS])


def moments(p, **grid):
    r = build(p, **grid).solve("current")               # 2024 caps: census-based moments
    mod19 = build(p, cap=cap_2019, **grid)
    r19 = mod19.solve("current")                        # 2019 caps: their survey and the shock
    lp = lpy_design(mod19, r19)
    r["lpy"] = lp
    r["eps_share_users"], r["users_size"] = lp["mean_share"], lp["workers"]
    r["slope_lpy"] = (lp["slope_bins"] + lp["slope_cubic"]) / 2
    r["eq_error"] = max(r["eq_error"], r19["eq_error"])
    r["type_share"] = [min(a, b) for a, b in zip(r["type_share"], r19["type_share"])]
    r["theta_2019"] = float(r19["out"]["x"])
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


if __name__ == "__main__" and sys.argv[1] == "time":
    d = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "v5_best.json"))
    p = {k: d[k] for k in NAMES}
    t0 = time.time()
    L, r = safe(p)
    print(f"loss {L:.4f} | {show(r) if r else 'failed'} | {time.time() - t0:.1f}s", flush=True)
    if r:
        print(json.dumps(dict(r["lpy"], theta_2019=r["theta_2019"], a2_data=A2_DATA), indent=1), flush=True)

if __name__ == "__main__" and sys.argv[1] == "calib":
    # Start from v5_best.json (or v6_best.json if it exists). Same search as run_v5.py.
    from multiprocessing import Pool
    d = json.load(open("v5_best.json"))
    try:
        d = json.load(open("v6_best.json"))
    except FileNotFoundError:
        pass
    best = {k: d[k] for k in NAMES}
    rng = np.random.default_rng(11)
    best_L, r = safe(best)
    print(f"start loss {best_L:.4f} | {show(r) if r else ''}", flush=True)
    step, stall = 0.2, 0
    with Pool(8) as pool:
        for i in range(int(sys.argv[2]) if len(sys.argv) > 2 else 120):
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
                json.dump(dict(loss=best_L, **best), open("v6_best.json", "w"), indent=1)
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
            json.dump(dict(loss=L, **p), open("v6_best.json", "w"), indent=1)
            print(f"nm: loss {L:.4f} | {show(r)}", flush=True)
        return L
    obj.best = best_L
    print("== local search done; Nelder-Mead", flush=True)
    minimize(obj, [best[k] for k in NAMES], method="Nelder-Mead",
             options=dict(maxiter=int(sys.argv[3]) if len(sys.argv) > 3 else 150, adaptive=True,
                          xatol=1e-4, fatol=1e-5))
    print("DONE", flush=True)

if __name__ == "__main__" and sys.argv[1] == "results":
    d = json.load(open("v6_best.json"))
    p = {k: d[k] for k in NAMES}
    r = moments(p)
    res = dict(params=p, loss=loss(r), targets=T, fit={k: float(r[k]) for k in T}, lpy=r["lpy"],
               theta_2019=r["theta_2019"], a2_data=A2_DATA, experiments={})
    for name, reg, Mx, cap in [("no EPS", "none", 0.0, cap_2024), ("current rule", "current", M, cap_2024),
                               ("size-neutral, same quota (by price)", "neutral", M, cap_2024),
                               ("current rule, quota +50%", "current", 1.5 * M, cap_2024),
                               ("current rule, quota -50%", "current", 0.5 * M, cap_2024),
                               ("2019 caps, same quota", "current", M, cap_2019)]:
        ri = build(p, Mx, cap=cap).solve(reg)
        res["experiments"][name] = dict(summary(ri), bunching=bunching(ri))
    base = res["experiments"]["current rule"]["net_Y"]
    res["net_Y_change_vs_current"] = {k: v["net_Y"] / base - 1 for k, v in res["experiments"].items()}
    json.dump(res, open("v6_results.json", "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("loss", "fit", "lpy", "theta_2019", "net_Y_change_vs_current")}, indent=1))
    print(json.dumps(res["experiments"]["current rule"]["bunching"]["steps"], indent=1))
    print("DONE", flush=True)

if __name__ == "__main__" and sys.argv[1] == "fine":
    d = json.load(open("v6_best.json"))
    p = {k: d[k] for k in NAMES}
    res = dict(params=p, grid=dict(nx=48, nz=21), experiments={})
    for name, reg in [("current rule", "current"), ("size-neutral, same quota (by price)", "neutral")]:
        ri = build(p, nx=48, nz=21).solve(reg)
        res["experiments"][name] = dict(summary(ri), bunching=bunching(ri))
    a, b = (res["experiments"][k]["net_Y"] for k in res["experiments"])
    res["net_Y_change_neutral"] = b / a - 1
    r = moments(p, nx=48, nz=21)
    res["fit"], res["lpy"] = {k: float(r[k]) for k in T}, r["lpy"]
    json.dump(res, open("v6_results_fine.json", "w"), indent=1)
    print(f"no size rule vs current: {100 * res['net_Y_change_neutral']:+.2f}%", flush=True)
    print(json.dumps(dict(res["fit"], **res["lpy"]), indent=1), flush=True)
