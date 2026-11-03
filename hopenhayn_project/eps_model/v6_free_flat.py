"""Two checks at v6_best for Prof. Hur's Nov 3 questions. No parameter or feature changes.

  python3 v6_free_flat.py exp                 # writes baseline/free_flat.json
  python3 v6_free_flat.py hist                # writes baseline/bumpy_line.json

exp: the price experiment changes two things at once: it drops the size link and charges for
permits. This separates them, with the same quota, free permits and one limit L for every plant:
m <= L for all plants with h >= 1 ("flat"), or also keeping eligibility 1 <= h < 300 ("flat_elig").
L clears the quota, as theta does under the current rule.

hist: is the bumpy no-size-rule line an approximation error? Solves the distribution at the prices
of the (48, 21) solution, on finer productivity grids, and compares the same histogram bins.
"""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.getcwd())
from baseline_diagnostics import plans, policy
from eps_model import cap_2024
from eps_model_v5 import EPSModelV5
from run_eps import FIRM, M, N, SIG_E
from run_v5 import NAMES, bunching, summary

d = json.load(open("v6_best.json"))
P = {k: d[k] for k in NAMES}
L_MAX = 2000.0
BINS = [(0, 5), (5, 10), (10, 30), (30, 50), (50, 100), (100, 300), (300, 1e9)]
LABELS = ["0-5", "6-10", "11-30", "31-50", "51-100", "101-300", "300+"]
PCT = (50, 90, 99)


class Flat(EPSModelV5):
    """The current-rule solver with m <= x * L_MAX in place of m <= x * q(h)."""
    keep_elig = False

    def _plan(self, w, x, regime, m_limit=None):
        if regime != "current":
            return super()._plan(w, x, regime, m_limit)
        hh, ll = self.hh, self.ll
        wk = (w * (1 + self.prem))[:, None] * np.ones_like(ll)
        cost_no = w * hh + wk * ll
        elig = (hh >= 1) & (hh < 300) if self.keep_elig else hh >= 1
        mcap = np.where(elig, x * L_MAX, 0.0) * np.ones_like(ll)
        if m_limit is not None:
            mcap = np.minimum(mcap, m_limit)
        m_ = np.minimum(ll, mcap)
        wm = self.phi * w
        m_ = np.where((m_ > 0) & (wm < wk), m_, 0.0)
        cost_use = w * hh + wm * m_ + wk * (ll - m_) + self.cm * (m_ > 0)
        better = cost_use < cost_no
        m = np.where(better, m_, 0.0)
        k = ll - m
        return np.where(better, cost_use, cost_no), m, k, (wk - w) * k + self.cm * (m > 0)


def build(kind="base", **grid):
    types = [dict(lam=P["lamA"], cf=P["cfA"], share=1 - P["shB"]), dict(lam=P["lamB"], cf=P["cfB"], share=P["shB"])]
    cls = Flat if kind.startswith("flat") else EPSModelV5
    mod = cls(types, N=N, M=M, rho=P["rho"], cm=P["cm"], psi=P["psi"], xi=P["xi"], sig_e=SIG_E, cap=cap_2024,
              alpha=FIRM["alpha"], rho_s=FIRM["rho_s"], sigma_s=P["sigma_s"], gamma=P["gamma"], ce=P["ce"], delta=P["delta"], **grid)
    if kind == "flat_elig":
        mod.keep_elig = True
    return mod


def size_rows(a):
    """By Korean workers at the plant (core + Korean manual), as in the baseline tables."""
    mu, n, m = a["mu"], a["n"], a["m"]
    y, tot = a["y"], n + m
    rows = {}
    for lab, (lo, hi) in zip(LABELS, BINS):
        i = (n > lo) & (n <= hi)
        rows[lab] = dict(plants=float(mu[i].sum() / mu.sum()), share_eps=float(mu[i] @ m[i] / (mu @ m)) if (mu @ m) > 0 else 0.0,
                         share_y=float(mu[i] @ y[i] / (mu @ y)), share_work=float(mu[i] @ tot[i] / (mu @ tot)))
    return rows


def by_productivity(a, cuts=PCT):
    """Plants grouped by where they stand in productivity among manual-intensive plants of the baseline."""
    i = a["type"] == 1
    return dict(eps=float(a["mu"][i] @ a["m"][i]), workers=float(a["mu"][i] @ (a["n"] + a["m"])[i]), y=float(a["mu"][i] @ a["y"][i]))


def experiment(job):
    name, kind, reg, grid = job
    mod = build(kind, **grid)
    r = mod.solve(reg)
    out = r["out"]
    a = plans(mod, out, reg)
    res = dict(name=name, grid=grid, **summary(r), Me=float(out["Me"]), size=size_rows(a), manual=by_productivity(a), bunching=bunching(r),
               limit=float(out["x"] * L_MAX) if kind.startswith("flat") else None, price=float(out["x"]) if reg == "neutral" else None,
               theta=float(out["x"]) if kind == "base" and reg == "current" else None)
    if not grid:
        i = a["type"] == 1
        o = np.argsort(a["s"][i])
        c = np.cumsum(a["mu"][i][o]) / a["mu"][i].sum()
        sg = np.array([a["s"][i][o][np.searchsorted(c, q / 100)] for q in PCT])
        res["manual_pct_s"] = sg.tolist()
        res["sg"] = sg.tolist()
    return res, mod, out


def run_exp(job):
    return experiment(job)[0]


def policies(sg, res):
    """Plans at the same productivity levels across regimes, for the manual-intensive type."""
    for x in res:
        if x["grid"]:
            continue
        kind, reg = dict(current=("base", "current"), price=("base", "neutral"), flat=("flat", "current"),
                         flat_elig=("flat_elig", "current"))[x["name"]]
        mod = build(kind)
        h, k, m = policy(mod, 1, x["w"], x["limit"] / L_MAX if x["limit"] else x["x"], reg, np.array(sg))
        x["policy"] = dict(h=h.tolist(), k=k.tolist(), m=m.tolist(), total=(h + k + m).tolist())


def hist_at(job):
    grid, reg, w, x = job
    mod = build("base", **grid)
    mod.M = M
    blocks = []
    for t, T in enumerate(mod.types):
        pi, h, k, m, y, rc = mod.static(t, w, x, reg)
        V, stay = mod.values(pi)
        blocks.append(dict(pi=pi, h=h, k=k, m=m, y=y, rc=rc, V=V, stay=stay, mu=T["share"] * mod.stationary(stay)))
    mu, h = np.concatenate([B["mu"] for B in blocks]), np.concatenate([B["h"] for B in blocks])
    b = bunching(dict(out=dict(blocks=blocks)))
    e, v = np.array(b["hist_edges"]), np.array(b["hist"]) / np.diff(b["hist_edges"])
    rough = float(np.std(np.diff(np.log(v[v > 0]), n=2)))
    ratio = {str(t): b["steps"][t]["density_above"] / max(b["steps"][t]["density_below"], 1e-300) for t in (50, 100, 150, 200)}
    return dict(grid=grid, reg=reg, edges=e.tolist(), density=v.tolist(), roughness=rough, step_ratio=ratio, states=len(mod.s),
                log_s_step=float(np.log(mod.s[grid.get("nz", 11)] / mod.s[0])), plants_above_20=float(mu[h >= 20].sum() / mu.sum()))


def premium_run(job):
    """Current rule and price experiment with another premium slope, nothing recalibrated. psi moves
    so the premium at 10 core Koreans stays as in v6_best, unless given."""
    xi, psi = job
    psi = psi if psi else P["psi"] * (11.0 ** (xi - P["xi"]))
    out = {}
    for reg in ("current", "neutral"):
        types = [dict(lam=P["lamA"], cf=P["cfA"], share=1 - P["shB"]), dict(lam=P["lamB"], cf=P["cfB"], share=P["shB"])]
        mod = EPSModelV5(types, N=N, M=M, rho=P["rho"], cm=P["cm"], psi=psi, xi=xi, sig_e=SIG_E, cap=cap_2024, alpha=FIRM["alpha"],
                         rho_s=FIRM["rho_s"], sigma_s=P["sigma_s"], gamma=P["gamma"], ce=P["ce"], delta=P["delta"])
        r = mod.solve(reg)
        a = plans(mod, r["out"], reg)
        h, k, m = policy(mod, 1, r["w"], r["out"]["x"], reg, np.array(job_sg))
        mu, mm = a["mu"], a["m"]
        u = mm > 0
        out[reg] = dict(**summary(r), total=(h + k + m).tolist(), m=m.tolist(), size=size_rows(a),
                        max_h_user=float(a["h"][u & (mu > 1e-7)].max()) if u.any() else 0.0)
    p, w = out["neutral"]["x"], out["neutral"]["w"]
    return dict(xi=xi, psi=psi, net=out["neutral"]["net_Y"] / out["current"]["net_Y"] - 1, gross=out["neutral"]["Y"] / out["current"]["Y"] - 1,
                cutoff=(p / (w * psi)) ** (-1 / xi) - 1, **out)


job_sg = [round(v, 6) for v in json.load(open("baseline/free_flat.json"))[0]["sg"]] if os.path.exists("baseline/free_flat.json") else []

if __name__ == "__main__" and sys.argv[1] == "premium":
    jobs = [(P["xi"], P["psi"]), (0.15, None), (0.10, None), (0.05, None), (0.101, 1.599), (0.35, None)]
    with Pool(4) as pool:
        res = pool.map(premium_run, jobs, chunksize=1)
    json.dump(res, open("baseline/premium_slope.json", "w"), indent=1, default=float)
    for x in res:
        c, n = x["current"], x["neutral"]
        print(f"xi {x['xi']:.3f} psi {x['psi']:.3f} net {100 * x['net']:+.2f}% gross {100 * x['gross']:+.2f}% cutoff {x['cutoff']:.0f} users {c['users']:.3f}->{n['users']:.3f} "
              f"users size {c['users_size']:.1f}->{n['users_size']:.1f} eq {c['eq_error']:.0e},{n['eq_error']:.0e}\n"
              f"    top plant h {n['max_h_user']:.0f} p50/90/99 total {[round(t) for t in c['total']]} -> {[round(t) for t in n['total']]} EPS {[round(t) for t in c['m']]} -> {[round(t) for t in n['m']]}", flush=True)
    print("DONE")

if __name__ == "__main__" and sys.argv[1] == "exp":
    fine = dict(nx=48, nz=21)
    jobs = [("current", "base", "current", {}), ("price", "base", "neutral", {}), ("flat", "flat", "current", {}), ("flat_elig", "flat_elig", "current", {}),
            ("current", "base", "current", fine), ("price", "base", "neutral", fine), ("flat", "flat", "current", fine), ("flat_elig", "flat_elig", "current", fine)]
    with Pool(8) as pool:
        res = pool.map(run_exp, jobs, chunksize=1)
    base = next(x for x in res if x["name"] == "current" and not x["grid"])
    policies(base["sg"], res)
    json.dump(res, open("baseline/free_flat.json", "w"), indent=1, default=float)
    for g in (False, True):
        b0 = next(x for x in res if x["name"] == "current" and bool(x["grid"]) == g)
        print("\nfiner grid" if g else "\nregular grid")
        for x in (y for y in res if bool(y["grid"]) == g):
            print(f"{x['name']:<10} net {100 * (x['net_Y'] / b0['net_Y'] - 1):+.3f}% gross {100 * (x['Y'] / b0['Y'] - 1):+.3f}% users {x['users']:.4f} "
                  f"size {x['avg_size']:.2f} w {x['w']:.4f} eq {x['eq_error']:.1e} limit {x['limit']} price {x['price']} manual share {x['type_share'][1]:.4f}")
            print("   EPS share by Korean workers:", {k: round(v["share_eps"], 3) for k, v in x["size"].items()})
            print("   work share:", {k: round(v["share_work"], 3) for k, v in x["size"].items()})
            if "policy" in x:
                print("   policy total at p50/90/99:", [round(t, 1) for t in x["policy"]["total"]], "EPS", [round(t, 1) for t in x["policy"]["m"]])
    print("DONE")

if __name__ == "__main__" and sys.argv[1] == "hist":
    R = {x["name"]: x for x in json.load(open("baseline/free_flat.json")) if x["grid"]}
    grids = [dict(nx=24, nz=11), dict(nx=48, nz=21), dict(nx=96, nz=41), dict(nx=192, nz=21)]
    jobs = [(g, reg, R[n]["w"], R[n]["x"]) for g in grids for reg, n in (("neutral", "price"), ("current", "current"))]
    with Pool(4) as pool:
        res = pool.map(hist_at, jobs, chunksize=1)
    json.dump(res, open("baseline/bumpy_line.json", "w"), indent=1)
    for x in res:
        print(x["reg"], x["grid"], "states", x["states"], "log s step", round(x["log_s_step"], 4), "roughness", round(x["roughness"], 3),
              "step ratios", {k: round(v, 2) for k, v in x["step_ratio"].items()}, flush=True)
    print("DONE")
