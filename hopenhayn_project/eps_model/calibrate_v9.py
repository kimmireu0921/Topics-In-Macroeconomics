"""v9 calibration driven by targets_v9.json. Same model as v8 (eps_model_v8.py); only the targets, their weights
and the split between free and externally set parameters come from the config file.

  python3 calibrate_v9.py check [params.json]      # moments and loss at a parameter file (default v9_best or v8_best)
  python3 calibrate_v9.py calib ROUNDS NM_STEPS    # local search + Nelder-Mead; writes v9_best.json, v9_calib.log

A parameter listed under "external" in the config with a value is held at that value; the rest of
NAMES that appear in "free" are estimated.
"""
import json
import os
import sys

import numpy as np

from moments_v9 import book
from run_eps import cap_2019
from run_v8 import build, lpy_design, BOUNDS, NAMES

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "targets_v9.json")))
EPS = CFG["quota"]["eps_share_of_workers"]
M = EPS / (1 - EPS)
FREE = [k for k in CFG["free"] if k in NAMES]
FIXED = {k: v["value"] for k, v in CFG["external"].items() if k in NAMES and v.get("value") is not None}
TARGETS = [t for t in CFG["targets"] if t.get("weight", 0) > 0 and t.get("value") is not None]


def start_params():
    for f in ("v9_best.json", "v8_best.json"):
        p = os.path.join(HERE, f)
        if os.path.exists(p):
            d = json.load(open(p))
            return {k: d[k] for k in NAMES}
    raise FileNotFoundError("no starting parameters")


def get(d, key):
    for part in key.split("."):
        d = d[part]
    return d


def moments(p):
    """Books under the 2024 and 2019 caps, plus the Lee-Peri-Yang design under 2019."""
    p = dict(p, **FIXED)
    m24 = build(p, M)
    r24 = m24.solve("current")
    m19 = build(p, M, cap=cap_2019)
    r19 = m19.solve("current")
    b24, b19 = book(m24, r24), book(m19, r19)
    lp = lpy_design(m19, r19)
    b19["lpy"] = lp
    b19["slope_lpy"] = (lp["slope_bins"] + lp["slope_cubic"]) / 2
    eq = max(r24["eq_error"], r19["eq_error"])
    types = min(min(r24["type_share"]), min(r19["type_share"]))
    return {2024: b24, 2019: b19, "eq_error": eq, "min_type_share": types}


def loss(mo):
    if mo["eq_error"] > 0.05 or mo["min_type_share"] < 0.03:
        return 50.0
    L = 0.0
    for t in TARGETS:
        v = get(mo[t["caps"]], t["moment"])
        L += t["weight"] * ((v - t["value"]) / t["value"]) ** 2
    return float(L)


def safe(p):
    try:
        mo = moments(p)
        return loss(mo), mo
    except Exception:
        return 50.0, None


def show(mo):
    return " ".join(f"{t['name']} {get(mo[t['caps']], t['moment']):.3f}" for t in TARGETS)


if __name__ == "__main__" and sys.argv[1] == "check":
    p = start_params() if len(sys.argv) < 3 else {k: v for k, v in json.load(open(sys.argv[2])).items() if k in NAMES}
    L, mo = safe(p)
    print(f"loss {L:.4f} | free {len(FREE)} params, {len(TARGETS)} targets | fixed {FIXED}")
    for t in CFG["targets"]:
        v = get(mo[t["caps"]], t["moment"])
        tag = "fit" if t in TARGETS else t["status"]
        print(f"  {t['name']:<22} model {v:8.4f}  data {t['value'] if t['value'] is not None else '   -':>8}  [{tag}]")

if __name__ == "__main__" and sys.argv[1] == "calib":
    from multiprocessing import Pool
    from scipy.optimize import minimize
    best = start_params()
    rng = np.random.default_rng(23)
    best_L, mo = safe(best)
    log = open(os.path.join(HERE, "v9_calib.log"), "a")
    say = lambda s: (print(s, flush=True), log.write(s + "\n"), log.flush())
    say(f"start loss {best_L:.4f} | free {FREE} | fixed {FIXED} | {show(mo) if mo else ''}")
    step, stall = 0.15, 0
    with Pool(8) as pool:
        for i in range(int(sys.argv[2])):
            cands = []
            for _ in range(8):
                c = dict(best)
                for k in FREE:
                    lo, hi = BOUNDS[k]
                    v = best[k] * np.exp(rng.normal(0, step)) if best[k] > 0 else best[k] + rng.normal(0, step / 2)
                    c[k] = float(min(max(v, lo), hi))
                cands.append(c)
            res = pool.map(safe, cands)
            j = int(np.argmin([L for L, _ in res]))
            if res[j][0] < best_L:
                best_L, best, stall = res[j][0], cands[j], 0
                say(f"round {i} (step {step:.3f}): loss {best_L:.4f} | {show(res[j][1])}")
                json.dump(dict(loss=best_L, **dict(best, **FIXED)), open(os.path.join(HERE, "v9_best.json"), "w"), indent=1)
            else:
                stall += 1
                if stall >= 6:
                    step, stall = max(step / 2, 0.02), 0

    def obj(x):
        p = dict(best, **dict(zip(FREE, x)))
        if any(not (BOUNDS[k][0] <= p[k] <= BOUNDS[k][1]) for k in FREE):
            return 50.0
        L, mo = safe(p)
        if L < obj.best:
            obj.best = L
            json.dump(dict(loss=L, **dict(p, **FIXED)), open(os.path.join(HERE, "v9_best.json"), "w"), indent=1)
            say(f"nm: loss {L:.4f} | {show(mo)}")
        return L
    obj.best = best_L
    say("== local search done; Nelder-Mead")
    minimize(obj, [best[k] for k in FREE], method="Nelder-Mead",
             options=dict(maxiter=int(sys.argv[3]), adaptive=True, xatol=1e-4, fatol=1e-5))
    say("DONE")
