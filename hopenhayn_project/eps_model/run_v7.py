"""
EPS model v5 recalibrated to sourced targets ("v7"). Same model and code as run_v6.py;
only the targets and the quota change. Every number below has a source (checked Nov 10, 2026).

Changed from v6 (v6 used figures with no source, written into the first model on Oct 15):
  avg_size      8.14   (v6: 7.5)   MDIS 전국사업체조사 2024, all 509,467 manufacturing plants;
                                   masked headcounts (*, **, ...) imputed at the mean of the same
                                   digit band among unmasked plants. v6 used unmasked plants <= 1,000.
  share_small   0.713  (v6: 0.70)  same file, plants with 1-4 workers
  exit_rate     0.066  (v6: 0.08, an assumption)  국가데이터처, 2025년 기업생멸행정통계(잠정),
                                   2026-10-22, Table 4: manufacturing 소멸률 6.6% in 2024 (p),
                                   6.8% in 2023. Enterprises, not plants.
  users         0.080  (v6: 0.10, no source)  workplaces employing E-9 workers in
                                   manufacturing, end of 2024: 38,981 E-9 only + 1,785 E-9 and H-2
                                   = 40,766 (e-나라지표 1501 고용허가제 고용동향, 고용노동부 /
                                   한국고용정보원, table 150106), over 509,467 census plants
  M             EPS = 5.29% of manufacturing workers (v6: 5.5%, no source): 219,507 E-9 workers
                                   in manufacturing, end of 2024 (e-나라지표 1501, table 150107),
                                   over 4,147,204 manufacturing workers (MDIS census 2024, imputed as above)
Unchanged, checked: eps_share_users 0.369 and users_size 20.78 (Lee, Peri and Yang 2026,
Table 3, p. 14); slope_lpy 0.152 (Table 6, cols 4-5: 0.154 and 0.150, p. 23); share_50plus
0.021 (census 2024: 0.0210 with imputation, 0.0213 unmasked).

  python3 run_v7.py time [params.json]         # one evaluation, with timing
  python3 run_v7.py calib 120 150              # local search + Nelder-Mead from v6_best (writes v7_best.json)
  python3 run_v7.py results                    # experiments + bunching (writes v7_results.json)
  python3 run_v7.py fine                       # current vs. no size rule, finer grid (writes v7_results_fine.json)
"""
import json
import sys
import time

import numpy as np
from scipy.optimize import minimize

from eps_model import cap_2024
from run_eps import cap_2019, SHOCK_YEARS
from run_v5 import BOUNDS, NAMES, build, bunching, summary

EPS_SHARE = 219_507 / 4_147_204                       # E-9 in manufacturing / manufacturing workers, 2024
M = EPS_SHARE / (1 - EPS_SHARE)                        # quota relative to Korean labor N = 1
T = dict(avg_size=8.14, share_small=0.713, exit_rate=0.066, users=0.080, eps_share_users=0.369,
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
    r = build(p, M, **grid).solve("current")               # 2024 caps: census-based moments
    mod19 = build(p, M, cap=cap_2019, **grid)
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
    # Start from v6_best.json (or v7_best.json if it exists). Same search as run_v6.py.
    from multiprocessing import Pool
    d = json.load(open("v6_best.json"))
    try:
        d = json.load(open("v7_best.json"))
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
                json.dump(dict(loss=best_L, **best), open("v7_best.json", "w"), indent=1)
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
            json.dump(dict(loss=L, **p), open("v7_best.json", "w"), indent=1)
            print(f"nm: loss {L:.4f} | {show(r)}", flush=True)
        return L
    obj.best = best_L
    print("== local search done; Nelder-Mead", flush=True)
    minimize(obj, [best[k] for k in NAMES], method="Nelder-Mead",
             options=dict(maxiter=int(sys.argv[3]) if len(sys.argv) > 3 else 150, adaptive=True,
                          xatol=1e-4, fatol=1e-5))
    print("DONE", flush=True)

if __name__ == "__main__" and sys.argv[1] == "results":
    d = json.load(open("v7_best.json"))
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
    json.dump(res, open("v7_results.json", "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("loss", "fit", "lpy", "theta_2019", "net_Y_change_vs_current")}, indent=1))
    print(json.dumps(res["experiments"]["current rule"]["bunching"]["steps"], indent=1))
    print("DONE", flush=True)

if __name__ == "__main__" and sys.argv[1] == "fine":
    d = json.load(open("v7_best.json"))
    p = {k: d[k] for k in NAMES}
    res = dict(params=p, grid=dict(nx=48, nz=21), experiments={})
    for name, reg in [("current rule", "current"), ("size-neutral, same quota (by price)", "neutral")]:
        ri = build(p, M, nx=48, nz=21).solve(reg)
        res["experiments"][name] = dict(summary(ri), bunching=bunching(ri))
    a, b = (res["experiments"][k]["net_Y"] for k in res["experiments"])
    res["net_Y_change_neutral"] = b / a - 1
    r = moments(p, nx=48, nz=21)
    res["fit"], res["lpy"] = {k: float(r[k]) for k in T}, r["lpy"]
    json.dump(res, open("v7_results_fine.json", "w"), indent=1)
    print(f"no size rule vs current: {100 * res['net_Y_change_neutral']:+.2f}%", flush=True)
    print(json.dumps(dict(res["fit"], **res["lpy"]), indent=1), flush=True)
