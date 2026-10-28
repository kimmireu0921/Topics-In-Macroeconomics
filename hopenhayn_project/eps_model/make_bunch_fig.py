"""Bunching histogram in model v5: plants by number of Korean core workers, current
rule vs. the same quota without the size rule. Reads v5_results.json (or the file
given), writes bunching_v5.png and bunching_v5.svg."""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

res = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "v5_results.json"))
ex = res["experiments"]
BLUE, AQUA, INK, MUTED, GRID = "#2a78d6", "#1baf7a", "#1F2A3C", "#5F6876", "#D8DEE8"

fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
for name, color, label, lw in [("size-neutral, same quota (by price)", AQUA, "Same quota, no size rule", 2.0),
                               ("current rule", BLUE, "Current rule (2024 caps)", 2.0)]:
    b = ex[name]["bunching"]
    e = np.array(b["hist_edges"])
    dens = np.array(b["hist"]) / np.diff(e)                 # share of plants per worker
    keep = (e[:-1] >= 20) & (e[:-1] < 380)
    ax.stairs(dens[keep], e[np.r_[keep, False] | np.r_[False, keep]], color=color, lw=lw, label=label, baseline=None)
for t in (50, 100, 150, 200):
    ax.axvline(t, color=MUTED, lw=1, ls=(0, (3, 3)), zorder=0)
    ax.text(t + 2, 2.2e-3, f"cap step {t}", color=MUTED, fontsize=9, va="top")
ax.axvline(300, color=MUTED, lw=1, ls=(0, (3, 3)), zorder=0)
ax.text(298, 2.2e-3, "eligible < 300", color=MUTED, fontsize=9, va="top", ha="right")
ax.set_yscale("log")
ax.set_ylim(1e-6, 3e-3)
ax.set_xlim(20, 400)
ax.set_xlabel("Korean core workers at the plant (h)", color=INK)
ax.set_ylabel("Share of plants per worker (log scale)", color=INK)
ax.grid(axis="y", color=GRID, lw=0.6)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(GRID)
ax.tick_params(colors=MUTED)
ax.legend(frameon=False, loc="lower left", labelcolor=INK)
fig.tight_layout()
fig.savefig("bunching_v5.png")
fig.savefig("bunching_v5.svg")
print("saved")
