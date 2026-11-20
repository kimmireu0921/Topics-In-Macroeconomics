"""Standalone figure for Prof. Hur: EPS workers / legal cap among plants with at least one EPS worker,
model (v8, 2019 caps) against the 2019 survey. Writes capuse_histogram.pdf and .png."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

R = json.load(open("../../hopenhayn_project/eps_model/v8_capuse_hist.json"))
plt.rcParams.update({"font.family": "Times New Roman", "font.size": 12, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#dddddd", "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "legend.frameon": False, "savefig.dpi": 300, "savefig.facecolor": "white"})
d, m = 100 * np.array(R["data"]["share"]), 100 * np.array(R["model"]["share"])
x, W = np.arange(len(d)), 0.4
fig, ax = plt.subplots(figsize=(9.5, 4.6))
for vals, off, c, lab in [(d, -W / 2, "#d9622b", f"Data: 2019 EPS survey ({R['data']['firms']} firms)"), (m, W / 2, "#2a78d6", "Model")]:
    bars = ax.bar(x + off, vals, W - 0.04, color=c, label=lab)
    for r, v in zip(bars, vals):
        if v >= 0.5:
            ax.text(r.get_x() + r.get_width() / 2, v + 0.5, f"{v:.0f}", ha="center", fontsize=9.5)
ax.set_xticks(x, ["0–10", "10–20", "20–30", "30–40", "40–50", "50–60", "60–70", "70–80", "80–90", "90–<100", "100", ">100"], fontsize=10.5)
ax.set_xlabel("EPS workers as a percentage of the plant's legal cap (2019 caps)")
ax.set_ylabel("Percent of plants with at least one EPS worker")
ax.grid(axis="x", visible=False)
ax.set_ylim(0, max(d.max(), m.max()) * 1.28)
ax.legend(loc="upper right")
s = lambda r: f"mean {100 * r['mean']:.0f}%, median {100 * r['median']:.0f}%, at or above cap {100 * r['at_or_above_cap']:.0f}%"
ax.text(0.01, 0.97, f"Data: {s(R['data'])}\nModel: {s(R['model'])}", transform=ax.transAxes, va="top", fontsize=10.5)
fig.tight_layout()
fig.savefig("capuse_histogram.pdf")
fig.savefig("capuse_histogram.png")
