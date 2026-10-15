"""
Calibrate the EPS model to Korean manufacturing and compare regimes.

Targets (current EPS rule):
  average plant size     7.5   census 2023-24 (MDIS, unmasked plants)
  share with 1-4 workers 0.70  census 2023-24
  annual exit rate       0.08  assumption, to be checked against KOSIS 기업생멸
  share of plants using EPS          0.10  ~50k EPS manufacturing workplaces / ~510k plants
  EPS share of workforce, EPS users  0.37  Lee, Peri and Yang (2026), Table 3
Aggregate EPS share of manufacturing employment is set to 5.5% through the quota
M (~240k E-9 manufacturing workers / ~4.4m manufacturing workers).

Experiments: none / current / neutral (same M, no size rule), quota +50% / -50%.
Sensitivity: rho in {0.2, 0.35, 0.65, 0.8}, re-fitting lam and cm each time.
"""
import json
import sys

import numpy as np
from scipy.optimize import minimize

from eps_model import EPSModel

N, EPS_SHARE = 1.0, 0.055
M = EPS_SHARE / (1 - EPS_SHARE) * N
TARGETS = dict(avg_size=7.5, share_small=0.70, exit_rate=0.08, users=0.10, eps_share_users=0.37)


def build(p, rho, M_=M):
    return EPSModel(rho=rho, cf=p["cf"], nu_top=p["nu_top"], sigma_s=p["sigma_s"], rho_s=0.9,
                    delta=0.07, lam=p["lam"], cm=p["cm"], N=N, M=M_)


def loss(r):
    return sum(((r[k] - v) / v) ** 2 for k, v in TARGETS.items())


def unpack(x, names, fixed):
    p = dict(fixed)
    for k, v in zip(names, x):
        p[k] = 1 / (1 + np.exp(-v)) if k == "nu_top" else np.exp(v)
    return p


def pack(p, names):
    return [np.log(p[k] / (1 - p[k])) if k == "nu_top" else np.log(p[k]) for k in names]


def calibrate(rho, start, names, maxiter):
    def obj(x):
        p = unpack(x, names, start)
        try:
            r = build(p, rho).solve("current")
        except Exception:
            return 1e3
        L = loss(r)
        print(f"  rho={rho} {', '.join(f'{k}={p[k]:.3f}' for k in names)} -> loss {L:.4f}", flush=True)
        return L
    res = minimize(obj, pack(start, names), method="Nelder-Mead",
                   options=dict(maxiter=maxiter, xatol=1e-3, fatol=1e-5))
    return unpack(res.x, names, start)


def row(r):
    keys = ["Y", "firms", "avg_size", "exit_rate", "avg_s", "share_small", "users", "eps_share", "eps_share_users", "w", "wm"]
    return {k: float(r[k]) for k in keys}


def experiments(p, rho):
    out = {}
    for name, regime, M_ in [("no EPS", "none", 0.0), ("current rule", "current", M),
                             ("size-neutral, same quota", "neutral", M),
                             ("current rule, quota +50%", "current", 1.5 * M),
                             ("current rule, quota -50%", "current", 0.5 * M)]:
        out[name] = row(build(p, rho, M_).solve(regime))
    return out


if __name__ == "__main__":
    # Step 1 (done separately, grid search with M = 0): firm-side parameters
    #   cf=0.5, nu_top=0.6, sigma_s=0.15, delta=0.07 -> size 8.4, 1-4 share 0.74, exit 7.6%
    # Step 2: for each rho, grid-search lam and cm to hit EPS users 10% and
    #   EPS share among users 37% under the current rule, then run experiments.
    firm = dict(cf=0.5, nu_top=0.6, sigma_s=0.15)
    eps_targets = dict(users=0.10, eps_share_users=0.37)
    results = {"firm_params": dict(firm, delta=0.07), "targets": TARGETS, "by_rho": {}}
    for rho in [0.2, 0.35, 0.5, 0.65, 0.8]:
        print(f"== rho = {rho}", flush=True)
        def fit(lam, cm):
            p = dict(firm, lam=lam, cm=cm)
            r = build(p, rho).solve("current")
            return sum(((r[k] - v) / v) ** 2 for k, v in eps_targets.items()), p, r
        grid = [fit(l, c) for l in np.geomspace(0.1, 3, 7) for c in np.geomspace(0.05, 5, 7)]
        L, p, r = min(grid, key=lambda g: g[0])
        fine = [fit(p["lam"] * a, p["cm"] * b) for a in np.geomspace(0.7, 1.4, 5) for b in np.geomspace(0.6, 1.7, 5)]
        L, p, r = min(fine + [(L, p, r)], key=lambda g: g[0])
        print(f"   fit loss {L:.4f}: lam={p['lam']:.3f} cm={p['cm']:.3f} users={r['users']:.3f} "
              f"share_users={r['eps_share_users']:.3f} size={r['avg_size']:.2f} exit={r['exit_rate']:.3f}", flush=True)
        results["by_rho"][str(rho)] = {"params": p, "fit_loss": L, "exp": experiments(p, rho)}
        json.dump(results, open(sys.argv[1] if len(sys.argv) > 1 else "eps_results.json", "w"), indent=1)
    print("DONE", flush=True)
