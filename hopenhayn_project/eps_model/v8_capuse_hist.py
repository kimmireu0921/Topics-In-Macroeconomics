"""Histogram asked for by Prof. Hur: among plants with at least one EPS worker, EPS workers / legal cap,
in the model (v8, 2019 caps, the caps the survey firms faced) and in the 2019 survey.
Writes v8_capuse_hist.json. Model plants are weighted by their mass in the stationary distribution."""
import json

import numpy as np

from run_eps import cap_2019
from run_v8 import build, M, NAMES, flat

EDGES = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, .99999, 1.00001, np.inf]
LABELS = ["0–10", "10–20", "20–30", "30–40", "40–50", "50–60", "60–70", "70–80", "80–90", "90–<100", "100 (at cap)", "over 100"]
p = json.load(open("v8_best.json"))
p = {k: p[k] for k in NAMES}
mod = build(p, M, cap=cap_2019)
out = mod.solve("current")["out"]
mu, h, k, m = flat(out, "mu"), flat(out, "h"), flat(out, "k"), flat(out, "m")
u = m >= 1                                           # at least one EPS worker, as in the survey
use = m[u] / mod.cap(h[u] + k[u])
w = mu[u] / mu[u].sum()
o = np.argsort(use)
median = float(use[o][np.searchsorted(np.cumsum(w[o]), 0.5)])
model = dict(share=np.histogram(use, bins=EDGES, weights=w)[0].tolist(), mean=float(w @ use), median=median,
             at_or_below_21=float(w[use <= 0.21].sum()), at_or_above_cap=float(w[use >= 1 - 1e-6].sum()),
             share_of_users_with_m_below_1=float(mu[(m > 0) & (m < 1)].sum() / mu[m > 0].sum()))
H = json.load(open("../../bunching/cap_use_hist.json"))
data = dict(share=list(H["bins"].values()), mean=H["mean"], median=H["median"], at_or_below_21=H["at_or_below_theta_0_21"],
            at_or_above_cap=H["at_or_above_cap"], firms=H["firms"])
json.dump(dict(labels=LABELS, model=model, data=data), open("v8_capuse_hist.json", "w"), indent=1)
print(json.dumps(dict(model={k: v for k, v in model.items() if k != "share"}, data={k: v for k, v in data.items() if k != "share"}), indent=1))
print("model", np.round(100 * np.array(model["share"]), 1).tolist())
print("data ", np.round(100 * np.array(data["share"]), 1).tolist())
