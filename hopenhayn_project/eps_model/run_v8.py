"""
EPS model v8 (eps_model_v8.py): random eligibility + the legal cap on all Korean workers.
Calibrated to the sourced v7 targets (TARGETS.md). The eligible share e is not a parameter: it
clears the quota, as theta did in v5-v7.

  python3 run_v8.py time [params.json]         # one evaluation, with timing
  python3 run_v8.py calib 120 150              # local search + Nelder-Mead (writes v8_best.json)
  python3 run_v8.py results                    # experiments (writes v8_results.json)
"""
import json
import sys
import time

import numpy as np
from scipy.optimize import minimize

from eps_model import cap_2024
from eps_model_v8 import EPSModelV8, N_STEPS
from run_eps import cap_2019, FIRM, N, SHOCK_YEARS, SIG_E
from run_v5 import BOUNDS, NAMES as NAMES5

EPS_SHARE = 219_507 / 4_147_204                       # E-9 in manufacturing / manufacturing workers, 2024
M = EPS_SHARE / (1 - EPS_SHARE)                        # quota relative to Korean labour N = 1
T = dict(avg_size=8.14, share_small=0.713, exit_rate=0.066, users=0.080, eps_share_users=0.369,
         users_size=20.78, share_50plus=0.021,
         use_of_cap=0.624)        # survey 2019: mean of EPS workers / 2019 legal cap (bunching/cap_use_hist.json)
CHECK = dict(slope_lpy=0.152)   # Lee-Peri-Yang closure slope: reported, not targeted (see TARGETS.md)
NAMES = list(NAMES5)     # eta (imperfect substitutes) stays at 1: perfect substitutes, as in v5-v7
KOREAN_BINS = [10, 30, 50, 100, 150, 200]
A2_BINS = [(0, 10), (10, 20), (20, 50), (50, 100), (100, 200), (200, 300), (300, np.inf)]
USE_EDGES = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, .99999, 1.00001, np.inf]
BOUNDS = dict(BOUNDS, shB=(0.05, 0.9), eta=(0.05, 0.98))


def build(p, M_=M, cap=cap_2024, e0=None, **grid):
    types = [dict(lam=p["lamA"], cf=p["cfA"], share=1 - p["shB"]),
             dict(lam=p["lamB"], cf=p["cfB"], share=p["shB"])]
    return EPSModelV8(types, e0=e0, eta=p.get("eta", 1.0), N=N, M=M_, rho=p["rho"], cm=p["cm"], psi=p["psi"], xi=p["xi"],
                      sig_e=SIG_E, cap=cap, alpha=FIRM["alpha"], rho_s=FIRM["rho_s"],
                      sigma_s=p["sigma_s"], gamma=p["gamma"], ce=p["ce"], delta=p["delta"], **grid)


def flat(out, key):
    return np.concatenate([B[key] for B in out["blocks"]])


def lpy_design(mod, res, kappa=0.2, periods=SHOCK_YEARS):
    """Lee-Peri-Yang's sample and regressions in the model (EPS firms only, plant-mass weights):
    extra closure after a two-year cut of kappa in EPS workers, on statutory exposure q/(n+q),
    with Korean-size-bin dummies or a cubic in total workers. Also the use of the legal cap."""
    out = res["out"]
    disc = mod.beta * (1 - mod.delta)
    rows = []
    for B in out["blocks"]:
        u = B["m"] > 0
        if not u.any():
            continue
        pi_sh, *_ = mod.static_block(B["block"], out["w"], out["x"], "current",
                                     m_limit_by_s=(1 - kappa) * B["m"] + 1e-12)
        Vsh = B["V"]
        for _ in range(periods):
            Vsh, _ = mod._bellman(pi_sh, Vsh)
        p_sh = 1.0 / (1.0 + np.exp(-(disc * mod.P @ Vsh) / mod.sig_e))
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

    use = m / q
    mean_share = float(wgt @ share)
    return dict(mean_share=mean_share, workers=float(wgt @ tot), koreans=float(wgt @ n),
                slope_bins=coef(extra, bins), slope_cubic=coef(extra, cubic),
                use_of_cap=float(wgt @ use), at_cap=float(wgt[use >= 1 - 1e-6].sum()),
                use_hist=np.histogram(use, bins=USE_EDGES, weights=wgt)[0].tolist(),
                size_bins=[float(wgt[(tot >= a) & (tot < b)].sum()) for a, b in A2_BINS])


def moments(p, **grid):
    r = build(p, M, **grid).solve("current")              # 2024 caps: census and ministry moments
    mod19 = build(p, M, cap=cap_2019, **grid)
    r19 = mod19.solve("current")                         # 2019 caps: the survey and the 2020-21 stop
    lp = lpy_design(mod19, r19)
    r["lpy"] = lp
    r["eps_share_users"], r["users_size"] = lp["mean_share"], lp["workers"]
    r["slope_lpy"] = (lp["slope_bins"] + lp["slope_cubic"]) / 2
    r["use_of_cap"] = lp["use_of_cap"]
    r["eq_error"] = max(r["eq_error"], r19["eq_error"])
    r["type_share"] = [min(a, b) for a, b in zip(r["type_share"], r19["type_share"])]
    r["e_2024"], r["e_2019"] = float(r["out"]["x"]), float(r19["out"]["x"])
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
    return " ".join(f"{k} {r[k]:.3f}" for k in list(T) + list(CHECK)) + f" | e {r['e_2024']:.3f}/{r['e_2019']:.3f}"


def summary(r):
    keys = ["net_Y", "Y", "firms", "avg_size", "share_small", "share_50plus", "exit_rate", "endo_exit_share",
            "users", "eps_share_users", "users_size", "eps_share", "elig_share_plants", "w", "x", "eq_error", "Me"]
    d = {k: float(r[k]) for k in keys}
    d["type_share"] = [float(v) for v in r["type_share"]]
    return d


def bunching_n(r):
    """Plant mass by all Korean workers n around each cap step: just below ([0.9t, t]) vs at or just
    past it ((t, 1.1t]), per worker of width."""
    out = r["out"]
    mu, n = flat(out, "mu"), flat(out, "h") + flat(out, "k")
    mu = mu / mu.sum()
    rows = {}
    for t in list(N_STEPS) + [300]:
        below = mu[(n >= 0.9 * t) & (n <= t * (1 + 1e-7))].sum() / (0.1 * t)
        above = mu[(n > t * (1 + 1e-7)) & (n <= 1.1 * t)].sum() / (0.1 * t)
        rows[t] = dict(density_below=float(below), density_above=float(above))
    return rows


if __name__ == "__main__" and sys.argv[1] == "time":
    d = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "v7_best.json"))
    p = {k: d.get(k, 1.0) for k in NAMES}
    for kv in sys.argv[3:]:
        k, v = kv.split("=")
        p[k] = float(v)
    t0 = time.time()
    L, r = safe(p)
    print(f"loss {L:.4f} | {show(r) if r else 'failed'} | {time.time() - t0:.1f}s", flush=True)
    if r:
        print(json.dumps(dict(r["lpy"], type_share=r["type_share"], elig=r["elig_share_plants"]), indent=1), flush=True)

if __name__ == "__main__" and sys.argv[1] == "calib":
    from multiprocessing import Pool
    start = sys.argv[4] if len(sys.argv) > 4 else "v8_start.json"
    try:
        d = json.load(open("v8_best.json"))
    except FileNotFoundError:
        d = json.load(open(start))
    best = {k: d[k] for k in NAMES}
    rng = np.random.default_rng(17)
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
                json.dump(dict(loss=best_L, **best), open("v8_best.json", "w"), indent=1)
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
            json.dump(dict(loss=L, **p), open("v8_best.json", "w"), indent=1)
            print(f"nm: loss {L:.4f} | {show(r)}", flush=True)
        return L
    obj.best = best_L
    print("== local search done; Nelder-Mead", flush=True)
    minimize(obj, [best[k] for k in NAMES], method="Nelder-Mead",
             options=dict(maxiter=int(sys.argv[3]) if len(sys.argv) > 3 else 150, adaptive=True,
                          xatol=1e-4, fatol=1e-5))
    print("DONE", flush=True)


TOT_BINS = [(0, 10), (10, 20), (20, 50), (50, 100), (100, 200), (200, 300)]


def detail(mod, r):
    """Who uses EPS, the size pattern among users (by total workers, as in the survey), and the
    plans of the median and top 1% eligible manual-intensive plants."""
    out = r["out"]
    rows = {}
    for B in out["blocks"]:
        rows[(B["type"], B["eligible"])] = B
    mu_all = sum(B["mu"].sum() for B in out["blocks"])
    groups = {}
    for (t, el), B in rows.items():
        u = B["m"] > 0
        groups[f"{'manual' if t == 1 else 'light'}_{'eligible' if el else 'not'}"] = dict(
            plants=float(B["mu"].sum() / mu_all), user_rate=float(B["mu"][u].sum() / B["mu"].sum()),
            size=float(B["mu"] @ (B["h"] + B["k"] + B["m"]) / B["mu"].sum()),
            exit=float(B["mu"] @ (1 - (1 - mod.delta) * B["stay"]) / B["mu"].sum()))
    mu, m, n = flat(out, "mu"), flat(out, "m"), flat(out, "h") + flat(out, "k")
    u = m > 0
    tot, share = n + m, np.where(u, m / np.maximum(n + m, 1e-12), 0)
    size = {f"{a}-{b}": dict(share_of_users=float(mu[u & (tot >= a) & (tot < b)].sum() / mu[u].sum()),
                             eps_share=float(mu[u & (tot >= a) & (tot < b)] @ share[u & (tot >= a) & (tot < b)]
                                             / max(mu[u & (tot >= a) & (tot < b)].sum(), 1e-300)))
            for a, b in TOT_BINS}
    return dict(groups=groups, size=size)


def plans_at(mod, w, x, regime, s_values, eligible=True):
    """h, k, m of a manual-intensive plant at given productivities."""
    b = mod.blocks_def.index((1, eligible))
    pi, h, k, m, y, rc = mod.static_block(b, w, x, regime)
    i = [int(np.argmin(np.abs(mod.s - s))) for s in s_values]
    return dict(h=h[i].tolist(), k=k[i].tolist(), m=m[i].tolist(), total=(h[i] + k[i] + m[i]).tolist(), s=mod.s[i].tolist())


def run_exp(job):
    name, regime, e0, Mx = job
    p = json.load(open("v8_best.json"))
    p = {k: p[k] for k in NAMES}
    mod = build(p, Mx, e0=e0)
    r = mod.solve(regime)
    d = dict(summary(r), bunching=bunching_n(r), **detail(mod, r))
    return name, d, r["out"]["w"], r["out"]["x"]


if __name__ == "__main__" and sys.argv[1] == "results":
    from multiprocessing import Pool
    d = json.load(open("v8_best.json"))
    p = {k: d[k] for k in NAMES}
    r = moments(p)
    e0 = r["e_2024"]
    res = dict(params=p, loss=loss(r), targets=T, fit={k: float(r[k]) for k in T}, lpy=r["lpy"],
               checks={k: float(r[k]) for k in CHECK},
               e_2024=e0, e_2019=r["e_2019"], use_edges=[str(x) for x in USE_EDGES], experiments={})
    jobs = [("no EPS", "none", e0, M), ("current rule", "current", e0, M), ("price", "neutral", e0, M),
            ("equal limit", "flat", e0, M), ("current rule, 2019 caps", "current19", e0, M)]
    jobs = [j for j in jobs if j[1] != "current19"]
    with Pool(4) as pool:
        outs = pool.map(run_exp, jobs)
    for name, dd, w, x in outs:
        res["experiments"][name] = dd
    mod19 = build(p, M, cap=cap_2019)
    r19 = mod19.solve("current")
    res["current_2019"] = dict(summary(r19), **detail(mod19, r19))
    base = res["experiments"]["current rule"]
    res["change_vs_current"] = {k: dict(net_Y=v["net_Y"] / base["net_Y"] - 1, Y=v["Y"] / base["Y"] - 1,
                                        firms=v["firms"] / base["firms"] - 1, w=v["w"] / base["w"] - 1)
                                for k, v in res["experiments"].items()}
    # median and top 1% eligible manual-intensive plants (by productivity, today's rule)
    mod = build(p, M, e0=e0)
    rc = mod.solve("current")
    B = [b for b in rc["out"]["blocks"] if b["type"] == 1 and b["eligible"]][0]
    o = np.argsort(mod.s)
    c = np.cumsum(B["mu"][o]) / B["mu"].sum()
    sg = [float(mod.s[o][np.searchsorted(c, q)]) for q in (0.5, 0.99)]
    ex = res["experiments"]
    res["plans"] = dict(s=sg, current=plans_at(mod, ex["current rule"]["w"], ex["current rule"]["x"], "current", sg),
                        price=plans_at(mod, ex["price"]["w"], ex["price"]["x"], "neutral", sg),
                        equal=plans_at(build(p, M, e0=e0), ex["equal limit"]["w"], ex["equal limit"]["x"], "flat", sg),
                        not_eligible=plans_at(mod, ex["current rule"]["w"], ex["current rule"]["x"], "current", sg, eligible=False))
    json.dump(res, open("v8_results.json", "w"), indent=1)
    print(json.dumps(dict(loss=res["loss"], fit=res["fit"], e=(e0, r["e_2019"]), change=res["change_vs_current"],
                          plans=res["plans"]), indent=1))
    print("DONE", flush=True)
