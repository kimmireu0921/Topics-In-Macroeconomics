"""Slide 46 chart: model EPS users against the 2019 survey by total workers (2019 caps).
Run from this folder: python3 fig_users_size.py. Writes fig_users_size.png."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

B = "../../hopenhayn_project/eps_model/baseline/"
D = json.load(open(B + "diagnostics.json"))
S = json.load(open(B + "survey_binding.json"))
ubt, sbt = D["runs"]["current_2019"]["users_by_total"], S["by_total_workers"]
keys = [("0-10", "Under 10"), ("10-20", "10–19"), ("20-50", "20–49"), ("50-100", "50–99"), ("100-200", "100–199"), ("200-300", "200–299")]
BLUE, ORANGE, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1F2A3C", "#5F6876", "#D8DEE8"
plt.rcParams.update({"font.family": "Arial", "font.size": 17, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "text.color": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True, "axes.titlecolor": INK,
                     "legend.frameon": False, "savefig.dpi": 200, "savefig.facecolor": "white"})
mf = [100 * ubt[k]["share_of_users"] for k, _ in keys]
sf = [100 * sbt[k]["share_of_firms"] for k, _ in keys]
ms = [100 * ubt[k]["eps_share"] for k, _ in keys]
ss = [100 * sbt[k]["eps_share"] for k, _ in keys]
labs = [l for _, l in keys]
x = np.arange(len(keys))
fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 5.2))
W = 0.38
for vals, off, c, lab in [(mf, -W / 2, BLUE, "Model"), (sf, W / 2, ORANGE, "Survey")]:
    bars = a.bar(x + off, vals, W - 0.04, color=c, label=lab)
    for r, v in zip(bars, vals):
        a.text(r.get_x() + r.get_width() / 2, v + 1.0, f"{v:.0f}", ha="center", fontsize=14, color=INK)
a.set_title("Where EPS firms are\n(% of EPS firms in each group)", fontsize=18, loc="left")
a.set_ylim(0, 62)
a.grid(axis="x", visible=False)
for vals, c, lab in [(ms, BLUE, "Model"), (ss, ORANGE, "Survey")]:
    b.plot(x, vals, color=c, lw=2.2, marker="o", ms=8, label=lab, markeredgecolor="white", markeredgewidth=1.5)
for i, (m, v) in enumerate(zip(ms, ss)):
    b.text(i, v + 2.2, f"{v:.0f}", ha="center", fontsize=14, color=INK)
    b.text(i, m - 5.2, f"{m:.0f}", ha="center", fontsize=14, color=INK)
b.set_title("EPS share of workers\nat those firms (%)", fontsize=18, loc="left")
b.set_ylim(0, 60)
for ax in (a, b):
    ax.set_xticks(x, labs, rotation=35, ha="right", fontsize=15)
    ax.set_xlabel("Total workers", fontsize=15)
    ax.tick_params(axis="y", labelsize=15)
a.legend(loc="upper right", fontsize=16)
fig.tight_layout(w_pad=2.5)
fig.savefig("fig_users_size.png")
print("model firms", [round(v) for v in mf], "survey firms", [round(v) for v in sf])
print("model share", [round(v) for v in ms], "survey share", [round(v) for v in ss])
