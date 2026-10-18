"""Where the EPS workers go: share of all EPS workers by the number of Korean workers
at the plant, under the current rule (2024 caps) and the size-neutral allocation
(same quota, permit price). Uses the recalibration in recal_best.json and writes
eps_by_size.json, which proposal/make_fig.py turns into Figure 2. Runs in ~30 s.
"""
import json
import numpy as np
from run_eps import build, NAMES

EDGES = [0, 5, 10, 20, np.inf]
LABELS = ["Under 5", "5–9", "10–19", "20 or more"]

d = json.load(open("recal_best.json"))
p = {k: d[k] for k in NAMES}
res = dict(bins=LABELS)
for reg in ("current", "neutral"):
    r = build(p).solve(reg)
    cat = lambda key: np.concatenate([B[key] for B in r["out"]["blocks"]])
    mu, h, k, m, y = cat("mu"), cat("h"), cat("k"), cat("m"), cat("y")
    n = h + k                                      # Korean workers at the plant
    eps = mu * m
    res[reg] = dict(
        share=[float(eps[(n >= a) & (n < b)].sum() / eps.sum()) for a, b in zip(EDGES[:-1], EDGES[1:])],
        y_per_worker=float(eps @ (y / (n + m)) / eps.sum()),   # EPS-weighted output per worker
        users=r["users"], net_Y=r["net_Y"], eq_error=r["eq_error"])
res["y_per_worker_gain"] = res["neutral"]["y_per_worker"] / res["current"]["y_per_worker"] - 1
json.dump(res, open("eps_by_size.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(res, indent=1, ensure_ascii=False))
