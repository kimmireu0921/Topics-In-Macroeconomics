"""
EPS model v4 (task-based, two plant types, quantity rationing): calibration and
experiments.

Fixed from step 1 (no-EPS firm-side fit, see NOTES.md):
  alpha=0.6916 sigma_s=0.1999 rho_s=0.8975 nu_top=0.6801 delta=0.0235 ce=2.6362
Calibrated here under the current rule, by random search then Nelder-Mead:
  rho (CES between core and manual work), cm (fixed cost of using EPS),
  psi, xi (Korean manual premium for small plants), and the two plant types:
  lam_A, cf_A (light), lam_B, cf_B (manual-intensive), share_B (entry share).
Targets:
  plant size 7.5, share with 1-4 workers 0.70, exit 8%      (MDIS census; exit assumed)
  EPS users 10% of plants, EPS share among users 0.37,
  users' average size 13                                       (Lee-Peri-Yang; E-9 counts)
  closure slope 0.15 (Lee-Peri-Yang 0.124-0.177; 20% EPS cut expected for 2 years)
Experiments: none / current / size-neutral (same quota, by price) / quota +-50%.
"""
import json
import sys

import numpy as np
from scipy.optimize import minimize

from eps_model import EPSModel, cap_2024


def cap_2019(n):
    """2019 manufacturing EPS caps by Korean workers (Lee, Peri and Yang 2026, Table 4)."""
    n = np.asarray(n, float)
    return np.select([n <= 5, n <= 10, n <= 30, n <= 50, n <= 100, n <= 150, n <= 200],
                     [5, 7, 10, 12, 15, 20, 25], default=30)

FIRM = dict(alpha=0.6916, sigma_s=0.1999, rho_s=0.8975, nu_top=0.6801, delta=0.0235, ce=2.6362)
N, EPS_SHARE = 1.0, 0.055
M = EPS_SHARE / (1 - EPS_SHARE) * N
SHOCK_YEARS = 2   # baseline: the 2020-21 stop lasted about two years (robustness: 5)
SIG_E = 0.1       # scale of the logit exit taste shock (smoothing)
T = dict(avg_size=7.5, share_small=0.70, exit_rate=0.08, users=0.10, eps_share_users=0.37,
         users_size=13.0, slope_lpy=0.15)
# eps_share_users (Jan 2020) and slope_lpy (2020-21 shock) are computed under the 2019 caps;
# all other moments under the 2024 caps. slope_lpy = Lee-Peri-Yang's design (EPS users only,
# statutory exposure).
NAMES = ["rho", "cm", "psi", "xi", "lamA", "cfA", "lamB", "cfB", "shB", "sigma_s", "nu_top", "ce", "delta"]
BOUNDS = dict(rho=(-1.5, 0.8), cm=(0.01, 3), psi=(0.5, 10), xi=(0.1, 1.5), lamA=(0.01, 0.5),
              cfA=(0.4, 2.5), lamB=(0.3, 4), cfB=(1, 15), shB=(0.05, 0.6),
              sigma_s=(0.08, 0.5), nu_top=(0.2, 0.9), ce=(0.3, 10), delta=(0.003, 0.05))
LOG = {"cm", "lamA", "lamB", "cfB", "psi"}


def build(p, M_=M, cap=cap_2024):
    types = [dict(lam=p["lamA"], cf=p["cfA"], share=1 - p["shB"]),
             dict(lam=p["lamB"], cf=p["cfB"], share=p["shB"])]
    firm = dict(FIRM, **{k: p[k] for k in ("sigma_s", "nu_top", "ce", "delta") if k in p})
    return EPSModel(types, N=N, M=M_, rho=p["rho"], cm=p["cm"], psi=p["psi"], xi=p["xi"], sig_e=SIG_E,
                    cap=cap, **firm)


def moments(p):
    r = build(p).solve("current")                      # 2024 caps: today's moments
    mod19 = build(p, cap=cap_2019)
    r19 = mod19.solve("current")                       # 2019 caps: Jan 2020 and the 2020-21 shock
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


def summary(r):
    keys = ["net_Y", "Y", "firms", "avg_size", "share_small", "exit_rate", "endo_exit_share", "users",
            "eps_share_users", "users_size", "eps_share", "w", "x", "eq_error"]
    d = {k: float(r[k]) for k in keys}
    d["type_share"] = [float(v) for v in r["type_share"]]
    return d


def experiments(p):
    out = {}
    for name, reg, Mx in [("no EPS", "none", 0.0), ("current rule", "current", M),
                          ("size-neutral, same quota (by price)", "neutral", M),
                          ("current rule, quota +50%", "current", 1.5 * M),
                          ("current rule, quota -50%", "current", 0.5 * M),
                          ("2019 caps, same quota", "current", M)]:
        cap = cap_2019 if name.startswith("2019") else cap_2024
        out[name] = summary(build(p, Mx, cap=cap).solve(reg))
    return out


def draw(rng):
    return {k: float(np.exp(rng.uniform(np.log(BOUNDS[k][0]), np.log(BOUNDS[k][1])))) if k in LOG
            else float(rng.uniform(*BOUNDS[k])) for k in NAMES}


def refine_from(start, outfile, maxiter=400):
    """Nelder-Mead from a given parameter dict (skips the random search)."""
    def obj(x):
        p = dict(zip(NAMES, x))
        if any(not (BOUNDS[k][0] <= p[k] <= BOUNDS[k][1]) for k in NAMES):
            return 50.0
        L, r = safe(p)
        if r is not None and L < obj.best:
            obj.best = L
            json.dump(dict(loss=L, **p), open("recal_best.json", "w"), indent=1)
        if r is not None and L < 50:
            print(f"eval loss {L:.4f} | users {r['users']:.3f} share_u {r['eps_share_users']:.2f} size_u {r['users_size']:.1f} "
                  f"slope_lpy {r['slope_lpy']:.3f} size {r['avg_size']:.2f} small {r['share_small']:.2f} exit {r['exit_rate']:.3f}", flush=True)
        return L
    obj.best = 50.0
    res = minimize(obj, [start[k] for k in NAMES], method="Nelder-Mead",
                   options=dict(maxiter=maxiter, adaptive=True, xatol=1e-4, fatol=1e-5))
    p = dict(zip(NAMES, res.x))
    r = moments(p)
    fit = {k: float(r[k]) for k in T}
    print("== fit:", {k: round(v, 3) for k, v in fit.items()}, flush=True)
    results = dict(firm=FIRM, params=p, loss=float(res.fun), targets=T, fit=fit,
                   shock_years=SHOCK_YEARS, experiments=experiments(p))
    json.dump(results, open(outfile, "w"), indent=1)
    print("DONE", flush=True)


if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[2] == "recal":
    # Recalibration (Oct 18): start from local_best.json, local search, then Nelder-Mead.
    d = json.load(open("local_best.json"))
    best = {k: d[k] for k in NAMES}
    rng = np.random.default_rng(5)
    best_L, r = safe(best)
    print(f"start loss {best_L:.4f} | slope_lpy {r['slope_lpy']:.3f} share_u {r['eps_share_users']:.2f}", flush=True)
    for i in range(int(sys.argv[3]) if len(sys.argv) > 3 else 150):
        cand = {}
        for k in NAMES:
            lo, hi = BOUNDS[k]
            v = best[k] * np.exp(rng.normal(0, 0.2)) if best[k] > 0 else best[k] + rng.normal(0, 0.1)
            cand[k] = float(min(max(v, lo), hi))
        L, r = safe(cand)
        if L < best_L:
            best_L, best = L, cand
            print(f"local {i}: loss {L:.4f} | users {r['users']:.3f} share_u {r['eps_share_users']:.2f} size_u {r['users_size']:.1f} "
                  f"slope_lpy {r['slope_lpy']:.3f} size {r['avg_size']:.2f} small {r['share_small']:.2f} exit {r['exit_rate']:.3f}", flush=True)
            json.dump(dict(loss=best_L, **best), open("recal_best.json", "w"), indent=1)
    print("== local search done; Nelder-Mead", flush=True)
    refine_from(best, sys.argv[1], maxiter=500)
    sys.exit()

if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[2] == "refine":
    # Start from the best v4 draw, plus firm-side values from step 1; first a local
    # random search (log-normal perturbations), then Nelder-Mead from the best point.
    top = json.load(open("top_draws.json"))
    d = [x for x in top if abs(x["loss"] - 3.28) < 0.01][0]
    start = {k: d[k] for k in NAMES if k in d}
    start.update(sigma_s=FIRM["sigma_s"], nu_top=FIRM["nu_top"], ce=FIRM["ce"], delta=FIRM["delta"])
    rng = np.random.default_rng(3)
    best_L, _ = safe(start)
    best = start
    print(f"start loss {best_L:.4f}", flush=True)
    for i in range(int(sys.argv[3]) if len(sys.argv) > 3 else 200):
        cand = {}
        for k in NAMES:
            lo, hi = BOUNDS[k]
            v = best[k] * np.exp(rng.normal(0, 0.25)) if best[k] > 0 else best[k] + rng.normal(0, 0.15)
            cand[k] = float(min(max(v, lo), hi))
        L, r = safe(cand)
        if L < best_L:
            best_L, best = L, cand
            print(f"local {i}: loss {L:.4f} | users {r['users']:.3f} share_u {r['eps_share_users']:.2f} size_u {r['users_size']:.1f} "
                  f"slope_lpy {r['slope_lpy']:.3f} size {r['avg_size']:.2f} small {r['share_small']:.2f} exit {r['exit_rate']:.3f}", flush=True)
    json.dump(dict(loss=best_L, **best), open("local_best.json", "w"), indent=1)
    print("== local search done; Nelder-Mead", flush=True)
    refine_from(best, sys.argv[1], maxiter=700)
    sys.exit()

if __name__ == "__main__":
    outfile = sys.argv[1] if len(sys.argv) > 1 else "eps_results.json"
    ndraw = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    rng = np.random.default_rng(11)
    draws = []
    for i in range(ndraw):
        p = draw(rng)
        L, r = safe(p)
        draws.append((L, p))
        if r is not None and L < 50:
            print(f"draw {i}: loss {L:.3f} | users {r['users']:.3f} share_u {r['eps_share_users']:.2f} "
                  f"size_u {r['users_size']:.1f} slope_lpy {r['slope_lpy']:.3f} size {r['avg_size']:.2f} "
                  f"small {r['share_small']:.2f} exit {r['exit_rate']:.3f}", flush=True)
    draws.sort(key=lambda d: d[0])
    json.dump([dict(loss=L, **p) for L, p in draws[:20]], open("top_draws.json", "w"), indent=1)
    print("== random search done; refining top 3", flush=True)

    def obj(x):
        p = dict(zip(NAMES, x))
        if any(not (BOUNDS[k][0] <= p[k] <= BOUNDS[k][1]) for k in NAMES):
            return 50.0
        return safe(p)[0]

    best = None
    for L0, p0 in draws[:3]:
        res = minimize(obj, [p0[k] for k in NAMES], method="Nelder-Mead",
                       options=dict(maxiter=300, adaptive=True, xatol=1e-4, fatol=1e-5))
        p = dict(zip(NAMES, res.x))
        print(f"   refined loss {res.fun:.4f} (from {L0:.3f}): " + " ".join(f"{k}={v:.4f}" for k, v in p.items()), flush=True)
        if best is None or res.fun < best[0]:
            best = (res.fun, p)
    L, p = best
    r = moments(p)
    fit = {k: float(r[k]) for k in T}
    print("== fit:", {k: round(v, 3) for k, v in fit.items()}, flush=True)
    results = dict(firm=FIRM, params=p, loss=L, targets=T, fit=fit, experiments=experiments(p))
    json.dump(results, open(outfile, "w"), indent=1)
    print("DONE", flush=True)
