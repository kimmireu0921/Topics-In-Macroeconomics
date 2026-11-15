"""Why the top 1% manual-intensive plant changes size between today's rule and the price
experiment (v6_best). Plans for the same productivity (the 99th percentile among
manual-intensive plants under today's rule) at each regime's wage and at the other wage, and
with no EPS at all. Writes baseline/top_plant.json. Run from hopenhayn_project/eps_model.
"""
import json
import sys

import numpy as np

sys.argv = sys.argv[:1] + ["none"]          # v6_free_flat runs its jobs only for known commands
from baseline_diagnostics import policy
from v6_free_flat import build

FF = {x["name"]: x for x in json.load(open("baseline/free_flat.json")) if not x["grid"]}
sg = np.array(FF["current"]["sg"])
mod = build("base")
wc, th = FF["current"]["w"], FF["current"]["x"]
wp, p = FF["price"]["w"], FF["price"]["x"]
rows = []
for label, w, x, reg in [("current rule, today's wage", wc, th, "current"), ("price, price-economy wage", wp, p, "neutral"),
                         ("price, today's wage", wc, p, "neutral"), ("no EPS, today's wage", wc, 0.0, "none"),
                         ("no EPS, price-economy wage", wp, 0.0, "none")]:
    h, k, m = (float(a[2]) for a in policy(mod, 1, w, x, reg, sg))
    rows.append(dict(label=label, w=float(w), h=h, k=k, m=m, total=h + k + m))
    print(f"{label:<28} w {w:.4f} h {h:.3f} k {k:.1f} m {m:.2f} total {h + k + m:.1f}")
json.dump(dict(s=float(sg[2]), cap_step=150, rows=rows),
          open("baseline/top_plant.json", "w"), indent=1)
