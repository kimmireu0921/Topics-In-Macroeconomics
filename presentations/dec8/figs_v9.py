"""Dec 8 figures from the v9 results and the data facts. Run from this folder: python3 figs_v9.py."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

E = "../../hopenhayn_project/eps_model/"
R = json.load(open(E + "results_v9.json"))
PE = json.load(open("../../bunching/premium_evidence.json"))
ML = json.load(open("mlfs_2026h1.json"))
BLUE, ORANGE, AQUA, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1baf7a", "#1F2A3C", "#5F6876", "#D8DEE8"
plt.rcParams.update({"font.family": "Arial", "font.size": 15, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "axes.axisbelow": True, "legend.frameon": False,
                     "savefig.dpi": 200, "savefig.facecolor": "white"})
C = R["changes"]

# 1. Hiring difficulty by size: survey unfilled Korean manual hires, MLFS shortage rate
fig, (a, b) = plt.subplots(1, 2, figsize=(16, 5.2))
lab = ["1-5", "6-10", "11-30", "31-50", "51+"]
v = [100 * PE["by_korean_workers"][k]["unfilled_manual_aggregate"] for k in ["1-5", "6-10", "11-30", "31-50", "51-plus"]]
bars = a.bar(lab, v, color=BLUE, width=0.6)
for r_, x in zip(bars, v):
    a.text(r_.get_x() + r_.get_width() / 2, x + 1, f"{x:.0f}%", ha="center", fontsize=14)
a.set_title("Planned Korean manual hires left unfilled\n(EPS survey 2019, by Korean workers)", loc="left", fontsize=16)
a.set_ylim(0, 70); a.grid(axis="x", visible=False)
ms = ML["manufacturing_by_size"]
labs = list(ms)
v2 = [ms[k]["shortage_rate"] for k in labs]
bars = b.bar(labs, v2, color=ORANGE, width=0.6)
for r_, x in zip(bars, v2):
    b.text(r_.get_x() + r_.get_width() / 2, x + 0.1, f"{x:.1f}%", ha="center", fontsize=14)
b.set_title("Labour shortage rate, all manufacturing plants\n(Ministry establishment survey 2026, by regular workers)", loc="left", fontsize=16)
b.set_ylim(0, 5); b.grid(axis="x", visible=False)
fig.tight_layout(w_pad=3); fig.savefig("fig_hiring.png"); plt.close(fig)

# 2. Why caps rarely bind: EPS workers a plant wants (all manual work) vs its legal cap
p = R["params"]
r = p["lamB"] ** (1 / (1 - p["rho"]))
h = np.arange(1, 151)
want = r * h
cap24 = np.select([h <= 10, h <= 50, h <= 100, h <= 150], [h + 10, np.minimum(30, 2 * h), 35, 40], 50)
cap19 = np.select([h <= 5, h <= 10, h <= 30, h <= 50, h <= 100, h <= 150], [5, 7, 10, 12, 15, 20], 25)
fig, ax = plt.subplots(figsize=(15, 5.4))
ax.plot(h, want, color=INK, lw=2.5, label=f"EPS workers a manual-intensive plant wants (≈ {r:.2f} × core Koreans)")
ax.step(h, cap24, where="post", color=BLUE, lw=2.5, label="2024 legal cap")
ax.step(h, cap19, where="post", color=ORANGE, lw=2.5, label="2019 legal cap")
x24 = int(h[np.argmax(want > cap24)]); x19 = int(h[np.argmax(want > cap19)])
for x, c, t in [(x24, BLUE, "2024 cap binds\nfrom about %d" % x24), (x19, ORANGE, "2019 cap binds\nfrom about %d" % x19)]:
    ax.axvline(x, color=c, ls=":", lw=1.5)
    ax.text(x + 2, 72 if c == BLUE else 55, t, color=c, fontsize=13)
ax.set_xlabel("Core Korean workers (no Korean manual workers)", fontsize=15)
ax.set_ylabel("EPS workers", fontsize=15)
ax.set_ylim(0, 85); ax.legend(loc="upper left", fontsize=14)
fig.tight_layout(); fig.savefig("fig_why_caps.png"); plt.close(fig)

# 3. Quota size and welfare
qs = sorted(C["quota"], key=float)
x = np.arange(len(qs) + 1)
labels = [f"×{q}" for q in qs[:2]] + ["today"] + [f"×{q}" for q in qs[2:]]
net = [100 * C["quota"][q]["net_Y"] for q in qs[:2]] + [0] + [100 * C["quota"][q]["net_Y"] for q in qs[2:]]
kw = [100 * C["quota"][q]["welfare_korean"] for q in qs[:2]] + [0] + [100 * C["quota"][q]["welfare_korean"] for q in qs[2:]]
fig, ax = plt.subplots(figsize=(15, 5.4))
W = 0.38
for vals, off, c, l in [(net, -W / 2, BLUE, "Net output (everyone)"), (kw, W / 2, AQUA, "Korean households' consumption")]:
    bars = ax.bar(x + off, vals, W - 0.04, color=c, label=l)
    for r_, vv in zip(bars, vals):
        if abs(vv) > 0.01:
            ax.text(r_.get_x() + r_.get_width() / 2, vv + (0.15 if vv > 0 else -0.45), f"{vv:+.1f}%", ha="center", fontsize=13)
ax.axhline(0, color=INK, lw=1)
ax.set_xticks(x, labels, fontsize=15); ax.set_xlabel("EPS quota relative to today (same rules)", fontsize=15)
ax.set_ylabel("Change vs today (%)", fontsize=15); ax.grid(axis="x", visible=False)
ax.legend(loc="upper left", fontsize=14)
fig.tight_layout(); fig.savefig("fig_quota.png"); plt.close(fig)

# 4. Summary: what each change is worth
items = [("Equal limit\n(no size link)", C["equal_vs_2024"]["net_Y"], C["equal_vs_2024"]["welfare_korean"]),
         ("Best cap tilt", max(v["net_Y"] for v in C["tilt"].values()), max(v["welfare_korean"] for v in C["tilt"].values())),
         ("Permit price\n(open access)", C["price_vs_2024"]["net_Y"], C["price_vs_2024"]["welfare_korean"]),
         ("Quota +25%", C["quota"]["1.25"]["net_Y"], C["quota"]["1.25"]["welfare_korean"])]
fig, ax = plt.subplots(figsize=(15, 5.4))
x = np.arange(len(items))
for vals, off, c, l in [([100 * i[1] for i in items], -W / 2, BLUE, "Net output (everyone)"), ([100 * i[2] for i in items], W / 2, AQUA, "Korean households' consumption")]:
    bars = ax.bar(x + off, vals, W - 0.04, color=c, label=l)
    for r_, vv in zip(bars, vals):
        ax.text(r_.get_x() + r_.get_width() / 2, vv + 0.03, "0.00%" if round(vv, 2) == 0 else f"{vv:+.2f}%", ha="center", fontsize=13)
ax.axhline(0, color=INK, lw=1)
ax.set_xticks(x, [i[0] for i in items], fontsize=15); ax.set_ylabel("Change vs today (%)", fontsize=15)
ax.grid(axis="x", visible=False); ax.legend(loc="upper left", fontsize=14)
fig.tight_layout(); fig.savefig("fig_summary.png"); plt.close(fig)
print("figures written; caps bind from", x24, "(2024) and", x19, "(2019) core Koreans")
