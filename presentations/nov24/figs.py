"""Nov 24 figures from the v8 model (eps_model_v8.py, v8_results.json) and the 2019 survey aggregates.
Run from this folder: python3 figs.py. Writes fig_capuse.png and fig_size.png."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

E = "../../hopenhayn_project/eps_model/"
R = json.load(open(E + "v8_results.json"))
H = json.load(open("../../bunching/cap_use_hist.json"))
S = json.load(open(E + "baseline/survey_binding.json"))
BLUE, ORANGE, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1F2A3C", "#5F6876", "#D8DEE8"
plt.rcParams.update({"font.family": "Arial", "font.size": 17, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "text.color": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True, "axes.titlecolor": INK,
                     "legend.frameon": False, "savefig.dpi": 200, "savefig.facecolor": "white"})

# 1. Share of the 2019 legal cap used, EPS firms: survey against the model (2019 caps)
labels = list(H["bins"])
survey = 100 * np.array(list(H["bins"].values()))
model = 100 * np.array(R["lpy"]["use_hist"])
short = ["0–10", "10–20", "20–30", "30–40", "40–50", "50–60", "60–70", "70–80", "80–90", "90–99", "100", "over 100"]
x = np.arange(len(labels))
fig, ax = plt.subplots(figsize=(16.0, 5.6))
W = 0.4
for vals, off, c, lab in [(model, -W / 2, BLUE, "Model (random eligibility, full legal cap)"), (survey, W / 2, ORANGE, "Survey, 2019")]:
    bars = ax.bar(x + off, vals, W - 0.05, color=c, label=lab)
    for r, v in zip(bars, vals):
        if v >= 0.5:
            ax.text(r.get_x() + r.get_width() / 2, v + 0.6, f"{v:.0f}", ha="center", fontsize=14, color=INK)
ax.axvline(1.6, color=INK, ls="--", lw=1.4)
ax.text(1.68, ax.get_ylim()[1] * 0.97 if ax.get_ylim()[1] > 30 else 30, "Old model: every plant\nlimited to 21% of its cap",
        fontsize=14, va="top", color=INK)
ax.set_xticks(x, short, fontsize=15)
ax.set_xlabel("EPS workers as a % of the firm's 2019 legal cap", fontsize=16)
ax.set_ylabel("% of EPS firms", fontsize=16)
ax.grid(axis="x", visible=False)
ax.legend(loc="upper right", fontsize=16)
fig.tight_layout()
fig.savefig("fig_capuse.png")

# 2. EPS users by total workers (2019 caps): where they are, and their EPS share
keys = [("0-10", "Under 10"), ("10-20", "10–19"), ("20-50", "20–49"), ("50-100", "50–99"), ("100-200", "100–199"), ("200-300", "200–299")]
ubt, sbt = R["current_2019"]["size"], S["by_total_workers"]
mf = [100 * ubt[k]["share_of_users"] for k, _ in keys]
sf = [100 * sbt[k]["share_of_firms"] for k, _ in keys]
ms = [100 * ubt[k]["eps_share"] for k, _ in keys]
ss = [100 * sbt[k]["eps_share"] for k, _ in keys]
x = np.arange(len(keys))
fig, (a, b) = plt.subplots(1, 2, figsize=(16.0, 5.4))
for vals, off, c, lab in [(mf, -W / 2, BLUE, "Model"), (sf, W / 2, ORANGE, "Survey, 2019")]:
    bars = a.bar(x + off, vals, W - 0.05, color=c, label=lab)
    for r, v in zip(bars, vals):
        a.text(r.get_x() + r.get_width() / 2, v + 1.0, f"{v:.0f}", ha="center", fontsize=14, color=INK)
a.set_title("Where EPS firms are (% of EPS firms)", fontsize=18, loc="left")
a.set_ylim(0, max(max(mf), max(sf)) * 1.2)
a.grid(axis="x", visible=False)
for vals, c, lab in [(ms, BLUE, "Model"), (ss, ORANGE, "Survey, 2019")]:
    b.plot(x, vals, color=c, lw=2.2, marker="o", ms=8, label=lab, markeredgecolor="white", markeredgewidth=1.5)
    for i, v in enumerate(vals):
        b.text(i, v + 2.0, f"{v:.0f}", ha="center", fontsize=14, color=c)
b.set_title("EPS share of workers at those firms (%)", fontsize=18, loc="left")
b.set_ylim(0, max(max(ms), max(ss)) * 1.25)
for axx in (a, b):
    axx.set_xticks(x, [l for _, l in keys], fontsize=15)
    axx.set_xlabel("Total workers", fontsize=15)
a.legend(loc="upper right", fontsize=16)
fig.tight_layout(w_pad=3)
fig.savefig("fig_size.png")
print("cap use model", np.round(model, 1).tolist())
print("size model", [round(v) for v in mf], [round(v) for v in ms])
