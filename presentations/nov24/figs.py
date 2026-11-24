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

# 1. Share of the 2019 legal cap used, EPS firms: survey against the model (2019 caps), with explanatory labels
labels = list(H["bins"])
survey = 100 * np.array(list(H["bins"].values()))
model = 100 * np.array(R["lpy"]["use_hist"])
short = ["0–10%", "10–20%", "20–30%", "30–40%", "40–50%", "50–60%", "60–70%", "70–80%", "80–90%", "90–99%", "100%\n(at cap)", "over\n100%"]
x = np.arange(len(labels))
fig, ax = plt.subplots(figsize=(16.0, 5.6))
YMAX = 52
ax.set_ylim(0, YMAX)
ax.set_xlim(-0.6, len(labels) - 0.4)
GREY = "#EEF1F5"
ax.axvspan(-0.5, 2.5, color=GREY, zorder=0)
ax.axvspan(9.5, 11.5, color=GREY, zorder=0)
W = 0.4
for vals, off, c, lab in [(survey, -W / 2, ORANGE, "Survey: real EPS firms in 2019 (772)"), (model, W / 2, BLUE, "Our model")]:
    bars = ax.bar(x + off, vals, W - 0.05, color=c, label=lab, zorder=2)
    for r, v in zip(bars, vals):
        if v >= 0.5:
            ax.text(r.get_x() + r.get_width() / 2, v + 0.6, f"{v:.0f}%", ha="center", fontsize=13, color=INK, zorder=3)
below_s, below_m = survey[:3].sum(), model[:3].sum()
at_s, at_m = survey[10:].sum(), model[10:].sum()
ax.text(1.0, YMAX - 1.5, f"Below 30% of the cap\nsurvey {below_s:.0f}%, model {below_m:.0f}%", ha="center", va="top", fontsize=14, color=INK, fontweight="bold")
ax.text(10.5, YMAX - 1.5, f"At or above the cap\nsurvey {at_s:.0f}%, model {at_m:.0f}%", ha="center", va="top", fontsize=14, color=INK, fontweight="bold")
ax.axvline(1.6, color=INK, ls="--", lw=1.6, zorder=1, ymax=0.56)
ax.annotate("Old model (last week):\nevery plant at 21%\nof its cap", xy=(1.6, 28), xytext=(-0.45, 36), fontsize=13, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.3), va="center", ha="left")
ax.axvline(5.5, color=ORANGE, ls=":", lw=2.2, zorder=1, ymax=0.62)
ax.text(5.55, 30, "Survey median:\nhalf of firms use\nless than 60%", fontsize=13, color="#b4491d", va="center")
ax.set_xticks(x, short, fontsize=14)
ax.set_xlabel("Share of its legal cap a firm uses  (EPS workers ÷ legal cap, 2019 caps)", fontsize=15)
ax.set_ylabel("% of firms with at least\none EPS worker", fontsize=15)
ax.grid(axis="x", visible=False)
ax.legend(loc="upper center", bbox_to_anchor=(0.62, 1.0), fontsize=15, ncol=2)
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
for i in range(len(keys)):                    # the higher point's label above, the lower one's below
    for v, other, c in ((ms[i], ss[i], BLUE), (ss[i], ms[i], ORANGE)):
        above = v >= other
        b.text(i, v + (2.0 if above else -2.2), f"{v:.0f}", ha="center", va="bottom" if above else "top", fontsize=14, color=c)
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
