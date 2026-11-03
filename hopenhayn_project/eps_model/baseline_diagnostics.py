"""Baseline diagnostics at v6_best, before any new experiment (Prof. Hur, Nov 3): who uses EPS and
why, who is held back by the limit, and where plants would be without it.

  python3 baseline_diagnostics.py          # writes baseline/diagnostics.json

Three plans for each plant, at the wage w of the solved economy:
  actual  the plan under the solved regime
  free    no limit and no permit price: EPS at cost w, plus the fixed cost c_m. This is the plant's
          preferred scale at today's prices. It is not an equilibrium: total demand exceeds the quota.
  none    no EPS at all
"""
import json
import os
from multiprocessing import Pool

import numpy as np

from eps_model import cap_2024
from run_eps import M, cap_2019
from run_v5 import NAMES, build, summary

d = json.load(open("v6_best.json"))
P = {k: d[k] for k in NAMES}
BINS = [(-1, 5), (5, 10), (10, 30), (30, 50), (50, 100), (100, 300), (300, 1e9)]
LABELS = ["0-5", "6-10", "11-30", "31-50", "51-100", "101-300", "300+"]
TOTAL_BINS = [(0, 10), (10, 20), (20, 50), (50, 100), (100, 200), (200, 300), (300, 1e9)]
JOBS = [("current_2024", "current", cap_2024, {}), ("current_2019", "current", cap_2019, {}),
        ("no_rule", "neutral", cap_2024, {}), ("current_2024_fine", "current", cap_2024, dict(nx=48, nz=21)),
        ("no_rule_fine", "neutral", cap_2024, dict(nx=48, nz=21))]


def plans(mod, out, reg):
    """One record per (type, productivity state), with the actual, free and no-EPS plans."""
    w, x = out["w"], out["x"]
    rows = []
    for t, B in enumerate(out["blocks"]):
        pi_f, h_f, k_f, m_f, y_f, _ = mod.static(t, w, 0.0, "neutral")
        pi_n, *_ = mod.static(t, w, 0.0, "none")
        cm = mod.cm
        mod.cm = 0.0
        pi_0, *_ = mod.static(t, w, x, reg)                     # same regime with no fixed cost of EPS
        pi_f0, *_ = mod.static(t, w, 0.0, "neutral")            # free access with no fixed cost
        mod.cm = cm
        n = B["h"] + B["k"]
        elig = (B["h"] >= 1) & (B["h"] < 300)
        q = mod.cap(B["h"]) * elig
        prem = mod.psi * (1 + B["h"]) ** (-mod.xi)
        rows.append(dict(type=np.full(len(n), t), s=mod.s, mu=B["mu"], h=B["h"], k=B["k"], m=B["m"], y=B["y"], n=n, elig=elig,
                         q=q, limit=x * q if reg == "current" else np.full(len(n), np.inf), prem=prem, pi=B["pi"],
                         pi_f=pi_f, pi_n=pi_n, pi_0=pi_0, pi_f0=pi_f0, h_f=h_f, k_f=k_f, m_f=m_f, y_f=y_f))
    return {key: np.concatenate([r[key] for r in rows]) for key in rows[0]}


def wavg(v, w):
    return float(v @ w / w.sum()) if w.sum() > 0 else None


def size_table(a, w, reg):
    mu, m, tot, tot_f = a["mu"], a["m"], a["n"] + a["m"], a["h_f"] + a["k_f"] + a["m_f"]
    users = m > 0
    wants = a["pi_f"] > a["pi"] + 1e-9
    at_limit = users & (m >= a["limit"] * (1 - 1e-9))
    value = w * a["prem"]                                       # value of one more permit if the plant still has k > 0
    out = {}
    for lab, (lo, hi) in zip(LABELS, BINS):
        i = (a["n"] > lo) & (a["n"] <= hi)
        u = i & users
        M_i = mu[i].sum()
        out[lab] = dict(plants=float(M_i / mu.sum()), manual_share=wavg(a["type"][i].astype(float), mu[i]),
                        user_rate=float(mu[u].sum() / M_i) if M_i else None, share_of_users=float(mu[u].sum() / mu[users].sum()),
                        share_of_eps=float(mu[u] @ m[u] / (mu @ m)), output_share=float(mu[i] @ a["y"][i] / (mu @ a["y"])),
                        users_at_limit=float(mu[u & at_limit].sum() / mu[u].sum()) if u.any() else None,
                        users_want_more=float(mu[u & wants].sum() / mu[u].sum()) if u.any() else None,
                        m_user=wavg(m[u], mu[u]), legal_cap_user=wavg(a["q"][u], mu[u]) if reg == "current" else None,
                        use_of_legal_cap=wavg((m[u] / np.maximum(a["q"][u], 1e-12)), mu[u]) if reg == "current" and u.any() else None,
                        free_user_rate=float(mu[i & (a["m_f"] > 0)].sum() / M_i) if M_i else None,
                        free_m=wavg(a["m_f"][i & (a["type"] == 1)], mu[i & (a["type"] == 1)]),
                        m_manual=wavg(m[i & (a["type"] == 1)], mu[i & (a["type"] == 1)]),
                        size=wavg(tot[i], mu[i]), free_size=wavg(tot_f[i], mu[i]),
                        size_manual=wavg(tot[i & (a["type"] == 1)], mu[i & (a["type"] == 1)]),
                        free_size_manual=wavg(tot_f[i & (a["type"] == 1)], mu[i & (a["type"] == 1)]),
                        permit_value=wavg(value[i & (a["type"] == 1)], mu[i & (a["type"] == 1)]))
    return out


def who_uses(a):
    """Non-users split by the reason that survives: would they use EPS even if free and unlimited?"""
    mu, users = a["mu"], a["m"] > 0
    light, manual = a["type"] == 0, a["type"] == 1
    tot = mu.sum()
    free_gain = a["pi_f"] > a["pi_n"] + 1e-9
    n_elig = ~a["elig"]
    s = lambda c: float(mu[c].sum() / tot)
    return dict(users=s(users), users_light=s(users & light), users_manual=s(users & manual),
                light=s(light), manual=s(manual),
                non_light_no_gain_if_free=s(~users & light & ~free_gain), non_light_gain_if_free=s(~users & light & free_gain),
                non_manual_ineligible=s(~users & manual & n_elig), non_manual_other=s(~users & manual & ~n_elig),
                light_gain_with_zero_cm=float(mu[light & (a["pi_f0"] > a["pi_n"] + 1e-9)].sum() / mu[light].sum()),
                light_manual_workers=wavg(a["k"][light], mu[light]), manual_manual_workers=wavg((a["k"] + a["m"])[manual], mu[manual]),
                light_core=wavg(a["h"][light], mu[light]), manual_core=wavg(a["h"][manual], mu[manual]),
                light_saving_if_free=wavg((a["pi_f0"] - a["pi_n"])[light], mu[light]),
                manual_saving_if_free=wavg((a["pi_f0"] - a["pi_n"])[manual], mu[manual]))


def users_by_total(a):
    mu, m, tot = a["mu"], a["m"], a["n"] + a["m"]
    u = m > 0
    out = {}
    for lo, hi in TOTAL_BINS:
        i = u & (tot >= lo) & (tot < hi)
        out[f"{lo}-{int(hi) if hi < 1e8 else '+'}"] = dict(share_of_users=float(mu[i].sum() / mu[u].sum()),
                                                            eps_share=wavg((m / tot)[i], mu[i]))
    return out


def binding(a, w, reg):
    mu, m = a["mu"], a["m"]
    u = m > 0
    at = u & (m >= a["limit"] * (1 - 1e-9))
    wants = a["pi_f"] > a["pi"] + 1e-9
    gain = a["pi_f"] - a["pi"]
    res = dict(users_at_limit=float(mu[at].sum() / mu[u].sum()), users_want_more=float(mu[u & wants].sum() / mu[u].sum()),
               users_below_limit=float(mu[u & ~at].sum() / mu[u].sum()),
               gain_user=wavg(gain[u], mu[u]), profit_user=wavg(a["pi"][u] + 0, mu[u]),
               demand_free=float(mu @ a["m_f"]), quota=float(mu @ m), ratio_free_to_quota=float((mu @ a["m_f"]) / (mu @ m)))
    if reg == "current":
        res["users_at_legal_cap"] = float(mu[u & (m >= a["q"] * (1 - 1e-9))].sum() / mu[u].sum())
    return res


def policy(mod, t, w, x, reg, sg):
    """Plan at any productivity, with the grid search used in static()."""
    cost, M_, K_, _ = (v.ravel() for v in mod._plan(w, x, reg))
    fr = mod.types[t]["fr"]
    o = np.argsort(cost, kind="stable")
    fo = fr[o]
    best = np.concatenate([[-np.inf], np.maximum.accumulate(fo)[:-1]])
    cand = o[fo > best]
    val = sg[:, None] * fr[cand][None, :] - cost[cand][None, :]
    j = cand[val.argmax(1)]
    return mod.hh.ravel()[j], K_[j], M_[j]


def run(job):
    name, reg, cap, grid = job
    mod = build(P, M, cap=cap, **grid)
    r = mod.solve(reg)
    out = r["out"]
    a = plans(mod, out, reg)
    res = dict(name=name, summary=summary(r), w=float(out["w"]), x=float(out["x"]), size_table=size_table(a, out["w"], reg),
               who_uses=who_uses(a), users_by_total=users_by_total(a), binding=binding(a, out["w"], reg))
    if not grid:
        keep = a["mu"] > 1e-7
        lo, hi = a["s"][keep].min(), a["s"][keep].max()
        sg = np.geomspace(lo, hi, 400)
        res["s_grid"] = sg.tolist()
        res["pct"] = {}
        for t, nm in enumerate(("light", "manual")):
            i = a["type"] == t
            o = np.argsort(a["s"][i])
            c = np.cumsum(a["mu"][i][o]) / a["mu"][i].sum()
            res["pct"][nm] = {str(q): float(a["s"][i][o][np.searchsorted(c, q / 100)]) for q in (50, 90, 99)}
        res["policy"] = {}
        for t, nm in enumerate(("light", "manual")):
            res["policy"][nm] = {}
            for lab, (xx, rr) in dict(actual=(out["x"], reg), free=(0.0, "neutral")).items():
                h, k, m = policy(mod, t, out["w"], xx, rr, sg)
                res["policy"][nm][lab] = dict(h=h.tolist(), k=k.tolist(), m=m.tolist())
    return res


if __name__ == "__main__":
    os.makedirs("baseline", exist_ok=True)
    with Pool(5) as pool:
        all_res = {x["name"]: x for x in pool.imap(run, JOBS)}
    json.dump(dict(params=P, quota=float(M), runs=all_res), open("baseline/diagnostics.json", "w"), indent=1, default=float)
    for name, x in all_res.items():
        print(f"\n=== {name}: w {x['w']:.4f} x {x['x']:.4f} users {x['summary']['users']:.4f}")
        print("who uses:", json.dumps({k: round(v, 4) for k, v in x["who_uses"].items()}))
        print("binding:", json.dumps({k: round(v, 4) for k, v in x["binding"].items()}))
        cols = ("plants", "manual_share", "user_rate", "share_of_eps", "output_share", "users_at_limit", "users_want_more",
                "m_user", "legal_cap_user", "use_of_legal_cap", "free_user_rate", "m_manual", "free_m", "size_manual", "free_size_manual", "permit_value")
        print("bin      " + " ".join(f"{c[:9]:>9}" for c in cols))
        for lab, r in x["size_table"].items():
            print(f"{lab:<9}" + " ".join(f"{(r[c] if r[c] is not None else float('nan')):>9.3f}" for c in cols))
        print("users by total:", json.dumps({k: (round(v["share_of_users"], 3), None if v["eps_share"] is None else round(v["eps_share"], 3)) for k, v in x["users_by_total"].items()}))
    print("DONE")
