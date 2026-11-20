"""Histogram asked for on Nov 17: among EPS firms in the 2019 survey (all 772 use at least one EPS
worker), the share of the 2019 legal cap each firm uses (EPS workers now / cap from its listed
Korean workers). The model's rule lets every plant use theta = 0.21 of its cap, so the model would
put its users in one spike at 0.21. Aggregates only; the survey file stays outside the repository.

  python3 cap_use_hist.py   -> cap_use_hist.png, cap_use_hist.json
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_stata(os.path.expanduser("~/EPS_data/eps.dta"), convert_categoricals=False)
listed, eps = df["korean"].astype(float), df["q13_1a"].astype(float)
cap = np.select([listed <= 5, listed <= 10, listed <= 30, listed <= 50, listed <= 100, listed <= 150, listed <= 200],
                [5, 7, 10, 12, 15, 20, 25], default=30)
u = (eps / cap)[eps >= 1].dropna()

cnt = np.histogram(np.clip(u, 0, 1.0001), bins=[0, .1, .2, .3, .4, .5, .6, .7, .8, .9, .99999, 1.00001, np.inf])[0]   # exact edges: a firm at 60% falls in 60–70
# bins: 0-0.1, ..., 0.8-0.9, 0.9-<1, exactly 1, above 1
labels = [f"{a:.0f}–{a + 10:.0f}%" for a in range(0, 90, 10)] + ["90–<100%", "exactly 100%", "above 100%"]
share = cnt / len(u)
out = dict(firms=int(len(u)), bins=dict(zip(labels, [round(float(s), 4) for s in share])),
           median=float(u.median()), mean=float(u.mean()), at_or_below_theta_0_21=float((u <= 0.21).mean()),
           at_or_above_cap=float((u >= 1).mean()), at_least_90pct=float((u >= 0.9).mean()))
json.dump(out, open("cap_use_hist.json", "w"), indent=1)
print(json.dumps(out, indent=1))

fig, ax = plt.subplots(figsize=(10, 5.2), dpi=150)
col = ["#2a78d6"] * 9 + ["#2a78d6", "#eb6834", "#eb6834"]
ax.bar(range(len(share)), 100 * share, color=col, width=0.8)
for i, s in enumerate(share):
    ax.text(i, 100 * s + 0.4, f"{100 * s:.1f}%" if 100 * s < 1 else f"{100 * s:.0f}%", ha="center", fontsize=11, color="#222")
ax.axvline(2 - 0.4 + 0.1 * 0.8, color="#222", ls="--", lw=1.5)   # 21% sits just inside the 20–30% bin
ax.set_ylim(0, 25)
ax.text(1.72, 24.5, " old model rule (v6, until Nov 17): every plant limited to 21% of its cap", fontsize=11, va="top")
ax.set_xticks(range(len(share)), labels, rotation=35, ha="right", fontsize=10)
ax.set_ylabel("% of EPS firms", fontsize=12)
ax.set_xlabel("EPS workers as a share of the firm's 2019 legal cap", fontsize=12)
ax.set_title(f"Survey: how much of their legal cap EPS firms use (2019, {len(u)} firms)", fontsize=13)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color="#ddd"); ax.set_axisbelow(True)
fig.text(0.01, 0.01, "Source: KDI–World Bank EPS survey 2019; caps from Lee, Peri and Yang, Table 4. Orange: at or above the cap.\nSpikes at 20, 40, 60, 80% come from small caps (cap 5: 1, 2, 3, 4 workers).",
         fontsize=9, color="#444")
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("cap_use_hist.png")
