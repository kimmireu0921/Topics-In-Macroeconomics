"""Slide-sized figures for Nov 10. Run from this folder: python3 figs.py. Reads the baseline outputs
in hopenhayn_project/eps_model/baseline and writes fig_*.png here. Sized so 24px text on the slide
is about 17pt here at figure width = displayed px / 100."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

B = "../../hopenhayn_project/eps_model/baseline/"
D = json.load(open(B + "diagnostics.json"))
S = json.load(open(B + "survey_binding.json"))
G = json.load(open(B + "bumpy_line.json"))
R = D["runs"]
CUR, NOR = R["current_2024"], R["no_rule"]
BLUE, ORANGE, AQUA, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1baf7a", "#1F2A3C", "#5F6876", "#D8DEE8"
plt.rcParams.update({"font.family": "Arial", "font.size": 17, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "text.color": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True, "axes.titlecolor": INK,
                     "legend.frameon": False, "savefig.dpi": 200, "savefig.facecolor": "white"})


def log_axis(ax, s):
    ax.set_xscale("log")
    ax.set_yscale("symlog", linthresh=1)
    ax.set_ylim(0, 3000)
    ax.set_xlim(s.min(), s.max())
    ax.set_xticks([1, 2, 5, 10], ["1", "2", "5", "10"])
    ax.minorticks_off()
    ax.set_yticks([0, 1, 10, 100, 1000], ["0", "1", "10", "100", "1,000"])


# 1. Policy functions: manual-intensive plants, current rule against their preferred plan
s = np.array(CUR["s_grid"])
cur, free = CUR["policy"]["manual"]["actual"], CUR["policy"]["manual"]["free"]
pct = CUR["pct"]["manual"]
fig, axes = plt.subplots(1, 3, figsize=(16.64, 4.9))
for ax, title, f in [(axes[0], "EPS workers, m", lambda p: np.array(p["m"])), (axes[1], "Korean manual workers, k", lambda p: np.array(p["k"])),
                     (axes[2], "All workers, h + k + m", lambda p: np.array(p["h"]) + np.array(p["k"]) + np.array(p["m"]))]:
    ax.plot(s, f(free), color=ORANGE, ls="--", lw=2.5, label="No limit, free permits", drawstyle="steps-post")
    ax.plot(s, f(cur), color=BLUE, lw=2.5, label="Current rule", drawstyle="steps-post")
    log_axis(ax, s)
    ax.set_title(title, loc="left", fontweight="bold", fontsize=18)
    ax.set_xlabel("Plant productivity s (log scale)")
    for q in ("50", "90", "99"):
        ax.axvline(pct[q], color=MUTED, lw=1, ls=(0, (2, 3)), zorder=0)
        ax.text(pct[q], 2000, f"p{q}", color=MUTED, fontsize=15, ha="center", va="bottom", clip_on=False)
# Labelled points at the median (p50) and top 1% (p99) plants: same grid point as the slide text
for j, f in enumerate([lambda p, i: p["m"][i], lambda p, i: p["k"][i], lambda p, i: p["h"][i] + p["k"][i] + p["m"][i]]):
    ax = axes[j]
    for q in ("50", "99"):
        i = int(np.searchsorted(s, pct[q]))
        for pol, c, dy in [(free, ORANGE, 1.6), (cur, BLUE, 0.55)]:
            v = f(pol, i)
            if v < 0.5 and pol is free and j == 1:
                continue                      # orange is 0 everywhere in the middle panel
            ax.plot(s[i], v, "o", ms=9, color=c, markeredgecolor="white", markeredgewidth=1.5, zorder=5)
            if pol is free:
                off, ha = (-10, 8), "right"          # orange: above left
            elif v < 0.5:
                off, ha = (-10, 10), "right"         # a zero sits on the axis: label above left
            else:
                off, ha = (10, -24), "left"          # blue: below right, clear of the rising lines
            ax.annotate(f"{v:.0f}", (s[i], v), xytext=off, textcoords="offset points", ha=ha, fontsize=15,
                        fontweight="bold", color=c, zorder=6,
                        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))
axes[1].set_facecolor("#EEF3FA")
axes[1].set_title("Korean manual workers, k  (key panel)", loc="left", fontweight="bold", fontsize=18)
axes[1].legend(loc="lower right", bbox_to_anchor=(1.0, 0.09), fontsize=16)
fig.tight_layout()
fig.savefig("fig_policy.png")
plt.close(fig)

# 2. Value of a permit against its price
P6 = D["params"]
w, p, psi, xi = NOR["w"], NOR["x"], P6["psi"], P6["xi"]
h = np.geomspace(1, 3000, 400)
cut = (p / (w * psi)) ** (-1 / xi) - 1
fig, ax = plt.subplots(figsize=(9.6, 5.2))
ax.plot(h, w * psi * (1 + h) ** (-xi), color=BLUE, lw=2.5)
ax.axhline(p, color=ORANGE, lw=2.5)
ax.axvline(cut, color=MUTED, lw=1, ls=(0, (3, 3)))
ax.text(1.15, 0.27, f"Permit price p = {p:.2f}", color=INK, va="top", fontsize=17)
ax.text(1.15, 0.72, "Value of one permit\n= w × premium", color=INK, va="top", fontsize=17)
ax.text(cut * 1.15, 0.72, f"Past about {cut:.0f} core Koreans,\nthe permit is not worth its price", color=INK, va="top", fontsize=17)
ax.set_xscale("log")
ax.set_xticks([1, 10, 100, 1000], ["1", "10", "100", "1,000"])
ax.minorticks_off()
ax.set_xlim(1, 3000)
ax.set_ylim(0, 0.8)
ax.set_xlabel("Core Korean workers at the plant, h (log scale)")
ax.set_ylabel("Model units per worker")
fig.tight_layout()
fig.savefig("fig_permit.png")
plt.close(fig)

# 3. Is the cap binding? Survey
bins = list(S["bins"])
x = np.arange(len(bins))
fig, ax = plt.subplots(figsize=(16.64, 4.5))
W = 0.27
for i, (k, c, lab) in enumerate([("at_or_above", BLUE, "At or above the cap, 2019 caps"), ("want_past_2019", ORANGE, "Would go past the cap, 2019 caps"),
                                 ("want_past_2024", AQUA, "Would go past the cap, 2024 caps on the same firms")]):
    v = [100 * S["bins"][b][k] for b in bins]
    bars = ax.bar(x + (i - 1) * W, v, W - 0.03, color=c, label=lab)
    for r, val in zip(bars, v):
        ax.text(r.get_x() + r.get_width() / 2, val + 0.8, f"{val:.0f}", ha="center", fontsize=16)
ax.set_xticks(x, [f"{b}  ({S['bins'][b]['firms']} firms)" for b in bins])
ax.set_ylabel("Share of firms, %")
ax.set_xlabel("Korean workers at the firm")
ax.set_ylim(0, 56)
ax.grid(axis="x", visible=False)
ax.legend(loc="upper left", ncol=3, fontsize=16)
fig.tight_layout()
fig.savefig("fig_binding.png")
plt.close(fig)

# 4. EPS workers each plant has and wants, 2019 caps
labs = ["0-5", "6-10", "11-30", "31-50", "51-100", "101-300"]
T = R["current_2019"]["size_table"]
fig, axes = plt.subplots(1, 2, figsize=(16.64, 4.5), sharey=True)
for ax, title, have, want in [(axes[0], "Model (manual-intensive plants)", [T[b]["m_manual"] for b in labs], [T[b]["free_m"] for b in labs]),
                              (axes[1], "Survey (firms using EPS)", [S["bins"][b]["eps"] for b in bins], [S["bins"][b]["wanted"] for b in bins])]:
    ax.plot(labs, want, color=ORANGE, lw=2.5, marker="o", ms=9, mec="white", mew=2, label="Wants with no limit")
    ax.plot(labs, have, color=BLUE, lw=2.5, marker="o", ms=9, mec="white", mew=2, label="Has now")
    for i, v in enumerate(want):
        ax.text(i, v * 1.22, f"{v:.0f}", ha="center", fontsize=16)
    for i, v in enumerate(have):
        ax.text(i, v / 1.5, f"{v:.0f}", ha="center", va="top", fontsize=16)
    ax.set_yscale("log")
    ax.set_ylim(1, 500)
    ax.set_yticks([1, 10, 100], ["1", "10", "100"])
    ax.minorticks_off()
    ax.set_xlabel("Korean workers at the plant")
    ax.grid(axis="x", visible=False)
    ax.set_title(title, loc="left", fontweight="bold", fontsize=18)
axes[0].set_ylabel("EPS workers per plant (log scale)")
axes[0].legend(loc="upper left", fontsize=16)
fig.tight_layout()
fig.savefig("fig_wants.png")
plt.close(fig)

# 5. The no-size-rule line on coarser and finer grids
def pick(reg, nx, nz, nh=None):
    return next(g for g in G if g["reg"] == reg and g["grid"]["nx"] == nx and g["grid"]["nz"] == nz and g["grid"].get("nh") == nh)


fig, ax = plt.subplots(figsize=(9.6, 5.2))
for (nx, nz, nh), c, lab, ls in [((48, 21, None), BLUE, "On the slide last week (48 × 21)", "-"), ((96, 41, 1280), ORANGE, "Finer productivity and size grids", "-")]:
    g = pick("neutral", nx, nz, nh)
    e, d = np.array(g["edges"]), np.array(g["density"])
    ax.stairs(d, e, color=c, lw=2.5, label=lab, ls=ls, baseline=None)
for t in (50, 100, 150, 200):
    ax.axvline(t, color=MUTED, lw=1, ls=(0, (3, 3)), zorder=0)
ax.set_yscale("log")
ax.set_xlim(20, 400)
ax.set_ylim(1e-6, 3e-3)
ax.set_xlabel("Korean core workers at the plant, h")
ax.set_ylabel("Share of plants per worker (log scale)")
ax.legend(loc="lower left", fontsize=16)
fig.tight_layout()
fig.savefig("fig_bumpy.png")
plt.close(fig)
print("cutoff", round(cut, 1), "done")
