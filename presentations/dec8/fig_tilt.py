"""Cap-tilt figure: change in net output against the tilt S of the cap schedule (cap = A * n^S), same quota and
same eligible plants. Reads hopenhayn_project/eps_model/v8_tilt.json; writes fig_tilt.png."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

E = "../../hopenhayn_project/eps_model/"
T = json.load(open(E + "v8_tilt.json"))
X = json.load(open(E + "v8_extra.json"))
runs = sorted(T["runs"], key=lambda d: d["S"])
S = np.array([d["S"] for d in runs])
net = 100 * np.array([d["net_change"] for d in runs])
BLUE, ORANGE, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1F2A3C", "#5F6876", "#D8DEE8"
plt.rcParams.update({"font.family": "Arial", "font.size": 15, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "axes.axisbelow": True, "savefig.dpi": 200, "savefig.facecolor": "white"})
fig, ax = plt.subplots(figsize=(14, 5.6))
ax.axhline(0, color=INK, lw=1)
ax.axhline(100 * X["caps2024"]["price"]["net"], color=ORANGE, ls="--", lw=2)
ax.text(S.min(), 100 * X["caps2024"]["price"]["net"] + 0.012, "For comparison: a permit price (open access), +0.39%", color="#b4491d", fontsize=14)
ax.plot(S, net, color=BLUE, lw=2.5, marker="o", ms=8, markeredgecolor="white", markeredgewidth=1.5, zorder=3)
for s, v, lab in [(0.0, None, "Equal limit\n(S = 0)"), (T["fit_today"]["S"], None, "Today's schedule\n(S ≈ 0.32)")]:
    ax.axvline(s, color=MUTED, ls=":", lw=1.5)
    ax.text(s + 0.03, -0.16, lab, fontsize=13, color=MUTED, va="bottom")
ax.text(-1.0, -0.06, "← small plants get bigger caps", fontsize=13, color=MUTED)
ax.text(0.85, 0.05, "large plants get bigger caps →", fontsize=13, color=MUTED)
ax.set_xlabel("Tilt S of the cap schedule  (cap = A × Korean workers^S;  A keeps total EPS at the quota)", fontsize=14)
ax.set_ylabel("Change in net output vs today (%)", fontsize=14)
ax.set_ylim(-0.17, 0.45)
fig.tight_layout()
fig.savefig("fig_tilt.png")
print(dict(zip(S.tolist(), np.round(net, 4).tolist())))
