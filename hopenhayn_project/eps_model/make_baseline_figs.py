"""Figures for the baseline diagnostics. Reads baseline/diagnostics.json and
baseline/survey_binding.json; writes baseline/fig_*.png."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

D = json.load(open("baseline/diagnostics.json"))
S = json.load(open("baseline/survey_binding.json"))
R = D["runs"]
CUR, NOR = R["current_2024"], R["no_rule"]
BLUE, ORANGE, AQUA, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1baf7a", "#1F2A3C", "#5F6876", "#D8DEE8"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": GRID, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
                     "legend.frameon": False, "savefig.dpi": 200, "savefig.bbox": "tight", "savefig.facecolor": "white"})


def total(p):
    return np.array(p["h"]) + np.array(p["k"]) + np.array(p["m"])


# 1. Policy functions, manual-intensive plants, at the prices of each solved economy
s = np.array(CUR["s_grid"])
s2 = np.array(NOR["s_grid"])
cur, free, nor = CUR["policy"]["manual"]["actual"], CUR["policy"]["manual"]["free"], NOR["policy"]["manual"]["actual"]
pct = CUR["pct"]["manual"]
fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.3))
series = [(s, cur, BLUE, "-", "Current rule"), (s, free, AQUA, "--", "No limit, free permits (not an equilibrium)"),
          (s2, nor, ORANGE, "-", "Same quota, no size rule (permit price)")]
for ax, title, f in [(axes[0], "EPS workers", lambda p: np.array(p["m"])),
                     (axes[1], "Korean manual workers", lambda p: np.array(p["k"])),
                     (axes[2], "Total workers", total)]:
    for xs, p, c, ls, lab in series:
        ax.plot(xs, f(p), color=c, ls=ls, lw=2, label=lab, drawstyle="steps-post")
    ax.set_xscale("log")
    ax.set_yscale("symlog", linthresh=1)
    ax.set_ylim(0, 3000)
    ax.set_xlim(s.min(), s.max())
    ax.set_xticks([1, 2, 5, 10], ["1", "2", "5", "10"])
    ax.minorticks_off()
    ax.set_yticks([0, 1, 10, 100, 1000])
    ax.set_yticklabels(["0", "1", "10", "100", "1,000"])
    ax.set_title(title, loc="left", color=INK, fontsize=12, fontweight="bold")
    ax.set_xlabel("Plant productivity s (log scale)")
    for q in ("50", "90", "99"):
        ax.axvline(pct[q], color=MUTED, lw=1, ls=(0, (2, 3)), zorder=0)
        ax.text(pct[q], 2300, f"p{q}", color=MUTED, fontsize=9, ha="center", va="bottom")
fig.legend(*axes[0].get_legend_handles_labels(), loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.07))
fig.tight_layout()
fig.savefig("baseline/fig_policy_manual.png")
plt.close(fig)

# 2. Light plants: same productivity, but no manual work
light_c, light_m = CUR["policy"]["light"]["actual"], CUR["policy"]["manual"]["actual"]
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.plot(s, np.array(light_m["k"]) + np.array(light_m["m"]), color=ORANGE, lw=2, drawstyle="steps-post", label="Manual-intensive plant")
ax.plot(s, np.array(light_c["k"]) + np.array(light_c["m"]), color=BLUE, lw=2, drawstyle="steps-post", label="Light plant")
ax.set_xscale("log")
ax.set_yscale("symlog", linthresh=1)
ax.set_ylim(0, 3000)
ax.set_yticks([0, 1, 10, 100, 1000])
ax.set_yticklabels(["0", "1", "10", "100", "1,000"])
ax.set_xlim(s.min(), s.max())
ax.set_xticks([1, 2, 5, 10], ["1", "2", "5", "10"])
ax.minorticks_off()
ax.set_xlabel("Plant productivity s (log scale)")
ax.set_title("Manual workers hired, current rule", loc="left", color=INK, fontsize=12, fontweight="bold")
ax.legend(loc="upper left")
fig.savefig("baseline/fig_manual_work_by_type.png")
plt.close(fig)

# 3. Value of one permit by core Koreans, against the permit price, this version and version 5
P5 = json.load(open("v5_best.json"))
R5 = json.load(open("v5_results.json"))["experiments"]["size-neutral, same quota (by price)"]
P6 = D["params"]
h = np.geomspace(1, 3000, 400)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharex=True, sharey=True)
for ax, title, w, p, psi, xi, c in [(axes[0], "Corrected model (version 6)", NOR["w"], NOR["x"], P6["psi"], P6["xi"], BLUE),
                                    (axes[1], "Version 5", R5["w"], R5["x"], P5["psi"], P5["xi"], BLUE)]:
    v = w * psi * (1 + h) ** (-xi)
    cut = (p / (w * psi)) ** (-1 / xi) - 1
    ax.plot(h, v, color=c, lw=2, label="Value of one permit = wage × premium")
    ax.axhline(p, color=ORANGE, lw=2, label="Permit price p")
    ax.axvline(cut, color=MUTED, lw=1, ls=(0, (3, 3)))
    ax.annotate(f"past about {round(cut, -2 if cut > 100 else 0):,.0f} core Koreans,\nplants stop using EPS", (cut, p), xytext=(-8, -46), textcoords="offset points",
                ha="right" if cut > 100 else "left", fontsize=10, color=INK) if cut > 100 else ax.annotate(
        f"past about {cut:,.0f} core Koreans,\nplants stop using EPS", (cut, p), xytext=(8, 40), textcoords="offset points", ha="left", fontsize=10, color=INK)
    ax.set_xscale("log")
    ax.set_xticks([1, 10, 100, 1000])
    ax.set_xticklabels(["1", "10", "100", "1,000"])
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Core Korean workers at the plant (log scale)")
    ax.set_title(title, loc="left", color=INK, fontsize=12, fontweight="bold")
axes[0].set_ylabel("Model units per worker, per year")
fig.legend(*axes[0].get_legend_handles_labels(), loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.07))
fig.tight_layout()
fig.savefig("baseline/fig_permit_value.png")
plt.close(fig)

# 4. Is the cap binding? Survey
bins = list(S["bins"])
x = np.arange(len(bins))
fig, ax = plt.subplots(figsize=(10, 4.4))
W = 0.26
rows = [("at_or_above", BLUE, "At or above the cap, 2019 caps"), ("want_past_2019", ORANGE, "Would go past the cap if they could, 2019 caps"),
        ("want_past_2024", AQUA, "Would go past the cap if they could, 2024 caps on the same firms")]
for i, (k, c, lab) in enumerate(rows):
    v = [100 * S["bins"][b][k] for b in bins]
    bars = ax.bar(x + (i - 1) * W, v, W - 0.02, color=c, label=lab)
    for r, val in zip(bars, v):
        ax.text(r.get_x() + r.get_width() / 2, val + 0.7, f"{val:.0f}", ha="center", color=INK, fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels([f"{b}\n({S['bins'][b]['firms']} firms)" for b in bins])
ax.set_ylabel("Share of firms in the group, %")
ax.set_xlabel("Korean workers at the firm")
ax.set_ylim(0, 58)
ax.grid(axis="x", visible=False)
ax.legend(loc="upper left")
fig.savefig("baseline/fig_binding_survey.png")
plt.close(fig)

# 5. EPS workers each plant has and wants, 2019 caps: model and survey on one scale
labs = ["0-5", "6-10", "11-30", "31-50", "51-100", "101-300"]
T = R["current_2019"]["size_table"]
sb = list(S["bins"])
x = np.arange(len(labs))
fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), sharey=True)
for ax, title, have, want in [(axes[0], "Model (manual-intensive plants)", [T[b]["m_manual"] for b in labs], [T[b]["free_m"] for b in labs]),
                              (axes[1], "Survey (firms using EPS)", [S["bins"][b]["eps"] for b in sb], [S["bins"][b]["wanted"] for b in sb])]:
    ax.plot(x, want, color=ORANGE, lw=2, marker="o", ms=8, mec="white", mew=1.5, label="Wants with no limit")
    ax.plot(x, have, color=BLUE, lw=2, marker="o", ms=8, mec="white", mew=1.5, label="Has now")
    for i, b in enumerate(want):
        ax.text(i, b * 1.2, f"{b:.0f}", ha="center", color=INK, fontsize=10)
    for i, a in enumerate(have):
        ax.text(i, a / 1.42, f"{a:.0f}", ha="center", color=INK, fontsize=10)
    ax.set_yscale("log")
    ax.set_ylim(1, 400)
    ax.set_yticks([1, 10, 100], ["1", "10", "100"])
    ax.minorticks_off()
    ax.set_xticks(x, labs)
    ax.set_xlabel("Korean workers at the plant")
    ax.grid(axis="x", visible=False)
    ax.set_title(title, loc="left", color=INK, fontsize=12, fontweight="bold")
axes[0].set_ylabel("EPS workers per plant (log scale)")
axes[0].legend(loc="upper left")
fig.tight_layout()
fig.savefig("baseline/fig_wanted_vs_has.png")
plt.close(fig)

# Numbers quoted in the write-up
for q in ("50", "90", "99"):
    i = int(np.searchsorted(s, pct[q]))
    j = int(np.searchsorted(s2, pct[q]))
    print(f"manual p{q}: s {pct[q]:.2f} current h/k/m/total {cur['h'][i]:.1f}/{cur['k'][i]:.1f}/{cur['m'][i]:.1f}/{total(cur)[i]:.1f}; "
          f"no rule {nor['h'][j]:.1f}/{nor['k'][j]:.1f}/{nor['m'][j]:.1f}/{total(nor)[j]:.1f}; free {free['h'][i]:.1f}/{free['k'][i]:.1f}/{free['m'][i]:.1f}/{total(free)[i]:.1f}")
m2 = np.array(nor["m"]) > 0
print("no-rule users, s band:", round(float(s2[m2].min()), 2), round(float(s2[m2].max()), 2))
m1 = np.array(cur["m"]) > 0
print("current users, s band:", round(float(s[m1].min()), 2), round(float(s[m1].max()), 2))
print("survey wanted", {b: round(S["bins"][b]["wanted"], 2) for b in sb}, "all", round(S["all"]["wanted"], 2), round(S["all"]["eps"], 2))
print("model 2019 has", {b: round(T[b]["m_manual"], 2) for b in labs}, "wants", {b: round(T[b]["free_m"], 2) for b in labs})
print("model 2019 ratio free/quota", round(R["current_2019"]["binding"]["ratio_free_to_quota"], 2))
for nm in ("light", "manual"):
    print(nm, "share of plants current/no rule", round(CUR["who_uses"][nm], 4), round(NOR["who_uses"][nm], 4))
print("done")
